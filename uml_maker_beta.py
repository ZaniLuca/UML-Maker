import os
# carichiamo il file all'interno del vettore
lines = []
with open("flappy_bird.py", 'rt') as f:
    for line in f:
        lines.append(line)


# contiamo in questo file quante volte compare la parola class
classes = []

def extract_classes():
    class_lines_index = []
    n_class = 0

    for line in range(len(lines)):
        if "class " in lines[line]:
            if "#" in lines[line]:
                pass
            elif ":" in lines[line]:
                class_lines_index.append(line)
                n_class += 1

    for classe in range(n_class):
        class_line = lines[class_lines_index[classe]]
        class_name = ""
        for char in range(6, len(class_line)):
            if class_line[char] == ":":
                break
            class_name += class_line[char]
        classes.append(class_name)

    return class_lines_index, n_class


class_lines_index, n_class = extract_classes()

# ora che sappiamo quante classi ci sono cerchiamo dove sono i
# constructor __init__ delle classi, che saranno tanti quante le classi
def search_init():
    init_lines_index = []
    init_ends = []
    for line in range(len(lines)):
        if "__init__" in lines[line]:
            init_lines_index.append(line)
            # CERCHIAMO LA FINE DELL'INIT
            for init_lines in range(line + 1, len(lines)):
                if "def " in lines[init_lines]:
                    init_ends.append(init_lines)
                    break

    return init_lines_index, init_ends


init_lines_index, init_ends = search_init()


# ora troviamo i parametri delle classi, e ritorniamo il numero di parametri per classe
def extract_params(i):
    got_comment = False  # bool, se sono presenti commenti
    comment_lines = 0  # numero di linee di commento all'inizio

    # CERCO COMMENTI
    for line in range(init_lines_index[i] + 1,
                      init_ends[i]):  # !!!!!!!!!! devo trovare un valore che vada bene come fine controllo !!!!!!!!!!
        if got_comment and '"""' in lines[line]:
            end_comment = line + 1  # RIGA DOVE FINISCONO
        if not got_comment and '"""' in lines[line]:
            got_comment = True
            start_comment = line  # RIGA DOVE INZIANO I COMMENTI

    # CALCOLO NUMERO DI COMMENTI
    if got_comment:
        comment_lines = end_comment - start_comment
    # print(f'linee di commento classe {classes[i]}: {comment_lines}')

    # UNA VOLTA CHE HO IL NUMERO DI RIGHE DI COMMENTO POSSO
    # INIZIARE A CONTARE QUANTI PARAMETRI CI SONO
    params_start_pos = init_lines_index[i] + 1 + comment_lines

    # CONTIAMO QUANTE LINEE DI PARAMETRI CI SONO (DOPO SELEZIONEREMO I PARAMETRI EFFETTIVI)
    # METTIAMO TUTTE LE LINEE IN UN VETTORE params_lines COSI DA POTERLE POI ESAMINARE
    count_param_lines = 0
    params_lines = []

    for line in range(params_start_pos, len(lines)):
        if "def " in lines[line]:
            break
        count_param_lines += 1
        params_lines.append(lines[line])
    # print(f'numero parametri classe {i}: {count_param_lines}')

    # DALLE LINEE DI PARAMETRI ESTRAIALI QUELLI CONTENENTI self.
    self_param_lines = []

    for line in range(len(params_lines)):
        if "self." and "=" in params_lines[line]:
            if "#" in params_lines[line]:
                pass
            else:
                self_param_lines.append(params_lines[line])

    # DA self_param_lines OVVERO IL VETTORE CONTENENTE LE LINEE DI PARAMETRI
    # CHE CONTENGONO LA PAROLA SELF ESTRAIAMO LA PARTE DOPO IL PUNTO: self.(colore) <--

    for line in range(len(self_param_lines)):
        param = ""
        element = str(self_param_lines[line].split())  # RIGA CHE ESAMINIAMO
        for char in range(7, len(element)):
            if element[char] == " " or element[char] == "." or element[char] == "(" or element[char] == "'":
                break
            param += element[char]
        params.append(param)

    return len(self_param_lines)  # RITORNIAMO len(self_param_lines) CIOE IL NUMERO DI PARAMETRI DELLA CLASSE


# cerchiamo i metodi

def extract_methods(i):
    conta_methods = 0
    # contiamo quanti metodi ci sono in questa classe e i loro indici li mettiamo nella lista

    methods_lines = []

    for line in range(class_lines_index[i] + 1, len(lines)):

        if "class " in lines[line]:
            if ":" in lines[line]:
                break
        # se nella linea c'e scritto class, allora e iniziata una nuova classe
        # e abbiamo finito di contare i metodi di quella precedente

        if "def" in lines[line]:
            if "(self" in lines[line]:
                if "__init__" in lines[line]:
                    pass
                else:
                    methods_lines.append(lines[line])
                    conta_methods += 1

    for element in range(conta_methods):
        method = ""
        new_line = str(methods_lines[element].split())
        for lettere in range(9, len(new_line)):
            if new_line[lettere] == "(" or new_line[lettere] == "'":
                break
            method += new_line[lettere]
        methods.append(method + '()')

    return conta_methods


params = []  # lista con i nomi dei parametri
num_params = []  # numero di parametri che ha ciascuna classe

methods = []  # lista con i nomi dei metodi
num_methods = []  # numero di metodi che ha ciascuna classe

for i in range(n_class):
    num_params.append(extract_params(i))
    num_methods.append(extract_methods(i))


# print(f'Nomi delle classi: {classes}')

# print(f'parametri: {params}')
# print(f'numero parametri per classi: {num_params}')

# print(f'metodi: {methods}')
# print(f'numero metodi per classi: {num_methods}')


# riassumo cio che ho ottenuto finora con una funzione
def recap():
    params_exam = 0  # contatore del numero di parametri esaminati
    methods_exam = 0  # contatore del numero metodi esaminati

    for i in range(n_class):

        # scrivo i parametri di ogni classe
        frase = "classe " + classes[i] + ": \nparams: "
        for param in range(params_exam, params_exam + num_params[i]):
            frase += params[param] + ", "

        # scrivo i metodi di ogni classe
        frase += "\nmethods: "
        for method in range(methods_exam, methods_exam + num_methods[i]):
            frase += methods[method] + ", "

        params_exam += num_params[i]
        methods_exam += num_methods[i]
        # aumentiamo il contatore con il numero dei parametri e metodi esaminati
        # cosicchè l'indice salterà la posizione di tali programmi

        print(frase)


recap()

from PIL import Image, ImageDraw, ImageFont

font = ImageFont.truetype(r'C:/Windows/Fonts/Arial.ttf', 20)

n_params = len(params)
n_methods = len(methods)

width = 300
row = 35
#height = row * (len(params) + len(methods)) + row #1 riga in piu per il nome classe

def draw():
    params_exam = 0  # contatore del numero di parametri esaminati
    methods_exam = 0  # contatore del numero metodi esaminati

    for i in range(n_class):
        height = row * (num_params[i] + num_methods[i]) + row

        img = Image.new("RGB", (width, height)) 
        shape = [(0, 0), (width, row)]

        rect = ImageDraw.Draw(img)
        rect.rectangle(shape, fill ="#8c8c8c")

        text = str(classes[i])
        rect.text((width//2-30, 5), text, font = font, align ="center", fill='black')

        for param in range(params_exam, params_exam + num_params[i]):
            shape = [(0, 35+row*(param-params_exam+1)), (width, 35+(row*(param-params_exam)+1))]
            rect = ImageDraw.Draw(img)

            rect.rectangle(shape, fill ="white")

            text = str(params[param])
            rect.text((5, 40+row*(param-params_exam)), text, font = font, align ="center", fill='black')

        # scrivo i metodi di ogni classe
        for method in range(methods_exam, methods_exam + num_methods[i]):

            shape = [(0, 0+num_params[i]*row+ row*(method-methods_exam+1)), (width, 35+num_params[i]*row+ row*(method-methods_exam+1))]
            rect = ImageDraw.Draw(img)

            rect.rectangle(shape, fill ="#d9d9d9")

            text = str(methods[method])
            rect.text((5, 40+num_params[i]*row+ row*(method-methods_exam)), text, font = font, align ="center", fill='black')

        params_exam += num_params[i]
        methods_exam += num_methods[i]
        # aumentiamo il contatore con il numero dei parametri e metodi esaminati
        # cosicchè l'indice salterà la posizione di tali programmi
        img.show()

draw()