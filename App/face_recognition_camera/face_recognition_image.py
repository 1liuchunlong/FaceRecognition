import cv2 as cv
import face_recognition
import dlib
import numpy as np
import time
from imutils import face_utils
from os import listdir, path
from App.face_recognition_camera.FaceSQL import FaceSQL
from App.face_recognition_camera.FaceTools import FaceTools


# 返回值是最像的人脸的标签

def face_recognitions(frame_rgb):
    face_tools = FaceTools()
    names, encodings = face_tools.load_faceOfDataBase()
    # print("=======", encodings)

    # # bgr转rgb
    frame_rgb = frame_rgb[:, :, ::-1]

    # 人脸检测
    frame_faces = face_recognition.face_locations(frame_rgb)

    # 人脸特征编码
    face_encodings = face_recognition.face_encodings(frame_rgb, frame_faces)

    # 与数据中的所有人脸进行比较
    for (top, right, bottom, left), face_encoding in zip(frame_faces, face_encodings):
        # 进行匹配
        matches = face_recognition.compare_faces(encodings, face_encoding)
        # 计算距离
        distances = face_recognition.face_distance(encodings, face_encoding)
        min_distance_index = np.argmin(distances)

        name = "unknown"
        if matches[min_distance_index]:
            name = names[min_distance_index]


    return name;
