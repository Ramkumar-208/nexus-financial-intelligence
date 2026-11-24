
# NEXUS – Financial Intelligence Platform

A Python-based financial operations dashboard designed to analyze transaction data, monitor financial risks, identify statistical anomalies, and generate automated reports.

## Project Overview

NEXUS is an interactive financial analytics application built using Python and Streamlit. It allows users to upload Excel transaction data and gain insights through automated analysis and visual reporting.

## Key Features

- Excel transaction data upload and validation
- Financial KPI monitoring
- Transaction filtering and analysis
- Customer-wise and status-wise analytics
- Statistical anomaly detection using the IQR method
- Automated financial summaries
- Rule-based financial data Q&A
- Risk alerts and monitoring
- Data quality checks
- Downloadable multi-sheet Excel reports
- Dark fintech dashboard interface

## Technology Stack

- Python
- Streamlit
- Pandas
- OpenPyXL
- Matplotlib / Plotly (if used in the application)

## Installation and Setup

1. Clone the repository:

   ```bash
   git clone YOUR_GITHUB_REPOSITORY_URL
   ```

2. Navigate to the project folder:

   ```bash
   cd AI_Financial_Dashboard
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   streamlit run app.py
   ```

## Input Data Format

Upload an Excel file containing these required columns:

- Transaction ID
- Customer
- Amount
- Status

A Date column can also be included for date-based analysis.

## Project Purpose

This project demonstrates practical applications of Python-based financial data analysis, automation, statistical monitoring, and interactive dashboard development.

## Important Note

This is a demonstration project using sample financial data. Statistical anomalies and risk alerts are indicators for further review and do not establish fraud.

The Q&A feature currently uses rule-based logic rather than a generative AI model.

