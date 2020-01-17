import os
import tkinter as tk
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
        self.cwd = os.getcwd()
        self.lines = []
        self.classes = []
        self.attributes = []
        self.methods = []
        # TODO better imports
        self.font = ImageFont.truetype(r'C:/Windows/Fonts/Arial.ttf', 20)
        self.bg = tk.PhotoImage(file='GUI.png')
        self.play_img = tk.PhotoImage(file='play_btn.png')

    def run(self):
        """
        creates the classes tables
        :return: None
        """
        if self.hasFile:
            num_params = []
            num_methods = []

            class_lines_index, n_class = self.extract_classes()
            # TODO add error message when a class isn't found
            init_lines_index, init_ends = self.search_init()

            for i in range(n_class):
                num_params.append(self.extract_attributes(i, init_lines_index, init_ends))
                num_methods.append(self.extract_methods(i, class_lines_index))
            self.recap(n_class, num_params, num_methods)
            self.draw(n_class, num_params, num_methods)
        else:
            # TODO add error msg when there isn't a file
            print('--No FILE detected--')

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
        self.root.geometry(str(self.width) + 'x' + str(self.height))
        self.root.title('UML Maker')
        self.root.resizable(False, False)

        panel = tk.Label(self.root, image=self.bg)
        panel.pack(side="bottom", fill="both", expand="yes")

        text_field = tkst.ScrolledText(self.root, wrap=tk.WORD, width=48, height=16).place(x=46, y=210)

        browse_btn = tk.Button(self.root, text='Open file', command=lambda: self.browse_file()).place(x=160, y=175)
        make_btn = tk.Button(self.root, image=self.play_img, command=lambda: self.run()).place(x=400, y=170)

        self.root.mainloop()

    def browse_file(self):
        """
        Command activated when button pressed
        :return: None
        """
        self.root.filename = filedialog.askopenfilename(initialdir=self.cwd, title='Pick a python file',
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
        text_field = tkst.ScrolledText(self.root, wrap=tk.WORD, width=48, height=16)

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
        self.update_text_field()

    def extract_classes(self):
        """
        extract the classes from the file
        :returns: int
        """
        class_lines_index = []
        n_class = 0

        for line in range(len(self.lines)):
            if "class " in self.lines[line]:
                if "#" in self.lines[line]:
                    pass
                elif ":" in self.lines[line]:
                    class_lines_index.append(line)
                    n_class += 1

        for classe in range(n_class):
            class_line = self.lines[class_lines_index[classe]]
            class_name = ""
            for char in range(6, len(class_line)):
                if class_line[char] == ":":
                    break
                class_name += class_line[char]
            self.classes.append(class_name)

        return class_lines_index, n_class

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
                # CERCHIAMO LA FINE DELL'INIT
                for init_lines in range(line + 1, len(self.lines)):
                    if "def " in self.lines[init_lines]:
                        init_ends.append(init_lines)
                        break

        return init_lines_index, init_ends

    def extract_attributes(self, i, init_lines_index, init_ends):
        """
        extract attributes from the file
        :param i: int
        :param init_lines_index: int
        :param init_ends: int
        :return: int
        """
        got_comment = False
        comment_lines = 0

        # CERCO COMMENTI
        for line in range(init_lines_index[i] + 1, init_ends[i]):
            if got_comment and '"""' in self.lines[line]:
                end_comment = line + 1  # RIGA DOVE FINISCONO
            if not got_comment and '"""' in self.lines[line]:
                got_comment = True
                start_comment = line  # RIGA DOVE INZIANO I COMMENTI

        # CALCOLO NUMERO DI COMMENTI
        if got_comment:
            comment_lines = end_comment - start_comment

        params_start_pos = init_lines_index[i] + 1 + comment_lines
        count_param_lines = 0
        params_lines = []

        for line in range(params_start_pos, len(self.lines)):
            if "def " in self.lines[line]:
                break
            count_param_lines += 1
            params_lines.append(self.lines[line])

        self_param_lines = []

        for line in range(len(params_lines)):
            if "self." and "=" in params_lines[line]:
                if "#" in params_lines[line]:
                    pass
                else:
                    self_param_lines.append(params_lines[line])

        for line in range(len(self_param_lines)):
            param = ""
            element = str(self_param_lines[line].split())
            for char in range(7, len(element)):
                if element[char] == " " or element[char] == "." or element[char] == "(" or element[char] == "'":
                    break
                param += element[char]
            self.attributes.append(param)

        return len(self_param_lines)

    def extract_methods(self, i, class_lines_index):
        """
        extract methods from the file
        :param i: int
        :param class_lines_index: int
        :return: int
        """
        # TODO better names
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
            for lettere in range(9, len(new_line)):
                if new_line[lettere] == "(" or new_line[lettere] == "'":
                    break
                method += new_line[lettere]
            self.methods.append(method + '()')

        return conta_methods

    def draw(self, n_class, num_params, num_methods):
        """
        Draw and open the tables
        :param n_class: int
        :param num_params: int
        :param num_methods: int
        :return: None
        """
        width = 300
        row = 35
        # TODO add color variables
        params_exam = 0
        methods_exam = 0

        for i in range(n_class):
            height = row * (num_params[i] + num_methods[i]) + row

            img = Image.new("RGB", (width, height))
            shape = [(0, 0), (width, row)]

            rect = ImageDraw.Draw(img)
            rect.rectangle(shape, fill="#8c8c8c")

            text = str(self.classes[i])
            rect.text((width // 2 - 30, 5), text, font=self.font, align="center", fill='black')

            for param in range(params_exam, params_exam + num_params[i]):
                shape = [(0, 35 + row * (param - params_exam + 1)), (width, 35 + (row * (param - params_exam) + 1))]
                rect = ImageDraw.Draw(img)

                rect.rectangle(shape, fill="white")

                text = str(self.attributes[param])
                rect.text((5, 40 + row * (param - params_exam)), text, font=self.font, align="center", fill='black')

            for method in range(methods_exam, methods_exam + num_methods[i]):
                shape = [(0, 0 + num_params[i] * row + row * (method - methods_exam + 1)),
                         (width, 35 + num_params[i] * row + row * (method - methods_exam + 1))]
                rect = ImageDraw.Draw(img)

                rect.rectangle(shape, fill="#d9d9d9")

                text = str(self.methods[method])
                rect.text((5, 40 + num_params[i] * row + row * (method - methods_exam)), text, font=self.font,
                          align="center", fill='black')

            params_exam += num_params[i]
            methods_exam += num_methods[i]

            img.show()
            img.save('C:/Users/Public/Documents/UML/output/'+ self.classes[i]+'.png', format='png')

    def recap(self, n_class, num_params, num_methods):

        params_exam = 0
        methods_exam = 0

        for i in range(n_class):

            frase = "class " + self.classes[i] + ": \nattributes: "
            for param in range(params_exam, params_exam + num_params[i]):
                frase += self.attributes[param] + ", "

            frase += "\nmethods: "
            for method in range(methods_exam, methods_exam + num_methods[i]):
                frase += self.methods[method] + ", "

            params_exam += num_params[i]
            methods_exam += num_methods[i]
            print(frase)


p = Program()
p.initialize()
