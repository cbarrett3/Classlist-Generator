from flask import Flask, render_template, request, send_from_directory, send_file, flash, send_file, make_response, redirect, url_for, session
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask_wtf.file import FileField
from flask_dropzone import Dropzone
import pandas as pd
from werkzeug.utils import secure_filename
from ClasslistCreation import ClasslistCreation
from Generator import Generator
from pandas import ExcelWriter
import xlsxwriter
from flask_mail import Message
from flask_mail import Mail, Message
import os

from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
# Create Flask App
app = Flask(__name__, static_folder='static')
dropzone = Dropzone(app)
app.secret_key = 'listenmoreoften'
app.config['SECRET_KEY'] = 'listenmoreoften'
address = ''
email = TextField('Email:', validators=[validators.required(), validators.Length(min=6, max=35)])


######### FLASK TESTING ##########
# Uploads settings
UPLOAD_FOLDER = os.getcwd() + '/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' }
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home Page (No Request)
@app.route('/')
def index():
	return render_template('index.html')

# Home Page (GET or POST HTTP Request)
@app.route('/', methods=['GET', 'POST'])
def my_index_post():
	flash("made it here")
	# Handle Uploaded Excel
	# if "up" in request.form:
	# 	flash("Awesome! Thanks for your patience. Enjoy your classlists, and we'll see you next year!")
	if request.method == 'POST':
		# Look for Email
		if "email" in request.form:
			address = request.form['email']
			print(address)
			flash("WE got your email, thanks!")
			# if form.validate():
				# Save the comment here.
				# flash("Awesome! Thanks for your patience. Enjoy your classlists, and we'll see you next year!")
			# else:
			# 	flash('Please enter a valid email address.')
		# Look for Uploaded File
		if 'file' not in request.files:
			flash('No file part')
			return redirect('index.html')
		# else, grab the uploaded file
		file = request.files.get('file')
        # check for empty submission
		if file.filename == '':
			flash('No selected file')
			return redirect('index.html')
		# check file format
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			flash("Awesome! Thanks for your patience. Enjoy your classlists, and we'll see you next year!")
			# TEMP
			return render_template('index.html', scroll='submitted')
		return render_template('index.html')
	
	return render_template('index.html')

		# uploaded_file = request.files['upload']
		# # save uploaded file into uploads folder
		# uploaded_file.save('uploads/' + secure_filename(uploaded_file.filename))
		# # call classlists creation method with uploaded file
		# classlists = ClasslistCreation(secure_filename(uploaded_file.filename))
		# # initiate early student placements
		# early_classlists = classlists.early_placement()
		# # initiate classlist generator
		# generator = Generator(early_classlists, classlists.kids, classlists.num_students, classlists.num_teachers)
		# # call the class generate method to generate classlists
		# generated_classlists = generator.generate()
		# # call method to get rid of columns we don't need
		# generated_classlists = clean_up_dfs(generated_classlists)
		# # create this as the file name
		# filename = 'GeneratedClasslists.xlsx'
		# # save cleaned df into an excel spreadsheet
		# save_xls(generated_classlists, 'generated/' + filename)
		# app.config.update(mail_settings)
		# mail = Mail(app)
		# global address
		# msg = Message(subject="Your Classlists are ready!", sender=app.config.get("MAIL_USERNAME"), recipients=[address], body="Attached are your classlists. Thanks again for using ClasslistGener8r!")
		# # with app.open_resource('generated/' + filename) as fp:
		# # 	msg.attach(filename, fp.read())
		# with app.open_resource('generated/' + filename) as fp:
		# 	msg.attach('generated/' + filename, 'generated/' + filename, fp.read())
		# mail.send(msg)
		# print('file sent successfully')
		# # if the submit button was clicked, render template at that same spot
		# return render_template('index.html', scroll='submitted')

	# save recipient email address to send email to
	# recipient_address = request.form.get('textbox')
	# # needed to modify global copy of address
	# address = recipient_address
	# flash("Got it! Check your inbox for the generated classlists within minutes after submitting the filled out template!")
	# return render_template('index.html', scroll='submitted')


# Download Template
@app.route('/download-template/')
def return_file():
	# return send_from_directory(app.static_folder, 'static/ClasslistGeneratorTemplate.xlsx', as_attachment=True)
	return send_file('static/ClasslistGeneratorTemplate.xlsx', as_attachment=True)

# Save DF into Excel Spreadsheet
def save_xls(dict_df, path):
	writer = pd.ExcelWriter(path, engine='xlsxwriter')
	for key, df in dict_df.items():  # loop through dictionary of df's
		df.to_excel(writer, sheet_name=key, index=False, index_label=False, header=True)  # send df to writer
		worksheet = writer.sheets[key]  # pull worksheet object
		for idx, col in enumerate(df):  # loop through all columns
			series = df[col]
			# adding a little more cushion space
			max_len = max((series.astype(str).map(len).max(), len(str(series.name)))) + 1
			# set column width
			worksheet.set_column(idx, idx, max_len)
	writer.save()


def clean_up_dfs(dict_df):
	# drops un-needed columns from kids
	for key in dict_df:
		dict_df[key] = dict_df[key].drop(['Future Teacher Last Name (N/A If Unknown)', 'Candidate Score'], axis=1)
		# dict_df[key] = dict_df[key].drop(dict_df[key].columns[0], axis=1)
	return dict_df

# Mail settings
mail_settings = {
	"MAIL_SERVER": 'smtp.gmail.com',
	"MAIL_PORT": 465,
	"MAIL_USE_TLS": False,
	"MAIL_USE_SSL": True,
	"MAIL_USERNAME": "connor.steven.barrett@gmail.com",
	"MAIL_PASSWORD": "Trained10!"
}

if __name__ == '__main__':
	app.run(debug=True)

