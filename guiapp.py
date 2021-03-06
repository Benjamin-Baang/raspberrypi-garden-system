from tkinter import *
import tkinter.ttk as ttk
import psycopg2
from config_db import config
import matplotlib.pyplot as plt


def automated():
    with psycopg2.connect(**config()) as con:
        cur = con.cursor()
        cur.execute('select * from app_user where id=%s', (1,))
        if cur.fetchall():
            cur.execute('update app_user set State=%s where id=%s', ('automated', '1'))
        else:
            cur.execute('insert into app_user (State) VALUES (%s)', ('automated',)) 


def manual():
    def submit():
        with psycopg2.connect(**config()) as con:
            cur = con.cursor()
            cur.execute('select * from app_user where id=%s', (1,))
            if cur.fetchall():
                cur.execute('update app_user set State=%s where id=%s', ('manual', 1))
            else:
                cur.execute('insert into app_user (State) VALUES (%s)', ('manual',)) 
            cur.execute('select * from manual where id=%s', (1,))
            if cur.fetchall():
                cur.execute("update manual set soil=%s, temperature=%s, humidity=%s, camera=%s where id=%s", (entry1.get(), entry2.get(), entry3.get(), entry4.get(), 1))
            else:
                cur.execute("insert into manual (soil, temperature, humidity, camera) VALUES (%s, %s, %s, %s)", (entry1.get(), entry2.get(), entry3.get(), entry4.get()))

        entry1.delete(0,END)
        entry2.delete(0,END)
        entry3.delete(0,END)
        entry4.delete(0,END)


    def query():
        with psycopg2.connect(**config()) as con:
            cur = con.cursor()
            cur.execute('select * from manual where id=%s', (1,))
            r=cur.fetchone()
            show=''
            for info in r:
                show=show + str(info)+"\n"
            c_label=Label(new_window,text=show).grid(row=7)


    new_window=Toplevel()
    new_window.geometry('470x400')

    l1=Label(new_window, text="Soil Moisture Value: ")
    l1.grid(row=0,column=0, padx=5, pady=10)

    entry1=Entry(new_window, bg="lightblue")
    entry1.grid(row=0,column=1)

    l2=Label(new_window, text="Temperature in F:")
    l2.grid(row=1,column=0, padx=5, pady=10)

    entry2=Entry(new_window, bg="lightblue")
    entry2.grid(row=1,column=1)

    l3=Label(new_window, text="Humidity in %: ")
    l3.grid(row=2,column=0, padx=5, pady=10)

    entry3=Entry(new_window, bg="lightblue")
    entry3.grid(row=2,column=1)
    
    l4=Label(new_window, text="NDVI Value: ")
    l4.grid(row=3,column=0, padx=5, pady=10)

    entry4=Entry(new_window, bg="lightblue")
    entry4.grid(row=3,column=1)
    
    aButton = Button(new_window, text="Submit Record To Database",command=submit)
    aButton.grid(row=5,column=1)

    qButton = Button(new_window, text="Show User Input",command=query)
    qButton.grid(row=6,column=1)
    

def timer():
    def submit():
        with psycopg2.connect(**config()) as con:
            cur=con.cursor()
            cur.execute('select * from app_user where id=%s', (1,))
            if cur.fetchall():
                cur.execute('update app_user set State=%s where id=%s', ('timer', 1))
            else:
                cur.execute('insert into app_user (State) VALUES (%s)', ('timer',)) 
            cur.execute('select * from timer where day=%s', (days.get(),))
            if cur.fetchall():
                cur.execute("update timer set STime=%s, FTime=%s,AmPm1=%s,AmPm2=%s where day=%s", 
                            (stime.get(),ftime.get(),ampm1.get(),ampm2.get(),days.get()))
            else:
                cur.execute("insert into timer (day, STime, FTime, AmPm1, AmPm2) VALUES (%s, %s, %s, %s, %s)", 
                            (days.get(), stime.get(),ftime.get(),ampm1.get(),ampm2.get()))

        stime.delete(0,END)
        ftime.delete(0,END)


    def query():
        with psycopg2.connect(**config()) as con:
            cur=con.cursor()

            cur.execute("SELECT * FROM timer")
            r=cur.fetchall()
            show=''
            for info in r:
                show=show + str(info)+"\n"
            c_label=Label(new_window,text=show).grid(row=7)

    new_window=Toplevel()
    new_window.geometry('500x450')

    l1=Label(new_window, text="Choose A Day Of the Week: ")
    l1.grid(row=0,column=0, padx=5, pady=10)

    options = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    days=StringVar()
    days.set("Monday")
    days_menu=OptionMenu(new_window, days, *options)
    days_menu.grid(row=0, column=1)

    A=Label(new_window,text="From: ")
    A.grid(row=1,column=1,pady=15)

    l2=Label(new_window, text="BEGINNING Time: ")
    l2.grid(row=2,column=0, padx=5, pady=10)

    stime=Entry(new_window, bg="lightblue")
    stime.grid(row=2,column=1)

    Aampm=Label(new_window, text="12-Hour Clock: ")
    Aampm.grid(row=3,column=0)
    
    options1 = ["AM","PM"]
    ampm1=StringVar()
    ampm1.set("AM")
    ampm1_menu=OptionMenu(new_window, ampm1, *options1)
    ampm1_menu.grid(row=3,column=1)

    B=Label(new_window,text="To: ")
    B.grid(row=4,column=1,pady=15)

    l3=Label(new_window, text="END Time: ")
    l3.grid(row=5,column=0, padx=5, pady=10)

    ftime=Entry(new_window, bg="lightblue")
    ftime.grid(row=5,column=1)

    Bampm=Label(new_window, text="12-Hour Clock: ")
    Bampm.grid(row=6,column=0)

    options2 = ["AM","PM"]
    ampm2=StringVar()
    ampm2.set("AM")
    ampm2_menu=OptionMenu(new_window,ampm2, *options2)
    ampm2_menu.grid(row=6,column=1)

    aButton = Button(new_window, text="Submit Record To Database",command=submit)
    aButton.grid(row=7,column=1,pady=15)

    bButton = Button(new_window, text="Show User Input",command=query)
    bButton.grid(row=8,column=1)


if __name__ == '__main__':
    ws = Tk()
    ws.title('Irrigation Controller')
    ws.geometry('1280x720')
    ws['bg']='#5b8f90'
    ws.minsize(800,600)

    l=Label(ws, text="Irrigation Controlling System", font=('Verdana', 35),bg='cyan')
    l.grid(row=0,columnspan=3,pady=20)

    l1=Label(ws, text="User Option", font=('Calibri', 22),bg='light blue')
    l1.grid(row=1,column=0,padx=15,pady=25)

    l2=Label(ws, text="Query Data", font=('Calibri', 22),bg='light blue')
    l2.grid(row=1,column=1,pady=25)

    l3=Label(ws, text="Admin Option", font=('Calibri', 22),bg='light blue')
    l3.grid(row=1,column=2,pady=25)
    
    automated_icon=PhotoImage(file = "images/manual.png")
    automated_image = automated_icon.subsample(7,7)  #resize the photo

    manual_icon=PhotoImage(file = "images/manual2.jpg")
    manual_image = manual_icon.subsample(7,7)

    timer_icon=PhotoImage(file = "images/timer2.jpg")
    timer_image = timer_icon.subsample(7,7)

    graph_icon=PhotoImage(file = "images/graph2.png")
    graph_image = graph_icon.subsample(7,7)

    table_icon=PhotoImage(file = "images/table2.png")
    table_image = table_icon.subsample(7,7)

    on_icon=PhotoImage(file = "images/on2.png")
    on_image = on_icon.subsample(3,4)

    off_icon=PhotoImage(file = "images/off2.png")
    off_image = off_icon.subsample(15,9)

    exit_icon=PhotoImage(file = "images/exit2.png")
    exit_image = exit_icon.subsample(4,5)


    def display_data():
        root=Toplevel()
        root.title('Present SQLite Data')
        root.geometry('800x800')


        def query_database():
            for item in my_tree.get_children():
                my_tree.delete(item)
            with psycopg2.connect(**config()) as con:
                cur=con.cursor()
                cur.execute('select * from sensors')
                records=cur.fetchall()
        
            global inc
            inc=0
            for record in records:
                    if inc%2==0: 
                        my_tree.insert(parent='',index='end',iid=inc,text='',values=(record[0],record[1],record[2],record[3],record[4]),tags=('evenrow',))
                    else:
                        my_tree.insert(parent='',index='end',iid=inc,text='',values=(record[0],record[1],record[2],record[3],record[4]),tags=('oddrow',))
                    inc+=1


        def data_query():
            for item in lower_tree.get_children():
                lower_tree.delete(item)
            with psycopg2.connect(**config()) as con:
                cur=con.cursor()
                cur.execute("select * from sensors where datetaken > NOW() - INTERVAL '1 minute'")
                records=cur.fetchall()
            
            global inc
            inc=0
            for record in records:
                    if inc%2==0:
                        lower_tree.insert(parent='',index='end',iid=inc,text='',values=(record[0],record[1],record[2],record[3],record[4]),tags=('evenrow',))
                    else:
                        lower_tree.insert(parent='',index='end',iid=inc,text='',values=(record[0],record[1],record[2],record[3],record[4]),tags=('oddrow',))
                    inc+=1
    

        style=ttk.Style()
        style.theme_use('default')
        style.configure("Treeview", 
            background="#D3D3D5",
            foreground="black",
            rowheight=25,
            fieldbackground="#D3D3D5")
        style.map('Treeview', background=[('selected', "#347083")])
        tree_frame=Frame(root)
        tree_frame.pack(pady=20)
        tree_scroll=Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)
        my_tree=ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
        my_tree.pack()
        tree_scroll.config(command=my_tree.yview)
        my_tree['columns']=("soil","temperature","humidity","camera","DateTaken")   

        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("soil", anchor=CENTER, width=150)
        my_tree.column("temperature", anchor=CENTER, width=130)
        my_tree.column("humidity", anchor=CENTER, width=130)
        my_tree.column("camera", anchor=CENTER, width=130)
        my_tree.column("DateTaken", anchor=CENTER, width=180)
        
        my_tree.heading("#0", text="", anchor=W)
        my_tree.heading("soil", text="soil", anchor=CENTER)
        my_tree.heading("temperature", text="temperature", anchor=CENTER)
        my_tree.heading("humidity", text="humidity", anchor=CENTER)
        my_tree.heading("camera", text="camera", anchor=CENTER)
        my_tree.heading("DateTaken", text="DateTaken", anchor=CENTER)

        my_tree.tag_configure('oddrow', background="white")
        my_tree.tag_configure('evenrow',background="lightblue")

        Button(root,text="Display Data",command=query_database).pack(pady=20)

        lower_tree = ttk.Treeview(root)
        lower_tree.pack()
        lower_tree['columns']=("soil","temperature","humidity","camera","DateTaken")
        
        lower_tree.column("#0", width=0, stretch=NO)
        lower_tree.column("soil", anchor=CENTER, width=150)
        lower_tree.column("temperature", anchor=CENTER, width=130)
        lower_tree.column("humidity", anchor=CENTER, width=130)
        lower_tree.column("camera", anchor=CENTER, width=130)
        lower_tree.column("DateTaken", anchor=CENTER, width=180)
        
        lower_tree.heading("#0", text="", anchor=W)
        lower_tree.heading("soil", text="soil", anchor=CENTER)
        lower_tree.heading("temperature", text="temperature", anchor=CENTER)
        lower_tree.heading("humidity", text="humidity", anchor=CENTER)
        lower_tree.heading("camera", text="camera", anchor=CENTER)
        lower_tree.heading("DateTaken", text="DateTaken", anchor=CENTER)

        Button(root,text="Display Past Weeks Data",command=data_query).pack(pady=20)
        
        root.mainloop()
    #==============================END of datadisplay=============================


    def soil_graph():
        with psycopg2.connect(**config()) as con:
            cur=con.cursor()
            cur.execute('select DateTaken, soil from sensors')
            data=cur.fetchall()

        dates=[]
        values=[]

        for row in data:
            dates.append(row[0])
            values.append(row[1])

        plt.plot_date(dates,values,'-', marker='o')
        plt.title('Soil vs Dates Taken')
        plt.xlabel('Dates Taken')
        plt.ylabel('Soil Information')
        plt.show()
        
    
    def temperature_graph():
        with psycopg2.connect(**config()) as con:
            cur=con.cursor()
            cur.execute('select DateTaken, temperature from sensors')
            data=cur.fetchall()
            
        dates=[]
        values=[]

        for row in data:
            dates.append(row[0])
            values.append(row[1])
        plt.plot_date(dates,values,'-', marker='o')
        plt.title('Temperature vs Dates Taken')
        plt.xlabel('Dates Taken')
        plt.ylabel('Temperature Information')
        plt.show()
        
    
    def humidity_graph():
        with psycopg2.connect(**config()) as con:
            cur=con.cursor()
            cur.execute('select DateTaken, humidity from sensors')
            data=cur.fetchall()

        dates=[]
        values=[]

        for row in data:
            dates.append(row[0])
            values.append(row[1])

        plt.plot_date(dates,values,'-', marker='o')
        plt.title('Humidity vs Dates Taken')
        plt.xlabel('Dates Taken')
        plt.ylabel('Humidity Information')
        plt.show()
        
    
    def camera_graph():
        with psycopg2.connect(**config()) as con:
            cur=con.cursor()
            cur.execute('select DateTaken, camera from sensors')
            data=cur.fetchall()

        dates=[]
        values=[]

        for row in data:
            dates.append(row[0])
            values.append(row[1])
        plt.plot_date(dates,values,'-', marker='o')
        plt.title('NDVI vs Dates Taken')
        plt.xlabel('Dates Taken')
        plt.ylabel('NDVI Value')
        plt.show()
    
    
    def on():
        with psycopg2.connect(**config()) as con:
            cur = con.cursor()
            cur.execute('select * from admin_user')
        
            cur.execute('update admin_user set command = %s', (1,))
            cur.execute('select * from app_user where id=%s', (1,))
            if cur.fetchall():
                cur.execute('update app_user set State=%s where id=%s', ('admin', '1'))
            else:
                cur.execute('insert into app_user (State) VALUES (%s)', ('admin',))


    def off():
        with psycopg2.connect(**config()) as con:
            cur = con.cursor()
            cur.execute('select * from admin_user')
        
            cur.execute('update admin_user set command = %s', (0,))
            cur.execute('select * from app_user where id=%s', (1,))
            if cur.fetchall():
                cur.execute('update app_user set State=%s where id=%s', ('admin', '1'))
            else:
                cur.execute('insert into app_user (State) VALUES (%s)', ('admin',))


    ws.grid_rowconfigure(0, weight=1)
    ws.grid_rowconfigure(1, weight=1)
    ws.grid_rowconfigure(2, weight=1)
    ws.grid_rowconfigure(3, weight=1)
    ws.grid_rowconfigure(4, weight=1)
    ws.grid_rowconfigure(5, weight=1)
    ws.grid_rowconfigure(6, weight=1)
    
    ws.grid_columnconfigure(0, weight=1, minsize=200)
    ws.grid_columnconfigure(1, weight=1, minsize=250)
    ws.grid_columnconfigure(2, weight=1, minsize=200)

    button1=Button(ws, text="Automated",image = automated_image, compound = LEFT, command=automated)
    button1.grid(row=2,column=0,padx=15,pady=10)
    button2=Button(ws, text="Manual", image = manual_image, compound = LEFT, command=manual)
    button2.grid(row=3,column=0,padx=15,pady=10)
    button3=Button(ws, text="Timer",image = timer_image, compound = LEFT,command=timer)
    button3.grid(row=4,column=0,padx=15,pady=10)
    button5=Button(ws, text=" Display Soil Graph",image=graph_image,compound = LEFT, command=soil_graph)
    button5.grid(row=2,column=1,padx=15,pady=10)
    button6=Button(ws, text=" Display Temperature Graph",image=graph_image,compound = LEFT, command=temperature_graph)
    button6.grid(row=3,column=1,padx=15,pady=10)
    button7=Button(ws, text=" Display Humidity Graph",image=graph_image,compound = LEFT, command=humidity_graph)
    button7.grid(row=4,column=1,padx=15,pady=10)
    button8=Button(ws, text=" Display Camera Graph",image=graph_image,compound = LEFT, command=camera_graph)
    button8.grid(row=5,column=1,padx=15,pady=10)
    button4=Button(ws, text="Exit",image = exit_image, compound = LEFT,command=ws.destroy)
    button4.grid(row=4,column=2,padx=15,pady=10)
    
    buttonon=Button(ws, text="ON",image = on_image, compound = LEFT,command=on)
    buttonon.grid(row=2,column=2,padx=15,pady=10)
    buttonoff=Button(ws, text="OFF",image = off_image, compound = LEFT,command=off)
    buttonoff.grid(row=3,column=2,padx=15,pady=10)

    button9=Button(ws, text="Display Data",image=table_image,compound = LEFT, command=display_data)
    button9.grid(row=6,column=1,padx=15,pady=10)
    button9.config(width=400)

    ws.mainloop()
