from flask import Flask, make_response, request,render_template
import pandas as pd
app = Flask(__name__)

@app.route('/')
def form():
    return render_template('index.html')

@app.route('/process', methods = ['POST'])
def process_view():
    if not request.files:
        return "No file"
    files = request.files.getlist("data_files")
    data_xls = pd.read_csv(files[0])

    return data_xls.to_html()


if __name__ == '__main__':
    app.run(debug=True)
