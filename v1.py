from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

# Store submitted reviews temporarily
reviews = []

# HTML page for adding and displaying reviews
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Review System - V1</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f1f5f9;
            margin: 0;
            padding: 30px;
        }

        .container {
            max-width: 650px;
            margin: auto;
            background-color: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 3px 12px #cccccc;
        }

        h1 {
            color: #1e3a8a;
            text-align: center;
        }

        h2 {
            color: #334155;
            margin-top: 30px;
        }

        label {
            display: block;
            margin-top: 15px;
            font-weight: bold;
        }

        input, select, textarea {
            width: 100%;
            padding: 10px;
            margin-top: 6px;
            box-sizing: border-box;
            border: 1px solid #cbd5e1;
            border-radius: 5px;
        }

        button {
            margin-top: 20px;
            padding: 12px 20px;
            background-color: #2563eb;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
        }

        button:hover {
            background-color: #1d4ed8;
        }

        .review {
            background-color: #eff6ff;
            padding: 15px;
            margin-top: 12px;
            border-radius: 8px;
            overflow-wrap: anywhere;
        }

        .empty {
            color: #64748b;
        }
    </style>
</head>

<body>
    <div class="container">
        <h1>Review System - V1</h1>
        <p>Submit your product review below.</p>

        <form action="/add_review" method="POST">

            <label for="product">Product Name</label>
            <input
                type="text"
                id="product"
                name="product"
                maxlength="100"
                required
            >

            <label for="rating">Rating</label>
            <select id="rating" name="rating" required>
                <option value="">Select a rating</option>
                <option value="1">1 - Poor</option>
                <option value="2">2 - Fair</option>
                <option value="3">3 - Good</option>
                <option value="4">4 - Very Good</option>
                <option value="5">5 - Excellent</option>
            </select>

            <label for="comment">Review Comment</label>
            <textarea
                id="comment"
                name="comment"
                rows="4"
                maxlength="1000"
                required
            ></textarea>

            <button type="submit">Submit Review</button>
        </form>

        <h2>Submitted Reviews</h2>

        {% if reviews %}
            {% for review in reviews %}
                <div class="review">
                    <strong>Product:</strong> {{ review.product }}<br>
                    <strong>Rating:</strong> {{ review.rating }}/5<br>
                    <strong>Comment:</strong> {{ review.comment }}
                </div>
            {% endfor %}
        {% else %}
            <p class="empty">No reviews submitted yet.</p>
        {% endif %}
    </div>
</body>
</html>
"""


@app.route("/")
def home():
    return redirect(url_for("show_reviews"))


@app.route("/reviews")
def show_reviews():
    return render_template_string(
        HTML_PAGE,
        reviews=reviews
    )


@app.route("/add_review", methods=["POST"])
def add_review():
    product = request.form.get("product", "").strip()
    rating_text = request.form.get("rating", "").strip()
    comment = request.form.get("comment", "").strip()

    # Validate required fields
    if not product or not rating_text or not comment:
        return "All fields are required.", 400

    # Validate input lengths
    if len(product) > 100 or len(comment) > 1000:
        return "Input exceeds the allowed length.", 400

    # Validate rating
    try:
        rating = int(rating_text)
    except ValueError:
        return "Rating must be a number between 1 and 5.", 400

    if rating < 1 or rating > 5:
        return "Rating must be between 1 and 5.", 400

    # Create and store the review
    review = {
        "product": product,
        "rating": rating,
        "comment": comment
    }

    reviews.append(review)

    # Return to the reviews page
    return redirect(url_for("show_reviews"))


@app.route("/health")
def health():
    return {
        "status": "healthy",
        "version": "v1"
    }, 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )