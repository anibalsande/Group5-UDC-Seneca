"""After researching we found that Tkinter, PyQt6 and Kivy were not only
the most popular libraries but also the most documented ones. As a result, we
focused on those three and researched about which was the most suitable.
We found out that Tkinder was the most limited both on GUI and efficiency.
While PyQt6 and Kivy were similar in efficiency and language, PyQt6 is the
best one for computers and laptops, while Kivy offers a great functionality
in touch screens and other type of devices. Finally, we decided to choose
PyQt because it offers the most wide range of options and it's a strong
library"""

import tkinter as tk
from tkinter import messagebox

# Crear la ventana principal
mainwindow = tk.Tk()
mainwindow.title("Test with Tkinter")
mainwindow.geometry("400x200")
mainwindow.configure(bg='WHITE')  # Color de fondo oscuro

# Función para mostrar un mensaje al hacer clic en el botón
def mostrar_mensaje():
    texto = entrada.get()  # Obtener el texto ingresado
    if texto:
        messagebox.showinfo("Mensaje", f"Has ingresado: {texto}")
    else:
        messagebox.showwarning("Advertencia", "El cuadro de texto está vacío.")

# Estilo de la fuente
fuente_label = ("Bahnschrift", 16, "bold")
fuente_boton = ("Bahnschrift", 10, "bold")

# Crear un label (etiqueta) con estilo personalizado
label = tk.Label(mainwindow, text="INTRODUZCA SU INFORMACIÓN", 
                 fg="#0B1E3E",  # Color del texto
                 bg='WHITE',  # Fondo igual al de la ventana
                 font=fuente_label)
label.pack(pady=10)

# Crear un Frame para contener el cuadro de texto y el botón
frame = tk.Frame(mainwindow, bg='WHITE')  # Color de fondo igual al de la ventana
frame.pack(pady=10)

# Crear un cuadro de texto personalizado
entrada = tk.Entry(frame, width=25, 
                   font=("Bahnschrift", 12), 
                   bg="#ffffff",  # Fondo blanco
                   fg="#0B1E3E",  # Texto azul
                   bd=2, relief="solid")  # Borde sólido
entrada.pack(side=tk.LEFT, padx=5)  # Colocar el cuadro de texto a la izquierda

# Crear un botón con estilo, colocado justo a la derecha del cuadro de texto
boton = tk.Button(frame, text=" ACEPTAR ", 
                  command=mostrar_mensaje,
                  font=fuente_boton,  # Fuente cursiva
                  fg="#0B1E3E",  # Texto blanco
                  bg="#f6be00",  # Fondo verde
                  activebackground="#0B1E3E",  # Fondo cuando está activo
                  activeforeground="WHITE",  # Texto cuando está activo
                  relief="solid",  # Relieve del botón
                  bd=0)  # Borde más grueso
boton.pack(side=tk.LEFT, padx=5)  # Colocar el botón a la derecha del cuadro de texto

# Iniciar el bucle de la interfaz gráfica
mainwindow.mainloop()