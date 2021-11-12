import cv2
import RPIservo
import Adafruit_PCA9685
import functions
import move
import time


# Servo Initializations
fuc = functions.Functions()
fuc.start()


T_sc = RPIservo.ServoCtrl()
T_sc.start()

G_sc = RPIservo.ServoCtrl()
G_sc.start()

	
	# Arm movement + grab declarations
    def armUP():
		T_sc.singleServo(2, 1, 3)  #up
	def armDown():
		T_sc.singleServo(2, -1, 3) #down
    def armStop():
        T_sc.singleServo(2, 1, 0)  #stop arm
	def grab():
		G_sc.singleServo(4, -1, 3) #grab
    def loose():
        G_sc.singleServo(4, 1, 3)  #loosen
    def grabStop():
        G_sc.singleServo(4, 1, 0)  #stop grab

    
    # Grab object function
    def grabObj():
        armDown()
        time.sleep(1)
        srmStop()
        time.sleep(0.5)
        grab()
        time.sleep(2)
        grabStop()
        time.sleep(0.5)
        armUp()
        time.sleep(1)
        armStop()
        # time.sleep(0.5)
        # loose()
        # time.sleep(2)
        # grabStop()
        
		


### Lego XML setup
objectName = 'Lego'
lego_cascade = cv2.CascadeClassifier(
    'classifier/cascade_lego.xml')  # path of cascade file

cap = cv2.VideoCapture(0)

#set init area to 0
  object_area = 0
  object_x = 0
  object_y = 0
  minimum_area = 250
  maximum_area = 100000
  center_image_x = image_width / 2
  center_image_y = image_height / 2
  
# Main loop to detect the image and create a box around it
while True:
    success, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # try to tune this 6.5 and 17 parameter to get good result
    legos = lego_cascade.detectMultiScale(
        gray, 1.7, 19)  # adjust scale factor and neighbors
    for(x, y, w, h) in legos:
        resized = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(img, objectName, (x, y-5),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)  # Puts the text 'Lego' around the box
        roi_color = img[y:y+h, x:x+w]
		
		found_area = w * h
        center_x = x + (w / 2)
        center_y = y + (h / 2)
        if object_area < found_area:
            object_area = found_area
            object_x = center_x
            object_y = center_y
		#Update object location
    if object_area > 0:
        location = [object_area, object_x, object_y]
    else:
        location = None

 
    if location && len(objectName)>= 1:
        if (location[0] > minimum_area) and (location[0] < maximum_area):
            if location[1] > (center_image_x + (image_width/3)):
				move.move(speed_set, 'forward', 'right', rad) #(speed, direction, turn, radius)
                print("Turning right")
            elif location[1] < (center_image_x - (image_width/3)):
				move.move(speed_set, 'forward', 'left', rad) #(speed, direction, turn, radius)
                print("Turning left")
            else:
				move.move(speed_set, 'forward', 'no', rad) #(speed, direction, turn, radius)
                print("Forward")
        elif (location[0] < minimum_area):
			move.move(speed_set, 'forward', 'left', rad) #(speed, direction, turn, radius)
            print("Target isn't large enough, searching")
        else:
            move.motorStop()
            print("Target large enough, stopping")
            print("\nAttempting to grab...")                # Attempt to grab object when target is close enough to rover
            grabObj()
    else:
		fuc.radarScan()
        move.move(speed_set, 'forward', 'left', rad) #(speed, direction, turn, radius)
        print("Target not found, searching")
		

    # Display the final output window
    cv2.imshow('img', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
