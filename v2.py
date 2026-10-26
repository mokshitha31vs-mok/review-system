from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

# Sample reviews for demonstration
reviews = [
    {"id": 1, "name": "Mokshitha", "rating": 5, "comment": "Excellent service!"},
    {"id": 2, "name": "Rahul", "rating": 4, "comment": "Good experience."}
]


HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Review System - V2</title>
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
        input, textarea, button {
            display: block;
            margin: 8px 0;
            padding: 8px;
        }
        button {
            background: #2980b9;
            color: white;
            border: none;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>Review System - V2 (Edit Review)</h1>
    <p>Update an existing review below.</p>

    {% for review in reviews %}
    <div class="review">
        <h3>Review ID: {{ review.id }}</h3>

        <form method="POST" action="{{ url_for('edit_review', review_id=review.id) }}">
            <label>Name:</label>
            <input type="text" name="name" value="{{ review.name }}" required>

            <label>Rating (1-5):</label>
            <input type="number" name="rating"
                   min="1" max="5" value="{{ review.rating }}" required>

            <label>Comment:</label>
            <textarea name="comment" required>{{ review.comment }}</textarea>

            <button type="submit">Update Review</button>
        </form>
    </div>
    {% endfor %}
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE, reviews=reviews)


@app.route("/edit_review/<int:review_id>", methods=["POST"])
def edit_review(review_id):
    review = next(
        (item for item in reviews if item["id"] == review_id),
        None
    )

    if review is None:
        return "Review not found", 404

    name = request.form.get("name", "").strip()
    comment = request.form.get("comment", "").strip()
    rating_text = request.form.get("rating", "").strip()

    if not name or not comment or not rating_text:
        return "All fields are required", 400

    try:
        rating = int(rating_text)
    except ValueError:
        return "Rating must be a number", 400

    if rating < 1 or rating > 5:
        return "Rating must be between 1 and 5", 400

    review["name"] = name
    review["rating"] = rating
    review["comment"] = comment

    return redirect(url_for("home"))


@app.route("/health")
def health():
    return {"status": "healthy", "version": "v2"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)