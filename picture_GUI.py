import tkinter as tk #大小寫要注意,如果小寫不行就改大寫
from tkinter import *
from PIL import  ImageTk, Image
import random
import window as wd

def first():
    img_right=ImageTk.PhotoImage(Image.open('Candlestick.png')) #取得圖片
    label_right.imgtk=img_right #換圖片
    label_right.config(image=img_right) #換圖片

def second():
    s1 = random.randint(1, 4)
    img_right = ImageTk.PhotoImage(Image.open('Vol.png'))
    label_right.imgtk=img_right
    label_right.config(image = img_right)

def third():
    s1 = random.randint(1, 4)
    img_left = ImageTk.PhotoImage(Image.open('close.png'))
    label_left.imgtk=img_left
    label_left.config(image = img_left)

def fourth():
    s1 = random.randint(1, 4)
    img_left = ImageTk.PhotoImage(Image.open('high.png'))
    label_left.imgtk=img_left
    label_left.config(image = img_left)

def fifth():
    s1 = random.randint(1, 4)
    img_left = ImageTk.PhotoImage(Image.open('low.png'))
    label_left.imgtk=img_left
    label_left.config(image = img_left)

# def sixth():
#     s1 = random.randint(1, 4)
#     img_left = ImageTk.PhotoImage(Image.open('psl.png'))
#     label_left.imgtk=img_left
#     label_left.config(image = img_left)

#創建一個視窗
top = tk.Tk() 

#視窗名稱
top.title('股票預測') 
#'寬x高+右移+下移'
top.geometry('880x1020+400+200') 

#開啟照片
img= ImageTk.PhotoImage(Image.open('stock.png'))
img2= ImageTk.PhotoImage(Image.open('stock.png'))

#用label來放照片
label_right= tk.Label(top,height=480,width=640,bg ='gray94',fg='blue',image = img) 
label_left= tk.Label(top,height=480,width=640,bg ='gray94',fg='blue',image = img2) 

#按鈕
button_1 = tk.Button(top,text = 'K線',bd=4,height=2,width=10,bg ='gray94',command =first)
button_2 = tk.Button(top,text = '成交量',bd=4,height=2,width=10,bg ='gray94',command =second)

button_3 = tk.Button(top,text = '收盤價',bd=4,height=2,width=10,bg ='gray94',command =third)
button_4 = tk.Button(top,text = '最高價',bd=4,height=2,width=10,bg ='gray94',command =fourth)
button_5 = tk.Button(top,text = '最低價',bd=4,height=2,width=10,bg ='gray94',command =fifth)
# button_6 = tk.Button(top,text = '七日低價',bd=4,height=2,width=10,bg ='gray94',command =sixth)

#位置
label_right.grid(row=1,column=0,padx=50, pady=20, sticky="nw") 
button_1.grid(row=1, column=0, padx=750, pady=160, sticky="nw")  
button_2.grid(row=1, column=0, padx=750, pady=300, sticky="nw") 

label_left.grid(row=1,column=0,padx=50, pady=520, sticky="nw") 
button_3.grid(row=1, column=0, padx=750, pady=650, sticky="nw")  
button_4.grid(row=1, column=0, padx=750, pady=780, sticky="nw") 
button_5.grid(row=1, column=0, padx=750, pady=910, sticky="nw") 
# button_6.grid(row=1, column=0, padx=750, pady=920, sticky="nw") 

top.mainloop() #執行視窗