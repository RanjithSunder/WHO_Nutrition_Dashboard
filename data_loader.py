import pandas as pd
import requests
import pycountry
import streamlit as st
import numpy as np
from datetime import datetime

# WHO API URLs
URLS = {
    'adult_obesity': 'https://ghoapi.azureedge.net/api/NCD_BMI_30C',
    'child_obesity': 'https://ghoapi.azureedge.net/api/NCD_BMI_PLUS2C',
    'adult_underweight': 'https://ghoapi.azureedge.net/api/NCD_BMI_18C',
    'child_thinness': 'https://ghoapi.azureedge.net/api/NCD_BMI_MINUS2C'
}

def load_who_data(url):
    """Load data from WHO API with caching"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data['value'])
    except Exception as e:
        st.error(f"Error loading data from {url}: {e}")
        return None

def convert_country_code(code):
    """Convert country codes to full names"""
    special_cases = {
        'GLOBAL': 'Global',
        'WB_LMI': 'Low & Middle Income',
        'WB_HI': 'High Income',
        'WB_LI': 'Low Income',
        'EMR': 'Eastern Mediterranean Region',
        'EUR': 'Europe',
        'AFR': 'Africa',
        'SEAR': 'South-East Asia Region',
        'WPR': 'Western Pacific Region',
        'AMR': 'Americas Region',
        'WB_UMI': 'Upper Middle Income'
    }

    if code in special_cases:
        return special_cases[code]

    try:
        country = pycountry.countries.get(alpha_3=code)
        return country.name if country else code
    except:
        return code

def clean_dataset(df):
    """Clean and process the dataset"""
    # Keep only required columns
    columns_to_keep = ['ParentLocation', 'Dim1', 'TimeDim', 'Low', 'High', 'NumericValue', 'SpatialDim', 'age_group']
    df = df[columns_to_keep].copy()

    # Rename columns
    df.rename(columns={
        'TimeDim': 'Year',
        'Dim1': 'Gender',
        'NumericValue': 'Mean_Estimate',
        'Low': 'LowerBound',
        'High': 'UpperBound',
        'ParentLocation': 'Region',
        'SpatialDim': 'Country'
    }, inplace=True)

    # Filter years 2012-2022
    df = df[(df['Year'] >= 2012) & (df['Year'] <= 2022)]

    # Standardize gender values
    gender_mapping = {'Male': 'Male', 'Female': 'Female', 'Both sexes': 'Both'}
    df['Gender'] = df['Gender'].map(gender_mapping)

    # Convert country codes to full names
    df['Country'] = df['Country'].apply(convert_country_code)

    # Calculate CI_Width
    df['CI_Width'] = df['UpperBound'] - df['LowerBound']

    return df

def categorize_obesity(value):
    """Categorize obesity levels"""
    if pd.isna(value):
        return 'Unknown'
    elif value >= 30:
        return 'High'
    elif value >= 25:
        return 'Moderate'
    else:
        return 'Low'

def categorize_malnutrition(value):
    """Categorize malnutrition levels"""
    if pd.isna(value):
        return 'Unknown'
    elif value >= 20:
        return 'High'
    elif value >= 10:
        return 'Moderate'
    else:
        return 'Low'

def load_and_process_data():
    """Load and process all WHO data"""
    datasets = {}

    # Load all datasets
    for key, url in URLS.items():
        with st.spinner(f"Loading {key} data..."):
            datasets[key] = load_who_data(url)

    if any(df is None for df in datasets.values()):
        st.error("Failed to load some datasets. Please try again.")
        return None, None

    # Add age_group column
    datasets['adult_obesity']['age_group'] = 'Adult'
    datasets['child_obesity']['age_group'] = 'Child/Adolescent'
    datasets['adult_underweight']['age_group'] = 'Adult'
    datasets['child_thinness']['age_group'] = 'Child/Adolescent'

    # Combine datasets
    df_obesity = pd.concat([datasets['adult_obesity'], datasets['child_obesity']], ignore_index=True)
    df_malnutrition = pd.concat([datasets['adult_underweight'], datasets['child_thinness']], ignore_index=True)

    # Clean datasets
    df_obesity_clean = clean_dataset(df_obesity)
    df_malnutrition_clean = clean_dataset(df_malnutrition)

    # Add categorization
    df_obesity_clean['obesity_level'] = df_obesity_clean['Mean_Estimate'].apply(categorize_obesity)
    df_malnutrition_clean['malnutrition_level'] = df_malnutrition_clean['Mean_Estimate'].apply(categorize_malnutrition)

    return df_obesity_clean, df_malnutrition_clean