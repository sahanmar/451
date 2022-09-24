import streamlit as st
from streamlit_agraph import Node, Edge
import json
import pandas as pd

NODE_COLOUR_PERSON = "#4684B2"
NODE_COLOUR_COMPANY = "#46B247"


@st.cache()
def get_subgraph_df():
    return pd.read_csv("subgraphs.csv", index_col="subgraph_hash")


@st.cache()
def get_nodes_df():
    return pd.read_csv("nodes.csv")


@st.cache()
def get_edges_df():
    return pd.read_csv("edges.csv")


@st.cache()
def build_agraph_components(
    nodes,
    edges,
    node_colour_person=NODE_COLOUR_PERSON,
    node_colour_company=NODE_COLOUR_COMPANY,
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
                color=node_colour_person
                if row["is_person"] == 1
                else node_colour_company,
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
