import streamlit as st
from storage import init_storage, save_entry
from llm_utils import (
    generate_user_response,
    generate_admin_summary,
    generate_recommended_action
)
from datetime import datetime


def run_user_dashboard():
    init_storage()

    st.title("📝 Submit Your Review")

    rating = st.selectbox("Select Rating", [1, 2, 3, 4, 5])
    review = st.text_area("Write your review")

    if st.button("Submit"):
        if review.strip():
            ai_response = generate_user_response(review, rating)
            summary = generate_admin_summary(review)
            action = generate_recommended_action(review, rating)

            save_entry({
                "timestamp": datetime.now(),
                "rating": rating,
                "review": review,
                "ai_response": ai_response,
                "ai_summary": summary,
                "ai_action": action
            })

            st.success("Thank you for your feedback!")
            st.subheader("AI Response")
            st.write(ai_response)
        else:
            st.warning("Please enter a review.")


# THIS MAKES IT WORK LOCALLY
if __name__ == "__main__":
    run_user_dashboard()
