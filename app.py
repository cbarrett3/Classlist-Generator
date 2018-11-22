from flask import Flask, render_template, request, send_from_directory, flash, send_file, make_response, redirect, url_for
from flask_wtf.file import FileField
import pandas as pd
from werkzeug.utils import secure_filename
app = Flask(__name__, static_folder='static')
app.secret_key = 'be quiet'


@app.route('/', methods=['GET', 'POST'])  # the methods argument will allow us to execute GET and POST HTTP methods
def index():

	if "up" in request.form:
		uploaded_file = request.files['upload']
		uploaded_file.save('uploads/' + secure_filename(uploaded_file.filename))
		flash("Perfect! Your Classlists are being generated. Check your email in about five minutes!")
		# if the submit button was clicked, render template at that same spot
		return render_template('index.html', scroll='submitted')

	# TODO: trigger email at this point to where the Classlists will be sent
	# else render template to top of page (normal refresh)
	return render_template('index.html')


# this handles saving the file into our uploads folder
@app.route('/return-file/')
def return_file():
	return send_from_directory(app.static_folder, 'ClasslistGeneratorTemplate.xlsx', as_attachment=True)


if __name__ == '__main__':
	app.run(debug=True)


