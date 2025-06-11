from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

# Sample data store (in production, you'd use a database)
data_store = {
    "items": [
        {"id": 1, "name": "Sample Item 1", "description": "This is a sample item"},
        {"id": 2, "name": "Sample Item 2", "description": "Another sample item"}
    ]
}

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to your Python backend!",
        "status": "running",
        "endpoints": [
            "GET /api/items - Get all items",
            "POST /api/items - Create new item",
            "GET /api/items/<id> - Get specific item",
            "PUT /api/items/<id> - Update item",
            "DELETE /api/items/<id> - Delete item"
        ]
    })

@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify(data_store["items"])

@app.route('/api/items', methods=['POST'])
def create_item():
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({"error": "Name is required"}), 400
    
    new_item = {
        "id": len(data_store["items"]) + 1,
        "name": data["name"],
        "description": data.get("description", "")
    }
    
    data_store["items"].append(new_item)
    return jsonify(new_item), 201

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in data_store["items"] if item["id"] == item_id), None)
    
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    return jsonify(item)

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = next((item for item in data_store["items"] if item["id"] == item_id), None)
    
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    data = request.get_json()
    
    if data:
        item["name"] = data.get("name", item["name"])
        item["description"] = data.get("description", item["description"])
    
    return jsonify(item)

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item_index = next((i for i, item in enumerate(data_store["items"]) if item["id"] == item_id), None)
    
    if item_index is None:
        return jsonify({"error": "Item not found"}), 404
    
    deleted_item = data_store["items"].pop(item_index)
    return jsonify({"message": "Item deleted", "item": deleted_item})

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)