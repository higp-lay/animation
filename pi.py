import func as f
import tkinter as tk

WINDOW_HEIGHT, WINDOW_WIDTH = 400, 400
SQUARE_LENGTH = 200

def main(circle_list=[(0, 0, SQUARE_LENGTH/2)]):
    wn = f.Window(height=WINDOW_HEIGHT, width=WINDOW_WIDTH, title='π Estimation Monte Carlo Simulation')
    wn.wn.bgcolor('#02FEFE')
    wn.create_square((-SQUARE_LENGTH/2, SQUARE_LENGTH/2), SQUARE_LENGTH, width=3, speed=2)
    
    hide = wn.create_button((-WINDOW_WIDTH/2+100, -WINDOW_HEIGHT/2+70), text='Hide dots', command=lambda: wn.hide_dots_and_delete_button(circle_list, hide, SQUARE_LENGTH), anchor=tk.CENTER)
    end = wn.create_button((WINDOW_WIDTH/2-100, -WINDOW_HEIGHT/2+70), text='   End   ', command=wn.end_simulation, anchor=tk.CENTER)
    clear = wn.create_button((0, -WINDOW_HEIGHT/2+70), text='  Reset  ', command=lambda: wn.reset(circle_list, is_pi=True), anchor=tk.CENTER)
    
    wn.create_circle((0, 0), radius=SQUARE_LENGTH/2, speed=0)
    wn.monte_carlo_simulation_pi(SQUARE_LENGTH, circle_list)
    
if __name__ == '__main__':
    main()