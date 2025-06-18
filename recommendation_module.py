from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import pandas as pd

df = pickle.load(open('df_new.pkl', 'rb'))

vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(df['keywords'])

def recommend_cards(user_input, top_n=3):
    """
    Recommends top N credit cards based on user input preferences.

    Parameters:
    - user_input: dict with keys:
        'max_joining_fee' (int),
        'max_renewal_fee' (int),
        'reward_preferences' (str),
        'welcome_bonus_preference' (bool)

    Returns:
    - DataFrame of top recommended cards with details
    """
    
    filtered_df = df.copy()
    if 'max_joining_fee' in user_input:
        filtered_df = filtered_df[
            pd.to_numeric(filtered_df['Joining Fees Cleaned'], errors='coerce').fillna(0) <= user_input['max_joining_fee']
        ]
    if 'max_renewal_fee' in user_input:
        filtered_df = filtered_df[
            pd.to_numeric(filtered_df['Renewal Fees Cleaned'], errors='coerce').fillna(0) <= user_input['max_renewal_fee']
        ]

    if filtered_df.empty:
        return "No cards match your fee preferences."

    
    user_query = user_input.get('reward_preferences', '')
    user_vector = vectorizer.transform([user_query])

    
    similarity_scores = cosine_similarity(user_vector, tfidf_matrix[filtered_df.index]).flatten()

    
    if user_input.get('welcome_bonus_preference', False):
        bonus_boost = filtered_df['USP'].apply(lambda x: 0.1 if isinstance(x, str) and len(x) > 10 else 0)
        similarity_scores += bonus_boost.values

    
    top_indices = similarity_scores.argsort()[::-1][:top_n]
    recommendations = filtered_df.iloc[top_indices].copy()
    recommendations['Similarity Score'] = similarity_scores[top_indices]

    
    return recommendations[
        ['Card Name', 'Joining Fees', 'Renewal Fees', 'USP', 'Card Page Link', 'combined_features','Pros','Cons' ,'Similarity Score']
    ]