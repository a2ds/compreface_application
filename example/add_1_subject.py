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

def add_new_subject(img_path: str, img_subject, name: str, DOMAIN = "http://localhost", PORT = "8000", API_KEY = '0000000000000000000000000000'):
    img_subject = str(img_subject)
    # Add to compreface
    compre_face: CompreFace = CompreFace(DOMAIN, PORT)
    recognition: RecognitionService = compre_face.init_face_recognition(API_KEY)

    face_collection: FaceCollection = recognition.get_face_collection()

    subjects: Subjects = recognition.get_subjects()

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
        json_data = {img_subject: name}
        json_date = {img_subject: today}
        json_time = {img_subject: time}

        with open(json_path_data, "w", encoding='utf8') as file:
            json.dump(json_data, file, ensure_ascii=False)
        with open(json_path_date, "w", encoding='utf8') as file:
            json.dump(json_date, file, ensure_ascii=False)
        with open(json_path_time, "w", encoding='utf8') as file:
            json.dump(json_time, file, ensure_ascii=False)

# EXAMPLE
add_new_subject("bao.png", 1001, "bao", API_KEY= "b5192adc-1258-43ad-8821-83198eef869b")














