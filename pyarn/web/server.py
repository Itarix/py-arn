"""web module is used to provide ihm and web server"""
from distutils import util
import flask
import os
import sys

val = os.path.dirname(sys.path[0])
sys.path.append(str(val).split("pyarn")[0])

import pyarn.comparison.complementary_arn as complementary
import pyarn.comparison.loop_arn as loop
import pyarn.comparison.position_arn as position
from pyarn.models import arn


app = flask.Flask(__name__, static_folder="./static", template_folder="templates")


@app.route('/')
def index():
    """
    Endpoint to return index.html page
    :return:
    """
    return send_html("index.html")


@app.route('/html/page/<path:path>')
def send_html(path):
    """
    Endpoint to return to specify page
    :param path:
    :return:
    """
    return flask.render_template("html/page/" + path, active_page=path)


@app.route('/js/<path:path>')
def send_js(path):
    """
    Endpoint to return js
    :param path:
    :return:
    """
    return flask.send_from_directory("static/js", path)


@app.route('/css/<path:path>')
def send_css(path):
    """
    Endpoint to return css
    :param path:
    :return:
    """
    return flask.send_from_directory("static/css", path)


@app.route('/compare/position', methods=['POST'])
def api_compare_position():
    """
    Endpoint used to compare position between 2 arns
    :return:
    """
    arn1 = arn.Arn(flask.request.form['arn1'])
    arn2 = arn.Arn(flask.request.form['arn2'])
    data = position.compare_position_arn(arn1, arn2, None)
    return flask.jsonify(data)


@app.route('/compare/complementary', methods=['POST'])
def api_compare_complementary():
    """
    Endpoint used to compare complementary between 2 arns
    :return:
    """
    arn1 = arn.Arn(flask.request.form['arn1'])
    arn2 = arn.Arn(flask.request.form['arn2'])
    percent_pairing = int(flask.request.form['percent_pairing'])
    val_space = util.strtobool(flask.request.form['add_space_sequence_1'])
    data = complementary.compare_complementary_arn(
        arn1, arn2,
        None, bool(val_space), percent_pairing
    )
    return flask.jsonify(data)


@app.route('/compare/loop', methods=['POST'])
def api_compare_loop():
    """
    Endpoint used to compare loop between 2 arns
    :return:
    """
    arn1 = arn.Arn(flask.request.form['arn1'])
    arn2 = arn.Arn(flask.request.form['arn2'])
    percent_pairing = int(flask.request.form['percent_pairing'])
    data = loop.compare_loop_one_arn(arn1, arn2, None, percent_pairing)
    return flask.jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)  # for test/dev
    # print("Available on : http://127.0.0.1:5000/")
    # waitress.serve(app, host="0.0.0.0", port=5000)
