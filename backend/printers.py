import threading

from flask import Flask, redirect, url_for, request
import time
import sys

app = Flask(__name__)

count_printer1 = 0
count_printer2 = 0
count_printer3 = 0


def printer1():
    global count_printer1
    if count_printer1 < 5:
        time.sleep(5)
    else:
        time.sleep(3)
    count_printer1 += 1
    return "success: printer1"


def printer2():
    global count_printer2
    if count_printer2 <= 3:
        time.sleep(10)
    else:
        time.sleep(1)
    count_printer2 += 1
    return "success: printer2"


def printer3():
    global count_printer3
    if count_printer3 <= 10:
        time.sleep(1)
    else:
        time.sleep(5)
    count_printer3 += 1
    return "success: printer3"


'''def printer1_test():
    if count_printer1 < 5:
        time.sleep(5)
    else:
        time.sleep(3)
    return "test: printer1"


def printer2_test():
    if count_printer2 <= 3:
        time.sleep(10)
    else:
        time.sleep(1)
    return "test: printer2"


def printer3_test():
    if count_printer3 <= 10:
        time.sleep(1)
    else:
        time.sleep(5)
    return "test: printer3"'''


'''def test_printers():
    threads = []
    test_functions = [printer1_test, printer2_test, printer3_test]

    for func in test_functions:
        thread = threading.Thread(target=func)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return "All printers tested successfully"'''


'''@app.route("/test-connection", methods=['GET'])
def test_all_printers():
    return test_printers()'''


hostnames = {
        '3d-printer-1': printer1,
        '3d-printer-2': printer2,
        '3d-printer-3': printer3
}


@app.route("/print-model", methods=['GET'])
def hello():
    print(request.host)
    domain = request.host.split(":")[0]
    if domain in hostnames:
        return hostnames[domain]()


if __name__ == "__main__":
    app.run(debug=True, port=4242)
