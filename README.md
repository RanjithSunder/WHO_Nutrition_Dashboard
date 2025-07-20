# WHO Nutrition Dashboard

A comprehensive dashboard application for visualizing and analyzing World Health Organization (WHO) nutrition data and global nutrition indicators.

## Overview

The WHO Nutrition Dashboard provides an interactive web-based interface for exploring global nutrition statistics, trends, and indicators. This tool enables researchers, health professionals, and policy makers to analyze nutrition data across different countries, regions, and time periods to support evidence-based decision making in public health.

## Features

- **Interactive Data Visualization**: Dynamic charts and graphs displaying nutrition indicators
- **Country Comparison**: Compare nutrition statistics across different countries and regions
- **Time Series Analysis**: Track nutrition trends over time
- **WHO Data Integration**: Direct integration with WHO nutrition databases
- **Export Functionality**: Export charts and data for reports and presentations
- **Responsive Design**: Mobile-friendly interface for accessibility across devices
- **Search and Filter**: Advanced filtering options for specific nutrition indicators

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript (with visualization libraries)
- **Backend**: Python (Flask/Django)
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Database**: SQLite/PostgreSQL
- **Deployment**: Docker (optional)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/RanjithSunder/WHO_Nutrition_Dashboard.git
   cd WHO_Nutrition_Dashboard
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (if applicable):
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize the database** (if applicable):
   ```bash
   python manage.py migrate  # For Django
   # or
   python init_db.py  # For Flask
   ```

6. **Run the application**:
   ```bash
   python app.py  # For Flask
   # or
   python manage.py runserver  # For Django
   ```

7. **Access the dashboard**:
   Open your browser and navigate to `http://localhost:5000` (Flask) or `http://localhost:8000` (Django)

## Usage

### Getting Started

1. **Data Loading**: The dashboard automatically loads WHO nutrition data on startup
2. **Navigation**: Use the sidebar menu to navigate between different nutrition indicators
3. **Filtering**: Apply filters by country, region, year, or specific nutrition metrics
4. **Visualization**: Select different chart types (bar, line, scatter, map) for data visualization
5. **Export**: Download charts as PNG/PDF or export data as CSV/Excel

### Key Nutrition Indicators

The dashboard includes visualizations for:
- Malnutrition rates (stunting, wasting, underweight)
- Overweight and obesity statistics
- Micronutrient deficiencies
- Infant and young child feeding practices
- Maternal nutrition indicators
- Food security metrics

## Data Sources

- World Health Organization (WHO) Global Health Observatory
- WHO Global Database on Child Growth and Malnutrition
- UNICEF-WHO-World Bank Joint Child Malnutrition Estimates
- WHO Global Nutrition Monitoring Framework

## Project Structure

```
WHO_Nutrition_Dashboard/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── config.py             # Configuration settings
├── data/                 # Data files and datasets
│   ├── raw/              # Raw WHO data files
│   └── processed/        # Cleaned and processed data
├── static/               # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
├── templates/            # HTML templates
├── utils/                # Utility functions
│   ├── data_loader.py    # Data loading functions
│   ├── visualizations.py # Chart generation
│   └── helpers.py        # Helper functions
└── tests/                # Unit tests

```

## Contributing

We welcome contributions to improve the WHO Nutrition Dashboard! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/new-feature`
3. **Make your changes** and add tests if applicable
4. **Commit your changes**: `git commit -m "Add new feature"`
5. **Push to the branch**: `git push origin feature/new-feature`
6. **Submit a pull request**

### Development Guidelines

- Follow PEP 8 style guidelines for Python code
- Write clear, documented code with comments
- Include unit tests for new features
- Update documentation as needed
- Test across different browsers and devices

## Testing

Run the test suite with:

```bash
python -m pytest tests/
# or
python -m unittest discover tests/
```

## Deployment

### Local Development
The application runs locally on `http://localhost:5000` or `http://localhost:8000`

### Production Deployment
For production deployment, consider:
- Using a production WSGI server (Gunicorn, uWSGI)
- Setting up a reverse proxy (Nginx)
- Configuring environment variables for production
- Using a production database (PostgreSQL, MySQL)

### Docker Deployment (if applicable)

```bash
docker build -t who-nutrition-dashboard .
docker run -p 5000:5000 who-nutrition-dashboard
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- World Health Organization for providing open nutrition data
- The global health community for nutrition indicator standards
- Contributors and maintainers of this project

## Support

For questions, issues, or suggestions:
- Open an issue on GitHub
- Contact the maintainer: [Your Email]
- Check the documentation wiki

## Changelog

### Version 1.0.0
- Initial release with basic dashboard functionality
- WHO data integration
- Interactive visualizations
- Country comparison features

---

**Note**: This dashboard is for educational and research purposes. Always consult official WHO publications and guidelines for policy decisions.
