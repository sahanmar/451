from curses import use_default_colors
import streamlit as st
from streamlit_agraph import Node, Edge
import json
import pandas as pd

NODE_COLOUR_NON_DODGY = "#72EF77"
NODE_COLOUR_DODGY = "#EF7272"
NODE_IMAGE_PERSON = "http://i.ibb.co/LrY3tfw/747376.png"  # https://www.flaticon.com/free-icon/user_747376
NODE_IMAGE_COMPANY = "http://i.ibb.co/fx6r1dZ/4812244.png"  # https://www.flaticon.com/free-icon/company_4812244

# @st.cache()
def get_subgraph_df():
    return pd.read_csv("./data/subgraphs.csv", index_col="subgraph_hash")


# @st.cache()
def get_nodes_df():
    return pd.read_csv("./data/nodes.csv")


# @st.cache()
def get_edges_df():
    return pd.read_csv("./data/edges.csv")


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
    out["total_risk"] = (
        (out["cyclicity"] * weight_cyclic / out["cyclicity"].max())
        + (
            out["multi_jurisdiction"]
            * weight_psc_haven
            / out["multi_jurisdiction"].max()
        )
        + (out["num_sanctions"] * weight_sanctions / out["num_sanctions"].max())
        + (out["num_peps"] * weight_pep / out["num_peps"].max())
    )
    return out.sort_values(by="total_risk", ascending=False)


def build_agraph_components(
    nodes,
    edges,
):
    """Create agraph object from node and edge list"""

    node_objects = []
    edge_objects = []

    for _, row in nodes.iterrows():
        node_metadata = json.loads(row["node_metadata"])
        node_objects.append(
            Node(
                id=row["node_id"],
                label=node_metadata["name"],
                size=25,
                color=NODE_COLOUR_DODGY
                if (row["pep"] > 0 or row["sanction"] > 0)
                else NODE_COLOUR_NON_DODGY,
                image=NODE_IMAGE_PERSON
                if row["is_person"] == 1
                else NODE_IMAGE_COMPANY,
                shape="circularImage",
            )
        )

    for _, row in edges.iterrows():
        edge_objects.append(
            Edge(
                source=row["source"],
                label=row["type"],
                target=row["target"],
            )
        )

    return (node_objects, edge_objects)
