from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
import time
from tkinter import *
import pickle
from array import *
import os
import subprocess
import platform
import re

driver = webdriver.Firefox()
driver.get('https://www.chess.com/play/computer')

os_name = platform.system()

if os_name == "Windows":
    print("Running on Windows")
    file_path = os.path.abspath('stockfishWindows.exe')
elif os_name == "Linux":
    print("Running on Linux")
    file_path = os.path.abspath('stockfishLinux')


moveLabel : Label
WhiteTurn : BooleanVar

blackQueenCastling : BooleanVar
blackKingCastling : BooleanVar
whiteQueenCastling : BooleanVar
whiteKingCastling : BooleanVar

depthTextBox : Entry

# Define the button click action
def button_click():
    global moveLabel
    

    allDivs = driver.find_elements(By.TAG_NAME, 'div')
    divNames = []
    for div in allDivs :
        divNames.append(div.get_attribute("class"))

    matrix = getAllPiecesFromAllDivs(divNames)
    fen = matrixToFEN(matrix)
    print(fen)
    depth = depthTextBox.get()
    try:
        int(depth)
    except ValueError:
        moveLabel.config(text=f"Depth input incorrect")
        return -1
     
    bestMove = getBestMove(fen, "20")
    print(bestMove)
    mateinN = bestMove[1]
    bestMove = bestMove[0]

    if isinstance(bestMove, int):
        print("ERROR:", bestMove)
        moveLabel.config(text=f"Engine error, make sure castling rights are correct")
        return -1
    moveLabel.config(text=f"{bestMove[:2]} {bestMove[2:4]} \n {mateinN}")
    # with open("allDivs.pickle", "wb") as f:
    #     pickle.dump(divNames, f)

    

def getAllPiecesFromAllDivs(allDivs: list[str]) -> list[str]:
    matrix = [
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None]
    ]
    

    for div in allDivs :
        # print("-"+div+"-")
        regex = re.compile(r"piece .. square-\d\d")
        if (regex.search(div) == None):
            continue
        
        if div[:5] == "piece":
            print(div)
            splitted = div.split(' ')
            coord = splitted[2].split('-')[1]
            col = coord[0]
            row = coord[1]
            bOrW = splitted[1][0]
            piece = splitted[1][1]
            if bOrW == 'w':
                piece = piece.upper()
            matrix[8 - int(row)][int(col)-1] = piece
            # print(div)
            # print("Row ", row, " Col", col, " b/w", bOrW, " piece", piece)
    return matrix

def matrixToFEN(board):

    global whiteKingCastling
    global whiteQueenCastling
    global blackKingCastling
    global blackQueenCastling
    global WhiteTurn

    fen = ""
    empty_count = 0

    # Convert the board matrix to a string representation
    for row in board:
        for square in row:
            if square is None:
                empty_count += 1
            else:
                if empty_count > 0:
                    fen += str(empty_count)
                    empty_count = 0
                fen += square
        if empty_count > 0:
            fen += str(empty_count)
            empty_count = 0
        fen += "/"

    # Add information about the state of the game
    if WhiteTurn.get() :
        turn = 'w'
    else :
        turn = 'b'
    
    castlingString = ""
    if whiteKingCastling.get():
        castlingString += "K"
    if whiteQueenCastling.get():
        castlingString += "Q"
    if blackKingCastling.get():
        castlingString += "k"
    if blackQueenCastling.get():
        castlingString += "q"
    if len(castlingString) == 0:
        castlingString = "-"

    fen += f" {turn} {castlingString} - 0 1"

    return fen


def getBestMove(fen: str, depth: str):

    process = subprocess.Popen([file_path], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    startedMsg = process.stdout.readline().decode('utf-8')
    print(startedMsg.encode("utf-8"))

    # run the executable program
    fenString = f"position fen {fen}\n"
    depthString = f"go depth {depth}\n"
    process.stdin.write(fenString.encode("utf-8"))
    process.stdin.write(depthString.encode("utf-8"))
    process.stdin.flush()
    # read the output continuously
    mateinN = ""

    while True:
        output = process.stdout.readline().decode('utf-8')
        print(output)
        if f"info depth {depth}" in output and "mate" in output:
            mateinN = "Mate in " + output.split(" ")[9]

        if output == '' and process.poll() is not None:
            break
        if output:
            if output.split(" ")[0] == "bestmove":
                return (output.split(" ")[1], mateinN)

    # get the return code of the process
    return_code = process.poll()
    return return_code



root : Tk

def main():
        # # Create the GUI window
    global root
    root = Tk()
    root.title('Chess.com cheating browser')
    root.wm_attributes("-topmost", True)
    global WhiteTurn
    WhiteTurn = BooleanVar(value=True)
    global frame
    frame = Frame(root, width=200, height=200)
    button = Button(frame, text='Get Move!', command=button_click, width=20, height=5)
    button.grid(row=0, column=0, pady=(15, 15), padx=15, sticky="nsew")
    global moveLabel
    moveLabel = Label(frame, text="Bestmove: ")
    moveLabel.config(font=("Arial", 24))
    moveLabel.grid(row=0, column=1, padx=15)
    
    global whiteTurnLabel
    whiteTurnCheckButton = Checkbutton(frame, variable=WhiteTurn, text="White turn?")
    whiteTurnCheckButton.grid(row=1, column=0, padx=15, pady=15)
    
    global whiteKingCastling
    global whiteQueenCastling
    global blackKingCastling
    global blackQueenCastling
    whiteKingCastling = BooleanVar(value=True)
    whiteQueenCastling = BooleanVar(value=True)
    blackKingCastling = BooleanVar(value=True)
    blackQueenCastling = BooleanVar(value=True)
    blackKingCastlingCheckButton = Checkbutton(frame, text="BlackKingCastling", variable=blackKingCastling)
    blackKingCastlingCheckButton.grid(row=2, column=0, padx=15, pady=15)
    blackQueenCastlingCheckButton = Checkbutton(frame, text="BlackQueenCastling", variable=blackQueenCastling)
    blackQueenCastlingCheckButton.grid(row=2, column=1, padx=15, pady=15)
    whiteKingCastlingCheckButton = Checkbutton(frame, text="WhiteKingCastling", variable=whiteKingCastling)
    whiteKingCastlingCheckButton.grid(row=3, column=0, padx=15, pady=15)
    whiteQueenCastlingCheckButton = Checkbutton(frame, text="WhiteQueenCastling", variable=whiteQueenCastling)
    whiteQueenCastlingCheckButton.grid(row=3, column=1, padx=15, pady=15)

    global depthTextBox
    depthLabel = Label(frame, text="Engine depth: ")
    depthLabel.grid(row=4, column=0, padx=15, pady=15)
    depthTextBox = Entry(frame)
    depthTextBox.insert(0, "20")
    depthTextBox.grid(row=4, column=1, padx=15, pady=15)
    

    frame.pack()
    # button.pack()

    # Start the GUI event loop
    root.mainloop()


    # with open("allDivs.pickle", "rb") as f:

    #     # Load the object from the file
    #     reloaded_object = pickle.load(f)

# driver.close()


if __name__ == "__main__":
    main()