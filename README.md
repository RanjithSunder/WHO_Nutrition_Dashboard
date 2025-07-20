# WHO Nutrition Data Analysis Dashboard

![WHO Logo](assets/who_logo.png)

Interactive dashboard for analyzing WHO nutrition data including obesity and malnutrition statistics.

## Features
- Global trends visualization
- Regional comparison tools
- Demographic pattern analysis
- Custom SQL query interface
- Data quality assessment

## Installation
bash
git clone https://github.com/yourusername/who-nutrition-dashboard.git
cd who-nutrition-dashboard
pip install -r requirements.txt
Usage
bash
streamlit run main.py
Data Sources
WHO Global Health Observatory


3. **requirements.txt**
streamlit==1.32.0
pandas==2.0.3
plotly==5.18.0
requests==2.31.0
pycountry==22.3.5
numpy==1.24.4
sqlite3==2.6.0
watchdog==3.0.0


4. **main.py**
python
import os
os.environ["STREAMLIT_SERVER_ENABLE_FILE_WATCHER"] = "false"

import streamlit as st
from database import check_database_exists, load_from_database, create_persistent_database
from data_loader import load_and_process_data

# Load custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("assets/style.css")

def main():
    st.set_page_config(
        page_title="WHO Nutrition Dashboard",
        layout="wide",
        initial_sidebar_state="expanded"
    )


if __name__ == "__main__":
    main()
assets/style.css (Optional styling)

css
/* Custom CSS for the dashboard */
.main-header {
    font-size: 2.5rem;
    color: #2E86AB;
    text-align: center;
    margin-bottom: 2rem;
}

.metric-container {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
}

.stButton>button {
    background-color: #2E86AB;
    color: white;
    border-radius: 8px;
}
Deploym
