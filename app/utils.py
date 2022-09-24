import streamlit as st
from streamlit_agraph import Node, Edge
import json
import pandas as pd

NODE_COLOUR_NON_DODGY = "#72EF77"
NODE_COLOUR_DODGY = "#F63333"
NODE_IMAGE_PERSON = "http://i.ibb.co/LrY3tfw/747376.png"  # https://www.flaticon.com/free-icon/user_747376
NODE_IMAGE_COMPANY = "http://i.ibb.co/fx6r1dZ/4812244.png"  # https://www.flaticon.com/free-icon/company_4812244


@st.cache()
def get_subgraph_df():
    return pd.read_parquet("./data/network.parquet", engine="pyarrow").set_index(
        "network_id"
    )


@st.cache()
def get_subgraph_nodes_df(subgraph_hash):
    return pd.read_parquet(
        "./data/nodes.parquet",
        filters=[[("subgraph_hash", "=", subgraph_hash)]],
        engine="pyarrow",
    )


@st.cache()
def get_subgraph_edges_df(subgraph_hash):
    return pd.read_parquet(
        "./data/edges.parquet",
        filters=[[("subgraph_hash", "=", subgraph_hash)]],
        engine="pyarrow",
    )


def get_subgraph_with_risk_score(
    subgraph_table,
    weight_chains,
    weight_cyclic,
    weight_psc_haven,
    weight_pep,
    weight_sanctions,
    weight_disqualified,
):

    out = subgraph_table.copy()
    out["total_risk"] = out["cyclicity"] * weight_cyclic / out["cyclicity"].max()
    return out.sort_values(by="total_risk", ascending=False)


def build_agraph_components(
    nodes,
    edges,
):
    """Create agraph object from node and edge list"""

    node_objects = []
    edge_objects = []

    for _, row in nodes.iterrows():
        # node_metadata = json.loads(row["node_metadata"])
        node_objects.append(
            Node(
                id=row["node_id"],
                label="\n".join(row["node_id"].split("|")[0].split(" ")),
                size=20,
                # color=NODE_COLOUR_DODGY
                # if (row["pep"] > 0 or row["sanction"] > 0)
                # else NODE_COLOUR_NON_DODGY,
                image=NODE_IMAGE_PERSON,
                # if row["is_person"] == 1
                # else NODE_IMAGE_COMPANY,
                shape="circularImage",
            )
        )

    for _, row in edges.iterrows():
        edge_objects.append(
            Edge(
                source=row["source"],
                # label=row["type"][0],
                target=row["target"],
            )
        )

    return (node_objects, edge_objects)


def build_markdown_strings_for_node(nodes_selected):
    """Separate into People and Company strings"""

    markdown_strings = dict()
    markdown_strings["companies"] = []
    markdown_strings["people"] = []

    for _, row in nodes_selected.iterrows():
        node_metadata = {
            "name": row["node_id"],
            "is_proxy": row["proxy_dir"],
            "is_person": True,
        }

        # node_metadata = json.loads(row["node_metadata"])
        # node_sanctions = (
        #     "" if row["sanction"] == 0 else f"! SANCTIONED: {row['sanction_metadata']}"
        # )
        # node_pep = "" if row["pep"] == 0 else f"! PEP: {row['pep_metadata']}"

        node_sanctions = ""
        node_pep = ""

        if node_metadata["is_person"]:
            # node_title = f"{node_metadata['name']} [{node_metadata['nationality']}/{node_metadata['yob']}/{node_metadata['mob']}]"
            node_title = f"{node_metadata['name']}"
            key = "people"
        else:
            # node_title = f"{node_metadata['name']} [{row['jur']}/{node_metadata['reg']}/{node_metadata['address']}]"
            node_title = f"{node_metadata['name']}"
            key = "companies"

        markdown_strings[key].append(
            "\n".join(
                [x for x in ["```", node_title, node_pep, node_sanctions] if len(x) > 0]
            )
        )

    return markdown_strings
