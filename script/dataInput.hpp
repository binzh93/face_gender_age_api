#include <opencv2/opencv.hpp>
#include <iostream>
#include <vector>
#include <json/json.h>
#include <cstring>
#include <string>
#include <fstream>
#include <utility>
#include <unistd.h>


using namespace std;
using namespace cv;

namespace FaceInception
{
    // get five points landmark
    vector<pair<vector<cv::Point2d>, string> > getPoints(const char* json_filename)  //, string output_path
    {

        vector<pair<vector<cv::Point2d>, string> > points;
        
        Json::Value jsonobj;
        Json::Reader reader;
        std::ifstream det_result(json_filename, std::ifstream::binary);
        string curline;

        while (getline(det_result, curline))
        {
            reader.parse(curline, jsonobj, false);
            for (int face_num = 0; face_num < jsonobj["result"]["landmarks"].size(); face_num++)
                {
                    double eye_left_1_x = jsonobj["result"]["landmarks"][face_num]["landmark"][37][0u].asDouble();
                    double eye_left_1_y = jsonobj["result"]["landmarks"][face_num]["landmark"][37][1].asDouble();
                    double eye_left_2_x = jsonobj["result"]["landmarks"][face_num]["landmark"][38][0u].asDouble();
                    double eye_left_2_y = jsonobj["result"]["landmarks"][face_num]["landmark"][38][1].asDouble();
                    double eye_left_3_x = jsonobj["result"]["landmarks"][face_num]["landmark"][40][0u].asDouble();
                    double eye_left_3_y = jsonobj["result"]["landmarks"][face_num]["landmark"][40][1].asDouble();
                    double eye_left_4_x = jsonobj["result"]["landmarks"][face_num]["landmark"][41][0u].asDouble();
                    double eye_left_4_y = jsonobj["result"]["landmarks"][face_num]["landmark"][41][1].asDouble();
                    // right eye
                    double eye_right_1_x = jsonobj["result"]["landmarks"][face_num]["landmark"][43][0u].asDouble();
                    double eye_right_1_y = jsonobj["result"]["landmarks"][face_num]["landmark"][43][1].asDouble();
                    double eye_right_2_x = jsonobj["result"]["landmarks"][face_num]["landmark"][44][0u].asDouble();
                    double eye_right_2_y = jsonobj["result"]["landmarks"][face_num]["landmark"][44][1].asDouble();
                    double eye_right_3_x = jsonobj["result"]["landmarks"][face_num]["landmark"][46][0u].asDouble();
                    double eye_right_3_y = jsonobj["result"]["landmarks"][face_num]["landmark"][46][1].asDouble();
                    double eye_right_4_x = jsonobj["result"]["landmarks"][face_num]["landmark"][47][0u].asDouble();
                    double eye_right_4_y = jsonobj["result"]["landmarks"][face_num]["landmark"][47][1].asDouble();
                    // nose
                    double nose_x = jsonobj["result"]["landmarks"][face_num]["landmark"][33][0u].asDouble();
                    double nose_y = jsonobj["result"]["landmarks"][face_num]["landmark"][33][1].asDouble();
                    // mouse
                    double mouse_left_1_x = jsonobj["result"]["landmarks"][face_num]["landmark"][48][0u].asDouble();
                    double mouse_left_1_y = jsonobj["result"]["landmarks"][face_num]["landmark"][48][1].asDouble();
                    double mouse_right_2_x = jsonobj["result"]["landmarks"][face_num]["landmark"][54][0u].asDouble();
                    double mouse_right_2_y = jsonobj["result"]["landmarks"][face_num]["landmark"][54][1].asDouble();

                    vector<cv::Point2d> point_list;

                    point_list.push_back(cv::Point2d((eye_left_1_x + eye_left_2_x + eye_left_3_x + eye_left_4_x) / 4.0, (eye_left_1_y + eye_left_2_y + eye_left_3_y + eye_left_4_y) / 4.0));
                    point_list.push_back(cv::Point2d((eye_right_1_x + eye_right_2_x + eye_right_3_x + eye_right_4_x) / 4.0, (eye_right_1_y + eye_right_2_y + eye_right_3_y + eye_right_4_y) / 4.0));
                    point_list.push_back(cv::Point2d(nose_x, nose_y));
                    point_list.push_back(cv::Point2d(mouse_left_1_x, mouse_left_1_y));
                    point_list.push_back(cv::Point2d(mouse_right_2_x, mouse_right_2_y));
                    
                    //string filepath = "" + ;
                    string filepath = jsonobj["url"].asString();
                    points.push_back({point_list, filepath});
                }
        }
        return points;
    }

    /*
        拆分字符串
    */
    void SplitString(const string& s, vector<string>& v, const string& c)
    {
        string::size_type pos1, pos2;
        pos2 = s.find(c);
        pos1 = 0;
        while(string::npos != pos2)
        {
            v.push_back(s.substr(pos1, pos2-pos1));
            
            pos1 = pos2 + c.size();
            pos2 = s.find(c, pos1);
        }
        if(pos1 != s.length())
            v.push_back(s.substr(pos1));
    }

    /*
    判断文件夹是否存在
    */

    bool dirExists(const std::string& dirName_in)
    {
        int ftyp = access(dirName_in.c_str(), 0);
    
        if (0 == ftyp)
            return true;   // this is a directory!
        else 
            return false;    // this is not a directory!
    }

    cv::Mat findNonReflectiveTransform(std::vector<cv::Point2d> source_points, std::vector<cv::Point2d> target_points, Mat &Tinv)
    {
        assert(source_points.size() == target_points.size());
        assert(source_points.size() >= 2);
        Mat U = Mat::zeros(target_points.size() * 2, 1, CV_64F);
        Mat X = Mat::zeros(source_points.size() * 2, 4, CV_64F);
        for (int i = 0; i < target_points.size(); i++)
        {
            U.at<double>(i * 2, 0) = source_points[i].x;
            U.at<double>(i * 2 + 1, 0) = source_points[i].y;
            X.at<double>(i * 2, 0) = target_points[i].x;
            X.at<double>(i * 2, 1) = target_points[i].y;
            X.at<double>(i * 2, 2) = 1;
            X.at<double>(i * 2, 3) = 0;
            X.at<double>(i * 2 + 1, 0) = target_points[i].y;
            X.at<double>(i * 2 + 1, 1) = -target_points[i].x;
            X.at<double>(i * 2 + 1, 2) = 0;
            X.at<double>(i * 2 + 1, 3) = 1;
        }
        Mat r = X.inv(DECOMP_SVD) * U;
        Tinv = (Mat_<double>(3, 3) << r.at<double>(0), -r.at<double>(1), 0,
                r.at<double>(1), r.at<double>(0), 0,
                r.at<double>(2), r.at<double>(3), 1);
        Mat T = Tinv.inv(DECOMP_SVD);
        Tinv = Tinv(Rect(0, 0, 2, 3)).t();
        return T(Rect(0, 0, 2, 3)).t();
    }

    cv::Mat findSimilarityTransform(std::vector<cv::Point2d> source_points, std::vector<cv::Point2d> target_points, Mat &Tinv)
    {
        Mat Tinv1, Tinv2;
        Mat trans1 = findNonReflectiveTransform(source_points, target_points, Tinv1);
        std::vector<Point2d> source_point_reflect;
        for (auto sp : source_points)
        {
            source_point_reflect.push_back(Point2d(-sp.x, sp.y));
        }
        Mat trans2 = findNonReflectiveTransform(source_point_reflect, target_points, Tinv2);
        trans2.colRange(0, 1) *= -1;
        std::vector<Point2d> trans_points1, trans_points2;
        transform(source_points, trans_points1, trans1);
        transform(source_points, trans_points2, trans2);
        double norm1 = norm(Mat(trans_points1), Mat(target_points), NORM_L2);
        double norm2 = norm(Mat(trans_points2), Mat(target_points), NORM_L2);
        Tinv = norm1 < norm2 ? Tinv1 : Tinv2;
        return norm1 < norm2 ? trans1 : trans2;
    }
} // namespace FaceInception

