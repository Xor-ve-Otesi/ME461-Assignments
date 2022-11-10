try:
  import cv2
  import mediapipe as mp
  import subprocess
  from pynput.keyboard import Key, Controller
  import time
except:
  print("Please install the necessary modules")

try:
  subprocess.Popen(["gnome-mines", "--small"])  # Open Minesweeper game
except:
  subprocess.run(["sudo", "apt-get", "install", "gnome-mines"])
# If there is no Gnome-Mines you should install with below code
# sudo apt-get install gnome-mines
try:
  keyboard = Controller()                       # Initialize Keyboard Controller
  radius  = 40                                  # Radius of the circles
  fingerTipIds = [8, 12, 16, 20]                # Mark IDs of the finger tips
  mp_draw = mp.solutions.drawing_utils          # Function to Draw Landmarks over Hand
  mp_hand = mp.solutions.hands                  # Hand Detection Function
  # Confidence level of AI, 1 is high 0 is low
  hands   = mp_hand.Hands(min_detection_confidence = 0.3, min_tracking_confidence = 0.3)
  old     = 0

  # Keyboard buttons
  def right_move():
    keyboard.press(Key.right)
    keyboard.release(Key.right)
  def left_move():
    keyboard.press(Key.left)
    keyboard.release(Key.left)
  def up_move():
    keyboard.press(Key.up)
    keyboard.release(Key.up)
  def down_move():
    keyboard.press(Key.down)
    keyboard.release(Key.down)
  def space():
    keyboard.press(Key.space)
    keyboard.release(Key.space)

  # Opening webcam
  cap = cv2.VideoCapture(0)
  # If you want to open your webcam 1280x720, you should uncomment below two lines                                           
  # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
  # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

  #### MAIN CODE ####
  while cap.isOpened():         #for every frame
    success, image = cap.read() #reading the frame
    h, w = image.shape[:2]      #height, width
    if not success:             #looking for if the frame is lost or not
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to pass by reference.
    image.flags.writeable = False
    results = hands.process(image)
    # Draw the hand annotations on the image.
    image.flags.writeable = True
    fingers_open = []
    landmarks_list = []

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[-1]
        for index, lm in enumerate(hand_landmarks.landmark):
            h, w, c = image.shape # Height, Width, Channels
            cx, cy = int(lm.x*w), int(lm.y*h)
            landmarks_list.append([index, cx, cy])
        # Drawing the Landmarks for only One Hand
        # Landmarks will be drawn for the Hand which was Detected First
        mp_draw.draw_landmarks(image, hand_landmarks, mp_hand.HAND_CONNECTIONS)
        hand_x = landmarks_list[9][1] # X coordinate of mark ID 9
        hand_y = landmarks_list[9][2] # Y coordinate of mark ID 9
        new = time.time()
        if  new - old > 0.4:                  # Constraint detection with time limit
          if hand_x < w*0.3:                  # If X coordinate is below 30% of width move right
            right_move()
          if hand_x > w*0.6:                  # If X coordinate is above 60% of width move left
            left_move()
          if hand_y < h*0.3:                  # If Y coordinate is below 30% of width move up
            up_move()
          if landmarks_list[0][2]> h*0.8:     # If Y coordinate is above 80% of width move down
            down_move()
          old = new

    # Stores 1 if finger is open and 0 if finger is closed
    # When a mark's Y coordinate is less than its previous mark's Y coordinate it means you make fist 
    fingers_open = []
    if len(landmarks_list) != 0 or len(landmarks_list) == 20:
        for tipId in fingerTipIds:
          if landmarks_list[tipId][2] < landmarks_list[tipId - 2][2]:
              fingers_open.append(1)
          else: 
              fingers_open.append(0)
              space()
    
    # Circle definitions
    red_cir     = cv2.circle(image, (int(w*0.1), int(h/2)),  radius, (0,0,255),  -1) # Red circle
    blue_cir    = cv2.circle(image, (int(w*0.9), int(h/2)),  radius, (255,0,0),  -1) # Blue circle
    yellow_cir  = cv2.circle(image, (int(w/2), int(h*0.1)),  radius, (255,0,255),-1) # Yellow circle
    green_cir   = cv2.circle(image, (int(w/2), int(h*0.9)),  radius, (0,255,0),  -1) # Green circle

    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1)) # Flip the image horizontally for a selfie-view display.
    if cv2.waitKey(5) & 0xFF == 27:                   # If you press ESC you leave
      break
  cap.release()                                       # Release capture
except:
  print("Unknown error.")
