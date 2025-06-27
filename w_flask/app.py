import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import tensorflow as tf
# Corrected Code
from tensorflow.keras.utils import load_img, img_to_array
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions

import numpy as np

# --- Configuration ---
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
SECRET_KEY = 'your-super-secret-key' # Change this!

# --- Flask App Initialization ---
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = SECRET_KEY
# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# --- Load the pre-trained model ---
try:
    # Ensure the model file 'vgg16.h5' is in the root 'w_flask' directory
    model = tf.keras.models.load_model('vgg16.h5')
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# --- Helper Functions ---
def allowed_file(filename):
    """Checks if the file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Flask Routes ---

@app.route('/', methods=['GET'])
def home():
    """Renders the main page with the upload form."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handles image upload and prediction."""
    if model is None:
        flash("Model is not loaded. Please check the server logs.", "error")
        return redirect(url_for('home'))

    if 'file' not in request.files:
        flash('No file part in the request.', 'error')
        return redirect(url_for('home'))

    file = request.files['file']

    if file.filename == '':
        flash('No image selected for uploading.', 'error')
        return redirect(url_for('home'))

    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(img_path)

            # Preprocess the image for the model
            img = load_img(img_path, target_size=(224, 224))
            img_array = img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            
            # Use the preprocess_input function specific to VGG16
            processed_img = preprocess_input(img_array)

            # Make a prediction
            prediction_array = model.predict(processed_img)
            predicted_index = np.argmax(prediction_array, axis=1)[0]

            # Define your class labels
            class_labels = ['Biodegradable', 'Recyclable', 'Trash']
            prediction_label = class_labels[predicted_index]

            # Pass the result to the portfolio-details page
            return render_template('portfolio-details.html', 
                                   prediction=prediction_label, 
                                   image_file=filename)
        except Exception as e:
            flash(f"An error occurred during prediction: {e}", "error")
            return redirect(url_for('home'))
    else:
        flash('Invalid file type. Allowed types are: png, jpg, jpeg', 'error')
        return redirect(url_for('home'))


# --- Other pages from your structure (with added ipython route) ---
@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/blog-single')
def blog_single():
    return render_template('blog-single.html')

@app.route('/ipython-details')
def ipython_details():
    return render_template('ipython.html')

# --- Main Execution ---
if __name__ == '__main__':
    # Running on port 2222 as per your screenshot
    app.run(debug=True, port=2222)