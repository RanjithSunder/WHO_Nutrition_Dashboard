import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def show_country_comparison(df_obesity, df_malnutrition):
    st.header("🏳️ Country Comparison")

    # Country selection
    countries = df_obesity['Country'].unique()
    countries = [c for c in countries if
                 c not in ['Global', 'Low & Middle Income', 'High Income', 'Low Income', 'Upper Middle Income']]

    selected_countries = st.multiselect(
        "Select countries to compare:",
        countries,
        default=['India', 'United States', 'China', 'Brazil', 'Nigeria'][:min(5, len(countries))]
    )

    if selected_countries:
        # Country comparison charts
        col1, col2 = st.columns(2)

        with col1:
            country_obesity = df_obesity[df_obesity['Country'].isin(selected_countries)].groupby('Country')[
                'Mean_Estimate'].mean()
            fig = px.bar(x=country_obesity.index, y=country_obesity.values,
                         title="Average Obesity by Country")
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            country_malnutrition = \
            df_malnutrition[df_malnutrition['Country'].isin(selected_countries)].groupby('Country')[
                'Mean_Estimate'].mean()
            fig = px.bar(x=country_malnutrition.index, y=country_malnutrition.values,
                         title="Average Malnutrition by Country", color_discrete_sequence=['red'])
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)

        # Time series comparison
        st.subheader("Trends Over Time")

        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Obesity Trends', 'Malnutrition Trends')
        )

        for country in selected_countries:
            # Obesity trends
            country_obesity_trend = df_obesity[df_obesity['Country'] == country].groupby('Year')['Mean_Estimate'].mean()
            fig.add_trace(
                go.Scatter(x=country_obesity_trend.index, y=country_obesity_trend.values,
                           mode='lines+markers', name=f'Obesity - {country}'),
                row=1, col=1
            )

            # Malnutrition trends
            country_malnutrition_trend = df_malnutrition[df_malnutrition['Country'] == country].groupby('Year')[
                'Mean_Estimate'].mean()
            fig.add_trace(
                go.Scatter(x=country_malnutrition_trend.index, y=country_malnutrition_trend.values,
                           mode='lines+markers', name=f'Malnutrition - {country}'),
                row=1, col=2
            )

        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

        # Detailed comparison table
        st.subheader("Detailed Country Statistics")

        comparison_data = []
        for country in selected_countries:
            obesity_data = df_obesity[df_obesity['Country'] == country]
            malnutrition_data = df_malnutrition[df_malnutrition['Country'] == country]

            comparison_data.append({
                'Country': country,
                'Avg_Obesity': obesity_data['Mean_Estimate'].mean(),
                'Avg_Malnutrition': malnutrition_data['Mean_Estimate'].mean(),
                'Obesity_Std': obesity_data['Mean_Estimate'].std(),
                'Malnutrition_Std': malnutrition_data['Mean_Estimate'].std(),
                'Avg_CI_Width_Obesity': obesity_data['CI_Width'].mean(),
                'Avg_CI_Width_Malnutrition': malnutrition_data['CI_Width'].mean()
            })

        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df)
