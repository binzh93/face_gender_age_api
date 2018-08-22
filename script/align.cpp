#include <iostream>
#include <vector>
#include <cstring>
#include <string>
#include <sys/stat.h> 
#include <json/json.h>
#include <opencv2/opencv.hpp>
#include "dataInput.hpp"
#include "file_process.hpp"


using namespace std;
using namespace FaceInception;
// using std::cout;
// using std::endl;
using cv::Mat;


int main(int argc,char **argv) 
{   

    char *jsonDir = argv[1];
    string read_root_path = argv[2];
    string write_root_path = argv[3];

    vector<cv::Point2d> target_points = {{17.8449, 24.4716}, {43.7537, 24.3534}, {30.8296, 39.2371}, {19.6095, 45.2218}, {41.6762, 45.3069}};
    
    vector<char *>  poseJsonList = readFileList(jsonDir);  
 
    char *jsonPath;
    string pic_original_path;
    for(size_t i=0; i < poseJsonList.size(); i++){
        
        const char *json_filename = poseJsonList[i];

        auto points = getPoints(json_filename);
 
        vector<Mat> croppedImages;
        for(size_t j=0; j<points.size(); j++){
            
            vector<string> url_split_list;

            SplitString(points[j].second, url_split_list, "/");

            if(! dirExists(write_root_path)){
                const char * temp_dir = write_root_path.data();
                mkdir(temp_dir, 0777);
                
            }
            vector<string> json_basename;
            SplitString(url_split_list[url_split_list.size()-1], json_basename, ".");
      
            string pic_savepath = write_root_path + json_basename[0] + "_" + to_string(j) + "." + json_basename[1];

            pic_original_path = read_root_path + url_split_list[url_split_list.size()-1];
            Mat image = imread(pic_original_path);
            

            Mat trans_inv;

            Mat trans = findSimilarityTransform(points[j].first, target_points, trans_inv);
            Mat cropImage;
 
            warpAffine(image, cropImage, trans, Size(56, 56));
                    
            imwrite(pic_savepath, cropImage);        
        }

    }
    // auto points = getPoints(json_filename);

    cout << "align all images sucessful" << endl;

    return 0;
}



