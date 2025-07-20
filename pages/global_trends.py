import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go  # Add this import
from plotly.subplots import make_subplots

def show_global_trends(df_obesity, df_malnutrition):
    st.header("📈 Global Trends Over Time")

    # Global trends
    global_obesity = df_obesity[df_obesity['Country'] == 'Global'].groupby('Year')['Mean_Estimate'].mean()
    global_malnutrition = df_malnutrition[df_malnutrition['Country'] == 'Global'].groupby('Year')[
        'Mean_Estimate'].mean()

    # Create subplot
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Global Obesity Trend', 'Global Malnutrition Trend',
                        'Age Group Comparison - Obesity', 'Age Group Comparison - Malnutrition'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )

    # Global obesity trend
    fig.add_trace(
        go.Scatter(x=global_obesity.index, y=global_obesity.values,
                   mode='lines+markers', name='Global Obesity', line=dict(color='blue')),
        row=1, col=1
    )

    # Global malnutrition trend
    fig.add_trace(
        go.Scatter(x=global_malnutrition.index, y=global_malnutrition.values,
                   mode='lines+markers', name='Global Malnutrition', line=dict(color='red')),
        row=1, col=2
    )

    # Age group trends - Obesity
    age_obesity_trend = df_obesity.groupby(['Year', 'age_group'])['Mean_Estimate'].mean().reset_index()
    for age_group in age_obesity_trend['age_group'].unique():
        if pd.notna(age_group):
            data = age_obesity_trend[age_obesity_trend['age_group'] == age_group]
            fig.add_trace(
                go.Scatter(x=data['Year'], y=data['Mean_Estimate'],
                           mode='lines+markers', name=f'Obesity - {age_group}'),
                row=2, col=1
            )

    # Age group trends - Malnutrition
    age_malnutrition_trend = df_malnutrition.groupby(['Year', 'age_group'])['Mean_Estimate'].mean().reset_index()
    for age_group in age_malnutrition_trend['age_group'].unique():
        if pd.notna(age_group):
            data = age_malnutrition_trend[age_malnutrition_trend['age_group'] == age_group]
            fig.add_trace(
                go.Scatter(x=data['Year'], y=data['Mean_Estimate'],
                           mode='lines+markers', name=f'Malnutrition - {age_group}'),
                row=2, col=2
            )

    fig.update_layout(height=800, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

    # Trend analysis
    st.subheader("Trend Analysis")

    col1, col2 = st.columns(2)

    with col1:
        if len(global_obesity) > 1:
            obesity_change = global_obesity.iloc[-1] - global_obesity.iloc[0]
            st.metric("Global Obesity Change (2012-2022)", f"{obesity_change:.2f}%")

        # Year-over-year growth
        st.write("**Obesity Year-over-Year Growth:**")
        for i in range(1, len(global_obesity)):
            year = global_obesity.index[i]
            growth = global_obesity.iloc[i] - global_obesity.iloc[i - 1]
            st.write(f"{year}: {growth:.2f}%")

    with col2:
        if len(global_malnutrition) > 1:
            malnutrition_change = global_malnutrition.iloc[-1] - global_malnutrition.iloc[0]
            st.metric("Global Malnutrition Change (2012-2022)", f"{malnutrition_change:.2f}%")

        # Year-over-year growth
        st.write("**Malnutrition Year-over-Year Growth:**")
        for i in range(1, len(global_malnutrition)):
            year = global_malnutrition.index[i]
            growth = global_malnutrition.iloc[i] - global_malnutrition.iloc[i - 1]
            st.write(f"{year}: {growth:.2f}%")
