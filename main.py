# Import necessary libraries
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QMenuBar, QStatusBar, QWidget, \
    QCalendarWidget
from PyQt5 import uic
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QTextCharFormat, QPalette
import sys


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # Load the UI file
        uic.loadUi("calendar.ui", self)

        # Find the necessary UI elements
        self.calendar = self.findChild(QCalendarWidget, "calendarWidget")
        self.label = self.findChild(QLabel, "label")
        self.selectButton = self.findChild(QPushButton, "pushButton")
        self.clearButton = self.findChild(QPushButton, "pushButton_2")
        self.resultLabel = self.findChild(QLabel, "label_2")

        # Initialize variables
        self.from_date = None
        self.to_date = None

        # Define the format for highlighting
        self.highlighter_format = QTextCharFormat()
        self.highlighter_format.setBackground(self.palette().brush(QPalette.Highlight))
        self.highlighter_format.setForeground(self.palette().color(QPalette.HighlightedText))

        # Connect signals to slots
        self.calendar.selectionChanged.connect(self.grab_date)
        self.selectButton.clicked.connect(self.retrieve_date_range)
        self.clearButton.clicked.connect(self.clear_date_range)

        # Show the main window
        self.show()

    def grab_date(self):
        # Update the label with the selected date
        selected_date = self.calendar.selectedDate()
        self.label.setText(str(selected_date.toString()))

        # Check if the Shift key is pressed for selecting date range
        if QApplication.keyboardModifiers() == Qt.ShiftModifier:
            if self.from_date is None:
                # Set the start date for the range
                self.from_date = selected_date
            else:
                # Set the end date for the range and highlight the range in the calendar
                self.to_date = selected_date
                self.highlight_range()

    def highlight_range(self):
        # Highlight the selected date range in the calendar
        if self.from_date and self.to_date:
            start_date = min(self.from_date, self.to_date)
            end_date = max(self.from_date, self.to_date)
            d1 = start_date
            while d1 <= end_date:
                self.calendar.setDateTextFormat(d1, self.highlighter_format)
                d1 = d1.addDays(1)

    def retrieve_date_range(self):
        # Retrieve the selected date range and display it in the result label
        if self.from_date and self.to_date:
            start_date = min(self.from_date, self.to_date)
            end_date = max(self.from_date, self.to_date)
            date_range = [start_date.addDays(i) for i in range((end_date.toPyDate() - start_date.toPyDate()).days + 1)]
            date_list = [str(date.toString()) for date in date_range]
            result = ', '.join(date_list)
            self.resultLabel.setText(result)
        else:
            self.resultLabel.setText("No date range is selected")

    def clear_date_range(self):
        # Clear the selected date range and reset the calendar
        self.from_date = None
        self.to_date = None
        self.calendar.setSelectedDate(QDate.currentDate())

        # Reset format for all dates in the calendar
        start_date = self.calendar.minimumDate()
        end_date = self.calendar.maximumDate()
        current_date = start_date
        format = QTextCharFormat()
        while current_date <= end_date:
            self.calendar.setDateTextFormat(current_date, format)  
            current_date = current_date.addDays(1)

        self.resultLabel.setText("")



app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
