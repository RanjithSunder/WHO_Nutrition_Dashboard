import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def show_regional_analysis(df_obesity, df_malnutrition):
    st.header("🌍 Regional Analysis")

    # Regional averages
    regional_obesity = df_obesity.groupby('Region')['Mean_Estimate'].mean().sort_values(ascending=False)
    regional_malnutrition = df_malnutrition.groupby('Region')['Mean_Estimate'].mean().sort_values(ascending=False)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Average Obesity by Region")
        fig = px.bar(x=regional_obesity.index, y=regional_obesity.values,
                     title="Average Obesity by Region")
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Average Malnutrition by Region")
        fig = px.bar(x=regional_malnutrition.index, y=regional_malnutrition.values,
                     title="Average Malnutrition by Region", color_discrete_sequence=['red'])
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

    # Regional trends over time
    st.subheader("Regional Trends Over Time")

    # Get available regions from the data
    available_regions = df_obesity['Region'].unique().tolist()

    # Create a safe default selection from available regions
    default_regions = []
    possible_defaults = ['Africa', 'Americas Region', 'Europe', 'AMR', 'EUR', 'AFR']

    for region in possible_defaults:
        if region in available_regions:
            default_regions.append(region)
        if len(default_regions) >= 3:  # Limit to 3 default selections
            break

    # If no matches found, use the first 3 available regions
    if not default_regions:
        default_regions = available_regions[:3]

    selected_regions = st.multiselect(
        "Select regions to compare:",
        available_regions,
        default=default_regions
    )

    if selected_regions:
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Obesity Trends by Region', 'Malnutrition Trends by Region')
        )

        # Obesity trends
        for region in selected_regions:
            region_data = df_obesity[df_obesity['Region'] == region].groupby('Year')['Mean_Estimate'].mean()
            fig.add_trace(
                go.Scatter(x=region_data.index, y=region_data.values,
                           mode='lines+markers', name=f'Obesity - {region}'),
                row=1, col=1
            )

        # Malnutrition trends
        for region in selected_regions:
            region_data = df_malnutrition[df_malnutrition['Region'] == region].groupby('Year')['Mean_Estimate'].mean()
            fig.add_trace(
                go.Scatter(x=region_data.index, y=region_data.values,
                           mode='lines+markers', name=f'Malnutrition - {region}'),
                row=1, col=2
            )

        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

    # Regional comparison table
    st.subheader("Regional Comparison Table")

    regional_comparison = pd.DataFrame({
        'Region': regional_obesity.index,
        'Avg_Obesity': regional_obesity.values,
        'Avg_Malnutrition': [regional_malnutrition.get(region, 0) for region in regional_obesity.index]
    })

    st.dataframe(regional_comparison)
