import base64
import json
import os

import cv2
import numpy as np
from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer

from App.face_recognition_camera.face_recognition_image import face_recognitions
from App.liveness_detection.test import liveness_detection

def recognition(img):
    imgData=img
    flag = liveness_detection(img)
    img = base64_to_image(imgData)
    # base64解码
    img = base64.b64decode(imgData)
    # 转换为np数组
    img = np.fromstring(img, np.uint8)
    name=face_recognitions(img)

    return (name,flag)

def base64_to_image(base64_code):
    """
    将base64编码解析成opencv可用图片
    base64_code: base64编码后数据
    Returns: cv2图像，numpy.ndarray
    """
    # base64解码
    img_data = base64.b64decode(base64_code)
    # 转换为np数组
    img_array = np.fromstring(img_data, np.uint8)
    # 转换成opencv可用格式
    img = cv2.imdecode(img_array, cv2.COLOR_RGB2BGR)
    # faceRecognition(img_array)
    return img


def show(img):
    cv2.imshow('000', img)
    cv2.waitKey(0)
    # cv.destroyAllWindows()
    print("22222222222222222222222222")


class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        print("接收到连接请求")
        # 有客户端来向后端发送websocket连接的请求时,自动触发.
        # 服务端允许和客户端创建连接
        self.accept()

    def websocket_receive(self, message):
        # 浏览器基于websocket向后端发送数据，自动触发接收消息。
        str_image = message['text']

        # show(img)
        self.send("你好")
        # jsonData=json.loads(str_image)
        # print(jsonData['username'])
        # 以下两行是识别部分
        # img=
        result=recognition(str_image)
        self.send("here  is"+result)

        # self.close()

    def websocket_disconnect(self, message):
        # 客户端与服务器断开连接时，自动触发。
        print("断开连接")
        raise StopConsumer()
