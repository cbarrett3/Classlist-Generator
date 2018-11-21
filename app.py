from flask import Flask, render_template, request, send_file, make_response, send_from_directory
from flask_wtf.file import FileField
import pandas as pd
from werkzeug.utils import secure_filename
app = Flask(__name__, static_folder='static')
# app.config[‘UPLOAD_FOLDER’]
import UploadForm


@app.route('/', methods=['GET', 'POST'])  # the methods argument will allow us to execute GET and POST HTTP methods
def index():
	# render_template('index.html')

	# current issue is that initial refresh or initital visit is considered a GET

	# download = request.files['download']
	# if request.method == 'GET' and download:

	# this isnt workin
	if "down" in request.form:
		# send_file('static/ClasslistGeneratorTemplate.xlsx',
		# mimetype='text/csv',
		# attachment_filename='static/ClasslistGeneratorTemplate.xlsx',
		# as_attachment=True)
		# return request.form['spreadsheet']
		send_from_directory(app.static_folder, 'ClasslistGeneratorTemplate.xlsx', as_attachment=True)

	# this works (still jumps to the top & doesnt stay tho, but it saves the file
	if "up" in request.form:
		uploaded_file = request.files['upload']
		uploaded_file.save('uploads/' + secure_filename(uploaded_file.filename))
		# return render_template('index.html')
		# return render_template('index.html')

	# working upload code

	# if request.method == 'POST':
	# 	uploaded_file = request.files['upload']
	# 	uploaded_file.save('uploads/' + secure_filename(uploaded_file.filename))
	# 	# pop up here saying Thank You!
	# 	# currently file gets saved but refresh brings us to top of page
	# 	# need to make it so it does not scroll to top after submit is clicked
	#
	# 	# pottentially trigger email at this point to where the Classlists will be sent
	# 	return render_template('index.html')
	# #

	# end of working upload code
	return render_template('index.html')


@app.route('/return-file/')
def return_file():
	return send_from_directory(app.static_folder, 'ClasslistGeneratorTemplate.xlsx', as_attachment=True)

#
# @app.route('/upload', methods=['GET', 'POST'])
# def upload_file():
# 	if request.method == 'POST':
# 		f = request.files['complete_sheet']
# 		# save() method allows us to store the file on the filesystem of the server
# 		f.save('/uploads/complete_sheet.txt' + secure_filename(f.filename))
# 	return 'file uploaded successfully'

if __name__ == '__main__':
	app.run(debug=True)


