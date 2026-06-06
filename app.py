import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Netflix Analytics", layout="wide")
st.title("🎬 Netflix Subscriber & Revenue Risk Dashboard")

# Read data sheet inside the app
df = pd.read_csv('Netflix Userbase.csv')
df['Join Date'] = pd.to_datetime(df['Join Date'])
df['Last Payment Date'] = pd.to_datetime(df['Last Payment Date'])
df['Lifespan_Days'] = (df['Last Payment Date'] - df['Join Date']).dt.days

# Sidebar Filter Group
st.sidebar.header("Dashboard Filters")
country_choice = st.sidebar.selectbox("Select Region", options=['All Matrix'] + list(df['Country'].unique()))

if country_choice != 'All Matrix':
    filtered_df = df[df['Country'] == country_choice]
else:
    filtered_df = df

# Metric Value Blocks
rev = filtered_df['Monthly Revenue'].sum()
days = filtered_df['Lifespan_Days'].mean()

c1, c2 = st.columns(2)
with c1:
    st.metric(label="Total Monitored Monthly Revenue", value=f"${rev:,.2f}")
with c2:
    st.metric(label="Average User Retention (Days)", value=f"{days:.1f} Days")

st.markdown("---")

# Visual Charts Setup
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Revenue Contribution by Account Tier")
    fig, ax = plt.subplots()
    sns.barplot(data=filtered_df, x='Subscription Type', y='Monthly Revenue', estimator=sum, ax=ax, palette='dark:red_r')
    st.pyplot(fig)

with chart_col2:
    st.subheader("Subscriber Device Usage Breakdown")
    fig, ax = plt.subplots()
    filtered_df['Device'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax, colors=['#e50914','#222222','#b3b3b3','#f5f5f1'])
    ax.set_ylabel('')
    st.pyplot(fig)
