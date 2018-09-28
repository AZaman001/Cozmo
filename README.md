# Cozmo Project

## For Demos

Place Cozmo in the center facing forward, place one cube behind him, and the remaining cubes facing inwards on either side of him. That way, to begin none of the objects are in front of Cozmo. When the endpoint is hit, the first thing Cozmo will do after announcing his task is turn 90 degrees, and face the first cube/object, take a picture and send it to the tensorflow endpoint. (That's why the object has to be facing inwards).

- Note: Try to make sure the background behind the objects are relatively clear/plain. Since that's how the pictures were taken for the training model.