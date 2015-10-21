#!/usr/bin/python3.4

__author__ = 'nicolas'

import subprocess
import tkinter as tk
from tkinter import messagebox
import hashlib
import ast


def read_file(path):
    """
    Lecture du fichier
    :param path: chemin vers le fichier
    :return: liste
    """
    lst = []
    try:
        with open(path) as f:
            for data in f:
                if len(data.split(' ')) != 0:
                    lst.append(data.split(' ')[0])
        return lst
    except IndexError:
        print("Can't open file")


class scroll:
    frame = None
    __box = None

    def __init__(self, height, box = None):
        self.frame = tk.Frame()
        self.__box = tk.Listbox(self.frame, selectmode=tk.SINGLE, height=height)
        # bbox = tk.Listbox(self.frame, selectmode=tk.SINGLE, height=height)
        ybar = tk.Scrollbar(self.frame)
        ybar.config(command=self.__box.yview)
        xbar = tk.Scrollbar(self.frame)
        xbar.config(command=self.__box.xview, orient=tk.HORIZONTAL)
        self.__box.config(yscrollcommand=ybar.set, xscrollcommand=xbar.set)
        ybar.pack(side=tk.RIGHT, fill=tk.Y)
        xbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.__box.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.__box.bind("<B1-ButtonRelease>", lambda e: self.__update(box))

    def __update(self, box):
        if box is not None:
            box.config(text=self.__box.get(self.__box.curselection()))

    def update(self, lst):
        lst.sort()
        self.__box.delete(0, tk.END)
        if lst is not None:
            for j in lst:
                self.__box.insert(tk.END, j)

    def get_elem(self):
        key = self.__box.curselection()
        if len(key) > 0:
            return self.__box.get(key)
        return None


class GBlih:
    Win = tk.Tk()
    user = tk.StringVar()
    token = tk.StringVar()
    __RepFrame = tk.Frame(Win)
    __SshFrame = tk.Frame(Win)
    scroll_rep = None
    scroll_ssh = None

    def __init__(self):
        self.Win.resizable(width=False, height=False)
        MenuOpt = 0

    def __get_size(self, width, height):
        xpos = int(self.Win.winfo_screenwidth() / 2 - (width / 2))
        ypos = int(self.Win.winfo_screenheight() / 2 - (height / 2))
        sr = str(width) + "x" + str(height) + "+" + str(xpos) + "+" + str(ypos)
        return sr

    def __resize(self, width, height):
        sr = self.__get_size(width, height)
        self.Win.geometry(sr)

    def __exec_command(self, cmd):
        cmd = "blih -u " + self.user.get() + " -t " + self.token.get() + " " + cmd
        print(cmd)
        err, msg = subprocess.getstatusoutput(cmd)
        if err != 0:
            return None
        ret = [x for x in msg.split(sep='\n')]
        return ret

    def __draw_menu(self):
        fr = tk.Frame(self.Win, bg="#b0b0ff", borderwidth=3, width=250, height=200)
        fr.pack(side=tk.TOP, fill=tk.X, padx=30, pady=10)
        tk.Button(fr, text="Repository", command=lambda: self.switch(0)).pack(side=tk.LEFT)
        tk.Button(fr, text="SSHKey", command=lambda: self.switch(1)).pack(side=tk.RIGHT)

    def __delete_repository(self):
        rep = self.scroll_rep.get_elem()
        if rep is None:
            return
        answer = messagebox.askyesno("Suppression " + rep, "Voulez vous supprimer le répertoire " + rep + " ?")
        if answer is True:
            self.__exec_command('repository delete ' + rep)
            print("Here i'm deleting " + rep)
            self.scroll_rep.update(self.__exec_command('repository list'))

    def win_acl(self):
        lusr = read_file('/home/nicolas/.acl_user')
        print(lusr)

    def __info(self):
        rep = self.scroll_rep.get_elem()
        if rep is None:
            return
        ret = self.__exec_command('repository info ' + rep)
        if ret is not None:
            d = ast.literal_eval(ret[0])
            info = tk.Toplevel(self.Win, padx=20, pady=20)
            info.title("Info " + rep)
            info.grab_set()
            j = 0
            key = list(d.keys())
            key.sort()
            for i in key:
                tk.Label(info, text=i + ':').grid(row=j, column=0, sticky=tk.W)
                tk.Label(info, text=d[i]).grid(row=j, column=1, sticky=tk.W)
                j += 1
            tk.Button(info, text='Ok', command=info.destroy).grid(row=j, column=0, columnspan=2, pady=(15, 0))
            info.update()
            info.geometry(self.__get_size(info.winfo_width(), info.winfo_height()))

    def __sub_create(self, val, win):
        if val != '':
            self.__exec_command("repository create " + val)
            self.scroll_rep.update(self.__exec_command('repository list'))
            win.destroy()

    def __create(self):
        repo = tk.StringVar()
        repo.set('')
        create = tk.Toplevel(self.Win, padx=20, pady=20)
        create.title("Create repository")
        create.grab_set()
        tk.Entry(create, textvariable=repo).pack()
        tk.Button(create, text='Create', command=lambda: self.__sub_create(repo.get(), create)).pack(pady=(10, 0))

    def __repository(self):
        box = tk.LabelFrame(self.__RepFrame, text="None", labelanchor="n")
        self.scroll_rep = scroll(14, box)
        self.scroll_rep.frame.pack(side=tk.LEFT, padx=10, anchor='nw', in_=self.__RepFrame)
        self.scroll_rep.update(self.__exec_command('repository list'))
        tk.Button(self.__RepFrame, text="Create", command=self.__create).pack(side=tk.TOP, pady=10)
        box.pack(anchor="w", side=tk.TOP, padx=10, fill=tk.X)
        tk.Button(box, text='ACL', command=self.win_acl).pack(side=tk.TOP, pady=5)
        tk.Button(box, text='Clone').pack(side=tk.TOP, pady=5)
        tk.Button(box, text='Info', command=self.__info).pack(side=tk.TOP, pady=5)
        tk.Button(box, text='Delete', command=self.__delete_repository).pack(side=tk.TOP, pady=5)

    def __info_ssh(self, lst):
        rep = self.scroll_ssh.get_elem()
        if rep is None:
            return
        info = tk.Toplevel(self.Win, padx=20, pady=20)
        info.title("Info sshkey" + rep)
        info.grab_set()
        for i in range(0, len(lst)):
            elem = lst[i].split(' ')
            if elem[-1] == rep:
                for j in elem:
                    tk.Label(info, text=j).pack(side=tk.TOP)
        tk.Button(info, text='Ok', command=info.destroy).pack(side=tk.TOP)
        info.update()
        info.geometry(self.__get_size(info.winfo_width(), info.winfo_height()))

    def __sshkey(self):
        box = tk.LabelFrame(self.__SshFrame, text="None", labelanchor="n")
        self.scroll_ssh = scroll(14, box)
        self.scroll_ssh.frame.pack(side=tk.LEFT, padx=10, anchor='nw', in_=self.__SshFrame)
        ret = self.__exec_command('sshkey list')
        seg = list()
        for i in range(0, len(ret)):
            seg.insert(-1, ret[i].split(' ')[-1])
        self.scroll_ssh.update(seg)
        tk.Button(self.__SshFrame, text='Upload').pack(side=tk.TOP, pady=5)
        box.pack(anchor="w", side=tk.TOP, padx=10, fill=tk.X)
        tk.Button(box, text='Info', command=lambda: self.__info_ssh(ret)).pack(side=tk.TOP, pady=5)
        tk.Button(box, text='Delete').pack(side=tk.TOP, pady=5)

    def switch(self, n):
        if n == 0:
            self.__RepFrame.pack(fill=tk.BOTH, expand=True)
            self.__SshFrame.pack_forget()
        else:
            self.__RepFrame.pack_forget()
            self.__SshFrame.pack(fill=tk.X)

    def __exec_login(self, LogFrame, wrong):
        st = hashlib.sha512(bytes(self.token.get(), 'utf8')).hexdigest()
        # st = bytes(hashlib.sha512(bytes(self.token.get(), 'utf8')).hexdigest(), 'utf8')
        self.token.set(st)
        if self.__exec_command('whoami') is None:
            self.token.set('')
            wrong.set('Wrong username or password')
        else:
            self.__resize(400, 300)
            LogFrame.pack_forget()
            self.__draw_menu()
            self.__repository()
            self.__sshkey()
            self.switch(0)
            self.Win.title("Blih Graphic")

    def login(self):
        self.__resize(350, 110)
        wrong = tk.StringVar()
        self.Win.title("Blih Graphic - Login")
        LogFrame = tk.Frame(self.Win)
        LogFrame.pack(anchor='center', expand=True, padx=20, pady=(5, 20))
        tk.Label(LogFrame, textvariable=wrong, fg='#ff2222').grid(row=0, column=0, columnspan=4)
        tk.Label(LogFrame, text='Login :').grid(row=1, column=0, sticky=tk.W)
        tk.Label(LogFrame, text='Password :').grid(row=2, column=0, sticky=tk.W)
        tk.Entry(LogFrame, textvariable=self.user).grid(row=1, column=1, pady=5, ipady=2)
        password = tk.Entry(LogFrame, textvariable=self.token, show='*')
        password.bind('<Return>', lambda e: self.__exec_login(LogFrame, wrong))
        password.grid(row=2, column=1, ipady=2)
        tk.Button(LogFrame, text="login", command=lambda: self.__exec_login(LogFrame, wrong)).grid(row=1, column=2, rowspan=2, columnspan=2, padx=10)



t = GBlih()
t.login()
t.Win.mainloop()