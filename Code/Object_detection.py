import numpy as np
import time
import cv2

# Configuring pre-trained model.
network = cv2.dnn.readNet("yolov3-tiny.weights",
                          "cfg/yolov3-tiny.cfg")
with open("coco.names", "r") as d:
    classes = [line.strip() for line in d.readlines()]
NameofLayer = network.getLayerNames()
output_layers = [NameofLayer[i[0] - 1]
                 for i in network.getUnconnectedOutLayers()]
colours = np.random.uniform(0, 255, size=(len(classes), 3))

# Using OpenCV to read video file.
data = cv2.VideoCapture('test1.mp4') # use 0 to use camera on the system.
label_font = cv2.FONT_HERSHEY_PLAIN
start_time = time.time()
frame_id = 0
#run_time = 1


while True:
    _, frame = data.read()
    frame_id += 1
    height, width, channels = frame.shape
    detect = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    network.setInput(detect)
    output = network.forward(output_layers)
    class_ids = []
    confidence_scores = []
    box = []
    for out in output:
        for obj_detect in out:
            scores = obj_detect[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.3:

                center_a = int(obj_detect[0] * width)
                center_b = int(obj_detect[1] * height)
                w = int(obj_detect[2] * width)
                h = int(obj_detect[3] * height)
                a = int(center_a - w / 2)
                b = int(center_b - h / 2)
                box.append([a, b, w, h])
                confidence_scores.append(float(confidence))
                class_ids.append(class_id)
    indexes = cv2.dnn.NMSBoxes(box, confidence_scores, 0.4, 0.3)
    for i in range(len(box)):
        if i in indexes:
            a, b, w, h = box[i]
            label = str(classes[class_ids[i]])
            confidence = confidence_scores[i]
            colour = colours[class_ids[i]]
            cv2.rectangle(frame, (a, b), (a + w, b + h), colour, 2)
            cv2.rectangle(frame, (a, b), (a + w, b + 30), colour, -1)
            cv2.putText(frame, label + " " + str(round(confidence, 2)),
                        (a, b + 30), label_font, 3, (255, 255, 255), 3)
        run_time = time.time() - start_time
    fps = frame_id / run_time
    cv2.putText(frame, "FPS: " + str(round(fps, 2)), (10, 50), label_font, 3, (0, 0, 0), 3)
    cv2.imshow("Image", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break


data.release()
cv2.destroyAllWindows()