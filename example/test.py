
import os
import json

today = "30_11_2022"
if not os.path.isfile(os.path.join(today, "subjects_in_frame.json")):
    with open("subjects_in_frame.json", "w") as file:
        json.dump([], file)