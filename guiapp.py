from tkinter import *
from tkinter import messagebox
from time import *
import tkinter.ttk as ttk
#import guiforData
import sqlite3
import database
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dateutil import parser

def create_window():
    new_window=Toplevel()
    new_window.geometry('450x210')

    l1=Label(new_window, text="Temperature in F: ")
    l1.grid(row=0,column=0, padx=5, pady=10)

    entry1=Entry(new_window, bg="lightblue")
    entry1.grid(row=0,column=1)

    # aButton1 = Button(new_window, text="Input a Num",command=subscribe)
    # aButton1.grid()

    l2=Label(new_window, text="Humidity in %: ")
    l2.grid(row=1,column=0, padx=5, pady=10)

    entry2=Entry(new_window, bg="lightblue")
    entry2.grid(row=1,column=1)

    # aButton2 = Button(new_window, text="Input a Num",command=subscribe)
    # aButton2.grid()

    l3=Label(new_window, text="Soil Moisture Value: ")
    l3.grid(row=2,column=0, padx=5, pady=10)

    entry3=Entry(new_window, bg="lightblue")
    entry3.grid(row=2,column=1)

    # aButton3 = Button(new_window, text="Input a Num",command=subscribe)
    # aButton3.grid()

    l4=Label(new_window, text="NDVI Value: ")
    l4.grid(row=3,column=0, padx=5, pady=10)

    entry4=Entry(new_window, bg="lightblue")
    entry4.grid(row=3,column=1)

    aButton = Button(new_window, text="Submit",command=subscribe)
    aButton.grid(row=4,column=1)

def create_window2():
    new_window=Toplevel()
    new_window.geometry('400x400')



    # sec=StringVar()
    # Entry(new_window, textvariable=sec, width=2).place(x=220,y=120)
    # sec.set('00')
    # mins=StringVar()
    # Entry(new_window,textvariable=mins, width=2).place(x=180,y=120)
    # mins.set('00')
    # hrs=StringVar()
    # Entry(new_window,textvariable=hrs, width=2).place(x=142, y=120)
    # hrs.set('00')

    # l=Label(new_window, text="Set Timer").pack(side=TOP, pady=10)

    # aButton = Button(new_window, text="Start",command=subscribe)
    # aButton.pack()



ws = Tk()
ws.title('Irrigation Controller')
ws.geometry('680x680')
#ws['bg']='#5d8f90'
ws['bg']='#5b8f90'

l=Label(ws, text="Irrigation Controlling System", font=('Verdana', 18)).pack(side=TOP, pady=10)

#creating a phto image object to use image
photo=PhotoImage(file = "images/manual.jpg")
photoimage = photo.subsample(4,4)  #resize the photo

photo1=PhotoImage(file = "images/manual.jpg")
photoimage1 = photo1.subsample(4,4)

photo2=PhotoImage(file = "images/manual.jpg")
photoimage2 = photo2.subsample(4,4)

photo3=PhotoImage(file = "images/manual.jpg")
photoimage3 = photo3.subsample(4,4)

photo3=PhotoImage(file = "images/manual.jpg")
photoimage4 = photo3.subsample(4,4)


#==================================database Display===========================
def open():
    root=Tk()
    root.title('Present SQLite Data')
    root.geometry('900x750')


    def query_database():
        con=sqlite3.connect("sensors.db")
        cur=con.cursor()
        cur.execute("SELECT * FROM sensors")
        records=cur.fetchall()  #fetching from the database and add to database
    
        #add data to screen
        global inc
        inc=0
        for record in records:
                if inc%2==0:   #if even row
                    my_tree.insert(parent='',index='end',iid=inc,text='',values=(record[0],record[1],record[2],record[3],record[4]),tags=('evenrow',))
                else:
                    my_tree.insert(parent='',index='end',iid=inc,text='',values=(record[0],record[1],record[2],record[3],record[4]),tags=('oddrow',))

                inc+=1

        con.commit()
        con.close()

    def data_query():
        con=sqlite3.connect("sensors.db")
        cur=con.cursor()
        cur.execute("SELECT * FROM sensors WHERE soil=80")
        records=cur.fetchall()
    #add data to screen
        global inc
        inc=0
        for record in records:
                if inc%2==0:   #if even row
                    lower_tree.insert(parent='',index='end',iid=inc,text='',values=(record[0],record[1],record[2],record[3],record[4]),tags=('evenrow',))
                else:
                    lower_tree.insert(parent='',index='end',iid=inc,text='',values=(record[0],record[1],record[2],record[3],record[4]),tags=('oddrow',))

                inc+=1
    
        con.commit()
        con.close()
   
#=========================================================

    #create style
    style=ttk.Style()
    #create theme
    style.theme_use('default')
    #configure Treeview colors
    style.configure("Treeview", 
         background="#D3D3D5",
         foreground="black",
         rowheight=25,
         fieldbackground="#D3D3D5")
    #change color
    style.map('Treeview', background=[('selected', "#347083")])
    #create frame
    tree_frame=Frame(root)
    tree_frame.pack(pady=20)
    #create scrollbar
    tree_scroll=Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)
    #create treeview
    my_tree=ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    my_tree.pack()
    #configure scrollbar
    tree_scroll.config(command=my_tree.yview)
    #define colums
    my_tree['columns']=("soil","temperature","humidity","camera","DateTaken")   

    #position columns
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("soil", anchor=CENTER, width=150)
    my_tree.column("temperature", anchor=CENTER, width=130)
    my_tree.column("humidity", anchor=CENTER, width=130)
    my_tree.column("camera", anchor=CENTER, width=130)
    my_tree.column("DateTaken", anchor=CENTER, width=180)
    #Create Headings
    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("soil", text="soil", anchor=CENTER)
    my_tree.heading("temperature", text="temperature", anchor=CENTER)
    my_tree.heading("humidity", text="humidity", anchor=CENTER)
    my_tree.heading("camera", text="camera", anchor=CENTER)
    my_tree.heading("DateTaken", text="DateTaken", anchor=CENTER)

    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow',background="lightblue")


    Button(root,text="Display Data",command=query_database).pack(pady=20)
#query_database()

#A second Treeview
    lower_tree = ttk.Treeview(root)
    lower_tree.pack()
    #define colums
    lower_tree['columns']=("soil","temperature","humidity","camera","DateTaken")
    #position columns
    lower_tree.column("#0", width=0, stretch=NO)
    lower_tree.column("soil", anchor=CENTER, width=150)
    lower_tree.column("temperature", anchor=CENTER, width=130)
    lower_tree.column("humidity", anchor=CENTER, width=130)
    lower_tree.column("camera", anchor=CENTER, width=130)
    lower_tree.column("DateTaken", anchor=CENTER, width=180)
    #Create Headings
    lower_tree.heading("#0", text="", anchor=W)
    lower_tree.heading("soil", text="soil", anchor=CENTER)
    lower_tree.heading("temperature", text="temperature", anchor=CENTER)
    lower_tree.heading("humidity", text="humidity", anchor=CENTER)
    lower_tree.heading("camera", text="camera", anchor=CENTER)
    lower_tree.heading("DateTaken", text="DateTaken", anchor=CENTER)

    Button(root,text="Display Past Weeks Data",command=data_query).pack(pady=20)

    root.mainloop()

#==============================END of datadisplay=============================


#perform an action when called
def subscribe():
    return messagebox.showinfo('Irrigation Controller','Thank you for subscribing!')


def soil_graph():
    con=sqlite3.connect("sensors.db")
    cur=con.cursor()
    cur.execute('Select DateTaken, soil From sensors')
    data=cur.fetchall()

    dates=[]
    values=[]

    for row in data:
        dates.append(parser.parse(row[0]))
        values.append(row[1])

    plt.plot_date(dates,values,'-')
    plt.show()
def temperature_graph():
    con=sqlite3.connect("sensors.db")
    cur=con.cursor()
    cur.execute('Select DateTaken, temperature From sensors')
    data=cur.fetchall()

    dates=[]
    values=[]

    for row in data:
        dates.append(parser.parse(row[0]))
        values.append(row[1])

    plt.plot_date(dates,values,'-')
    plt.show()
def humidity_graph():
    con=sqlite3.connect("sensors.db")
    cur=con.cursor()
    cur.execute('Select DateTaken, humidity From sensors')
    data=cur.fetchall()

    dates=[]
    values=[]

    for row in data:
        dates.append(parser.parse(row[0]))
        values.append(row[1])

    plt.plot_date(dates,values,'-')
    plt.show()
def camera_graph():
    con=sqlite3.connect("sensors.db")
    cur=con.cursor()
    cur.execute('Select DateTaken, camera From sensors')
    data=cur.fetchall()

    dates=[]
    values=[]

    for row in data:
        dates.append(parser.parse(row[0]))
        values.append(row[1])

    plt.plot_date(dates,values,'-')
    plt.show()


Button(ws, text="Automated",image = photoimage, compound = LEFT, command=create_window).pack(pady=5)
Button(ws, text="Manual", image = photoimage1, compound = LEFT, command=subscribe).pack(pady=5)
Button(ws, text="Timer",image = photoimage2, compound = LEFT,command=create_window2).pack(pady=5)
Button(ws, text="Exit",image = photoimage3, compound = LEFT,command=ws.destroy).pack(pady=5)
Button(ws, text=" Display Soil Graph",image=photoimage4,compound = LEFT, command=soil_graph).pack(pady=5)
Button(ws, text=" Display Temperature Graph",image=photoimage4,compound = LEFT, command=temperature_graph).pack(pady=5)
Button(ws, text=" Display Humidity Graph",image=photoimage4,compound = LEFT, command=humidity_graph).pack(pady=5)
Button(ws, text=" Display Camera Graph",image=photoimage4,compound = LEFT, command=camera_graph).pack(pady=5)

Button(ws, text="Display Data",image=photoimage4,compound = LEFT, command=open).pack(pady=5)


ws.mainloop()
