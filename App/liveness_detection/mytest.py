import cv2 as cv

# from App.liveness_detection.test import test import
from App.liveness_detection.test import liveness_detection
capture = cv.VideoCapture(0)
if not capture.isOpened():
    raise IOError("CAMERA ERROR")

model_dir="./resources/anti_spoof_models"
while True:
    ret, frame = capture.read()

    show_image=liveness_detection(frame, model_dir, 0)
    cv.imshow("chunchun",show_image)

    if cv.waitKey(1)== 27:
        break

capture.release()
cv.destroyAllWindows()

