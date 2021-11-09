import cv2.aruco
import numpy as np


class Board:

    tileDstWidth = 70
    transMargin = 50

    def __init__(self, sideTiles):
        self.dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        self.board = cv2.aruco.CharucoBoard_create(sideTiles, sideTiles, .025, .0125, self.dictionary)
        self.sideTiles = sideTiles
        self.sideCorners = sideTiles - 1

        #create an array of points destination after transformation
        self.dstCorners = []
        for i in range(sideTiles - 1, 0, -1):
            for j in range(1, sideTiles):
                self.dstCorners = np.append(self.dstCorners, [self.transMargin + j * self.tileDstWidth, self.transMargin + i * self.tileDstWidth], axis=0)
        self.dstCorners = np.reshape(self.dstCorners, (self.sideCorners * self.sideCorners, 2))
        self.dstCorners = np.asarray(self.dstCorners, dtype=np.float32)

        #create an array of charuco Corner ids for relative transformation squares
        self.squaresIds = []
        tmpCornersIds = []
        for i in range(self.sideCorners - 1, -1, -1):
            tmpCornersIds = np.append(tmpCornersIds, np.linspace(i * self.sideCorners, (i + 1) * self.sideCorners, self.sideCorners, endpoint=False)).reshape((self.sideCorners - i, self.sideCorners))


        if self.sideTiles % 2 == 1:
            self.squaresNum = int((self.sideTiles - 1) / 2)
        else:
            self.squaresNum = int((self.sideTiles - 2) / 2)

        for i in range(int(self.squaresNum)):
           self.squaresIds = np.append(self.squaresIds, [tmpCornersIds[self.sideCorners - 1 - i][i],
                                                         tmpCornersIds[self.sideCorners - 1 - i][self.sideCorners - 1 - i],
                                                         tmpCornersIds[i][ i],
                                                         tmpCornersIds[i][self.sideCorners - 1 - i]]).astype(int).reshape((i + 1, 4))

        self.transFrameWindow = int(2 * self.transMargin + self.sideTiles * self.tileDstWidth)


    def findCharucoCorners(self, frame):

        frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frameGray, self.dictionary)
        detectedCorners, detectedIds, rejectedCorners, recoveredIdxs = cv2.aruco.refineDetectedMarkers(frameGray, self.board,
                                                                                                       corners, ids,
                                                                                                       rejectedImgPoints)
        if len(detectedCorners) > 0:
            retval, charucoCorners, charucoIds = cv2.aruco.interpolateCornersCharuco(detectedCorners, detectedIds, frameGray, self.board)
        else:
            retval = 0
            charucoCorners = []
            charucoIds = []
        return retval, charucoCorners, charucoIds


    def isSquareVisible(self, squareIds, charucoIds):
        for i in range(len(squareIds)):
            if squareIds[i] not in charucoIds:
                return False
        return True


    def transformBoard(self, frame, charucoCorners, charucoIds):

        if (charucoIds is not None):
            charucoIds = np.reshape(charucoIds, len(charucoIds))
            for i in range(self.squaresNum):
                if self.isSquareVisible(self.squaresIds[i], charucoIds):
                    # frame = cv2.aruco.drawDetectedCornersCharuco(frame, charucoCorners, charucoIds)
                    pointsIndxs = np.searchsorted((charucoIds), self.squaresIds[i])

                    srcPoints = np.row_stack((charucoCorners[pointsIndxs[0]], charucoCorners[pointsIndxs[1]],
                                              charucoCorners[pointsIndxs[2]], charucoCorners[pointsIndxs[3]]))
                    dstPoints = np.row_stack(
                        (self.dstCorners[self.squaresIds[i][0]], self.dstCorners[self.squaresIds[i][1]],
                         self.dstCorners[self.squaresIds[i][2]], self.dstCorners[self.squaresIds[i][3]]))
                    M = cv2.getPerspectiveTransform(srcPoints, dstPoints)
                    transFrame = cv2.warpPerspective(frame, M, (self.transFrameWindow, self.transFrameWindow))

                    cv2.circle(transFrame,
                               (self.dstCorners[self.squaresIds[i][0]][0], self.dstCorners[self.squaresIds[i][0]][1]),
                               4, (0, 255, 0), 4)
                    cv2.circle(transFrame,
                               (self.dstCorners[self.squaresIds[i][1]][0], self.dstCorners[self.squaresIds[i][1]][1]),
                               3, (0, 0, 255), 2)
                    cv2.circle(transFrame,
                               (self.dstCorners[self.squaresIds[i][2]][0], self.dstCorners[self.squaresIds[i][2]][1]),
                               3, (0, 0, 255), 2)
                    cv2.circle(transFrame,
                               (self.dstCorners[self.squaresIds[i][3]][0], self.dstCorners[self.squaresIds[i][3]][1]),
                               3, (0, 0, 255), 2)
                    cv2.circle(frame, (srcPoints[0][0], srcPoints[0][1]), 4, (0, 255, 0), 4)
                    cv2.circle(frame, (srcPoints[1][0], srcPoints[1][1]), 3, (0, 0, 255), 2)
                    cv2.circle(frame, (srcPoints[2][0], srcPoints[2][1]), 3, (0, 0, 255), 2)
                    cv2.circle(frame, (srcPoints[3][0], srcPoints[3][1]), 3, (0, 0, 255), 2)




                    return frame, transFrame

        frame_height = np.size(frame, 0)
        frame_width = np.size(frame, 1)
        cropFrame = frame[int((frame_height - self.transFrameWindow) / 2):int((frame_height + self.transFrameWindow) / 2), int((frame_width - self.transFrameWindow) / 2):int((frame_width + self.transFrameWindow) / 2)]
        return frame, cropFrame


    def ballPosition(self, frameTrans, low, high, can):
        frameTBlur = cv2.GaussianBlur(frameTrans, (7, 7), 0)
        frameTHSV = cv2.cvtColor(frameTBlur, cv2.COLOR_BGR2HSV)
        light_orange = low #(1, 150, 150)
        dark_orange = high #(20, 255, 255)
        frameMask = cv2.inRange(frameTHSV, light_orange, dark_orange)
        frameMask = cv2.erode(frameMask, None, iterations=2)
        frameMask = cv2.dilate(frameMask, None, iterations=2)

        x = -1
        y = -1

        circles = cv2.HoughCircles(frameMask, cv2.HOUGH_GRADIENT, can / 100, 3000, minRadius=15, maxRadius=70)
        cv2.circle(frameTrans, (int(self.transFrameWindow / 2), int(self.transFrameWindow / 2)), 3, (0, 0, 255), 3)
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            x = circles[0, 0]
            y = circles[0, 1]
            r = circles[0, 2]
            text = '{}, {}'.format(x, y)
            cv2.circle(frameTrans, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(frameTrans, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

            cv2.putText(frameTrans, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), thickness=2)

        return frameTrans, x, y