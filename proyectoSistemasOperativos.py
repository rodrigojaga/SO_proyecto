import threading
import time
import random
import tkinter as tk
from tkinter import messagebox

"""
VARIABLES ALGORTIMO DE DEKKER
"""
# Variables compartidas para el Algoritmo de Dekker
turn = 0
flag = [False, False]  # flag[0] para el proceso 1, flag[1] para el proceso 2
N_ITERATIONS = 5  # Iteraciones que hace cada proceso

"""
VARIABLES COMENSALES FILOSOFOS
"""
# filosofos y comidas por filosofo
filosofosCant = 5
comidasFilosofo = 5
# tenedores (semaforos)
tenedores = [threading.Semaphore(1) for _ in range(filosofosCant)]
# veces que los filosofos comieron
comidasRealizadas = [0] * filosofosCant
# controla el acceso a comidasRealizadas (variable compartida)
comidasLock = threading.Lock()

"""
INICIO COMENSALES FILOSOFOS
"""
# filosofos comensales
def mesaFilosofos(noFilosofo, textBoxes):
    global comidasRealizadas
    while True:
        with comidasLock:
            if comidasRealizadas[noFilosofo] >= comidasFilosofo:
                textBoxes[noFilosofo].insert(tk.END, f"Filosofo {noFilosofo} comió 5 veces y se va de la mesa.\n")
                return

        textBoxes[noFilosofo].insert(tk.END, f"Filosofo {noFilosofo} esta pensando.\n")
        time.sleep(random.uniform(1, 3))

        textBoxes[noFilosofo].insert(tk.END, f"Filosofo {noFilosofo} quiere comer.\n")

        # intenta tomar tenedores
        tenedores[noFilosofo].acquire()
        textBoxes[noFilosofo].insert(tk.END, f"Filosofo {noFilosofo} toma el tenedor izquierdo ({noFilosofo}).\n")

        if filosofosCant - 1 == noFilosofo:
            tenedores[0].acquire()
            tmp = 0
        else:
            tenedores[noFilosofo + 1].acquire()
            tmp = noFilosofo + 1

        textBoxes[noFilosofo].insert(tk.END, f"Filosofo {noFilosofo} toma el tenedor derecho ({tmp}).\n")

        #comer
        textBoxes[noFilosofo].insert(tk.END, f"Filosofo {noFilosofo} esta comiendo.\n")
        time.sleep(random.uniform(1, 2))

        with comidasLock:
            comidasRealizadas[noFilosofo] += 1
            textBoxes[noFilosofo].insert(tk.END,
                                          f"Filosofo {noFilosofo} ya comio {comidasRealizadas[noFilosofo]} veces.\n")

        #dejar los tenedores
        tenedores[noFilosofo].release()
        textBoxes[noFilosofo].insert(tk.END, f"Filosofo {noFilosofo} dejo el tenedor izquierdo ({noFilosofo}).\n")

        if filosofosCant - 1 == noFilosofo:
            tenedores[0].release()
            tmp = 0
        else:
            tenedores[noFilosofo + 1].release()
            tmp = noFilosofo + 1

        textBoxes[noFilosofo].insert(tk.END, f"Filosofo {noFilosofo} dejó el tenedor derecho ({tmp}).\n")
        textBoxes[noFilosofo].insert(tk.END, f"Filosofo {noFilosofo} termino de comer y esta pensando.\n\n")


#nueva ventana para filosofos comenzales
def iniciarComensales():
    global comidasRealizadas
    comidasRealizadas = [0] * filosofosCant
    ventanaFilosofos = tk.Toplevel()
    ventanaFilosofos.title("Problema de los Comensales Filosofos")

    textBoxes = []
    for i in range(filosofosCant):
        textBox = tk.Text(ventanaFilosofos, height=10, width=50)
        textBox.grid(row=i, column=0, padx=10, pady=5)
        textBoxes.append(textBox)

    def ejecutarFilosofos():
        filosofos = []
        for i in range(filosofosCant):
            t = threading.Thread(target=mesaFilosofos, args=(i, textBoxes,))
            filosofos.append(t)
            t.start()

        for t in filosofos:
            t.join()

        messagebox.showinfo("Completado", "Los Filsofos han terminado de comer.")
        ventanaFilosofos.destroy()
        root.deiconify()

    threading.Thread(target=ejecutarFilosofos).start()
"""
FIN COMENSALES FILOSOFOS
"""
"""
INICIO ALGORITMO DE DEKKER
"""
# Funciones para el Algoritmo de Dekker
def process_1(text_box):
    global turn, flag
    for i in range(N_ITERATIONS):
        text_box.insert(tk.END, f"Proceso 1 intentando entrar en la seccion crítica, iteración {i + 1}\n")
        flag[0] = True
        while flag[1]:
            if turn == 1:
                flag[0] = False
                while turn == 1:
                    pass
                flag[0] = True

        text_box.insert(tk.END, "Proceso 1 esta en la sección crítica\n")
        time.sleep(1)
        text_box.insert(tk.END, "Proceso 1 sale de la sección crítica\n")
        turn = 1
        flag[0] = False
        time.sleep(1)


def process_2(text_box):
    global turn, flag
    for i in range(N_ITERATIONS):
        text_box.insert(tk.END, f"Proceso 2 intentando entrar en la sección crítica, iteración {i + 1}\n")
        flag[1] = True
        while flag[0]:
            if turn == 0:
                flag[1] = False
                while turn == 0:
                    pass
                flag[1] = True

        text_box.insert(tk.END, "Proceso 2 está en la sección crítica\n")
        time.sleep(1)
        text_box.insert(tk.END, "Proceso 2 sale de la sección crítica\n")
        turn = 0
        flag[1] = False
        time.sleep(1)


def iniciarDekker():
    dekker_window = tk.Toplevel()
    dekker_window.title("Algoritmo de Dekker")

    process1_text = tk.Text(dekker_window, width=50, height=10)
    process1_text.grid(row=0, column=0, padx=10, pady=5)
    process1_text.insert(tk.END, "Proceso 1 listo\n")

    process2_text = tk.Text(dekker_window, width=50, height=10)
    process2_text.grid(row=1, column=0, padx=10, pady=5)
    process2_text.insert(tk.END, "Proceso 2 listo\n")

    def ejecutarDekker():
        t1 = threading.Thread(target=process_1, args=(process1_text,))
        t2 = threading.Thread(target=process_2, args=(process2_text,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        messagebox.showinfo("Completado", "Simulación del Algoritmo de Dekker completada.")
        dekker_window.destroy()
        root.deiconify()

    threading.Thread(target=ejecutarDekker).start()
"""
FIN ALGORITMO DE DEKKER
"""


# Crear la ventana principal
root = tk.Tk()
root.title("PROYECTO SISTEMAS OPERATIVOS")


def ocultarPrincipal():
    root.withdraw()


# Botones para seleccionar entre el algoritmo de Dekker y el problema de los comensales filósofos
btn_filosofos = tk.Button(root, text="Problema de Comensales Filósofos",
                          command=lambda: [ocultarPrincipal(), iniciarComensales()])
btn_filosofos.pack(pady=20)

btn_dekker = tk.Button(root, text="Algoritmo de Dekker",
                       command=lambda: [ocultarPrincipal(), iniciarDekker()])
btn_dekker.pack(pady=20)

root.mainloop()
