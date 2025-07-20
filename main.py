import streamlit as st
from data_loader import load_and_process_data
from database import check_database_exists, load_from_database, create_persistent_database
import os

# Set page configuration
st.set_page_config(
    page_title="WHO Nutrition Data Analysis",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
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
    .insight-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E86AB;
        margin: 1rem 0;
    }
    .data-status {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #2E86AB;
        margin: 1rem 0;
    }
    [data-testid="stSidebarNav"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)


def show_data_status():
    """Show current data status and options"""
    from database import get_database_info

    st.markdown('<div class="data-status">', unsafe_allow_html=True)
    st.subheader("📊 Data Status")

    db_info = get_database_info()

    if db_info:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Obesity Records", f"{db_info['obesity_count']:,}")
        with col2:
            st.metric("Malnutrition Records", f"{db_info['malnutrition_count']:,}")
        with col3:
            st.metric("Database Size", db_info['file_size'])
        with col4:
            st.metric("Last Updated", db_info['timestamp'][:10] if db_info['timestamp'] != 'Unknown' else 'Unknown')

        st.success("✅ Using existing database")

        # Option to refresh data
        if st.button("🔄 Refresh Data from WHO API", type="secondary"):
            if st.session_state.get('confirm_refresh', False):
                with st.spinner("Processing new data from WHO API..."):
                    df_obesity, df_malnutrition = load_and_process_data()
                    if df_obesity is not None and df_malnutrition is not None:
                        # Remove old database
                        if os.path.exists("who_nutrition_data.db"):
                            os.remove("who_nutrition_data.db")

                        # Create new database
                        conn = create_persistent_database(df_obesity, df_malnutrition)

                        # Update session state
                        st.session_state.df_obesity = df_obesity
                        st.session_state.df_malnutrition = df_malnutrition
                        st.session_state.conn = conn
                        st.session_state.data_loaded = True
                        st.session_state.confirm_refresh = False

                        st.success("✅ Data refreshed successfully!")
                        st.rerun()
            else:
                st.warning(
                    "⚠️ This will download fresh data from WHO API and replace the existing database. Click again to confirm.")
                st.session_state.confirm_refresh = True

    else:
        st.info("🔄 No existing database found. Data will be processed from WHO API.")

    st.markdown('</div>', unsafe_allow_html=True)


def main():
    st.markdown('<h1 class="main-header">🌍 WHO Nutrition Data Analysis Dashboard</h1>', unsafe_allow_html=True)

    # Show data status
    show_data_status()

    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a section:",
        ["Data Overview", "Global Trends", "Regional Analysis", "Demographic Patterns",
         "Country Comparison", "Custom Queries", "Data Quality", "Insights & Recommendations"]
    )

    # Load data
    if 'data_loaded' not in st.session_state:
        if check_database_exists():
            # Load from existing database
            with st.spinner("Loading data from database..."):
                df_obesity, df_malnutrition, conn = load_from_database()
                if df_obesity is not None and df_malnutrition is not None:
                    st.session_state.df_obesity = df_obesity
                    st.session_state.df_malnutrition = df_malnutrition
                    st.session_state.conn = conn
                    st.session_state.data_loaded = True
                    st.success("✅ Data loaded from existing database")
                else:
                    st.error("Failed to load data from database. Please refresh.")
                    return
        else:
            # Process data from API
            with st.spinner("Processing WHO nutrition data for the first time..."):
                df_obesity, df_malnutrition = load_and_process_data()
                if df_obesity is not None and df_malnutrition is not None:
                    # Create persistent database
                    conn = create_persistent_database(df_obesity, df_malnutrition)

                    st.session_state.df_obesity = df_obesity
                    st.session_state.df_malnutrition = df_malnutrition
                    st.session_state.conn = conn
                    st.session_state.data_loaded = True
                    st.success("✅ Data processed and saved to database")
                else:
                    st.error("Failed to load data. Please refresh the page.")
                    return

    # Page routing
    if page == "Data Overview":
        from pages.data_overview import show_data_overview
        show_data_overview(st.session_state.df_obesity, st.session_state.df_malnutrition)
    elif page == "Global Trends":
        from pages.global_trends import show_global_trends
        show_global_trends(st.session_state.df_obesity, st.session_state.df_malnutrition)
    elif page == "Regional Analysis":
        from pages.regional_analysis import show_regional_analysis
        show_regional_analysis(st.session_state.df_obesity, st.session_state.df_malnutrition)
    elif page == "Demographic Patterns":
        from pages.demographic_patterns import show_demographic_patterns
        show_demographic_patterns(st.session_state.df_obesity, st.session_state.df_malnutrition)
    elif page == "Country Comparison":
        from pages.country_comparison import show_country_comparison
        show_country_comparison(st.session_state.df_obesity, st.session_state.df_malnutrition)
    elif page == "Custom Queries":
        import pages.custom_queries
        # Modified to include query categories
        pages.custom_queries.st.sidebar.subheader("Query Categories")
        query_category = pages.custom_queries.st.sidebar.radio(
            "Select query type:",
            ["General Queries", "Obesity Queries", "Malnutrition Queries", "Combined Analysis"],
            horizontal=True
        )
        if query_category == "General Queries":
            pages.custom_queries.show_custom_queries(pages.custom_queries.st.session_state.df_obesity, pages.custom_queries.st.session_state.df_malnutrition) # Your original custom query function
        elif query_category == "Obesity Queries":
            pages.custom_queries.show_obesity_queries()
        elif query_category == "Malnutrition Queries":
            pages.custom_queries.show_malnutrition_queries()
        elif query_category == "Combined Analysis":
            pages.custom_queries.show_combined_queries()
    elif page == "Data Quality":
        from pages.data_quality import show_data_quality
        show_data_quality(st.session_state.df_obesity, st.session_state.df_malnutrition)
    elif page == "Insights & Recommendations":
        from pages.insights_recommendations import show_insights_recommendations
        show_insights_recommendations(st.session_state.df_obesity, st.session_state.df_malnutrition)


if __name__ == "__main__":
    main()