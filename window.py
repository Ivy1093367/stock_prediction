# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageTk, Image
import LSTM_Prediction_new as LS

window=tk.Tk()
window.title('股票預測')
window.geometry('800x780+400+200') #第1個加號是距離屏幕左邊的寬，第2個加號是距離屏幕頂部的高
#圖片
photo=ImageTk.PhotoImage(file="snum.jpg")
imageLab=tk.Label(window, image=photo).grid(row=0,column=0,columnspan= 2,padx= 200,pady= 0, sticky="nw")
#imageLab=tk.Label(window, image=photo, justify=tk.CENTER).grid(row= 0,column= 0,rowspan= 2,padx= 0,pady= 0)
#文字輸入欄
def entry_action():
    get = input1.get()+"/"+input2.get() #get()取得輸入
    output.set(get) #set()顯示輸出

    # LS.name=input1.get()
    # LS.company=input2.get()
    # LS.run()

input1 = tk.StringVar()
input2 = tk.StringVar()
enlabel1 = tk.Label(window, text='股票編號:')
enlabel1.grid(row=0,column=0, padx= 250, pady= 620, sticky="nw")
entry_1 = tk.Entry(window, width = 40, textvariable = input1)
entry_1.grid(row=0,column=0, padx= 330, pady= 620, sticky="nw")
enlabel2 = tk.Label(window, text='股票名稱:')
enlabel2.grid(row=0,column=0, padx= 250, pady= 650, sticky="nw")
entry_2 = tk.Entry(window, width = 40, textvariable = input2)
entry_2.grid(row=0,column=0, padx= 330, pady= 650, sticky="nw")
# entry_2.grid(row=4,column=1)

# button_input = tk.Button(window, text = "Enter", command = entry_action)
# button_input.grid(row=5,column=0)

output = tk.StringVar()
label_2 = tk.Label(window, width = 40, textvariable = output) #textvariable 設定文字變數，如果變量被修改，標籤的文本也會自動更新
label_2.grid(row=5,column=1)

# def button_event():
#      print(mycombobox.current(), mycombobox.get())
#      buttonText.set(mycombobox.get())
#      #buttonText.set('idx:' + str(mycombobox.current()) + ', ' + mycombobox.get())

# comboboxList = ['2022/6/20','2022/5/20','2022/4/20','2022/3/20','2022/2/20','2022/1/20',
#                 '2021/12/20','2021/11/20','2021/10/20','2021/9/20','2021/8/20','2021/7/20']
# colabel = tk.Label(window, text='欲查看日期:')
# colabel.grid(row=6,column=0)
# mycombobox = ttk.Combobox(window, state='readonly')
# mycombobox['values'] = comboboxList

# mycombobox.grid(row=6,column=1)
# mycombobox.current(0)

# buttonText =  tk.StringVar()
# buttonText.set('Go')
# tk.Button(window, textvariable=buttonText, command=button_event).grid(row=7,column=1)

colabel2 = tk.Label(window, text='欲查看日期:')
colabel2.grid(row=0,column=0, padx= 250, pady= 680, sticky="nw")
def combobox_selected(event):
    get = input1.get()+"/"+input2.get() #get()取得輸入
    output.set(get) #set()顯示輸出
    LS.parameter=input1.get()
    LS.companyname=input2.get()
    LS.end_time=comboboxText.get()
    LS.run()
    # print(input1.get())
    # print(input2.get())
    # print(comboboxText.get())     
    # print(mycombobox2.current(), comboboxText.get())
    labelText.set(comboboxText.get())


comboboxText = tk.StringVar()

mycombobox2 = ttk.Combobox(window, textvariable=comboboxText, state='readonly')
mycombobox2['values'] = ['2022/6/20','2022/5/20','2022/4/20','2022/3/20','2022/2/20','2022/1/20',
                        '2021/12/20','2021/11/20','2021/10/20','2021/9/20','2021/8/20','2021/7/20']
mycombobox2.grid(row=0,column=0, padx= 330, pady= 680, sticky="nw")
mycombobox2.current()
mycombobox2.bind('<<ComboboxSelected>>', combobox_selected)

#底下不用看(大概)
labelText = tk.StringVar()
colabel3 = tk.Label(window, textvariable=labelText, height=3, font=('Arial', 10))
colabel3.grid(row=9,column=1)

columns = [ '現在時間', '開盤價', '最高價', '最低價', '收盤價', '調整後收盤價', '成交量' ]
table = ttk.Treeview(
        master =window,   #父容器
        height=10,   #表格顯示的行數,height行
        columns=columns,   #顯示的列
        show= ' headings ' ,   #隱藏首列
        )
table.heading(column = '現在時間' , text= '現在時間' , anchor= 'w' ,
              command = lambda : print ( '現在時間' ))   #定義表頭
table.heading( '開盤價' , text= '開盤價' , )   #定義表頭
table.heading( '最高價' , text= '最高價' , )   #定義表頭
table.heading( '最低價' , text= '最低價' , )   #定義表頭
table.heading( '收盤價' , text= '收盤價' , )   #定義表頭
table.heading( '調整後收盤價', text= '調整後收盤價' , )   #定義表頭
table.heading( '成交量' , text= '成交量' , )   #定義表頭

table.column( '現在時間' , width=100, minwidth=100, anchor='s', )   #定義列
table.column( '開盤價' , width=100, minwidth=100, anchor='s')   #定義列
table.column( '最高價' , width=100, minwidth=50, anchor='s')   #定義列
table.column( '最低價' , width=100, minwidth=50, anchor='s')   #定義列
table.column( '收盤價', width=100, minwidth=100, anchor='s')   #定義列
table.column( '調整後收盤價' , width=150, minwidth=100, anchor='s')   #定義列
table.column( '成交量' , width=150, minwidth=100, anchor='s')   #定義列
table.grid(row=10)

def insert():
     #插入數據
    info = [
        [ ' 1001 ' , '1001' , ' 1001 ' , ' 1001 ' , ' 1001 ' , ' 1001 ' ,' 1001 ' ],
        [ ' 1002 ' , ' 1002 ' , ' 1002 ' , ' 1002 ' , ' 1002 ' , ' 1002 ' ,' 1002 ' ],
        [ ' 1003 ' , ' 1003 ' , ' 1003 ' , ' 1003 ' , ' 1003 ' , ' 1003 ' ,' 1003 ' ],
        [ ' 1004 ' , ' 1004 ' , ' 1004 ' , ' 1004 ' , ' 1004 ' , ' 1004 ' ,' 1004 ' ],
        ]
    for index, data in enumerate(info):
        table.insert( '' , "end", values=data)   #添加數據到末尾
insert()

    



#ysb = tk.Scrollbar(window)
#ysb.pack(side="right", fill="y")
#listbox = tk. Listbox(window, yscrollcommand = ysb.set)

#for i in range(100):
#        listbox.insert("end", str(i))
#listbox.insert(tk.END,imageLab)
#listbox.pack(side=tk.LEFT, fill=tk.BOTH)
#ysb.config(command=listbox.yview)

window.mainloop() 

# if __name__ == '__main__':
#     cw()

