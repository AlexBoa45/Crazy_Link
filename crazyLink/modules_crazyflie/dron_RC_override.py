import threading
import time
import logging

# !!!!!!!!!! SCRIPT TO BE TESTED !!!!!!!!!

# Secondary function to normalize trim values
def rc_to_normalized(value, channel='throttle'):
    # Converts a typical RC value (1000–2000) to a normalized value for Crazyflie.
    # For roll, pitch, yaw: scales to [-1, 1]
    # For throttle: scales to [0, 1]
    if channel == 'throttle':
        # throttle usually ranges from 1000 (min) to 2000 (max) -> 0 to 1
        normalized = (value - 1000) / 1000
        # Limit to [0, 1]
        return max(0.0, min(1.0, normalized))
    else:
        # roll, pitch, yaw: 1000 (min) -> -1, 1500 (center) -> 0, 2000 (max) -> +1
        normalized = (value - 1500) / 500
        # Limit to [-1, 1]
        return max(-1.0, min(1.0, normalized))

# Primary function, input trim values of a controller,(geocage maybe will not work with this) (to be tested with geocage) (top-bot cages will not work)
# Allows 2 methods, second method is more recommended, additionally, optional velocities can be applied.
def send_rc(self, roll, pitch, throttle, yaw, bare_mode=False, velocity_horitzontal=0.3, velocity_vertical=0.2):
    
    if bare_mode:
        # First mode
        # Send normalized RC commands to the drone via MotionCommander.
        # roll, pitch, yaw in [-1,1], throttle in [0,1]
        try:
            # Normalizes values
            roll_n = rc_to_normalized(roll, 'rc')
            pitch_n = rc_to_normalized(pitch, 'rc')
            yaw_n = rc_to_normalized(yaw, 'rc')
            throttle_n = rc_to_normalized(throttle, 'throttle')

            # Sends setpoints
            self.mc.commander.send_setpoint(roll_n, pitch_n, yaw_n, throttle_n)

            return True

        except Exception as e:
            print(f"Error enviando comando RC: {e}")
            return False
    else:
        # Second mode
        try:
            # Check if the controller has any drift and compensate
            if 1600 > throttle > 1400:
                throttle = 1500

            if 1600 >  roll > 1400:
                roll = 1500

            if 1600 > pitch > 1400:
                pitch = 1500

            if 1600 > yaw > 1400:
                yaw = 1500

            # Calculate a proportional controller
            roll = (roll - 1500)
            if roll != 0:
                roll = roll/500

            pitch = (pitch - 1500)
            if pitch != 0:
                pitch = pitch / 500

            yaw = (yaw- 1500)
            if yaw != 0:
                yaw = yaw / 500

            throttle = (throttle - 1500)
            if throttle != 0:
                throttle = throttle / 500
            
            # If the distance to the ground is so small don't allow the user go down.
            if self.position[2] < 0.05:
                if throttle < 0:
                    throttle = 0
            
            # Starts linear movements
            self.mc.start_linear_motion(velocity_horitzontal*pitch, -velocity_horitzontal*roll, velocity_vertical*throttle)

        except Exception as e:
            print(f"Error enviando comando RC: {e}")
            return False




