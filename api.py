from flask import Flask, request, jsonify
from flask_cors import CORS
import modelapi  # Assuming this is the module with your existing functions

app = Flask(__name__)
CORS(app)  # Apply CORS settings to the entire application

@app.route('/saveSignedUrls', methods=['POST'])
def save_signed_urls():
    try:
        data = request.get_json()

        if not data or not isinstance(data, dict) or 'urls' not in data or 'catalogId' not in data:
            return jsonify({"error": "Invalid data format. Expected 'urls' and 'catalogId'"}), 422

        urls = data['urls']
        catalog_id = data['catalogId']

        if not isinstance(urls, list):
            return jsonify({"error": "Invalid data format. Expected a list of objects with 'url'"}), 422

        print(f"Received catalogId: {catalog_id}")
        print("Received URLs:")

        for item in urls:
            if not isinstance(item, dict) or 'url' not in item:
                return jsonify({"error": f"Invalid item format: {item}"}), 422
            
            url = item.get('url')
            print(url)

        # Train the model with the received URLs and catalogId
        modelapi.trainModel(urls, catalog_id)

        return jsonify({
            "message": "URLs received and processed successfully",
            "count": len(urls)
        }), 200

    except Exception as e:
        print("Error processing request:", str(e))
        return jsonify({"error": "An error occurred", "details": str(e)}), 500


@app.route("/matchImage", methods=['POST'])
def matched_image():
    try:
        # Get the image URL from the request
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({"error": "No image URL provided"}), 422
        
        # Extract the URL
        image_url = data['url']
        catalog_id = data["catalogId"]
        
        # Perform image matching
        match_result = modelapi.matchImage(image_url, catalog_id)
        
        if match_result is None:
            return jsonify({
                "error": "Could not find a matching image",
                "status": "no_match"
            }), 404
        
        # Unpack the match result
        matched_index, similarity_score = match_result
        print(matched_index)
        return jsonify({
            "index":matched_index
        }), 200
    
    except Exception as e:
        print("Error matching image:", str(e))
        return jsonify({
            "error": "An error occurred during image matching", 
            "details": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=3500)