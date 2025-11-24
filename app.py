from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data (can be replaced with database interaction)
data = [
        {"id": 1, "name": "A", "description": "This is item A"},
        {"id": 2, "name": "B", "description": "This is item B"},
        {"id": 3, "name": "C", "description": "This is item C"},
    ]

@app.route('/health')
def health():
    return {"status": "healthy"}

@app.route('/get_products',methods=["GET"])
def get_all_products():
    """
    Returns a list of all items.
    """
    return jsonify(data), 200


@app.route('/get_product/<int:product_id>', methods=["GET"])
def get_single_product(product_id):
    """
    Return a specific product.
    """
    product = next((product for product in data if product['id'] == product_id), None)
    if product:
        return jsonify(product), 200
    return jsonify({"message":"Item Not Found"}), 404

@app.route('/create_product',methods=["POST"])
def create_product():
    """
    Create new product and add it to the list of existing products.
    """
    new_product = request.get_json()

    if not new_product or 'name' not in new_product:
        return jsonify({"error": "Invalid data. 'name' is required."}), 400
    max_current_id = max((item['id'] for item in data), default=0)
    new_product['id'] = max_current_id + 1
    data.append(new_product)
    return jsonify({"message": "Item added successfully", "item": new_product}), 201

@app.route('/delete_product/<int:product_id>', methods=["DELETE"])
def delete_product(product_id):
    """
    Delete a specific product.
    """
    product = next((product for product in data if product['id'] == product_id), None)
    if product:
        data.remove(product)
        return jsonify({"message":"Product successfully deleted."})
    return jsonify({"message":"Item Not Found"}), 404

if __name__ == '__main__':
    app.run(debug=True)