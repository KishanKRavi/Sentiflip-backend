from django.http import JsonResponse
from .scraper.flipkart_scraper import search_product, reviewAllPages
from .scraper.review_processor import process_reviews, detailed_reviews
from .scraper.sentiment_analyzer import analyze_sentiments
from .scraper.geminiAPI import gemeniAPI
# Search Product API
def search_products(request):
    query = request.GET.get('query')
    if not query:
        return JsonResponse({'error': 'No query provided.'}, status=400)
    products = search_product(query)
    return JsonResponse({'products': products})
# Analyze Product Reviews API
def analyze_product_reviews(request):
    url = request.GET.get('url')
    if not url:
        return JsonResponse({'error': 'No URL provided.'}, status=400)
    # Scrape reviews
    all_reviews = reviewAllPages(url)
    if not all_reviews:
        return JsonResponse({'error': 'No reviews found.'}, status=404)
    # Preprocess
    processed_reviews = process_reviews(all_reviews)
    detailed_reviews_collection = detailed_reviews(all_reviews)
    # Sentiment analysis with all data
    sentiment_result = analyze_sentiments(processed_reviews)
    return JsonResponse({
        "positive_percent": sentiment_result["positive_percent"],
        "negative_percent": sentiment_result["negative_percent"],
        "neutral_percent": sentiment_result["neutral_percent"],
        "overall_score": sentiment_result["overall_score"],
        "sentiment_label": sentiment_result["sentiment_label"],
        "final_verdict": sentiment_result["final_verdict"],
        "pros_keywords": sentiment_result["pros_keywords"],
        "cons_keywords": sentiment_result["cons_keywords"],
        "top_positive_reviews": sentiment_result["top_positive_reviews"],
        "top_negative_reviews": sentiment_result["top_negative_reviews"],
        "reviews": detailed_reviews_collection,
    })
# Gemini API
def geminiAPI(request):
    query = request.GET.get('title')
    if not query:
        return JsonResponse({'error': 'No query provided.'}, status=400)
    products = gemeniAPI(query)
    return JsonResponse({'details_of_product': products})
