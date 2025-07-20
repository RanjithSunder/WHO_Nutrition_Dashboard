import streamlit as st
import pandas as pd
import plotly.express as px

def show_data_quality(df_obesity, df_malnutrition):
    st.header("🔍 Data Quality Assessment")

    # Missing values analysis
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Missing Values - Obesity")
        missing_obesity = df_obesity.isnull().sum()
        fig = px.bar(x=missing_obesity.index, y=missing_obesity.values,
                     title="Missing Values in Obesity Dataset")
        st.plotly_chart(fig, use_container_width=True)

        st.write("**Missing Values Summary:**")
        st.dataframe(missing_obesity)

    with col2:
        st.subheader("Missing Values - Malnutrition")
        missing_malnutrition = df_malnutrition.isnull().sum()
        fig = px.bar(x=missing_malnutrition.index, y=missing_malnutrition.values,
                     title="Missing Values in Malnutrition Dataset")
        st.plotly_chart(fig, use_container_width=True)

        st.write("**Missing Values Summary:**")
        st.dataframe(missing_malnutrition)

    # Data distribution analysis
    st.subheader("Data Distribution Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Obesity Data Distribution:**")
        fig = px.histogram(df_obesity, x='Mean_Estimate', nbins=30,
                           title="Distribution of Obesity Estimates")
        st.plotly_chart(fig, use_container_width=True)

        # Outlier detection
        Q1 = df_obesity['Mean_Estimate'].quantile(0.25)
        Q3 = df_obesity['Mean_Estimate'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = df_obesity[(df_obesity['Mean_Estimate'] < lower_bound) |
                              (df_obesity['Mean_Estimate'] > upper_bound)]

        st.write(f"**Outliers detected:** {len(outliers)}")
        if len(outliers) > 0:
            st.dataframe(outliers[['Country', 'Year', 'Mean_Estimate']].head(10))

    with col2:
        st.write("**Malnutrition Data Distribution:**")
        fig = px.histogram(df_malnutrition, x='Mean_Estimate', nbins=30,
                           title="Distribution of Malnutrition Estimates")
        st.plotly_chart(fig, use_container_width=True)

        # Outlier detection
        Q1 = df_malnutrition['Mean_Estimate'].quantile(0.25)
        Q3 = df_malnutrition['Mean_Estimate'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = df_malnutrition[(df_malnutrition['Mean_Estimate'] < lower_bound) |
                                   (df_malnutrition['Mean_Estimate'] > upper_bound)]

        st.write(f"**Outliers detected:** {len(outliers)}")
        if len(outliers) > 0:
            st.dataframe(outliers[['Country', 'Year', 'Mean_Estimate']].head(10))

    # Confidence interval analysis
    st.subheader("Confidence Interval Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Obesity CI Width Distribution:**")
        fig = px.box(df_obesity, y='CI_Width', title="Obesity Confidence Interval Width")
        st.plotly_chart(fig, use_container_width=True)

        # Countries with highest CI width
        high_ci_obesity = df_obesity.groupby('Country')['CI_Width'].mean().sort_values(ascending=False).head(10)
        st.write("**Countries with Highest CI Width:**")
        st.dataframe(high_ci_obesity)

    with col2:
        st.write("**Malnutrition CI Width Distribution:**")
        fig = px.box(df_malnutrition, y='CI_Width', title="Malnutrition Confidence Interval Width")
        st.plotly_chart(fig, use_container_width=True)

        # Countries with highest CI width
        high_ci_malnutrition = df_malnutrition.groupby('Country')['CI_Width'].mean().sort_values(ascending=False).head(
            10)
        st.write("**Countries with Highest CI Width:**")
        st.dataframe(high_ci_malnutrition)

    # Data completeness by country
    st.subheader("Data Completeness by Country")

    # Calculate completeness
    total_years = 11  # 2012-2022

    obesity_completeness = df_obesity.groupby('Country').size() / total_years * 100
    malnutrition_completeness = df_malnutrition.groupby('Country').size() / total_years * 100

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Obesity Data Completeness:**")
        fig = px.histogram(x=obesity_completeness.values, nbins=20,
                           title="Obesity Data Completeness (%)")
        st.plotly_chart(fig, use_container_width=True)

        incomplete_countries = obesity_completeness[obesity_completeness < 50].sort_values()
        if len(incomplete_countries) > 0:
            st.write("**Countries with <50% completeness:**")
            st.dataframe(incomplete_countries.head(10))

    with col2:
        st.write("**Malnutrition Data Completeness:**")
        fig = px.histogram(x=malnutrition_completeness.values, nbins=20,
                           title="Malnutrition Data Completeness (%)")
        st.plotly_chart(fig, use_container_width=True)

        incomplete_countries = malnutrition_completeness[malnutrition_completeness < 50].sort_values()
        if len(incomplete_countries) > 0:
            st.write("**Countries with <50% completeness:**")
            st.dataframe(incomplete_countries.head(10))