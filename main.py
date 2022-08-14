import math
import re
import sys

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
        self.buttonList = ['7', '8', '9', ' * ', ' ** ', '√', 'log(', 'CLR',
                           '4', '5', '6', ' / ', 'π', 'e', 'ln(', 'DEL',
                           '1', '2', '3', ' + ', 'sin(', 'cos(', 'tan(', '!',
                           'ANS', '0', '.', ' - ', '(', ')', 'RAND', '=']

        self.columns = len(self.buttonList) // 4
        # Set up lambdas for each operation to be called in line
        self.op = {'+': lambda x, y: x + y,
                   '-': lambda x, y: x - y,
                   '*': lambda x, y: x * y,
                   '/': lambda x, y: x / y,
                   '**': lambda x, y: x ** y,
                   '//': lambda x, y: x // y,
                   }

        # Set up text input
        self.line = QLineEdit(self)
        self.line.setSizePolicy(self.sizePolicy)
        self.populate()

    def populate(self):
        grid = QGridLayout()
        grid.addWidget(self.display, 0, 0, 1, self.columns)  # Last should be changed to match # of columns
        grid.addWidget(self.line, 5, 0, 1, self.columns - 1)
        text_button = QPushButton('ENTER', self)
        # Makes button scale vertically

        text_button.clicked.connect(self.textUpdateDisplay)
        text_button.setSizePolicy(self.sizePolicy)
        grid.addWidget(text_button, 5, self.columns - 1, 1, 1)
        x = 0
        y = 1  # Accounts for display

        for index, character in enumerate(self.buttonList):  # Makes grid
            button = QPushButton(character, self)
            button.setSizePolicy(self.sizePolicy)
            self.buttonGroup.addButton(button, index)
            grid.addWidget(button, y, x)

            x += 1
            if x >= self.columns:  # Comparison should be changed to match # of columns
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
        if character == '=':
            if (answer := self.calculate(self.displayString)) == "Syntax Error":
                self.display.setText(answer)
            else:
                self.display.setText(self.displayString + ' = ' + answer)
            self.displayString = ''
            return
        elif character == 'ANS':
            character = self.prevAns
        elif character == 'DEL':
            character = ''
            self.displayString = self.displayString[:-1]
        elif character == 'CLR':
            character = ''
            self.displayString = ''
        self.displayString += character
        self.display.setText(self.displayString)

    def calculate(self, equation):

        equation = self.handleBrackets(equation)  # Replaces any brackets with expected output

        equation = re.sub(r'√\S+', self.handleSqrt, equation)  # Replaces any sqrts with expected output

        equation = re.sub(r'sin\S+', self.handleSine, equation)  # Replaces any sin with expected output
        equation = re.sub(r'cos\S+', self.handleCosine, equation)  # Replaces any cos with expected output
        equation = re.sub(r'tan\S+', self.handleTangent, equation)  # Replaces any tan with expected output

        equation = re.sub(r'log\S+', self.handleLogarithm, equation)  # Replaces any log with expected output
        equation = re.sub(r'ln\S+', self.handleNaturalLogarithm, equation)  # Replaces any ln with expected output

        equation = re.sub(r'\S+e', self.handleE, equation)  # Replaces any e with expected output
        equation = re.sub(r'\S+π', self.handlePI, equation)  # Replaces any pi with expected output

        equation = re.sub(r'\d+!+', self.handleFactorial, equation)  # Replaces any factorials with expected output

        equation = equation.split()
        while len(equation) >= 3:  # Keeps calculating and replacing until only answer is left
            try:
                # Manual implementation of BIDMAS
                for index, term in enumerate(equation):
                    if term == '**' or term == '//':
                        answer = self.op[equation[index]](float(equation[index - 1]), float(equation[index + 1]))
                        equation.pop(index - 1)
                        equation.pop(index - 1)
                        equation[index - 1] = str(answer)
                for index, term in enumerate(equation):
                    if term == '*' or term == '/':
                        answer = self.op[equation[index]](float(equation[index - 1]), float(equation[index + 1]))
                        equation.pop(index - 1)
                        equation.pop(index - 1)
                        equation[index - 1] = str(answer)
                for index, term in enumerate(equation):
                    if term == '+' or term == '-':
                        answer = self.op[equation[index]](float(equation[index - 1]), float(equation[index + 1]))
                        equation.pop(index - 1)
                        equation.pop(index - 1)
                        equation[index - 1] = str(answer)
            except ZeroDivisionError:
                return "Undefined"
            except ValueError:
                return "Syntax Error"
        self.prevAns = equation[0]  # Store for answer button
        return equation[0]

    # Functions to deal with special characters
    def handleBrackets(self, equation):
        if equation.count('(') != equation.count(')'):
            return "Syntax Error"
        opening = equation.find('(')
        closing = equation.find(')')
        while opening != -1 and closing != -1:
            opening = equation.find('(')
            closing = equation.find(')')
            if opening != -1 and closing != -1:
                equation = equation.replace(equation[opening:closing + 1],
                                            self.calculate(equation[opening + 1:closing]))
        return equation

    @staticmethod
    def handleFactorial(match_object):
        match_object = match_object[0]
        number_of_factorials = match_object.count('!')
        total = 1
        for number in range(int(match_object[:-number_of_factorials]))[::-number_of_factorials]:
            total *= number + 1
        return str(total)

    def handleSqrt(self, matchObject):
        return str(math.sqrt(float(self.calculate(matchObject[0][1:]))))

    @staticmethod
    def handleE(matchObject):
        return str(math.e * float(matchObject[0][:-1]))

    @staticmethod
    def handlePI(matchObject):
        return str(math.pi * float(matchObject[0][:-1]))

    def handleSine(self, matchObject):
        return str(math.sin(float(self.calculate(matchObject[0][3:])) / (180 / math.pi)))

    def handleCosine(self, matchObject):
        return str(math.cos(float(self.calculate(matchObject[0][3:])) / (180 / math.pi)))

    def handleTangent(self, matchObject):
        return str(math.tan(float(self.calculate(matchObject[0][3:])) / (180 / math.pi)))

    def handleLogarithm(self, matchObject):
        return str(math.log10(float(self.calculate(matchObject[0][3:]))))

    def handleNaturalLogarithm(self, matchObject):
        return str(math.log(float(self.calculate(matchObject[0][2:]))))


def main():
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
