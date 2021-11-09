import urllib.request
import numpy as np
import cv2 as cv2
from PlatformVisualAnalysis import Board
from PlatformPoseControl import Platform

def nothing(x):
    pass

cameraMatrix = np.matrix([[559.65898622, 0.,  324.64485928], [0., 567.44218001, 213.19173344], [0., 0., 1., ]])
cameraCoeffs = np.array([[ 9.14211287e-01, -1.80790008e+01, -4.73235254e-03, -1.47965156e-03, 1.25432032e+02]])

url = 'http://192.168.0.102:8080/shot.jpg' # 'http://192.168.43.1:8080/shot.jpg' #'http://192.168.0.102:8080/shot.jpg'
cv2.namedWindow('win1', cv2.WINDOW_AUTOSIZE)
cv2.namedWindow('win2', cv2.WINDOW_AUTOSIZE)


cv2.createTrackbar('low H', 'win2', 1, 255, nothing)
cv2.createTrackbar('low S', 'win2', 86, 255, nothing)
cv2.createTrackbar('low V', 'win2', 115, 255, nothing)
cv2.createTrackbar('high H', 'win2', 35, 255, nothing)
cv2.createTrackbar('high S', 'win2', 255, 255, nothing)
cv2.createTrackbar('high V', 'win2', 255, 255, nothing)
cv2.createTrackbar('accum res / 100', 'win2', 430, 1000, nothing)


sideTiles = 5

board = Board(sideTiles)

platform = Platform()
platform.calculatePose(0.1, 0, 6)
#board2 = cv2.aruco.CharucoBoard_create(8, 8, .025, .0175, dictionary)
#img = board2.draw((200*5, 200*5))


#cv2.imwrite('charuco8x8.png', img)
pts = np.array([[0, 0], [0, 50], [50, 0], [50, 50]], dtype=np.float32)

print(cv2.getPerspectiveTransform(pts, pts))
while True:
    imgResponse = urllib.request.urlopen(url)
    imgNp = np.array(bytearray(imgResponse.read()), dtype=np.uint8)

    frame = cv2.imdecode(imgNp, -1)

    #frame = cv2.imread('im1.png')
    retval, charucoCorners, charucoIds = board.findCharucoCorners(frame)
    frame, frameTrans = board.transformBoard(frame, charucoCorners, charucoIds)

    low = (cv2.getTrackbarPos('low H', 'win2'), cv2.getTrackbarPos('low S', 'win2'), cv2.getTrackbarPos('low V', 'win2'))
    high = (cv2.getTrackbarPos('high H', 'win2'), cv2.getTrackbarPos('high S', 'win2'), cv2.getTrackbarPos('high V', 'win2'))
    acc_res = cv2.getTrackbarPos('accum res / 100', 'win2')
    frameTrans, ballX, ballY = board.ballPosition(frameTrans, low, high, acc_res)
    print(ballX, ballY)
    cv2.imshow('win1', frame)
    cv2.imshow('win2', frameTrans)

    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()

