import cv2 as cv
import face_recognition
import dlib
import numpy as np
from imutils import face_utils

# 初始化眨眼次数
blink_total = 0
# 初始化张嘴次数
mouth_total = 0
# 设置图片存储路径
pic_path = r'images\viode_face.jpg'
# 图片数量
pic_total = 0
# 初始化眨眼的连续帧数以及总的眨眼次数
blink_counter = 0
# 初始化张嘴状态为闭嘴
mouth_status_open = 0



def eye_aspect_ratio(eye):
    # (|e1-e5|+|e2-e4|) / (2|e0-e3|)
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    ear = (A + B) / (2.0 * C)
    return ear
# 嘴长宽比例
def mouth_aspect_ratio(mouth):
    A = np.linalg.norm(mouth[1] - mouth[7])  # 61, 67
    B = np.linalg.norm(mouth[3] - mouth[5])  # 63, 65
    C = np.linalg.norm(mouth[0] - mouth[4])  # 60, 64
    mar = (A + B) / (2.0 * C)
    return mar


# 加载图片
liu=cv.imread('liu001.jpg')
guo=cv.imread('guo001.jpg')
chun=cv.imread('friends11.jpg')
peng=cv.imread('peng.jpg')

# bgr转rgb
liu_rgb=liu[:,:,::-1]
guo_rgb=guo[:,:,::-1]
chun_rgb=chun[:,:,::-1]
peng_rgb=peng[:,:,::-1]
# 检测人脸
liu_face=face_recognition.face_locations(liu_rgb)
guo_face=face_recognition.face_locations(guo_rgb)
chun_face=face_recognition.face_locations(chun_rgb)
peng_face=face_recognition.face_locations(peng_rgb)


# 人脸特征编码
liu_encodings=face_recognition.face_encodings(liu_rgb,liu_face)[0]
guo_encodings=face_recognition.face_encodings(guo_rgb,guo_face)[0]
chun_encodings=face_recognition.face_encodings(chun_rgb,chun_face)[0]
peng_encodings=face_recognition.face_encodings(peng_rgb,peng_face)[0]

# 人脸数据库
encodings=[liu_encodings,guo_encodings,chun_encodings,peng_encodings]
names=["liu de hua","guo fu cheng","liu chun long","peng yu yan"]

# 打开摄像头
capture=cv.VideoCapture(0)

EAR_THRESH = 0.15
EAR_CONSEC_FRAMES_MIN = 1
EAR_CONSEC_FRAMES_MAX = 5  # 当EAR小于阈值时，接连多少帧一定发生眨眼动作
# 嘴长宽比例值
MAR_THRESH = 0.2

# 初始化眨眼的连续帧数
blink_counter = 0
# 初始化眨眼次数总数
blink_total = 0


# 人脸检测器 null这里用face_rg
# 特征点检测器
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
# 获取左眼的特征点
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
# 获取右眼的特征点
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
# 获取嘴巴特征点
(mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["inner_mouth"]
if not capture.isOpened():
    raise IOError("CAMERA ERROR")

while True:
    ret,frame=capture.read()

    # bgr转rgb
    frame_rgb=frame[:,:,::-1]
    # 人脸检测
    frame_faces=face_recognition.face_locations(frame_rgb)

    # 人脸特征编码
    face_encodings=face_recognition.face_encodings(frame_rgb,frame_faces)

    # 与数据中的所有人脸进行比较
    for (top,right,bottom,left),face_encoding in zip(frame_faces,face_encodings):
        # 进行匹配
        matches=face_recognition.compare_faces(encodings,face_encoding)
        #计算距离
        distances=face_recognition.face_distance(encodings,face_encoding)
        min_distance_index=np.argmin(distances)

        name="unknown"
        if matches[min_distance_index]:
            name=names[min_distance_index]

        # 绘制人脸矩形框
        cv.rectangle(frame,(left,top),(right,bottom),color=(0,255,0),thickness=2)

        # 绘制名字
        cv.rectangle(frame,(left,bottom-30),(right,bottom),color=(255,0,0),thickness=1)

        cv.putText(frame,name,(left+10,bottom-10),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),thickness=1)


    ##张嘴检测
    if len(frame_faces)==1:

        gray=cv.cvtColor(frame_rgb,cv.COLOR_BGR2GRAY)
        shape = predictor(gray, frame_faces[0])  # 保存68个特征点坐标的<class 'dlib.dlib.full_object_detection'>对象
        shape = face_utils.shape_to_np(shape)  # 将shape转换为numpy数组，数组中每个元素为特征点坐标

        left_eye = shape[lStart:lEnd]  # 取出左眼对应的特征点
        right_eye = shape[rStart:rEnd]  # 取出右眼对应的特征点
        left_ear = eye_aspect_ratio(left_eye)  # 计算左眼EAR
        right_ear = eye_aspect_ratio(right_eye)  # 计算右眼EAR
        ear = (left_ear + right_ear) / 2.0  # 求左右眼EAR的均值

        mouth = shape[mStart:mEnd]  # 取出嘴巴对应的特征点
        mar = mouth_aspect_ratio(mouth)  # 求嘴巴mar的均值

        # EAR低于阈值，有可能发生眨眼，眨眼连续帧数加一次
        if ear < EAR_THRESH:
            blink_counter += 1

        # EAR高于阈值，判断前面连续闭眼帧数，如果在合理范围内，说明发生眨眼
        else:
            if EAR_CONSEC_FRAMES_MIN <= blink_counter <= EAR_CONSEC_FRAMES_MAX:
                blink_total += 1
            blink_counter = 0
        # 通过张、闭来判断一次张嘴动作
        if mar > MAR_THRESH:
            mouth_status_open = 1
        else:
            if mouth_status_open:
                mouth_total += 1
            mouth_status_open = 0
    elif len(frame_faces) == 0:
        print("No face!")
        break
    elif len(frame_faces) > 1:
        print("More than one face!")
        # 判断眨眼次数大于2、张嘴次数大于1则为活体,退出循环
    if blink_total >= 1 or mouth_total >= 1:
        cv.putText(frame,"Is real",(left,top+10),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),thickness=4)

    cv.imshow("recognition",frame)
    if cv.waitKey(1)==27:
        break
capture.release()
cv.destroyAllWindows()

# 惊醒