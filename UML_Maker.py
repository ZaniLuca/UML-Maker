import os
import platform
import tkinter as tk
import tkinter.messagebox
import tkinter.scrolledtext as tkst
from tkinter import filedialog

from PIL import Image, ImageDraw, ImageFont


class Program:

    def __init__(self):
        self.root = tk.Tk()
        self.width = 500
        self.height = 600
        self.running = False
        self.hasFile = False
        self.hasClass = False
        self.system = platform.system()
        self.stw = 55 if self.system == 'Darwin' else 48
        self.sth = 20 if self.system == 'Darwin' else 16
        self.lines = []
        self.classes = []
        self.attributes = []
        self.methods = []

        self.assets_folder = os.path.join(os.path.dirname(__file__), 'assets')
        self.font = ImageFont.truetype(os.path.join(self.assets_folder, 'Arial.ttf'), 20)
        self.bg = tk.PhotoImage(file=os.path.join(self.assets_folder, 'GUI.png'))
        self.play_img = tk.PhotoImage(file=os.path.join(self.assets_folder, 'play_btn.png'))
        self.logo = os.path.join(self.assets_folder, 'logo.ico')

    def run(self):
        """
        creates the classes tables
        :return: None
        """
        if self.hasFile:
            num_attributes = []
            num_methods = []

            class_lines_index, num_class = self.extract_classes()
            if self.hasClass:
                init_lines_index, init_ends = self.search_init()

                for i in range(num_class):
                    num_attributes.append(self.extract_attributes(i, init_lines_index, init_ends))
                    num_methods.append(self.extract_methods(i, class_lines_index))
                self.recap(num_class, num_attributes, num_methods)
                self.draw(num_class, num_attributes, num_methods)
            else:
                alert = tkinter.messagebox.showwarning('Error!', 'No class has been found')
        else:
            alert = tkinter.messagebox.showwarning('Error!', 'File not detected')

    def initialize(self):
        """
        Initialize the window
        :return: None
        """
        self.root.geometry(str(self.width) + 'x' + str(self.height))
        self.root.title('UML Maker')
        self.root.wm_iconbitmap(self.logo)
        self.root.resizable(False, False)

        panel = tk.Label(self.root, image=self.bg)
        panel.pack(side="bottom", fill="both", expand="yes")

        text_field = tkst.ScrolledText(self.root, wrap=tk.WORD, width=self.stw, height=self.sth)
        text_field.place(x=46, y=210)

        browse_btn = tk.Button(self.root, text='Open file', command=lambda: self.browse_file())
        browse_btn.place(x=160, y=175)
        make_btn = tk.Button(self.root, image=self.play_img, command=lambda: self.run())
        make_btn.place(x=400, y=170)

        self.root.mainloop()

    def browse_file(self):
        """
        Command activated when button pressed
        :return: None
        """
        self.root.filename = filedialog.askopenfilename(initialdir=os.getcwd(), title='Pick a python file',
                                                        filetypes=(('Python Files', '*.py'), ("all files", "*.*")))

        if self.root.filename:
            if self.hasFile:
                self.clear()
            self.read(self.root.filename)

    def read(self, py_file):
        """
        Reads the content of the file
        :param py_file: file
        :return: None
        """
        with open(py_file, 'rt') as f:
            for line in f:
                self.lines.append(line)

        self.update_text_field()

    def update_text_field(self):
        """
        Updates the ScrolledText with the file content
        :return: None
        """
        text_field = tkst.ScrolledText(self.root, wrap=tk.WORD, width=self.stw, height=self.sth)

        for line in range(len(self.lines)):
            text_field.insert('insert', self.lines[line])

        text_field.config(state=tk.DISABLED)
        text_field.place(x=46, y=210)

        self.hasFile = True

    def clear(self):
        """
        clears the text
        :return: None
        """
        self.lines = []
        self.classes = []
        self.attributes = []
        self.methods = []
        self.hasFile = False
        self.hasClass = False
        self.update_text_field()

    def extract_classes(self):
        """
        extract the classes from the file
        :returns: int
        """
        class_lines_index = []
        num_class = 0

        for line in range(len(self.lines)):
            if "class " in self.lines[line]:
                if "#" in self.lines[line]:
                    pass
                elif ":" in self.lines[line]:
                    self.hasClass = True
                    class_lines_index.append(line)
                    num_class += 1

        for classe in range(num_class):
            class_line = self.lines[class_lines_index[classe]]
            class_name = ""
            for char in range(6, len(class_line)):
                if class_line[char] == ":":
                    break
                class_name += class_line[char]
            self.classes.append(class_name)

        return class_lines_index, num_class

    def search_init(self):
        """
        search for every constructor function
        :returns: int
        """
        init_lines_index = []
        init_ends = []
        for line in range(len(self.lines)):
            if "__init__" in self.lines[line]:
                init_lines_index.append(line)
                for init_lines in range(line + 1, len(self.lines)):
                    if "def " in self.lines[init_lines]:
                        init_ends.append(init_lines)
                        break

        return init_lines_index, init_ends

    def extract_attributes(self, i, init_lines_index, init_ends):
        """
        extract attributes from the file
        :attribute i: int
        :attribute init_lines_index: int
        :attribute init_ends: int
        :return: int
        """
        got_comment = False
        comment_lines = 0

        for line in range(init_lines_index[i] + 1, init_ends[i]):
            if got_comment and '"""' in self.lines[line]:
                end_comment = line + 1
            if not got_comment and '"""' in self.lines[line]:
                got_comment = True
                start_comment = line

        if got_comment:
            comment_lines = end_comment - start_comment

        attributes_start_pos = init_lines_index[i] + 1 + comment_lines
        count_attributes_lines = 0
        attributes_lines = []

        for line in range(attributes_start_pos, len(self.lines)):
            if "def " in self.lines[line]:
                break
            count_attributes_lines += 1
            attributes_lines.append(self.lines[line])

        self_attributes_lines = []

        for line in range(len(attributes_lines)):
            if "self." and "=" in attributes_lines[line]:
                if "#" in attributes_lines[line]:
                    pass
                else:
                    self_attributes_lines.append(attributes_lines[line])

        for line in range(len(self_attributes_lines)):
            attribute = ""
            element = str(self_attributes_lines[line].split())
            for char in range(7, len(element)):
                if element[char] == " " or element[char] == "." or element[char] == "(" or element[char] == "'":
                    break
                attribute += element[char]
            self.attributes.append(attribute)

        return len(self_attributes_lines)

    def extract_methods(self, i, class_lines_index):
        """
        extract methods from the file
        :param i: int
        :param class_lines_index: int
        :return: int
        """
        conta_methods = 0

        methods_lines = []

        for line in range(class_lines_index[i] + 1, len(self.lines)):

            if "class " in self.lines[line]:
                if ":" in self.lines[line]:
                    break

            if "def" in self.lines[line]:
                if "(self" in self.lines[line]:
                    if "__init__" in self.lines[line]:
                        pass
                    else:
                        methods_lines.append(self.lines[line])
                        conta_methods += 1

        for element in range(conta_methods):
            method = ""
            new_line = str(methods_lines[element].split())
            for char in range(9, len(new_line)):
                if new_line[char] == "(" or new_line[char] == "'":
                    break
                method += new_line[char]
            self.methods.append(method + '()')

        return conta_methods

    def draw(self, num_class, num_attributes, num_methods):
        """
        Draw and open the tables
        :param num_class: int
        :param num_attributes: int
        :param num_methods: int
        :return: None
        """
        width = 300
        row = 35
        attributes_exam = 0
        methods_exam = 0

        for i in range(num_class):
            # Colors
            class_color = "#8c8c8c"
            attributes_color = "#FFFFFF"
            methods_color = "#d9d9d9"

            height = row * (num_attributes[i] + num_methods[i]) + row
            img = Image.new("RGB", (width, height))

            shape = [(0, 0), (width, row)]
            rect = ImageDraw.Draw(img)
            rect.rectangle(shape, fill=class_color)

            text = str(self.classes[i])
            rect.text((width // 2 - 30, 5), text, font=self.font, align="center", fill='black')

            for attribute in range(attributes_exam, attributes_exam + num_attributes[i]):
                shape = [(0, 35 + row * (attribute - attributes_exam + 1)),
                         (width, 35 + (row * (attribute - attributes_exam) + 1))]
                rect = ImageDraw.Draw(img)

                rect.rectangle(shape, fill=attributes_color)

                text = str(self.attributes[attribute])
                rect.text((5, 40 + row * (attribute - attributes_exam)), text, font=self.font, align="center",
                          fill='black')

            for method in range(methods_exam, methods_exam + num_methods[i]):
                shape = [(0, 0 + num_attributes[i] * row + row * (method - methods_exam + 1)),
                         (width, 35 + num_attributes[i] * row + row * (method - methods_exam + 1))]
                rect = ImageDraw.Draw(img)

                rect.rectangle(shape, fill=methods_color)

                text = str(self.methods[method])
                rect.text((5, 40 + num_attributes[i] * row + row * (method - methods_exam)), text, font=self.font,
                          align="center", fill='black')

            attributes_exam += num_attributes[i]
            methods_exam += num_methods[i]

            img.show()
            img.save(os.path.join(os.getcwd(), 'output') + '/' + self.classes[i] + '.png', format='png')

    def recap(self, num_class, num_attributes, num_methods):

        attributes_exam = 0
        methods_exam = 0

        for i in range(num_class):

            frase = "class " + self.classes[i] + ": \nattributes: "
            for attribute in range(attributes_exam, attributes_exam + num_attributes[i]):
                frase += self.attributes[attribute] + ", "

            frase += "\nmethods: "
            for method in range(methods_exam, methods_exam + num_methods[i]):
                frase += self.methods[method] + ", "

            attributes_exam += num_attributes[i]
            methods_exam += num_methods[i]
            print(frase)


p = Program()
p.initialize()
