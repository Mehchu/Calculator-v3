import sys
import math
import re
from PyQt6.QtWidgets import (QWidget, QPushButton, QApplication,
                             QGridLayout, QButtonGroup, QLabel, QSizePolicy, QLineEdit)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.display = QLabel(self)
        self.display.setStyleSheet("background-color: lightgray;border: 1px solid black")
        self.sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum,
                                      QSizePolicy.Policy.Minimum)

        self.displayString = ''
        self.prevAns = ''
        self.buttonGroup = QButtonGroup()

        # Visual for GUI, used to create buttons (left to right)
        self.buttonList = ['7', '8', '9', ' * ', ' ** ', '(',
                           '4', '5', '6', ' / ', ' // ', ')',
                           '1', '2', '3', ' + ', 'del', '!',
                           ' = ', '0', '.', ' - ', 'ans', 'sqrt(']
        # Set up lambdas for each operation to be called in line
        self.op = {'+': lambda x, y: x + y,
                   '-': lambda x, y: x - y,
                   '*': lambda x, y: x * y,
                   '/': lambda x, y: x / y,
                   '**': lambda x, y: x ** y,
                   '//': lambda x, y: x // y,
                   }
        # No clue what this does, somehow changes font size
        self.fontD = self.font()
        self.fontD.setPointSize(20)
        self.display.setFont(self.fontD)

        self.line = QLineEdit(self)
        self.line.setSizePolicy(self.sizePolicy)
        self.populate()

    def populate(self):
        grid = QGridLayout()
        grid.addWidget(self.display, 0, 0, 1, 6)  # Last should be changed to match # of columns
        grid.addWidget(self.line, 5, 0, 1, 5)
        textButton = QPushButton('Enter', self)
        # Makes button scale vertically

        textButton.clicked.connect(self.textUpdateDisplay)
        textButton.setSizePolicy(self.sizePolicy)
        grid.addWidget(textButton, 5, 5, 1, 1)
        x = 0
        y = 1  # Accounts for display

        for index, character in enumerate(self.buttonList):  # Makes grid
            button = QPushButton(character, self)
            button.setSizePolicy(self.sizePolicy)
            self.buttonGroup.addButton(button, index)
            grid.addWidget(button, y, x)

            x += 1
            if x >= 6:  # Comparison should be changed to match # of columns
                x = 0
                y += 1

        self.buttonGroup.buttonClicked.connect(self.textEntered)

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

    def textUpdateDisplay(self):
        self.displayString = self.line.text()
        self.display.setText(self.displayString)

    def textEntered(self, called):
        character = self.buttonList[self.buttonGroup.id(called)]  # Finds which button was pressed
        # Checking for special inputs
        if character == ' = ':
            if (answer := self.calculate(self.displayString)) == "Syntax Error":
                self.display.setText(answer)
            else:
                self.display.setText(self.displayString + ' = ' + answer)
            self.displayString = ''
            return
        elif character == 'ans':
            character = self.prevAns
        elif character == 'del':
            character = ''
            self.displayString = self.displayString[:-1]

        self.displayString += character
        self.display.setText(self.displayString)

    def calculate(self, equation):
        equation = self.handleBrackets(equation)
        equation = re.sub(r'\d+!+', self.handleFactorial, equation)  # Replaces any factorials with expected output
        equation = re.sub(r'sqrt.+', self.handleSqrt, equation)  # Replaces any sqrts with expected output
        equation = equation.split()
        if len(equation) % 2 == 0 and len(
                equation) != 1:  # Only allows complete expressions (which have to have an odd amount of terms)
            return "Syntax Error"
        while len(equation) >= 3:  # Keeps calculating and replacing until only answer is left
            try:
                answer = self.op[equation[1]](float(equation[0]), float(equation[2]))
            except ZeroDivisionError:
                return "Undefined"
            except ValueError:
                return "Syntax Error"
            equation.pop(0)
            equation.pop(0)
            equation[0] = str(answer)
        self.prevAns = equation[0]  # Store for ans button
        return equation[0]

    # Functions to deal with special characters
    def handleBrackets(self, equation):
        opening = equation.find('(')
        closing = equation.find(')')
        while opening != -1 and closing != -1:
            opening = equation.find('(')
            closing = equation.find(')')
            if opening != -1 and closing != -1:
                equation = equation.replace(equation[opening:closing + 1],
                                            self.calculate(equation[opening + 1:closing]))
        return equation

    def handleFactorial(self, matchObject):
        matchObject = matchObject[0]
        numberOfFactorials = matchObject.count('!')
        total = 1
        for number in range(int(matchObject[:-numberOfFactorials]))[::-numberOfFactorials]:
            total *= number + 1
        return str(total)

    def handleSqrt(self, matchObject):
        return str(math.sqrt(float(self.calculate(matchObject[0][4:]))))


def main():
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
