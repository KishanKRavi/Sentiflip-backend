# yourapp/utils/analyze_sentiments.py
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from collections import Counter
import re

nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

def clean_text(text):
    return re.sub(r'[^\w\s]', '', text.lower())

def extract_keywords(reviews, top_n=5):
    all_words = []
    for review, _ in reviews:
        words = clean_text(review).split()
        all_words.extend(words)
    common_words = Counter(all_words).most_common(top_n)
    return [word for word, _ in common_words if word not in ['the', 'is', 'was', 'very', 'and', 'this', 'with']]

def analyze_sentiments(reviews):
    sentiment_data = {"positive": [], "negative": [], "neutral": [], "scores": []}

    for review in reviews:
        score = sia.polarity_scores(review)
        compound = score['compound']
        sentiment_data["scores"].append(compound)
        if compound >= 0.5:
            sentiment_data["positive"].append((review, compound))
        elif compound <= -0.5:
            sentiment_data["negative"].append((review, compound))
        else:
            sentiment_data["neutral"].append((review, compound))

    total = len(reviews)
    pos_count, neg_count, neu_count = map(len, [sentiment_data["positive"], sentiment_data["negative"], sentiment_data["neutral"]])
    avg_score = sum([(x + 1) * 50 for x in sentiment_data["scores"]]) / total

    def get_sentiment_label(score):
        if score >= 85: return "Very Positive"
        elif score >= 70: return "Positive"
        elif score >= 40: return "Neutral"
        elif score >= 20: return "Negative"
        else: return "Very Negative"

    def get_final_verdict(score, positive_percent):
        if score > 75 and positive_percent > 60: return "Highly Recommended ✅"
        elif score > 60: return "Recommended 👍"
        elif score > 45: return "Consider Alternatives ⚠️"
        else: return "Not Recommended ❌"

    return {
        "positive_percent": round((pos_count / total) * 100, 2),
        "negative_percent": round((neg_count / total) * 100, 2),
        "neutral_percent": round((neu_count / total) * 100, 2),
        "overall_score": round(avg_score, 2),
        "sentiment_label": get_sentiment_label(avg_score),
        "final_verdict": get_final_verdict(avg_score, (pos_count / total) * 100),
        "top_positive_reviews": [r[0] for r in sorted(sentiment_data["positive"], key=lambda x: x[1], reverse=True)[:3]],
        "top_negative_reviews": [r[0] for r in sorted(sentiment_data["negative"], key=lambda x: x[1])[:3]],
        "pros_keywords": extract_keywords(sentiment_data["positive"]),
        "cons_keywords": extract_keywords(sentiment_data["negative"]),
    }
