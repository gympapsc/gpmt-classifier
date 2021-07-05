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

client = pymongo.MongoClient(os.environ["MONGO_URL"])
if "gpmt" in client.list_database_names():
    gpmt_db = client["gpmt"]

    micturition = gpmt_db["micturition"]
    stress = gpmt_db["stress"]
    drinking = gpmt_db["drinking"]
    users = gpmt_db["users"]
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

@app.route("/micturition")
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

    drinkingEntries = drinking.find({
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
    #     drinking=drinkingEntries,
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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=os.environ["PORT"])