from ctypes import *
import math
import random
import os
import cv2
import numpy as np
import time
import darknet
from numba import jit

@jit
def iou(bb_test, bb_gt):
  # current frame(detections) , past frame (trackers)
  # x increases as we go to the right and y increases as we go down
  # iou = intersection/(rect1 + rect2 - intersection) 
  """
  Computes IUO between two bboxes in the form [x1,y1,x2,y2]
  """
  xx1 = np.maximum(bb_test[0], bb_gt[0])
  yy1 = np.maximum(bb_test[1], bb_gt[1])
  xx2 = np.minimum(bb_test[2], bb_gt[2])
  yy2 = np.minimum(bb_test[3], bb_gt[3])
  w = np.maximum(0., xx2 - xx1)
  h = np.maximum(0., yy2 - yy1)
  wh = w * h
  o = wh / ((bb_test[2] - bb_test[0]) * (bb_test[3] - bb_test[1])
    + (bb_gt[2] - bb_gt[0]) * (bb_gt[3] - bb_gt[1]) - wh)
  return(o)

def associate_dets_with_roi(dets , roi):
    matches = {}
    cost_matrix = np.zeros((len(dets) , len(roi)))
    for k , det in enumerate(dets):
        for j , one_roi in enumerate(roi):
            cost_matrix[k][j] = iou(det , one_roi)
            #print(cost_matrix)
    for i in range (0 , cost_matrix.shape[0] , 1):
        max_index = np.argmax(cost_matrix[i])
        if cost_matrix[i][max_index] > 0.50:
            matches[i] = max_index
    return matches


def get_file_contents(roi):
    try:
        f = open("utils/roi_test3.txt", 'r')
        rois = f.read().split('\n')
        for i in range (0 , len(rois)-1 , 1):
            vals = rois[i].split(' ')
            roi.append((int(vals[0]) , int(vals[1]) , int(vals[0])+int(vals[2]) , int(vals[1])+int(vals[3])))
    finally:
        f.close()
    return roi

def cvDrawBoxes(detections, img):
    for detection in detections:
        x, y, w, h = detection[2][0],\
            detection[2][1],\
            detection[2][2],\
            detection[2][3]
        xmin, ymin, xmax, ymax = convertBack(
            float(x), float(y), float(w), float(h))
        pt1 = (xmin, ymin)
        pt2 = (xmax, ymax)
        cv2.rectangle(img, pt1, pt2, (0, 255, 0), 1)
        cv2.putText(img,
                    detection[0].decode() +
                    " [" + str(round(detection[1] * 100, 2)) + "]",
                    (pt1[0], pt1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    [0, 255, 0], 2)
    return img


def convertBack(x, y, w, h):
    xmin = int(round(x - (w / 2)))
    xmax = int(round(x + (w / 2)))
    ymin = int(round(y - (h / 2)))
    ymax = int(round(y + (h / 2)))
    return xmin, ymin, xmax, ymax


netMain = None
metaMain = None
altNames = None
roi = []

def YOLO():

    global metaMain, netMain, altNames , roi
    configPath = "./cfg/yolov4.cfg"
    weightPath = "./yolov4.weights"
    metaPath = "./cfg/coco.data"
    if not os.path.exists(configPath):
        raise ValueError("Invalid config path `" +
                         os.path.abspath(configPath)+"`")
    if not os.path.exists(weightPath):
        raise ValueError("Invalid weight path `" +
                         os.path.abspath(weightPath)+"`")
    if not os.path.exists(metaPath):
        raise ValueError("Invalid data file path `" +
                         os.path.abspath(metaPath)+"`")
    if netMain is None:
        netMain = darknet.load_net_custom(configPath.encode(
            "ascii"), weightPath.encode("ascii"), 0, 1)  # batch size = 1
    if metaMain is None:
        metaMain = darknet.load_meta(metaPath.encode("ascii"))
    if altNames is None:
        try:
            with open(metaPath) as metaFH:
                metaContents = metaFH.read()
                import re
                match = re.search("names *= *(.*)$", metaContents,
                                  re.IGNORECASE | re.MULTILINE)
                if match:
                    result = match.group(1)
                else:
                    result = None
                try:
                    if os.path.exists(result):
                        with open(result) as namesFH:
                            namesList = namesFH.read().strip().split("\n")
                            altNames = [x.strip() for x in namesList]
                except TypeError:
                    pass
        except Exception:
            pass
    #cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture("test_videos/test_parking3.mp4")
    cap.set(3, 1280)
    cap.set(4, 720)
    out = cv2.VideoWriter(
        "output.avi", cv2.VideoWriter_fourcc(*"MJPG"), 10.0,
        (darknet.network_width(netMain), darknet.network_height(netMain)))
    print("Starting the YOLO loop...")

    # Create an image we reuse for each detect
    darknet_image = darknet.make_image(darknet.network_width(netMain),
                                    darknet.network_height(netMain),3)
    roi = get_file_contents(roi)
    while True:
        prev_time = time.time()
        ret, frame_read = cap.read()
        frame_rgb = cv2.cvtColor(frame_read, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb,
                                   (darknet.network_width(netMain),
                                    darknet.network_height(netMain)),
                                   interpolation=cv2.INTER_LINEAR)

        darknet.copy_image_from_bytes(darknet_image,frame_resized.tobytes())

        detections = darknet.detect_image(netMain, metaMain, darknet_image, thresh=0.25)
        #image = cvDrawBoxes(detections, frame_resized)
        image = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        dets = []
        if len(detections) > 0:
		# loop over the indexes we are keeping
            for i in range (0,len(detections)):
                if(detections[i][0].decode() == "car" and detections[i][1] > 0.25):
                    (x, y) = (detections[i][2][0], detections[i][2][1])
                    (w, h) = (detections[i][2][2] , detections[i][2][3] )
                    dets.append([float(x-w/2), float(y-h/2), float(x+w/2), float(y+h/2), float(detections[i][1])])
        matches = associate_dets_with_roi(dets , roi)
        print(1/(time.time()-prev_time))
        for i in range (0 , len(roi) , 1):
            cv2.rectangle(image , (roi[i][0]  , roi[i][1] ) , (roi[i][2] , roi[i][3])  , (0 , 0, 255) , 1)
            cv2.putText(image , str(i) , (int((roi[i][0] + roi[i][2])/2) -15 , int((roi[i][1] + roi[i][3])/2)-10) , cv2.FONT_HERSHEY_SIMPLEX, 1 , [0, 0, 255], 2 )
        for i in matches.keys():
            roi_idx = matches[i]
            cv2.rectangle(image , (roi[roi_idx][0]  , roi[roi_idx][1] ) , (roi[roi_idx][2] , roi[roi_idx][3])  , (0 , 255, 0) , 2)
            cv2.putText(image , str(roi_idx) , (int((roi[roi_idx][0] + roi[roi_idx][2])/2) -15 , int((roi[roi_idx][1] + roi[roi_idx][3])/2)-10) , cv2.FONT_HERSHEY_SIMPLEX, 1 , [0, 255, 0], 2 )
        cv2.imshow('Demo', image)
        cv2.waitKey(3)
    cap.release()
    out.release()

if __name__ == "__main__":
    YOLO()
