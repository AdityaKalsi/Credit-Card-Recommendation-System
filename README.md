# **💳 Credit Card Recommendation System (LLM + Streamlit + Ollama)**

<p>&nbsp;</p>

This end-to-end system intelligently recommends credit cards to users based on their preferences and budget. It combines:

- **An intelligent rule-based recommendation engine**
- **A conversational LLM assistant for follow-up queries**
- **A clean, modern UI powered by Streamlit**

The assistant answers questions about the recommended cards using **contextual memory** and **LangChain**, while the recommendation logic filters cards based on real-time inputs like fees, reward preferences, and welcome bonuses.

---

![Alt Text](https://github.com/AdityaKalsi/Credit-Card-Recommendation-System/blob/10c0545b0ba6b792441a8738936fc94064b99e0b/Screenshot%202025-06-18%20144945.png)
![Alt Text](https://github.com/AdityaKalsi/Credit-Card-Recommendation-System/blob/ea952aab4df53941e7be05dc181d2f7fd47ffe7e/Screenshot%202025-06-18%20145528.png)
![Alt Text](https://github.com/AdityaKalsi/Credit-Card-Recommendation-System/blob/113e54acc1f8a0aa4594f7b077a0f590a05c698f/Screenshot%202025-06-18%20154258.png)

---

## **📥 Data Collection**

To build a useful recommendation system, we first gathered data from trusted banking portals and financial comparison websites using custom **web scraping scripts**.

### Scraped Features:
- Card Name
- Joining Fee and Renewal Fee
- USP (Unique Selling Proposition)
- Pros & Cons
- Card Image URLs
- Official Application Links

Once scraped, the data was cleaned, deduplicated, and saved to `final_credit_card.csv`.

---

## 🔍 Recommendation Engine

The heart of this project lies in an intelligent recommendation engine (`recommendation_module.py`) that combines advanced NLP techniques with smart filtering and user-driven customization to deliver personalized credit card suggestions.

---

### 📥 Data Preprocessing Pipeline

1. **Data Ingestion and Parsing**  
   The dataset is loaded from `final_card_data.csv`. A key column, `'Rewards and Benefits'`, contains a stringified dictionary, which is parsed using `ast.literal_eval()` into structured Python dictionaries.

2. **Cleaning and Standardizing Reward Information**  
   The parsed reward dictionaries are cleaned to remove 'N/A' values and irrelevant entries. These are converted to plain-text using a function (`rewards_to_text`) so they can be vectorized later.

3. **Cleaning Joining and Renewal Fees**  
   Textual fee entries are cleaned using `clean_joining_fee` and `clean_renewal_fee`. This involves:
   - Handling `NaN`, `nil`, and `free` values
   - Extracting numeric parts from messy strings  
   The cleaned values are stored in `Joining Fees Cleaned` and `Renewal Fees Cleaned`.

4. **Combining Key Features**  
   A new column `combined_features` is created by merging `USP` (Unique Selling Proposition) with the textual benefits. These are split into sentences and stored in `combined_features_list`.

5. **Creating Enriched Feature Set**  
   `main_features` merges `Annual Fee` (if available) with the combined sentence list, preparing a strong textual representation for NLP analysis.

---

### 🧠 AI-Powered Recommendation Logic

1. **Hybrid Feature Engineering (Text + Numeric)**  
   Combines structured fields (fees) with unstructured text (USP, rewards) for holistic representation. Textual benefits are converted into a natural, user-like language.

2. **Advanced Keyword Extraction using spaCy**  
   Uses `spaCy` to extract:
   - Noun chunks (e.g., "airport lounge access")
   - Named entities (e.g., "Amazon", "Zomato")
   - Key descriptors (nouns, adjectives)  
   This results in a rich `keywords` column capturing human-like understanding of card benefits.

3. **TF-IDF Vectorization for Semantic Matching**  
   All extracted keyword features are transformed into vectors using TF-IDF. This ensures each card's features are numerically comparable and emphasizes important but unique terms.

4. **User-Driven Cosine Similarity Matching**  
   - User enters preferences: reward type, fee limits, and bonus preference.
   - Input is vectorized and compared with each card using cosine similarity.
   - Top N cards with highest alignment are returned.

5. **Behavioral Boosting with Welcome Bonus**  
   If a user prefers welcome bonuses, the system adds a score boost to cards with strong USP descriptions, aligning output with user *intent*, not just content.

6. **Smart Filtering Before Ranking**  
   The model first filters cards based on user fee limits (`max_joining_fee`, `max_renewal_fee`) before applying NLP, reducing computation and improving relevance.





---

## **🖼️ UI & Input Flow**

Built using **Streamlit**, the interface is clean and interactive.

- The form takes user preferences.
- Once submitted, the backend filters and ranks relevant cards.
- The top recommendations are displayed with:
  - Card Image
  - Joining & Renewal Fee
  - USP, Pros, Cons
  - Similarity Score
  - Apply Now button
- Recommendations are also passed to the chatbot context via `st.session_state`.

---
![Alt text](https://github.com/AdityaKalsi/Credit-Card-Recommendation-System/blob/a8ede1e14003665a08317bb1982e77e0f4b6339b/Screenshot%202025-06-18%20145305.png)
![Alt text](https://github.com/AdityaKalsi/Credit-Card-Recommendation-System/blob/d26482eb33d54bb745733e2de25c3bb63415eaba/Screenshot%202025-06-18%20140908.png)

## **🧠 LLM Chat Assistant (LangChain + Ollama)**

Users can click **"Ask the Advisor"** to initiate the conversational agent. The agent uses:

1. 🧠 LLM as an Interactive Explainer for Card Recommendations
The core recommendation logic (recommendation_module.py) handles the selection and ranking of credit cards based on user constraints like joining fees, renewal fees, reward types, and welcome bonus preferences.

Once recommendations are generated, the LLM does not participate in decision-making — instead, it becomes active after the cards are selected, acting as a personal credit card assistant to answer user queries about those specific cards.

2. 📄 Context Injection via Card Summary for Grounded Responses
To ensure accurate and relevant LLM responses, the app builds a structured card_context string summarizing all recommended cards' key details (name, USP, pros, cons).

This context is injected into the LLM system prompt before any user query is processed.

As a result, the LLM operates with full awareness of what was recommended — allowing it to answer follow-up questions like:

“Which card has the lowest joining fee?”

“Which one is best for travel?”
without hallucinating or straying off-topic.

3. 💬 Session-Based Conversational Memory for Multi-Turn Chat
The LLM chat interface (main.py) uses LangChain’s RunnableWithMessageHistory to maintain a chat memory that persists across user interactions.

Each session has a unique session_id, enabling contextual continuity, where the LLM can handle multi-turn conversations like:

User: “Which one has cashback?”
User: “Okay, and does that one have a welcome bonus?”

This makes the experience feel natural and dialogue-driven, rather than one-off responses.

4. 🔄 Seamless Integration with Streamlit Frontend
On the frontend:

app.py handles user inputs and displays recommendations.

main.py manages the LLM-based follow-up interaction.

Once the cards are recommended, the app stores their information (recommended_cards and card_context) in st.session_state.

If the user clicks “💬 Ask the Advisor”, Streamlit switches to the chat page, and the LLM is bootstrapped with the same session context — providing a fluid, cross-page experience without data loss or reset.

5. 🧩 LLM Complements Logic by Enhancing Explainability and Engagement
The LLM doesn’t replace traditional logic but complements it by:

Clarifying recommendations through natural language.

Answering subjective queries (e.g., “Which card is better for students?”).

Enabling comparisons in a user-friendly, conversational format.

This results in a hybrid architecture where rule-based systems offer precision, and the LLM provides engagement, clarity, and trust through an AI-powered conversational layer.
## **🛠️ Tech Stack**

- **Frontend**: Streamlit
- **Backend**: Python
- **Recommendation Logic**: Pandas, custom scoring
- **Chatbot**: LangChain + Ollama (Mistral)
- **Scraping**: BeautifulSoup, requests
- **LLM**: Mistral (run locally via Ollama)


