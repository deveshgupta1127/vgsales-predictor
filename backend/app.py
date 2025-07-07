from flask import Flask, request, jsonify
import pickle
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load model and preprocessing files
with open("model.pkl", "rb") as f:
    model = pickle.load(f)
with open("label_encoders.pkl", "rb") as f:
    label_encoders = pickle.load(f)
with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    try:
        df = pd.DataFrame([data])

        for col in ['Platform', 'Genre', 'Publisher']:
            df[col] = label_encoders[col].transform(df[col])

        df[['Critic_Score', 'User_Score']] = scaler.transform(df[['Critic_Score', 'User_Score']])

        prediction = model.predict(df)[0]
        return jsonify({"prediction": round(float(prediction), 2)})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)