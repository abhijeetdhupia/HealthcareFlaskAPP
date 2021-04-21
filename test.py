import os 
parent_dir = 'static/uploads/covid/'
patientID = 'p_id'
try: 
    finalpath =os.path.join(parent_dir, patientID)
    os.rmdir(f"{finalpath}")
    print(os.curdir)
    os.makedirs(f"{finalpath}")
except OSError as error: 
    print(error)  

@app.route('/COVID19.html', methods=['POST', 'GET'])
def COVID():
    if request.method == 'POST':
        patient_id = request.form["p_id"]
        file = request.files['file']
        filename = secure_filename(file.filename)
        path = os.path.join(os.curdir, app.config['UPLOAD_FOLDER'], patient_id)
        file.save(path, filename)
        # sample_img_path = "/data/healthcare/Banu/COVID-19/Radiopaedia-CoronacasesCT/5FoldCV/Fold_0/CT/coronacases_002_081.png"
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'input.png'))

        inference(sample_img_path, save_path)
        # send_from_directory(UPLOAD_FOLDER, save_path)

        return render_template('CovidPrediction.html', filename='test.png')
    return render_template("COVID19.html")

        # save_path = prepend + "/covid/" + filename.split('.')[0] + "_mask." + filename.split('.')[1]
        # return f"Image Path: {image_path}, Save Path: {save_path}"