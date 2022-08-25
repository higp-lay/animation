import func as f
from random import uniform
from time import sleep
from func import dist
import tkinter as tk

WINDOW_HEIGHT, WINDOW_WIDTH = 400, 400
SQUARE_LENGTH = 200
MIN_RADIUS, MAX_RADIUS = 50, 100
MIN_DISTANCE_BETWEEN_CIRCLES = 0

# BORDER_HEIGHT, BORDER_WIDTH = WINDOW_HEIGHT-SQUARE_HEIGHT, WINDOW_WIDTH-SQUARE_WIDTH

def check_all_intersect(l, x, y, r):
    for (xx, yy, rr) in l:
        d = dist(x, y, xx, yy)
        if d >= rr+r - MIN_DISTANCE_BETWEEN_CIRCLES:
            return False
    return True

def generate_circle_list(n):
    circle_list = []
    tlx, tly = -SQUARE_LENGTH/2, SQUARE_LENGTH/2
    brx, bry = SQUARE_LENGTH/2, -SQUARE_LENGTH/2
    while len(circle_list) < n:
        x, y = uniform(tlx, brx), uniform(tly, bry)
        r = uniform(MIN_RADIUS, MAX_RADIUS)
        if x-r < tlx or x+r > brx or y+r > tly or y-r < bry:
            continue
        elif not check_all_intersect(circle_list, x, y, r):
            continue
        circle_list.append((x, y, r))
        # print(tlx, tly, brx, bry, x, y, r)
    return circle_list
            
def main(circle_list=None):
    wn = f.Window(height=WINDOW_HEIGHT, width=WINDOW_WIDTH, title='Core Area Monte Carlo Simulation')
    wn.wn.bgcolor('#02FEFE')
    if circle_list is None:
        circle_list_size = wn.integer_entry(title='Enter number of circle', description='Between 1 to 10', default=2, f=1, t=10)
        circle_list = generate_circle_list(circle_list_size)
    wn.create_square((-SQUARE_LENGTH/2, SQUARE_LENGTH/2), SQUARE_LENGTH, width=3, speed=2)
    
    hide = wn.create_button((-WINDOW_WIDTH/2+70, -WINDOW_HEIGHT/2+70), text='Hide dots', command=lambda: wn.hide_dots_and_delete_button(circle_list, hide, SQUARE_LENGTH), anchor=tk.CENTER)
    end = wn.create_button((WINDOW_WIDTH/2-70, -WINDOW_HEIGHT/2+70), text='   End   ', command=wn.end_simulation, anchor=tk.CENTER)
    clear = wn.create_button(((WINDOW_WIDTH-140)/4-WINDOW_WIDTH/2+95, -WINDOW_HEIGHT/2+70), text='  Reset  ', command=lambda: wn.reset(circle_list, is_pi=False), anchor=tk.CENTER)
    restart = wn.create_button(((WINDOW_WIDTH-140)/4+WINDOW_WIDTH/2-219, -WINDOW_HEIGHT/2+70), text=' Restart ', command=lambda: wn.restart_core(), anchor=tk.CENTER)
    
    for (x, y, r) in circle_list:
        wn.create_circle((x, y), r, speed=0)
    wn.monte_carlo_simulation_area(circle_list, SQUARE_LENGTH)
    # wn.create_circle((0, 0), 100)

if __name__ == '__main__':
    main()