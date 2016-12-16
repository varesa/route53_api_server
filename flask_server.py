import traceback

from flask import Flask, request

from r53 import Route53Connection


app = Flask(__name__)

debug = False


@app.route('/')
def home():
    return """
    <html><body>
    Please make a POST request to POST with the parameters aws_access_id, aws_secret_access_key, aws_route53_zone, record_name, record_type and record_value.
    If request_type is 'A' you may omit record_value and the IP address you are connecting from will be used instead.
    </body></html>
    """


def make_message(msg):
    return msg


@app.route('/change', methods=['POST'])
def change():
    if debug:    
        print(request.headers)
        print(request.form)

    if 'X-Forwarded-For' in request.headers.keys():
        source_ip = request.headers['X-Forwarded-For']
    else:
        source_ip = request.remote_addr

    if debug: print("Client address: " + str(source_ip))  
  

    # Check for missing parameters
    if 'aws_access_key_id' not in request.form or 'aws_secret_access_key' not in request.form:
        return make_message("aws_access_key_id or aws_secret_access_key POST parameters missing")

    if 'aws_route53_zone' not in request.form.keys() or 'record_name' not in request.form.keys():
        return make_message("aws_route53_zone or record_name POST parameters missing")


    # Default to setting A record to client IP if parameters missing
    record_type = request.form['record_type'] if 'record_type' in request.form.keys() else 'A'
    record_value = request.form['record_value'] if 'record_value' in request.form.keys() else source_ip

    # Try to update the record
    ret = ""
    try:
        c = Route53Connection(request.form['aws_access_key_id'], request.form['aws_secret_access_key'], request.form['aws_route53_zone'])
        ret = c.change_record(request.form['record_name'], record_type, record_value)
    except:
        print(traceback.format_exc())
        return make_message("An error occurred")

    return make_message(ret)
