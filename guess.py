import func as f
import tkinter as tk

WINDOW_HEIGHT, WINDOW_WIDTH = 800, 800
BOT, TOP = 1, 100
SLEEP = 1.5 # in seconds

def main():
    wn = f.Window(height=WINDOW_HEIGHT, width=WINDOW_WIDTH, title='Guess the number')
    wn.wn.bgcolor('#02FEFE')
    # restart = wn.create_button((0, 300), text='Restart', command=wn.guess_the_number, anchor=tk.CENTER, font='Arial 30 bold')
    wn.guess_the_number(BOT, TOP, SLEEP)

if __name__ == '__main__':
    main()