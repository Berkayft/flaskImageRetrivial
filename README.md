# Image Retrieval Submodule

This submodule is designed for image retrieval using Flask, TensorFlow, and a locally hosted MongoDB database. Below, you will find instructions for setting up the necessary dependencies and configuring the environment.

## Prerequisites

Ensure you have the following installed on your system:

1. **MongoDB**: A local MongoDB instance is required. You can download and install MongoDB from the official website: [MongoDB Download](https://www.mongodb.com/try/download/community).

2. **Python**: This project is compatible with Python 3.8 or later. Install Python from the official website: [Python Download](https://www.python.org/downloads/).

## Installation Steps

1. **Install MongoDB**
   - Follow the installation guide for your operating system from the MongoDB documentation: [MongoDB Installation Guide](https://docs.mongodb.com/manual/installation/).
   - Ensure the MongoDB service is running locally.

2. **Set up a Python Virtual Environment (Optional but Recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Required Python Libraries**
   Install the following dependencies using `pip`:
   ```bash
   pip install flask flask-cors tensorflow
   ```
   - **Flask**: A lightweight web framework for Python.
   - **Flask-CORS**: Enables Cross-Origin Resource Sharing (CORS) for Flask applications.
   - **TensorFlow**: A powerful library for machine learning and image processing.

   > **Note**: TensorFlow installation may vary based on your system configuration (e.g., CPU or GPU support). Refer to the official TensorFlow installation guide for detailed instructions: [TensorFlow Installation Guide](https://www.tensorflow.org/install).

## Usage

1. **Start the MongoDB Service**
   Ensure the local MongoDB instance is running before starting the application. You can verify this by connecting to the MongoDB shell:
   ```bash
   mongo
   ```

2. **Run the Flask Application**
   Execute the following command to start the Flask server:
   ```bash
   python api.py
   ```

3. **Test the Submodule**
   Once the server is running, use tools like `curl`, Postman, or a web browser to interact with the endpoints.

## Notes
- This submodule assumes that MongoDB is running with its default settings (port 27017).
- The TensorFlow library should be compatible with the Python version installed on your system.

For any issues or questions, please refer to the official documentation of the respective libraries or contact the development team.

---
