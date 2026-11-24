
import streamlit as st
import pandas as pd
import re
from io import BytesIO

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="NEXUS | Financial Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. DARK FINTECH DESIGN
# ==========================================

st.markdown("""
<style>

.stApp {
    background-color: #0B1120;
    color: #E5E7EB;
}

[data-testid="stHeader"] {
    background-color: #0B1120;
}

[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #263449;
}

[data-testid="stSidebar"] * {
    color: #E5E7EB;
}

h1, h2, h3 {
    color: #F8FAFC !important;
}

p, label, span {
    color: #CBD5E1;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

[data-testid="stMetric"] {
    background-color: #151F32;
    border: 1px solid #263449;
    padding: 18px;
    border-radius: 12px;
}

[data-testid="stMetricLabel"] {
    color: #94A3B8 !important;
}

[data-testid="stMetricValue"] {
    color: #F8FAFC !important;
}

[data-testid="stMetricDelta"] {
    color: #38BDF8 !important;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #263449;
    border-radius: 10px;
    overflow: hidden;
}

.stButton > button {
    background-color: #2563EB;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 18px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #1D4ED8;
    color: white;
    border: none;
}

.stDownloadButton > button {
    background-color: #0F766E;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
}

.stDownloadButton > button:hover {
    background-color: #115E59;
    color: white;
}

div[data-baseweb="select"] > div {
    background-color: #151F32;
    border-color: #334155;
}

div[data-testid="stAlert"] {
    border-radius: 10px;
}

hr {
    border-color: #263449;
}

[data-testid="stFileUploader"] {
    background-color: #151F32;
    border: 1px dashed #475569;
    border-radius: 12px;
    padding: 15px;
}

[data-testid="stExpander"] {
    background-color: #151F32;
    border: 1px solid #263449;
    border-radius: 10px;
}

.stCaption {
    color: #64748B;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. SIDEBAR
# ==========================================

with st.sidebar:

    st.title("◈ NEXUS")

    st.caption("FINANCIAL INTELLIGENCE PLATFORM")

    st.divider()

    st.markdown("### Navigation")

    page = st.radio(
        "Dashboard Sections",
        [
            "Overview",
            "Transactions",
            "Analytics",
            "AI Intelligence",
            "Risk Monitoring",
            "Data Quality",
            "Reports"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### System Status")

    st.success("Dashboard Active")

    st.caption("Python Analytics Engine")

    st.caption("Version 5.0")

# ==========================================
# 4. MAIN HEADER
# ==========================================

st.title("Financial Operations Dashboard")

st.caption(
    "Monitor transactions, analyse financial performance "
    "and identify unusual activity."
)

st.divider()

# ==========================================
# 5. FILE UPLOAD
# ==========================================

st.subheader("📁 Financial Data Source")

uploaded_file = st.file_uploader(
    "Upload your Excel transaction file",
    type=["xlsx"]
)

if uploaded_file is None:

    st.info(
        "Upload an Excel file to access your financial dashboard."
    )

    st.stop()

# ==========================================
# 6. READ EXCEL
# ==========================================

try:

    df = pd.read_excel(uploaded_file)

except Exception as e:

    st.error(f"Unable to read Excel file: {e}")
    st.stop()

if df.empty:

    st.error("The uploaded Excel file is empty.")
    st.stop()

# ==========================================
# 7. COLUMN VALIDATION
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

    st.write("Required columns:", required_columns)

    st.stop()

st.success("Financial data uploaded and validated successfully.")

# ==========================================
# 8. DATA CLEANING
# ==========================================

original_rows = len(df)

empty_rows = df.isna().all(axis=1).sum()

df = df.dropna(how="all").copy()

for column in [
    "Transaction ID",
    "Customer",
    "Status"
]:

    df[column] = (
        df[column]
        .astype("string")
        .str.strip()
    )

missing_id_count = (
    df["Transaction ID"].isna() |
    df["Transaction ID"].eq("")
).sum()

missing_customer_count = (
    df["Customer"].isna() |
    df["Customer"].eq("")
).sum()

missing_status_count = (
    df["Status"].isna() |
    df["Status"].eq("")
).sum()

df["Customer"] = (
    df["Customer"]
    .replace("", pd.NA)
    .fillna("Unknown")
)

df["Status"] = (
    df["Status"]
    .replace("", pd.NA)
    .fillna("Unknown")
)

df["Amount"] = pd.to_numeric(
    df["Amount"],
    errors="coerce"
)

invalid_amount_count = df["Amount"].isna().sum()

df = df.dropna(subset=["Amount"]).copy()

if df.empty:

    st.error("No valid transaction amounts found.")
    st.stop()

duplicate_count = df.loc[
    df["Transaction ID"].notna() &
    df["Transaction ID"].ne(""),
    "Transaction ID"
].duplicated().sum()

df["Transaction ID"] = (
    df["Transaction ID"]
    .replace("", pd.NA)
    .fillna("Unknown")
)

df["Status"] = df["Status"].str.title()

has_date = "Date" in df.columns

invalid_date_count = 0

if has_date:

    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    invalid_date_count = df["Date"].isna().sum()

# ==========================================
# 9. DATA QUALITY REPORT
# ==========================================

quality_report = pd.DataFrame({
    "Validation Check": [
        "Original Rows",
        "Empty Rows Removed",
        "Missing Transaction IDs",
        "Missing Customers",
        "Missing Status Values",
        "Invalid Amounts",
        "Duplicate Transaction IDs",
        "Invalid Dates"
    ],

    "Count": [
        original_rows,
        empty_rows,
        missing_id_count,
        missing_customer_count,
        missing_status_count,
        invalid_amount_count,
        duplicate_count,
        invalid_date_count
    ]
})

# ==========================================
# 10. FINANCIAL CALCULATIONS
# ==========================================

total_transactions = len(df)

total_amount = df["Amount"].sum()

average_amount = df["Amount"].mean()

successful_transactions = (
    df["Status"] == "Success"
).sum()

failed_transactions = (
    df["Status"] == "Failed"
).sum()

success_percentage = (
    successful_transactions / total_transactions
) * 100

failed_percentage = (
    failed_transactions / total_transactions
) * 100

highest_transaction = df.loc[
    df["Amount"].idxmax()
]

lowest_transaction = df.loc[
    df["Amount"].idxmin()
]

# ==========================================
# 11. ANOMALY DETECTION
# ==========================================

q1 = df["Amount"].quantile(0.25)

q3 = df["Amount"].quantile(0.75)

iqr = q3 - q1

lower_limit = q1 - (1.5 * iqr)

upper_limit = q3 + (1.5 * iqr)

anomalies = df[
    (df["Amount"] < lower_limit) |
    (df["Amount"] > upper_limit)
].copy()

def classify_anomaly(amount):

    if amount < lower_limit:
        return "Low"

    elif amount >= upper_limit + (2 * iqr):
        return "High"

    return "Medium"


if not anomalies.empty:

    anomalies["Severity"] = anomalies["Amount"].apply(
        classify_anomaly
    )

    anomalies["Detection Reason"] = anomalies["Amount"].apply(
        lambda amount:
        "Below statistical lower limit"
        if amount < lower_limit
        else "Above statistical upper limit"
    )

# ==========================================
# 12. NAVIGATION: OVERVIEW
# ==========================================

if page == "Overview":

    st.header("📊 Financial Overview")

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
        successful_transactions
    )

    col4.metric(
        "Failed",
        failed_transactions
    )

    st.divider()

    st.subheader("🤖 Automated Financial Summary")

    st.info(
        f"""
        Your dataset contains {total_transactions} transactions.

        Total transaction value: ₹{total_amount:,.2f}

        Successful transactions: {successful_transactions}
        ({success_percentage:.1f}%).

        Failed transactions: {failed_transactions}
        ({failed_percentage:.1f}%).

        Average transaction amount: ₹{average_amount:,.2f}.

        Highest transaction: {highest_transaction['Transaction ID']}
        belonging to {highest_transaction['Customer']},
        with an amount of ₹{highest_transaction['Amount']:,.2f}.
        """
    )

    st.divider()

    st.subheader("📈 Transaction Performance")

    chart1, chart2 = st.columns(2)

    with chart1:

        st.write("Transactions by Status")

        st.bar_chart(
            df["Status"].value_counts()
        )

    with chart2:

        st.write("Transaction Amount by Status")

        st.bar_chart(
            df.groupby("Status")["Amount"].sum()
        )

    st.divider()

    st.subheader("🚨 Anomaly Overview")

    a1, a2 = st.columns(2)

    a1.metric(
        "Detected Anomalies",
        len(anomalies)
    )

    a2.metric(
        "Failed Transactions",
        failed_transactions
    )

# ==========================================
# 13. NAVIGATION: TRANSACTIONS
# ==========================================

elif page == "Transactions":

    st.header("📋 Transaction Management")

    st.subheader("Transaction Filters")

    col1, col2 = st.columns(2)

    with col1:

        status_options = ["All"] + sorted(
            df["Status"].unique().tolist()
        )

        status_filter = st.selectbox(
            "Filter by Status",
            status_options
        )

    with col2:

        min_amount = float(df["Amount"].min())

        max_amount = float(df["Amount"].max())

        if min_amount < max_amount:

            amount_range = st.slider(
                "Transaction Amount Range",
                min_value=min_amount,
                max_value=max_amount,
                value=(min_amount, max_amount),
                format="₹%.2f"
            )

        else:

            amount_range = (min_amount, max_amount)

    filtered_df = df.copy()

    if status_filter != "All":

        filtered_df = filtered_df[
            filtered_df["Status"] == status_filter
        ]

    filtered_df = filtered_df[
        (filtered_df["Amount"] >= amount_range[0]) &
        (filtered_df["Amount"] <= amount_range[1])
    ]

    if has_date:

        valid_dates = df["Date"].dropna()

        if not valid_dates.empty:

            st.subheader("Date Filter")

            date_range = st.date_input(
                "Select transaction dates",
                value=(
                    valid_dates.min().date(),
                    valid_dates.max().date()
                ),
                min_value=valid_dates.min().date(),
                max_value=valid_dates.max().date()
            )

            if isinstance(date_range, (tuple, list)) and len(date_range) == 2:

                start_date, end_date = date_range

                filtered_df = filtered_df[
                    filtered_df["Date"].notna() &
                    (filtered_df["Date"].dt.date >= start_date) &
                    (filtered_df["Date"].dt.date <= end_date)
                ]

    col1, col2 = st.columns(2)

    col1.metric(
        "Filtered Transactions",
        len(filtered_df)
    )

    col2.metric(
        "Filtered Amount",
        f"₹{filtered_df['Amount'].sum():,.2f}"
    )

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

# ==========================================
# 14. NAVIGATION: ANALYTICS
# ==========================================

elif page == "Analytics":

    st.header("📈 Financial Analytics")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Transaction Count")

        st.bar_chart(
            df["Status"].value_counts()
        )

    with col2:

        st.subheader("Transaction Amount")

        st.bar_chart(
            df.groupby("Status")["Amount"].sum()
        )

    st.divider()

    st.subheader("Customer-wise Analysis")

    customer_analysis = (
        df.groupby("Customer")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(customer_analysis)

    if has_date:

        st.divider()

        st.subheader("Date-wise Financial Trends")

        date_data = df.dropna(
            subset=["Date"]
        ).copy()

        if not date_data.empty:

            daily_analysis = (
                date_data.groupby(
                    date_data["Date"].dt.date
                )["Amount"].sum()
            )

            st.line_chart(daily_analysis)

        else:

            st.info("No valid transaction dates available.")

# ==========================================
# 15. NAVIGATION: AI INTELLIGENCE
# ==========================================

elif page == "AI Intelligence":

    st.header("🤖 Financial Intelligence Centre")

    st.subheader("Automated Financial Summary")

    st.info(
        f"""
        The dataset contains {total_transactions} transactions.

        Total value: ₹{total_amount:,.2f}

        Average amount: ₹{average_amount:,.2f}

        Success rate: {success_percentage:.1f}%

        Failure rate: {failed_percentage:.1f}%
        """
    )

    st.divider()

    st.subheader("💬 Ask Your Financial Data")

    st.write(
        "Ask questions about your uploaded transaction data."
    )

    question = st.text_input(
        "Enter your question",
        placeholder="Example: Who is the top customer?"
    )

    if st.button("Get Answer"):

        if not question.strip():

            st.warning("Please enter a question.")

        else:

            q = re.sub(
                r"[^a-z0-9\s]",
                " ",
                question.lower()
            )

            q = " ".join(q.split())

            answer = None

            if any(
                phrase in q for phrase in [
                    "highest transaction",
                    "largest transaction",
                    "maximum transaction"
                ]
            ):

                row = df.loc[df["Amount"].idxmax()]

                answer = (
                    f"The highest transaction is "
                    f"{row['Transaction ID']} by {row['Customer']}, "
                    f"amounting to ₹{row['Amount']:,.2f}."
                )

            elif any(
                phrase in q for phrase in [
                    "lowest transaction",
                    "smallest transaction",
                    "minimum transaction"
                ]
            ):

                row = df.loc[df["Amount"].idxmin()]

                answer = (
                    f"The lowest transaction is "
                    f"{row['Transaction ID']} by {row['Customer']}, "
                    f"amounting to ₹{row['Amount']:,.2f}."
                )

            elif any(
                phrase in q for phrase in [
                    "top customer",
                    "highest customer",
                    "best customer",
                    "customer spent most"
                ]
            ):

                totals = df.groupby("Customer")["Amount"].sum()

                customer = totals.idxmax()

                answer = (
                    f"{customer} has the highest total transaction "
                    f"amount of ₹{totals.max():,.2f}."
                )

            elif any(
                phrase in q for phrase in [
                    "total amount",
                    "total transaction value",
                    "overall amount"
                ]
            ):

                answer = (
                    f"The total transaction amount is "
                    f"₹{total_amount:,.2f}."
                )

            elif "average" in q or "mean amount" in q:

                answer = (
                    f"The average transaction amount is "
                    f"₹{average_amount:,.2f}."
                )

            elif "failed percentage" in q or "failure percentage" in q:

                answer = (
                    f"The failed transaction percentage is "
                    f"{failed_percentage:.1f}%."
                )

            elif "failed" in q or "failure" in q:

                answer = (
                    f"There are {failed_transactions} failed transactions, "
                    f"representing {failed_percentage:.1f}%."
                )

            elif "successful" in q or "success rate" in q:

                answer = (
                    f"There are {successful_transactions} successful "
                    f"transactions. Success rate: {success_percentage:.1f}%."
                )

            elif any(
                phrase in q for phrase in [
                    "anomaly",
                    "anomalies",
                    "unusual transaction"
                ]
            ):

                answer = (
                    f"The system detected {len(anomalies)} unusual "
                    "transaction(s) using the IQR method."
                )

            elif "duplicate" in q:

                answer = (
                    f"There are {duplicate_count} duplicate "
                    "transaction ID(s)."
                )

            elif any(
                phrase in q for phrase in [
                    "total transactions",
                    "transaction count",
                    "how many transactions"
                ]
            ):

                answer = (
                    f"The dataset contains {total_transactions} transactions."
                )

            elif "date range" in q or "transaction period" in q:

                if has_date and df["Date"].notna().any():

                    answer = (
                        f"The transaction period is from "
                        f"{df['Date'].min().date()} to "
                        f"{df['Date'].max().date()}."
                    )

                else:

                    answer = "No valid Date column is available."

            if answer:

                st.success(answer)

            else:

                st.warning(
                    "I couldn't understand that question. Try asking about "
                    "total amount, average amount, highest transaction, "
                    "lowest transaction, top customer, failed transactions, "
                    "success rate, anomalies, duplicates or date range."
                )

# ==========================================
# 16. NAVIGATION: RISK MONITORING
# ==========================================

elif page == "Risk Monitoring":

    st.header("⚠️ Risk Monitoring Centre")

    if failed_percentage >= 20:

        st.error(
            f"HIGH ALERT: {failed_percentage:.1f}% of transactions failed."
        )

    elif failed_transactions > 0:

        st.warning(
            f"{failed_transactions} failed transactions require review."
        )

    else:

        st.success("No failed transactions detected.")

    if duplicate_count > 0:

        st.warning(
            f"{duplicate_count} duplicate transaction IDs detected."
        )

    if not anomalies.empty:

        st.warning(
            f"{len(anomalies)} unusual transaction amounts detected."
        )

        st.subheader("Anomaly Severity")

        st.bar_chart(
            anomalies["Severity"].value_counts()
        )

        st.dataframe(
            anomalies,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success("No unusual transaction amounts detected.")

    st.divider()

    st.subheader("Failed Transaction Records")

    failed_df = df[
        df["Status"] == "Failed"
    ]

    if not failed_df.empty:

        st.dataframe(
            failed_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success("No failed transactions.")

# ==========================================
# 17. NAVIGATION: DATA QUALITY
# ==========================================

elif page == "Data Quality":

    st.header("🛡️ Data Quality Centre")

    st.write(
        "Validation results for the uploaded Excel transaction data."
    )

    q1, q2, q3, q4 = st.columns(4)

    q1.metric("Valid Rows", len(df))

    q2.metric("Invalid Amounts", invalid_amount_count)

    q3.metric("Duplicate IDs", duplicate_count)

    q4.metric("Invalid Dates", invalid_date_count)

    st.subheader("Detailed Validation Report")

    st.dataframe(
        quality_report,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Validation Observations")

    if invalid_amount_count > 0:

        st.warning(
            f"{invalid_amount_count} invalid amount rows were removed."
        )

    if duplicate_count > 0:

        st.warning(
            f"{duplicate_count} duplicate transaction IDs were found."
        )

    if missing_customer_count > 0:

        st.info(
            f"{missing_customer_count} missing customer values "
            "were marked as Unknown."
        )

    if (
        invalid_amount_count == 0
        and duplicate_count == 0
        and missing_id_count == 0
        and missing_customer_count == 0
        and missing_status_count == 0
    ):

        st.success("No major data quality issues detected.")

# ==========================================
# 18. NAVIGATION: REPORTS
# ==========================================

elif page == "Reports":

    st.header("📥 Financial Reports Centre")

    st.write(
        "Generate and download financial transaction reports."
    )

    report_buffer = BytesIO()

    summary_df = pd.DataFrame({
        "Metric": [
            "Total Transactions",
            "Total Transaction Amount",
            "Successful Transactions",
            "Failed Transactions",
            "Average Transaction Amount",
            "Success Percentage",
            "Failed Percentage",
            "Detected Anomalies",
            "Duplicate Transaction IDs",
            "Filtered Transactions"
        ],

        "Value": [
            total_transactions,
            total_amount,
            successful_transactions,
            failed_transactions,
            average_amount,
            success_percentage,
            failed_percentage,
            len(anomalies),
            duplicate_count,
            total_transactions
        ]
    })

    with pd.ExcelWriter(
        report_buffer,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            sheet_name="All Transactions",
            index=False
        )

        summary_df.to_excel(
            writer,
            sheet_name="Financial Summary",
            index=False
        )

        anomalies.to_excel(
            writer,
            sheet_name="Anomaly Detection",
            index=False
        )

        failed_df = df[
            df["Status"] == "Failed"
        ]

        failed_df.to_excel(
            writer,
            sheet_name="Failed Transactions",
            index=False
        )

        quality_report.to_excel(
            writer,
            sheet_name="Data Quality",
            index=False
        )

    report_buffer.seek(0)

    st.download_button(
        label="📥 Download Complete Financial Report",
        data=report_buffer,
        file_name="NEXUS_Financial_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.caption(
        "The report includes transaction data, financial summary, "
        "anomalies, failed transactions and data quality."
    )

# ==========================================
# 19. FOOTER
# ==========================================

st.divider()

st.caption(
    "NEXUS Financial Intelligence Platform | "
    "Python | Pandas | Streamlit | Statistical Analysis"
)

st.caption(
    "Demonstration project using sample financial data. "
    "Statistical alerts are indicators for review, not proof of fraud."
)
