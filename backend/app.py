from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/upload-xml', methods=['POST'])
def upload_xml():
    try:
        # print(request)
        xml_data = request.files['xmlData'].read()
        # print(xml_data)
        print("XML Data Received:")
        print(xml_data.decode())
        return jsonify({"message": "XML data received successfully"})
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)})


@app.route('/get-xml', methods=['POST'])
def get_xml_data():
    xml_data = request.data
    app.logger.info("Received XML data: %s", xml_data)
    # Your XML processing logic here
    return jsonify({"message": "XML data received successfully"})


if __name__ == '__main__':
    app.run(debug=True)
