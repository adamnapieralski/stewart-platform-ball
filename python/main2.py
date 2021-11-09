import urllib.request
import numpy as np
import cv2.aruco
import cv2 as cv2
from  PlatformVisualAnalysis import Board

def nothing(x):
    pass


cameraMatrix = np.matrix([[559.65898622, 0.,  324.64485928], [0., 567.44218001, 213.19173344], [0., 0., 1., ]])
cameraCoeffs = np.array([[ 9.14211287e-01, -1.80790008e+01, -4.73235254e-03, -1.47965156e-03, 1.25432032e+02]])
objp = np.zeros((4*4,3), np.float32)
objp[:,:2] = np.mgrid[0:4,0:4].T.reshape(-1,2)
print(objp)
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
objpoints.append(objp)

pt0 = np.array([0, 0]).reshape(2, 1)
pt1 = np.array([500, 0]).reshape(2, 1)
pt2 = np.array([0, 500]).reshape(2, 1)
pt3 = np.array([500, 500]).reshape(2, 1)

url = 'http://192.168.0.102:8080/shot.jpg'
cv2.namedWindow('win1', cv2.WINDOW_AUTOSIZE)
cv2.namedWindow('win2', cv2.WINDOW_AUTOSIZE)

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
board = cv2.aruco.CharucoBoard_create(5, 5, .025, .0125, dictionary)
board2 = cv2.aruco.CharucoBoard_create(8, 8, .025, .0175, dictionary)
img = board2.draw((200*5, 200*5))

platform = Board(dictionary, board)
cv2.imwrite('charuco8x8.png', img)

#pts1 = np.array([[0, 0, 0], [3, 0, 0], [0, 3, 0], [3, 3, 0]])
pts1 = np.array([[0, 0, 0], [3, 0, 0], [0, 3, 0], [3, 3, 0]])


while True:
    imgResponse = urllib.request.urlopen(url)
    imgNp = np.array(bytearray(imgResponse.read()), dtype=np.uint8)

    frame = cv2.imdecode(imgNp, -1)
    #frame = cv2.imread('charuco.png')
    #frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frameGray, dictionary)
    #detectedCorners, detectedIds, rejectedCorners, recoveredIdxs = cv2.aruco.refineDetectedMarkers(frameGray, board, corners, ids, rejectedImgPoints)
    #print(detectedCorners)
    #if len(detectedCorners) > 0:
        #retval, charucoCorners, charucoIds = cv2.aruco.interpolateCornersCharuco(detectedCorners, detectedIds, frameGray, board)
        #print(retval)
        ##cornersFrame = cv2.aruco.drawDetectedCornersCharuco(frame, charucoCorners, charucoIds)
        #retval, rvec, tvec = cv2.aruco.estimatePoseCharucoBoard(charucoCorners, charucoIds, board, cameraMatrix, cameraCoeffs)
        #print(charucoCorners[0])
        #if(retval):
            #cv2.aruco.drawAxis(frame, cameraMatrix, cameraCoeffs, rvec, tvec, 0.05)
            #imgpoints.append(charucoCorners)

            #R, _ = cv2.Rodrigues(rvec)
            #R = np.asarray(R)
            #R = np.delete(R, 2, 0)
            #R = np.delete(R, 2, 1)
            #original_point = np.matrix([[1], [1], [1]])#np.matrix([[1], [1], [1]])
            #rpt0 = R@pt0

            #rpt1 = R@pt1
            #rpt2 = R @ pt2
            #rpt3 = R @ pt3
            #pts = []
            #rpts = []
            #pts.append(pt0)
            #pts.append(pt1)
            #pts.append(pt2)
            #pts.append(pt3)
            #rpts.append(rpt0)
            #rpts.append(rpt1)
            #rpts.append(rpt2)
            #rpts.append(rpt3)
            #print(pts)
            #print(type(pts))
            #pts = np.asanyarray(pts, dtype=np.float32)
            #rpts = np.asanyarray(rpts, dtype=np.float32)

            #M = cv2.getPerspectiveTransform(pts, rpts)
            #srcPoints = np.row_stack((charucoCorners[0], charucoCorners[3], charucoCorners[12], charucoCorners[15]))
            #print(srcPoints)
            #print(np.reshape(charucoIds, (len(charucoIds))))
            #frameTrans = cv2.warpPerspective(frame, M, (500, 500))
            #cv2.imshow('win1', frameTrans)

        #frame = platform.transformBoard(frame, charucoCorners, charucoIds)
    retval, charucoCorners, charucoIds = platform.findCharucoCorners(frame)
    frameTrans = platform.transformBoard(frame, charucoCorners, charucoIds)
    cv2.imshow('win1', frame)
    cv2.imshow('win2', frameTrans)

    if cv2.waitKey(1) == 27:
        #ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, frameGray.shape[::-1], None, None)
        #print(mtx)
        #print(dist)
        break
cv2.destroyAllWindows()

