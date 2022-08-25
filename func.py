import turtle as tt
import tkinter as tk
from random import uniform
from math import sqrt
import time

PIXEL_TO_MM = 0.264583333333333333333333333333333333333333333333333
        
def dist(x0, y0, x1, y1):
    return sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)

def is_coordinate(x: tuple):
    return len(x) == 2

def is_in_all_circles(dot:tuple, circle_list: list):
    if not is_coordinate(dot):
        raise TypeError('You did not enter a valid coordinate')
    for (x, y, r) in circle_list:
        if dist(dot[0], dot[1], x, y) > r:
            return False
    return True

class Window():
    def __init__(self, width: int, height: int, title: str, background_color='white'):
        self.wn = tt.Screen()
        self.wn.setup(width, height)
        self.wn.title(title)
        self.wn.bgcolor(background_color)
        self.canvas = tt.getcanvas()
        self.root = self.canvas.master
        self.wp = tt.Turtle()
        self.wp.ht()
        self.wp.up()
        tt.delay(0)
        
        self.textpen = tt.Turtle()
        self.textpen.ht()
    
    def integer_entry(self, title: str, description: str, default: int, f: int, t: int, wait=0) -> int:
        # print(wait)
        time.sleep(wait)
        entry = tt.numinput(title, description, default=default, minval=f, maxval=t)
        # check if entry is an integer
        if entry is None:
            return self.integer_entry(title, description, default, f, t)
        elif int(entry) != entry:
            tk.messagebox.showinfo('Warning', f'The number you entered: {entry}, is not an integer, please try again.')
            return self.integer_entry(title, description, default, f, t)
        return int(entry)
    
    def create_button(self, top_left: tuple, text: str, command, anchor=tk.SW, font='Arial 12'):
        if not is_coordinate(top_left):
            raise TypeError('You did not enter a valid coordinate')
        button = tk.Button(self.canvas.master, text=text, command=command, font=font)
        self.canvas.create_window(top_left[0], top_left[1], anchor=anchor, window=button)
        # button.grid(row=row, column=column)
        return button
    
    def create_rectangle(self, top_left: tuple, lower_right: tuple, width=3, speed=5):
        if not is_coordinate(top_left) or not is_coordinate(lower_right):
            raise TypeError('You did not enter a valid coordinate')
        self.wp.speed(speed)
        self.wp.width(width)
        self.wp.goto(top_left[0], top_left[1])
        self.wp.down()
        rec_width, rec_height = abs(top_left[0]-lower_right[0]), abs(top_left[1]-lower_right[1])
        for _ in range(2):
            self.wp.forward(rec_width)
            self.wp.right(90)
            self.wp.forward(rec_height)
            self.wp.right(90)
        self.wp.up()
    
    def create_circle(self, center: tuple, radius: int, width=3, speed=5):
        if not is_coordinate(center):
            raise TypeError('You did not enter a valid coordinate')
        # draw need offset y value by negative radius   
        center = (center[0], center[1]-radius)
        self.wp.goto(center[0], center[1])
        self.wp.speed(speed)
        self.wp.down()
        self.wp.circle(radius)
        self.wp.up()
    
    # font --> 'Font Size (bold/underline..)'
    def create_text(self, text: str, top_left: tuple, font: str, anchor=tk.SW, fill='Black'):
        if not is_coordinate(top_left):
            raise TypeError('You did not enter a valid coordinate')
        tmp = self.canvas.create_text(top_left, text=text, fill=fill, font=font, anchor=anchor)
        return tmp 
        
    def monte_carlo_simulation_area(self, circle_list: list, square_length: int, dot_size=3):   
        self.show_dots = True
        self.end_sim = False
        core_area_text=self.create_text(f'Core area: {0:.5f} mm^2', top_left=(-square_length/2-30, 125), font='Arial 15 bold')
        sample_taken_text=self.create_text(f'Sample taken: 0', top_left=(-square_length/2-30, 145), font='Arial 15 bold')
        time_text=self.create_text(f'Runtime: 00:00:00.000', top_left=(-square_length/2-30, 165), font='Arial 15 bold')
        cnt, num = 0, 0
        tlx, tly = -square_length/2, square_length/2
        brx, bry = square_length/2, -square_length/2
        self.wp.speed(0)
        start_time = time.time()
        while True:
            if self.end_sim:
                break
            num += 1
            dot = (uniform(tlx, brx), uniform(tly, bry))
            self.wp.goto(dot[0], dot[1])
            if is_in_all_circles(dot, circle_list):
                if self.show_dots:
                    self.wp.dot(dot_size, 'green')
                cnt += 1
            elif self.show_dots:
                self.wp.dot(dot_size, 'red')
            area = cnt/num*(square_length*PIXEL_TO_MM)**2
            self.canvas.itemconfig(core_area_text, text=f'Core area: {area:.5f} mm^2')
            self.canvas.itemconfig(sample_taken_text, text=f'Sample taken: {num}')
            sep = time.time()-start_time
            self.canvas.itemconfig(time_text, text=f'Runtime: {int(sep//3600):02d}:{int(sep//60)%60:02d}:{int(sep%60):02d}.{int(sep%1*1000):03d}')

    def monte_carlo_simulation_pi(self, square_length: int, circle_list: list, dot_size=3):
        self.show_dots = True
        self.end_sim = False
        estimated_pi=self.create_text(f'π estimated: {0:.10f}', top_left=(-square_length/2-30, 125), font='Arial 15 bold')
        sample_taken_text=self.create_text(f'Sample taken: 0', top_left=(-square_length/2-30, 145), font='Arial 15 bold')
        time_text=self.create_text(f'Runtime: 00:00:00.000', top_left=(-square_length/2-30, 165), font='Arial 15 bold')
        tlx, tly = -square_length/2, square_length/2
        brx, bry = square_length/2, -square_length/2
        num, cnt = 0, 0
        self.wp.speed(0)
        start_time=time.time()
        while True:
            if self.end_sim:
                break
            num += 1
            dot = (uniform(tlx, brx), uniform(tly, bry))
            self.wp.goto(dot[0], dot[1])
            if is_in_all_circles(dot, circle_list):
                if self.show_dots:
                    self.wp.dot(dot_size, 'green')
                cnt += 1
            elif self.show_dots:
                self.wp.dot(dot_size, 'red')
            pi = cnt/num*4
            # print(pi)
            self.canvas.itemconfig(estimated_pi, text=f'π estimated: {pi:.10f}')
            self.canvas.itemconfig(sample_taken_text, text=f'Sample taken: {num}')
            sep = time.time()-start_time
            self.canvas.itemconfig(time_text, text=f'Runtime: {int(sep//3600):02d}:{int(sep//60)%60:02d}:{int(sep%60):02d}.{int(sep%1*1000):03d}')
    
    def create_square(self, top_left: tuple, side_length: int, width=3, speed=5):
        if not is_coordinate(top_left):
            raise TypeError('You did not enter a valid coordinate')
        self.create_rectangle(top_left, (top_left[0]+side_length,top_left[1]+side_length), width=width)
        
    def hide_dots_and_delete_button(self, circle_list, button, square_length):
        self.show_dots = False
        self.wp.up()
        self.wp.color('black')
        self.wp.clear()
        self.create_square((-square_length/2, square_length/2), square_length, width=3, speed=2)
        button.destroy()
        for (x, y, r) in circle_list:
            self.create_circle((x, y), r, speed=0)

    def end_simulation(self):
        self.end_sim = not self.end_sim
    
    def reset(self, circle_list, is_pi):
        self.end_simulation()
        self.canvas.delete('all')
        self.wp.clear()
        if is_pi:
            import pi
            pi.main(circle_list)
        else:
            import core
            core.main(circle_list)
    
    def restart_core(self):
        self.end_simulation()
        self.canvas.delete('all')
        self.wp.clear()
        import core
        core.main()
        
    def restart_guess(self):
        self.end_simulation()
        self.canvas.delete('all')
        self.wp.clear()
        import guess
        guess.main()
        
    
    def guess_the_number(self, bot, top, SLEEP):
        import math, random
        self.end_sim = False
        title=self.create_text(f'GUESS THE NUMBER', (0, -300), font='Arial 50 bold', anchor=tk.CENTER, fill='Black')
        tries = int(math.ceil(math.log2(top-bot+1)));
        used = 0
        used_text = self.create_text(f'Chances used: {used}/{tries}', (0, 200), font='Arial 30 bold', anchor=tk.CENTER)
        target = random.randint(bot, top)
        instruction=self.create_text(f'Guess the number between {bot} and {top}', (0, -150), font='Arial 30 bold', anchor=tk.CENTER)
        print(target)
        guessed = False
        for i in range(tries):
            if self.end_sim or guessed:
                break
            self.canvas.itemconfig(instruction, text=f'Guess the number between {bot} and {top}')
            input = self.integer_entry(title='Guess', description=f'Type in a number between {bot} and {top}', default=0, f=bot, t=top, wait=0 if used == 0 else SLEEP)
            if input < target:
                if i == tries-1:
                    continue
                higher_text = self.create_text(f'The target is higher than {input}', (0, 0), font='Arial 30 bold', anchor=tk.CENTER, fill='Blue')
                self.canvas.update()
                self.root.after(int(SLEEP*1000), self.canvas.delete, higher_text)
                bot = input+1
            elif input > target:
                if i == tries-1:
                    continue
                lower_text = self.create_text(f'The target is lower than {input}', (0, 0), font='Arial 30 bold', anchor=tk.CENTER, fill='Blue')
                self.canvas.update()
                self.root.after(int(SLEEP*1000), self.canvas.delete, lower_text)
                top = input-1
            else:
                self.canvas.delete(instruction)
                self.create_text(f'Congrats!', (0, -150), font='Arial 30 bold', fill='Red', anchor=tk.CENTER)
                self.create_text(f'You guessed the correct number!', (0, -100), font='Arial 30 bold', fill='Red', anchor=tk.CENTER)
                self.create_text(f'The correct answer is: {target}', (0, -20), font='Arial 25 bold', anchor=tk.CENTER)
                self.create_text(f'Number of chances used: {used+1}', (0, 20), font='Arial 25 bold', anchor=tk.CENTER)
                self.canvas.update()
                guessed = True
            
            used += 1
            self.canvas.itemconfig(used_text, text=f'Chances used: {used}/{tries}')
        
        if not guessed:
            self.canvas.delete(instruction)
            self.canvas.itemconfig(used_text, text=f'Chances used: {tries}/{tries}')
            self.create_text(f'Mission Failed.', (0, -150), font='Arial 30 bold', fill='Red', anchor=tk.CENTER)
            self.create_text(f'You ran out of chances!', (0, -100), font='Arial 30 bold', fill='Red', anchor=tk.CENTER)
            self.create_text(f'The correct answer is: {target}', (0, -20), font='Arial 25 bold', anchor=tk.CENTER)
            self.create_text(f'Number of chances used: {used}', (0, 20), font='Arial 25 bold', anchor=tk.CENTER)
        
        self.create_button((-100, 100), text='Restart', command=self.restart_guess, anchor=tk.CENTER, font='Arial 30 bold')
        self.create_button((100, 100), text='  End  ', command=exit, anchor=tk.CENTER, font='Arial 30 bold')
        tt.done()
        