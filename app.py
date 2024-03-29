import pytesseract as pt
from PIL import Image
import os
import urllib.request
from flask import Flask, request, redirect, jsonify, render_template
from werkzeug.utils import secure_filename
# pt.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'

# OCR function
def ocr_core(filename):
    """
    This function will handle the core OCR processing of images.
    """
    img = Image.open(filename)
    text = pt.image_to_string(img)  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text
 


# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
# UPLOAD_FOLDER = 'C:/uploads'
# UPLOAD_FOLDER = 'C:\Users\BUCHI\Documents\HNGIntership\HNG6\Task 8 scrape\gabby\OCRi\uplo'
app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


# route and function to handle the upload page
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def home():
    return redirect("https://documenter.getpostman.com/view/9310664/SW18vENi?version=latest")


@app.route('/', methods=['POST'])
def analyze_file():
	# check if the post request has the file part
	if 'file' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	file = request.files['file']
	if file.filename == '':
		resp = jsonify({'message' : 'No file selected for OCR'})
		resp.status_code = 400
		return resp
	if file and allowed_file(file.filename):
		# filename = secure_filename(file.filename)
		# file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		extracted_text = ocr_core(file)
		if extracted_text == '':
			extracted_text = "Sorry characters could not be clearly recognized"
			resp = jsonify({'message' : extracted_text})
			resp.status_code = 400
			return resp
		# resp = jsonify({'message' : 'File successfully uploaded'})
		resp = jsonify({'extracted_text' : extracted_text})
		resp.status_code = 200
		return resp
	else:
		resp = jsonify({'message' : 'Allowed file types are png, jpg, jpeg'})
		resp.status_code = 400
		return resp


if __name__ == '__main__':
	app.run()
