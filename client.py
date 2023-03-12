import socket
from tkinter import *
from  threading import Thread
import random
from PIL import ImageTk, Image
import platform

screen_width = None
screen_height = None

SERVER = None
PORT = None
IP_ADDRESS = None
playerName = None

ticketGrid = {}
currentNumberList = []

canvas1 = None
canvas2 = None

nameEntry = None
nameWindow = None
gameWindow = None

def saveName():
    global SERVER
    global playerName
    global nameWindow
    global nameEntry

    playerName = nameEntry.get()
    nameEntry.delete(0, END)
    nameWindow.destroy()

    SERVER.send(playerName.encode())

    game_window()

    



def game_window():
    global gameWindow
    global canvas2
    global screen_height
    global screen_width

    gameWindow = Tk()
    gameWindow.title('TAMBOLA FAMILY FUN')
    gameWindow.geometry('800x600')

    screen_height = gameWindow.winfo_screenheight()
    screen_width = gameWindow.winfo_screenwidth()

    bg = ImageTk.PhotoImage(file = "./assets/background.png")

    canvas2 = Canvas(gameWindow,width=500,height = 500)
    canvas2.pack(fill='both',expand=True)

    canvas2.create_image(0,0,image = bg,anchor = 'nw')
    canvas2.create_text(screen_width/4,screen_height/6,text="TAMBOLA FAMILY FUN",font = ("Chalkboard SE",40),fill="black")
    
    gameWindow.resizable(True,True)
    gameWindow.mainloop()
    
    createTicket()
    placeNumbers()

def createTicket():
    global gameWindow
    global ticketGrid

    xPos = 105
    yPos = 130

    mainLabel = Label(gameWindow,width=65,height=16,relief="ridge",borderwidth=5,bg="white")
    mainLabel.place(x=95,y=119)
    for row in range(0,3):
        row_list = []
        for col in range(0,9):
            if(platform.system() == "Darwin"):
                boxButton = Label(gameWindow,font=("Chalkboard",20),borderwidth=3,pady=23,padx=22,bg="#fff376",highlightbackground="#fff376",activebackground="#c5ela5")
                boxButton.place(x=xPos,y=yPos)
            else:
                boxButton = Label(gameWindow,font=("Chalkboard",20),borderwidth=5,width=3,height=3,bg="#fff376")
                boxButton.place(x=xPos,y=yPos)
            row_list.append(boxButton)
            xPos += 64
        ticketGrid.append(row_list)
        xPos = 105
        yPos += 82

def placeNumbers():
    global ticketGrid
    global currentNumberList

    for row in range(0,3):
        randomColList = []
        counter = 0

        while counter <= 4:
            randomCol = random.randint(0,8)
            if(randomCol not in randomColList):
                randomColList.append(randomCol)
                counter += 1

    numberContainer = {
        "0": [1,2,3,4,5,6,7,8,9],
        "1": [10,11,12,13,14,15,16,17,18,19],
        "2": [20,21,22,23,24,25,26,27,28,29],
        "3": [30,31,32,33,34,35,36,37,38,39],
        "4": [40,41,42,43,44,45,46,47,48,49],
        "5": [50,51,52,53,54,55,56,57,58,59],
        "6": [60,61,62,63,64,65,66,67,68,69],
        "7": [70,71,72,73,74,75,76,77,78,79],
        "8": [80,81,82,83,84,85,86,87,88,89,90],
    }

    counter = 0
    while (counter < len(randomColList)):
        colNum = randomColList[counter]
        numbersListByIndex = numberContainer[str(colNum)]
        randomNumber = random.choice(numbersListByIndex)

        if(randomNumber not in currentNumberList):
            numberBox = ticketGrid[row][colNum]
            numberBox.configure(text=randomNumber, fg= 'black')
            currentNumberList.append(randomNumber)

            counter += 1



def askPlayerName():
    global playerName
    global nameEntry
    global nameWindow
    global canvas1

    nameWindow  = Tk()
    nameWindow.title("Tambola Family Fun")
    nameWindow.geometry('800x600')


    screen_width = nameWindow.winfo_screenwidth()
    screen_height = nameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file = "./assets/background.png")

    canvas1 = Canvas( nameWindow, width = 500,height = 500)
    canvas1.pack(fill = "both", expand = True)
    # Display image
    canvas1.create_image( 0, 0, image = bg, anchor = "nw")
    canvas1.create_text( screen_width/4.5,screen_height/8, text = "Enter Name", font=("Chalkboard SE",60), fill="black")

    nameEntry = Entry(nameWindow, width=15, justify='center', font=('Chalkboard SE', 30), bd=5, bg='white')
    nameEntry.place(x = screen_width/7, y=screen_height/5.5 )


    button = Button(nameWindow, text="Save", font=("Chalkboard SE", 30),width=11, command=saveName, height=2, bg="#80deea", bd=3)
    button.place(x = screen_width/6, y=screen_height/4)

    nameWindow.resizable(True, True)
    nameWindow.mainloop()





def recivedMsg():
    pass


def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    PORT  = 6000
    IP_ADDRESS = '127.0.0.1'

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))

    thread = Thread(target=recivedMsg)
    thread.start()

    askPlayerName()


setup()
