from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from caching_helper_func import get_cached_all_products, cache_all_products, get_cached_product, cache_product, \
    invalidate_cache

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


@app.route('/products', methods=['GET'])
def get_all_products():
    """Get all products with caching"""

    # Step 1: Check cache first
    cached = get_cached_all_products()
    if cached:
        # Cache HIT!
        response = jsonify(cached)
        response.headers['X-Cache-Status'] = 'HIT'
        return response, 200

    # Step 2: Cache MISS - query database
    products = Product.query.all()
    products_list = [p.to_dict() for p in products]

    # Step 3: Store in cache for next time
    cache_all_products(products_list)

    # Step 4: Return with cache status header
    response = jsonify(products_list)
    response.headers['X-Cache-Status'] = 'MISS'
    return response, 200


@app.route('/products/<int:product_id>', methods=["GET"])
def get_single_product(product_id):
    """
    Return a specific product.
    """
    cached = get_cached_product(product_id)
    if cached:
        # Cache HIT!
        response = jsonify(cached)
        response.headers['X-Cache-Status'] = 'HIT'
        return response, 200

    product = Product.query.get(product_id)
    if product:
        cache_product(product_id,product.to_dict())
        response = jsonify(product.to_dict())
        response.headers['X-Cache-Status'] = 'MISS'
        return response, 200
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
        invalidate_cache()
        return jsonify({"message": "Item added successfully", "item": new_product.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update a product"""
    request_data = request.get_json()
    cached = get_cached_product(product_id)
    if cached:
        # Cache HIT!
        product = jsonify(cached)
    else:
        # Cache MISS!
        product = Product.query.get(product_id)

    product.name = request_data['name']
    product.description = request_data['description']
    product.price = request_data['price']
    product.category = request_data['category']
    db.session.commit()
    invalidate_cache(product_id)
    return jsonify({"message": "Item updated successfully", "item": product.to_dict()}), 201


@app.route('/products/<int:product_id>', methods=["DELETE"])
def delete_product(product_id):
    """
    Delete a specific product.
    """
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        invalidate_cache(product_id)
        return jsonify({"message":"Product successfully deleted."})
    return jsonify({"message":"Item Not Found"}), 404

# Create tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)