# Flatland
==============================

Introduction
-------------

This is a python3 program simulates the world a flatlander sees.

Environment Requirement.
---------------

1. A (Linux/MacOs/Windows) system with Python3 Installed. 
2. Libraries Requirement:
   `pip install matplotlib` (My working version of matplotlib is 3.2.2)
   `pip install numpy`
3. (Optional) If video saving is required, ffmpeg need to be installed.
    For MacOS, I recommand to use homebrew install. `brew install ffmpeg`
    This url might help if you find any issue installing ffmpeg: https://ffmpeg.org/
    
Running & Testing
-------

1. Run the terminal command 
    `python3 flatland.py`
   This would generate a window directly shows the moving 2-D objects with a 1-D flat view.
   Example snapshots and videos could be found in this folder.
   
2. If you wanna save a video like the example video mentioned above. You may:
   Confirm you have ffmpeg installed in your environment.
   Make modifications to the script: Uncomment line 23 and 227, Comment line 224 in the flatland.py file. (Their are hint lines in the .py file)
   Then, run `python3 flatland.py`. This should save a .mp4 file in the folder.

Implementation Details
-----------

This implementation is based on matplotlib. The 2-D objects are implemented by matplotlib.patch(), while the matched 1-D view objects are written based on numpy arrays. Observing point lays at (0, 0), watching towards postive y-direction.
Object types include: Rectangle, Triangle, Circle and Hexagon.
This work made vector operations at the 1-D view generating phase, such that the pixel value would be efficently calculated for the light different view (the closer the pixel distance to the observing point, the lightter the pixel would be).
Light source are added through numpy arrays.
Motions of the objects are basically random works. Collision avoidance is achieved from “back to the same way” setting of objects after a certain number of iterations of the animation, and precise calculations of objects' speed.

More detialed informations could be presented and explained better at the comments in the script file.


Make Modifications
----------------

I would be really happy if you wanna make any new work based on this project. :)
Unfortunately, because of the properties of matplotlib.patch, it was hard for me to make modular design for the objects append. So you might need to duplicate some of the code describing the initial and motion of particular object and make modifications to have new objects added in. (which might require you to make a little understanding of this code structure.) 
I'm more than happy to help if you meet any problem while make modifications on this, definately go contact me if you need any help. :)
