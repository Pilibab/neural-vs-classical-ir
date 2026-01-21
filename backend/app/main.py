from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    # Set host='0.0.0.0' to make the server externally available (useful for testing across networks)
    # The default port is 5000
    app.run(debug=True)