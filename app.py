import streamlit as st
import pandas as pd
import plotly.express as px

# === Page Setup ===
st.set_page_config(page_title="2025 Data Job Salaries", layout="wide")
st.title("💼 2025 Data Job Salaries Dashboard")

# === Load Data with Caching ===
@st.cache_data
def load_data():
    return pd.read_csv("C:/Users/Swara/Desktop/Git_projects/data-job-salaries-2025/data/DataScience_Salaries.csv")

df = load_data()

# === Main Tabs ===
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📥 Data Import",
    "🧹 Data Cleaning",
    "🔍 EDA + Filters",
    "📊 Visualizations",
    "💡 Insights"
])

# === Tab 1: Data Import ===
with tab1:
    st.header("📥 Data Import")
    st.success("Data loaded successfully!")
    st.dataframe(df.head())

# === Tab 2: Data Cleaning ===
with tab2:
    st.header("🧹 Data Cleaning")
    st.markdown("Check for missing values and data types.")
    st.write("**Missing Values:**")
    st.dataframe(df.isnull().sum())
    st.write("**Column Data Types:**")
    st.dataframe(df.dtypes)

# === Tab 3: EDA + Filters ===
with tab3:
    st.header("🔍 Exploratory Data Analysis + Filters")

    with st.expander("🎛️ Apply Filters"):
        exp_options = sorted(df["experience_level"].unique())
        cat_options = sorted(df["job_category"].unique())
        setting_options = sorted(df["work_setting"].unique())

        experience = st.multiselect("Select Experience Level", exp_options, default=exp_options)
        category = st.multiselect("Select Job Category", cat_options, default=cat_options)
        setting = st.multiselect("Select Work Setting", setting_options, default=setting_options)

    # Apply filters
    filtered_df = df[
        df["experience_level"].isin(experience) &
        df["job_category"].isin(category) &
        df["work_setting"].isin(setting)
    ]

    st.write(f"🔎 Filtered Records: {len(filtered_df)}")
    st.dataframe(filtered_df)

# === Tab 4: Visualizations ===
with tab4:
    st.header("📊 Visualizations")

    salary_tab1, salary_tab2, salary_tab3 = st.tabs(["💰 Salary by Experience", "🌍 Salary by Country", "🏢 Salary by Work Setting"])

    with salary_tab1:
        fig1 = px.box(filtered_df, x="experience_level", y="salary_in_usd", color="job_category")
        st.plotly_chart(fig1, use_container_width=True)

    with salary_tab2:
        avg_country = filtered_df.groupby("employee_residence")["salary_in_usd"].mean().reset_index()
        fig2 = px.bar(avg_country, x="employee_residence", y="salary_in_usd", color="salary_in_usd")
        st.plotly_chart(fig2, use_container_width=True)

    with salary_tab3:
        avg_setting = filtered_df.groupby("work_setting")["salary_in_usd"].mean().reset_index()
        fig3 = px.bar(avg_setting, x="work_setting", y="salary_in_usd", color="salary_in_usd")
        st.plotly_chart(fig3, use_container_width=True)

# === Tab 5: Insights + Export ===
with tab5:
    st.header("💡 Key Insights")
    st.markdown("""
    - 💼 **Remote roles** often pay highly, especially for Senior positions.
    - 🏙️ **San Francisco, New York, London** are top salary hubs.
    - 🤖 **AI Engineers & Principal Data Scientists** earn the most.
    """)

    st.download_button("⬇ Download Filtered Data as CSV", filtered_df.to_csv(index=False), "filtered_data.csv")
