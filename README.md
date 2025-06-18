# **💳 Credit Card Recommendation System (LLM + Streamlit + Ollama)**

<p>&nbsp;</p>

This end-to-end system intelligently recommends credit cards to users based on their preferences and budget. It combines:

- **An intelligent rule-based recommendation engine**
- **A conversational LLM assistant for follow-up queries**
- **A clean, modern UI powered by Streamlit**

The assistant answers questions about the recommended cards using **contextual memory** and **LangChain**, while the recommendation logic filters cards based on real-time inputs like fees, reward preferences, and welcome bonuses.

---


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

Once scraped, the data was cleaned, deduplicated, and saved to `data/credit_cards.csv`.

---

## **🔍 Recommendation Engine**

Implemented in `recommendation_module.py`, the engine takes user preferences and matches them with cards in the dataset.

### User Input:
Collected through a Streamlit form:
- Max Joining Fee
- Max Renewal Fee
- Reward Preferences (keywords like cashback, travel, fuel, etc.)
- Welcome Bonus Preference (boolean)

### Core Logic:
- Filters cards based on max fee inputs.
- Calculates a similarity score between user keywords and the USP, pros, cons.
- Optionally filters for cards mentioning welcome bonuses.
- Sorts cards based on similarity score.

### Output:
A sorted DataFrame of top recommended cards.

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


