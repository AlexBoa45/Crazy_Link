import logging
import time

# Secondary function that makes the action: startTopGeofence
def _checkTopGeofence (self, alt):
    # Check if the height of the drone is inside bounds.
    if self.checkMaxAlt == True:
        if alt >= self.maxAltGeofence:
                logging.warning("[Dron] Dentro de zona de exclusion superior.")
                return True
        else:
                return False
    else:
            return False

# Alternative function in order to move the drone inside the Geofence
def _moveTopGeofence (self):
    if self.mc != None:
        if self.checkMaxAlt == True:
            if self.position[2] > self.maxAltGeofence:
                correction = abs(self.position[2] - self.maxAltGeofence)
                self.mc.down(correction)
                logging.warning("[Dron] Dentro de zona de exclusion superior, moviendo dron.")
                time.sleep(1.5)

# Primary function to start the top Geofence
def startTopGeofence (self, maxAlt, processBreach = None):
    self.maxAltGeofence = maxAlt
    self.checkMaxAlt = True

# Function to stop the top geofence
def stopTopGeofence (self):
    self.checkMinAlt = False
