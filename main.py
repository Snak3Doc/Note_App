# main.py
#* THIS IS THE GOOD ONE!!!!!!!!
### Imports ###
import sys
import json

from PyQt6 import QtCore
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton,
    QLabel, QGroupBox, QLineEdit, QTextEdit,
    QInputDialog, QListWidget, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtCore import Qt

# from rich import print # Color codes data types when we print them
# from rich.traceback import install
# install(show_locals=True) # Creates custom error messages and displays variable values in the terminal


### Data ###
#note_data = {} # All the note and tag data will be stored here while the program is running


### Main Window Class ###
class MainWin(QMainWindow): # Make a copy of QMainWindow, so we can modify it for our purposes.
    def __init__(self): # The constructor builds the application at runtime.
        super().__init__() # The super constructor allows our child class to communicate with the parent

        self.build_ui() # Call the method to build the UI
        self.event_handlers()


    def build_ui(self):
        ### Window Setup ###
        self.setGeometry(100, 100, 900, 600) # Set the window postion and size
        self.setWindowTitle("Note App")

        ### Build UI ###
        ## Text Edit Setup
        # Widgets
        self.txt_edit = QTextEdit(self) # Where we view and edit our notes

        # Layouts
        lyt_main_text = QVBoxLayout()

        # Setup
        lyt_main_text.addWidget(self.txt_edit)


        ## Tools Setup
        # Widgets
        self.lbl_notes = QLabel("Notes", self)
        self.lbl_tags = QLabel("Tags", self)

        self.lst_notes = QListWidget(self)
        self.lst_tags = QListWidget(self)

        self.btn_note_add = QPushButton("Create", self)
        self.btn_note_delete = QPushButton("Delete", self)
        self.btn_tag_add = QPushButton("Add", self)
        self.btn_tag_delete = QPushButton("Delete", self)
        self.btn_tag_search = QPushButton("Search", self)

        self.txt_search = QLineEdit(self, placeholderText="Enter a tag...")

        # Layouts
        lyt_main_tools = QVBoxLayout()
        lyt_tools_notes = QHBoxLayout()
        lyt_tools_tags = QHBoxLayout()

        # Setup
        lyt_tools_notes.addWidget(self.btn_note_add)
        lyt_tools_notes.addWidget(self.btn_note_delete)

        lyt_tools_tags.addWidget(self.btn_tag_add)
        lyt_tools_tags.addWidget(self.btn_tag_search)
        lyt_tools_tags.addWidget(self.btn_tag_delete)

        lyt_main_tools.addWidget(self.lbl_notes)
        lyt_main_tools.addWidget(self.lst_notes)
        lyt_main_tools.addLayout(lyt_tools_notes)
        lyt_main_tools.addWidget(self.lbl_tags)
        lyt_main_tools.addWidget(self.lst_tags)
        lyt_main_tools.addWidget(self.txt_search)
        lyt_main_tools.addLayout(lyt_tools_tags)


        ## Main Win Setup
        # Wigets
        central_widget = QWidget()

        # Layouts
        lyt_main = QHBoxLayout()

        # Setup
        lyt_main.addLayout(lyt_main_text)
        lyt_main.addLayout(lyt_main_tools)

        central_widget.setLayout(lyt_main)
        self.setCentralWidget(central_widget)


    def event_handlers(self):
        #* select widget | detect event type | connect to an action/method
        self.txt_edit.focusOutEvent = self.auto_save
        self.lst_notes.itemClicked.connect(self.note_show)
        self.btn_note_add.clicked.connect(self.note_create)
        self.btn_note_delete.clicked.connect(self.note_delete)
        self.btn_tag_add.clicked.connect(self.tag_create)
        self.btn_tag_delete.clicked.connect(self.tag_delete)
        self.btn_tag_search.clicked.connect(self.tag_search)

    def auto_save(self, event):
        if self.lst_notes.selectedItems(): # If the list of selected items is not empty
            print("Auto save running")
            note_name = self.lst_notes.selectedItems()[0].text()
            note_data[note_name]["text"] = self.txt_edit.toPlainText()
            self.json_write()


    def json_read(self):
        with open("note_data.json", "r") as file:
            temp_data = json.load(file)
        self.lst_notes.addItems(temp_data) #* addItems
        return temp_data #* When we call this method we will save all the temp_data to the note_data dictionary
    

    def json_write(self):
        with open("note_data.json", "w") as file:
            json.dump(note_data, file, sort_keys=True, ensure_ascii=False, indent=4)

    def note_show(self):
        note_name = self.lst_notes.selectedItems()[0].text() # Get the name of the selected note
        self.txt_edit.setText(note_data[note_name]["text"]) # Get & Set the text of the selected note
        self.lst_tags.clear() # Clear the list of tags
        self.lst_tags.addItems(note_data[note_name]["tags"]) # Get & Set the tags of the selected note

    def note_create(self):
        note_name, state = QInputDialog.getText(main_win, "Create New Note", "Enter Note Name:")
        if any(char.isalpha() for char in note_name): # Check to see if there are real characters in the name
            note_data[note_name] = {"tags" : [], "text" : ""} # Creates a new note in the dictionary
            self.lst_notes.clear() # Clear the list of notes
            self.lst_notes.addItems(note_data) # Add the note names from the dictionary
            self.lst_tags.clear() # Clear the list of tags
            self.lst_tags.addItems(note_data[note_name]["tags"]) # Add the tags of the new note

    def note_delete(self):
        if self.lst_notes.selectedItems():
            note_name = self.lst_notes.selectedItems()[0].text()
            del note_data[note_name]
            self.lst_notes.clear()
            self.lst_tags.clear()
            self.txt_edit.clear()
            self.lst_notes.addItems(note_data)
            self.json_write()

    def tag_create(self):
        if self.lst_notes.selectedItems():
            note_name = self.lst_notes.selectedItems()[0].text()
            tag_name = self.txt_search.text()
            if tag_name not in note_data[note_name]["tags"]: # Check if the tag already exists for this note
                note_data[note_name]["tags"].append(tag_name) # Add the tag to the selected note item
                self.lst_tags.addItem(tag_name)
                self.txt_search.clear()
                self.json_write()

    def tag_delete(self):
        if self.lst_notes.selectedItems() and self.lst_tags.selectedItems():
            note_name = self.lst_notes.selectedItems()[0].text()
            tag_name = self.lst_tags.selectedItems()[0].text()
            note_data[note_name]["tags"].remove(tag_name)
            self.lst_tags.clear()
            self.lst_tags.addItems(note_data[note_name]["tags"])
            self.json_write()


    def tag_search(self):
        if self.txt_search.text():
            query = self.txt_search.text()
            if self.btn_tag_search.text() == "Search" and query:
                notes_filtered = {}
                for note_name in note_data:
                    if query in note_data[note_name]["tags"]:
                        notes_filtered[note_name] = note_data[note_name]
                self.btn_tag_search.setText("Reset")
                self.lst_notes.clear()
                self.lst_tags.clear()
                self.lst_notes.addItems(notes_filtered)

            elif self.btn_tag_search.text() == "Reset":
                self.txt_search.clear()
                self.lst_notes.clear()
                self.lst_tags.clear()
                self.lst_notes.addItems(note_data)
                self.btn_tag_search.setText("Search")





### Application Execution ###
if __name__ == '__main__':
    app = QApplication(sys.argv) # The app object is like the engine for our application
    app.setStyle("Windows")
    #stylesheet.set_style(app)
    main_win = MainWin()
    main_win.show() # Display the app on the screen at runtime
    note_data = main_win.json_read()
    sys.exit(app.exec()) 
    # app.exec starts the engine, when the app is closed it communicates the event to
    #   windows through sys.exit.