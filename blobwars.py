#!/usr/bin/env python3  

from tkinter import * 
from tkinter.messagebox import *

button_dict = {}
sel_point = (-1, -1)
tour = "Red-1"
number_red = 20
number_blue = 20


def valid_move(point_1, point_2):
    return ((abs(point_1[0] - point_2[0]) < 3) & (abs(point_1[1] - point_2[1]) < 3)) + ((abs(point_1[0] - point_2[0]) < 2) & (abs(point_1[1] - point_2[1]) < 2))


def move_is_possible():
    global button_dict
    global tour
    counter = 0
    if tour == 'Red-1':
        for point1, button1 in button_dict.items():
            if button1.cget('bg') == 'red':
                for point2, button2 in button_dict.items():
                    if button2.cget('bg') == 'red' and point1 != point2:
                        counter += valid_move(point1, point2)
        if counter == 0:
            tour = 'Blue-1'
            move_not_possible()
            return False
    elif tour == 'Blue-1':
        for point1, button1 in button_dict.items():
            if button1.cget('bg') == 'blue':
                for point2, button2 in button_dict.items():
                    if button2.cget('bg') == 'blue' and point1 != point2:
                        counter += valid_move(point1, point2)
        if counter == 0:
            tour = 'Red-1'
            move_not_possible()
            return False
    return True

        


def move_not_possible():
    showinfo('', 'You cannot play!')


def invalid_move():
    showinfo('', 'Your move is not valid')
        

def diffuse_color(point):
    global number_red
    global number_blue
    global button_dict
    color = button_dict[point].cget('bg')
    for row_index in range(-1, 2):
        for col_index in range(-1, 2):
            x = point[0] + row_index
            y = point[1] + col_index
            if button_dict.get((x, y)):
                if color == 'red':
                    if 'red' != button_dict[x, y].cget('bg') != 'yellow':
                        button_dict[x, y].config(bg='red')
                        number_red += 1
                        number_blue -= 1
                else:
                    if 'blue' != button_dict[x, y].cget('bg') != 'yellow':
                        button_dict[x, y].config(bg='blue')
                        number_red -= 1
                        number_blue += 1



def modify_menu():
    global tour
    menubar.delete(2)
    menu2 = Menu(menubar, tearoff=0)
    if tour == "Red-1":
        menubar.add_cascade(label="Red select the starting point",  foreground='red', menu=menu2)
    if tour == "Red-2":
        menubar.add_cascade(label="Red select the destination point", foreground='red', menu=menu2)
    if tour == "Blue-1":
        menubar.add_cascade(label="Blue select the starting point", foreground='blue', menu=menu2)
    if tour == "Blue-2":
        menubar.add_cascade(label="Blue select the destination point", foreground='blue', menu=menu2)


root = Tk()
root.title("Blobwars") 



def play(point):
    global number_red
    global number_blue
    global button_dict
    global tour
    global sel_point
    if (tour == "Red-1") & (button_dict[point].cget('bg') == 'red'):
        if move_is_possible():
            sel_point = point
            tour = "Red-2"
    elif (tour == "Red-2") & (button_dict[point].cget('bg') == 'yellow'):
        move_to_do = valid_move(point, sel_point)
        if move_to_do == 2:
        # Verify if the move is valid
            button_dict[point].config(bg='red')
            number_red += 1
            diffuse_color(point)
            tour = "Blue-1"
        elif move_to_do == 1:
            button_dict[point].config(bg='red')
            diffuse_color(point)
            button_dict[sel_point].config(bg='yellow')
            tour = "Blue-1"
        else:
            tour = "Red-1"
            invalid_move()
    if (tour == "Blue-1") & (button_dict[point].cget('bg') == 'blue'):
        if move_is_possible():
            sel_point = point
            tour = "Blue-2"
    elif (tour == "Blue-2") & (button_dict[point].cget('bg') == 'yellow'):
        move_to_do = valid_move(point, sel_point)
        if move_to_do == 2:
        # Verify if the move is valid
            button_dict[point].config(bg='blue')
            number_blue += 1
            diffuse_color(point)
            tour = "Red-1"
        elif move_to_do == 1:
            button_dict[point].config(bg='blue')
            diffuse_color(point)
            button_dict[sel_point].config(bg='yellow')
            tour = "Red-1"
        else:
            tour = "Blue-1"
            invalid_move()
    if number_red + number_blue == 100:
        winner()
    modify_menu()




Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)


menubar = Menu(root)

def p(): 
    print('salut')

#Create & Configure parent 
parent = Frame(root)
parent.grid(row=0, column=0, sticky=N+S+E+W)

#Create a 10x10 (rows x columns) grid of buttons inside the parent

def winner():
    if number_red > number_blue:
        showinfo('', 'Red player won the game!')
    elif number_red < number_blue:
        showinfo('', 'Blue player won the game!')
    else:
        showinfo('', 'Both players are tied')


def invalid_move():
    showinfo('', 'Your move is not valid!')

def quit_game():
    global root
    if askyesno('Quit the game', 'Are you sure to quit the game?'):
        root.quit()

def restart_game():
    global root
    if askyesno('Restart the game', 'Are you sure to quit the game?'):
        menubar.delete(1)
        menubar.delete(1)
        init_table()

def init_table():
    menu1 = Menu(menubar, tearoff=0)
    menu1.add_command(label="Resume")
    menu1.add_command(label="Restart", command=restart_game)
    menu1.add_command(label="Quit", command=quit_game)
    menubar.add_cascade(label="Pause", menu=menu1)

    menu2 = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Red select the starting point", foreground='red', menu=menu2)

    name = '0'
    color = 'red'
    for row_index in range(10):
        Grid.rowconfigure(parent, row_index, weight=1)
        for col_index in range(10):
            Grid.columnconfigure(parent, col_index, weight=1)
            if row_index < 2:
                color = 'red'
            elif row_index > 7:
                color = 'blue'
            else:
                color = 'yellow'
            button_dict[(row_index, col_index)] = Button(parent, bg=color, text=name, command=lambda point=(row_index, col_index): play(point))
            button_dict[(row_index, col_index)].grid(row=row_index, column=col_index, sticky=N+S+E+W)
            name =  str(int(name) + 1)
    





root.config(menu=menubar)


init_table()

root.mainloop()