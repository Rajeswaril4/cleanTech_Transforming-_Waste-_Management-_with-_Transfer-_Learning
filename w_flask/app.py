import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import tensorflow as tf
from tensorflow.keras.utils import load_img, img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input
import numpy as np

# --- Configuration ---
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
SECRET_KEY = 'a-very-strong-secret-key-for-your-app'

# --- Flask App Initialization ---
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = SECRET_KEY

# Ensure the upload folder exists; create it if it doesn't.
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# --- Load The Pre-Trained Model ---
# This block attempts to load the model. If it fails, the app will still run,
# but the 'model' variable will be None, and predictions will be disabled.
try:
    print("--- Loading the Keras model... ---")
    model = tf.keras.models.load_model('vgg16.h5')
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    print("--- Model could not be loaded. Please check the file path and integrity. ---")
    model = None


# --- Helper Function ---
def is_allowed_file(filename):
    """Checks if the file has a valid extension (png, jpg, jpeg)."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# --- Routes ---
@app.route('/')
def home():
    """Renders the main page (index.html)."""
    return render_template('index.html')

@app.route('/blog')
def blog():
    """Renders the blog listing page (blog.html)."""
    return render_template('blog.html')

@app.route('/blog-single')
def blog_single():
    """Renders the blog single page (blog-single.html)."""
    return render_template('blog-single.html')

@app.route('/portfolio-details')
def portfolio_details():
    """Renders the portfolio details page (portfolio-details.html)."""
    # portfolio-details expects `prediction`, `image_file`, `confidence` when rendered after prediction.
    # If accessed directly, render a simple version without those variables.
    return render_template('portfolio-details.html', prediction=None, image_file=None, confidence=None)

@app.route('/predict', methods=['POST'])
def predict():
    """Handles the file upload and prediction process."""

    # 1. Check if the model loaded correctly
    if model is None:
        flash("Model is not available. Please check server logs for the error.", "error")
        return redirect(url_for('home'))

    # 2. Check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part in the request. The form might be misconfigured.', 'error')
        return redirect(url_for('home'))

    file = request.files['file']

    # 3. Check if the user selected a file
    if file.filename == '':
        flash('No image selected for uploading.', 'error')
        return redirect(url_for('home'))

    # 4. Check if the file is valid and has an allowed extension
    if file and is_allowed_file(file.filename):
        try:
            # Sanitize the filename to prevent security issues
            filename = secure_filename(file.filename)
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(img_path)
            print(f"--- Image saved to: {img_path} ---")

            # --- Image Preprocessing ---
            img = load_img(img_path, target_size=(224, 224))
            img_array = img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            processed_img = preprocess_input(img_array)

            # --- Prediction ---
            prediction_array = model.predict(processed_img)
            predicted_index = np.argmax(prediction_array, axis=1)[0]
            confidence_score = float(np.max(prediction_array)) * 100
            
            # IMPORTANT: This order must match the order used during model training!
            class_labels = ['Biodegradable', 'Recyclable', 'Trash']
            prediction_label = class_labels[predicted_index]

            print(f"🧠 Prediction: {prediction_label} with {confidence_score:.2f}% confidence.")

            # Render the results page
            return render_template('portfolio-details.html',
                                   prediction=prediction_label,
                                   image_file=filename,
                                   confidence=f"{confidence_score:.2f}")

        except Exception as e:

            print(f"❌ CAUGHT AN EXCEPTION DURING PREDICTION: {e}")
            # ==================================================================
            flash(f"An error occurred during prediction. Please check the server logs.", "error")
            return redirect(url_for('home'))
    else:
        flash('Invalid file type. Please upload a PNG, JPG, or JPEG file.', 'error')
        return redirect(url_for('home'))


# --- Run the App ---
if __name__ == '__main__':
    app.run(debug=True, port=2222)
