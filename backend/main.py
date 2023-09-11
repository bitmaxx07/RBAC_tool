import pprint

from fastapi import FastAPI
import xml.etree.ElementTree as ET
import xmltodict

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello"}

# with open('output (1).xml', 'r', encoding='utf-8') as file:
#     xml_file = file.read()

# xml_dict = xmltodict.parse(xml_file)
# pprint.pprint(xml_dict, indent=2)

node_list = []


class Node(object):
    def __init__(self, name, mother, node_type):
        self.name = name
        self.mother = mother
        self.node_type = node_type

    def print_node(self):
        print(self.name, self.mother, self.node_type)


def handle_none_string(input_string):
    if input_string is None:
        input_string = "None"
    return input_string


def extract_node(xml_f):
    xml_dic = xmltodict.parse(xml_f)
    temp_list = xml_dic["data"]["operationList"]["operation"]
    if isinstance(temp_list, list):
        for item in xml_dic["data"]["operationList"]["operation"]:
            if item["mother"] is not None:
                node_list.append(Node(item["name"], handle_none_string(item["mother"]["item"]), item["type"]))
            else:
                node_list.append(Node(item["name"], "None", item["type"]))
    else:
        if temp_list["mother"] is not None:
            node_list.append(Node(temp_list["name"], temp_list["mother"]["item"], temp_list["type"]))
        else:
            node_list.append(Node(temp_list["name"], "None", temp_list["type"]))

    temp_list = xml_dic["data"]["roleList"]["role"]
    if isinstance(temp_list, list):
        for item in xml_dic["data"]["roleList"]["role"]:
            node_list.append(Node(item["name"], handle_none_string(item["mother"]["item"]), item["type"]))
    else:
        node_list.append(Node(temp_list["name"], temp_list["mother"]["item"], temp_list["type"]))

    temp_list = xml_dic["data"]["userList"]["user"]
    if isinstance(temp_list, list):
        for item in xml_dic["data"]["userList"]["user"]:
            node_list.append(Node(item["name"], handle_none_string(item["mother"]["item"]), item["type"]))
    else:
        node_list.append(Node(temp_list["name"], temp_list["mother"]["item"], temp_list["type"]))


# extract_node(xml_file)
'''for node in node_list:
    Node.print_node(node)'''


def find_user_by_operation(li, operation, temp_res):
    res = temp_res
    # DFS here?
    for item in li:
        if isinstance(item.mother, str):
            if item.mother == operation and item.node_type == "user":
                res.add(item.name)
            if item.mother == operation and item.node_type != "user":
                find_user_by_operation(li, item.name, res)
        if isinstance(item.mother, list):
            if operation in item.mother and item.node_type == "user":
                res.add(item.name)
            if operation in item.mother and item.node_type != "user":
                find_user_by_operation(li, item.name, res)

    return res


def get_domain_by_operation(xml_f, operation):
    xml_dic = xmltodict.parse(xml_f)
    temp_list = xml_dic["data"]["operationList"]["operation"]
    if isinstance(temp_list, list):
        for item in xml_dic["data"]["operationList"]["operation"]:
            if item["name"] == operation:
                return item["domainName"]
    else:
        if xml_dic["data"]["operationList"]["operation"]["name"] == operation:
            return xml_dic["data"]["operationList"]["operation"]["domainName"]

    return "Operation", operation, "not found! Please check"


def get_user_info(xml_dic, user):
    temp = xml_dic["data"]["userList"]["user"]
    if isinstance(temp, list):
        for item in temp:
            if item["name"] == user:
                return item
    else:
        if temp["name"] == user:
            return temp


# print(find_user_by_operation(node_list, "operation-operation1", set()))

# user_list = find_user_by_operation(node_list, "operation-operation1", set())

'''for u in user_list:
    info = get_user_info(xml_dict, u)
    if info["occupied"] == "false":
        print(u)'''

# print(get_user_info(xml_dict, "user-user2"))
