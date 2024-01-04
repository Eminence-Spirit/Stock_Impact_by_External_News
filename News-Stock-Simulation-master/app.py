
from flask import Flask, render_template, jsonify
from classes.trader import *  # Assuming this is your module name
from classes.market import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # HTML file to be created


@app.route('/simulate')
def simulate():
    market = MarketModel()
    market.simulate_market()
    data = market.get_time_series()  # This should return the time series data
    
    # Adjust this line to correctly format data

    formatted_data = [{"x": point['x'], "y": point['y']} for point in data]
    return jsonify({"stockPrices": formatted_data})
if __name__ == '__main__':
    app.run(debug=True)
