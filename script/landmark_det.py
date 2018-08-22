from threading import Thread
from multiprocessing import Queue
import os
import cv2
import time
import qiniu
from ava_auth import AuthFactory
import requests
import json
from argparse import ArgumentParser


stop_signal = False
frame_url_queue = Queue()

default_config_file = 'config_file/ava_auth_config.json'

############functions about upload frames to bucket and add url to frame_url_queue#######
def load_config_file(config_json):
    if not os.path.exists(default_config_file):
        print("===> Error: Cannot find config_file: " + default_config_file)
        return
    with open(config_json, "r") as fr:
        configs = json.load(fr)
    return configs


def get_ava_auth(configs):
    ava_auth_conf = configs["ava_auth_conf"]
    upload_access_key = ava_auth_conf["your_access_key"]
    upload_secret_key = ava_auth_conf["your_secret_key"]
    process_access_key = ava_auth_conf["atlab_access_key"]
    process_secret_key = ava_auth_conf["atlab_secret_key"]

    upload_auth = qiniu.Auth(upload_access_key, upload_secret_key)
    process_auth = AuthFactory(process_access_key, process_secret_key).get_qiniu_auth()

    return upload_auth, process_auth


def upload_single_frame(filepath, configs, upload_auth):
    bucket_name = configs["your_bucket_name"]
    filename = os.path.basename(filepath)
    upload_token = upload_auth.upload_token(bucket_name, filename, 3600)
    ret, _ = qiniu.put_file(upload_token, filename, filepath)
    return ret["hash"] == qiniu.etag(filepath)
    

def upload_frame(filepath, configs, upload_auth, reupload=3):
    bucket_url = configs["your_bucket_url"]
    global frame_url_queue
    upload_success = False
    while not upload_success and reupload:
        upload_success = upload_single_frame(filepath, configs, upload_auth)
        reupload -= 1
    if upload_success:
        frame_url = bucket_url + os.path.basename(filepath)
        frame_url_queue.put(frame_url)
        print("upload->  " + frame_url + "  sucess!")
    else:
        print("upload->  " + frame_url + "  failed!")
    return upload_success


def upload_frames(frames_dir, configs, upload_auth):
    
    global stop_signal
    picNameList = [".jpg", ".jpeg", "png"]
    files = [ f for f in os.listdir(frames_dir) if os.path.isfile(os.path.join(frames_dir, f))]
    for f in files:
        if os.path.splitext(f)[1] in picNameList:
            upload_frame(os.path.join(frames_dir, f), configs, upload_auth)
    stop_signal = True


###############functions about process frames
def detect_frame(fileurl, configs, process_auth):
    detect_url = configs["detect_url"]
    header = {"Content-Type":"application/json"}
    data = {"data":{"uri":fileurl}}
    r = requests.post(detect_url, None, data, headers=header, auth=process_auth)
    contentObj = json.loads(r.content)
    # print("detected->  " + fileurl)
    return contentObj["result"]

    
def pose_frame(fileurl, det_rst, configs, process_auth):
    pose_url = configs["pose_url"]
    header = {"Content-Type":"application/json"}
    if len(det_rst["detections"]) != 0:
        data = {"data":{"uri":fileurl, "attribute":det_rst}}
        r = requests.post(pose_url, None, data, headers=header, auth=process_auth)
        contentObj = json.loads(r.content)
        if "error" in contentObj.keys():
            return {"landmarks":[]}
        else:
            return contentObj["result"]
    else:
        return {"landmarks":[]}


def save_result(rstdir, fileurl, det_rst, pose_rst):
    if not os.path.exists(rstdir):
        os.mkdir(rstdir)
    with open(os.path.join(rstdir, "detect_" + os.path.basename(fileurl).split(".")[0] + ".json"), "a") as f:
        result = {"url":fileurl, "result":det_rst}
        f.write(json.dumps(result) + "\n")
    with open(os.path.join(rstdir, "pose_" + os.path.basename(fileurl).split(".")[0] + ".json"), "a") as f:
        result = {"url":fileurl, "result":pose_rst}
        f.write(json.dumps(result) + "\n")


def process_frames(srcdir, rstdir, configs, process_auth):
    while not stop_signal or not frame_url_queue.empty():
        if not frame_url_queue.empty():
            frameurl = frame_url_queue.get()
            det_rst = detect_frame(frameurl, configs, process_auth)
            pose_rst = pose_frame(frameurl, det_rst, configs, process_auth)
            save_result(rstdir, frameurl, det_rst, pose_rst)


def landmark_detection():
    ap = ArgumentParser('draw boxs and points')
    ap.add_argument('--src', required=True, type=str, help='dir to get image data')
    ap.add_argument('--rst', required=True, type=str, help="dir to save results, it need to be empty!")
    args = ap.parse_args()
    src = args.src
    rst = args.rst

    if not os.path.exists(src):
        print("source dir is not exists!")
        os._exit(0)

    if os.path.exists(rst):
        if len(os.listdir(rst)) != 0:
            print("dir already exists and not empty!")
            os._exit(0)
    else:
        os.mkdir(rst)

    configs = load_config_file(default_config_file) 
    upload_auth, process_auth = get_ava_auth(configs)  # To grant authorization

    upload_frame_thread = Thread(target = upload_frames, args=(src, configs, upload_auth))
    process_frame_thread = Thread(target = process_frames, args=(src, rst, configs, process_auth))
    
    upload_frame_thread.start()
    process_frame_thread.start()

    while upload_frame_thread.is_alive() or process_frame_thread.is_alive():
        time.sleep(1)
    print("landmark detection is done!")


if __name__ == "__main__":
    landmark_detection()
    
