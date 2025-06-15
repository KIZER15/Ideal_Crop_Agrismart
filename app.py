from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the fertilizer data
data = pd.read_csv("fertilizer.csv")

@app.route('/get_details', methods=['POST'])
def get_crop_details():
    content = request.get_json()

    if not content or 'crop' not in content:
        return jsonify({'error': 'Please provide a JSON body with a "crop" field.'}), 400

    crop = content['crop'].strip().lower()
    matched = data[data['Crop'].str.lower() == crop]

    if matched.empty:
        return jsonify({'error': f"No data found for crop '{crop}'"}), 404

    # Extract required columns
    result = matched.iloc[0][['N', 'P', 'K', 'pH', 'soil_moisture']].to_dict()

    return jsonify({
        'crop': crop,
        'details': result
    })

if __name__ == '__main__':
    app.run(debug=True)
