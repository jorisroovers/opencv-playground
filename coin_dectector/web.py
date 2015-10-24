from coins import detector
from flask import Flask
from flask import request, jsonify, render_template, send_from_directory

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", name="joris")


@app.route('/assets/<path:path>')
def assets(path):
    return send_from_directory('assets', path)


@app.route('/generated/<path:path>')
def generated(path):
    return send_from_directory('generated', path)


@app.route("/detect", methods=['POST'])
def detect():
    data = request.json
    dst_path = detector.detect('assets/coins.png', float(data['param1']), float(data['param2']))
    return jsonify(**{"url": dst_path})


if __name__ == "__main__":
    app.run(debug=True)
