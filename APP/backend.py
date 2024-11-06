from flask import Flask, request , render_template , jsonify
from time import sleep

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('GreenTech.html')


if __name__ == '__main__':
    app.run(host='10.1.24.200', port=8080)
