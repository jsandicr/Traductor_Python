import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QTextEdit, QComboBox, QHBoxLayout, QPushButton, QDialog
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon
from googletrans import Translator
import subprocess
from gtts import gTTS
import pygame
import os

languages = [
    {
        "name": "English",
        "code": "en" 
    },
    {
        "name": "Spanish",
        "code": "es" 
    },
    {
        "name": "Italian",
        "code": "it",
    },
    {
        "name": "Portuguese",
        "code": "pt",
    },
    {
        "name": "French",
        "code": "fr",
    },
    {
        "name": "Russian",
        "code": "ru",
    },
    {
        "name": "Japanese",
        "code": "ja",
    },
    {
        "name": "Korean",
        "code": "ko",
    },
    {
        "name": "Chinese (Simplified)",
        "code": "zh-CN",
    }
]

class TranslatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        pyqtSignal()
        pygame.init()
        self.translator_ui = None

        self.initUI()
        self.debounce_timer = QTimer()
        self.debounce_timer.setInterval(1000)
        self.debounce_timer.setSingleShot(True)
        self.debounce_timer.timeout.connect(self.debounce_timeout)

    def initUI(self):

        self.setWindowTitle("NeuraTranslate")
        self.setGeometry(100, 100, 800, 600)

        with open("styles.css", "r") as css_file:
            self.setStyleSheet(css_file.read())

        self.label_language_1_text = ""
        self.label_language_2_text = ""

        layout = QVBoxLayout()

        hbox_layout = QHBoxLayout()
        hbox_layout.setObjectName("hboxLayout")
        hbox_layout2 = QHBoxLayout()
        hbox_layout2.setObjectName("hboxLayout")
        hbox_layout3 = QHBoxLayout()
        hbox_layout3.setObjectName("hboxLayout")
        hbox_layout4 = QHBoxLayout()
        hbox_layout4.setObjectName("hboxLayout")

        copy_button = QPushButton()
        icon = QIcon("copy-icon.svg")
        copy_button.setIcon(icon)
        copy_button.setFixedSize(60, 50)
        copy_button.clicked.connect(self.copy_to_clipboard_1)

        copy_button2 = QPushButton()
        copy_button2.setIcon(icon)
        copy_button2.setFixedSize(60, 50)
        copy_button2.clicked.connect(self.copy_to_clipboard_2)
        
        self.listen_button = QPushButton()
        icon = QIcon("sound-icon.svg")
        self.listen_button.setIcon(icon)
        self.listen_button.setFixedSize(60, 50)
        self.listen_button.clicked.connect(self.text_to_speech_1)
        
        self.listen_button2 = QPushButton()
        self.listen_button2.setIcon(icon)
        self.listen_button2.setFixedSize(60, 50)
        self.listen_button2.clicked.connect(self.text_to_speech_2)

        self.label_language_1 = QLabel("Spanish")
        self.label_language_1.setObjectName("languageTitle1")
        self.label_language_1.setAlignment(Qt.AlignRight)

        self.label_language_2 = QLabel("English")
        self.label_language_2.setObjectName("languageTitle2")

        self.empty_label = QLabel("")
        self.select_language_label = QLabel("NeuraTranslate")
        self.select_language_label.setObjectName("titulo")
        self.select_language_label.setAlignment(Qt.AlignRight)

        self.languages_combobox = QComboBox()
        self.languages_combobox.setObjectName("languagesComboBox")
        language_names = [language["name"] for language in languages]
        self.languages_combobox.addItems(language_names)
        
        self.languages_combobox.activated.connect(self.languages_combobox_activated)

        self.languages_combobox2 = QComboBox()
        self.languages_combobox2.setObjectName("languagesComboBox")
        self.languages_combobox2.addItem("Automatic detectic")
        language_names = [language["name"] for language in languages]
        self.languages_combobox2.addItems(language_names)
        
        self.languages_combobox2.activated.connect(self.languages_combobox2_activated) 

        self.input_text_edit = QTextEdit()
        self.input_text_edit.setObjectName("inputTextEdit")
        self.input_text_edit.textChanged.connect(self.reset_debounce_timer)

        self.translated_text_edit = QTextEdit()
        self.translated_text_edit.setReadOnly(True)
        self.translated_text_edit.setObjectName("translatedTextEdit")

        hbox_layout3.addWidget(self.select_language_label)
        hbox_layout3.addWidget(self.empty_label)
        layout.addLayout(hbox_layout3)
        hbox_layout.addWidget(self.languages_combobox2)
        hbox_layout.addWidget(copy_button)
        hbox_layout.addWidget(self.listen_button)
        hbox_layout.addWidget(self.empty_label)
        layout.addLayout(hbox_layout)
        layout.addWidget(self.input_text_edit)
        layout.addWidget(self.empty_label)
        hbox_layout2.addWidget(self.languages_combobox)
        hbox_layout2.addWidget(copy_button2)
        hbox_layout2.addWidget(self.listen_button2)
        hbox_layout2.addWidget(self.empty_label)
        layout.addLayout(hbox_layout2)
        layout.addWidget(self.translated_text_edit)
        hbox_layout4.addWidget(self.label_language_1)
        hbox_layout4.addWidget(self.label_language_2)
        layout.addLayout(hbox_layout4)

        container = QWidget()
        container.setObjectName("centralWidget")
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.language_mapping = {language["name"]: language["code"] for language in languages}

        self.translator = Translator()

    def copy_to_clipboard_1(self):
        input_text = self.input_text_edit.toPlainText()
        if not input_text.strip():
            return
        subprocess.run(['clip'], input=input_text, text=True)

    def copy_to_clipboard_2(self):
        translated_text = self.translated_text_edit.toPlainText()
        if not translated_text.strip():
            return
        subprocess.run(['clip'], input=translated_text, text=True)

    def text_to_speech_1(self):
        lang = self.label_language_1_text
        if(lang == ""):
            return
        
        message = self.input_text_edit.toPlainText()
        speech_file = 'data_1.mp3'
        speech = gTTS(text=message, lang=lang)
        speech.save(speech_file)

        sound = pygame.mixer.Sound(speech_file)
        sound.play()

        pygame.time.wait(int(sound.get_length() * 1000))

        sound.stop()
        os.remove(speech_file)
    
    def text_to_speech_2(self):
        lang = self.label_language_2_text
        if(lang == ""):
            return
        
        message = self.translated_text_edit.toPlainText()
        speech_file = 'data_2.mp3'
        speech = gTTS(text=message, lang=lang)
        speech.save(speech_file)

        sound = pygame.mixer.Sound(speech_file)
        sound.play()

        pygame.time.wait(int(sound.get_length() * 1000))

        sound.stop()
        os.remove(speech_file)

    def languages_combobox_activated(self, index):
        if index > 0:
            self.translate_text_realtime()

    def languages_combobox2_activated(self, index):
        if index > 0 and self.languages_combobox.currentIndex() > 0:
            self.translate_text_realtime()

    def reset_debounce_timer(self):
        self.translated_text_edit.setPlainText("Translate...")
        self.debounce_timer.stop()
        self.debounce_timer.start()

    def debounce_timeout(self):
        self.translate_text_realtime()

    def translate_text_realtime(self):
        try:
            input_text = self.input_text_edit.toPlainText()
            if not input_text.strip():
                self.translated_text_edit.setPlainText("")
                return

            target_language = self.language_mapping[self.languages_combobox.currentText()]
            if not target_language:
                self.translated_text_edit.setPlainText("")
                return

            if self.languages_combobox2.currentIndex() == 0: 
                target_language_2 = None
            else:
                target_language_2 = self.language_mapping[self.languages_combobox2.currentText()]

            if target_language_2 is None:
                translated_text = self.translator.translate(input_text, dest=target_language)

                language_code_to_name = {language["code"]: language["name"] for language in languages}
                self.label_language_1.setText(language_code_to_name.get(translated_text.src, ""))
                self.label_language_1_text = translated_text.src
                self.label_language_2.setText(language_code_to_name.get(target_language, ""))
                self.label_language_2_text = target_language
            else:
                translated_text = self.translator.translate(input_text, src=target_language_2, dest=target_language)
                language_code_to_name = {language["code"]: language["name"] for language in languages}
                self.label_language_1.setText(language_code_to_name.get(translated_text.src, ""))
                self.label_language_1_text = translated_text.src
                self.label_language_2.setText(language_code_to_name.get(target_language, ""))
                self.label_language_2_text = target_language

            self.translated_text_edit.setPlainText(translated_text.text)
        except:
            print("An exception occurred")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    translator_app = TranslatorApp()
    translator_app.show()
    sys.exit(app.exec_())