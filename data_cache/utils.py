import random
from tqdm import tqdm
import networkx as nx
from collections import defaultdict


TAX_HEAVENS = {
    'jersey',
    'luxembourg',
    'virgin islands, british',
    'cayman islands',
    'switzerland',
    'hong kong',
    'singapore',
    'guernsey',
    'bermuda',
    'seychelles',
    'united arab emirates',
    'marshall islands',
    'belize',
    "isle of man",
    "barbados",
    "panama",
    "bahamas",
    "saint lucia",
    "dominica",
}


class ProduceEntityResolution:
    def __init__(self, company_df, max_rand=10 ** 8, min_len=7):
        self.company_name_to_reg = {
            n.upper().strip(): r for n, r in zip(company_df.company_name, company_df.company_number)
        }
        self.max_rand = max_rand
        self.er_map = {}
        self.min_len = min_len

    def missing_entry_randomisation(self):
        return random.randint(0, self.max_rand)

    def get_person_identifier(self, forenames, surname, yob, mob):
        if not surname:
            return f"p|rand_{self.missing_entry_randomisation()}"
        if forenames is None or len(forenames) == 0:
            return f"p|rand_{self.missing_entry_randomisation()}"
        elif isinstance(forenames, list):
            name = " ".join(forenames).lower()
        else:
            name = forenames.lower()
        return f"p|{name} {surname.lower()}|{yob}|{mob}"

    def get_company_identifier(self, cname, cnum):
        if cnum and len(cnum) >= self.min_len:
            return f"c|{cnum}"
        if cname in self.company_name_to_reg:
            return f"c|{self.company_name_to_reg[cname]}"
        if len(cname) > self.min_len:
            return f"c|company_named_{cname}"
        return f"c|rand_{self.missing_entry_randomisation()}"

    def resolve_entities(self, company_df, officer_df, psc_company_df, psc_person_df):

        # Company ER
        inps = zip(company_df.mention_id, company_df.company_name, company_df.company_number)
        for mid, cname, cnum in tqdm(inps, desc="UKCH Company er map", total=company_df.shape[0]):
            self.er_map[mid] = self.get_company_identifier(cname, cnum)

        off_person_df = officer_df[~officer_df.is_corporate_body]
        inps = zip(
            off_person_df.mention_id,
            off_person_df.forenames,
            off_person_df.surname,
            off_person_df.yob,
            off_person_df.mob,
        )
        for mid, fs, cs, yob, mob in tqdm(inps, desc="Officer (person) er map", total=off_person_df.shape[0]):
            self.er_map[mid] = self.get_person_identifier(fs, cs, yob, mob)

        off_company_df = officer_df[officer_df.is_corporate_body]
        inps = zip(off_company_df.mention_id, off_company_df.surname)
        for mid, cname in tqdm(inps, desc="Officer (company) er map", total=off_company_df.shape[0]):
            self.er_map[mid] = self.get_company_identifier(cname, None)

        # PSC Company ER
        inps = zip(psc_company_df.mention_id, psc_company_df.name, psc_company_df.psc_derived_company_number)
        for mid, cname, cnum in tqdm(inps, desc="PSC (company) er map", total=psc_company_df.shape[0]):
            self.er_map[mid] = self.get_company_identifier(cname, cnum)

        # People of significant control [physical people] ER:
        inps = zip(
            psc_person_df.mention_id,
            psc_person_df.name_elements_forename,
            psc_person_df.name_elements_middle_name,
            psc_person_df.name_elements_surname,
            psc_person_df.date_of_birth_year,
            psc_person_df.date_of_birth_month,
        )
        for mid, cf, cm, cs, yob, mob in tqdm(inps, desc="PSC (person) er map", total=psc_person_df.shape[0]):
            forenames = [x for x in [cf, cm] if x is not None]
            self.er_map[mid] = self.get_person_identifier(forenames, cs, yob, mob)


class GraphBuilder:
    def __init__(self):
        self.G = nx.DiGraph()
        self.G_undir = nx.Graph()
        self.CCs = []
        self.ccs_len = []
        self.hash_to_subn_map = {}

    def build_G(self, per, psc_company_df, psc_person_df, officer_df):
        for target_eid, source_mid in tqdm(zip(psc_company_df.company_number, psc_company_df.mention_id),
                                           desc="PSC company graph"):
            self.G_undir.add_edge(per.er_map[source_mid], f"c|{target_eid}", edge_type="own")

        for target_eid, source_mid in tqdm(zip(psc_person_df.company_number, psc_person_df.mention_id),
                                           desc="PSC person graph"):
            self.G_undir.add_edge(per.er_map[source_mid], f"c|{target_eid}", edge_type="own")

        for target_eid, source_mid in tqdm(zip(officer_df.company_number, officer_df.mention_id), desc="Officer graph"):
            self.G_undir.add_edge(per.er_map[source_mid], f"c|{target_eid}", edge_type="control")

    def get_neigh(self, nodes, radius=2):
        nodes = set([n for n in nodes if n in self.G_undir])
        for node in list(nodes):
            neighbors = set(self.G_undir.neighbors(node))
            neighbors = set([x for x in neighbors if isinstance(x, str)])
            nodes = nodes.union(neighbors)
        return nodes if radius == 1 else self.get_neigh(nodes, radius - 1)

    def build(self, per, psc_company_df, psc_person_df, officer_df):
        self.build_G(per, psc_company_df, psc_person_df, officer_df)
        self.CCs = sorted(nx.connected_components(self.G_undir), key=len, reverse=True)
        self.ccs_len = [len(c) for c in self.CCs]
        print(f"Top 10 Connected component sizes: {self.ccs_len[:10]}")

    @staticmethod
    def hash_subnetwork(nodes: iter):
        return sum(hash(n) % 2 ** 32 for n in nodes)

    def break_into_subgraphs(self, max_size=1000):
        for cc in self.CCs:
            # Small connected components go in as they are:
            if len(cc) < max_size:
                subnetwork_hash = self.hash_subnetwork(cc)
                self.hash_to_subn_map[subnetwork_hash] = cc
            # Giant component gets added by unique neighbourhoods
            else:
                size_before = len(self.hash_to_subn_map)
                extra_nodes = 0
                for node in tqdm(cc, desc=f"Breaking down Giant CC (size {len(cc)})"):
                    subnetwork = self.get_neigh([node])
                    subnetwork_hash = self.hash_subnetwork(subnetwork)
                    if subnetwork_hash not in self.hash_to_subn_map:
                        self.hash_to_subn_map[subnetwork_hash] = subnetwork
                        extra_nodes += len(subnetwork)
                print(f"""Giant Component of size {len(cc)} was broken down.
    Added {len(self.hash_to_subn_map) - size_before} neighbourhoods, 
    Sum of all nodes = {extra_nodes}
    Overhead ratio={extra_nodes / len(cc)}
""")


class NodeDescriber:
    def __init__(self, per):
        self.per = per
        self.node_to_jurs = defaultdict(set)
        self.node_to_names = {}
        self.node_to_metadata = {}
        self.metadata_cols = {
            "company": ["mention_id", "name", "industry_code", "company_number", "country", "address"],
            "psc_person": ["mention_id", "name", "nationality", "address_postal_code", "date_of_birth_year",
                           "date_of_birth_month"],
            "psc_company": ["mention_id", "name", "psc_derived_company_number", "combined_address", "address_country",
                            "kind"],
            "officer_person": ["mention_id", "forenames", "surname", "nationality", "yob", "mob"],
            "officer_company": ["mention_id", "surname", "country", 'appointment_role', 'post_town', 'postal_code'],
        }

    def unify_jur(self, c):
        if c is None:
            return None
        if c in ['england', 'wales', 'northern ireland', 'scotland', "uk"]:
            return 'united kingdom'
        if c in ["usa", "united states", "united states of america"]:
            return "united states"
        if c in ["british virgin islands", "virgin islands, british", "virgin islands"]:
            return "virgin islands, british"
        return c

    def add_node_to_names(self):
        for eid in set(self.per.er_map.values()):
            if eid.startswith("p|"):
                self.node_to_names[eid] = eid.split("|")[1]

    def add_dataset_metadata(self, df, dataset_name):
        c = self.metadata_cols[dataset_name]
        inp = zip(df[c[0]], df[c[1]], df[c[2]], df[c[3]], df[c[4]], df[c[5]])
        for tpl in tqdm(inp, desc=dataset_name, total=df.shape[0]):
            eid = self.per.er_map[tpl[0]]
            if eid not in self.node_to_metadata:
                self.node_to_metadata[eid] = {}
                for col_inx in range(1, len(c)):
                    col = self.metadata_cols[dataset_name][col_inx]
                    self.node_to_metadata[eid][col] = tpl[col_inx]
                    if col in ["country", "address_country", "reg_address_country"]:
                        if isinstance(tpl[col_inx], str):
                            unified_jur = self.unify_jur(tpl[col_inx].lower())
                            self.node_to_jurs[eid].add(unified_jur)

    def add_metadata(self, company_df, officer_df, psc_company_df, psc_person_df):
        self.add_dataset_metadata(company_df, "company")
        self.add_dataset_metadata(officer_df[~officer_df.is_corporate_body], "officer_person")
        self.add_dataset_metadata(officer_df[officer_df.is_corporate_body], "officer_company")
        self.add_dataset_metadata(psc_person_df, "psc_person")
        self.add_dataset_metadata(psc_company_df, "psc_company")
        self.add_node_to_names()
