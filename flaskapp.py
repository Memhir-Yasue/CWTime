from flask import Flask, make_response, request,render_template

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('index.html')

@app.route('/process_data', methods = ['POST'])
def process_data():
    return "processed!"


if __name__ == '__main__':
    app.run(debug=True)
