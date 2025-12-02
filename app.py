from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://inventory_user:inventory_pass@localhost:2345/inventory_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, default=0.0)
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category': self.category,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

@app.route('/health')
def health():
    return {"status": "healthy"}

@app.route('/products',methods=["GET"])
def get_all_products():
    """
    Returns a list of all items.
    """
    data = Product.query.all()
    data = [product.to_dict() for product in data]
    return jsonify(data), 200


@app.route('/products/<int:product_id>', methods=["GET"])
def get_single_product(product_id):
    """
    Return a specific product.
    """
    product = Product.query.get(product_id)
    if product:
        return jsonify(product.to_dict()), 200
    return jsonify({"message":"Item Not Found"}), 404

@app.route('/products',methods=["POST"])
def create_product():
    """
    Create new product and add it to the list of existing products.
    """
    data = request.get_json()

    if not data or 'name' not in data:
        return jsonify({"error": "Invalid data. 'name' is required."}), 400
    try:
        new_product = Product(
            name=data['name'],
            description=data.get('description'),
            price = data.get('price'),
            category = data.get('category'),
            )
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"message": "Item added successfully", "item": new_product.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@app.route('/products/<int:product_id>', methods=["DELETE"])
def delete_product(product_id):
    """
    Delete a specific product.
    """
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message":"Product successfully deleted."})
    return jsonify({"message":"Item Not Found"}), 404

# Create tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)