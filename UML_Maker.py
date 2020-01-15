import os
import tkinter as tk
import tkinter.scrolledtext as tkst
import webbrowser
from tkinter import filedialog


class Program:

    def __init__(self):
        self.root = None
        self.width = 500
        self.height = 600
        self.current_dir = os.getcwd()
        self.running = False
        self.hasFile = False
        self.hasClass = False
        self.cwd = os.getcwd()
        self.lines = []
        self.classes = []
        self.attributes = []
        self.methods = []

    def run(self):
        """
        program loop
        :return: None
        """
        self.initialize()
        self.running = True

        while self.running:
            if self.hasFile:
                pass
            self.root.protocol("WM_DELETE_WINDOW", self.close)
            self.root.mainloop()

    def close(self):
        """
        end the loop and closes the window
        :return: None
        """
        self.running = False
        self.root.destroy()

    def initialize(self):
        """
        Initialize the window
        :return: None
        """
        self.root = tk.Tk()
        self.root.configure(background='#B0E0E6')
        self.root.geometry(str(self.width) + 'x' + str(self.height))
        self.root.title('UML Maker')

        title = tk.Label(self.root,
                         text='UML Maker',
                         font=("", 36, 'bold'),
                         background='#B0E0E6').pack()
        subtitle = tk.Label(self.root,
                            text='Made by Zani Luca',
                            font=("", 14),
                            background='#B0E0E6').pack()

        github_link = tk.Label(self.root,
                               text='https://github.com/ZaniLuca',
                               fg='#0000FF',
                               cursor='hand2',
                               background='#B0E0E6')
        github_link.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/ZaniLuca"))
        github_link.pack()

        description = tk.Message(self.root,
                                 width=self.width - 10,
                                 text='\nThis is a UML table maker, you need to import a .py '
                                      'file in order to extract classes, attributes and methods, '
                                      'click the button below to import a file\n',
                                 relief='sunken',
                                 borderwidth=3).pack()

        browse_button = tk.Button(self.root, text='Open File',
                                  command=lambda: self.browse_file(text_field)).pack()

        text_field = tkst.ScrolledText(self.root,
                                       wrap=tk.WORD,
                                       height=20)


    def browse_file(self, text_field):
        """
        Command activated when button pressed
        :param text_field: ScrolledText Object
        :return: None
        """
        self.root.filename = filedialog.askopenfilename(initialdir=self.cwd,
                                                        title='Pick a python file',
                                                        filetypes=(('Python Files', '*.py'),
                                                                   ("all files", "*.*")))
        if self.root.filename:
            self.read(self.root.filename, text_field)

    def read(self, py_file, text_field):
        """
        Reads the content of the file
        :param py_file: file
        :param text_field: ScrolledText Object
        :return: None
        """
        with open(py_file, 'rt') as f:
            for line in f:
                self.lines.append(line)

        self.update_text_field(text_field)

    def update_text_field(self, text_field):
        """
        Updates the ScrolledText with the file content
        :param text_field: ScrolledText Object
        :return: None
        """
        for line in range(len(self.lines)):
            text_field.insert('insert', self.lines[line])

        text_field.config(state=tk.DISABLED)
        text_field.pack()

        self.hasFile = True


p = Program()
p.run()
