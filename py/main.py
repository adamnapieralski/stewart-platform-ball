import cv2 as cv2
import urllib.request
import numpy as np

url = 'http://192.168.0.103:8080/shot.jpg'
cv2.namedWindow('cos', cv2.WINDOW_AUTOSIZE)

while True:
    imgResponse = urllib.request.urlopen(url)
    imgNp = np.array(bytearray(imgResponse.read()), dtype=np.uint8)
    frame = cv2.imdecode(imgNp, -1)

    cv2.imshow('cos', frame)

    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()


