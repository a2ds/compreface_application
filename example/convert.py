import json

json_path_data = "data.json"

def subject_to_name(list_of_subject: list):
    result = []
    with open(json_path_data, "r", encoding='utf8') as file:
        json_data = json.load(file)
    for subject in list_of_subject:
        result.append(json_data[subject])
    return result