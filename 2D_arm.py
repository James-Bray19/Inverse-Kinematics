import numpy as np
import tkinter as tk

segment_lengths = [100, 80, 60, 40, 20]
screen_width = 400
screen_height = 400

class Segment():
    def __init__(self, length, start_pos, end_pos):
        self.length = length
        self.start_pos = start_pos
        self.end_pos = end_pos

    def follow(self, target):
        # point segment at target
        target_vector = target - self.start_pos
        target_direction = target_vector / np.linalg.norm(target_vector)
        self.end_pos = self.start_pos + target_direction * self.length

        # move segment towards target
        self.move(target - self.end_pos)

    def move(self, disp):
        self.start_pos += disp
        self.end_pos += disp

# called when mouse is moved
def update(event):

    # inverse kinematics
    for i in reversed(range(len(segments))):
        if i == len(segments) - 1:
            segments[i].follow(np.array([event.x, event.y]))
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
canvas.bind("<Motion>", update)

root.mainloop()