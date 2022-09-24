import streamlit as st
import pandas as pd
from streamlit_agraph import agraph, Config
from utils import build_agraph_components, get_edges_df, get_subgraph_df, get_nodes_df


st.set_page_config(layout="wide")


SLIDER_MIN = 1
SLIDER_MAX = 100
SLIDER_DEFAULT = 50

nodes = get_nodes_df()
edges = get_edges_df()
subgraphs = get_subgraph_df()

with st.sidebar:
    st.title("Corporate risks")

    weight_chains = st.slider(
        "Long ownership chains",
        min_value=SLIDER_MIN,
        max_value=SLIDER_MAX,
        value=SLIDER_DEFAULT,
    )
    weight_cyclic = st.slider(
        "Cyclic ownership",
        min_value=SLIDER_MIN,
        max_value=SLIDER_MAX,
        value=SLIDER_DEFAULT,
    )
    weight_psc_haven = st.slider(
        "Persons of significant control associated with tax havens",
        min_value=SLIDER_MIN,
        max_value=SLIDER_MAX,
        value=SLIDER_DEFAULT,
    )
    weight_pep = st.slider(
        "Officers/PSCs are politically exposed",
        min_value=SLIDER_MIN,
        max_value=SLIDER_MAX,
        value=SLIDER_DEFAULT,
    )
    weight_sanctions = st.slider(
        "Officers/PSCs/Companies are sanctioned",
        min_value=SLIDER_MIN,
        max_value=SLIDER_MAX,
        value=SLIDER_DEFAULT,
    )
    weight_disqualified = st.slider(
        "Officers are disqualified directors",
        min_value=SLIDER_MIN,
        max_value=SLIDER_MAX,
        value=SLIDER_DEFAULT,
    )

    custom_names_a = st.multiselect(
        label="Custom persons of interest",
        options=nodes["node_id"],
        default=None,
    )
    custom_names_b = st.file_uploader(label="Custom persons of interest", type="csv")

    go = st.button("Go")


with st.container():
    st.write(subgraphs)

    selected_subgraph_hash = st.selectbox(
        label="Select subgraph to explore", options=subgraphs.index
    )

nodes_selected = nodes.loc[nodes["subgraph_hash"] == selected_subgraph_hash]
edges_selected = edges.loc[edges["subgraph_hash"] == selected_subgraph_hash]

with st.container():

    col1, col2 = st.columns(2)

    with col1:
        (node_objects, edge_objects) = build_agraph_components(
            nodes_selected, edges_selected
        )
        agraph(
            nodes=node_objects,
            edges=edge_objects,
            config=Config(
                width=500,
                height=500,
            ),
        )

    with col2:
        st.write(nodes_selected)
