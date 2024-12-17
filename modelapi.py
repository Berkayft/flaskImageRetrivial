import tensorflow as tf
import numpy as np
from pymongo import MongoClient
from sklearn.metrics.pairwise import cosine_similarity
from tensorflow.keras.applications import MobileNet
from tensorflow.keras.applications.mobilenet import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from io import BytesIO
from PIL import Image
import requests

# MongoDB bağlantısını kur
client = MongoClient("mongodb://localhost:27017/")
db = client["models"]
collection = db["models"]

# MobileNet modelini yükle (son katman çıkarıldı)
model = MobileNet(weights="imagenet", include_top=False, pooling="avg")

def extract_features(image):
    """
    Bir görüntüden özellikleri çıkarmak için MobileNet kullanır.
    """
    try:
        image = image.resize((224, 224))  # MobileNet için uygun boyut
        image_array = img_to_array(image)
        image_array = np.expand_dims(image_array, axis=0)
        image_array = preprocess_input(image_array)

        # Özellik vektörünü çıkar
        features = model.predict(image_array)
        return features[0]
    except Exception as e:
        print(f"Error extracting features: {e}")
        return None

def trainModel(image_urls, catalog_id):
    """
    A function to extract features from a list of image URLs and save them in MongoDB with catalogId.
    """
    collection.delete_many({"catalogId": catalog_id})
    for idx, url_dict in enumerate(image_urls):  # Assuming image_urls is a list of dictionaries
        try:
            # Extract the URL from the dictionary (assuming the key is 'url')
            url = url_dict.get('url')
            if url is None:
                print(f"Invalid URL for image {idx}.")
                continue

            # Download the image
            response = requests.get(url)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))

            # Extract features
            features = extract_features(image)
            
            # Save to MongoDB with catalogId
            if features is not None:
                collection.insert_one({
                    "catalogId": catalog_id,
                    "index": idx,
                    "features": features.tolist()
                })
                print(f"Image {idx} from catalog {catalog_id} processed and saved.")
        except Exception as e:
            print(f"Error processing image {idx}: {e}")



def matchImage(aws_url, catalog_id):
    """
    Matches a new image with stored images, considering the catalogId.
    """
    try:
        # Download the image from AWS URL
        response = requests.get(aws_url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))

        # Extract features
        query_features = extract_features(image)
        if query_features is None:
            print("Failed to extract features from the input image.")
            return None

        # Retrieve all features for the specific catalogId
        all_features = list(collection.find({"catalogId": catalog_id}))
        feature_vectors = np.array([item["features"] for item in all_features])
        indices = [item["index"] for item in all_features]

        # Calculate cosine similarity
        similarities = cosine_similarity([query_features], feature_vectors)[0]
        best_match_idx = np.argmax(similarities)

        return indices[best_match_idx], similarities[best_match_idx]
    except Exception as e:
        print(f"Error matching image: {e}")
        return None


# Örnek kullanım
