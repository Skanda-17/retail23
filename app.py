from flask import Flask, request, jsonify
from flask_cors import CORS
from retail_sales_kaggle import forecast_sales

app = Flask(__name__)
CORS(app)  # Allow React frontend to talk to Flask backend

@app.route('/forecast', methods=['POST'])
def forecast():
    data = request.get_json()
    store_nbr = data.get('store_nbr')
    family = data.get('family')

    if not store_nbr or not family:
        return jsonify({"error": "Missing store_nbr or family in request."}), 400

    try:
        forecast_df = forecast_sales(store_nbr, family)
        forecast_list = forecast_df.to_dict(orient='records')
        return jsonify(forecast_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "Retail Sales Forecasting API running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
