from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit, join_room
from pymongo import MongoClient
from urllib.parse import urlparse
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def get_mongo_client(uri):
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')  # Test connection
        return client
    except Exception as e:
        logging.error(f"MongoDB connection failed: {str(e)}")
        return None

@app.route('/mongodb', methods=['POST'])
def handle_mongodb_post():
    try:
        data = request.get_json()
        uri = data.get('uri')
        query = data.get('query')
        if not uri or not query:
            return jsonify({'status': 'error', 'error': 'Missing uri or query'}), 400
        
        client = get_mongo_client(uri)
        if not client:
            return jsonify({'status': 'error', 'error': 'Failed to connect to MongoDB'}), 500
        
        db_name = query.get('db')
        collection_name = query.get('collection')
        operation = query.get('operation')
        db = client[db_name]
        collection = db[collection_name]
        
        if operation == 'create':
            # Create collection if it doesn't exist
            if collection_name not in db.list_collection_names():
                db.create_collection(collection_name)
                result = {'status': 'success', 'message': f'Collection {collection_name} created'}
            else:
                result = {'status': 'success', 'message': f'Collection {collection_name} already exists'}
        
        elif operation == 'find':
            filter_query = query.get('filter', {})
            results = list(collection.find(filter_query))
            for doc in results:
                doc['_id'] = str(doc['_id'])
            result = {'status': 'success', 'results': results}
        
        elif operation == 'insert':
            data = query.get('data')
            inserted = collection.insert_one(data)
            result = {'status': 'success', 'inserted_id': str(inserted.inserted_id)}
        
        else:
            return jsonify({'status': 'error', 'error': 'Unsupported operation'}), 400
        
        client.close()
        return jsonify(result)
    except Exception as e:
        logging.error(f"Error in POST /mongodb: {str(e)}")
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/mongodb', methods=['PUT'])
def handle_mongodb_put():
    try:
        data = request.get_json()
        uri = data.get('uri')
        query = data.get('query')
        if not uri or not query:
            return jsonify({'status': 'error', 'error': 'Missing uri or query'}), 400
        
        client = get_mongo_client(uri)
        if not client:
            return jsonify({'status': 'error', 'error': 'Failed to connect to MongoDB'}), 500
        
        db_name = query.get('db')
        collection_name = query.get('collection')
        operation = query.get('operation')
        db = client[db_name]
        collection = db[collection_name]
        
        if operation == 'update':
            filter_query = query.get('filter', {})
            update_data = query.get('update', {})
            result = collection.update_one(filter_query, update_data)
            result = {'status': 'success', 'matched_count': result.matched_count, 'modified_count': result.modified_count}
        
        else:
            return jsonify({'status': 'error', 'error': 'Unsupported operation'}), 400
        
        client.close()
        return jsonify(result)
    except Exception as e:
        logging.error(f"Error in PUT /mongodb: {str(e)}")
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/mongodb', methods=['DELETE'])
def handle_mongodb_delete():
    try:
        data = request.get_json()
        uri = data.get('uri')
        query = data.get('query')
        if not uri or not query:
            return jsonify({'status': 'error', 'error': 'Missing uri or query'}), 400
        
        client = get_mongo_client(uri)
        if not client:
            return jsonify({'status': 'error', 'error': 'Failed to connect to MongoDB'}), 500
        
        db_name = query.get('db')
        collection_name = query.get('collection')
        operation = query.get('operation')
        db = client[db_name]
        collection = db[collection_name]
        
        if operation == 'delete':
            filter_query = query.get('filter', {})
            result = collection.delete_one(filter_query)
            result = {'status': 'success', 'deleted_count': result.deleted_count}
        
        else:
            return jsonify({'status': 'error', 'error': 'Unsupported operation'}), 400
        
        client.close()
        return jsonify(result)
    except Exception as e:
        logging.error(f"Error in DELETE /mongodb: {str(e)}")
        return jsonify({'status': 'error', 'error': str(e)}), 500

@socketio.on('connect', namespace='/mongodb')
def handle_connect(auth):
    join_room(request.sid)
    logging.debug(f"Client connected: {request.sid}")
    emit('connect_response', {'status': 'success', 'message': 'Connected to MongoDB namespace'}, room=request.sid)

@socketio.on('disconnect', namespace='/mongodb')
def handle_disconnect():
    logging.debug(f"Client disconnected: {request.sid}")

@socketio.on('mongodb', namespace='/mongodb')
def handle_mongodb_event(data):
    try:
        uri = data.get('uri')
        query = data.get('query')
        if not uri or not query:
            emit('response', {'status': 'error', 'error': 'Missing uri or query'}, room=request.sid)
            return
        
        client = get_mongo_client(uri)
        if not client:
            emit('response', {'status': 'error', 'error': 'Failed to connect to MongoDB'}, room=request.sid)
            return
        
        db_name = query.get('db')
        collection_name = query.get('collection')
        operation = query.get('operation')
        db = client[db_name]
        collection = db[collection_name]
        
        if operation == 'create':
            if collection_name not in db.list_collection_names():
                db.create_collection(collection_name)
                result = {'status': 'success', 'message': f'Collection {collection_name} created'}
            else:
                result = {'status': 'success', 'message': f'Collection {collection_name} already exists'}
        
        elif operation == 'find':
            filter_query = query.get('filter', {})
            results = list(collection.find(filter_query))
            for doc in results:
                doc['_id'] = str(doc['_id'])
            result = {'status': 'success', 'results': results}
        
        elif operation == 'insert':
            data = query.get('data')
            inserted = collection.insert_one(data)
            result = {'status': 'success', 'inserted_id': str(inserted.inserted_id)}
        
        elif operation == 'update':
            filter_query = query.get('filter', {})
            update_data = query.get('update', {})
            result = collection.update_one(filter_query, update_data)
            result = {'status': 'success', 'matched_count': result.matched_count, 'modified_count': result.modified_count}
        
        elif operation == 'delete':
            filter_query = query.get('filter', {})
            result = collection.delete_one(filter_query)
            result = {'status': 'success', 'deleted_count': result.deleted_count}
        
        else:
            emit('response', {'status': 'error', 'error': 'Unsupported operation'}, room=request.sid)
            return
        
        client.close()
        emit('response', result, room=request.sid)
    except Exception as e:
        logging.error(f"Error in WebSocket mongodb event: {str(e)}")
        emit('response', {'status': 'error', 'error': str(e)}, room=request.sid)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
