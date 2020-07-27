'''
##################################################################
# Course Information: UCB-EMP Program Module 1 Course 2.         #
# Description: Simulation for a "Flatland World".                #
# Last Edited at: Jul/20/2020.                                   #
# Written by: Lianzhe Wang.                                      #
##################################################################
'''
# import libraries
import matplotlib
import matplotlib.pyplot
import matplotlib.animation
import matplotlib.colors as colors
from matplotlib.colors import to_rgba
import numpy as np
import ffmpeg
import random
from copy import deepcopy
plt = matplotlib.pyplot


######## UNCOMMNET this line below for generating output Video. #########
# matplotlib.use("Agg") 


# Movie writer declaration.
Writer = matplotlib.animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)

# Plot layout definition. 
# 2 Subplots: ax for 2D view, ax2 for 1D projection view (the way a flatlander sees).
fig = plt.figure(constrained_layout=True,figsize = (6, 7))
fig.canvas.set_window_title('Flatland_Simulation')
gs1 = fig.add_gridspec(nrows=6, ncols=5, left=0.05, right=0.9, wspace=0.05)
ax = fig.add_subplot(gs1[:-1, :])
ax2 = fig.add_subplot(gs1[-1, :])
ax2.set_yticklabels([])
ax.grid(color = 'gray')
ax2.grid()
ax.set_xlim(-100, 100)
ax.set_ylim(0, 200)
ax2.set_xlim(-100, 100)
ax2.set_ylim(-20, 20)
ax.set_ylabel('2-D View')

# The moving objects difination. Type: matplotlib.patches 
# Objects include: Rectangle, Triangle, Circle & Hexagon.
# Color declared by cmap helps to maintain the consistence between 2-D static and 1-D dynamic pixel colors. 
cmap = matplotlib.cm.get_cmap('Greens')
rect1 = matplotlib.patches.Rectangle((5, 105), 20, 16, fc = cmap(0.65)) 
cmap = matplotlib.cm.get_cmap('Oranges')
rect2 = matplotlib.patches.Rectangle((0, 160), 17, 16, fc = cmap(0.5)) 
cmap = matplotlib.cm.get_cmap('YlOrBr')
circle = matplotlib.patches.Ellipse((75, 125), 25, 25, angle=0, fc = cmap(0.5))
xy = np.array([[-70,25],[-40,25],[-55,10]])
cmap = matplotlib.cm.get_cmap('Blues')
triangle = matplotlib.patches.Polygon(xy, closed=True, fc = cmap(0.5))
cmap = matplotlib.cm.get_cmap('Reds')
rect3 = matplotlib.patches.Rectangle((-7, 50), 17, 16, fc = cmap(0.7)) 
cmap = matplotlib.cm.get_cmap('BuPu')
circle2 = matplotlib.patches.Ellipse((-75, 75), 25, 25, angle=0, fc = cmap(0.75))
xy2 = np.array([[70,50],[40,50],[55,35]])
cmap = matplotlib.cm.get_cmap('Purples')
triangle2 = matplotlib.patches.Polygon(xy2, closed=True, fc = cmap(0.8))
xy3 = np.array([[-65,150],[-75,150],[-80,157.5],[-75,165],[-65,165],[-60,157.5]])
cmap = matplotlib.cm.get_cmap('YlGn')
hexagon = matplotlib.patches.Polygon(xy3, closed=True, fc = cmap(0.6))
mat_patches = [rect1, rect2, circle, triangle, rect3, circle2, triangle2, hexagon]

# Objects speed
speed = [4.5, 3.0, 3.0, 3.0, 3.0, 2.5, 3.0, 5.0]

# Add patches into the plot.
for patch in mat_patches:
    ax.add_patch(patch)

# Add light sources into the plot.
x_axis = np.linspace(-2, 2, 256)
y_axis = np.linspace(-2, 2, 256)

xx, yy = np.meshgrid(x_axis, y_axis)
arr = np.sqrt((0-xx) ** 2 + (0-yy) ** 2)
arr_ = np.sqrt((0-xx) ** 2)
inner = np.array([0.5, 0.5, 0.5])[None, None, :]
outer = np.array([1, 1, 1])[None, None, :]

arr = arr[:, :, None]
arr = arr * inner + (1 - arr) * outer

pic = np.ones((800,800,3), dtype=float)
pic *= 0
pic[400: 400+256, 500: 500+256] = arr
pic[25: 25+256, 25: 25+256] = arr
pic = np.clip(pic, 0, 1)
ax.imshow(pic, cmap='gray', extent=[-100, 100, 0, 200], alpha = 0.4)
ax.text(-80, 160, r'Light Source 1', fontsize=8)
ax.text(40, 65, r'Light Source 2', fontsize=8)
ax.text(-35, 3, r'↑↑↑ Observation Position ↑↑↑', fontsize=10)

arr_ = arr_[:, :, None]
arr_ = arr_ * inner + (1 - arr_) * outer
pic = np.ones((800,800,3), dtype=float)
pic *= 0
pic[272+64: 272+256-64, 500: 500+256] = arr_[0:128, :]
pic[272+64: 272+256-64, 25: 25+256] = arr_[0:128, :]
ax2.imshow(pic, cmap='gray', extent=[-100, 100, -20, 20], alpha = 0.4)

# Frame information for animation.
frame_paths = []
frames_ = 80
for i in range(0,int(frames_ / 2 + 1)):
    frame_paths.append([[rect1.get_x(),rect1.get_y()],[rect2.get_x(),rect2.get_y()],[rect3.get_x(),rect3.get_y()],
    circle.get_center(),circle2.get_center(),triangle.get_xy(),triangle2.get_xy(),hexagon.get_xy()])

ims = []

# Other configures
Opacity_ = 0.9 # for a better view.


# Animation functions: init() and animate(i) need to be defined to support the calling from matplotlib.animation.FuncAnimation.
def init():
    '''
    init() function.
    Here the implmentation is not needed.
    '''
    pass

def animate(i):
    '''
    animate() function. Takes one integer input (Frame count).
    This is the most important part. The updates of locations of both 2-D and 1-D views need to be finished within this function.
    '''
    # 2D object locations update. on ax.
    # The motions of 2-D objects are basically randomized. 
    # To prevent collisions, the objects would move the way back every frames_/2 of frames. And the speed of objects have been carefully designed.
    if i == 0:
        pass

    # First half frames_: the objects make random moves.
    elif i < (frames_ / 2):
        frame_paths[i][0] = [speed[0] * (random.random() - 0.5) + rect1.get_x(), rect1.get_y()]
        rect1.set_xy(frame_paths[i][0])
        frame_paths[i][1] = [speed[1] * (random.random() - 0.5) + rect2.get_x(), speed[1] * (random.random() - 0.5) + rect2.get_y()]
        rect2.set_xy(frame_paths[i][1])
        frame_paths[i][2] = [speed[2] * (random.random() - 0.5) + rect3.get_x(), speed[2] * (random.random() - 0.5) + rect3.get_y()]
        rect3.set_xy(frame_paths[i][2])
        frame_paths[i][3] = (circle.get_center()[0] + speed[3] * (random.random() - 0.5), circle.get_center()[1] + speed[3] * (random.random() - 0.5))
        circle.set_center(frame_paths[i][3])
        frame_paths[i][4] = (circle2.get_center()[0] + speed[4] * (random.random() - 0.5), circle2.get_center()[1] + speed[4] * (random.random() - 0.5))
        circle2.set_center(frame_paths[i][4])
        frame_paths[i][5] = triangle.get_xy() + speed[5] * (random.random() - 0.5)
        triangle.set_xy(frame_paths[i][5])
        frame_paths[i][6] = triangle2.get_xy() + speed[6] * (random.random() - 0.5)
        triangle2.set_xy(frame_paths[i][6])
        frame_paths[i][7] = hexagon.get_xy() + speed[7] * (random.random() - 0.5)
        hexagon.set_xy(frame_paths[i][7])
    
    # Second half frames_: the objects make the firs half way back, to the initial location.    
    else:
        rect1.set_xy(frame_paths[frames_-1-i][0])
        rect2.set_xy(frame_paths[frames_-1-i][1])
        rect3.set_xy(frame_paths[frames_-i-1][2])
        circle.set_center(frame_paths[frames_-1-i][3])
        circle2.set_center(frame_paths[frames_-1-i][4])
        triangle.set_xy(frame_paths[frames_-1-i][5])
        triangle2.set_xy(frame_paths[frames_-1-i][6])
        hexagon.set_xy(frame_paths[frames_-1-i][7])

    # Draw on ax2 for the 1-D flat view.
    # Using numpy arrays to generate different 1-D object views.
    # Sequential colormaps are used to show different distance light.
    ax2.clear()
    ax2.set_ylabel('1-D(Flatlander\'s) View')
    ax2.set_yticklabels([])
    ax2.grid()
    ax2.set_xlim(-100, 100)
    ax2.set_ylim(-20, 20)
    ax2.imshow(pic, cmap='gray', extent=[-100, 100, -20, 20], alpha = 0.4) 

    # Here, vector operation are utlized for the update of EVERY pixel values. The closer, the brighter.
    # The [distance to observing point] : [Brightness Level] relation are set to be linear. 
    Proj_rect2 = np.ones((10,10)) * ((200 - rect2.get_y()) / 200)
    ax2.imshow(Proj_rect2, cmap='Oranges', norm=colors.LogNorm(vmin=0.01, vmax=1), extent=[rect2.get_x(), rect2.get_x()+17, -4, 4], alpha = Opacity_)

    Proj_rect1 = np.ones((10,10)) * ((200 - rect1.get_y()) / 200)
    ax2.imshow(Proj_rect1, cmap='Greens', norm=colors.LogNorm(vmin=0.01, vmax=1), extent=[rect1.get_x(), rect1.get_x()+20, -4, 4], alpha = Opacity_)

    Proj_rect3 = np.ones((10,10)) * ((200 - rect3.get_y()) / 200)
    ax2.imshow(Proj_rect3, cmap='Reds', norm=colors.LogNorm(vmin=0.01, vmax=1), extent=[rect3.get_x(), rect3.get_x()+20, -4, 4], alpha = Opacity_)

    Proj_hexagon = np.concatenate([np.linspace(7.5,0,10),np.linspace(0, 0, 20), np.linspace(0,7.5,10)])
    Proj_hexagon = np.vstack((Proj_hexagon, Proj_hexagon))
    Proj_hexagon = (200 - Proj_hexagon - hexagon.get_xy()[2][1])/200
    ax2.imshow(Proj_hexagon, cmap='YlGn', norm=colors.LogNorm(vmin=0.05, vmax=0.5), extent=[hexagon.get_xy()[5][0], hexagon.get_xy()[2][0], -4, 4], alpha = Opacity_)

    # 1-D circle is the most interesting one. Here the vector operation could smoothly generate different brightness values for every pixel point on it.
    Proj_circle = 1 - (np.linspace(-1, 1, 30)**2)
    Proj_circle = np.vstack((Proj_circle, Proj_circle))
    Proj_circle = (200 - Proj_circle - circle.get_center()[1])/200
    ax2.imshow(Proj_circle, cmap='YlOrBr', norm=colors.LogNorm(vmin=0.25, vmax=0.5), extent=[circle.get_center()[0]-12.5, circle.get_center()[0]+12.5, -4, 4], alpha = Opacity_)

    Proj_circle2 = 1 - (np.linspace(-1, 1, 30)**2)
    Proj_circle2 = np.vstack((Proj_circle2, Proj_circle2))
    Proj_circle2 = (200 - Proj_circle2 - circle2.get_center()[1])/200
    ax2.imshow(Proj_circle2, cmap='BuPu', norm=colors.LogNorm(vmin=0.35, vmax=0.75), extent=[circle2.get_center()[0]-12.5, circle2.get_center()[0]+12.5, -4, 4], alpha = Opacity_)

    Proj_triangle = np.concatenate([np.linspace(15,0,30),np.linspace(0, 15, 30)])
    Proj_triangle = np.vstack((Proj_triangle, Proj_triangle))
    Proj_triangle = (200 - Proj_triangle - triangle.get_xy()[2][1])/200
    ax2.imshow(Proj_triangle, cmap='Blues', norm=colors.LogNorm(vmin=0.75, vmax=1), extent=[triangle.get_xy()[2][0]-15, triangle.get_xy()[2][0]+15, -4, 4], alpha = 1)

    Proj_triangle2 = np.concatenate([np.linspace(15,0,30),np.linspace(0, 15, 30)])
    Proj_triangle2 = np.vstack((Proj_triangle2, Proj_triangle2))
    Proj_triangle2 = (200 - Proj_triangle2 - triangle2.get_xy()[2][1])/200
    ax2.imshow(Proj_triangle, cmap='Purples', norm=colors.LogNorm(vmin=0.55, vmax=0.97), extent=[triangle2.get_xy()[2][0]-15, triangle2.get_xy()[2][0]+15, -4, 4], alpha = 1)

    #Animation function end.
    
anim = matplotlib.animation.FuncAnimation(fig, animate, init_func=init, frames=frames_, interval=200, save_count=900)


######### COMMNET this line below for generating output Video. ##########
plt.show() 

######## UNCOMMNET this line below for generating output Video. #########
#anim.save("Flatland.mp4", writer=writer) # UNCOMMNET this line for Video Output.