import json
import pandas as pd
import streamlit as st
from streamlit_agraph import agraph, Config
from utils import (
    build_agraph_components,
    get_subgraph_nodes_df,
    get_subgraph_df,
    get_subgraph_edges_df,
    get_subgraph_with_risk_score,
    build_markdown_strings_for_node,
)


st.set_page_config(layout="wide")


SLIDER_MIN = 0
SLIDER_MAX = 100
SLIDER_DEFAULT = 50
DEFAULT_NUM_SUBGRAPHS_TO_SHOW = 3
GRAPH_PLOT_HEIGHT_PX = 400
GRAPH_SIZE_RENDER_LIMIT = 40
subgraphs = get_subgraph_df()

with st.sidebar:
    st.title("451 Corporate Risk Miner")

    weight_chains = (
        st.slider(
            "Long ownership chains",
            min_value=SLIDER_MIN,
            max_value=SLIDER_MAX,
            value=SLIDER_DEFAULT,
            disabled=True,
        )
        / SLIDER_MAX
    )
    weight_cyclic = (
        st.slider(
            "Cyclic ownership",
            min_value=SLIDER_MIN,
            max_value=SLIDER_MAX,
            value=SLIDER_DEFAULT,
        )
        / SLIDER_MAX
    )
    weight_psc_haven = (
        st.slider(
            "Persons of significant control associated with tax havens",
            min_value=SLIDER_MIN,
            max_value=SLIDER_MAX,
            value=SLIDER_DEFAULT,
            disabled=True,
        )
        / SLIDER_MAX
    )
    weight_pep = (
        st.slider(
            "Officers/PSCs are politically exposed",
            min_value=SLIDER_MIN,
            max_value=SLIDER_MAX,
            value=SLIDER_DEFAULT,
            disabled=True,
        )
        / SLIDER_MAX
    )
    weight_sanctions = (
        st.slider(
            "Officers/PSCs/Companies are sanctioned",
            min_value=SLIDER_MIN,
            max_value=SLIDER_MAX,
            value=SLIDER_DEFAULT,
            disabled=True,
        )
        / SLIDER_MAX
    )
    weight_disqualified = (
        st.slider(
            "Officers are disqualified directors",
            min_value=SLIDER_MIN,
            max_value=SLIDER_MAX,
            value=SLIDER_DEFAULT,
            disabled=True,
        )
        / SLIDER_MAX
    )

    custom_names = st.file_uploader(
        label="Custom persons/companies of interest", type="csv"
    )

    if custom_names:
        custom_names = pd.read_csv(custom_names, header=None)[0].tolist()
        st.write(custom_names)

    go = st.button("Go")


with st.container():

    subgraph_with_risk_scores = get_subgraph_with_risk_score(
        subgraphs,
        weight_chains=weight_chains,
        weight_cyclic=weight_cyclic,
        weight_psc_haven=weight_psc_haven,
        weight_pep=weight_pep,
        weight_sanctions=weight_sanctions,
        weight_disqualified=weight_disqualified,
    )

    st.dataframe(data=subgraph_with_risk_scores, use_container_width=True)

    selected_subgraph_hashes = st.multiselect(
        label="Select corporate network(s) to explore",
        options=list(subgraph_with_risk_scores.index),
        default=list(
            subgraph_with_risk_scores.head(DEFAULT_NUM_SUBGRAPHS_TO_SHOW).index
        ),
    )


with st.container():
    num_subgraphs_to_display = len(selected_subgraph_hashes)

    if num_subgraphs_to_display > 0:
        cols = st.columns(num_subgraphs_to_display)

        for c, subgraph_hash in enumerate(selected_subgraph_hashes):
            nodes_selected = get_subgraph_nodes_df(subgraph_hash)
            edges_selected = get_subgraph_edges_df(subgraph_hash)

            with cols[c]:
                if len(nodes_selected) < GRAPH_SIZE_RENDER_LIMIT:
                    (node_objects, edge_objects) = build_agraph_components(
                        nodes_selected, edges_selected
                    )
                    agraph(
                        nodes=node_objects,
                        edges=edge_objects,
                        config=Config(
                            width=round(1080 / num_subgraphs_to_display),
                            height=GRAPH_PLOT_HEIGHT_PX,
                            nodeHighlightBehavior=True,
                            highlightColor="#F7A7A6",
                            directed=True,
                            collapsible=True,
                        ),
                    )
                else:
                    st.error("Subgraph is too large to render")

                # Build markdown strings for representing metadata
                markdown_strings = build_markdown_strings_for_node(nodes_selected)

                st.markdown(":busts_in_silhouette: **People**")
                for p in markdown_strings["people"]:
                    st.markdown(p)

                st.markdown(":office: **Companies**")
                for c in markdown_strings["companies"]:
                    st.markdown(c)
