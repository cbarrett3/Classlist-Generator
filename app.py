from ClasslistCreation import ClasslistCreation
from Generator import Generator
from forms import ContactForm
from flask import Flask, render_template, request, send_from_directory, send_file, flash, send_file, make_response, redirect, url_for, session
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_wtf import FlaskForm
from flask_dropzone import Dropzone
from flask_mail import Message, Mail
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from werkzeug.utils import secure_filename
from pandas import ExcelWriter
import pandas as pd
import xlsxwriter
import os

# create flask app
app = Flask(__name__, static_folder='static', instance_relative_config=True)
# now we can access config variables via app.config['var_name']
app.config.from_object('config')
# now we can use secret variables from instance folders config.py
app.config.from_pyfile('config.py')
# get secret key from environment variable
app.secret_key = app.config['SECRET_KEY']
# upload folder location
UPLOAD_FOLDER = os.getcwd() + '/uploads'
# allowed extensions for uploaded file
ALLOWED_EXTENSIONS = {'xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' }
# mail settings
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_DEFAULT_SENDER = 'connor.steven.barrett@gmail.com',
    MAIL_USERNAME = 'connor.steven.barrett@gmail.com',
    MAIL_PASSWORD = app.config['MAIL_PASSWORD']
)
# initialize mail instance
mail = Mail(app)

# Home PageS
@app.route('/')
def index():
	return render_template('index.html')

# Home Page (POST HTTP Request)
@app.route('/', methods=['POST'])
def my_index_post():
    if request.method == "POST":
        # get name
        Name = request.form["Name"]
        # get email
        Email = request.form["Email"]
        # get school
        School = request.form["School"]
        # array to hold the keys of missing input(s)
        missing = list()
        for key, value, in request.form.items():
            if value == "":
                missing.append(key)
        if missing:
            feedback = f"Missing fields for {', '.join(missing)}"
            return render_template("index.html", feedback=feedback, scroll='form')
        # get file
        file = request.files['file']
        # check file existence
        if file.filename == '':
            feedback = "No Selected File"
            return render_template("index.html", feedback=feedback, scroll='form')
        # check file type
        elif allowed_file(file.filename) == False:
            feedback = "File Type Not Supported"
            return render_template("index.html", feedback=feedback, scroll='form')
        # save file
        else:
            file.save('uploads/' + secure_filename(file.filename))
            # call classlists creation method with uploaded file
            classlists = ClasslistCreation(secure_filename(file.filename))
            # initiate early student placements
            early_classlists = classlists.early_placement()
            # initiate classlist generator
            generator = Generator(early_classlists, classlists.kids, classlists.num_students, classlists.num_teachers)
            # call the class generate method to generate classlists
            generated_classlists = generator.generate()
            # call method to get rid of columns we don't need
            generated_classlists = clean_up_dfs(generated_classlists)
            # create this as the file name
            filename = 'GeneratedClasslists.xlsx'
            # save cleaned df into an excel spreadsheet
            save_xls(generated_classlists, 'generated/' + filename)
            # send email
            email = Message(subject="Your Balanced Classlists are Attatched!", sender=app.config.get("MAIL_USERNAME"), recipients=[Email], body="Thank you for using ClasslistGener8r!")
            # with app.open_resource('generated/' + filename) as fp:
            # 	email.attach(filename, fp.read())
            with app.open_resource('generated/' + filename) as fp:
            	email.attach(filename, 'generated/' + filename, fp.read())
            mail.send(email)
            feedback = "Awesome! Thanks for your patience. Enjoy your classlists, and we'll see you next year!"
            return render_template("index.html", feedback=feedback, scroll='form')
    else:
        return render_template("index.html", scroll='form')

# download template
@app.route('/download-template/')
def return_file():
	# return send_from_directory(app.static_folder, 'static/ClasslistGeneratorTemplate.xlsx', as_attachment=True)
	return send_file('static/ClasslistGeneratorTemplate.xlsx', as_attachment=True)

# Save DF into Excel Spreadsheet
def save_xls(dict_df, path):
	writer = pd.ExcelWriter(path, engine='xlsxwriter')
    # loop through dictionary of df's
	for key, df in dict_df.items():
        # send df to writer
		df.to_excel(writer, sheet_name=key, index=False, index_label=False, header=True)
        # pull worksheet object
		worksheet = writer.sheets[key]
        # loop through all columns
		for idx, col in enumerate(df):
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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
	app.run()
