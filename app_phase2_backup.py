
import streamlit as st
import pandas as pd
from io import BytesIO

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Financial Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# 2. DASHBOARD HEADER
# ==========================================

st.title("📊 AI Financial Operations Dashboard")

st.write(
    "Monitor, filter and analyse financial transactions "
    "through an interactive dashboard."
)

st.divider()

# ==========================================
# 3. EXCEL FILE UPLOAD
# ==========================================

st.subheader("📁 Upload Financial Data")

uploaded_file = st.file_uploader(
    "Choose your Excel file",
    type=["xlsx"]
)

if uploaded_file is None:
    st.info("Please upload an Excel file to get started.")
    st.stop()

# ==========================================
# 4. READ EXCEL FILE
# ==========================================

try:
    df = pd.read_excel(uploaded_file)
    st.success("Excel file uploaded successfully!")

except Exception as e:
    st.error(f"Unable to read Excel file: {e}")
    st.stop()

# ==========================================
# 5. DATA VALIDATION
# ==========================================

required_columns = [
    "Transaction ID",
    "Customer",
    "Amount",
    "Status"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(
        f"Missing required columns: {', '.join(missing_columns)}"
    )
    st.stop()

if df.empty:
    st.error("The uploaded Excel file contains no transactions.")
    st.stop()

# ==========================================
# 6. DATA CLEANING
# ==========================================

df["Amount"] = pd.to_numeric(
    df["Amount"],
    errors="coerce"
)

invalid_rows = df["Amount"].isna().sum()

if invalid_rows > 0:
    st.warning(
        f"{invalid_rows} rows with invalid amounts were removed."
    )

    df = df.dropna(subset=["Amount"]).copy()

df["Status"] = (
    df["Status"]
    .astype(str)
    .str.strip()
    .str.title()
)

if df.empty:
    st.error("No valid transaction data available.")
    st.stop()

# Optional date column

has_date = "Date" in df.columns

if has_date:
    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    invalid_dates = df["Date"].isna().sum()

    if invalid_dates > 0:
        st.warning(
            f"{invalid_dates} rows have invalid dates. "
            "They will be excluded from date-wise analysis."
        )

# ==========================================
# 7. DASHBOARD METRICS
# ==========================================

st.subheader("📈 Financial Overview")

total_transactions = len(df)

total_amount = df["Amount"].sum()

successful_transactions = (
    df["Status"] == "Success"
).sum()

failed_transactions = (
    df["Status"] == "Failed"
).sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Transactions",
    f"{total_transactions:,}"
)

col2.metric(
    "Total Amount",
    f"₹{total_amount:,.2f}"
)

col3.metric(
    "Successful",
    f"{successful_transactions:,}"
)

col4.metric(
    "Failed",
    f"{failed_transactions:,}"
)

st.divider()

# ==========================================
# 8. ADVANCED FILTERS
# ==========================================

st.subheader("🔍 Advanced Transaction Filters")

filter_col1, filter_col2 = st.columns(2)

with filter_col1:

    status_options = ["All"] + sorted(
        df["Status"].dropna().unique().tolist()
    )

    status_filter = st.selectbox(
        "Filter by Status",
        status_options
    )

with filter_col2:

    min_amount = float(df["Amount"].min())
    max_amount = float(df["Amount"].max())

    amount_range = st.slider(
        "Filter by Transaction Amount",
        min_value=min_amount,
        max_value=max_amount,
        value=(min_amount, max_amount),
        step=1.0 if max_amount - min_amount >= 1 else 0.01,
        format="₹%.2f"
    )

# Apply status filter

filtered_df = df.copy()

if status_filter != "All":
    filtered_df = filtered_df[
        filtered_df["Status"] == status_filter
    ]

# Apply amount filter

filtered_df = filtered_df[
    (filtered_df["Amount"] >= amount_range[0]) &
    (filtered_df["Amount"] <= amount_range[1])
]

# ==========================================
# 9. DATE FILTER
# ==========================================

if has_date:

    st.subheader("📅 Date Range Filter")

    valid_dates = df["Date"].dropna()

    if not valid_dates.empty:

        min_date = valid_dates.min().date()
        max_date = valid_dates.max().date()

        date_range = st.date_input(
            "Select transaction date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

        if isinstance(date_range, tuple) and len(date_range) == 2:

            start_date, end_date = date_range

            filtered_df = filtered_df[
                filtered_df["Date"].notna() &
                (filtered_df["Date"].dt.date >= start_date) &
                (filtered_df["Date"].dt.date <= end_date)
            ]

    else:
        st.info("No valid dates are available for date filtering.")

else:
    st.info(
        "Your Excel file does not contain a Date column. "
        "Add a column named 'Date' to enable date-wise analysis."
    )

# ==========================================
# 10. FILTERED RESULTS
# ==========================================

st.divider()

st.subheader("📋 Filtered Transaction Details")

result_col1, result_col2 = st.columns(2)

result_col1.metric(
    "Filtered Transactions",
    f"{len(filtered_df):,}"
)

result_col2.metric(
    "Filtered Transaction Amount",
    f"₹{filtered_df['Amount'].sum():,.2f}"
)

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

# ==========================================
# 11. INTERACTIVE STATUS CHART
# ==========================================

st.divider()

st.subheader("📊 Transaction Status Analysis")

if not filtered_df.empty:

    status_counts = filtered_df["Status"].value_counts()

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:

        st.write("Transaction Count by Status")

        st.bar_chart(status_counts)

    with chart_col2:

        st.write("Transaction Amount by Status")

        amount_by_status = (
            filtered_df.groupby("Status")["Amount"]
            .sum()
        )

        st.bar_chart(amount_by_status)

else:
    st.warning("No transactions match the selected filters.")

# ==========================================
# 12. CUSTOMER-WISE ANALYSIS
# ==========================================

st.divider()

st.subheader("👥 Customer-wise Transaction Analysis")

if not filtered_df.empty:

    customer_analysis = (
        filtered_df.groupby("Customer")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(customer_analysis)

else:
    st.info("Customer analysis will appear when matching transactions are available.")

# ==========================================
# 13. DATE-WISE TRANSACTION ANALYSIS
# ==========================================

if has_date:

    st.divider()

    st.subheader("📅 Date-wise Financial Trends")

    date_data = filtered_df.dropna(subset=["Date"]).copy()

    if not date_data.empty:

        daily_analysis = (
            date_data.groupby(
                date_data["Date"].dt.date
            )["Amount"]
            .sum()
        )

        st.write("Daily Transaction Amount")

        st.line_chart(daily_analysis)

    else:
        st.info("No valid dated transactions match the selected filters.")

# ==========================================
# 14. EXCEL REPORT DOWNLOAD
# ==========================================

st.divider()

st.subheader("📥 Download Financial Report")

report_buffer = BytesIO()

summary_df = pd.DataFrame({
    "Metric": [
        "Total Transactions",
        "Total Transaction Amount",
        "Successful Transactions",
        "Failed Transactions",
        "Filtered Transactions",
        "Filtered Transaction Amount"
    ],

    "Value": [
        total_transactions,
        total_amount,
        successful_transactions,
        failed_transactions,
        len(filtered_df),
        filtered_df["Amount"].sum()
    ]
})

with pd.ExcelWriter(
    report_buffer,
    engine="openpyxl"
) as writer:

    filtered_df.to_excel(
        writer,
        sheet_name="Filtered Transactions",
        index=False
    )

    summary_df.to_excel(
        writer,
        sheet_name="Financial Summary",
        index=False
    )

report_buffer.seek(0)

st.download_button(
    label="📥 Download Financial Excel Report",
    data=report_buffer,
    file_name="financial_report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# ==========================================
# 15. FOOTER
# ==========================================

st.divider()

st.caption(
    "AI Financial Operations Dashboard | "
    "Built with Python, Pandas and Streamlit"
)
