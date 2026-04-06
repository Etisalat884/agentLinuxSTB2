import json
import re

import requests
import datetime


def listconv(list1, list2):
    res1 = list1.split(r"-")
    res2 = list2.split(r"-")
    dict1 = {}
    for i, j in zip(res1, res2):
        dict1[j] = i
    return dict1


def Status(trigger_id, agent_id, status, result):
    key = {"trigger_id": trigger_id, "agent_id": agent_id}
    res = {"result": result}
    Post_Result(key, res)
    status = {"status": status}
    Post_status(key, status)

    return res, status


def Evaluate_time_result(execution_id, result, start_time, end_time):
    # Convert input strings to datetime objects
    format = "%Y-%m-%d %H:%M:%S"
    start = datetime.datetime.strptime(start_time, format)
    end = datetime.datetime.strptime(end_time, format)
    elapsed_time = str(end - start)
    print("elapsed_time", elapsed_time)
    exec_id = {"execution_id": execution_id}
    attribute = {"duration_of_testing": elapsed_time, "result": result}
    # status_res = {"execution_id": execution_id, "result": result}
    status_res = {"result": result}
    Post_Result(exec_id, status_res)
    Post_time_result(exec_id, attribute)
    return elapsed_time


def Post_time_result(key, attribute):
    url = "http://192.168.1.58:5000/update_test_case_tracking_details?key="
    data1 = json.dumps(key)
    data2 = json.dumps(attribute)
    print(url + data1 + "&attribute=" + data2)
    x = requests.post(url + data1 + "&attribute=" + data2)
    print(x)
    return x


def Post_status(key, dict_data):
    print("JS,", dict_data)
    url_s = "http://192.168.1.58:5000/update_data_dashboard?key="
    data1 = json.dumps(key)
    data2 = json.dumps(dict_data)
    print(url_s + data1 + "&attribute=" + data2)
    x = requests.post(url_s + data1 + "&attribute=" + data2)
    return x


def Post_Result(key, dict_data):
    print("JS,", dict_data)
    url = "http://192.168.1.58:5000/update_data_dashboard?key="
    data1 = json.dumps(key)
    data2 = json.dumps(dict_data)
    print(url + data1 + "&attribute=" + data2)
    x = requests.post(url + data1 + "&attribute=" + data2)
    return x

