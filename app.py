from flask import Flask, render_template
from flask_wtf.file import FileField
import pandas as pd
app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html')
	# df = pd.read_excel()

if __name__ == '__main__':
	app.run(debug=False)


