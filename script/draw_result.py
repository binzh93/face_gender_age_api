#-*- coding: utf-8 -*-
import os
import cv2



imgPath = '../examples/original_img/timg.jpeg'
img = cv2.imread(imgPath)
# 画矩形框
cv2.rectangle(img, (562, 534), (562, 656), (0,255,0), 4)
# 标注文本
font = cv2.FONT_HERSHEY_SUPLEX
text = '001'
cv2.putText(img, text, (562, 534), font, 2, (0,0,255), 1)
cv2.imwrite(os.path.basename(imgPath), img)


savePath
def mark_frame_from_file(imgPath, rstdir, det_rst, pose_rst):
    if not os.path.exists(savePath):
        os.mkdir(savePath)
    frame = cv2.imread(imgPath)
    for detection in det_rst["detections"]:
        if detection["class"] == "face":
            topleft = (int(detection["pts"][0][0]), int(detection["pts"][0][1]))
            bottomright = (int(detection["pts"][2][0]), int(detection["pts"][2][1]))
            cv2.rectangle(frame, topleft, bottomright, (255, 255, 0), 2)
    for landmark in pose_rst["landmarks"]:
        topleftpoint = [99999, 99999]
        for point in landmark["landmark"]:
            point = (int(point[0]), int(point[1]))
            cv2.circle(frame, point, 1, (0, 255, 255), 1)
            if point[0] < topleftpoint[0]:
                topleftpoint[0] = point[0]
            if point[1] < topleftpoint[1]:
                topleftpoint[1] = point[1]
        text = str(int(landmark["pos"][0])) + ", " + str(int(landmark["pos"][1])) + ", " + str(int(landmark["pos"][2]))
        cv2.putText(frame, text, (topleftpoint[0], topleftpoint[1]), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

    #cv2.imwrite(os.path.join(savePath, os.path.basename(srcfilepath)), frame)
    print("marked->  " + srcfilepath)









