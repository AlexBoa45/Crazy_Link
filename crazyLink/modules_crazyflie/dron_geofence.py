
import threading
import time
import logging
import math

# Tertiary function to check the dron position within the geofence and move it in case of
def _moveSimpleScenario(self, callback=None, params = None):
    # Scenario = [ forward/backward, right or left ]

    # Check the state
    if self.state == "flying" and self.checksimpleGeofence == True:
        # Obtain the position
        x, y, z = self.position
        y = -y  # correction
        limit_x, limit_y = self.simpleGeofence
        # For safety
        limit_x = abs(limit_x)
        limit_y = abs(limit_y)

        # Obtain the excess
        excess_x = 0
        if x > limit_x:
            excess_x = x - limit_x
        elif x < -limit_x:
            excess_x = x + limit_x

        excess_y = 0
        if y > limit_y:
            excess_y = y - limit_y
        elif y < -limit_y:
            excess_y = y + limit_y

        # If the excess is not enough don't move the drone
        if abs(excess_x) < 0.2 and abs(excess_y) < 0.2:

            if callback != None:
                if self.id == None:
                    if params == None:
                        callback()
                    else:
                        callback(params)
                else:
                    if params == None:
                        callback(self.id)
                    else:
                        callback(self.id, params)

            return
        else:

            # Change direction and multiply by a factor of correction (the factor can be changes as the user wants)
            dx_w = -excess_x*1.2
            dy_w = -excess_y*1.2

            # Obtain the heading and correct it
            yaw_rad = -math.radians(self.attitude[2])

            # Rotation based on the drone's coordinate axis
            dx_body = dx_w * math.cos(yaw_rad) + dy_w * math.sin(yaw_rad)
            dy_body = -dx_w * math.sin(yaw_rad) + dy_w * math.cos(yaw_rad)

            # Stop the drone
            self.mc.stop()
            time.sleep(0.5)

            # Send the corrections to the drone (these are the easiest correction)
            # Another method would be use goto/move
            if dx_body > 0:
                self.mc.forward(dx_body)
            elif dx_body < 0:
                self.mc.back(abs(dx_body))

            if dy_body > 0:
                self.mc.right(dy_body)
            elif dy_body < 0:
                self.mc.left(abs(dy_body))

            # Callback
            if callback != None:
                if self.id == None:
                    if params == None:
                        callback()
                    else:
                        callback(params)
                else:
                    if params == None:
                        callback(self.id)
                    else:
                        callback(self.id, params)

    return

# Secondary function to check repeatedly or not the state of the dron and move if it is needed
def _watchSimpleScenario(self,watchdog,callback=None, params = None):

    if watchdog == True:
        while self.checksimpleGeofence == True:
            self._moveSimpleScenario(callback, params)
            time.sleep(0.3)
    else:
        self._moveSimpleScenario(callback,params)
        time.sleep(0.3)
    return

# Secondary function to check if the drone is inside or out the geofence
def _checkSimpleScenario(self, transversal, lateral):
    if  self.checksimpleGeofence == True:
        if abs(transversal) >= abs(self.simpleGeofence[0]) or abs(lateral) >= abs(self.simpleGeofence[1]):
            return True
        else:
            return False
    else:
        return False

# Primary function to set the simple scenario (rectangular geofence)
# As input Scenario = [ abs(forward/backward), abs(right/left) ]
# The watchdog is a method used to check periodically the state of the drone within the geofence,
# it can be disabled (watchdog== False), though the simpleScenario will only check the drone once it is executed
def setSimpleScenario (self,scenario, watchdog=True, blocking=True, callback=None, params = None):
    # Check if the scenario is too small
    try:
        if abs(scenario[0]) < 1 or abs(scenario[1]) < 1:
            logging.info(f"El escenario debe tener valores numéricos positivos, >1m !!!.")
            return
    except:
        logging.info(f"El escenario debe tener valores numéricos positivos, >1m !!!.")
        return

    if blocking and watchdog == False:
        logging.info(f"[Dron] Geofence simple creado.")
        self.checksimpleGeofence = True
        self.simpleGeofence = scenario
        self._watchSimpleScenario(watchdog)
        return True
    else:
        logging.info(f"[Dron] Geofence simple creado.")
        self.checksimpleGeofence = True
        self.simpleGeofence = scenario
        scenarioThread = threading.Thread(target=self._watchSimpleScenario, args=[watchdog,callback, params])
        scenarioThread.start()

        return True

# Primary function to be unable the geofence of the simple scenario
def deleteSimpleScenario (self):
    self.checksimpleGeofence = False
    return True
