import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps
import sys
import os
import shutil
import requests
import json
import time
import asyncio
import datetime
import csv
import subprocess


isProcessing = False
isTakingPicture = False
targetObject = sys.argv[1]
discoveredObject = False

print(targetObject)


# from Cozmo Detextive, disects response from Tensor Flow training model
def parseResponse(response):
    print(f"response is {response}")
    global targetObject
    global discoveredObject
    entries = {}
    highestConfidence = 0.0
    highestEntry = ''
    print(response)
    labels=[]
    values=[]
    for key in response.keys():
        if key == "answer":
            for guess in response[key].keys():
                print(f"guess: {guess}")
                labels.append(guess)
                values.append(response[key][guess])
                entries[response[key][guess]] = guess
    for key in entries.keys():
        if key > highestConfidence:
            highestConfidence = key
            highestEntry = entries[key]
    if highestConfidence > 0.8:
        if targetObject == highestEntry:
            discoveredObject = True
    print(labels)
    print(values)
    with open("result.csv",'w') as resultFile:
        wr = csv.writer(resultFile)
        wr.writerow(labels)
        wr.writerow(values)
    subprocess.call('pipenv run python3 graph.py', shell=True)


# Cozmo Detective's model of taking a picture
# Store photos taken locally and also posts it to tensorflow training model to recognize object
def on_new_camera_image(evt, **kwargs):
    global isProcessing
    global isTakingPicture
    global discoveredObject

    if isTakingPicture:
            if not isProcessing:
                if not discoveredObject:
                    isProcessing = True
                    pilImage = kwargs['image'].raw_image
                    photo_location = f"photos/fromcozmo-{kwargs['image'].image_number}.jpeg"
                    print(f"photo_location is {photo_location}")
                    pilImage.save(photo_location, "JPEG")
                    with open(photo_location, 'rb') as f:
                        # tensorflow endpoint
                        print("hitting tensorflow endpoint")
                        r = requests.post('https://cozmoimagerecognition-restoncloudhub.uscom-central-1.oraclecloud.com/tensorflow', files={'file': f})
                    print(r)
                    parseResponse(r.json())
                    isProcessing = False

# function created to pick up the cube which has the identified object on it
def get_object(robot: cozmo.robot.Robot):
    # Cozmo should observe the cube the obj is on
    robot.set_head_angle(degrees(-5.0)).wait_for_completed()

    print("Cozmo is waiting until he sees a cube")
    cube = robot.world.wait_for_observed_light_cube()

    # go to pick up cube, once seen
    print("Cozmo found a cube, and will now attempt to pick it up:")
    action = robot.pickup_object(cube, num_retries=2)

    action.wait_for_completed()
    print("result for LIFTING object:", action.result)

    # go away with picked up obj
    robot.drive_straight(distance_mm(-100), speed_mmps(100)).wait_for_completed()
    robot.turn_in_place(degrees(180)).wait_for_completed()
    robot.drive_straight(distance_mm(50), speed_mmps(100)).wait_for_completed()

    # set it down on the ground, "deliver"
    action = robot.place_object_on_ground_here(cube)
    action.wait_for_completed()
    print("result for PLACING object:", action.result)
    robot.say_text(f"I have completed my task. {targetObject} for John Dunbar.").wait_for_completed()

# from Cozmo Detective to look until target object is recognized.
def cozmo_program(robot: cozmo.robot.Robot):

    global isTakingPicture
    # creates a local directory if its not already there
    if os.path.exists('photos'):
        shutil.rmtree('photos')
    if not os.path.exists('photos'):
        os.makedirs('photos')

    #mute Cozmo while testing. Leave it in case we want it later.
    robot.say_text(f"Somebody just ordered the {targetObject}. I'll go get it for him.").wait_for_completed()
    # reset Cozmo's arms and head
    robot.set_head_angle(degrees(10.0)).wait_for_completed()
    robot.set_lift_height(0.0).wait_for_completed()

    robot.add_event_handler(cozmo.world.EvtNewCameraImage, on_new_camera_image)


    while not discoveredObject:
        isTakingPicture = False
        robot.turn_in_place(degrees(90)).wait_for_completed()
        isTakingPicture = True
        time.sleep(5)


    isTakingPicture = False

    if discoveredObject:

        # acknowledge its been found
        robot.say_text(f"Oh yay! I've found {targetObject}").wait_for_completed()
        # robot.play_anim_trigger(cozmo.anim.Triggers.MajorWin).wait_for_completed()

        # go to pick up obj
        cozmo.run_program(get_object(robot))



cozmo.run_program(cozmo_program, use_viewer=True, force_viewer_on_top=True)
