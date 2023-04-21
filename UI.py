#!/usr/bin/env python3
# coding: utf-8
# File: answer_search.py
# Author: zlh<994182204@mail.dlut.edu.cn>
# Date: 23-4-21


import tkinter as tk
from tkinter import *
import time
from chatbot_graph import *


face_1 = tk.Tk()
handler = ChatBotGraph()
timestr = time.strftime("%H:%M:%S")  # 获取当前的时间并转化为字符串

# 设计函数
def getTextInput():
    question = text1.get("1.0", tk.END)  # 获取文本输入框的内容
    if question == '\n':
        print("No input")
        text2.insert(tk.END, "请重新输入")
    else:
        print(question)
        # 在尾端加入文本
        answer = handler.chat_main(question)
        text2.insert(tk.END, '-----------------查询时间：'+timestr+'------------------------'+ '\n'+answer + '\n') # 获取时间

def clean():
    text1.delete('0.0', tk.END)
    text2.delete('0.0', tk.END)

def explain_face_2():  # 使用说明窗口
    face_2_explain = Tk()
    face_2_explain.geometry('500x250')
    face_2_explain.title('使用说明')
    f = open('./music/QA.txt', 'r', encoding='utf-8')
    text3 = tk.Text(face_2_explain, height=17)
    text3.pack()
    for i in range(10):
        line = f.readline()
        text3.insert(tk.END,'-----------------------------------'+ '\n'+line)

    face_2_explain.mainloop()
    f.close()

# 基本界面布局
face_1.title("在线音乐查询系统")
face_1.geometry('800x700')  # 窗口大小
photo = tk.PhotoImage(file="./img/1.gif")

tk.Label(face_1, bd=10, text='欢迎使用在线音乐查询系统', font=('微软雅黑', 20)).pack()
tk.Label(face_1, image=photo).place(x=200, y=520)

label_1 = tk.Label(face_1, text='输入问题后开始提问>>>>>>>', font=('微软雅黑', 10))
label_1.place(x=150, y=75)

button_1 = tk.Button(face_1, text='开始', font=('微软雅黑', 10), width=15, command=getTextInput)
button_1.place(x=350, y=75)
button_2 = tk.Button(face_1, text='清除', font=('微软雅黑', 10), width=15, command=clean)
button_2.place(x=500, y=75)

tk.Label(face_1, bd=10, text='输入问句', font=("楷体", 13, "bold")).place(x=100, y=110)
tk.Label(face_1, bd=10, text='回答', font=("楷体", 13, "bold")).place(x=100, y=220)

text1 = tk.Text(face_1, bd=10, height=3)
text1.pack()
text1.place(x=100, y=150)

text2 = tk.Text(face_1, bd=10, height=20)
text2.pack()
text2.place(x=100, y=280)

menu_bar = Menu(face_1)
menu_bar.add_command(label='使用说明', command=explain_face_2)
face_1.config(menu=menu_bar)  # 根菜单记录

face_1.mainloop()
