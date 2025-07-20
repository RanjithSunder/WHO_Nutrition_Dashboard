import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def create_trend_comparison_chart(df_obesity, df_malnutrition, title):
    """Create a comparison chart for obesity and malnutrition trends"""
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Obesity Trend", "Malnutrition Trend"))

    # Add obesity trace
    fig.add_trace(
        go.Scatter(
            x=df_obesity['Year'],
            y=df_obesity['Mean_Estimate'],
            mode='lines+markers',
            name='Obesity'
        ),
        row=1, col=1
    )

    # Add malnutrition trace
    fig.add_trace(
        go.Scatter(
            x=df_malnutrition['Year'],
            y=df_malnutrition['Mean_Estimate'],
            mode='lines+markers',
            name='Malnutrition',
            line=dict(color='red')
        ),
        row=1, col=2
    )

    fig.update_layout(title_text=title, height=400)
    return fig