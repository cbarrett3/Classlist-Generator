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

# uploads settings
UPLOAD_FOLDER = os.getcwd() + '/uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' }

# Create Flask App
app = Flask(__name__, static_folder='static')
#app.config.from_object('config.Config')
dropzone = Dropzone(app)
app.secret_key = 'listenmoreoften'
# Use hardcoded string as environment variable for now
app.config['SECRET_KEY'] = 'listenmoreoften'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Home Page (No Request)
@app.route('/')
def index():
	return render_template('index.html')

# Home Page (GET or POST HTTP Request)
@app.route('/', methods=['POST'])
def my_index_post():

    if request.method == "POST":
        print(request.form)
        print(request.files)
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
            # if the submit button was clicked, render template at that same spot
            return render_template('index.html', scroll='form')
    else:
        return render_template("index.html", scroll='form')
    
    # Check for Email Address
    if "email" in request.form:
        address = request.form['email']
        print(address)
        flash("WE got your email, thanks!")
        return render_template('/')
		# if form.validate():
			# Save the comment here.
			# flash("Awesome! Thanks for your patience. Enjoy your classlists, and we'll see you next year!")
		# else:
		# 	flash('Please enter a valid email address.')
	# Check for Uploaded File
    if 'file' not in request.files:
        flash('No file part')
        return redirect('index.html')
    # Grab the uploaded file
    else:
        file = request.files.get('file')
		# Check for empty file submission
        if file.filename == '':
            flash('No selected file')
            return redirect('index.html')
		# Save file to upload folder
        else:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                flash("Awesome! Thanks for your patience. Enjoy your classlists, and we'll see you next year!")
				# TEMP -- we'll add logic here
                return render_template('index.html', scroll='submitted')
            else:
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


# download template
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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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

