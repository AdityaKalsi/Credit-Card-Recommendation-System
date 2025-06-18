import streamlit as st
import requests
import pandas as pd
from recommendation_module import recommend_cards

# ---- Step 1: Define Questions ----
questions = [
    {"key": "max_joining_fee", "text": "What is the maximum joining fee you are willing to pay?"},
    {"key": "max_renewal_fee", "text": "What is the maximum annual/renewal fee you are comfortable with?"},
    {"key": "reward_preferences", "text": "What types of rewards do you prefer (e.g., travel, Zomato, Amazon, Personal Accident Cover)?"},
    {"key": "welcome_bonus_preference", "text": "Do you prefer cards with a welcome bonus? (yes/no)"}
]

st.title("💳 Credit Card Advisor (LLM + Ollama)")

# ---- Step 2: Form for All Questions ----
with st.form("user_form"):
    answers = {}
    for q in questions:
        answers[q["key"]] = st.text_input(q["text"], key=q["key"])

    submitted = st.form_submit_button("Submit")

# ---- Step 3: After Submission ----
if submitted:
    st.session_state.answers = answers

    # Preprocess inputs
    try:
        user_input = {
            'max_joining_fee': int(answers['max_joining_fee']),
            'max_renewal_fee': int(answers['max_renewal_fee']),
            'reward_preferences': answers['reward_preferences'],
            'welcome_bonus_preference': answers['welcome_bonus_preference'].strip().lower() == 'yes'
        }
    except Exception as e:
        st.error(f"Invalid input: {e}")
        st.stop()

    st.success("✅ Inputs received. Generating recommendations...")

    # ---- Step 4: Get Recommendations ----
    results = recommend_cards(user_input)

    # ---- Step 5: Display Results ----
    if isinstance(results, str):
        st.warning(results)
    else:
        st.markdown("## 🏆 Top Card Recommendations")

        # Store for chat context
        st.session_state.recommended_cards = results.to_dict(orient='records')

        # Build context string for LLM
        card_context = "\n\n".join(
            f"Card Name: {card['Card Name']}\nUSP: {card['USP']}\nPros: {card['Pros']}\nCons: {card['Cons']}"
            for card in st.session_state.recommended_cards
        )
        st.session_state.card_context = card_context

        # Show each card in UI
        for _, row in results.iterrows():
            with st.container():
                st.subheader(row['Card Name'])
                if 'Image URL' in row and isinstance(row['Image URL'], str):
                    st.image(row['Image URL'], width=300)
                st.markdown(f"**Joining Fees:** {row['Joining Fees']}")
                st.markdown(f"**Renewal Fees:** {row['Renewal Fees']}")
                st.markdown(f"**USP:** {row['USP']}")
                st.markdown(f"**Similarity Score:** {row['Similarity Score']:.2f}")
                st.markdown("### ✅ Pros")
                st.write(row['Pros'])
                st.markdown("### ❌ Cons")
                st.write(row['Cons'])
                st.markdown(f"[🔗 Card Link]({row['Card Page Link']})")
                st.markdown("---")

        # ---- Step 6: Link to Chat Page ----
        st.success("🎉 Want to ask questions about these cards?")
        if st.button("💬 Ask the Advisor"):
            st.switch_page("pages/main.py")
