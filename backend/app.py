import os.path

import xmltodict
from flask import Flask, request, jsonify, make_response, render_template
from flask_cors import CORS
from main import *
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return "Hello, World!"


# Always configure here!
operation_name = "operation-op1"
response = ""
first_user_endpoint = ""


@app.route('/upload-xml', methods=['POST'])
def upload_xml():
    global response
    try:
        # print(request)
        print("Reading xml data...")
        if 'xmlData' in request.files:
            xml_data = request.files['xmlData'].read()
        else:
            # Thia line is just for REST Client testing
            xml_data = request.data
        # print(xml_data)
        print("XML Data Received:")
        print(xml_data.decode())

        extract_node(xml_data)
        user_list = find_user_by_operation(node_list, operation_name, set())

        res_list = []
        for u in user_list:
            info = get_user_info(xmltodict.parse(xml_data), u)
            if info["occupied"] == "false":
                res_list.append(u)

        response = "Available Users: "

        for u in res_list:
            info = get_user_info(xmltodict.parse(xml_data), u)
            # print(info)
            res_endpoint = info["attribute"] + "/" + get_domain_by_operation(xml_data, operation_name)
            response += u
            response += ", Endpoint of the user: "
            response += res_endpoint
            response += ". "

        info = get_user_info(xmltodict.parse(xml_data), res_list[0])
        global first_user_endpoint
        first_user_endpoint = info["attribute"] + "/" + get_domain_by_operation(xml_data, operation_name)

        print(response)

        # return jsonify({"message": "XML data received successfully"})
        return response

    except Exception as e:
        print(e)
        # print(request.headers)
        # print(request.data)
        '''print(request.content_type)
        return request.data'''
        error_response = make_response("Error: " + str(e), 400)
        error_response.headers['Content-Type'] = 'text/plain'
        return error_response


@app.route('/get-xml', methods=['POST'])
def get_xml_data():
    xml_data = request.data
    app.logger.info("Received XML data: %s", xml_data)

    return jsonify({"message": "XML data received successfully"})


@app.route('/response/<string:op_name>', methods=['GET'])
def get_response(op_name):
    if op_name == operation_name:
        return response
    else:
        return "Operation not found!"


@app.route('/access/<string:op_name>', methods=['GET'])
def get_resource(op_name):
    """
    This method returns all HTML elements of the endpoint of the first available user
    :param op_name: operation name
    :return: HTML elements of the first user's endpoint
    """
    if op_name == operation_name:
        global first_user_endpoint
        if not first_user_endpoint.startswith("https://") or not first_user_endpoint.startswith("http://"):
            first_user_endpoint = "https://" + first_user_endpoint
        r = requests.get(first_user_endpoint)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            elements = soup.find_all(True)
            res = ""
            for e in elements:
                res += str(e)
            return res
        else:
            return "Failed to retrieve webpage, status code: " + str(r.status_code)
        # return response
    else:
        return "Operation not found!"


@app.route('/take-user/<string:username>', methods=['POST'])
def take_user(username):
    '''try:
        # Trigger changeUserStatus(userName) in temp.html
        # changeUserStatus(username)
        javascript_call = f"changeUserStatus('{username}');"
        javascript_path = os.path.join(os.path.abspath('../Whiteboard'), 'temp.html')
        # return jsonify({"message": "User status changed successfully"})
        return render_template(javascript_path, javascript_call=javascript_call)
    except Exception as e:
        return jsonify({"error": str(e)}), 500'''
    try:
        print("starting chrome driver...")
        driver = webdriver.Chrome(executable_path="/Users/maqiaoming/Downloads/chromedriver-mac-x64/chromedriver")
        print("ok for chrome driver")
        driver.set_page_load_timeout(30)

        driver.get('/Users/maqiaoming/WebstormProjects/RBAC_tool/Whiteboard/temp.html')

        script = f"""
        const userIndex = userList.findIndex(obj => obj.name === '{username}')
        if (userIndex !== -1) {{
          userList[userIndex].occupied = userList[userIndex].occupied === "true" ? "false" : "true";
          console.log(userList[userIndex]);
        }}
        else {{
          console.log("User not found!");
        }}
        """

        driver.execute_script(script)
        driver.quit()
        return jsonify({"message": "User status changed successfully"})
    except TimeoutException as e:
        return "TimeoutException: Page load timed out."
    except Exception as e:
        error_message = "An error occurred: " + str(e)
        print(error_message)
        return error_message


if __name__ == '__main__':
    app.run(debug=True)
