import os
import json
from damsenviet.kle import Keyboard

# relative to this file
json_relative_file_path = "./keyboard-layout.json"
json_absolute_file_path = os.path.abspath(
    os.path.join(
        os.path.dirname(os.path.realpath('__file__')),
        json_relative_file_path,
    )
)

print(json_absolute_file_path)
keyboard = Keyboard.from_json(
    json.loads(json_absolute_file_path)
)

# for key in keyboard.keys:
#     for label in key.labels:
#         pass