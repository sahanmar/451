import streamlit as st
from streamlit_agraph import Node, Edge

import pandas as pd

NODE_COLOUR_NON_DODGY = "#D1E2F8"
NODE_COLOUR_DODGY = "#F99292"
NODE_IMAGE_PERSON = "https://raw.githubusercontent.com/sahanmar/451/main/data/person_icon.png"  # https://www.flaticon.com/free-icon/user_747376
NODE_IMAGE_COMPANY = "https://raw.githubusercontent.com/sahanmar/451/main/data/company_icon.png"  # https://www.flaticon.com/free-icon/company_4812244


@st.cache()
def get_subgraph_df():
    subgraphs = pd.read_parquet(
        "./data/1m_networks.parquet", engine="pyarrow"
    ).set_index("network_id")
    return subgraphs


@st.cache()
def get_subgraph_nodes_df(subgraph_hash):
    nodes = pd.read_parquet(
        "./data/1m_nodes.parquet",
        filters=[[("subgraph_hash", "=", subgraph_hash)]],
        engine="pyarrow",
    )

    return nodes


@st.cache()
def get_subgraph_edges_df(subgraph_hash):
    return pd.read_parquet(
        "./data/1m_edges.parquet",
        filters=[[("subgraph_hash", "=", subgraph_hash)]],
        engine="pyarrow",
    )


@st.cache()
def get_subgraph_with_risk_score(
    subgraph_table,
    weight_cyclic,
    weight_company_ratio,
    weight_proxy_directors,
    weight_multi_jurisdiction,
    weight_tax_havens,
    weight_pep,
    weight_russian_pep,
):

    out = subgraph_table.copy()
    out["total_risk"] = (
        (out["cyclicity"] * weight_cyclic / out["cyclicity"].max())
        + (out["company_ratio"] * weight_company_ratio / out["company_ratio"].max())
        + (
            out["multi_jurisdiction"]
            * weight_multi_jurisdiction
            / out["multi_jurisdiction"].max()
        )
        + (out["tax_haven"] * weight_tax_havens / out["tax_haven"].max())
        + (out["proxy"] * weight_proxy_directors / out["proxy"].max())
        + (out["potential_pep_match"] * weight_pep / out["potential_pep_match"].max())
        + (
            out["potential_rus_pep_match"]
            * weight_russian_pep
            / out["potential_rus_pep_match"].max()
        )
    )
    return out.sort_values(by="total_risk", ascending=False).query("total_risk > 0")


def build_agraph_components(
    nodes,
    edges,
):
    """Create agraph object from node and edge list"""

    node_objects = []
    edge_objects = []

    for _, row in nodes.iterrows():

        node_features = parse_node_features(row)

        node_objects.append(
            Node(
                id=row["node_id"],
                label=node_features["name"],
                size=20,
                color=NODE_COLOUR_DODGY
                if node_features["is_dodgy"]
                else NODE_COLOUR_NON_DODGY,
                image=NODE_IMAGE_PERSON
                if node_features["is_person"]
                else NODE_IMAGE_COMPANY,
                shape="circularImage",
            )
        )

    for _, row in edges.iterrows():
        edge_objects.append(
            Edge(
                source=row["source"],
                label=row["type"][0],
                target=row["target"],
                smooth=True,
            )
        )

    return (node_objects, edge_objects)


@st.cache()
def build_markdown_strings_for_node(nodes_selected):
    """Separate into People and Company strings"""

    markdown_strings = dict()
    markdown_strings["companies"] = []
    markdown_strings["people"] = []

    for _, row in nodes_selected.iterrows():

        node_features = parse_node_features(row)

        if node_features["is_person"]:
            text = f"{node_features['name']} [{node_features['nationality']}/{node_features['yob']}/{node_features['mob']}]"
            key = "people"
        else:
            text = f"{node_features['name']} [{node_features['company_number']}/{node_features['country']}]"
            key = "companies"

        if node_features["is_proxy"]:
            text += "\n !! Proxy director !!"

        if node_features["is_pep"]:
            text += "\n !! Politically-exposed person !!"
            text += f"\n -> {row['politician_metadata']}"

        if node_features["is_rus_pep"]:
            text += "\n !! Russian politically-exposed person !!"
            text += f"\n -> {row['rus_politician_metadata']}"

        markdown_strings[key].append(f"```\n{text}")

    return markdown_strings


@st.cache()
def parse_node_features(row):
    out = dict()

    out["is_person"] = row["is_person"] == 1
    out["is_proxy"] = row["proxy_dir"] == 1
    out["is_pep"] = row["politician"] == 1
    out["is_rus_pep"] = row["rus_politician"] == 1
    out["is_dodgy"] = out["is_proxy"] or out["is_pep"] or out["is_rus_pep"]

    if row["node_metadata"]:
        node_metadata = row["node_metadata"]
    else:
        node_metadata = {"forenames": None, "surname": None, "name": None}

    if out["is_person"]:
        if node_metadata["forenames"] and node_metadata["surname"]:
            out["name"] = node_metadata["forenames"] + " " + node_metadata["surname"]
        else:
            out["name"] = row["node_id"]
    else:
        if node_metadata["name"]:
            out["name"] = node_metadata["name"]
        else:
            out["name"] = node_metadata["surname"]

    raw_metadata = row["node_metadata"] if row["node_metadata"] else {}
    raw_metadata = {k: v for k, v in raw_metadata.items() if v is not None}

    out["address"] = raw_metadata.get("address", "")
    out["country"] = raw_metadata.get("country", "")
    out["yob"] = raw_metadata.get("yob", "")
    out["mob"] = raw_metadata.get("mob", "")
    out["nationality"] = raw_metadata.get("nationality", "")
    out["company_number"] = raw_metadata.get("company_number", "")

    return out
