from flask import Flask, redirect, url_for, render_template_string

app = Flask(__name__)

# Sample reviews for demonstration
reviews = [
    {"id": 1, "name": "Mokshitha", "rating": 5, "comment": "Excellent service!"},
    {"id": 2, "name": "Rahul", "rating": 4, "comment": "Good experience."},
    {"id": 3, "name": "Priya", "rating": 3, "comment": "Average experience."}
]


HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Review System - V3</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            background: #f4f6f9;
        }
        h1 { color: #2c3e50; }
        .review {
            background: white;
            padding: 15px;
            margin: 15px 0;
            border-radius: 8px;
        }
        button {
            background: #e74c3c;
            color: white;
            border: none;
            padding: 10px 15px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>Review System - V3 (Delete Review)</h1>
    <p>Delete reviews that are no longer required.</p>

    {% for review in reviews %}
    <div class="review">
        <h3>{{ review.name }}</h3>
        <p><strong>Review ID:</strong> {{ review.id }}</p>
        <p><strong>Rating:</strong> {{ review.rating }}/5</p>
        <p><strong>Comment:</strong> {{ review.comment }}</p>

        <form method="POST"
              action="{{ url_for('delete_review', review_id=review.id) }}"
              onsubmit="return confirm('Are you sure you want to delete this review?');">
            <button type="submit">Delete Review</button>
        </form>
    </div>
    {% else %}
    <p>No reviews available.</p>
    {% endfor %}
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE, reviews=reviews)


@app.route("/delete_review/<int:review_id>", methods=["POST"])
def delete_review(review_id):
    review = next(
        (item for item in reviews if item["id"] == review_id),
        None
    )

    if review is None:
        return "Review not found", 404

    reviews.remove(review)

    return redirect(url_for("home"))


@app.route("/health")
def health():
    return {"status": "healthy", "version": "v3"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)