from flask import Flask, request
from r53 import Route53Connection
app = Flask(__name__)

@app.route('/')
def home():
    return """
    <html><body>
    Please make a POST request to POST with the parameters aws_access_id, aws_secret_access_key, aws_route53_zone, record_name, record_type and record_value.
    </body></html>
    """

@app.route('/change', methods=['POST'])
def change():
    print(request.form)
    c = Route53Connection(request.form['aws_access_key_id'], request.form['aws_secret_access_key'], request.form['aws_route53_zone'])
    c.change_record(request.form['record_name'], request.form['record_type'], request.form['record_value'])
    return """
    <html><body>
    OK
    </body></html>
    """
