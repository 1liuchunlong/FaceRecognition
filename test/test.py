import cv2
import dlib
import numpy as np

# 初始化人脸检测器和关键点检测器
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# 边缘检测参数
edge_threshold1 = 50
edge_threshold2 = 200

# 检测人脸并提取边缘图像
def detect_face(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    for face in faces:
        landmarks = predictor(gray, face)
        # 计算人脸旋转角度，使人脸水平
        angle = np.arctan2(landmarks.part(27).y - landmarks.part(30).y,
                           landmarks.part(27).x - landmarks.part(30).x) * 180 / np.pi
        rotated_image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE if angle > 0 else cv2.ROTATE_90_COUNTERCLOCKWISE)
        # 提取人脸边缘图像
        edges = cv2.Canny(rotated_image, edge_threshold1, edge_threshold2)
        return edges
    return None

# 统计边缘图像中不同方向的像素数量，并计算出垂直和水平方向的像素比例
def count_edges(edges):
    height, width = edges.shape[:2]
    # 垂直和水平方向的像素数量
    vertical_pixels = np.sum(edges, axis=1)
    horizontal_pixels = np.sum(edges, axis=0)
    # 垂直和水平方向的像素比例
    vertical_ratio = np.max(vertical_pixels) / height
    horizontal_ratio = np.max(horizontal_pixels) / width
    return vertical_ratio, horizontal_ratio

# 测试代码 它从摄像头中读取实时视频流，对每一帧图像进行活体检测并输出检测结果。当检测到假脸时，在图像上显示红色的"Fake Face"标签；当检测到真脸#时，在图像上显示绿色的"Real Face"标签。
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if ret:
        edges = detect_face(frame)
        if edges is not None:
            vertical_ratio, horizontal_ratio = count_edges(edges)
            if abs(vertical_ratio - horizontal_ratio) > 0.1:
                cv2.putText(frame, "Fake Face", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                cv2.putText(frame, "Real Face", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
