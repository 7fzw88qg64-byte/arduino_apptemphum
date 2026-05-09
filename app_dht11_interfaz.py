import serial
import time
import tkinter as tk

# Cambia COM4 si tu Arduino está en otro puerto
PUERTO = 'COM4'
BAUDIOS = 9600

arduino = None


def conectar_arduino():
    global arduino

    try:
        arduino = serial.Serial(PUERTO, BAUDIOS, timeout=1)
        time.sleep(2)
        estado_label.config(text="Arduino conectado")
    except Exception as e:
        arduino = None
        estado_label.config(text="Arduino no conectado")
        print("Error conectando Arduino:", e)


def leer_datos():
    global arduino

    if arduino is None:
        estado_label.config(text="Arduino no conectado")
        ventana.after(2000, leer_datos)
        return

    try:
        linea = arduino.readline().decode('utf-8', errors='ignore').strip()

        print("Dato recibido:", linea)

        if linea == "":
            estado_label.config(text="Esperando datos...")

        elif linea == "ERROR":
            temperatura_label.config(text="-- °C")
            humedad_label.config(text="-- %")
            estado_label.config(text="Error leyendo el DHT11")

        else:
            datos = linea.split(",")

            if len(datos) == 2:
                temperatura = datos[0].strip()
                humedad = datos[1].strip()

                temperatura_label.config(text=f"{temperatura} °C")
                humedad_label.config(text=f"{humedad} %")
                estado_label.config(text="Lectura correcta")
            else:
                estado_label.config(text="Formato no valido")

    except Exception as e:
        estado_label.config(text="Error leyendo datos")
        print("Error:", e)

    ventana.after(2000, leer_datos)


def cerrar_app():
    global arduino

    if arduino is not None:
        arduino.close()

    ventana.destroy()


# Ventana principal
ventana = tk.Tk()
ventana.title("Monitor DHT11")
ventana.geometry("430x330")
ventana.resizable(False, False)

titulo = tk.Label(
    ventana,
    text="Monitor de Temperatura y Humedad",
    font=("Arial", 16, "bold")
)
titulo.pack(pady=20)

texto_temp = tk.Label(
    ventana,
    text="Temperatura",
    font=("Arial", 13)
)
texto_temp.pack()

temperatura_label = tk.Label(
    ventana,
    text="-- °C",
    font=("Arial", 30, "bold")
)
temperatura_label.pack(pady=5)

texto_hum = tk.Label(
    ventana,
    text="Humedad",
    font=("Arial", 13)
)
texto_hum.pack()

humedad_label = tk.Label(
    ventana,
    text="-- %",
    font=("Arial", 30, "bold")
)
humedad_label.pack(pady=5)

estado_label = tk.Label(
    ventana,
    text="Iniciando...",
    font=("Arial", 10)
)
estado_label.pack(pady=10)

boton_salir = tk.Button(
    ventana,
    text="Salir",
    command=cerrar_app,
    width=12
)
boton_salir.pack(pady=10)

# Primero conecta Arduino, luego empieza a leer
conectar_arduino()
leer_datos()

ventana.protocol("WM_DELETE_WINDOW", cerrar_app)
ventana.mainloop()