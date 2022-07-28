import sys
import math
import re

from PyQt6.QtWidgets import (QWidget, QPushButton, QApplication,
                             QGridLayout, QButtonGroup, QLabel, QSizePolicy)

displayString = ''
prevAns = ''
buttonGroup = QButtonGroup()

# Visual for GUI, used to create buttons (left to right)
buttonList = ['7', '8', '9', ' * ', ' ** ', '(',
              '4', '5', '6', ' / ', ' // ', ')',
              '1', '2', '3', ' + ', 'del', 'no',
              ' = ', '0', '.', ' - ', 'ans', 'no']
# Set up lambdas for each operation to be called in line
op = {'+': lambda x, y: x + y,
      '-': lambda x, y: x - y,
      '*': lambda x, y: x * y,
      '/': lambda x, y: x / y,
      '**': lambda x, y: x ** y,
      '//': lambda x, y: x // y,
      }


def handleMatch(matchObject):
    return calculate(matchObject[0][1:-1])  # Return bracket replacement


def calculate(string):
    global prevAns
    string = re.sub(r'\((.*)\)', handleMatch, string)  # Replaces any brackets with the sum contained within
    string = string.split()
    if len(string) % 2 == 0:  # Only allows complete expressions (which have to have an odd amount of terms)
        return "Syntax Error"
    while len(string) >= 3:  # Keeps calculating and replacing until only answer is left
        try:
            answer = op[string[1]](float(string[0]), float(string[2]))
        except ZeroDivisionError:
            return "Undefined"
        string.pop(0)
        string.pop(0)
        string[0] = str(answer)
    prevAns = string[0]  # Store for ans button
    return string[0]


def textEntered(called):
    global displayString
    character = buttonList[buttonGroup.id(called)]  # Finds which button was pressed
    # Checking for special inputs
    if character == ' = ':
        window.display.setText(calculate(displayString))
        displayString = ''
        return
    elif character == 'ans':
        character = prevAns
    elif character == 'del':
        character = ''
        displayString = displayString[:-1]

    displayString += character
    window.display.setText(displayString)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.display = QLabel(self)
        self.display.setStyleSheet("background-color: lightgray;border: 1px solid black")
        # No clue what this does, somehow changes font size
        self.fontD = self.font()
        self.fontD.setPointSize(20)
        self.display.setFont(self.fontD)
        self.populate()

    def populate(self):
        grid = QGridLayout()
        grid.addWidget(self.display, 0, 0, 1, 6)  # Last should be changed to match # of columns

        x = 0
        y = 1  # Accounts for display
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)  # Makes button scale vertically
        for index, character in enumerate(buttonList):  # Makes grid
            button = QPushButton(character, self)
            button.setSizePolicy(sizePolicy)
            buttonGroup.addButton(button, index)
            grid.addWidget(button, y, x)

            x += 1
            if x >= 6:  # Comparison should be changed to match # of columns
                x = 0
                y += 1

        buttonGroup.buttonClicked.connect(textEntered)

        # So GUI scales sensibly
        grid.setRowStretch(0, 3)
        for row in range(grid.rowCount() - 1):
            row += 1
            grid.setRowStretch(row, 2)
        # Final setup
        grid.setSpacing(5)
        self.setLayout(grid)

        self.setGeometry(300, 300, 200, 200)
        self.setWindowTitle('Calculator')

        self.show()


def main():
    global window
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())


if __name__ == '__main__':
    # print(string)  # For testing specific equations
    main()
