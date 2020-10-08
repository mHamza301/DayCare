# USAGE
# python recognize_faces_video_file.py --encodings encodings.pickle --input videos/lunch_scene.mp4
# python recognize_faces_video_file.py --encodings encodings.pickle --input videos/lunch_scene.mp4 --output output/lunch_scene_output.avi --

# import the necessary packages
from imutils.video import VideoStream
import face_recognition
import imutils
import pickle
import time
import cv2
import sys

if __name__ == '__main__':
    # construct the argument parser and parse the arguments
    encodings = 'F:\\FYP 2019-2020\\Facial Recognition Python\\encodingsTset.pickle'

    output = 'F:\\FYP 2019-2020\\Facial Recognition Python\\output\\output.avi'

    display = 0;

    detectionMethod = 'hog'

    # load the known faces and embeddings
    print("[INFO] loading encodings...")
    data = pickle.loads(open(encodings, "rb").read())

    Room = "Room1"
    # initialize the video stream and pointer to output video file, then
    # allow the camera sensor to warm up
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    writer = None
    time.sleep(2.0)

    path1 = 'F://FYP 2019-2020//Facial Recognition Python//output//Room1.txt'
    path2 = 'F://FYP 2019-2020//Facial Recognition Python//output//Room2.txt'
    Room1File = open(path1,'r')
    Room2File = open(path2,'r')
    Room1Data = Room1File.read().split('\n')
    Room2Data = Room2File.read().split('\n')
    Room1File.close()
    Room2File.close()
    List1 = {}
    List2 = {}
    
    for idx, word in enumerate(Room1Data):
        if len(word) > 1:
            line = word.split('\t\t')
            #print(line)
            name = line[0]
            present = line[1]
            List1[name] = present

    for idx, word in enumerate(Room2Data):
        if len(word) > 1:
            line = word.split('\t\t')
            #print(line)
            name = line[0]
            present = line[1]
            List2[name] = present
    #print(List1)
    #print(List2)

    counts2 = {}
    # loop over frames from the video file stream
    frames = 0;
    while True:
        # grab the next frame
        frame = vs.read()
        frames = frames + 1;
        face = 0;
        
        # convert the input frame from BGR to RGB then resize it to have
        # a width of 750px (to speedup processing)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb = imutils.resize(frame, width=750)
        r = frame.shape[1] / float(rgb.shape[1])
        
        # detect the (x, y)-coordinates of the bounding boxes
        # corresponding to each face in the input frame, then compute
        # the facial embeddings for each face
        boxes = face_recognition.face_locations(rgb,model=detectionMethod)
        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []
        
        # loop over the facial embeddings
        for encoding in encodings:
            face = face  + 1;
            # attempt to match each face in the input image to our known
            # encodings
            matches = face_recognition.compare_faces(data["encodings"],encoding)
            name = "Unknown"

            # check to see if we have found a match
            if True in matches:
                # find the indexes of all matched faces then initialize a
                # dictionary to count the total number of times each face
                # was matched
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                
                # loop over the matched indexes and maintain a count for
                # each recognized face face
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                # determine the recognized face with the largest number
                # of votes (note: in the event of an unlikely tie Python
                # will select first entry in the dictionary)
                name = max(counts, key=counts.get)

                if Room == "Room1":
                    List2[name] = 0
                    List1[name] = 1
                if Room == "Room2":
                    List1[name] = 0
                    List2[name] = 1
                print("[INFO] Updating files ..")
                f = open(path1, "w")
                for xname in List1:
                    f.write(xname + "\t\t" + str(List1[xname]) + "\n")
                f.close()
                f2 = open(path2, "w")
                for xname in List2:
                    f2.write(xname + "\t\t" + str(List2[xname]) + "\n")
                f2.close()


                #counts2[name] = counts2.get(name,0) + 1
                #print("for frame "+str(frames) +" in encoding " + str(face) + " name is " + name)
                #if False in matches:
                #print("for frame "+str(frames) +" in encoding " + str(face) + " name is " + name)
                #counts2[name] = counts2.get(name,0) + 1
		
            # update the list of names
            names.append(name)

        # loop over the recognized faces
        for ((top, right, bottom, left), name) in zip(boxes, names):
            # rescale the face coordinates
            top = int(top * r)
            right = int(right * r)
            bottom = int(bottom * r)
            left = int(left * r)

            # draw the predicted face name on the image
            cv2.rectangle(frame, (left, top), (right, bottom),(255, 0, 0), 2)
            y = top - 15 if top - 15 > 15 else top + 20
            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,0.75, (0, 0, 255), 2)

        # if the video writer is None *AND* we are supposed to write
        # the output video to disk initialize the writer
        if writer is None and output is not None:
            fourcc = cv2.VideoWriter_fourcc(*"MJPG")
            writer = cv2.VideoWriter(output, fourcc, 15,(frame.shape[1], frame.shape[0]), True)

        # if the writer is not None, write the frame with recognized
        # faces t odisk
        if writer is not None:
            writer.write(frame)

        # check to see if we are supposed to display the output frame to
        # the screen
        if display > 0:
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF

            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break

    # close the video file pointers
    cv2.destroyAllWindows()
    vs.stop()

    #finalname = max(counts2, key=counts2.get)
    #print(finalname)

	

    # check to see if the video writer point needs to be released
    if writer is not None:
        writer.release()