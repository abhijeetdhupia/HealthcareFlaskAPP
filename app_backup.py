import os
from flask import Flask, render_template, url_for, request, send_from_directory, redirect
from werkzeug.utils import secure_filename
from covid import get_mask_rcnn_model, inference

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        filename = secure_filename(file.filename)
        prepend = os.getcwd()
        image_path = prepend + "/static/uploads/covid/" + patient_id + filename 
        save_path = prepend + "/static/uploads/covid/" + patient_id + "test.png"
        # save_path = prepend + "/covid/" + filename.split('.')[0] + "_mask." + filename.split('.')[1]
        # return f"Image Path: {image_path}, Save Path: {save_path}"
        sample_img_path = "/data/healthcare/Banu/COVID-19/Radiopaedia-CoronacasesCT/5FoldCV/Fold_0/CT/coronacases_002_081.png"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'covid','input.png'))

        inference(sample_img_path, save_path)
        # send_from_directory(UPLOAD_FOLDER, save_path)

        return render_template('CovidPrediction.html', filename='test.png')
    return render_template("COVID19.html")

@app.route('/display/<filename>')
def display_image(filename):
	print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/covid/' + filename), code=301)

if __name__ == "__main__":
    app.run(debug=True)
