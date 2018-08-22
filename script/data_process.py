#-*- coding: utf-8 -*-
import os
import json
import cv2



def load_all_face_pic_list(alignFaceDir):
    imgType = ["jpg", "jpeg", "png"]
    facePathList = []
    for picName in os.listdir(alignFaceDir):
        if picName in imgType:
            facePathList.append(os.path.join(alignFaceDir, picName))
    return facePathList


def load_pose_data(jsonfilePath):
    with open(jsonfilePath, "r") as fr:
        pose_data = json.load(fr)
    return pose_data    


def load_det_data(detfilePath):
    with open(detfilePath, "r") as fr:
        det_data = json.load(fr)
    return det_data 



def get_pose_json_list(josnPath):
    poseList = []
    detList = []
    for jsonfilename in os.listdir(josnPath):
        if jsonfilename.startswith("pose") and jsonfilename.endswith(".json"):
            poseList.append(os.path.join(josnPath, jsonfilename))
    return poseList

 



def draw_result(imgPath, saveDir, det_dict, pose_dict, genderList, ageList, landmark_flag=0):
    # if landmark_flag is 0 do not mark it on img else mark on img
    if not os.path.exists(saveDir):
        os.mkdir(saveDir)
    #frame = cv2.imread(imgPath)
    img = cv2.imread(imgPath)

    pose_result = pose_dict["result"]["landmarks"]  
    det_result = det_dict["result"]["detections"]

    nums = 0
    for det in det_result:
        if det["class"] == "face":
            topleft = (int(det["pts"][0][0]), int(det["pts"][0][1]))
            bottomright = (int(det["pts"][2][0]), int(det["pts"][2][1]))
            cv2.rectangle(img, topleft, bottomright, (255, 255, 0), 2)
            
            if genderList[nums] == 0:
                gender = "Male"
            else:
                gender = "Female"

            text = gender + "," + str(ageList[nums])
            # 输入参数为图像、文本、位置、字体、大小、颜色数组、粗细
            # cv2.putText(img, text, (x,y), Font, Size, (B,G,R), Thickness)
            cv2.putText(img, text, (topleft[0], topleft[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)    
            nums += 1

    if landmark_flag:
        for landmark in pose_result:
            topleftpoint = [99999, 99999]
            for point in landmark["landmark"]:
                point = (int(point[0]), int(point[1]))
                cv2.circle(img, point, 1, (0, 255, 255), 1)
                if point[0] < topleftpoint[0]:
                    topleftpoint[0] = point[0]
                if point[1] < topleftpoint[1]:
                    topleftpoint[1] = point[1]
 
    cv2.imwrite(os.path.join(saveDir, os.path.basename(imgPath)), img)
                
