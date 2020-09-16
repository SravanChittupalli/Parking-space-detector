import cv2
import argparse

arg = argparse.ArgumentParser()
arg.add_argument("-d" , "--dimentions" , required=True , help="input dims of the model")
args = vars(arg.parse_args())

vid = cv2.VideoCapture('test_parking3.mp4')

_ , frame = vid.read()
frame = cv2.resize(frame , (int(args["dimentions"]), int(args["dimentions"])) , interpolation=cv2.INTER_LINEAR)
cv2.imshow("selectROI" , frame)
#use space or enter to finish current selection and start a new one, . use esc to terminate multiple ROI selection process
rois = cv2.selectROIs("selectROI" , frame )
print(rois)
cv2.destroyAllWindows()
print("Saving ROI's in file...")
try:
    f = open('roi.txt' , 'w')
    print("Opened file")
    for i in range (0 , len(rois) , 1):
        for j in range (0 , 4 , 1):
            to_write = str(rois[i][j])
            f.write(to_write + " ")
        f.write('\n')
finally:
    f.close()
    print("Closed file")
    print("Save successful...")