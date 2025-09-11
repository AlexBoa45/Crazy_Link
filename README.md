# CrazyLink

CrazyLink is a library designed to facilitate the development of control applications for the Crazyflie drone.
This repository was created by a user as part of a master’s thesis project.
It was created using a Crazyflie 2.1 platform  with a Flow v2 deck and additionally, a Multi-ranger deck.
CrazyLink generally does not present errors, but it is not entirely exempt. 
During the creation of this library, its design was based on the DroneLink library.

All the detailed explanation can be found in the master’s thesis of: **Development of an application for the use of drones in Neurorehabilitation** by Alejandro Boadella





## Structure

Pycham has been used to develop this library.
Its structure is basic.

- **crazyLink folder**: Folder that contains the main Dron_crazyflie object, plus 2 additional folders.
    - **modules_crazyflie**: set of modules that composes the main library.
    - **test_crazyflie**: set of python script to test the drone in a simple way.

- **demostradores_crazyflie folder**: Folder that contains python scripts to test the drone with a GUI.

## Used libraries 

These are the used libraries:

- **shapely 2.1.1**: It is used in calculating the position of the drone.

- **cflib 0.1.27**: Main library to receive data and control the drone via python code

- **matplotlib 3.9.3**: Used to plot drone position.

- **tkintermapview 1.29**: Widget of tkinter to obtain interactive maps.

- **ttkbootstrap 1.10.1**: Additional package of style for tkinter library.

- **tkinter**: Already included with python. GUI library used for demos. 

- **customtkinter 5.2.2**: This library has been used to improve visual quality of the principal GUI library tkinter.

- **numpy 1.26.4**: Used to reckon drone position and display it via matplotlib.

- **scipy 1.14.1**: Extends numpy library, it has been used to filter data with a gaussian filter.



## Running Simple Tests

All the tests can be found in **crazyLink folder**.
For instance to run a simple test, run the following command in python:

```bash
import time
from time import sleep

from crazyLink.Dron_crazyflie import Dron

# Test general
    dron = Dron ()
    dron.connect()
    print ('conectado')
    dron.arm()
    print ('ya he armado')
    dron.takeOff (0.7)
    time.sleep (5)
    dron.go('Forward')
    time.sleep(1)
    print ('ya he alcanzado el punto indicado')
    dron.change_altitude(0.5)
    print ('ya he alcanzado la nueva altitud')
    dron.go ('Right')
    print ('voy a la derecha')
    time.sleep (2)
    dron.Land()
    print ('ya estoy en tierra')
    dron.disconnect()
```

Indeed, it is really simple, create a Dron object and play with it using object functions.
All the functions can be found in **modules_crazyflie**, and they are all explained.

## Running GUI Tests

Tkinter has been the main GUI developer library. 
Inside the **demostradores_crazyflie folder**, there are 3 scripts, 2 of them are GUI initiator.
 - **Dashboard Directo**: Opens a simple real time drone controller.
 - **Dashboard Plot**:  Opens a drone controller, allows the user to create geofences and displays drone position in real time.

## Video Explanation

Because of editing issues, here are the sections of the video:
 - Basic test script (till min 3)
 - Main code explanation (from min 3 till min 29)
 - Explanation of GUI tests (after min 29)

[![Watch the video](https://img.youtube.com/vi/58KjJVsbeIk/mqdefault.jpg)](https://youtu.be/58KjJVsbeIk)

##  Video Demo

[![Watch the video](https://img.youtube.com/vi/56AXOiJG1PU/mqdefault.jpg)](https://youtu.be/56AXOiJG1PU)

## Deployment

To connect the drone with the computer it can’t be done via bluetooth or at least it isn’t thought of. The way to connect the drone is via a crazyradio.

There are two types of radios: **Crazyradio PA** and **Crazyradio 2.0**. 

- **For the Crazyradio 2.0**:
    - The only necessary step is to add the software. Press the radio button and insert the USB into the computer at the same time. **Link**: https://github.com/bitcraze/crazyradio2-firmware/releases/tag/1.1
    - Download the file from the link above named:
            **crazyradio2-CRPA-emulation-[version].uf2**
    - Drag the downloaded file into the USB radio folder. 
    - Once this is done, the radio will update and emit a white light for a moment, every time it is connected again.
- **For the Crazyradio 2.0 and Crazyradio PA**:
    - Install Zadig. Zadig is a driver installer program whose purpose is to install a translator between different programs. **Link**: http://zadig.akeo.ie/
    - Once you have Zadig, connect the radio, select the radio in the top selector, choose “libusb”, and install the drivers.
    - If you don’t see any radio, check Device Manager within Zadig. Go to Options and select: List All Devices.
    - If an error occurs, you can reinstall the libusb driver.

To manage the antenna, you have to install Python +3.10 (https://www.python.org/). During the installation, an option will appear to enable the "Add Python to PATH" checkbox (for Command Prompt/CMD). It is important to select this option.

 - **Application (important to install)**:
This installation is dedicated for **Windows**, otherwise take a look at Bitcraze.

To install the application, you can either download it from this **link**: https://pypi.org/project/cfclient/

Also using PyCharm, it can be found as cfclient if searching for libraries.

Or install it directly via CMD with:

    pip3 install cfclient 

Once the application is installed, you can access it using the following commands in CMD (especially cfclient):

    cfclient 
    cfheadless 
    cfloader 
    cfzmq 
    python3 -m cfclient.gui 

To connect the drone, make sure the USB radio is plugged in and the drone is turned on.

In the cfclient interface, click the "Scan" button at the top left, then select and connect to the drone.

Once connected, you will be able to see the mode and stabilization status of the drone.

The drone can be controlled with the controller or by using the commands at the right bottom.

- **Other considerations**:
To update the Crazyflie firmware (recommended when using decks), make sure to attach all the decks before updating. If the drone detects these decks, it will automatically download the appropriate firmware.

With the drone powered on, open the cfclient application, then go to Connect → Bootloader. Connect the Crazyflie. 

Once connected, under "From release", select the latest firmware version for cf2 (Crazyflie 2.x). If nothing appears, under "From file", you can upload the latest version from the internet (cf2) using this **link**: https://github.com/bitcraze/crazyflie-release/releases.

Once the firmware is selected, click "Program" and wait. The drone will restart multiple times (meanwhile do not touch the drone). Once the blue progress bar is complete, the update is finished.


- **Fly using drone Crazyflie Library (important to install)**:

This installation is dedicated for Windows, otherwise take a look at Bitcraze.

To use Python, you need to install cflib. You can install it directly from this **link**:
https://github.com/bitcraze/crazyflie-lib-python

Also using PyCharm it can be found as cflib if searching for libraries.

However, I recommend creating a repository and cloning it manually.

    git clone https://github.com/bitcraze/crazyflie-clients-python 
    cd crazyflie-clients-python 

Install cflib using the following command:

    pip3 install -e . 

To uninstall cflib, use:

    pip uninstall cflib

In order to control the drone with Python code, simply turn on the drone, connect the radio, and click play on the code.

## Starting functions:
- **Script dron_connect ->** connect (self, freq = 4, cf_uri="radio://0/80/2M/E7E7E7E7E7")

- **Script dron_arm ->** arm(self, blocking=True, callback=None, params=None)

- **Script dron_takeOff ->** takeOff(self, aTargetAltitude, blocking=True, callback=None, params=None)

- **Script dron_RTL_LAND:** 
    - Land (self, blocking=True, callback=None, params = None) 
    - RTL (self, blocking=True, callback=None, params = None)


## Movement functions:
- **Script dron_altitude ->** change_altitude(self, altitude, blocking=True, callback=None, params=None)

- **Script dron_goto ->** goto (self, transversal, lateral, alt, blocking=True, callback=None, params = None)

- **Script dron_move:**
    - move_distance (self, direction, distance, blocking=True, callback=None, params = None)
    - setMoveSpeed (self, speed)

- **Script dron_nav:**
    - go(self, direction, blocking = True)
    - changeNavSpeed (self, speed)
    - changeHeading (self, absoluteDegrees, blocking=True, callback=None, params = None)

- **Script dron_RC_override ->** send_rc(self, roll, pitch, throttle, yaw, blocking=True, bare_mode=False, velocity_horizontal=0.3, velocity_vertical=0.2, yaw_velo=20)

## Geofence/Geocage functions:
The ComplexGeofence/Geofence functions define a buffer zone between the flyable area and the restricted zone. This buffer can be adjusted when necessary. 
It is implemented because optical flow noise in self-positioning reduces accuracy, and the buffer ensures a safe margin between the geofence limit and the point where the drone will automatically return to the flyable area.

- **Script dron_bottomGeofence:**
    - startBottomGeofence (self, minAlt)
    - stopBottomGeofence (self)

- **Script dron_topGeofence:**
    - startTopGeofence (self, minAlt)
    - stopTopGeofence (self)

- **Script dron_geofence:**
    - setSimpleScenario (self,scenario, watchdog=True, blocking=True, callback=None, params = None)
    - deleteSimpleScenario (self)

- **Script dron_complex_geofence:**
    - setComplexScenario (self,inside_polygon, exclusion, watchdog=True, blocking=True, callback=None, params = None)
    - deleteComplexScenario (self)

## Telemetry functions:

- **Script dron_local_telemetry:**
    - send_local_telemetry_info(self, process_local_telemetry_info)
    - stop_sending_local_telemetry_info(self)

- **Script dron_custom_telemetry:**
    - getParams(self, parameters, process_params=None)
    - stop_sending_params(self)
