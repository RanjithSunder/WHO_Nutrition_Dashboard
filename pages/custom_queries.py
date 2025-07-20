import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sqlite3
from datetime import datetime
import plotly.graph_objects as go
from database import check_database_exists

def show_custom_queries(df_obesity, df_malnutrition):
    st.header("🔍 Custom SQL Queries")

    # Create a fresh connection for this session
    def get_fresh_connection():
        """Create a fresh SQLite connection for the current thread"""
        if not check_database_exists():
            st.error("Database not found. Please refresh data first.")
            return None
        return sqlite3.connect("who_nutrition_data.db")

    # Pre-defined queries
    query_options = {
        "Top 5 Countries with Highest Obesity": """
            SELECT Country, AVG(Mean_Estimate) as avg_obesity 
            FROM obesity 
            WHERE Country NOT IN ('Global', 'Low & Middle Income', 'High Income', 'Low Income', 'Upper Middle Income') 
            GROUP BY Country 
            ORDER BY avg_obesity DESC 
            LIMIT 5
        """,
        "Global Obesity Trend": """
            SELECT Year, AVG(Mean_Estimate) as avg_obesity 
            FROM obesity 
            WHERE Country = 'Global' 
            GROUP BY Year 
            ORDER BY Year
        """,
        "Gender Differences in Obesity": """
            SELECT Gender, AVG(Mean_Estimate) as avg_obesity 
            FROM obesity 
            WHERE Gender IN ('Male', 'Female') 
            GROUP BY Gender
        """,
        "Regional Malnutrition Comparison": """
            SELECT Region, AVG(Mean_Estimate) as avg_malnutrition 
            FROM malnutrition 
            GROUP BY Region 
            ORDER BY avg_malnutrition DESC
        """,
        "Countries with High Confidence Intervals": """
            SELECT Country, AVG(CI_Width) as avg_ci_width 
            FROM obesity 
            WHERE Country NOT IN ('Global', 'Low & Middle Income', 'High Income', 'Low Income', 'Upper Middle Income') 
            GROUP BY Country 
            ORDER BY avg_ci_width DESC 
            LIMIT 10
        """,
        "Obesity vs Malnutrition Correlation": """
            SELECT 
                o.Country,
                AVG(o.Mean_Estimate) as avg_obesity,
                AVG(m.Mean_Estimate) as avg_malnutrition
            FROM obesity o
            LEFT JOIN malnutrition m ON o.Country = m.Country AND o.Year = m.Year
            WHERE o.Country NOT IN ('Global', 'Low & Middle Income', 'High Income', 'Low Income', 'Upper Middle Income')
            GROUP BY o.Country
            HAVING COUNT(m.Mean_Estimate) > 0
            ORDER BY avg_obesity DESC
            LIMIT 20
        """,
        "Year-over-Year Growth Analysis": """
            WITH yearly_avg AS (
                SELECT 
                    Year, 
                    Country,
                    AVG(Mean_Estimate) as avg_value
                FROM obesity 
                WHERE Country = 'Global'
                GROUP BY Year, Country
            ),
            growth_calc AS (
                SELECT 
                    Year,
                    avg_value,
                    LAG(avg_value) OVER (ORDER BY Year) as prev_value
                FROM yearly_avg
            )
            SELECT 
                Year,
                ROUND(avg_value, 2) as obesity_rate,
                ROUND(avg_value - prev_value, 2) as year_over_year_change,
                CASE 
                    WHEN prev_value IS NULL THEN 'N/A'
                    ELSE ROUND(((avg_value - prev_value) / prev_value) * 100, 2) || '%'
                END as percentage_change
            FROM growth_calc
            ORDER BY Year
        """
    }

    # Query selection
    selected_query = st.selectbox("Select a pre-defined query:", list(query_options.keys()))

    if selected_query:
        query = query_options[selected_query]
        st.code(query, language='sql')

        if st.button("Execute Query", key="execute_predefined"):
            conn = get_fresh_connection()
            if conn:
                try:
                    with st.spinner("Executing query..."):
                        result = pd.read_sql_query(query, conn)
                        conn.close()

                    st.subheader("Query Results")
                    st.dataframe(result, use_container_width=True)

                    # Visualize results if appropriate
                    if len(result.columns) >= 2:
                        numeric_columns = result.select_dtypes(include=[np.number]).columns.tolist()

                        if len(numeric_columns) >= 1:
                            # Create visualization based on query type
                            if "trend" in selected_query.lower() or "growth" in selected_query.lower():
                                # Time series plot
                                if 'Year' in result.columns:
                                    fig = px.line(result, x='Year', y=numeric_columns[0],
                                                  title=f"Results: {selected_query}")
                                else:
                                    fig = px.bar(result, x=result.columns[0], y=numeric_columns[0],
                                                 title=f"Results: {selected_query}")
                            elif len(numeric_columns) >= 2:
                                # Scatter plot for correlation
                                fig = px.scatter(result, x=numeric_columns[0], y=numeric_columns[1],
                                                 hover_data=[result.columns[0]] if len(result.columns) > 2 else None,
                                                 title=f"Results: {selected_query}")
                            else:
                                # Bar chart
                                fig = px.bar(result, x=result.columns[0], y=numeric_columns[0],
                                             title=f"Results: {selected_query}")

                            fig.update_xaxes(tickangle=45)
                            st.plotly_chart(fig, use_container_width=True)

                    # Show summary statistics for numeric columns
                    numeric_cols = result.select_dtypes(include=[np.number])
                    if len(numeric_cols.columns) > 0:
                        st.subheader("Summary Statistics")
                        st.dataframe(numeric_cols.describe())

                except Exception as e:
                    st.error(f"Error executing query: {e}")
                finally:
                    if 'conn' in locals() and conn:
                        conn.close()

    # Custom query interface
    st.subheader("Write Your Own Query")

    # Add some helpful information
    with st.expander("💡 Query Tips & Table Information"):
        st.write("**Available Tables:**")
        st.write(
            "- `obesity`: Contains obesity data with columns: Country, Region, Year, Gender, age_group, Mean_Estimate, LowerBound, UpperBound, CI_Width, obesity_level")
        st.write(
            "- `malnutrition`: Contains malnutrition data with same structure but malnutrition_level instead of obesity_level")
        st.write("- `metadata`: Contains processing information")

        st.write("**Example Queries:**")
        st.code("""
-- Countries with highest obesity in 2022
SELECT Country, Mean_Estimate 
FROM obesity 
WHERE Year = 2022 AND Gender = 'Both' 
ORDER BY Mean_Estimate DESC 
LIMIT 10;

-- Comparison of obesity between genders
SELECT Gender, AVG(Mean_Estimate) as avg_obesity 
FROM obesity 
WHERE Gender IN ('Male', 'Female') 
GROUP BY Gender;
        """)

    custom_query = st.text_area(
        "Enter your SQL query:",
        height=150,
        placeholder="SELECT * FROM obesity WHERE Country = 'India' ORDER BY Year DESC LIMIT 10;",
        key="custom_query_text"
    )

    if st.button("Execute Custom Query", key="execute_custom"):
        if custom_query.strip():
            # Basic security check - prevent potentially harmful queries
            dangerous_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE']
            if any(keyword in custom_query.upper() for keyword in dangerous_keywords):
                st.error("🚫 Only SELECT queries are allowed for security reasons.")
                return

            conn = get_fresh_connection()
            if conn:
                try:
                    with st.spinner("Executing custom query..."):
                        result = pd.read_sql_query(custom_query, conn)
                        conn.close()

                    st.subheader("Custom Query Results")

                    # Show results count
                    st.info(f"📊 Query returned {len(result)} rows and {len(result.columns)} columns")

                    # Display results
                    st.dataframe(result, use_container_width=True)

                    # Auto-generate visualization if possible
                    if len(result) > 0 and len(result.columns) >= 2:
                        numeric_columns = result.select_dtypes(include=[np.number]).columns.tolist()

                        if len(numeric_columns) >= 1:
                            st.subheader("Visualization")

                            # Let user choose visualization type
                            viz_type = st.selectbox("Select visualization type:",
                                                    ["Bar Chart", "Line Chart", "Scatter Plot", "Histogram"])

                            try:
                                if viz_type == "Bar Chart" and len(result.columns) >= 2:
                                    x_col = result.columns[0]
                                    y_col = numeric_columns[0]
                                    fig = px.bar(result.head(20), x=x_col, y=y_col,
                                                 title="Query Results Visualization")
                                    fig.update_xaxes(tickangle=45)
                                    st.plotly_chart(fig, use_container_width=True)

                                elif viz_type == "Line Chart" and len(numeric_columns) >= 1:
                                    if 'Year' in result.columns:
                                        fig = px.line(result, x='Year', y=numeric_columns[0],
                                                      title="Query Results Over Time")
                                    else:
                                        fig = px.line(result, y=numeric_columns[0],
                                                      title="Query Results Trend")
                                    st.plotly_chart(fig, use_container_width=True)

                                elif viz_type == "Scatter Plot" and len(numeric_columns) >= 2:
                                    fig = px.scatter(result, x=numeric_columns[0], y=numeric_columns[1],
                                                     title="Query Results Scatter Plot")
                                    st.plotly_chart(fig, use_container_width=True)

                                elif viz_type == "Histogram" and len(numeric_columns) >= 1:
                                    fig = px.histogram(result, x=numeric_columns[0],
                                                       title="Query Results Distribution")
                                    st.plotly_chart(fig, use_container_width=True)

                            except Exception as viz_error:
                                st.warning(f"Could not create visualization: {viz_error}")

                    # Download option for results
                    if len(result) > 0:
                        csv_data = result.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Results as CSV",
                            data=csv_data,
                            file_name=f"query_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )

                except Exception as e:
                    st.error(f"Error executing custom query: {e}")
                    st.info("💡 Make sure your SQL syntax is correct and table names are valid.")
                finally:
                    if 'conn' in locals() and conn:
                        conn.close()
        else:
            st.warning("Please enter a query to execute.")

    # Query history (optional enhancement)
    if 'query_history' not in st.session_state:
        st.session_state.query_history = []

    if custom_query.strip() and st.button("Save Query to History", key="save_query"):
        if custom_query not in st.session_state.query_history:
            st.session_state.query_history.append(custom_query)
            st.success("Query saved to history!")

    if st.session_state.query_history:
        st.subheader("📝 Query History")
        for i, historical_query in enumerate(st.session_state.query_history[-5:]):  # Show last 5
            with st.expander(
                    f"Query {len(st.session_state.query_history) - len(st.session_state.query_history[-5:]) + i + 1}"):
                st.code(historical_query, language='sql')
                if st.button(f"Load Query {i + 1}", key=f"load_query_{i}"):
                    st.session_state.custom_query_text = historical_query
                    st.rerun()


def show_obesity_queries():
    """Display pre-defined obesity-related queries"""
    st.header("🍔 Obesity Analysis Queries")

    query_options = {
        "Top 5 regions with highest obesity (2022)": """
            SELECT Region, AVG(Mean_Estimate) as avg_obesity
            FROM obesity
            WHERE Year = 2022
            GROUP BY Region
            ORDER BY avg_obesity DESC
            LIMIT 5;
        """,
        "Top 5 countries with highest obesity": """
            SELECT Country, AVG(Mean_Estimate) as avg_obesity
            FROM obesity
            GROUP BY Country
            ORDER BY avg_obesity DESC
            LIMIT 5;
        """,
        "Obesity trend in India": """
            SELECT Year, AVG(Mean_Estimate) as avg_obesity
            FROM obesity
            WHERE Country = 'India'
            GROUP BY Year
            ORDER BY Year;
        """,
        "Average obesity by gender": """
            SELECT Gender, AVG(Mean_Estimate) as avg_obesity
            FROM obesity
            GROUP BY Gender;
        """,
        "Country count by obesity level and age group": """
            SELECT obesity_level, age_group, COUNT(DISTINCT Country) as country_count
            FROM obesity
            GROUP BY obesity_level, age_group
            ORDER BY obesity_level, age_group;
        """,
        "Countries with highest/lowest CI Width": """
            -- Top 5 least reliable (highest CI_Width)
            SELECT Country, AVG(CI_Width) as avg_ci_width
            FROM obesity
            GROUP BY Country
            ORDER BY avg_ci_width DESC
            LIMIT 5;

            -- Top 5 most consistent (smallest CI_Width)
            SELECT Country, AVG(CI_Width) as avg_ci_width
            FROM obesity
            GROUP BY Country
            ORDER BY avg_ci_width ASC
            LIMIT 5;
        """,
        "Average obesity by age group": """
            SELECT age_group, AVG(Mean_Estimate) as avg_obesity
            FROM obesity
            GROUP BY age_group
            ORDER BY avg_obesity DESC;
        """,
        "Top 10 consistent low obesity countries": """
            SELECT Country, 
                   AVG(Mean_Estimate) as avg_obesity,
                   AVG(CI_Width) as avg_ci_width,
                   (AVG(Mean_Estimate) + AVG(CI_Width)) as consistency_score
            FROM obesity
            GROUP BY Country
            ORDER BY consistency_score ASC
            LIMIT 10;
        """,
        "Countries where female obesity exceeds male": """
            SELECT o1.Country, o1.Year,
                   o1.Mean_Estimate as female_obesity,
                   o2.Mean_Estimate as male_obesity,
                   (o1.Mean_Estimate - o2.Mean_Estimate) as difference
            FROM obesity o1
            JOIN obesity o2 ON o1.Country = o2.Country 
                          AND o1.Year = o2.Year
                          AND o1.age_group = o2.age_group
            WHERE o1.Gender = 'Female' 
              AND o2.Gender = 'Male'
              AND (o1.Mean_Estimate - o2.Mean_Estimate) > 5
            ORDER BY difference DESC;
        """,
        "Global average obesity per year": """
            SELECT Year, AVG(Mean_Estimate) as global_avg_obesity
            FROM obesity
            GROUP BY Year
            ORDER BY Year;
        """
    }

    _display_query_interface(query_options)


def show_malnutrition_queries():
    """Display pre-defined malnutrition-related queries"""
    st.header("👾 Malnutrition Analysis Queries")

    query_options = {
        "Average malnutrition by age group": """
            SELECT age_group, AVG(Mean_Estimate) as avg_malnutrition
            FROM malnutrition
            GROUP BY age_group
            ORDER BY avg_malnutrition DESC;
        """,
        "Top 5 countries with highest malnutrition": """
            SELECT Country, AVG(Mean_Estimate) as avg_malnutrition
            FROM malnutrition
            GROUP BY Country
            ORDER BY avg_malnutrition DESC
            LIMIT 5;
        """,
        "Malnutrition trend in Africa": """
            SELECT Year, AVG(Mean_Estimate) as avg_malnutrition
            FROM malnutrition
            WHERE Region = 'Africa'
            GROUP BY Year
            ORDER BY Year;
        """,
        "Gender-based average malnutrition": """
            SELECT Gender, AVG(Mean_Estimate) as avg_malnutrition
            FROM malnutrition
            GROUP BY Gender;
        """,
        "Malnutrition level and CI Width by age group": """
            SELECT malnutrition_level, age_group, AVG(CI_Width) as avg_ci_width
            FROM malnutrition
            GROUP BY malnutrition_level, age_group
            ORDER BY malnutrition_level, age_group;
        """,
        "Yearly malnutrition in India, Nigeria, Brazil": """
            SELECT Country, Year, AVG(Mean_Estimate) as avg_malnutrition
            FROM malnutrition
            WHERE Country IN ('India', 'Nigeria', 'Brazil')
            GROUP BY Country, Year
            ORDER BY Country, Year;
        """,
        "Regions with lowest malnutrition": """
            SELECT Region, AVG(Mean_Estimate) as avg_malnutrition
            FROM malnutrition
            GROUP BY Region
            ORDER BY avg_malnutrition ASC;
        """,
        "Countries with increasing malnutrition": """
            SELECT Country,
                   MIN(Mean_Estimate) as min_malnutrition,
                   MAX(Mean_Estimate) as max_malnutrition,
                   (MAX(Mean_Estimate) - MIN(Mean_Estimate)) as increase
            FROM malnutrition
            GROUP BY Country
            HAVING (MAX(Mean_Estimate) - MIN(Mean_Estimate)) > 0
            ORDER BY increase DESC;
        """,
        "Min/Max malnutrition year-wise": """
            SELECT Year,
                   MIN(Mean_Estimate) as min_malnutrition,
                   MAX(Mean_Estimate) as max_malnutrition,
                   (MAX(Mean_Estimate) - MIN(Mean_Estimate)) as range_difference
            FROM malnutrition
            GROUP BY Year
            ORDER BY Year;
        """,
        "High CI Width flags (CI_width > 5)": """
            SELECT Country, Region, Year, Gender, age_group, CI_Width, Mean_Estimate
            FROM malnutrition
            WHERE CI_Width > 5
            ORDER BY CI_Width DESC;
        """
    }

    _display_query_interface(query_options)


def show_combined_queries():
    """Display pre-defined combined obesity/malnutrition queries"""
    st.header("🔗 Combined Analysis Queries")

    query_options = {
        "Obesity vs malnutrition (5 countries)": """
            SELECT o.Country,
                   AVG(o.Mean_Estimate) as avg_obesity,
                   AVG(m.Mean_Estimate) as avg_malnutrition
            FROM obesity o
            JOIN malnutrition m ON o.Country = m.Country
            WHERE o.Country IN ('India', 'USA', 'Brazil', 'Nigeria', 'China')
            GROUP BY o.Country
            ORDER BY o.Country;
        """,
        "Gender disparity in obesity/malnutrition": """
            SELECT o.Gender,
                   AVG(o.Mean_Estimate) as avg_obesity,
                   AVG(m.Mean_Estimate) as avg_malnutrition,
                   (AVG(o.Mean_Estimate) - AVG(m.Mean_Estimate)) as difference
            FROM obesity o
            JOIN malnutrition m ON o.Gender = m.Gender 
                              AND o.Country = m.Country 
                              AND o.Year = m.Year
            GROUP BY o.Gender;
        """,
        "Region-wise comparison (Africa/America)": """
            SELECT o.Region,
                   AVG(o.Mean_Estimate) as avg_obesity,
                   AVG(m.Mean_Estimate) as avg_malnutrition
            FROM obesity o
            JOIN malnutrition m ON o.Region = m.Region 
                              AND o.Country = m.Country 
                              AND o.Year = m.Year
            WHERE o.Region IN ('Africa', 'America')
            GROUP BY o.Region;
        """,
        "Countries with obesity up & malnutrition down": """
            WITH obesity_trend AS (
                SELECT Country,
                       (MAX(Mean_Estimate) - MIN(Mean_Estimate)) as obesity_change
                FROM obesity
                GROUP BY Country
            ),
            malnutrition_trend AS (
                SELECT Country,
                       (MAX(Mean_Estimate) - MIN(Mean_Estimate)) as malnutrition_change
                FROM malnutrition
                GROUP BY Country
            )
            SELECT ot.Country,
                   ot.obesity_change,
                   mt.malnutrition_change
            FROM obesity_trend ot
            JOIN malnutrition_trend mt ON ot.Country = mt.Country
            WHERE ot.obesity_change > 0 AND mt.malnutrition_change < 0
            ORDER BY ot.obesity_change DESC;
        """,
        "Age-wise trend analysis": """
            SELECT o.age_group,
                   AVG(o.Mean_Estimate) as avg_obesity,
                   AVG(m.Mean_Estimate) as avg_malnutrition,
                   COUNT(*) as record_count
            FROM obesity o
            JOIN malnutrition m ON o.age_group = m.age_group 
                                AND o.Country = m.Country 
                                AND o.Year = m.Year
            GROUP BY o.age_group
            ORDER BY o.age_group;
        """
    }

    _display_query_interface(query_options)


def _display_query_interface(query_options):
    """Helper function to display the query interface (reused across all query types)"""
    selected_query = st.selectbox("Select a pre-defined query:", list(query_options.keys()))

    def get_fresh_connection():
        """Create a fresh SQLite connection for the current thread"""
        if not check_database_exists():
            st.error("Database not found. Please refresh data first.")
            return None
        return sqlite3.connect("who_nutrition_data.db")

    if selected_query:
        query = query_options[selected_query]
        st.code(query, language='sql')

        if st.button("Execute Query"):
            conn = get_fresh_connection()
            if conn:
                try:
                    with st.spinner("Executing query..."):
                        result = pd.read_sql_query(query, conn)
                        conn.close()

                    st.subheader("Query Results")
                    st.dataframe(result, use_container_width=True)

                    # Visualization logic (same as in your original function)
                    if len(result.columns) >= 2:
                        numeric_columns = result.select_dtypes(include=[np.number]).columns.tolist()
                        if len(numeric_columns) >= 1:
                            if "trend" in selected_query.lower() or "growth" in selected_query.lower():
                                if 'Year' in result.columns:
                                    fig = px.line(result, x='Year', y=numeric_columns[0],
                                                  title=f"Results: {selected_query}")
                                else:
                                    fig = px.bar(result, x=result.columns[0], y=numeric_columns[0],
                                                 title=f"Results: {selected_query}")
                            elif len(numeric_columns) >= 2:
                                fig = px.scatter(result, x=numeric_columns[0], y=numeric_columns[1],
                                                 hover_data=[result.columns[0]] if len(result.columns) > 2 else None,
                                                 title=f"Results: {selected_query}")
                            else:
                                fig = px.bar(result, x=result.columns[0], y=numeric_columns[0],
                                             title=f"Results: {selected_query}")

                            fig.update_xaxes(tickangle=45)
                            st.plotly_chart(fig, use_container_width=True)

                    # Show summary statistics
                    numeric_cols = result.select_dtypes(include=[np.number])
                    if len(numeric_cols.columns) > 0:
                        st.subheader("Summary Statistics")
                        st.dataframe(numeric_cols.describe())

                except Exception as e:
                    st.error(f"Error executing query: {e}")
                finally:
                    if 'conn' in locals() and conn:
                        conn.close()

