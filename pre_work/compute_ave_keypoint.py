# -*- coding: utf-8 -*-
import json


def compute_ave_keypoint(json_filename):

    with open(json_filename) as f:
        ave_nums = 0
        for line in f:
            line = line.strip()
            json_dict = json.loads(line)

            if len(json_dict['result']['landmarks']) == 0:
                # can't detect the face
                #print json_dict['result']['landmarks']
                pass
            else:
                #print len(json_dict['result']['landmarks'][0]['landmark'])
                keypoint_list = json_dict['result']['landmarks'][0]['landmark']
                #pic_name = json_dict["url"].split("/")[-1]#"/Users/bin/Desktop/base_rst/7939.jpg"
                eye_left1 = keypoint_list[36]
                eye_left2 = keypoint_list[39]
                eye_right1 = keypoint_list[42]
                eye_right2 = keypoint_list[45]
                nose = keypoint_list[33]
                mouse_left = keypoint_list[48]
                mouse_right = keypoint_list[54]

                if ave_nums == 0:
                    eye_left1_ave = eye_left1
                    eye_left2_ave = eye_left2
                    eye_right1_ave = eye_right1
                    eye_right2_ave = eye_right2
                    nose_ave = nose
                    mouse_left_ave = mouse_left
                    mouse_right_ave = mouse_right
                    ave_nums += 1
                else:
                    eye_left1_ave = [eye_left1_ave[0]+eye_left1[0], eye_left1_ave[1]+eye_left1[1]]
                    eye_left2_ave = [eye_left2_ave[0]+eye_left2[0], eye_left2_ave[1]+eye_left2[1]]
                    eye_right1_ave = [eye_right1_ave[0]+eye_right1[0], eye_right1_ave[1]+eye_right1[1]]
                    eye_right2_ave = [eye_right2_ave[0]+eye_right2[0], eye_right2_ave[1]+eye_right2[1]]
                    nose_ave = [nose_ave[0]+nose[0], nose_ave[1]+nose[1]]
                    mouse_left_ave = [mouse_left_ave[0]+mouse_left[0], mouse_left_ave[1]+mouse_left[1]]
                    mouse_right_ave = [mouse_right_ave[0]+mouse_right[0], mouse_right_ave[1]+mouse_right[1]]
                    ave_nums += 1

                #print len(keypoint_list)
    eye_left1_ave = [eye_left1_ave[0]*1.0/ave_nums, eye_left1_ave[1]*1.0/ave_nums]
    eye_left2_ave = [eye_left2_ave[0]*1.0/ave_nums, eye_left2_ave[1]*1.0/ave_nums]
    eye_right1_ave = [eye_right1_ave[0]*1.0/ave_nums, eye_right1_ave[1]*1.0/ave_nums]
    eye_right2_ave = [eye_right2_ave[0]*1.0/ave_nums, eye_right2_ave[1]*1.0/ave_nums]
    nose_ave = [nose_ave[0]*1.0/ave_nums, nose_ave[1]*1.0/ave_nums]
    mouse_left_ave = [mouse_left_ave[0]*1.0/ave_nums, mouse_left_ave[1]*1.0/ave_nums]
    mouse_right_ave = [mouse_right_ave[0]*1.0/ave_nums, mouse_right_ave[1]*1.0/ave_nums]

    print "eye_left1_average:   ", eye_left1_ave
    print "eye_left2_average:   ", eye_left2_ave
    print "eye_right1_average:  ", eye_right1_ave
    print "eye_right2_average:  ", eye_right2_ave
    print "nose_average:        ", nose_ave
    print "mouse_left_average:  ", mouse_left_ave
    print "mouse_right_average: ", mouse_right_ave


if __name__ == "__main__":
    json_filename = "/Users/bin/Desktop/base_rst/pose_result.json"
    compute_ave_keypoint(json_filename)








