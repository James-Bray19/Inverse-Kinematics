import numpy as np
import tkinter as tk

segment_lengths = [100, 80, 60, 40, 20]
screen_width = 400
screen_height = 400
fps = 60

class Segment():
    def __init__(self, length, start_pos, end_pos):
        self.length = length
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.omega = 1 # rad/s

    def follow(self, target):
        # rotate segment towards target with angular velocity omega
        current_vector = self.end_pos - self.start_pos
        target_vector = target - self.start_pos

        dot_product = np.dot(current_vector, target_vector)
        angle = np.arccos(np.clip(dot_product / (np.linalg.norm(current_vector) * np.linalg.norm(target_vector)), -1.0, 1.0))

        cross_product = np.cross(current_vector, target_vector)
        if cross_product < 0:
            angle = -angle

        if abs(angle) < self.omega / fps:
            self.rotate(angle)
        elif angle < 0:
            self.rotate(-self.omega / fps)
        else:
            self.rotate(self.omega / fps)

        # move segment towards target
        self.move(target - self.end_pos)

    def move(self, disp):
        self.start_pos += disp
        self.end_pos += disp

    # rotate around start position
    def rotate(self, angle):
        vector = self.end_pos - self.start_pos
        x_new = vector[0] * np.cos(angle) - vector[1] * np.sin(angle)
        y_new = vector[0] * np.sin(angle) + vector[1] * np.cos(angle)
        self.end_pos = self.start_pos + np.array([x_new, y_new])


# called when mouse is moved
def update():
    # inverse kinematics
    for i in reversed(range(len(segments))):
        if i == len(segments) - 1:
            segments[i].follow(mouse)
        else:
            segments[i].follow(segments[i+1].start_pos)

    # fix arm to base
    base_disp = np.array([screen_width/2, screen_height]) - segments[0].start_pos
    for i in range(len(segments)):
        segments[i].move(base_disp)

    # draw arm
    canvas.delete('all')
    for i in segments:
        interp = i.length / max(segment_lengths)
        canvas.create_line(i.start_pos[0], i.start_pos[1], i.end_pos[0], i.end_pos[1], width=interp * 8)

    root.after(1000 // fps, update)

# initialise segments
segments = []
start_y = screen_height
for length in segment_lengths:
    segments.append(Segment(length, np.array([screen_width/2, start_y]), np.array([screen_width/2, start_y - length])))
    
# tkinter
root = tk.Tk()
root.title("Inverse Kinematics")

canvas = tk.Canvas(root, width=screen_width, height=screen_height)
canvas.pack()

# mouse tracking
mouse = [0, 0]
def set_pos(event):
    mouse[0] = event.x
    mouse[1] = event.y
canvas.bind("<Motion>", set_pos)

update()

root.mainloop()