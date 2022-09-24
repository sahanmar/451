import streamlit as st
from streamlit_agraph import agraph, Config
from utils import (
    build_agraph_components,
    get_edges_df,
    get_subgraph_df,
    get_nodes_df,
    get_subgraph_with_risk_score,
)


st.set_page_config(layout="wide")


SLIDER_MIN = 0
SLIDER_MAX = 100
SLIDER_DEFAULT = 50
DEFAULT_NUM_SUBGRAPHS_TO_SHOW = 3

nodes = get_nodes_df()
edges = get_edges_df()
subgraphs = get_subgraph_df()

with st.sidebar:
    st.title("Corporate risks")

    weight_chains = (
        st.slider(
            "Long ownership chains",
            min_value=SLIDER_MIN,
            max_value=SLIDER_MAX,
            value=SLIDER_DEFAULT,
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
        )
        / SLIDER_MAX
    )
    weight_pep = (
        st.slider(
            "Officers/PSCs are politically exposed",
            min_value=SLIDER_MIN,
            max_value=SLIDER_MAX,
            value=SLIDER_DEFAULT,
        )
        / SLIDER_MAX
    )
    weight_sanctions = (
        st.slider(
            "Officers/PSCs/Companies are sanctioned",
            min_value=SLIDER_MIN,
            max_value=SLIDER_MAX,
            value=SLIDER_DEFAULT,
        )
        / SLIDER_MAX
    )
    weight_disqualified = (
        st.slider(
            "Officers are disqualified directors",
            min_value=SLIDER_MIN,
            max_value=SLIDER_MAX,
            value=SLIDER_DEFAULT,
        )
        / SLIDER_MAX
    )
    custom_names_a = st.multiselect(
        label="Custom persons of interest",
        options=nodes["node_id"],
        default=None,
    )
    custom_names_b = st.file_uploader(label="Custom persons of interest", type="csv")

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
    cols = st.columns(num_subgraphs_to_display)

    for c, subgraph_hash in enumerate(selected_subgraph_hashes):
        nodes_selected = nodes.loc[nodes["subgraph_hash"] == subgraph_hash]
        edges_selected = edges.loc[edges["subgraph_hash"] == subgraph_hash]

        with cols[c]:
            (node_objects, edge_objects) = build_agraph_components(
                nodes_selected, edges_selected
            )
            agraph(
                nodes=node_objects,
                edges=edge_objects,
                config=Config(
                    width=round(1080 / num_subgraphs_to_display),
                    height=200,
                ),
            )

            st.markdown("*People*")
            st.dataframe(
                nodes_selected.query("is_person == 1"),
                use_container_width=True,
            )

            st.markdown("*Companies*")
            st.dataframe(
                nodes_selected.query("is_person == 0"),
                use_container_width=True,
            )
