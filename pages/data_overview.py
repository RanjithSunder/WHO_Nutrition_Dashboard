import streamlit as st
import pandas as pd
import plotly.express as px

def show_data_overview(df_obesity, df_malnutrition):
    st.header("📊 Data Overview")

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Obesity Records", f"{len(df_obesity):,}")
    with col2:
        st.metric("Malnutrition Records", f"{len(df_malnutrition):,}")
    with col3:
        st.metric("Countries", f"{df_obesity['Country'].nunique()}")
    with col4:
        st.metric("Years Covered", "2012-2022")

    # Dataset summaries
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Obesity Dataset")
        st.dataframe(df_obesity.describe())

        st.subheader("Obesity by Level")
        obesity_levels = df_obesity['obesity_level'].value_counts()
        fig = px.pie(values=obesity_levels.values, names=obesity_levels.index,
                     title="Distribution of Obesity Levels")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Malnutrition Dataset")
        st.dataframe(df_malnutrition.describe())

        st.subheader("Malnutrition by Level")
        malnutrition_levels = df_malnutrition['malnutrition_level'].value_counts()
        fig = px.pie(values=malnutrition_levels.values, names=malnutrition_levels.index,
                     title="Distribution of Malnutrition Levels")
        st.plotly_chart(fig, use_container_width=True)

    # Data preview
    st.subheader("Data Preview")
    tab1, tab2 = st.tabs(["Obesity Data", "Malnutrition Data"])

    with tab1:
        st.dataframe(df_obesity.head(20))

    with tab2:
        st.dataframe(df_malnutrition.head(20))
