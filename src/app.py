from datetime import datetime, timedelta
from flask import Flask, request
import pymongo
import random
import math
from bson.objectid import ObjectId
import os

# from pipeline import Predictor

app = Flask(__name__)

# predictor = Predictor()

print(os.environ["MONGO_URL"])

client = pymongo.MongoClient(os.environ["MONGO_URL"])

if "gpmt" in client.list_database_names():
    gpmt_db = client["gpmt"]

    micturition = gpmt_db["Micturition"]
    stress = gpmt_db["Stress"]
    hydration = gpmt_db["Hydration"]
    users = gpmt_db["Users"]
else:
    print("No GPMT Database found")

@app.route("/")
def index():
    user_id = request.args.get("user_id")

    user = users.find_one({"_id": ObjectId(user_id)})

    return {
        "user_id": user_id,
        "firstname": user["firstname"],
        "surname": user["surname"]
    }

@app.route("/photo/classification", methods=["POST"])
def photo_classification():
    user_id = request.args.get("user_id")
    return {
        "user_id": user_id,
        "classification": "testClassification"
    }

@app.route("/forecast/micturition", methods=["POST"])
def micturition_forecast():
    user_id = request.args.get("user_id")

    user = users.find_one({
        "_id": ObjectId(user_id)
    })

    end = datetime.now()
    start = end - timedelta(7)

    micturitionEntries = micturition.find({
        "user": ObjectId(user_id),
        "date": {
            "$gte": start,
            "$lte": end
        }
    })

    hydrationEntries = hydration.find({
        "user": ObjectId(user_id),
        "date": {
            "$gte": start,
            "$lte": end
        }
    })

    stressEntries = stress.find({
        "user": ObjectId(user_id),
        "date": {
            "$gte": start,
            "$lte": end
        }
    })

    # forecast = predictor.forecast_micturition(
    #     micturition=micturitionEntries,
    #     hydration=hydrationEntries,
    #     stress=stressEntries,
    #     user=user,
    # )

    def floor_dt(dt, delta):
        seconds = math.floor(dt.timestamp())
        seconds = seconds - seconds % delta.seconds
        return datetime.fromtimestamp(seconds)

    now = floor_dt(datetime.now(), timedelta(hours=1))

    return {
        "user_id": user_id,
        "timestamp": datetime.now().isoformat(),
        "start": start.isoformat(),
        "end": end.isoformat(),
        "forecast": [
            { "prediction": random.random(), "date": now + timedelta(hours=i), "user": user_id }
            for i in range(25)
        ],
        "micturitionFrequency": random.random() * 3
    }


@app.route("/hydration")
def hydration_stats():
    user_id = request.args.get("user_id")

    end = datetime.now()
    start = end - timedelta(7)

    hydrationEntries = hydration.find({
        "user": ObjectId(user_id),
        "date": {
            "$gte": start,
            "$lte": end
        }
    })

    print(hydrationEntries)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=os.environ["PORT"])