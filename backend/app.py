import xmltodict
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from main import *

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/upload-xml', methods=['POST'])
def upload_xml():
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

        # Configure operation name here
        operation_name = "operation-operation1"

        extract_node(xml_data)
        user_list = find_user_by_operation(node_list, operation_name, set())

        res_list = []
        for u in user_list:
            info = get_user_info(xmltodict.parse(xml_file), u)
            if info["occupied"] == "false":
                res_list.append(u)

        response = "Available Users: \n"

        for u in res_list:
            info = get_user_info(xmltodict.parse(xml_file), u)
            # print(info)
            res_endpoint = info["attribute"] + "/" + operation_name
            response += u
            response += ", Endpoint of the user: "
            response += res_endpoint
            response += "\n"

        # return jsonify({"message": "XML data received successfully"})
        return response

    except Exception as e:
        print(e)
        print(request.headers)
        print(request.data)
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


if __name__ == '__main__':
    app.run(debug=True)
