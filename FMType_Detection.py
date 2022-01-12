import cv2 as cv
import numpy as np

Conf_threshold = 0.4
NMS_threshold = 0.4

COLORS = [(255,0,0),(255,0,255),(0,0,255),(0,255,255)]

"""
    Color Code:
        Red = 0,0,255
        Violet = 0,255,0 
        Yellow = 0,255,255
        Blue = 255,0,0 
"""

class_name = []
with open('MaskTypes.names','r') as f:
    class_name = [cname.strip() for cname in f.readlines()]
print(class_name)

net = cv.dnn.readNet('Mask.weights','Mask.cfg')
net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA_FP16)

model = cv.dnn_DetectionModel(net)
model.setInputParams(size=(416,416), scale = 1/255, swapRB=True)

cap = cv.VideoCapture(0)

while True:
    ret, frame =cap.read()
    
    if ret == False:
        break
    
    classes, scores, boxes = model.detect(frame,Conf_threshold, NMS_threshold)
    for (classid, score, box) in zip(classes, scores, boxes):
        classes = np.argmax(scores) 
        confidence = scores[classes]

        if confidence > 0.7:
            color = COLORS[int(classid)%len(COLORS)]
            label = "%s : %f" % (class_name[classid[0]], score)
                
        else:
            color = 0,0,255
            label = "%s : %f" % ('No Mask Detected', score)
        
        cv.rectangle(frame,box,color,1)
        cv.putText(frame,label, (box[0], box[1]-10), cv.FONT_HERSHEY_COMPLEX, 0.5,color, 2)
   
    cv.imshow('frame',frame)
    key = cv.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
