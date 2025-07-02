from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError
import json

app = Flask(__name__)

@app.route('/')
def index():
    """Return a simple welcome message."""
    return jsonify({'message': 'Welcome to the MongoDB API. Use /mongodb endpoint for operations.'})

@app.route('/mongodb', methods=['POST'])
def mongodb_create_insert_find():
    """Handle MongoDB create, insert, and find operations via HTTP POST requests."""
    try:
        # Extract URI and query from JSON body
        data = request.get_json()
        if not data or 'uri' not in data or 'query' not in data:
            return jsonify({'error': 'Missing uri or query in JSON body'}), 400

        uri = data['uri']
        query = data['query']

        # Validate query structure
        required_keys = ['db', 'collection', 'operation']
        if not all(key in query for key in required_keys):
            return jsonify({'error': 'Query must include db, collection, and operation'}), 400

        # Connect to MongoDB
        try:
            client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            client.admin.command('ping')  # Test connection
        except (ConnectionFailure, ConfigurationError) as e:
            return jsonify({'error': f'Failed to connect to MongoDB: {str(e)}'}), 500

        # Access database
        db_name = query['db']
        collection_name = query['collection']
        operation = query['operation']
        db = client[db_name]
        
        # For create operation, collection is created below if needed
        if operation != 'create':
            collection = db[collection_name]

        # Execute the requested operation
        try:
            if operation == 'create':
                # Check if collection exists; create if it doesn't
                if collection_name not in db.list_collection_names():
                    db.create_collection(collection_name)
                    return jsonify({'message': f'Collection {collection_name} created in database {db_name}'}), 200
                else:
                    return jsonify({'message': f'Collection {collection_name} already exists in database {db_name}'}), 200

            elif operation == 'insert':
                if 'data' not in query:
                    return jsonify({'error': 'Insert operation requires data'}), 400
                data = query['data']
                # Handle single document or list of documents
                if isinstance(data, list):
                    result = collection.insert_many(data)
                    return jsonify({'inserted_ids': [str(id) for id in result.inserted_ids]}), 200
                else:
                    result = collection.insert_one(data)
                    return jsonify({'inserted_id': str(result.inserted_id)}), 200

            elif operation == 'find':
                if 'filter' not in query:
                    return jsonify({'error': 'Find operation requires a filter'}), 400
                results = list(collection.find(query['filter']))
                # Convert ObjectId to string for JSON serialization
                for result in results:
                    if '_id' in result:
                        result['_id'] = str(result['_id'])
                return jsonify({'results': results}), 200

            else:
                return jsonify({'error': f'Unsupported operation: {operation}'}), 400

        except Exception as e:
            return jsonify({'error': f'Query execution failed: {str(e)}'}), 500

    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

    finally:
        # Ensure MongoDB client is closed
        if 'client' in locals():
            client.close()

@app.route('/mongodb', methods=['PUT'])
def mongodb_update():
    """Handle MongoDB update operation via HTTP PUT requests."""
    try:
        # Extract URI and query from JSON body
        data = request.get_json()
        if not data or 'uri' not in data or 'query' not in data:
            return jsonify({'error': 'Missing uri or query in JSON body'}), 400

        uri = data['uri']
        query = data['query']

        # Validate query structure
        required_keys = ['db', 'collection', 'operation', 'filter', 'update']
        if not all(key in query for key in required_keys):
            return jsonify({'error': 'Query must include db, collection, operation, filter, and update'}), 400

        if query['operation'] != 'update':
            return jsonify({'error': 'PUT method only supports update operation'}), 400

        # Connect to MongoDB
        try:
            client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            client.admin.command('ping')  # Test connection
        except (ConnectionFailure, ConfigurationError) as e:
            return jsonify({'error': f'Failed to connect to MongoDB: {str(e)}'}), 500

        # Access database and collection
        db_name = query['db']
        collection_name = query['collection']
        db = client[db_name]
        collection = db[collection_name]

        # Execute update operation
        try:
            result = collection.update_many(query['filter'], query['update'])
            return jsonify({
                'matched_count': result.matched_count,
                'modified_count': result.modified_count
            }), 200

        except Exception as e:
            return jsonify({'error': f'Query execution failed: {str(e)}'}), 500

    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

    finally:
        # Ensure MongoDB client is closed
        if 'client' in locals():
            client.close()

@app.route('/mongodb', methods=['DELETE'])
def mongodb_delete():
    """Handle MongoDB delete operation via HTTP DELETE requests."""
    try:
        # Extract URI and query from JSON body
        data = request.get_json()
        if not data or 'uri' not in data or 'query' not in data:
            return jsonify({'error': 'Missing uri or query in JSON body'}), 400

        uri = data['uri']
        query = data['query']

        # Validate query structure
        required_keys = ['db', 'collection', 'operation', 'filter']
        if not all(key in query for key in required_keys):
            return jsonify({'error': 'Query must include db, collection, operation, and filter'}), 400

        if query['operation'] != 'delete':
            return jsonify({'error': 'DELETE method only supports delete operation'}), 400

        # Connect to MongoDB
        try:
            client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            client.admin.command('ping')  # Test connection
        except (ConnectionFailure, ConfigurationError) as e:
            return jsonify({'error': f'Failed to connect to MongoDB: {str(e)}'}), 500

        # Access database and collection
        db_name = query['db']
        collection_name = query['collection']
        db = client[db_name]
        collection = db[collection_name]

        # Execute delete operation
        try:
            result = collection.delete_many(query['filter'])
            return jsonify({'deleted_count': result.deleted_count}), 200

        except Exception as e:
            return jsonify({'error': f'Query execution failed: {str(e)}'}), 500

    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

    finally:
        # Ensure MongoDB client is closed
        if 'client' in locals():
            client.close()

if __name__ == '__main__':
    app.run()