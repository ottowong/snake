import curses
from random import randint
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
import sqlite3
from datetime import datetime
import os

height = 20
width = 40

score = 0

wallDeath = False

food = [1,1]

snake = [[1,1]]
while(food == snake[0]):
    food = [randint(1,height-2),randint(1,width-2)]

stdscr = curses.initscr()
win = curses.newwin(height, width, 0, 0)    
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.nodelay(1)

key = KEY_RIGHT
head = ">"

lost = False

win.addch(food[0], food[1], "*")

def lose():
    global lost
    lost = True
    win.addstr(height-1, int((width/2)-5), " YOU LOSE ")
    key = -1
    while (key != 27): # wait for press esc
        key = win.getch()

while key != 27: # escape
    win.border(0)
    win.addstr(0, 2, " Score : " + str(score) + " ")
    # win.addstr(0, 27, " SNAKE ")
    speed = int(150 - (len(snake)/5 + len(snake)/10)%120)  
    if(speed < 0):
        speed = 0
    win.timeout(speed)
    oldKey = key
    event = win.getch()
    key = key if event == -1 else event 

    if(key == 32):
        win.addstr(height-1, int((width/2)-4), " paused ")
        key = -1
        while (key != 32 and key != 27):
            key = win.getch()

    if key not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27, 119, 97, 115, 100]:
        key = oldKey

    if(key == KEY_DOWN or key == 115):
        snake.insert(0, [snake[0][0] + 1, snake[0][1]])
        head = "v"
    elif(key == KEY_UP or key == 119):
        snake.insert(0, [snake[0][0] - 1, snake[0][1]])
        head = "^"
    elif(key == KEY_LEFT or key == 97):
        snake.insert(0, [snake[0][0], snake[0][1] - 1])
        head = "<"
    elif(key == KEY_RIGHT or key == 100):
        snake.insert(0, [snake[0][0], snake[0][1] + 1])
        head = ">"

    # check if we've hit a wall
    if(snake[0][0] == height-1): # down
        snake[0][0] = 1
        if wallDeath:
            lose()
    elif(snake[0][0] == 0): # up
        snake[0][0] = height - 2
        if wallDeath:
            lose()
    elif(snake[0][1] == width-1): # right
        snake[0][1] = 1
        if wallDeath:
            lose()
    elif(snake[0][1] == 0): # left
        snake[0][1] = width - 2
        if wallDeath:
            lose()

    try:
        win.addch(snake[1][0], snake[1][1], "#")
    except:
        pass
    win.addch(snake[0][0], snake[0][1], head)

    if(snake[0] in snake[1:]): # death condition
        lose()

    if(snake[0] != food): # if snake is not currently eating food
        removed = snake.pop()
        win.addch(removed[0],removed[1], " ")
    else: # if snake is currently eating food
        score += 1 
        while(food in snake):
            food = [randint(1,height-2),randint(1,width-2)]
        win.addch(food[0],food[1], "*")

    if(lost):
        break

curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()

conn = sqlite3.connect("scores.db")
c = conn.cursor()

try:
    c.execute("CREATE TABLE scores ([id] INTEGER PRIMARY KEY,[name] text, [score] integer, [Date] date)")
    conn.commit()
except:
    pass

c.execute("SELECT name, score, date FROM scores ORDER BY score DESC LIMIT 3")
records = c.fetchall()

os.system('cls' if os.name == 'nt' else 'clear')

print("HIGH SCORES\n")

for row in records:
    print("Name: "+str(row[0])+"\nScore: "+str(row[1])+"\nDate: "+str(row[2]+"\n"))

now = datetime.now()
print("Your score: " + str(score))
if(input("Would you like to save your score? (Y/N): ").lower() == "y"):
    name = input("Enter your name: ")
    c.execute("INSERT INTO scores (name, score, Date) VALUES (?, ?, ?)", [name, score, now])
    conn.commit()
os.system('cls' if os.name == 'nt' else 'clear')