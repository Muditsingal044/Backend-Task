from models import db, Product

def initialize_db(data):
    """Initialize the database with seed data."""
    db.drop_all()
    db.create_all()

    for item in data:
        product = Product(
            title=item["title"],
            description=item.get("description", ""),
            price=float(item["price"]),
            category=item["category"],
            date_of_sale=item["dateOfSale"],
            sold=bool(item["sold"])
        )
        db.session.add(product)

    db.session.commit()

