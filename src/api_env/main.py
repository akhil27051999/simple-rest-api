from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Create Routes

@app.route("/")
def home():
    return "Hello!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 5000, debug=True)
