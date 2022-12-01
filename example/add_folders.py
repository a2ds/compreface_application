import random

from compreface import CompreFace
from compreface.service import RecognitionService
from compreface.collections import FaceCollection
from compreface.collections.face_collections import Subjects
from datetime import datetime
import os
import json

# def some keywords use later
now = datetime.today()
currenttime = now.strftime("%d-%m-%Y-%H-%M-%S")
today = now.strftime("%d-%m-%Y")
time = now.strftime("%H:%M:%S")

def add_new_subjects(data_path: str, names: list, DOMAIN = "http://localhost", PORT = "8000", API_KEY = '0000000000000000000000000000'):
    compre_face: CompreFace = CompreFace(DOMAIN, PORT)

    recognition: RecognitionService = compre_face.init_face_recognition(API_KEY)

    face_collection: FaceCollection = recognition.get_face_collection()

    subjects: Subjects = recognition.get_subjects()

    # Read folder
    data_folders = os.listdir((data_path))
    images_list = []
    folders_list = []

    for folder in data_folders:
        image_subjects = os.listdir(os.path.join(data_path, folder))
        for subject in image_subjects:
            images_list.append(os.path.join(data_path, folder, subject))
            folders_list.append(str(folder))

    for img_path, img_subject in zip(images_list, folders_list):
        image_path: str = img_path
        subject: str = img_subject
        face_collection.add(image_path=image_path, subject=subject)

    # Add to json file

    json_path_data = "data.json"
    json_path_date = "date.json"
    json_path_time = "time.json"

    # Case 1: db has data
    if os.path.isfile(json_path_data):
        with open(json_path_data, "r", encoding='utf8') as file:
            json_data = json.load(file)
        with open(json_path_date, "r", encoding='utf8') as file:
            json_date = json.load(file)
        with open(json_path_time, "r", encoding='utf8') as file:
            json_time = json.load(file)

        for img_subject, name in zip(folders_list, names):
            # if that person already exist in db:
            if img_subject in list(json_data.keys()):
                pass
            else:
                json_data[img_subject] = name
                json_date[img_subject] = str(today)
                json_time[img_subject] = str(time)

        with open(json_path_data, "w", encoding='utf8') as file:
            json.dump(json_data, file, ensure_ascii=False)
        with open(json_path_date, "w", encoding='utf8') as file:
            json.dump(json_date, file, ensure_ascii=False)
        with open(json_path_time, "w", encoding='utf8') as file:
            json.dump(json_time, file, ensure_ascii=False)

    # Case 2: db no data
    else:
        json_data = {}
        json_date = {}
        json_time = {}

        for img_subject, name in zip(folders_list, names):
            # if that person already exist in db:
            if img_subject in list(json_data.keys()):
                pass
            else:
                json_data[img_subject] = name
                json_date[img_subject] = str(today)
                json_time[img_subject] = str(time)

        with open(json_path_data, "w", encoding='utf8') as file:
            json.dump(json_data, file, ensure_ascii=False)
        with open(json_path_date, "w", encoding='utf8') as file:
            json.dump(json_date, file, ensure_ascii=False)
        with open(json_path_time, "w", encoding='utf8') as file:
            json.dump(json_time, file, ensure_ascii=False)

# EXAMPLE
names = list(range(0,77))
add_new_subjects("staff", names, API_KEY="25ea8347-b03c-4ad5-a04c-ca7b70e7cd0a")













