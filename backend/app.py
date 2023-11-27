import os.path
import re
import time

import xmltodict
from flask import Flask, request, jsonify, make_response, render_template, redirect
from flask_cors import CORS
from main import *
# from selenium import webdriver
# from selenium.common.exceptions import TimeoutException
import requests
from bs4 import BeautifulSoup
import random
import threading

app = Flask(__name__)
CORS(app)


class Endpoint:
    def __init__(self, name):
        self.name = name
        self.occupied = False


@app.route('/')
def index():
    return "Hello, World!"


# Always configure here! The operation name is formed as this: operation-[operation_name]
operation_name = "operation-op1"
response = ""
first_user_endpoint = ""

connections_list = []
endpoints = []

connections_mapping = {}
fastest_endpoint = ""


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

        for item in res_list:
            endpoint_info = get_user_info(xmltodict.parse(xml_data), item)
            # print(endpoint_info)
            global connections_list
            url = endpoint_info["attribute"] + "/" + get_domain_by_operation(xml_data, operation_name)
            # print(url)
            connections_list.append(url)
            # print(connections_list)
            connections_mapping.update({url: item})
            # print(connections_mapping)

        # print(connections_list)
        '''connections_list = [Endpoint(name) for name in connections_list]
        print(connections_list)
        response += "Fastest connection is " + test_connections() + " from " + connections_mapping[test_connections()]
        print(response)'''

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


def test_connections():
    global connections_list, endpoints

    if not endpoints:
        endpoints = [Endpoint(name) for name in connections_list]

    fastest_connection = None
    fastest_response = float('inf')

    for item in endpoints:
        print(item.name, item.occupied)
        if not item.occupied:
            url, response_time = check_response_time(item.name)
            if response_time < fastest_response:
                fastest_connection = url
                fastest_response = response_time

    global fastest_endpoint
    fastest_endpoint = fastest_connection

    return fastest_connection


@app.route('/fastest', methods=['GET'])
def get_fastest():
    test_connections()
    for item in endpoints:
        print(item.name, item.occupied)
    print(fastest_endpoint)
    if fastest_endpoint == "":
        return "Fastest connection not found or all endpoints are unavailable!"
    else:
        '''external_url = complete_url(fastest_endpoint)
        url_index = None
        for i, item in enumerate(connections_list):
            if complete_url(item.name) == external_url:
                url_index = i
                break
        if url_index is not None:
            # Print something here
            connections_list[url_index].occupied = True
            time.sleep(10)'''
        # print(external_url)
        thread = threading.Thread(target=set_occupied, args=(fastest_endpoint, 120))
        thread.start()
        return redirect(complete_url(fastest_endpoint))


@app.route('/fastest-element', methods=['GET'])
def get_fastest_element():
    test_connections()
    '''for item in endpoints:
        print(item.name, item.occupied)
    print(fastest_endpoint)'''
    if fastest_endpoint == "":
        return "Fastest connection not found or all endpoints are unavailable!"
    else:
        thread = threading.Thread(target=set_occupied, args=(fastest_endpoint, 120))
        thread.start()
        return get_html_element(fastest_endpoint)


def set_occupied(endpoint, delay):
    # print(endpoint)
    external_url = complete_url(endpoint)
    url_index = None
    for i, item in enumerate(endpoints):
        if complete_url(item.name) == external_url:
            url_index = i
            break
    if url_index is not None:
        endpoints[url_index].occupied = True
        time.sleep(delay)
        endpoints[url_index].occupied = False
    else:
        print(f"{endpoint} not found in connection list!")


def complete_url(url):
    if is_valid_ip_address(url) or url.startswith("http://") or url.startswith("https://"):
        return url

    else:
        completed_url = "http://" + url
        return completed_url


def is_valid_ip_address(url):
    ip_pattern = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][" \
                 r"0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    return re.match(ip_pattern, url)


def check_response_time(url):
    try:
        # print(url)
        start_time = time.time()
        res = requests.get(complete_url(url))
        # print(complete_url(url))
        end_time = time.time()
        res_ms = (end_time - start_time) * 1000
        if res.status_code == 200:
            print(url, "connection time: ", str(res_ms) + "ms")
            return url, end_time - start_time
        else:
            # print(res.status_code)
            return url, float('inf')
    except Exception as e:
        print(f"Error checking {url}: {e}")
        return url, float('inf')


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


def get_html_element(address):
    r = requests.get(complete_url(address))
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        elements = soup.find_all(True)
        res = ""
        for e in elements:
            res += str(e)
        return res
    else:
        return "Failed to retrieve webpage, status code: " + str(r.status_code)


@app.route('/fastest/html', methods=['GET'])
def get_fastest_html():
    r = requests.get(complete_url(fastest_endpoint))
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        elements = soup.find_all(True)
        res = ""
        for e in elements:
            res += str(e)
        # Set the fastest endpoint as occupied
        # set_occupied(fastest_endpoint)
        result_message = res
        thread = threading.Thread(target=set_occupied, args=(fastest_endpoint, 120))
        thread.start()
        return result_message
        # return res
    else:
        result_message = "Failed to retrieve webpage, status code: " + str(r.status_code)
        return result_message


@app.route('/epsilon', methods=['GET'])
def epsilon_greedy():
    test_connections()

    p = random.random()
    # configure p as 0.7
    if p < 0.7:
        print("The fastest connection selected")
        thread = threading.Thread(target=set_occupied, args=(fastest_endpoint, 120))
        thread.start()
        return fastest_endpoint
    else:
        print("Randomly selected")
        selected_endpoint = random.choice(endpoints).name
        thread = threading.Thread(target=set_occupied, args=(selected_endpoint, 120))
        thread.start()
        return selected_endpoint


@app.route('/epsilon-element', methods=['GET'])
def epsilon_greedy_element():
    test_connections()
    p = random.random()
    if p < 0.7:
        print("The fastest connection selected")
        thread = threading.Thread(target=set_occupied, args=(fastest_endpoint, 120))
        thread.start()
        return get_html_element(fastest_endpoint)
    else:
        print("Randomly selected")
        selected_endpoint = random.choice(endpoints).name
        thread = threading.Thread(target=set_occupied, args=(selected_endpoint, 120))
        thread.start()
        return get_html_element(selected_endpoint)


@app.route('/take-user/<string:username>', methods=['POST'])
def take_user(username):
    """
    This method sets user from unoccupied to occupied by sending a post request
    :param username: user to take
    :return: server feedback
    """
    '''try:
        # Trigger changeUserStatus(userName) in temp.html
        # changeUserStatus(username)
        javascript_call = f"changeUserStatus('{username}');"
        javascript_path = os.path.join(os.path.abspath('../Whiteboard'), 'temp.html')
        # return jsonify({"message": "User status changed successfully"})
        return render_template(javascript_path, javascript_call=javascript_call)
    except Exception as e:
        return jsonify({"error": str(e)}), 500'''
    '''try:
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
        return error_message'''
    res = username, "occupied"
    return res, 200


@app.route('/set-unoccupied/<string:username>', methods=['POST'])
def set_unoccupied(username):
    """
    This method sets user from occupied to unoccupied by sending a post request
    :param username:
    :return:
    """
    res = username, "unoccupied"
    return res, 200


if __name__ == '__main__':
    app.run(debug=True)
