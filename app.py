import os
from flask import Flask, render_template, url_for, request, send_from_directory, redirect
from werkzeug.utils import secure_filename
from covid import get_mask_rcnn_model, inference

UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/iCare.html')
def iCare():
    return render_template("iCare.html")

@app.route('/WCE.html')
def WCE():
    return render_template("WCE.html")

@app.route('/COVID19.html', methods=['POST', 'GET'])
def COVID():
    if request.method == 'POST':
        patient_id = request.form["p_id"]
        file = request.files['file']
        
        # Input image name 
        filename = secure_filename(file.filename)
        # Predicted image name 
        predimage_name = filename.split('.')[0] + "_mask." + filename.split('.')[1]
        # Patient directory 
        path = os.path.join(app.config['UPLOAD_FOLDER'], 'covid', patient_id)
        # Input image path 
        inputimage = os.path.join(path, filename) 
        # Predicted image path 
        predimage = os.path.join(path, predimage_name)
        # Make the directories
        os.makedirs(f"{path}")
        # Save the uploaded input image 
        file.save(inputimage)
        # Predict the mask 
        inference(inputimage, predimage)
        # Return the template with the input image and predicted mask 
        return render_template('CovidPrediction.html', inputimg = inputimage, predimg =  predimage)
    return render_template("COVID19.html")

# @app.route('/display/<filename>')
# def display_image(filename):
# 	return redirect(url_for('static', filename = filename), code=301)

if __name__ == "__main__":
    app.run(debug=True)