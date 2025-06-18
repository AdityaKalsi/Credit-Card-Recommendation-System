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

### 🎯 Output

A sorted list of top-N recommended credit cards, each with:
- 🖼️ Image  
- 🃏 Card Name  
- 💰 Joining & Renewal Fees  
- 🌟 USP (Key Selling Point)  
- ✅ Pros & ❌ Cons  
- 🔗 Card Page Link  
- 📈 Similarity Score (for tr




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

- LangChain’s `RunnableWithMessageHistory`
- Ollama’s **Mistral** LLM running locally
- Chat history memory using `ChatMessageHistory`

### Context Injection:
The top recommended cards are formatted into a string with their:
- Name
- USP
- Pros and Cons

This is passed into the LLM context so it can only answer based on the shown cards.

### Example Questions the LLM Can Handle:
- “Which card is good for travel?”
- “Which one has the lowest fee?”
- “Do any of these offer free lounge access?”

The chatbot only answers questions about the currently displayed recommendations.

---

## **🎯 Key Features**

### Recommendation Engine:
- Budget-based filtering
- Reward preference matching using keyword scoring
- Welcome bonus filtering
- Ranked output with similarity score

### LLM Chat Assistant:
- Conversational query answering
- Limited context (top recommended cards only)
- Session-based memory
- Real-time interaction with LangChain

### UI/UX:
- Clean and intuitive Streamlit layout
- Visual card listings
- Seamless transition to chatbot
- "Apply Now" buttons and card images

---

## **🛠️ Tech Stack**

- **Frontend**: Streamlit
- **Backend**: Python
- **Recommendation Logic**: Pandas, custom scoring
- **Chatbot**: LangChain + Ollama (Mistral)
- **Scraping**: BeautifulSoup, requests
- **LLM**: Mistral (run locally via Ollama)


