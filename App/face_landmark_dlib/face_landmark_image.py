import cv2 as cv
import matplotlib.pyplot as plt
import dlib
import numpy

# def main():
#
#
#     detector=dlib.get_frontal_face_detector()
#     # 预测模型
#     predictor=dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
#
#     while True:
#         ret,frame=capture.read()
#         if ret:
#             gray=cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
#             faces=detector(gray,1)
#             for face in faces:
#                 cv.rectangle(frame,(face.left(),face.top()),(face.right(),face.bottom()),color=(0,255,0),thickness=2)
#                 #获取关键点
#                 shape=predictor(frame,face)
#                 #循环遍历关键点
#                 for pt in shape.parts():
#                     pt_pos=(pt.x,pt.y)
#                     cv.circle(frame,pt_pos,1,color=(255,0,0),thickness=-1)
#             cv.imshow("detection", frame)
#         if cv.waitKey(10)==27:
#             break
#     cv.destroyAllWindows()
#     capture.release()


def detect_landmark(image):
    detector = dlib.get_frontal_face_detector()
    # 预测模型
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    #转为灰度

    gray=cv.cvtColor(image,cv.COLOR_BGR2GRAY)
    faces=detector(gray,1)
    for face in faces:
        cv.rectangle(image, (face.left(), face.top()), (face.right(), face.bottom()), color=(0, 255, 0), thickness=2)
        # 获取关键点
        shape = predictor(image, face)
        # 循环遍历关键点
        for pt in shape.parts():
            pt_pos = (pt.x, pt.y)
            cv.circle(image, pt_pos, 3, color=(255, 0, 0), thickness=-1)
    return image

# if __name__ == '__main__':
#     image=cv.imread('2.jpg')
#     mark_img=detect_landmark(image)
#
#     while True:
#         cv.imshow("landmark", mark_img)
#         if cv.waitKey(10)==27:
#             break
#
#     cv.destroyAllWindows()