def process_reviews(reviews):
    text_entries = []
    for entry in reviews:
        if (entry, dict):  # Ensure it's a dictionary
            review_text = entry.get("Review_Text")  # Adjust key name as per your JSON structure
            review_title = entry.get("Review_Heading")  # Adjust key name as per your JSON structure
            text_entries.append(review_text)
            text_entries.append(review_title)

    print(text_entries)
    return text_entries

def detailed_reviews(reviews):
    text_entries = []
    for entry in reviews:
        if (entry, dict):  # Ensure it's a dictionary
            text_entries.append(entry)

    print(text_entries)
    return text_entries
