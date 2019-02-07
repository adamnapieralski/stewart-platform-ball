#include <opencv2/highgui.hpp>
#include <opencv2/core.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/objdetect.hpp>
#include <opencv2/opencv.hpp>
#include <string>
#include <iostream>

using namespace cv;
using namespace std;

int main() {
    Mat imgOrg = imread("/home/napiad/stewart-platform-ball/square_ball_2.jpg");
    Mat imgGray, imgBlur, imgThresh, imgCanny;
    vector<vector<Point> > contours;
    vector<Point> approx;
    vector<Vec4i> hierarchy;
    cvtColor(imgOrg, imgGray, CV_BGR2GRAY);
    namedWindow("w1", WINDOW_AUTOSIZE);

    //namedWindow("w2", WINDOW_AUTOSIZE);

    GaussianBlur(imgGray, imgBlur, Size(3, 3), 0);
    threshold(imgBlur, imgThresh, 50, 255, 0);
    Canny(imgThresh, imgCanny, 100, 200);


    findContours(imgCanny, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0));
    Mat drawing = Mat::zeros(imgCanny.size(), CV_8UC3);
    drawContours(drawing, contours, 0, Scalar(0, 255, 0), 1);

    double epsilon = arcLength(Mat(contours[0]), true) * 0.1;
    approxPolyDP(contours[0], approx, epsilon, true);
    line(imgOrg, approx.at(0), approx.at(1), Scalar(0, 255, 0), 1);
    line(imgOrg, approx.at(1), approx.at(2), Scalar(0, 255, 0), 1);
    line(imgOrg, approx.at(2), approx.at(3), Scalar(0, 255, 0), 1);
    line(imgOrg, approx.at(3), approx.at(0), Scalar(0, 255, 0), 1);


    Point p4(300, 300), p3(100, 300), p1(300, 100), p2(100, 100), c(200, 200);

    vector<Point2f> cornersIn, cornersOut;
    cornersIn.push_back(approx.at(0));
    cornersIn.push_back(approx.at(1));
    cornersIn.push_back(approx.at(2));
    cornersIn.push_back(approx.at(3));
    cornersOut.push_back(p1);
    cornersOut.push_back(p2);
    cornersOut.push_back(p3);
    cornersOut.push_back(p4);
    Mat M = getPerspectiveTransform(cornersIn, cornersOut);
    Mat dst;
    Size dsize(400, 400);
    warpPerspective(imgOrg, dst, M, dsize);

    cvtColor(dst, dst, CV_BGR2GRAY);
    vector<Vec3f> circles;
    HoughCircles(dst, circles, HOUGH_GRADIENT, 2, imgBlur.rows / 4);
    if(circles.size() > 0){
        cout << "Ball position x = " << circles[0][0]
             << ", y = " << circles[0][1]
             << ", radius = " << circles[0][2] << endl;
        circle(dst, Point((int)circles[0][0], (int)circles[0][1]), 3, Scalar(0, 255, 0), 0);
        circle(dst, Point((int)circles[0][0] + 1, (int)circles[0][1]), 3, Scalar(0, 255, 0), 0);
        circle(dst, Point((int)circles[0][0], (int)circles[0][1]), (int)circles[0][2], Scalar(0, 255, 0), 1);
        //putText(dst, to_string((int)circles[i][0]) + "," + to_string((int)circles[i][1]), Point((int)circles[i][0], (int)circles[i][1] + 30), 1, 1, Scalar(0, 255, 0), 2);
    }
    cout << "x error: " << 200 - circles[0][0] << endl << "x error: " << 200 - circles[0][1] << endl;
    imshow("w1", dst);

    waitKey(0);
    return 0;
}