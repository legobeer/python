#!/usr/bin/env python3  

"""
Programming the game blobwars with a graphical interface.
The game is developed with a 10x10 grid
"""

import tkinter as tk
import tkinter.messagebox as tkmsg

# root window
root = None

# menubar
menubar = None

# stores the buttons forming the grid
button_dict = {}

# starting point of pawn duplication or move
sel_point = (-1, -1)

# define which player should play
turn = "red-1"

# number of red squares
number_red = 2

# number of blue squares
number_blue = 2


def valid_move(point_1, point_2):
    """
    Return 0 if the move is not valid.
    Return 1 if the move does not creat a new colored squared.
    Return 2 if the move is a duplication.
    """
    return (((abs(point_1[0] - point_2[0]) < 3) & (abs(point_1[1] - point_2[1]) < 3))
           + ((abs(point_1[0] - point_2[0]) < 2) & (abs(point_1[1] - point_2[1]) < 2)))


def move_is_possible():
    """
    Return True if the player can play otherwise False.
    """
    global button_dict
    global turn
    counter = 0
    color = turn[:-2]
    if turn[-1] == '1':
        for point1, button1 in button_dict.items():
            if button1.cget('bg') == color:
                for point2, button2 in button_dict.items():
                    if (button2.cget('bg') == color or button2.cget('bg') == 'yellow') and point1 != point2:
                        counter += valid_move(point1, point2)
        if counter == 0:
            if color == 'red':
                turn = 'blue-1'
            else:
                turn = 'red-1'
            move_not_possible()
            return False
    return True


def move_not_possible():
    """
    Displays on the screen that the player cannot play.
    """
    tkmsg.showinfo('', 'You cannot play!')


def invalid_move():
    """
    Displays on the screen that the move is not possible.    
    """
    tkmsg.showinfo('', 'Your move is not valid')


def winner():
    """
    Shows on the screen who is the winner and refresh the game.
    """    
    global number_blue
    global number_red
    global root
    global menubar
    global turn
    if number_red > number_blue:
        tkmsg.showinfo('', 'red player won the game!')
    elif number_red < number_blue:
        tkmsg.showinfo('', 'blue player won the game!')
    else:
        tkmsg.showinfo('', 'Both players are tied')
    menubar.delete(1)
    menubar.delete(1)
    # Recreate the initial array in the same root window.
    number_red = 2
    number_blue = 2
    turn = "red-1"
    create_menubar()
    modify_menu()
    create_grid()


def quit_game():
    """
    This function is used when the user clicks quit on the menubar, it erased the window.
    """
    global root
    if tkmsg.askyesno('Quit the game', 'Are you sure to quit the game?'):
        root.quit()
        

def restart_game():
    """
    This function is used when the user clicks restart on the menubar, it resets the array.
    """
    global number_blue
    global number_red
    global root
    global menubar
    global turn
    if tkmsg.askyesno('Restart the game', 'Are you sure to quit the game?'):
        menubar.delete(1)
        menubar.delete(1)
        # Recreate the initial array in the same root window.
        number_red = 2
        number_blue = 2
        turn = "red-1"
        create_menubar()
        modify_menu()
        create_grid()


def diffuse_color(point):
    """
    We look at the color of the neighbors of moore of a box as a
    parameter to diffuse the color of this one to its neighbors of Moore.
    """
    global number_red
    global number_blue
    global button_dict
    color = button_dict[point].cget('bg')
    # Visit the neighbor of Moore
    for row_index in range(-1, 2):
        for col_index in range(-1, 2):
            x = point[0] + row_index
            y = point[1] + col_index
            if button_dict.get((x, y)):
                if color != button_dict[x, y].cget('bg') != 'yellow':
                    button_dict[x, y].config(bg=color)
                    number_red += (color == 'red') - (color == 'blue')
                    number_blue += (color == 'blue') - (color == 'red')


def modify_menu():
    """
    Update which player should play and if they should select
    their first space or their second. Also refresh the score.
    """
    global turn
    # delete the menu
    menubar.delete(2)
    menu2 = tk.Menu(menubar, tearoff=0)
    # refresh the score
    menu2.add_command(label=f"red : {number_red}", foreground='red')
    menu2.add_command(label=f"blue : {number_blue}", foreground='blue')
    if turn[-1] == "1":
        # update the menu
        menubar.add_cascade(label=f"{turn[:-2]} select the starting point",  foreground=turn[:-2], menu=menu2)
    elif turn[-1] == "2":
        # update the menu
        menubar.add_cascade(label=f"{turn[:-2]} select the destination point", foreground=turn[:-2], menu=menu2)


def update_turn_invalid():
    """
    Return the turn which was updated when the move is not valid.
    """
    global turn
    if turn == "red-2":
        turn = "red-1"
    elif turn == "blue-2":
        turn = "blue-1"


def update_turn_valid():
    """
    Return the turn which was updated when the move is valid.
    """
    global turn
    if turn == "red-2":
        turn = "blue-1"
    elif turn == "blue-2":
        turn = "red-1"


def play(point):
    """
    Manage the smooth running of the game.
    """
    global number_red
    global number_blue
    global button_dict
    global turn
    global sel_point
    color = turn[:-2]
    if (turn[-1] == "1") & (button_dict[point].cget('bg') == turn[:-2]) & move_is_possible():
        sel_point = point
        turn = turn[:-1] + "2"
    elif (turn[-1] == "2") & (button_dict[point].cget('bg') == 'yellow'):
        move_to_do = valid_move(point, sel_point)
        if move_to_do == 2:
            button_dict[point].config(bg=color)
            number_red += (turn[:-2] == 'red')
            number_blue += (turn[:-2] == 'blue')
            update_turn_valid()
            diffuse_color(point)
        elif move_to_do == 1:
            button_dict[point].config(bg=turn[:-2])
            update_turn_valid()
            diffuse_color(point)
            button_dict[sel_point].config(bg='yellow')
        else:
            update_turn_invalid()
            invalid_move()
    if (number_red + number_blue == 100) or (number_blue == 0) or (number_red == 0):
        # One player won
        winner()
    else:
        modify_menu()
    

def create_root():
    """
    Create the root window.
    """
    global root
    root = tk.Tk()
    root.title("Blobwars") 
    root.minsize(450, 300)
    tk.Grid.rowconfigure(root, 0, weight=1)
    tk.Grid.columnconfigure(root, 0, weight=1)


def create_menubar():
    """
    Create the menubar.
    """
    global menubar
    menubar = tk.Menu(root)

    menu1 = tk.Menu(menubar, tearoff=0)
    menu1.add_command(label="Resume")
    menu1.add_command(label="Restart", command=restart_game)
    menu1.add_command(label="Quit", command=quit_game)
    menubar.add_cascade(label="Pause", menu=menu1)

    menu2 = tk.Menu(menubar, tearoff=0)
    menu2.add_command(label=f"red : {number_red}", foreground='red')
    menu2.add_command(label=f"blue : {number_blue}", foreground='blue')

    menubar.add_cascade(label="red select the starting point", foreground='red', menu=menu2)
    # add menubar to the root window
    root.config(menu=menubar)


def create_grid():
    """
    Create a 10x10 grid of buttons inside the parent.
    """
    # Create & Configure parent 
    parent = tk.Frame(root)
    parent.grid(row=0, column=0, sticky=tk.NSEW)
    name = '0'
    color = 'yellow'
    for row_index in range(10):
        tk.Grid.rowconfigure(parent, row_index, weight=1)
        for col_index in range(10):
            tk.Grid.columnconfigure(parent, col_index, weight=1)
            if ((row_index == 0) and (col_index== 0)) or ((row_index == 0) and (col_index== 9)):
                color = 'red'
            elif ((row_index == 9) and (col_index== 0)) or ((row_index == 9) and (col_index== 9)):
                color = 'blue'
            else:
                color = 'yellow'
            # Add button to the dict
            button_dict[(row_index, col_index)] = tk.Button(parent, bg=color, text=name, command=lambda point=(row_index, col_index): play(point), padx=20)
            button_dict[(row_index, col_index)].grid(row=row_index, column=col_index, sticky=tk.NSEW)
            name =  str(int(name) + 1)


def init_table():
    """
    Create the initial array and the root window.
    """
    create_root()
    create_menubar()
    create_grid()
    

# Display the game
init_table()
root.mainloop()
