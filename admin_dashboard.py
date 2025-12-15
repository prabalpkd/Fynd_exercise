import streamlit as st
from storage import load_entries

st.title("📊 Admin Dashboard")

df = load_entries()

if df.empty:
    st.info("No reviews yet.")
else:
    st.metric("Total Reviews", len(df))
    st.metric("Average Rating", round(df["rating"].mean(), 2))

    st.subheader("All Submissions")
    st.dataframe(df.sort_values("timestamp", ascending=False))

    st.subheader("Rating Distribution")
    st.bar_chart(df["rating"].value_counts().sort_index())
