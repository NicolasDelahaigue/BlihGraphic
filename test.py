#! /usr/bin/python3.4
__author__ = 'nicolas'
import tkinter as tk


class scroll:
    frame = None
    __box = []

    def __init__(self, height, box = None, ):
        self.frame = tk.Frame()
        self.__box.append(tk.Listbox(self.frame, selectmode=tk.SINGLE, height=height))
        # bbox = tk.Listbox(self.frame, selectmode=tk.SINGLE, height=height)
        ybar = tk.Scrollbar(self.frame)
        ybar.config(command=self.__box[0].yview)
        xbar = tk.Scrollbar(self.frame)
        xbar.config(command=self.__box[0].xview, orient=tk.HORIZONTAL)
        self.__box[0].config(yscrollcommand=ybar.set, xscrollcommand=xbar.set)
        ybar.pack(side=tk.RIGHT, fill=tk.Y)
        xbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.__box[0].pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.__box[0].bind("<B1-ButtonRelease>", lambda e: self.__update(box))

    def __update(self, box):
        if box is not None:
            box.config(text=self.__box.get(self.__box.curselection()))

    def update(self, lst, index):
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

sc = scroll()