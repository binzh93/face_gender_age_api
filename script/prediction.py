# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import os
import numpy as np
import cv2
import caffe
import argparse
from data_process import *


def predict_gender_and_age_by_jsonfile(model_def, model_weights, jsonfileDir, alignImgDir, originalImgDir, saveImgDir, landmark_flag=0):
    caffe.set_mode_gpu()  #设置为GPU运行    
    net = caffe.Net(model_def,      
                    model_weights,  
                    caffe.TEST)     

    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2,0,1))  
    transformer.set_raw_scale('data', 255)  
    transformer.set_mean('data', np.array([127.5, 127.5, 127.5])) 
    transformer.set_input_scale('data', 1/128.0) 
    transformer.set_channel_swap('data', (2, 1, 0))  

    poseList = get_pose_json_list(jsonfileDir)
    
    for posePath in poseList:
        pose_data = load_pose_data(posePath)
        
        face_nums = len(pose_data["result"]["landmarks"])
        if face_nums == 0:
            continue
        detJsonName = "detect" + "_" + os.path.basename(posePath).split("_")[1]
        detPath = os.path.join(jsonfileDir, detJsonName)
        det_data = load_det_data(detPath)

        genderList = []
        ageList = []

        for num in xrange(face_nums):
            imgNameSplitList = os.path.basename(pose_data["url"]).split(".")
            imgPath = os.path.join(alignImgDir, imgNameSplitList[0] + "_" + str(num) + "." + imgNameSplitList[1])
            image = caffe.io.load_image(imgPath) 
            transformed_image = transformer.preprocess('data', image)
            net.blobs['data'].data[...] = transformed_image
            net.blobs['data'].reshape(1, 3, 56, 56)
            output = net.forward()
            output_prob = net.blobs['prob'].data[0]
            output_age = net.blobs['reg_age'].data[0]

            pre_gender_num = output_prob.argmax()
            pre_age = int(output_age*70 + 0.5)

            genderList.append(pre_gender_num)
            ageList.append(pre_age)

        originalImgPath = os.path.join(originalImgDir, os.path.basename(pose_data["url"]))
        draw_result(originalImgPath, saveImgDir, det_data, pose_data, genderList, ageList, landmark_flag)


def predict_gender_and_age_by_single_aligned_img(model_def, model_weights, imgPath):
    caffe.set_mode_gpu()  #设置为GPU运行    
    net = caffe.Net(model_def,      
                    model_weights,  
                    caffe.TEST)     

    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2,0,1))  
    transformer.set_raw_scale('data', 255)  
    transformer.set_mean('data', np.array([127.5, 127.5, 127.5])) 
    transformer.set_input_scale('data', 1/128.0) 
    transformer.set_channel_swap('data', (2, 1, 0))  

    image = caffe.io.load_image(imgPath) 
    transformed_image = transformer.preprocess('data', image)
    net.blobs['data'].data[...] = transformed_image
    net.blobs['data'].reshape(1, 3, 56, 56)
    output = net.forward()
    output_prob = net.blobs['prob'].data[0]
    output_age = net.blobs['reg_age'].data[0]

    pre_gender_num = output_prob.argmax()
    if pre_gender_num == 0:
        pre_gender_str = 'Male'
    else:
        pre_gender_str = 'Female'
    pre_age = int(output_age*70 + 0.5)

    print("prediction result gender: {}({}), age: {}".format(pre_gender_num, pre_gender_str, pre_age))


def main():
    parse = argparse.ArgumentParser(description="Prediction gender and age")

    parse.add_argument('--model_def', required=True, type=str, help='deploy file path')
    parse.add_argument('--model_weights', required=True, type=str, help='caffemodel file path')
    parse.add_argument('--jsonfileDir', required=True, type=str, help='pose and det jsonfile dir')
    parse.add_argument('--alignImgDir', required=True, type=str, help='aligned image dir')
    parse.add_argument('--originalImgDir', required=True, type=str, help='original image dir')
    parse.add_argument('--saveImgDir', required=True, type=str, help='output save dir')
    parse.add_argument('--landmark_flag', default=0, type=int, help='if landmark_flag is 0 do not mark 68 points landmark else mark points')

    args = parse.parse_args()
    predict_gender_and_age_by_jsonfile(args.model_def, 
                                        args.model_weights, 
                                        args.jsonfileDir, 
                                        args.alignImgDir, 
                                        args.originalImgDir, 
                                        args.saveImgDir, 
                                        args.landmark_flag)

if __name__ == "__main__":
    main()
