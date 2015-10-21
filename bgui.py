#! /usr/bin/python3.4
__author__ = 'nicolas'

import tkinter as tk


def toto(e):
    print("toto")


def affiche(e):
    tot = tk.StringVar()
    Fc = tk.Toplevel()
    Fc.grab_set()
    Fc.geometry("100x50")
    index = repbox.curselection()
    nom = repbox.get(index)
    tot.set(nom)
    tot.set(nom)
    tata.config(text=nom)
    print(index, "-", nom)
    t = tk.Label(Fc, textvariable=tot, fg="black")
    t.pack()
    t.bind("<Button-1>", toto)
    tk.Button(Fc, text="Fermer", command=Fc.destroy).pack()


def select_repository():
    FSshkey.pack_forget()
    FRepository.pack(side=tk.TOP, fill=tk.X)


def select_sshkey():
    FRepository.pack_forget()
    FSshkey.pack(side=tk.TOP, fill=tk.X)


def draw_menu():
    fr = tk.Frame(Win, bg="#b0b0ff", borderwidth=3, width=250, height=200)
    fr.pack(side=tk.TOP, fill=tk.X, padx=30, pady=10)
    tk.Button(fr, text="Repository", command=select_repository).pack(side=tk.LEFT)
    tk.Button(fr, text="SSHKey", command=select_sshkey).pack(side=tk.RIGHT)


def draw_repository():
    frame = tk.Frame(FRepository, bg="#b0b0ff", borderwidth=3, width=250, height=200)
    frame.pack(side=tk.LEFT)
    repbox = tk.Listbox(frame)
    ybar = tk.Scrollbar(frame)
    ybar.config(command=repbox.yview)
    xbar = tk.Scrollbar(frame)
    xbar.config(command=repbox.xview, orient=tk.HORIZONTAL)
    repbox.config(yscrollcommand=ybar.set, xscrollcommand=xbar.set)
    ybar.pack(side=tk.RIGHT, fill=tk.Y)
    xbar.pack(side=tk.BOTTOM, fill=tk.X)
    repbox.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
    repbox.bind("<B1-ButtonRelease>", affiche)
    for j in range(0, 100):
        repbox.insert(tk.END, j)
    repbox.insert(tk.END, "Jean ive de la mole fesse 42 eme régiment")
    return repbox

Win = tk.Tk()
# define size and position of the window
width = 400
height = 250
xpos = int(Win.winfo_screenwidth() / 2 - (width / 2))
ypos = int(Win.winfo_screenheight() / 2 - (height / 2))
sr = str(width) + "x" + str(height) + "+" + str(xpos) + "+" + str(ypos)
Win.geometry(sr)

# Menu bar
# menu1 = tk.Menu(Win)
# fichier = tk.Menu(menu1, tearoff=False)
# menu1.add_cascade(label="Fichier", menu=fichier)
# fichier.add_command(label="Quit", command=Win.quit)
# cascad = tk.Menu(menu1)

# Body
draw_menu()
FRepository = tk.Frame(Win, bg="#ffbbbb")
FSshkey = tk.Frame(Win, bg="#ffbbbb")

repbox = draw_repository()

tk.Button(FRepository, text="Create").pack(side=tk.TOP, pady=10)
tata = tk.LabelFrame(FRepository, text="None", labelanchor="n")
tata.pack(anchor="w", side=tk.TOP, padx=10, fill=tk.X)
for i in ["ACL", "Clone", "Info"]:
    tk.Button(tata, text=i).pack(side=tk.TOP, pady=5)

for i in ["Upload", "Delete"]:
    tk.Button(FSshkey, text=i).pack(side=tk.TOP, pady=5)

FRepository.pack(side=tk.TOP, fill=tk.X)
# Win.config(menu=menu1)

# Loop
Win.mainloop()