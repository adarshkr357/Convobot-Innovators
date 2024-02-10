import os
from functions import *
from datetime import datetime

from flask import Flask, render_template, request, jsonify


app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    icon_time_datetime = datetime.fromtimestamp(os.path.getmtime('static/images/favicon.png'))
    icon_time_timestamp = int(icon_time_datetime.timestamp())
    style_time_datetime = datetime.fromtimestamp(os.path.getmtime('static/css/style.css'))
    style_time_timestamp = int(style_time_datetime.timestamp())
    js_time_datetime = datetime.fromtimestamp(os.path.getmtime('static/js/script.js'))
    js_time_timestamp = int(js_time_datetime.timestamp())
    robot_time_datetime = datetime.fromtimestamp(os.path.getmtime('static/images/robot.png'))
    robot_time_timestamp = int(robot_time_datetime.timestamp())
    cloud_time_datetime = datetime.fromtimestamp(os.path.getmtime('static/images/cloud.png'))
    cloud_time_timestamp = int(cloud_time_datetime.timestamp())
    return render_template('index.html', icon_time=icon_time_timestamp, style_time=style_time_timestamp, robot_time=robot_time_timestamp, cloud_time=cloud_time_timestamp, js_time=js_time_timestamp)


@app.route('/process-data', methods=['POST'])
def process_data():
    data = request.get_json()
    query = data.get('query')
    keyword = get_keyword(query)
    if not keyword:
        return jsonify({ 'success': False, 'error': 'Wrong input. Please try again !!' }), 400

    keyword = keyword.replace(' ', '+')
    response = []

    # amazon = get_amazon(keyword)
    snapdeal = get_snapdeal(keyword)

    # response.append(amazon)
    response.append(snapdeal)

    return jsonify({ 'success': True, 'data': response }), 200


if __name__ == '__main__':
    app.run(debug=True)
