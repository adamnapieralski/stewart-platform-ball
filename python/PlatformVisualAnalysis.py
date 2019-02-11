import urllib.request
import numpy as np
import cv2


def nothing(x):
    pass


url = 'http://192.168.0.102:8080/shot.jpg'
cv2.namedWindow('win1', cv2.WINDOW_AUTOSIZE)
cv2.namedWindow('win2', cv2.WINDOW_AUTOSIZE)
cv2.createTrackbar('Thresh_type', 'win1', 0, 4, nothing)
cv2.createTrackbar('Thresh_lower', 'win1', 90, 255, nothing)
cv2.createTrackbar('Thresh_upper', 'win1', 255, 255, nothing)

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
board = cv2.aruco.CharucoBoard_create(5, 5, .025, .0125, dictionary)
img = board.draw((200*5, 200*5))

cv2.imwrite('charuco.png', img)

while True:
    imgResponse = urllib.request.urlopen(url)
    imgNp = np.array(bytearray(imgResponse.read()), dtype=np.uint8)
    frame = cv2.imdecode(imgNp, -1)
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frameBlur = cv2.GaussianBlur(frameGray, (3, 3), 0)
    ret, frameThresh = cv2.threshold(frameBlur, cv2.getTrackbarPos('Thresh_lower', 'win1'), cv2.getTrackbarPos('Thresh_upper', 'win1'), cv2.getTrackbarPos('Thresh_type', 'win1'))
    frameCanny = cv2.Canny(frameThresh, 100, 200)

    contours, hierarchy = cv2.findContours(frameThresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 1)
    cv2.imshow('win1', frameThresh)
    cv2.imshow('win2', frame)

    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()