from tkinter import *
import tkinter.ttk as ttk
import psycopg2
from config_db import config
import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
# from dateutil import parser


def app_setup():
    '''
    Check if tables exist. If not, create them.
    '''
    with psycopg2.connect(**config()) as con:
        cur=con.cursor()
        cur.execute("""create table if not exists sensors (
                            soil REAL,
                            temperature REAL, 
                            humidity REAL, 
                            camera REAL,
                            DateTaken TIMESTAMP
                            )""")
        cur.execute('''delete from sensors''')
        cur.execute('''create table if not exists app_user (
                            id serial primary key,
                            State text
                            )''')
        cur.execute("select * from app_user")
        if cur.fetchone() is None:
            cur.execute("insert into app_user (id, State) VALUES(%s, %s)", (0, 'automatic'))
        cur.execute("""create table if not exists manual (
            id serial primary key,
            soil real,
            temperature real,
            humidity real,
            camera real
            )""")
        
        cur.execute("""create table if not exists timer (
            day TEXT,
            BTime real,
            Etime real,
            AmPm1 real,
            AmPm2 real
            )""")

#perform an action when called
def subscribe():
    with psycopg2.connect(**config()) as con:
        cur = con.cursor()
        cur.execute('select * from app_user where id=%s', (1,))
        if cur.fetchall():
            cur.execute('update app_user set State=%s where id=%s', ('automated', '1'))
        else:
            cur.execute('insert into app_user (State) VALUES (%s)', ('automated',)) 


def create_window():
    with psycopg2.connect(**config()) as con:
        cur = con.cursor()
        cur.execute('select * from app_user where id=%s', (1,))
        if cur.fetchall():
            cur.execute('update app_user set State=%s where id=%s', ('manual', 1))
        else:
            cur.execute('insert into app_user (State) VALUES (%s)', ('manual',)) 


    def submit():
        with psycopg2.connect(**config()) as con:
            cur = con.cursor()
            cur.execute('select * from manual where id=%s', (1,))
            if cur.fetchall():
                cur.execute("update manual set soil=%s, temperature=%s, humidity=%s, camera=%s where id=%s", (entry1.get(), entry2.get(), entry3.get(), entry4.get(), 1))
            else:
                cur.execute("insert into manual (soil, temperature, humidity, camera) VALUES (%s, %s, %s, %s)", (entry1.get(), entry2.get(), entry3.get(), entry4.get()))

        entry1.delete(0,END)
        entry2.delete(0,END)
        entry3.delete(0,END)
        entry4.delete(0,END)


    #To display data
    def query():
        with psycopg2.connect(**config()) as con:
            cur = con.cursor()
            cur.execute('select * from manual where id=%s', (1,))
            r=cur.fetchone()
            show=''
            for info in r:
                show=show + str(info)+"\n"
            c_label=Label(new_window,text=show).grid(row=7)


    new_window=Tk()
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
    

def create_window2():
    def insert():
        #con=sqlite3.connect("sensors.db")
        with psycopg2.connect(**config()) as con:
            cur=con.cursor()

            cur.execute('select * from timer where day=%s', (clicked.get(),))
            if cur.fetchall():
                cur.execute("update timer set Btime=%s, Etime=%s,AmPm1=%s,AmPm2=%s where day=%s", (EndTime.get(),EndTime.get(),clicked.get(),clicked1.get(),clicked2.get()))
            else:
                cur.execute("INSERT INTO timer VALUES (:drdnMenu,:BegTime,:EndTime,:drdnAMPM1,:drdnAMPM2)",
                {
                    'drdnMenu': clicked.get(),
                    'BegTime': BegTime.get(),
                    'EndTime': EndTime.get(),
                    'drdnAMPM1': clicked1.get(),
                    'drdnAMPM2': clicked2.get()
                })

        BegTime.delete(0,END)
        EndTime.delete(0,END)

    def queryfTimer():
        #con=sqlite3.connect("sensors.db")
        with psycopg2.connect(**config()) as con:
            cur=con.cursor()

            cur.execute("SELECT * FROM timer")
            #cur.execute("select * from timer2 where id=?", (1,))
            r=cur.fetchall()
            show=''
            for info in r:
                show=show + str(info)+"\n"

            c_label=Label(new_window,text=show).grid(row=7)


    new_window=Tk()
    new_window.geometry('500x450')


    l1=Label(new_window, text="Choose A Day Of the Week: ")
    l1.grid(row=0,column=0, padx=5, pady=10)


    clicked=StringVar()
    options = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

    drdnMenu=OptionMenu(new_window,clicked, *options)
    drdnMenu.grid(row=0,column=1)


    A=Label(new_window,text="From: ")
    A.grid(row=1,column=1,pady=15)


    l2=Label(new_window, text="BEGINNING Time: ")
    l2.grid(row=2,column=0, padx=5, pady=10)

    BegTime=Entry(new_window, bg="lightblue")
    BegTime.grid(row=2,column=1)

    Aampm=Label(new_window, text="12-Hour Clock: ")
    Aampm.grid(row=3,column=0)
    #============================
    clicked1=StringVar()
    options1 = ["AM","PM"]

    drdnAMPM1=OptionMenu(new_window,clicked1, *options1)
    drdnAMPM1.grid(row=3,column=1)

    #===================

    B=Label(new_window,text="To: ")
    B.grid(row=4,column=1,pady=15)

    l3=Label(new_window, text="END Time: ")
    l3.grid(row=5,column=0, padx=5, pady=10)

    EndTime=Entry(new_window, bg="lightblue")
    EndTime.grid(row=5,column=1)

    Bampm=Label(new_window, text="12-Hour Clock: ")
    Bampm.grid(row=6,column=0)

    clicked2=StringVar()
    options2 = ["AM","PM"]

    drdnAMPM2=OptionMenu(new_window,clicked2, *options2)
    drdnAMPM2.grid(row=6,column=1)

    aButton = Button(new_window, text="Submit Record To Database",command=insert)
    aButton.grid(row=7,column=1,pady=15)

    bButton = Button(new_window, text="Show User Input",command=queryfTimer)
    bButton.grid(row=8,column=1)


if __name__ == '__main__':
    app_setup()
    
    ws = Tk()
    ws.title('Irrigation Controller')
    ws.geometry('680x900')
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
            with psycopg2.connect(**config()) as con:
                cur=con.cursor()
                cur.execute('select * from sensors')
                records=cur.fetchall()
        
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
            with psycopg2.connect(**config()) as con:
                cur=con.cursor()
                cur.execute("select * from sensors where DateTaken < timestamp '2022-03-15 00:00:00'")
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

        plt.plot_date(dates,values,'-')
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
        plt.plot_date(dates,values,'-')
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

        plt.plot_date(dates,values,'-')
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
        plt.plot_date(dates,values,'-')
        plt.show()


    Button(ws, text="Automated",image = photoimage, compound = LEFT, command=subscribe).pack(pady=5)
    Button(ws, text="Manual", image = photoimage1, compound = LEFT, command=create_window).pack(pady=5)
    Button(ws, text="Timer",image = photoimage2, compound = LEFT,command=create_window2).pack(pady=5)
    Button(ws, text="Exit",image = photoimage3, compound = LEFT,command=ws.destroy).pack(pady=5)
    Button(ws, text=" Display Soil Graph",image=photoimage4,compound = LEFT, command=soil_graph).pack(pady=5)
    Button(ws, text=" Display Temperature Graph",image=photoimage4,compound = LEFT, command=temperature_graph).pack(pady=5)
    Button(ws, text=" Display Humidity Graph",image=photoimage4,compound = LEFT, command=humidity_graph).pack(pady=5)
    Button(ws, text=" Display Camera Graph",image=photoimage4,compound = LEFT, command=camera_graph).pack(pady=5)
    Button(ws, text="Display Data",image=photoimage4,compound = LEFT, command=open).pack(pady=5)

    ws.mainloop()
