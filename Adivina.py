import tkinter as tk
import json
import os

# Función para cargar datos desde un archivo
def cargar_datos(archivo):
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"preguntas": [], "personajes": {}}

# Función para guardar datos en un archivo
def guardar_datos(archivo, datos):
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

# Clase principal del juego
class JuegoF1:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Adivina el Personaje de F1")
        self.ventana.geometry("600x400")
        self.ventana.resizable(False, False)

        self.datos = cargar_datos("f1_lista.json")
        self.pregunta_actual = 0
        self.respuestas = []

        self.crear_interfaz()

    def crear_interfaz(self):
        self.titulo = tk.Label(self.ventana, text="¡Adivina el Piloto o Escudería de F1!",
                               font=("Arial", 16, "bold"))
        self.titulo.pack(pady=10)

        self.contenedor_pregunta = tk.Frame(self.ventana)
        self.contenedor_pregunta.pack(pady=20)

        self.etiqueta_pregunta = tk.Label(self.contenedor_pregunta, text="Presiona 'Empezar' para iniciar el juego.",
                                          font=("Arial", 12), wraplength=500)
        self.etiqueta_pregunta.pack()

        self.boton_empezar = tk.Button(self.ventana, text="Empezar", command=self.iniciar_juego, bg="#4CAF50", fg="white")
        self.boton_empezar.pack(pady=10)

        self.boton_si = tk.Button(self.ventana, text="Sí", command=lambda: self.responder("sí"), state="disabled")
        self.boton_no = tk.Button(self.ventana, text="No", command=lambda: self.responder("no"), state="disabled")
        self.boton_si.pack(side=tk.LEFT, padx=20, pady=10)
        self.boton_no.pack(side=tk.RIGHT, padx=20, pady=10)

        self.etiqueta_resultado = tk.Label(self.ventana, text="", font=("Arial", 12), fg="blue")
        self.etiqueta_resultado.pack(pady=10)

    def iniciar_juego(self):
        if not self.datos["preguntas"]:
            self.etiqueta_resultado.config(text="No hay preguntas registradas.")
            return

        self.pregunta_actual = 0
        self.respuestas = []
        self.etiqueta_resultado.config(text="")
        self.boton_empezar.config(state="disabled")
        self.boton_si.config(state="normal")
        self.boton_no.config(state="normal")
        self.mostrar_pregunta()

    def mostrar_pregunta(self):
        if self.pregunta_actual < len(self.datos["preguntas"]):
            self.etiqueta_pregunta.config(text=self.datos["preguntas"][self.pregunta_actual])
        else:
            self.finalizar_juego()

    def responder(self, respuesta):
        self.respuestas.append(1 if respuesta == "sí" else 0)
        self.pregunta_actual += 1
        self.mostrar_pregunta()

    def finalizar_juego(self):
        coincidencias = [p for p, r in self.datos["personajes"].items() if r == self.respuestas]
        self.boton_si.config(state="disabled")
        self.boton_no.config(state="disabled")

        if coincidencias:
            mensaje = f"¡Tu personaje es: {', '.join(coincidencias)}!"
        else:
            mensaje = "No se encontró coincidencia. Puedes agregar el nuevo personaje."
            self.pedir_nuevo_personaje()
        self.etiqueta_resultado.config(text=mensaje)

    def pedir_nuevo_personaje(self):
        self.etiqueta_pregunta.config(text="¿Cuál era el personaje?")
        self.entrada_personaje = tk.Entry(self.ventana)
        self.entrada_personaje.pack(pady=5)

        self.boton_guardar = tk.Button(self.ventana, text="Guardar", command=self.guardar_personaje, bg="#4CAF50", fg="white")
        self.boton_guardar.pack(pady=5)

    def guardar_personaje(self):
        nuevo_personaje = self.entrada_personaje.get().strip()
        if nuevo_personaje:
            self.datos["personajes"][nuevo_personaje] = self.respuestas
            guardar_datos("datos_f1.json", self.datos)
            self.etiqueta_resultado.config(text=f"Personaje guardado: {nuevo_personaje}")
        self.entrada_personaje.destroy()
        self.boton_guardar.destroy()
        self.boton_empezar.config(state="normal")

# Función principal
def main():
    ventana = tk.Tk()
    app = JuegoF1(ventana)
    ventana.mainloop()

if __name__ == "__main__":
    main()