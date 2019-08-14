from flask import Flask, make_response, request,render_template

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('index.html')

@app.route('/process', methods = ['POST'])
def process_view():
    if not request.files:
        return "No file"
    request_file = request.files['data_file']

    return "processed!"


if __name__ == '__main__':
    app.run(debug=True)
