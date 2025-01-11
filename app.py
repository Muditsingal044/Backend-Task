from flask import Flask, request, jsonify
from models import db, Product
from database import initialize_db
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/initialize', methods=['GET'])
def initialize():
    """Fetch and initialize the database with seed data."""
    response = requests.get("https://s3.amazonaws.com/roxiler.com/product_transaction.json")
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data"}), 500

    data = response.json()
    initialize_db(data)
    return jsonify({"message": "Database initialized with seed data"}), 200


@app.route('/transactions', methods=['GET'])
def list_transactions():
    """List all transactions with search and pagination."""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    search = request.args.get('search', '')

    query = Product.query
    if search:
        query = query.filter((Product.title.ilike(f'%{search}%')) |
                             (Product.description.ilike(f'%{search}%')) |
                             (Product.price.like(f'%{search}%')))
    transactions = query.paginate(page, per_page, False).items

    return jsonify([product.to_dict() for product in transactions]), 200


@app.route('/statistics', methods=['GET'])
def statistics():
    """Get statistics for the selected month."""
    month = request.args.get('month', '').capitalize()
    products = Product.query.filter(Product.date_of_sale.contains(f"-{month}-")).all()

    total_sales = sum([product.price for product in products if product.sold])
    sold_items = len([product for product in products if product.sold])
    not_sold_items = len([product for product in products if not product.sold])

    return jsonify({
        "total_sales": total_sales,
        "sold_items": sold_items,
        "not_sold_items": not_sold_items
    }), 200


@app.route('/bar_chart', methods=['GET'])
def bar_chart():
    """Generate a bar chart response."""
    month = request.args.get('month', '').capitalize()
    products = Product.query.filter(Product.date_of_sale.contains(f"-{month}-")).all()

    ranges = {
        "0-100": 0, "101-200": 0, "201-300": 0, "301-400": 0,
        "401-500": 0, "501-600": 0, "601-700": 0, "701-800": 0,
        "801-900": 0, "901-above": 0
    }

    for product in products:
        if product.price <= 100:
            ranges["0-100"] += 1
        elif product.price <= 200:
            ranges["101-200"] += 1
        elif product.price <= 300:
            ranges["201-300"] += 1
        elif product.price <= 400:
            ranges["301-400"] += 1
        elif product.price <= 500:
            ranges["401-500"] += 1
        elif product.price <= 600:
            ranges["501-600"] += 1
        elif product.price <= 700:
            ranges["601-700"] += 1
        elif product.price <= 800:
            ranges["701-800"] += 1
        elif product.price <= 900:
            ranges["801-900"] += 1
        else:
            ranges["901-above"] += 1

    return jsonify(ranges), 200


@app.route('/pie_chart', methods=['GET'])
def pie_chart():
    """Generate a pie chart response."""
    month = request.args.get('month', '').capitalize()
    products = Product.query.filter(Product.date_of_sale.contains(f"-{month}-")).all()

    category_counts = {}
    for product in products:
        category_counts[product.category] = category_counts.get(product.category, 0) + 1

    return jsonify(category_counts), 200


@app.route('/combined', methods=['GET'])
def combined():
    """Fetch combined data from all APIs."""
    month = request.args.get('month', '').capitalize()
    stats = statistics().json
    bar = bar_chart().json
    pie = pie_chart().json

    return jsonify({
        "statistics": stats,
        "bar_chart": bar,
        "pie_chart": pie
    }), 200


if __name__ == '__main__':
    app.run(debug=True)
