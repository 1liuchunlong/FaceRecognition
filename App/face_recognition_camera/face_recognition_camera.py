import cv2 as cv
import face_recognition
import dlib
import numpy as np
import time
from imutils import face_utils
from os import listdir, path
from FaceSQL import FaceSQL
from FaceTools import FaceTools


# 嘴长宽比例
def mouth_aspect_ratio(mouth):
    A = np.linalg.norm(mouth[1] - mouth[7])  # 61, 67
    B = np.linalg.norm(mouth[3] - mouth[5])  # 63, 65
    C = np.linalg.norm(mouth[0] - mouth[4])  # 60, 64
    mar = (A + B) / (2.0 * C)
    return mar


# 加载图片
# liu=cv.imread('./liu001.jpg')
# guo=cv.imread('./guo001.jpg')
# chun=cv.imread('./friends11.jpg')
# peng=cv.imread('./peng.jpg')

##新加内容实现数据库管理
face_tools = FaceTools()
# face_tools.add_Face("liu001.jpg","liudehua")
# face_tools.add_Face("guo001.jpg","guofucheng")
# face_tools.add_Face("peng.jpg","pengyuyan")
# face_tools.add_Face("friends11.jpg","liuchunlong")


# bgr转rgb
# liu_rgb=liu[:,:,::-1]
# guo_rgb=guo[:,:,::-1]
# chun_rgb=chun[:,:,::-1]
# peng_rgb=peng[:,:,::-1]
# # 检测人脸
# liu_face=face_recognition.face_locations(liu_rgb)
# guo_face=face_recognition.face_locations(guo_rgb)
# chun_face=face_recognition.face_locations(chun_rgb)
# peng_face=face_recognition.face_locations(peng_rgb)
#
#
# # 人脸特征编码
# liu_encodings=face_recognition.face_encodings(liu_rgb,liu_face)[0]
# guo_encodings=face_recognition.face_encodings(guo_rgb,guo_face)[0]
# chun_encodings=face_recognition.face_encodings(chun_rgb,chun_face)[0]
# peng_encodings=face_recognition.face_encodings(peng_rgb,peng_face)[0]

# 人脸数据库
# encodings=[liu_encodings,guo_encodings,chun_encodings,peng_encodings]
# names=["liu de hua","guo fu cheng","liu chun long","peng yu yan"]
names, encodings = face_tools.load_faceOfDataBase()
print("=======", encodings)

# 打开摄像头
capture = cv.VideoCapture(0)
if not capture.isOpened():
    raise IOError("CAMERA ERROR")

while True:
    ret, frame = capture.read()

    # bgr转rgb
    frame_rgb = frame[:, :, ::-1]
    # 人脸检测
    frame_faces = face_recognition.face_locations(frame_rgb)
    print("------------------------------")
    frame_faces = np.array(frame_faces).astype('uint8')
    print(type(frame_faces))

    # 人脸特征编码
    # face_encodings = face_recognition.face_encodings(frame_rgb)
    #
    # # 与数据中的所有人脸进行比较
    # for (top, right, bottom, left), face_encoding in zip(frame_faces, face_encodings):
    #     # 进行匹配
    #     matches = face_recognition.compare_faces(encodings, face_encoding)
    #     # 计算距离
    #     distances = face_recognition.face_distance(encodings, face_encoding)
    #     min_distance_index = np.argmin(distances)
    #
    #     name = "unknown"
    #     if matches[min_distance_index]:
    #         name = names[min_distance_index]
    #
    #     # 绘制人脸矩形框
    #     cv.rectangle(frame, (left, top), (right, bottom), color=(0, 255, 0), thickness=2)
    #
    #     # 绘制名字
    #     cv.rectangle(frame, (left, bottom - 30), (right, bottom), color=(255, 0, 0), thickness=1)
    #
    #     cv.putText(frame, name, (left + 10, bottom - 10), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), thickness=1)
    #
    # cv.imshow("recognition", frame)
    # if cv.waitKey(1) == 27:
    #     break
capture.release()
cv.destroyAllWindows()

# 惊醒
