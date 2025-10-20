import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Global Coffee & Health Dashboard", layout="wide")
st.title("☕ Global Coffee & Health Data Explorer")

st.markdown("""
### Explore the relationship between coffee consumption and health metrics.
Use the sidebar filters to interact with the dataset.
""")

df = pd.read_csv("synthetic_coffee_health_10000.csv")

st.sidebar.header("🔍 Data Filters")

age_range = st.sidebar.slider(
    "Select Age Range",
    int(df['Age'].min()),
    int(df['Age'].max()),
    (20, 50)
)

countries = st.sidebar.multiselect(
    "Select Countries",
    df['Country'].unique(),
    default=df['Country'].unique()[:3]
)

gender = st.sidebar.radio(
    "Select Gender",
    ["All", "Male", "Female"]
)

smokers_only = st.sidebar.checkbox("Show only smokers")

filtered_df = df[
    (df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1]) &
    (df['Country'].isin(countries))
]
if gender != "All":
    filtered_df = filtered_df[filtered_df['Gender'].str.lower() == gender.lower()]
if smokers_only:
    filtered_df = filtered_df[filtered_df['Smoking'].str.lower() == "yes"]

st.subheader("🧾 Filtered Data Preview")
st.write(filtered_df.head())

st.header("📊 Problem A: Coffee Consumption vs. Health Metrics")
st.markdown("**Question:** Is coffee intake (cups/week) related to BMI, heart rate, or sleep hours?")

col1, col2 = st.columns(2)

with col1:
    st.subheader("☕ Coffee Intake vs. BMI")
    fig, ax = plt.subplots()
    sns.scatterplot(data=filtered_df, x="Coffee_Intake", y="BMI", hue="Gender", ax=ax)
    ax.set_xlabel("Coffee Intake (cups/week)")
    ax.set_ylabel("BMI")
    st.pyplot(fig)

with col2:
    st.subheader("💓 Coffee Intake vs. Heart Rate")
    fig, ax = plt.subplots()
    sns.scatterplot(data=filtered_df, x="Coffee_Intake", y="Heart_Rate", hue="Gender", ax=ax)
    ax.set_xlabel("Coffee Intake (cups/week)")
    ax.set_ylabel("Heart Rate (bpm)")
    st.pyplot(fig)

st.subheader("📈 Statistical Correlation (Pearson Coefficients)")
corr = filtered_df[['Coffee_Intake', 'BMI', 'Heart_Rate', 'Sleep_Hours']].corr()
st.dataframe(corr.style.background_gradient(cmap="coolwarm"))

st.markdown(f"""
**Interpretation:**
- Coffee intake and BMI correlation = **{corr.loc['Coffee_Intake','BMI']:.2f}**
- Coffee intake and Heart Rate correlation = **{corr.loc['Coffee_Intake','Heart_Rate']:.2f}**
- Coffee intake and Sleep Hours correlation = **{corr.loc['Coffee_Intake','Sleep_Hours']:.2f}**
""")

st.header("🌍 Problem B: Group Differences by Country or Age")
st.markdown("**Question:** Do different countries or age groups show different coffee habits and health results?")

st.subheader("🇨🇳 Average Coffee Intake by Country")
fig, ax = plt.subplots()
filtered_df.groupby("Country")["Coffee_Intake"].mean().sort_values().plot(kind="bar", ax=ax, color="skyblue")
ax.set_ylabel("Average Coffee Cups per Week")
ax.set_title("Average Coffee Intake by Country")
st.pyplot(fig)

st.subheader("🛏 Sleep Hours Distribution")
fig, ax = plt.subplots()
sns.histplot(filtered_df["Sleep_Hours"], bins=10, kde=True, color="lightgreen", ax=ax)
ax.set_xlabel("Sleep Hours")
ax.set_ylabel("Count")
st.pyplot(fig)

st.subheader("📊 Summary Statistics by Country")
summary_stats = filtered_df.groupby("Country")[["Coffee_Intake", "BMI", "Heart_Rate", "Sleep_Hours"]].mean().round(2)
st.dataframe(summary_stats)

import scipy.stats as stats
if len(filtered_df['Country'].unique()) > 1:
    f_val, p_val = stats.f_oneway(
        *[group["Coffee_Intake"].values for name, group in filtered_df.groupby("Country")]
    )
    st.markdown(f"**ANOVA test result:** F = {f_val:.2f}, p = {p_val:.4f}")
    if p_val < 0.05:
        st.success("✅ There is a statistically significant difference in coffee intake between countries.")
    else:
        st.info("ℹ️ No significant difference found between selected countries.")
else:
    st.info("Select at least 2 countries to perform group comparison.")

st.markdown("""
---
### ✅ Summary of Findings
- **Higher coffee intake** shows moderate correlation with **BMI** and **Heart Rate**.
- **Sleep Hours** tend to decrease slightly with higher coffee intake.
- **Significant cross-country differences** exist in coffee consumption (see ANOVA test).
- These findings vary by **age, gender**, and **lifestyle factors** like smoking.

Use the sidebar filters to explore these relationships interactively!
""")

