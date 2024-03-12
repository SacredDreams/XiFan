from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
import json
import random

class Main:
    def __init__(self):
        self.main_ui = QUiLoader().load("ui\\XiFan.ui")
        self.settings_ui = QUiLoader().load("ui\\settings.ui")
        self.pushButtons = [
            self.main_ui.pushButton, self.main_ui.pushButton_2, self.settings_ui.pushButton_3,
            self.settings_ui.pushButton_4, self.settings_ui.pushButton_5
        ]
        self.functions = [
            self.select, self.settings, self.add, self.delete, self.save
        ]
        self.options = []
        self.selected_options = []
        self.settings_dict = {}
        self.state = True

        self.init()

    def init(self):
        # read options
        with open("data\\options.json", "r", encoding="utf-8") as file:
            self.options = json.load(file)
        print("Options:\t\t", self.options)

        self.settings_ui.listWidget.clear()
        for i in self.options:
            self.settings_ui.listWidget.addItem(i)

        # read settings
        with open("data\\ui.json", "r", encoding="utf-8") as file:
            self.settings_dict = json.load(file)
        print("Settings:\t\t", self.settings_dict)

        self.main_ui.label.setStyleSheet(
            '''#label{border-width:1px; border-style:solid; border-color:black; font-size: %spx;}'''
            % self.settings_dict["font-size"]
        )
        self.settings_ui.lineEdit_2.setText(str(self.settings_dict["font-size"]))
        self.settings_ui.checkBox.setChecked(self.settings_dict["re"])

        # build connections
        if self.state:
            self.state = False
            for i in range(0, len(self.pushButtons)):
                self.pushButtons[i].clicked.connect(self.functions[i])

    def select(self):
        while True:
            if len(self.options) == len(self.selected_options):
                self.selected_options = []
            selected = self.options[random.randint(0, len(self.options) - 1)]
            if self.settings_dict["re"] is False:
                print("Selected:\t\t", selected)
                self.main_ui.label.setText(selected)
                self.selected_options = []
                break
            if self.settings_dict["re"] and selected in self.selected_options:
                continue
            else:
                print("Selected:\t\t", selected)
                self.main_ui.label.setText(selected)
                self.selected_options.append(selected)
                break

    def settings(self):
        self.settings_ui.show()

    def add(self):
        new = self.settings_ui.lineEdit.text()
        self.options.append(new)
        with open("data\\options.json", "w", encoding="utf-8") as file:
            json.dump(self.options, file, ensure_ascii=False)
        self.settings_ui.lineEdit.clear()
        self.init()

    def delete(self):
        selected_index = self.settings_ui.listWidget.currentRow()
        self.settings_ui.listWidget.takeItem(selected_index)
        self.options.remove(self.options[selected_index])
        with open("data\\options.json", "w", encoding="utf-8") as file:
            json.dump(self.options, file, ensure_ascii=False)
        self.init()

    def save(self):
        try:
            self.settings_dict["font-size"] = int(self.settings_ui.lineEdit_2.text())
            self.settings_dict["re"] = self.settings_ui.checkBox.isChecked()
            with open("data\\ui.json", "w", encoding="utf-8") as file:
                json.dump(self.settings_dict, file, ensure_ascii=False)
            self.settings_ui.close()
            self.init()
        except:
            self.settings_ui.setWindowTitle("设置 - 参数错误！！！")

if __name__ == '__main__':
    App = QApplication()
    run = Main()
    run.main_ui.show()
    App.exec_()