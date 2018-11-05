from flask import Flask, render_template, request, send_file
from flask_wtf.file import FileField
import pandas as pd
app = Flask(__name__)
# app.config[‘UPLOAD_FOLDER’]
import UploadForm


@app.route('/', methods=['GET', 'POST'])
def index():
	# if request.method == 'GET':
	# 	if request.form['download_button'] == 'Download Template':
	# 		pass
	# 	else:
	# 		pass
	# 	elif request.method == 'GET':
	return render_template('index.html')
	if request.method == 'GET':
		render_template('index.html')
		return send_file('ClasslistGeneratorTemplate.xltx', mimetype='text/csv', attachment_filename='ClasslistGeneratorTemplate.xltx', as_attachment=True)
	return render_template('index.html')
# def download_csv():
# 	return send_file('../ClasslistGeneratorTemplate.csv', mimetype='text/csv', attachment_filename='ClasslistGeneratorTemplate.csv', as_attachment=True)

#
# @app.route('/', methods = ['GET', 'POST'])
# def index():
# 	if request.method == 'POST':
# 		f = request.files['file']
# 		f.save(secure_filename(f.filename))
# 		return 'file uploaded successfully'
#
#














if __name__ == '__main__':
	app.run(debug=False)


