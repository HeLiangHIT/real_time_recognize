#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-04 15:57:53
# @Author  : He Liang (heianghit@foxmail.com)
# @Link    : https://github.com/HeLiangHIT

"""
创建人脸数据库，保存为npy和img文件到文件夹中，以人名字来命名
Usage:
  face_db.py [--name=<arg>] [--image=<arg>] [--dir=dir]
  face_db.py --version
Options:
  --name=name       select name. [default: unkown]
  --image=image     image path or use camera.
  --dir=dir         face info save dir. *default: $HOME/Pictures/head/
"""

import platform
import numpy
import cv2
import face_recognition
import os
from docopt import docopt

sysstr = platform.system() # Windows  Linux  


def list_file(filedir, sufix=None):
    # 根据输入的后缀来列举文件夹中的文件, 也许可以使用 glob.glob(os.path.join(filedir, "*.jpg")) 精简
    file_list = os.listdir(filedir)
    file_list = [os.path.join(filedir, f) for f in file_list] # add path for files
    if sufix is not None:
        ret_list = [f for f in file_list if f.endswith(sufix)]
        return ret_list
    else:
        return file_list


def encode_face(filename=None):
    # 提取照片中最明显的人脸并进行特征提取, 如果输入照片为空则打开摄像机取照片
    if filename is not None:
        image = cv2.imread(filename)
    else:
        # Get a reference to webcam #0 (the default one)
        video_capture = cv2.VideoCapture(0)
        print("press the space or enter if ready!")
        while True:
            # Grab a single frame of video
            ret, frame = video_capture.read()
            # Display the resulting image
            cv2.imshow('Video', frame)
            k = cv2.waitKey(1)
            if k in [13, 32]: # enter or space
                break
            # else:
            #     print("you pressed %d " % k)
        # Convert the image from BGR color (which OpenCV uses) to RGB color
        # (which face_recognition uses)
        image = frame # [:, :, ::-1]  # mac unnecessary
        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()

    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)
    top, right, bottom, left = face_locations[0]
    face_img = image[top:bottom, left:right, :]
    face_encode = face_encodings[0]
    return face_encode, face_img


def load_faces_db(dirname):
    # 从数据库加载人脸数据
    face_encodes = []
    face_names = []
    for filename in list_file(dirname, '.npy'):
        face_names.append(filename.split("/")[-1].split(".")[0])
        face_encode = numpy.load(filename)
        face_encodes.append(face_encode)
    return face_encodes, face_names


def load_faces_img(dirname):
    # 从人脸图像加载人脸数据
    face_encodes = []
    face_names = []
    for img_file in list_file(dirname, '.jpg'):
        face_names.append(img_file.split("/")[-1].split(".")[0])
        face_encode = encode_face(img_file)
        face_encodes.append(face_encode)
    return face_encodes, face_names


def save_face_db(face_encode, name, dirname):
    # 人脸特征保存下来
    filename = '%s/%s.npy' % (dirname, name)
    numpy.save(filename, face_encode)


def save_face_photo(face_img, name, dirname):
    filename = '%s/%s.jpg' % (dirname, name)
    cv2.imwrite(filename, face_img)


if __name__ == '__main__':
    arguments = docopt(__doc__, version="face_db 0.0.1")
    if not arguments["--dir"]:
        home = os.path.expanduser('~') # os.environ['HOME']
        arguments["--dir"] = "%s/Pictures/head/" % home
        print("use default dir %s to save face db!" % arguments["--dir"])
    try:
        os.makedirs(arguments["--dir"])
    except FileExistsError:
        pass
    face_encode, face_img = encode_face(arguments["--image"])
    save_face_photo(face_img, arguments["--name"], arguments["--dir"])
    save_face_db(face_encode, arguments["--name"], arguments["--dir"])
