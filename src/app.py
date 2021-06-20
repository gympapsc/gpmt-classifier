from flask import Flask, request
import pymongo
import os

app = Flask(__name__)

client = pymongo.MongoClient(os.environ["MONGO_URL"])
if "gpmt" in client.list_database_names():
    gpmt_db = client["gpmt"]
else:
    print("No GPMT Database found")

@app.route("/")
def index():
    user_id = request.args.get("user_id")
    return {
        "user_id": user_id
    }

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=os.environ["PORT"])