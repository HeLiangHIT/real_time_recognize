#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-04 15:59:05
# @Author  : He Liang (heianghit@foxmail.com)
# @Link    : https://github.com/HeLiangHIT
"""
根据人脸数据库匹配人脸
Usage:
  run_recongnize.py [--dir=dir]
  run_recongnize.py --version
Options:
  --dir=dir         face info save dir. *default: .data/face_db
"""

import cv2
import face_recognition
from docopt import docopt
from face_db import *
arguments = docopt(__doc__, version="real time face recognize 0.0.1")
if not arguments["--dir"]:
    arguments["--dir"] = ".data/face_db"
    print("use default dir %s to save face db!" % arguments["--dir"])
known_face_encodings, known_face_names = load_faces_db(arguments["--dir"])
# known_face_encodings, known_face_names = load_faces_img(arguments["--dir"])


def recognize_faces(face_encodings):
    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(
            known_face_encodings, face_encoding)
        name = "unknown"
        # If a match was found in known_face_encodings, just use the
        # first one.
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
        face_names.append(name)
    return face_names


def real_time_face_detect(callback=None):
    '''
    传入参数为回调函数，原型为 names = func(face_encodings), 其中 face_encodings 是人脸编码结果
    '''
    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)
    process_this_frame = True
    scale_factor = 4
    print("press q to quit!")
    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()
        # Resize frame of video to 1/4 size for faster face recognition
        # processing
        small_frame = cv2.resize(
            frame, (0, 0), fx=1.0 / scale_factor, fy=1.0 / scale_factor)
        # Convert the image from BGR color (which OpenCV uses) to RGB color
        # (which face_recognition uses)
        rgb_small_frame = small_frame  # [:, :, ::-1]  # mac unnecessary
        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of
            # video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations)
            face_names = callback(face_encodings)
        process_this_frame = not process_this_frame
        # Display the results
        for pos, name in zip(face_locations, face_names):
            (top, right, bottom, left) = pos
            # Scale back up face locations since the frame we detected in was
            # scaled to 1/4 size
            top *= scale_factor
            right *= scale_factor
            bottom *= scale_factor
            left *= scale_factor

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35),
                          (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX 
            # 中文暂不支持，改进参考 https://www.cnblogs.com/YouXiangLiThon/p/7815124.html
            cv2.putText(frame, name, (left + 6, bottom - 6),
                        font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    real_time_face_detect(recognize_faces)
