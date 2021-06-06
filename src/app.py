from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/")
def index():
    user_id = request.args.get("user_id")
    return {
        "user_id": user_id
    }

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=os.environ["PORT"])