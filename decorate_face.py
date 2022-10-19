#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-04 15:59:05
# @Author  : He Liang (heianghit@foxmail.com)
# @Link    : https://github.com/HeLiangHIT
"""
查找人脸并在此基础上装饰人脸
Usage:
  decorate_face.py [--deco=deco]
  decorate_face.py --version
Options:
  --deco=deco         face info save deco. *default: cigarette
"""

import cv2
import numpy as np
from PIL import Image
from imutils import face_utils, resize
from dlib import get_frontal_face_detector, shape_predictor
from docopt import docopt
arguments = docopt(__doc__, version="real time face recognize 0.0.1")
if not arguments["--deco"]:
    arguments["--deco"] = "cigarette"


# 基本人脸检测对象
detector = get_frontal_face_detector()
predictor = shape_predictor('./res/shape_predictor_68_face_landmarks.dat')


cigarette = Image.open('./res/cigarette.png') 
glasses = Image.open('./res/glasses.png') 
def add_cigarettes(image):
    # 验证是否存在人脸
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rects = detector(img_gray, 0)
    if len(rects) == 0:
        return image # 不存在人脸
    draw_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    for rect in rects:
        # 寻找各个位置
        face_width = rect.right() - rect.left()
        predictor_shape = predictor(img_gray, rect)
        face_shape = face_utils.shape_to_np(predictor_shape)

        # mouth = face_shape[49:68]
        mouth_center = face_shape[49:68].mean(axis=0).astype("int")
        cigarette_sized = cigarette.resize(
            (face_width, int(face_width * cigarette.size[1] / cigarette.size[0])),
            resample=Image.LANCZOS)
        cigarette_pos = (face_shape[49:68][0, 0] - face_width + int(16 * face_width / cigarette.size[0]), mouth_center[1])

        # left_eye,right_eye = face_shape[36:42],face_shape[42:48]
        left_eye_center = face_shape[36:42].mean(axis=0).astype("int")
        right_eye_center = face_shape[42:48].mean(axis=0).astype("int")
        y = left_eye_center[1] - right_eye_center[1]
        x = left_eye_center[0] - right_eye_center[0]
        eye_angle = np.rad2deg(np.arctan2(y, x))
        glasses_resized = glasses.resize(
            (face_width, int(face_width * glasses.size[1] / glasses.size[0])),
            resample=Image.LANCZOS)

        glasses_roted = glasses_resized.rotate(eye_angle, expand=True)
        glasses_fliped = glasses_roted.transpose(Image.FLIP_TOP_BOTTOM)

        glasses_pos = (face_shape[36:42][0, 0] - face_width // 4, face_shape[36:42][0, 1] - face_width // 6)
        # 绘制人脸装饰物
        draw_img.paste(cigarette_sized, cigarette_pos, cigarette_sized)
        draw_img.paste(glasses_fliped, glasses_pos, glasses_fliped)
    return cv2.cvtColor(np.asarray(draw_img), cv2.COLOR_RGB2BGR)

deco_func={
    "cigarette": add_cigarettes,
}


def real_time_face_decorate(callback=None):
    '''
    传入参数为回调函数，原型为 result = func(image), 其中 image 是摄像头拍摄图像
    '''
    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)
    scale_factor = 2
    print("press q to quit!")
    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=1.0 / scale_factor, fy=1.0 / scale_factor)
        # Convert the image from BGR color (which OpenCV uses) to RGB color
        # (which face_recognition uses)
        rgb_small_frame = small_frame  # [:, :, ::-1]  # mac unnecessary
        # Only process every other frame of video to save time
        result = callback(rgb_small_frame)
        # Display the resulting image
        cv2.imshow('Video', result)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    if arguments["--deco"] not in deco_func.keys():
        print("undefined deco: %" % arguments["--deco"])
    else:
        real_time_face_decorate(deco_func[arguments["--deco"]])
