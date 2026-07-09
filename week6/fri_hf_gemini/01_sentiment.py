from transformers import pipeline

sentiment = pipeline("sentiment-analysis")

result = sentiment("I love this restaurant, the food was amazing!")

reviews = [
    "The pasta was cold and undercooked.",
    "Best pizza I've had in years!",
    "It was fine, nothing special.",
    "The waiter was rude and slow.",
]

results = sentiment(reviews)

for review, r in zip(reviews, results):
    print(f"{r['label']} ({r['score']:.2f}) — {review}")

print(result)