
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Data Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Data Analytics Dashboard")
st.write("Explore, filter, and visualize your dataset.")

# Load a CSV uploaded by the user or the local cleaned dataset
uploaded_file = st.sidebar.file_uploader(
    "Upload your CSV dataset",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    csv_path = Path("cleaned_dataset.csv")

    if csv_path.exists():
        df = pd.read_csv(csv_path)
    else:
        # Sample data so the dashboard works immediately
        df = pd.DataFrame({
            "Product": ["Laptop", "Phone", "Tablet", "Laptop",
                        "Phone", "Tablet", "Laptop", "Phone"],
            "Category": ["Electronics"] * 8,
            "Sales": [50000, 20000, 15000, 45000,
                      25000, 12000, 55000, 22000],
            "Quantity": [2, 4, 3, 2, 5, 2, 3, 4],
            "Region": ["West", "North", "South", "West",
                       "North", "South", "East", "East"]
        })
        st.info(
            "Showing sample data. Upload your CSV or add "
            "cleaned_dataset.csv to this project folder."
        )

if df.empty:
    st.warning("The dataset is empty. Please upload another CSV.")
    st.stop()

# Data preview and sidebar filters
st.sidebar.header("Dashboard Filters")

filtered_df = df.copy()
categorical_columns = df.select_dtypes(
    include=["object", "category", "string"]
).columns.tolist()

if categorical_columns:
    filter_column = st.sidebar.selectbox(
        "Filter by category",
        ["All"] + categorical_columns
    )

    if filter_column != "All":
        options = df[filter_column].dropna().unique().tolist()
        selected = st.sidebar.multiselect(
            f"Select {filter_column}",
            options,
            default=options
        )

        filtered_df = filtered_df[
            filtered_df[filter_column].isin(selected)
        ]

st.subheader("📌 Key Performance Indicators")

numeric_columns = filtered_df.select_dtypes(
    include="number"
).columns.tolist()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Records", f"{len(filtered_df):,}")
col2.metric("Total Columns", len(filtered_df.columns))
col3.metric(
    "Missing Values",
    f"{int(filtered_df.isna().sum().sum()):,}"
)

if numeric_columns:
    col4.metric(
        f"Average {numeric_columns[0]}",
        f"{filtered_df[numeric_columns[0]].mean():,.2f}"
    )
else:
    col4.metric("Numeric Columns", 0)

st.divider()

st.subheader("📈 Data Visualizations")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    if numeric_columns:
        selected_numeric = st.selectbox(
            "Choose a numeric column",
            numeric_columns
        )
        fig_hist = px.histogram(
            filtered_df,
            x=selected_numeric,
            title=f"Distribution of {selected_numeric}",
            template="plotly_white"
        )
        st.plotly_chart(fig_hist, use_container_width=True)
    else:
        st.info("No numeric columns available for a histogram.")

with chart_col2:
    if categorical_columns and numeric_columns:
        selected_category = st.selectbox(
            "Choose a category for comparison",
            categorical_columns,
            key="category_chart"
        )
        selected_value = st.selectbox(
            "Choose a value to summarize",
            numeric_columns,
            key="value_chart"
        )

        summary = (
            filtered_df.groupby(selected_category, dropna=False)[selected_value]
            .sum()
            .reset_index()
        )

        fig_bar = px.bar(
            summary,
            x=selected_category,
            y=selected_value,
            title=f"{selected_value} by {selected_category}",
            template="plotly_white"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Add a category and numeric column to compare values.")

st.subheader("🗂️ Dataset Preview")
st.dataframe(filtered_df, use_container_width=True)

st.subheader("⬇️ Download Filtered Data")
csv_data = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download CSV",
    data=csv_data,
    file_name="dashboard_data.csv",
    mime="text/csv"
)

st.caption("Built with Python, Pandas, Streamlit, and Plotly.")
