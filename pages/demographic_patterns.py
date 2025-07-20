import streamlit as st
import pandas as pd
import plotly.express as px

def show_demographic_patterns(df_obesity, df_malnutrition):
    st.header("👥 Demographic Patterns")

    # Gender analysis
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Gender Distribution - Obesity")
        gender_obesity = df_obesity[df_obesity['Gender'].isin(['Male', 'Female'])].groupby('Gender')[
            'Mean_Estimate'].mean()

        if len(gender_obesity) > 0:
            gender_obesity_df = pd.DataFrame({
                'Gender': gender_obesity.index,
                'Mean_Estimate': gender_obesity.values
            })
            fig = px.bar(gender_obesity_df, x='Gender', y='Mean_Estimate',
                         title="Average Obesity by Gender")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No gender data available for obesity")

    with col2:
        st.subheader("Gender Distribution - Malnutrition")
        gender_malnutrition = df_malnutrition[df_malnutrition['Gender'].isin(['Male', 'Female'])].groupby('Gender')[
            'Mean_Estimate'].mean()

        if len(gender_malnutrition) > 0:
            gender_malnutrition_df = pd.DataFrame({
                'Gender': gender_malnutrition.index,
                'Mean_Estimate': gender_malnutrition.values
            })
            fig = px.bar(gender_malnutrition_df, x='Gender', y='Mean_Estimate',
                         title="Average Malnutrition by Gender", color_discrete_sequence=['red'])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No gender data available for malnutrition")

    # Age group analysis
    st.subheader("Age Group Distribution")

    col1, col2 = st.columns(2)

    with col1:
        age_obesity = df_obesity.groupby('age_group')['Mean_Estimate'].mean()
        if len(age_obesity) > 0:
            fig = px.pie(values=age_obesity.values, names=age_obesity.index,
                         title="Obesity Distribution by Age Group")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No age group data available for obesity")

    with col2:
        age_malnutrition = df_malnutrition.groupby('age_group')['Mean_Estimate'].mean()
        if len(age_malnutrition) > 0:
            fig = px.pie(values=age_malnutrition.values, names=age_malnutrition.index,
                         title="Malnutrition Distribution by Age Group")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No age group data available for malnutrition")

    # Box plots for variability
    st.subheader("Distribution Variability")

    col1, col2 = st.columns(2)

    with col1:
        if 'age_group' in df_obesity.columns and len(df_obesity) > 0:
            fig = px.box(df_obesity, x='age_group', y='Mean_Estimate',
                         title="Obesity Distribution by Age Group")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No data available for obesity box plot")

    with col2:
        if 'age_group' in df_malnutrition.columns and len(df_malnutrition) > 0:
            fig = px.box(df_malnutrition, x='age_group', y='Mean_Estimate',
                         title="Malnutrition Distribution by Age Group")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No data available for malnutrition box plot")
