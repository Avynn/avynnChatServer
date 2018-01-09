import curses, time, os, locale

def receiveMessage(window, div, message){
    cursorY, cursorX = window.getyx()
    window.addstr((cursorY + 1), 0, message)
    cursorY, cursorX = window.getyx()
    if (cursorY > div):
        window.scroll((cursorY - div))
}

locale.setlocale(locale.LC_ALL, "")
code = locale.getpreferredencoding()

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(1)

height, width = stdscr.getmaxyx()

div = int(round(height - (height/6)))
divHeight = int(round(height/6))

receiveMessageBox = curses.newwin(div, width, 0, 0)
sendMessageBox = curses.newwin(divHeight, width, div, 0)

receiveMessageBox.addstr(0, 0, message1)
receiveMessageBox.addstr(1, 0, message2)
receiveMessageBox.refresh()

curses.echo()
userMessage = sendMessageBox.getstr(0,0)
curses.noecho()
sendMessageBox.clear()
sendMessageBox.refresh()

receiveMessageBox.addstr(2, 0, userMessage)
receiveMessageBox.refresh()


curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()

