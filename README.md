# raspberrypi-garden-system

# What was used
> OS: Raspbian OS Lite (Legacy) \
> Python Version: 3.7.3 \
> Check the python module versions in ```requirements.txt```.

# Installing Raspbian OS (only if you have the Raspberry Pi): 
0. Before installing the new OS, save any work that you might have in the Raspberry Pi. 
1. Install the Raspbian OS Lite/Desktop (Legacy) ("Legacy Version") normally. This is different from Raspbian OS Lite/Desktop without "(Legacy)" ("Non-Legacy Version") .The Non-Legacy Version should be the newest updated Raspbian OS for the Raspberry Pi. However, this version has not added support for the Python camera module, which is needed to run the code. Thus, in order to run the code, the Legacy Version is needed.
2. Install the Legacy Version with the normal procedures.

# Download the code
You can clone the code (if you are familiar with how Github works), or you can download the code as a zip file (Code => Download Zip). Unzip the file if applicable.

# Updating the Linux shell
1. Update and upgrade Linux. \
```sudo apt-get update``` \
```sudo apt-get upgrade```

2. Remove unnecessary/leftover packages just in case. \
```sudo apt-get autoremove```

3. Check if you have Python installed. \
```python3 --version``` \
If not installed, use this command. \
```sudo apt-get install python3.7```
> Note: it may not matter what Python version you have. However, the Legacy Version comes with Python 3.7 pre-installed, so that's the version we will work with.

4. Check if you have Pip installed. \
```pip --version``` \
If not installed, use this command. \
```sudo apt-get install python3-pip```

5. Create a Python virtual environment. This will let us install pip packages that will "stay" within the virtual environment, not affecting the overall system. Think of the phrase : "Whatever happens here, stays here". \
```python3 -m venv .```
> Note: the period at the end is intentional; it basically says to install the virtual environment in the current directory. Alternatively, you can replace the period with a path to where you want to install the virtual environment.

6. Activate the virtual environment. \
```source bin/activate```
> Note: if you have installed the virtual environment elsewhere, replace ```bin/activate``` with ```path/to/venv/bin/activate```.

7. Install the numpy module. This will help us with array math. \
```sudo pip install numpy```

8. Install the opencv module. This is the primary module for image processing. \
```sudo pip install opencv-python```

9. Test if opencv works. \
```python -c "import cv2"```

10. If importing cv2 results in an error, it may be because the related opencv packages are not installed. This is especially so with the Legacy Version. Input the following commands line by line. This will take up quite a bit of space. \
```sudo apt-get install libtiff5-dev libjasper-dev libpng12-dev``` \
```sudo apt-get install libjpeg-dev``` \
```sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev``` \
```sudo apt-get install libgtk2.0-dev``` \
```sudo apt-get install libatlas-base-dev gfortran``` \
Run this command again to see if unneeded packages were installed. \
```sudo apt-get autoremove```

11. Install the PiCamera Module. (Let me know if this doesn't work). \
```sudo apt-get install python3-camera```

# Displaying the images
If working with the Legacy Version with Desktop, running the command should work as intended by displaying 4 images, one after another. Cycle through each image by pressing any key. \
```python ndvi.py``` \
Need to do some research for Mac and more research for Legacy Version in case running the command does not work.

# Ignore these commands for now
```export DISPLAY=IP_ADDR:0.0```

```export LIBGL_ALWAYS_INDIRECT=1```
