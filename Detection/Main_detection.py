import cv2
import numpy as np
import glob
import random


def take_from_image():
    Result = []
    # Load Yolo

    net = cv2.dnn.readNet("./Detection/yolov3_training_last.weights", "./Detection/yolov3_testing.cfg")

    # print('vllll')
    # Name custom object
    classes = ["character"]

    # Images path
    # images_path = glob.glob("\*")
    # print(images_path)
    images_path = ['C:\\Users\\Admin\\Desktop\\Project\\Detection\\1.jpg']



    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    # Insert here the path of your images
    # random.shuffle(images_path)
    # loop through all the images
    for img_path in images_path:
        # Loading image
        
        img = cv2.imread(img_path)
        img = cv2.resize(img, None, fx=0.4, fy=0.4)
        print(img)
        height, width, channels = img.shape

        # Detecting objects
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

        net.setInput(blob)
        outs = net.forward(output_layers)

        # Showing informations on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.3:
                    # Object detected
                    print(class_id)
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,51,9)
        
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        # print('vlxxxx')
        print(indexes)
        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                x -= 10
                y -= 10
                w += 20
                h += 20
                label = str(classes[class_ids[i]])
                color = colors[class_ids[i]]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                crop_image = thresh[y:y+h, x:x+w]
                crop_image = cv2.resize(crop_image, ((28, 28)))
                Result.append(crop_image)
                # cv2.imwrite('test'+ str(x) + str(y) + str(w) + str(h) +'.png', crop_image)


        cv2.imshow("Image", img)
        key = cv2.waitKey(0)

    cv2.destroyAllWindows()

    return Result


def take_from_array(images_array, show_detail = 0):
    Result = []
    ListX = []
    # Load Yolo
    net = cv2.dnn.readNet("./Detection/yolov3_training_last.weights", "./Detection/yolov3_testing.cfg")

    # Name custom object
    classes = ["character"]

    # Images path

    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))


    # loop through all the images
    for img_path in images_array:
        # Loading image
        img = img_path
        img = cv2.resize(img, None, fx=0.4, fy=0.4)
        height, width, channels = img.shape

        # Detecting objects
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

        net.setInput(blob)
        outs = net.forward(output_layers)

        # Showing informations on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.3:
                    # Object detected
                    print(class_id)
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,51,9)
        
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        print(indexes)
        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                ListX.append(x)
                x -= int(x/40)
                y -= int(y/9)
                w += 2*int(x/40)
                h += 2*int(y/8)
                # if(y < 0):
                #     y = 0
                # if(x < 0):
                #     x = 0
                # w += 20
                # h += 20
                print(x, y, w, h)
                label = str(classes[class_ids[i]])
                color = colors[class_ids[i]]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                print(x, y, w, h)
                crop_image = thresh[y:y+h, x:x+w]
                if w > h: 
                    a = int(18*h/w)
                    crop_image = cv2.resize(crop_image, ((18, a)))               
                    img_pad = np.zeros([28, 28])    
                    img_pad[5:5+a, 5:23] = crop_image
                    crop_image = img_pad
                    # if show_detail == 1:
                        # cv2.imshow("pad", img_pad)
                        # cv2.waitKey(0)
                    Result.append(crop_image)
                if h >= w:
                    a = int(18*w/h)
                    crop_image = cv2.resize(crop_image, ((a, 18)))               
                    img_pad = np.zeros([28, 28])    
                    img_pad[5:23, 5:5+a] = crop_image
                    crop_image = img_pad
                    # cv2.imshow("pad", img_pad)
                    # cv2.waitKey(0)
                    Result.append(crop_image)
        if show_detail == 1:
            cv2.imshow("Image", img)
            
        key = cv2.waitKey(0)
        
    for i in range(0, len(ListX), 1):
        for j in range(i, len(ListX), 1):
            if ListX[i] > ListX[j]:
                temp = ListX[i]
                ListX[i] = ListX[j]
                ListX[j] = temp
                temp_A = Result[i]
                Result[i] = Result[j]
                Result[j] = temp_A

    cv2.destroyAllWindows()
    print('confidence: ')
    print(confidences)

    return Result