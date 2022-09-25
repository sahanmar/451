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
GRAPH_SIZE_RENDER_LIMIT = 50
subgraphs = get_subgraph_df()

with st.sidebar:
    st.title("451 Corporate Risk Miner")

    only_include_small_subnetworks = st.checkbox(
        f"Only include networks small enough to render (<{GRAPH_SIZE_RENDER_LIMIT} nodes)",
        value=True,
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
    weight_company_ratio = (
        st.slider(
            "High company:officer ratio",
            min_value=SLIDER_MIN,
            max_value=SLIDER_MAX,
            value=SLIDER_DEFAULT,
        )
        / SLIDER_MAX
    )
    weight_proxy_directors = (
        st.slider(
            "Presence of proxy directors",
            min_value=SLIDER_MIN,
            max_value=SLIDER_MAX,
            value=SLIDER_DEFAULT,
        )
        / SLIDER_MAX
    )
    weight_multi_jurisdiction = (
        st.slider(
            "Associated with multiple jurisdictions",
            min_value=SLIDER_MIN,
            max_value=SLIDER_MAX,
            value=SLIDER_DEFAULT,
        )
        / SLIDER_MAX
    )
    weight_tax_havens = (
        st.slider(
            "Associated with tax havens",
            min_value=SLIDER_MIN,
            max_value=SLIDER_MAX,
            value=SLIDER_DEFAULT,
        )
        / SLIDER_MAX
    )
    weight_pep = (
        st.slider(
            "Officers/PSCs are politically exposed persons",
            min_value=SLIDER_MIN,
            max_value=SLIDER_MAX,
            value=SLIDER_DEFAULT,
        )
        / SLIDER_MAX
    )
    weight_russian_pep = (
        st.slider(
            "Officers/PSCs are Russian politically exposed persons",
            min_value=SLIDER_MIN,
            max_value=SLIDER_MAX,
            value=SLIDER_DEFAULT,
        )
        / SLIDER_MAX
    )

with st.container():

    subgraph_with_risk_scores = get_subgraph_with_risk_score(
        subgraphs,
        weight_cyclic=weight_cyclic,
        weight_company_ratio=weight_company_ratio,
        weight_proxy_directors=weight_proxy_directors,
        weight_multi_jurisdiction=weight_multi_jurisdiction,
        weight_tax_havens=weight_tax_havens,
        weight_pep=weight_pep,
        weight_russian_pep=weight_russian_pep,
    )

    if only_include_small_subnetworks:
        subgraph_with_risk_scores = subgraph_with_risk_scores.query(
            "node_num < @GRAPH_SIZE_RENDER_LIMIT"
        )

    # Only show top 2000 networks
    subgraph_with_risk_scores = subgraph_with_risk_scores.head(2000)

    st.dataframe(
        data=subgraph_with_risk_scores,
        use_container_width=True,
    )

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
                            width=round(1920 / num_subgraphs_to_display),
                            height=GRAPH_PLOT_HEIGHT_PX,
                            nodeHighlightBehavior=True,
                            highlightColor="#F7A7A6",
                            directed=True,
                            collapsible=True,
                            physics={
                                "enabled": True,
                                "maxVelocity": 5,
                            },
                        ),
                    )
                else:
                    st.error("Subgraph is too large to render")

                # Build markdown strings for representing metadata on dodgy entities
                markdown_strings = build_markdown_strings_for_node(nodes_selected)

                st.markdown(":busts_in_silhouette: **People**")
                for p in markdown_strings["people"]:
                    st.markdown(p)

                st.markdown(":office: **Companies**")
                for c in markdown_strings["companies"]:
                    st.markdown(c)

                st.download_button(
                    "Download subnetwork",
                    nodes_selected.to_csv().encode("utf-8"),
                    file_name=f"{subgraph_hash}.csv",
                )
