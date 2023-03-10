"""
auteur:         Athos Cruchet
date:           03.02.2023
version:        2.0
description:    jeux 2048
"""
from tkinter import *

#variables
width = 300
height = 500
espace_un = x = 20
espace_deux = y = 75
intervalex = 55
nmove = 0

#création et caractéristiques de la fenetre (aide carlos)
windows = Tk()
windows.title("2048")
screenwidth = windows.winfo_screenwidth()
screenheight = windows.winfo_screenheight()
x = (screenwidth/2) - (width / 2)
y = (screenheight/2) - (height / 2)
windows.geometry("%dx%d+%d+%d" % (width, height, x, y))
windows.config(background="#FFE599")

#affichage
espace_frame = Frame(windows, background="#FFE599", height=20, width=160)
espace_frame.pack()
grosse_frame = Frame(windows, background="#FFE599", height=20, width=300)
grosse_frame.pack()
logo_frame = Frame(grosse_frame, background="#FFE599", height=20, width=160)
logo_frame.pack(side=LEFT)
espace2_frame = Frame(grosse_frame, background="#FFE599", height=20, width=120)
espace2_frame.pack(side=LEFT)
top_frame = Frame(grosse_frame, background="#FFE599", height=20, width=120)
top_frame.pack(side=LEFT)

logo_label = Label(logo_frame, text="2048", background="#FFE599", font=("arial", 15))
logo_label.pack()
score_label = Label(top_frame, text="score", background="#FFE599", font=("arial", 15))
score_label.pack()
top_label = Label(top_frame, text="top", background="#FFE599", font=("arial", 15))
top_label.pack()

jeux_frame = Frame(windows, background="#FFE599", height=250, width=250)
jeux_frame.pack(pady=60)

# tableau des couleurs (idee de Tiago)
hex_colors = {
             0: "#FFFFFF",
             2: "#444444",
             4: "#9FC5F8",
             8: "#2B78E4",
             16: "#00FFFF",
             32: "#93C47D",
             64: "#009E0F",
             128: "#FFD966",
             256: "#FF9900",
             512: "#CF2A27",
             1024: "#9900FF",
             2048: "#FF00FF",
             4096: "#4C1130",
             8192: "#A64D79",
}

# définitions
numbers = [[0, 2, 2, 2], [4, 4, 4, 4], [8, 8, 8, 8], [4096, 8192, 0, 0]]
labels = [[None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None]]
for line in range(len(numbers)):
    for col in range(len(numbers[line])):
        labels[line][col] = Label(jeux_frame, text="", width=6, height=3, borderwidth=1, relief="solid", font=("Arial", 10))
        labels[line][col].place(x=15 + intervalex * col, y=15 + intervalex * line)

def display():
    for line in range(len(numbers)):
        for col in range(len(numbers[line])):
            if numbers[line][col] == 0:
                labels[line][col].config(text="", bg="#FFFFFF")
            else:
                labels[line][col].config(text=numbers[line][col], bg=hex_colors[numbers[line][col]])

def tasse_4(a, b, c, d):
    #oter les 0 s'il y a qq chose à droite, depuis la droit
    nmove = 0
    if (c == 0 and d > 0):
        c, d = d, 0
        nmove += 1

    if (b==0 and c>0):
        b, c, d = c, d, 0
        nmove += 1

    if (a==0 and b>0):
        a, b, c, d = b, c, d, 0
        nmove += 1

    #fusionner deux par deux depuis la gauche
    if a == b and b > 0:
        a, b, c, d = a+b, c, d, 0
        nmove += 1

    if (b==c and c>0):
        b, c, d = b+c, d, 0
        nmove += 1

    if (c==d and d>0):
        c, d = c+d, 0
        nmove += 1

    print(nmove)

    # ici on retourne les cinq valeurs en un tableau
    # tableau temporaire de fin (aide carlos + esteban)
    temp = [a, b, c, d, nmove]
    return temp

def move_right (event):
    totmove = 0
    n = 0
    for line in range(len(numbers)):
        [numbers[line][3], numbers[line][2], numbers[line][1],
         numbers[line][0], n] = tasse_4(numbers[line][3], numbers[line][2], numbers[line][1], numbers[line][0])
        totmove += n;
        display()
    print(totmove)

def move_left(event):
    totmove = 0
    n = 0
    for line in range(len(numbers)):
        [numbers[line][0], numbers[line][1], numbers[line][2],
         numbers[line][3], n] = tasse_4(numbers[line][0], numbers[line][1], numbers[line][2], numbers[line][3])
        totmove += n;
        display()
        print(totmove)

def move_up(event):
    totmove = 0
    n = 0
    for col in range(len(numbers)):
        [numbers[0][col], numbers[1][col], numbers[2][col],
         numbers[3][col], n] = tasse_4(numbers[0][col], numbers[1][col], numbers[2][col], numbers[3][col])
        totmove += n;
        display()
        print(totmove)

def move_down(event):
    totmove = 0
    n = 0
    for col in range(len(numbers)):
        [numbers[3][col], numbers[2][col], numbers[1][col],
         numbers[0][col], n] = tasse_4(numbers[3][col], numbers[2][col], numbers[1][col], numbers[0][col])
        totmove += n;
        display()
        print(totmove)

#boutton new game
def new_game():
    global numbers
    numbers = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    display()

button_nouveau = Button(command=new_game, text="nouveau", background="#FFE599")
button_nouveau.pack()

#assignation des touches "a" "w" "d" "s"
windows.bind("a", move_left)
windows.bind("d", move_right)
windows.bind("w", move_up)
windows.bind("s", move_down)

display()
windows.mainloop()