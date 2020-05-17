import numpy as np
import cv2
import sys
import os
import time

if __name__=="__main__":

    start=0
    end=0
    delay=0
    count=0

    # create writer object
    fileName=sys.argv[2]  # change the file name if needed
    imgSize=(960,540)
    frame_per_second=20.0
    fourcc=cv2.cv.CV_FOURCC(*'I420')
    #fourcc=cv2.VideoWriter_fourcc(*'I420')
    #writer = cv2.VideoWriter(fileName,cv2.VideoWriter_fourcc('I','4','2','0'),15,(960,540),True)#cv2.VideoWriter_fourcc(*"X264"), frame_per_second,imgSize)#0x00000021,15,(1280,720)) #cv2.VideoWriter_fourcc(*"X264"), frame_per_second,imgSize)
    writer = cv2.VideoWriter(fileName,fourcc,15,(960,540),True)#cv2.VideoWriter_fourcc(*"X264"), frame_per_second,imgSize)#0x00000021,15,(1280,720)) #cv2.VideoWriter_fourcc(*"X264"), frame_per_second,imgSize)
    #writer_init = cv2.VideoWriter('/home/nvidia/SHAHHOS/processing/noisy.avi',cv2.VideoWriter_fourcc('I','4','2','0'),15,(960,540),True)

    if len(sys.argv) == 1:
        print("Please set input file")
        sys.exit(1)
    # TODO: check if file is possible to open

    cnt = 0
    cap = cv2.VideoCapture(sys.argv[1])
    while(cap.isOpened()):
        start=time.time()
        cnt+=1
        print(cnt)
        ret, frame = cap.read()
        if ret==True:
            count=count+1
            frame_denoised = cv2.fastNlMeansDenoisingColored(frame,None,10,10,7,21)
            writer.write(frame_denoised)
            end=time.time()
            delay=delay+(end-start)*1000       
            #writer_init.write(frame)
        else:
            print("Average FPS is:"+str(delay/count)+" ms")
            break

    # Release everything if job is finished
    cap.release()
    writer.release()
