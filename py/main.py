import cv2 as cv2
import urllib.request
import numpy as np
import cv2.aruco
url = 'http://192.168.0.102:8080/shot.jpg'
cv2.namedWindow('cos', cv2.WINDOW_AUTOSIZE)

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
board = cv2.aruco.CharucoBoard_create(5, 5, .025, .0125, dictionary)

objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
print(objp)

while True:
    imgResponse = urllib.request.urlopen(url)
    imgNp = np.array(bytearray(imgResponse.read()), dtype=np.uint8)

    frame = cv2.imdecode(imgNp, -1)
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frameGray, dictionary)
    cv2.imshow('cos', frame)

    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()


