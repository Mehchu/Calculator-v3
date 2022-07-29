import sys
import math
import regex
import re
from PyQt6.QtWidgets import (QWidget, QPushButton, QApplication,
                             QGridLayout, QButtonGroup, QLabel, QSizePolicy, QLineEdit)

displayString = ''
prevAns = ''
buttonGroup = QButtonGroup()

# Visual for GUI, used to create buttons (left to right)
buttonList = ['7', '8', '9', ' * ', ' ** ', '(',
              '4', '5', '6', ' / ', ' // ', ')',
              '1', '2', '3', ' + ', 'del', '!',
              ' = ', '0', '.', ' - ', 'ans', 'sqrt(']
# Set up lambdas for each operation to be called in line
op = {'+': lambda x, y: x + y,
      '-': lambda x, y: x - y,
      '*': lambda x, y: x * y,
      '/': lambda x, y: x / y,
      '**': lambda x, y: x ** y,
      '//': lambda x, y: x // y,
      }


def handleBrackets(equation):
    opening = equation.find('(')
    closing = equation.find(')')
    while opening != -1 and closing != -1:
        opening = equation.find('(')
        closing = equation.find(')')
        if opening != -1 and closing != -1:
            equation = equation.replace(equation[opening:closing + 1],
                                        calculate(equation[opening + 1:closing]))
    return equation
    # return str(calculate(matchObject[0][1:-1]))  # Return bracket replacement


def handleFactorial(matchObject):
    return str(math.factorial(int(matchObject[0][:-2])))


def handleSqrt(matchObject):
    return str(math.sqrt(int(matchObject[0][4:])))


def calculate(equation):
    global prevAns

    equation = handleBrackets(equation)
    # equation = regex.sub(r'(\((.+)\))', handleBrackets, equation)  # Replaces any brackets with expected output
    equation = regex.sub(r'.+! ', handleFactorial, equation)  # Replaces any factorials with expected output
    equation = regex.sub(r'sqrt.+', handleSqrt, equation)  # Replaces any sqrts with expected output
    equation = equation.split()
    if len(equation) % 2 == 0 and len(
            equation) != 1:  # Only allows complete expressions (which have to have an odd amount of terms)
        return "Syntax Error"
    while len(equation) >= 3:  # Keeps calculating and replacing until only answer is left
        try:
            answer = op[equation[1]](float(equation[0]), float(equation[2]))
        except ZeroDivisionError:
            return "Undefined"
        except ValueError:
            return "Syntax Error"
        equation.pop(0)
        equation.pop(0)
        equation[0] = str(answer)
    prevAns = equation[0]  # Store for ans button
    return equation[0]


def textEntered(called):
    global displayString
    character = buttonList[buttonGroup.id(called)]  # Finds which button was pressed
    # Checking for special inputs
    if character == ' = ':
        window.display.setText(displayString + ' = ' + calculate(displayString))
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
        self.line = QLineEdit(self)
        self.populate()

    def populate(self):
        grid = QGridLayout()
        grid.addWidget(self.display, 0, 0, 1, 6)  # Last should be changed to match # of columns
        grid.addWidget(self.line, 5, 0, 1, 5)
        textButton = QPushButton('Enter', self)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum,
                                 QSizePolicy.Policy.Minimum)  # Makes button scale vertically

        textButton.clicked.connect(textUpdateDisplay)
        textButton.setSizePolicy(sizePolicy)
        grid.addWidget(textButton, 5, 5, 1, 1)
        x = 0
        y = 1  # Accounts for display

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


def textUpdateDisplay():
    global displayString
    displayString = window.line.text()
    window.display.setText(displayString)


def main():
    global window
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
