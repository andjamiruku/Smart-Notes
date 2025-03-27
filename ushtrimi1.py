from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import json

note = {
    "Welcome!":{
        "text":"This is the bet note taking app in the world",
        "tags":["good","instuctions"]
    }
}

with open("notes.json","w") as file:
    json.dump(note,file)

app = QApplication([])
notes_win = QWidget()
notes_win.setWindowTitle("Smart Notes")
notes_win.resize(900,600)

list_notes = QListWidget()
list_notes_label = QLabel("List of notes")

create_button = QPushButton("Create Button")
delete_button = QPushButton ("Delete Button")
save_note_button = QPushButton("Save note")

list_tags = QListWidget()
list_tags_label = QLabel("List of tags")
field_tag = QLineEdit("")
field_tag.setPlaceholderText("Enter tag...")

add_button = QPushButton("Add to notes")
de_tag_button = QPushButton("Untag from note")
search_button = QPushButton("Search notes by tag")

field_text = QTextEdit()

layout_notes = QHBoxLayout()
column1 = QVBoxLayout()
column1.addWidget(field_text) 

column2 = QVBoxLayout()
column2.addWidget(list_notes_label)
column2.addWidget(list_notes)

row1 = QHBoxLayout()
row1.addWidget(create_button)
row1.addWidget(delete_button)

row2 = QHBoxLayout()
row2.addWidget(save_note_button)
column2.addLayout(row1)
column2.addLayout(row2)

column2.addWidget(list_tags_label)
column2.addWidget(list_tags)
column2.addWidget(field_tag)

row3 = QHBoxLayout()
row3.addWidget(add_button)
row3.addWidget(de_tag_button)

row4 = QHBoxLayout()
row4.addWidget(search_button)

column2.addLayout(row3)
column2.addLayout(row4)

layout_notes.addLayout(column1,stretch=2)
layout_notes.addLayout(column2,stretch=1)

notes_win.setLayout(layout_notes)

def add_note():
    note_name,ok = QInputDialog.getText(notes_win,"Add note","Note name:")
    if ok and note_name != "":
        note[note_name] = {"text":"","tags":[]}
        list_notes.addItem(note_name)
        list_tags.addItems(note[note_name]["tags"])
    
def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        note[key]["text"] = field_text.toPlainText()

        with open("notes.json","w") as file:
            json.dump(note,file,sort_keys = True)
            print(note)
    else:
        print("Note to save is not selected!")

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del note[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(note)
        with open("notes.json","w") as file:
            json.dump(note,file,sort_keys=True,ensure_ascii=False)
        print(note)
    else:
        print("Note to be deleted is not selected")

def show_note():
    key = list_notes.selectedItems()[0].text()
    print(key)
    field_text.setText(note[key]["text"])
    list_tags.clear()
    list_tags.addItems(note[key]["tags"])

def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        
        if not tag in note[key]["tags"]:
            note[key]["tags"].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
        with open("notes.json","w") as file:
            json.dump(note,file,sort_keys=True,ensure_ascii=False)
        print(note)
    else:
        print("Note to add a tag is not selected!")

def del_tag():
    if list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()

        note[key]["tags"].remove(tag)
        list_tags.clear()
        list_tags.addItems(note[key]["tags"])
        with open("notes.json","w") as file:
            json.dump(note,file,sort_keys=True,ensure_ascii=False)
        print(note)
    else:
        print("Tag to delete is not selected!")

def search_tag():
    print(search_button.text())
    tag = field_tag.text()
    if search_button.text() == "Search notes by tag" and tag :
        print(tag)
        notes_filtered ={}
        for notes in note:
            if tag in note[notes]["tags"]:
                notes_filtered[notes] = note[notes]
        search_button.setText("Reset search")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
        print(search_button.text())
    elif search_button.text() == "Reset search":
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(note)
        search_button.setText("Search notes by tag")
        print(search_button.text())
    else:
        pass
create_button.clicked.connect(add_note)
list_notes.itemClicked.connect(show_note)
save_note_button.clicked.connect(save_note)
delete_button.clicked.connect(del_note)
add_button.clicked.connect(add_tag)
de_tag_button.clicked.connect(del_tag)
search_button.clicked.connect(search_tag)

notes_win.show()
with open("notes.json","r") as file:
    note = json.load(file)
list_notes.addItems(note)
app.exec_()