import os
from tkinter import *
import math

class Main(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()
        self.root = master
        self.base_path = os.path.dirname(os.path.abspath(__file__))

        self.canvas = Canvas(self.root, width=800, height=400)
        self.canvas.config(width=1920, height=678)
        self.canvas.pack()

        self.pelotilla = None
        self.teclas_presionadas = {}  # Diccionario para rastrear teclas presionadas
        self.inicio()

        # Inicia el bucle de movimiento
        self.actualizar_movimiento()

    def inicio(self):
        oreja1 = self.canvas.create_polygon(200, 120, 210, 70, 220, 120, fill='orange')
        oreja2 = self.canvas.create_polygon(250, 120, 240, 70, 230, 120, fill='orange')
        cabeza = self.canvas.create_oval(200, 100, 250, 150, fill='orange')
        ojo1 = self.canvas.create_oval(210, 120, 220, 130, fill='black')
        ojo2 = self.canvas.create_oval(230, 120, 240, 130, fill='black')
        pata1 = self.canvas.create_oval(210, 180, 220, 220, fill='orange')
        pata2 = self.canvas.create_oval(290, 180, 300, 220, fill='orange')
        cuerpo = self.canvas.create_oval(210, 140, 310, 200, fill='orange')
        pata3 = self.canvas.create_oval(220, 180, 230, 220, fill='orange')
        pata4 = self.canvas.create_oval(300, 180, 310, 220, fill='orange')
        self.gato = [cabeza, ojo1, ojo2, cuerpo, oreja1, oreja2, pata1, pata2, pata3, pata4]

        # Vincula eventos de teclado
        self.root.bind('<KeyPress>', self.tecla_presionada)
        self.root.bind('<KeyRelease>', self.tecla_liberada)
        self.root.bind('<Button-1>', lambda event: self.buscar_pelota(event))

    def tecla_presionada(self, event):
        self.teclas_presionadas[event.keysym] = True

    def tecla_liberada(self, event):
        if event.keysym in self.teclas_presionadas:
            del self.teclas_presionadas[event.keysym]

    def actualizar_movimiento(self):
        dx, dy = 0, 0
        if 'Up' in self.teclas_presionadas:
            dy -= 5
        if 'Down' in self.teclas_presionadas:
            dy += 5
        if 'Left' in self.teclas_presionadas:
            dx -= 5
        if 'Right' in self.teclas_presionadas:
            dx += 5

        if dx != 0 or dy != 0:
            for i in self.gato:
                self.canvas.move(i, dx, dy)

        # Llama a este método nuevamente después de 20 ms
        self.root.after(20, self.actualizar_movimiento)

    def buscar_pelota(self, event):
        if self.pelotilla is not None:
            self.canvas.delete(self.pelotilla)

        self.pelotilla = self.canvas.create_oval(event.x-5, event.y-5, event.x+5, event.y+5, fill='skyblue')
        self.mover_gato(event.x, event.y)

    def mover_gato(self, x_destino, y_destino):
        x1, y1, x2, y2 = self.canvas.coords(self.gato[2])
        x_actual = (x1 + x2) / 2
        y_actual = (y1 + y2) / 2

        dx = x_destino - x_actual
        dy = y_destino - y_actual
        distancia = math.sqrt(dx**2 + dy**2)

        pasos = int(distancia / 2)
        for _ in range(pasos):
            if distancia < 2:
                break
            paso_x = dx / pasos
            paso_y = dy / pasos
            for i in self.gato:
                self.canvas.move(i, paso_x, paso_y)
            self.root.update()
            x1, y1, x2, y2 = self.canvas.coords(self.gato[0])
            x_actual = (x1 + x2) / 2
            y_actual = (y1 + y2) / 2
            dx = x_destino - x_actual
            dy = y_destino - y_actual
            distancia = math.sqrt(dx**2 + dy**2)


if __name__ == '__main__':
    root = Tk()
    root.title('Gatito')
    root.geometry('800x400')
    app = Main(root)
    app.mainloop()