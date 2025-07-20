import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def show_insights_recommendations(df_obesity, df_malnutrition):
    st.header("💡 Insights & Recommendations")

    # Key insights
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.subheader("🔍 Key Insights")

    # Calculate key statistics
    global_obesity_trend = df_obesity[df_obesity['Country'] == 'Global'].groupby('Year')['Mean_Estimate'].mean()
    global_malnutrition_trend = df_malnutrition[df_malnutrition['Country'] == 'Global'].groupby('Year')[
        'Mean_Estimate'].mean()

    if len(global_obesity_trend) > 1:
        obesity_change = global_obesity_trend.iloc[-1] - global_obesity_trend.iloc[0]
        malnutrition_change = global_malnutrition_trend.iloc[-1] - global_malnutrition_trend.iloc[0]

        st.write(f"**1. Global Trends (2012-2022):**")
        st.write(
            f"   - Global obesity has {'increased' if obesity_change > 0 else 'decreased'} by {abs(obesity_change):.2f}%")
        st.write(
            f"   - Global malnutrition has {'increased' if malnutrition_change > 0 else 'decreased'} by {abs(malnutrition_change):.2f}%")

    # Regional insights
    regional_obesity = df_obesity.groupby('Region')['Mean_Estimate'].mean().sort_values(ascending=False)
    regional_malnutrition = df_malnutrition.groupby('Region')['Mean_Estimate'].mean().sort_values(ascending=False)

    st.write(f"**2. Regional Disparities:**")
    st.write(f"   - Highest obesity rates: {regional_obesity.index[0]} ({regional_obesity.iloc[0]:.2f}%)")
    st.write(
        f"   - Highest malnutrition rates: {regional_malnutrition.index[0]} ({regional_malnutrition.iloc[0]:.2f}%)")

    # Demographic insights
    gender_obesity = df_obesity[df_obesity['Gender'].isin(['Male', 'Female'])].groupby('Gender')['Mean_Estimate'].mean()
    gender_malnutrition = df_malnutrition[df_malnutrition['Gender'].isin(['Male', 'Female'])].groupby('Gender')[
        'Mean_Estimate'].mean()

    st.write(f"**3. Gender Patterns:**")
    if len(gender_obesity) == 2:
        if gender_obesity['Female'] > gender_obesity['Male']:
            st.write(
                f"   - Obesity: Women have higher rates ({gender_obesity['Female']:.2f}% vs {gender_obesity['Male']:.2f}%)")
        else:
            st.write(
                f"   - Obesity: Men have higher rates ({gender_obesity['Male']:.2f}% vs {gender_obesity['Female']:.2f}%)")

    if len(gender_malnutrition) == 2:
        if gender_malnutrition['Female'] > gender_malnutrition['Male']:
            st.write(
                f"   - Malnutrition: Women have higher rates ({gender_malnutrition['Female']:.2f}% vs {gender_malnutrition['Male']:.2f}%)")
        else:
            st.write(
                f"   - Malnutrition: Men have higher rates ({gender_malnutrition['Male']:.2f}% vs {gender_malnutrition['Female']:.2f}%)")

    # Age group insights
    age_obesity = df_obesity.groupby('age_group')['Mean_Estimate'].mean()
    age_malnutrition = df_malnutrition.groupby('age_group')['Mean_Estimate'].mean()

    st.write(f"**4. Age Group Patterns:**")
    if 'Adult' in age_obesity.index and 'Child/Adolescent' in age_obesity.index:
        if age_obesity['Adult'] > age_obesity['Child/Adolescent']:
            st.write(
                f"   - Obesity: Adults more affected ({age_obesity['Adult']:.2f}% vs {age_obesity['Child/Adolescent']:.2f}%)")
        else:
            st.write(
                f"   - Obesity: Children/Adolescents more affected ({age_obesity['Child/Adolescent']:.2f}% vs {age_obesity['Adult']:.2f}%)")

    st.markdown('</div>', unsafe_allow_html=True)

    # Recommendations
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.subheader("🎯 Recommendations")

    st.write("**1. Immediate Actions:**")
    st.write("   - Implement targeted interventions in high-risk regions")
    st.write("   - Develop gender-specific nutrition programs")
    st.write("   - Establish early childhood nutrition initiatives")
    st.write("   - Create public awareness campaigns")

    st.write("**2. Policy Recommendations:**")
    st.write("   - Strengthen food security policies")
    st.write("   - Implement sugar and fat taxation")
    st.write("   - Improve school nutrition programs")
    st.write("   - Regulate food advertising")

    st.write("**3. Data & Monitoring:**")
    st.write("   - Improve data collection consistency")
    st.write("   - Reduce confidence intervals in estimates")
    st.write("   - Establish real-time monitoring systems")
    st.write("   - Enhance cross-country data sharing")

    st.write("**4. Long-term Strategies:**")
    st.write("   - Integrate nutrition into healthcare systems")
    st.write("   - Develop sustainable food systems")
    st.write("   - Address socioeconomic determinants")
    st.write("   - Foster international cooperation")

    st.markdown('</div>', unsafe_allow_html=True)

    # Interactive risk assessment
    st.subheader("🎯 Risk Assessment Tool")

    col1, col2 = st.columns(2)

    with col1:
        selected_region = st.selectbox("Select Region:", df_obesity['Region'].unique())
        selected_gender = st.selectbox("Select Gender:", ['Both', 'Male', 'Female'])
        selected_age = st.selectbox("Select Age Group:", df_obesity['age_group'].unique())

    with col2:
        # Calculate risk based on selections
        filter_conditions = (df_obesity['Region'] == selected_region) & (df_obesity['age_group'] == selected_age)

        if selected_gender != 'Both':
            filter_conditions &= (df_obesity['Gender'] == selected_gender)

        filtered_data = df_obesity[filter_conditions]

        if len(filtered_data) > 0:
            avg_obesity = filtered_data['Mean_Estimate'].mean()
            risk_level = "High" if avg_obesity >= 25 else "Moderate" if avg_obesity >= 15 else "Low"

            st.metric("Average Obesity Rate", f"{avg_obesity:.2f}%")
            st.metric("Risk Level", risk_level)

            # Risk interpretation
            if risk_level == "High":
                st.error("🚨 High risk - Immediate intervention required")
            elif risk_level == "Moderate":
                st.warning("⚠️ Moderate risk - Preventive measures recommended")
            else:
                st.success("✅ Low risk - Continue monitoring")

    # Download options
    st.subheader("📥 Download Data")

    col1, col2 = st.columns(2)

    with col1:
        csv_obesity = df_obesity.to_csv(index=False)
        st.download_button(
            label="Download Obesity Data (CSV)",
            data=csv_obesity,
            file_name="who_obesity_data.csv",
            mime="text/csv"
        )

    with col2:
        csv_malnutrition = df_malnutrition.to_csv(index=False)
        st.download_button(
            label="Download Malnutrition Data (CSV)",
            data=csv_malnutrition,
            file_name="who_malnutrition_data.csv",
            mime="text/csv"
        )