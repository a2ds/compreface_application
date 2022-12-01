import os
import numpy as np
import json
import cv2
import argparse
import time
from datetime import datetime
from threading import Thread
from compreface import CompreFace
from compreface.service import RecognitionService
from convert import subject_to_name

# def some keywords use later
now = datetime.today()
today = now.strftime("%d_%m_%Y")

if not os.path.isdir(today):
    os.mkdir(today)

subjects_in_frame_json = os.path.join(today, "subjects_in_frame.json")
if not os.path.isfile(subjects_in_frame_json):
    with open(subjects_in_frame_json, "w") as file:
        json.dump([], file)

def parseArguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("--api-key", help="CompreFace recognition service API key", type=str, default='b5192adc-1258-43ad-8821-83198eef869b')
    parser.add_argument("--host", help="CompreFace host", type=str, default='http://localhost')
    parser.add_argument("--port", help="CompreFace port", type=str, default='8000')

    args = parser.parse_args()

    return args

class ThreadedCamera:
    def __init__(self, api_key, host, port):
        self.active = True
        self.results = []
        self.capture = cv2.VideoCapture("rtsp://admin:caothang2021@192.168.0.250:1250")
        # self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 2)

        compre_face: CompreFace = CompreFace(host, port, {
            "limit": 0,
            "det_prob_threshold": 0.2,
            "prediction_count": 1,
            "face_plugins": "age,gender",
            "status": False
        })

        self.recognition: RecognitionService = compre_face.init_face_recognition(api_key)
        self.subjects = self.recognition.get_subjects()

        # Start frame retrieval thread
        self.thread = Thread(target=self.show_frame, args=())
        self.thread.daemon = True
        self.thread.start()

    def show_frame(self):
        print("Started")


        subjects_last_150_frames = []
        while self.capture.isOpened():
            self.tic = time.time()
            now = datetime.today()
            current_time = now.strftime("%H_%M_%S")

            (status, frame_raw) = self.capture.read()
            self.frame = cv2.flip(frame_raw, 1)

            subjects_current_frame = []
            if self.results:

                results = self.results

                for result in results:
                    box = result.get('box')
                    subjects = result.get('subjects')
                    if box:
                        cv2.rectangle(img=self.frame, pt1=(box['x_min'], box['y_min']),
                                      pt2=(box['x_max'], box['y_max']), color=(0, 255, 0), thickness=1)

                    if subjects:
                        subjects = sorted(subjects, key=lambda k: k['similarity'], reverse=True)
                        subject = f"No known faces"
                        similarity = f"Similarity: {subjects[0]['similarity']}"

                        if subjects[0]['similarity'] > 0.7:
                            subject = subjects[0]['subject']
                            subjects_current_frame.append(subject)
                            subject = f"Subject: {subjects[0]['subject']}"
                            cv2.putText(self.frame, similarity, (box['x_max'], box['y_min'] + 95),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
                        cv2.putText(self.frame, subject, (box['x_max'], box['y_min'] + 75),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)

                # Save frame:
                save_frame = False

                for subject in subjects_current_frame:
                    k = True in (subject in fr for fr in subjects_last_150_frames)
                    if k:
                        pass
                    else:
                        with open(subjects_in_frame_json, "r") as file:
                            subjects_in_frame = json.load(file)

                        new_subjects_in_frame = {"time": current_time, "subject": subjects_current_frame, "name": subject_to_name(subjects_current_frame)}
                        subjects_in_frame.append(new_subjects_in_frame)
                        with open(subjects_in_frame_json, "w") as file:
                            json.dump(subjects_in_frame, file)
                        cv2.imwrite(os.path.join(today, f"{current_time}.png"), self.frame)
                        break

            # Save current subject to list:
            subjects_last_150_frames.append(subjects_current_frame)
            if len(subjects_last_150_frames) == 150:
                subjects_last_150_frames.pop(0)

            self.toc = time.time()
            total_time = self.toc-self.tic
            self.FPS = 1/total_time
            cv2.putText(self.frame, str(self.FPS), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)


            cv2.imshow('CompreFace demo', self.frame)

            if cv2.waitKey(1) & 0xFF == 27:
                self.capture.release()
                cv2.destroyAllWindows()
                self.active=False

    def is_active(self):
        return self.active

    def update(self):
        if not hasattr(self, 'frame'):
            return

        _, im_buf_arr = cv2.imencode(".jpg", self.frame)
        byte_im = im_buf_arr.tobytes()
        data = self.recognition.recognize(byte_im)
        self.results = data.get('result')

if __name__ == '__main__':
    args = parseArguments()
    threaded_camera = ThreadedCamera(args.api_key, args.host, args.port)
    while threaded_camera.is_active():
        threaded_camera.update()