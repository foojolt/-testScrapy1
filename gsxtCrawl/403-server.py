

from flask import Flask, request, url_for, send_from_directory, Response
import json
import urllib2,urllib
import re

PORT = 5000
app = Flask(__name__)

@app.route('/cgi/error', methods=['GET', "POST"])
def error():
    resp = Response(response="<html>403 forbidden</html>", status=403, mimetype="text/html")
    return resp

app.run( port = PORT )