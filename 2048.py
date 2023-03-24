"""
auteur:         Athos Cruchet
date:           03.02.2023
version:        3.0
description:    jeux 2048
"""
# importation
from tkinter import *
import random
import copy
from tkinter import messagebox

#variables
width = 300
height = 500
espace_un = x = 20
espace_deux = y = 75
intervalex = 55
nmove = 0
first2048 = 1
score = 0

#création et caractéristiques de la fenetre (aide carlos)
windows = Tk()
windows.title("2048")
screenwidth = windows.winfo_screenwidth()
screenheight = windows.winfo_screenheight()
x = (screenwidth/2) - (width / 2)
y = (screenheight/2) - (height / 2)
windows.geometry("%dx%d+%d+%d" % (width, height, x, y))
windows.config(background="#FFE599")


# affichage/ espacement entre les frames

espace_frame = Frame(windows,
background="#FFE599", height=20, width=160)
espace_frame.pack()


grosse_frame = Frame(windows,
background="#FFE599", height=20, width=300)
grosse_frame.pack()


logo_frame = Frame(grosse_frame,
background="#FFE599", height=20, width=160)
logo_frame.pack(side=LEFT)


espace2_frame = Frame(grosse_frame,
background="#FFE599", height=20, width=120)
espace2_frame.pack(side=LEFT)


top_frame = Frame(grosse_frame,
background="#FFE599", height=20, width=120)
top_frame.pack(side=LEFT)


logo_label = Label(logo_frame,
text="2048", background="#FFE599", font=("arial", 15))
logo_label.pack()


score_label = Label(top_frame,
text="score", background="#FFE599", font=("arial", 15))
score_label.pack()


jeux_frame = Frame(windows,
background="#FFE599", height=250, width=250)
jeux_frame.pack(pady=60)


# ici sont representées les différentes couleurs de mon jeux. (idee de Tiago)
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
# tabbleau des valeurs pour la fonction tasse 4
numbers = [[0, 0, 4, 8],
           [0, 0, 0, 0],
           [0, 0, 0, 2048],
           [0, 0, 0, 0]]

labels = [[None, None, None, None],
          [None, None, None, None],
          [None, None, None, None],
          [None, None, None, None]]

for line in range(len(numbers)):
    for col in range(len(numbers[line])):
        labels[line][col] = Label(jeux_frame, text="", width=6, height=3, borderwidth=1, relief="solid", font=("Arial", 10))
        labels[line][col].place(x=15 + intervalex * col, y=15 + intervalex * line)

# cette fonction génere une tuile de 2 ou 4 dans une case vide
def generate():
    candidates = []
    for line in range(len(numbers)):
        for col in range(len(numbers[line])):
            if numbers[line][col] == 0:
                candidates.append((line, col))
    if candidates:
        line, col = random.choice(candidates)
        numbers[line][col] = random.choice([2, 4])

    # fonction qui permet de relancer une partie avec un boutton
def new_game():
    global numbers,score
    numbers = [[0, 0, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0]]
    score = 0
    score_label.config(text=f"Score\n {score}")

    # fait apparaitre deux tuile de deux apres une nouvelle partie
    for i in range(2):
        line, col = random.randint(0, 3), random.randint(0, 3)
        while numbers[line][col] != 0:
            line, col = random.randint(0, 3), random.randint(0, 3)
        numbers[line][col] = 2
    display()

button_newgame = Button(windows, text="nouvelle partie",background= '#FFE599', command=new_game)
button_newgame.pack()

#focntion qui actualise la fenêtre
def display():
    for line in range(len(numbers)):
        for col in range(len(numbers[line])):
            if numbers[line][col] == 0:
                labels[line][col].config(text="", bg="#FFFFFF")
            else:
                labels[line][col].config(text=numbers[line][col], bg=hex_colors[numbers[line][col]])
#fonction qui permet de tasser et d'addicionner les chiffres entre eux
def tasse_4(a, b, c, d,bscore):
    global score
    # Enlever les zéros s'il y a quelque chose à droite, de droite à gauche
    nmove = 0
    if c == 0 and d > 0:
        c, d = d, 0
        nmove += 1

    if b == 0 and c > 0:
        b, c, d = c, d, 0
        nmove += 1

    if a == 0 and b > 0:
        a, b, c, d = b, c, d, 0
        nmove += 1

    if a == b and b > 0:
        a, b, c, d = a*2, c, d, 0
        nmove += 1
        if bscore :
            score+=a

    if b == c and c > 0:
        b, c, d = b*2, d, 0
        nmove += 1
        if bscore:
            score+=b

    if c == d and c > 0:
        c, d = c*2, 0
        nmove += 1
        if bscore:
            score+=c

    score_label.config(text=f"Score\n {score}")
    print(score)
    # ici on retourne les cinq valeurs en un tableau
    # tableau temporaire de fin (aide carlos + esteban)
    temp = [a, b, c, d, nmove]
    return temp

#cette fonction permet de réaliser un test afin de savoir s'il existe encore un mouvement possible. si non, la partie est perdue.
def perdre():
    global numbers
    partie_perdue = 0
    numbers_2 = copy.deepcopy(numbers)

    # pour la droite (aide fakime)
    for line in range(len(numbers)):
        [numbers_2[line][3], numbers_2[line][2], numbers_2[line][1], numbers_2[line][0], n] = tasse_4(numbers_2[line][3], numbers_2[line][2], numbers_2[line][1], numbers_2[line][0], False)
        partie_perdue += n
    # pour la gauche
    for line in range(len(numbers)):
        [numbers_2[line][0], numbers_2[line][1], numbers_2[line][2], numbers_2[line][3], n] = tasse_4(numbers_2[line][0], numbers_2[line][1], numbers_2[line][2], numbers_2[line][3], False)
        partie_perdue += n
    # vers le haut
    for col in range(len(numbers)):
        [numbers_2[0][col], numbers_2[1][col], numbers_2[2][col], numbers_2[3][col], n] = tasse_4(numbers_2[0][col], numbers_2[1][col], numbers_2[2][col], numbers_2[3][col], False)
        partie_perdue += n
    # vers le bas
    for col in range(len(numbers)):
        [numbers_2[3][col], numbers_2[2][col], numbers_2[1][col], numbers_2[0][col], n] = tasse_4(numbers_2[3][col], numbers_2[2][col], numbers_2[1][col], numbers_2[0][col], False)
        partie_perdue += n
    #message de fin de partie (perdue)
    if partie_perdue == 0:
        messagebox.showinfo("Perdu!", "Vous avez perdu")


#cette fonction permet de reconnaitre une case contenant un 2048. Si oui, la partie est gagnée + message de victoire
def gagner():
    global first2048
    for line in range(len(numbers)):
        for col in range(len(numbers[line])):
            if first2048 == 1:
                if numbers[line][col] == 2048:
                    messagebox.showinfo("2048", "Vous avez gagné!")
                    first2048 = 0
                    display()


#cette fonction possibilite de bouger vers la droite. la fonction réalise également deux test (gagné/perdu) et compte le nombre de mouvement et m'affiche ce nombre.
def move_right (event):
    global nmove
    totmove = 0
    n = 0
    for line in range(len(numbers)):
        [numbers[line][3], numbers[line][2], numbers[line][1], numbers[line][0], n] = tasse_4(numbers[line][3], numbers[line][2], numbers[line][1], numbers[line][0],True)
        totmove += n;
    if totmove > 0:
        generate()
    display()
    gagner()
    perdre()
    print(totmove)


#cette fonction possibilite de bouger vers la gauche. la fonction réalise également deux test (gagné/perdu) et compte le nombre de mouvement et m'affiche ce nombre.
def move_left(event):
    global nmove
    totmove = 0
    n = 0
    for line in range(len(numbers)):
        [numbers[line][0], numbers[line][1], numbers[line][2], numbers[line][3], n] = tasse_4(numbers[line][0], numbers[line][1], numbers[line][2], numbers[line][3],True)
        totmove += n;
    if totmove > 0:
        generate()
    display()
    gagner()
    perdre()
    print(totmove)


#cette fonction possibilite de bouger vers le bas. la fonction réalise également deux test (gagné/perdu) et compte le nombre de mouvement et m'affiche ce nombre.
def move_up(event):
    global nmove
    totmove = 0
    n = 0
    for col in range(len(numbers)):
        [numbers[0][col], numbers[1][col], numbers[2][col], numbers[3][col], n] = tasse_4(numbers[0][col], numbers[1][col], numbers[2][col], numbers[3][col], True)
        totmove += n;
    if totmove > 0:
        generate()
    display()
    gagner()
    perdre()
    print(totmove)


#cette fonction possibilite de bouger vers le haut. la fonction réalise également deux test (gagné/perdu) et compte le nombre de mouvement et m'affiche ce nombre.
def move_down(event):
    global nmove
    totmove = 0
    n = 0
    for col in range(len(numbers)):
        [numbers[3][col], numbers[2][col], numbers[1][col], numbers[0][col], n] = tasse_4(numbers[3][col], numbers[2][col], numbers[1][col], numbers[0][col],True)
        totmove += n;
    if totmove > 0:
        generate()
    display()
    gagner()
    perdre()
    print(totmove)

#assignation des touches "a" "w" "d" "s"
windows.bind("a", move_left)
windows.bind("d", move_right)
windows.bind("w", move_up)
windows.bind("s", move_down)

display()
windows.mainloop()