from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(1024), nullable=True)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(255), nullable=False)
    date_of_sale = db.Column(db.String(50), nullable=False)
    sold = db.Column(db.Boolean, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "category": self.category,
            "date_of_sale": self.date_of_sale,
            "sold": self.sold
        }

