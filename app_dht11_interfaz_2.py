import serial
import time
import tkinter as tk

# Cambia COM4 si tu Arduino está en otro puerto
PUERTO = 'COM4'
BAUDIOS = 9600

arduino = None
leyendo = False


def conectar_arduino():
    global arduino

    try:
        arduino = serial.Serial(PUERTO, BAUDIOS, timeout=1)
        time.sleep(2)
        estado_conexion.config(text="Arduino conectado", fg="#1f8f4d")
        return True

    except Exception as e:
        arduino = None
        estado_conexion.config(text="Arduino no conectado", fg="#b00020")
        estado_lectura.config(text="Revisa el puerto o la conexión USB")
        print("Error conectando Arduino:", e)
        return False


def evaluar_temperatura(temp):
    if temp < 30:
        return (
            "Clima agradable. Puedes salir con normalidad, solo recuerda mantenerte hidratado.",
            "#2e7d32"
        )
    elif temp >= 30 and temp <= 35:
        return (
            "Hace calor. Si vas a salir, lleva agua, usa ropa ligera y evita exponerte mucho tiempo al sol. Usa protector solar.",
            "#f9fd1d"
        )

    elif temp > 35 and temp < 40:
        return (
            "Calor intenso. Procura salir solo si es necesario, busca sombra y evita actividad física de alta intensidad.",
            "#ef7f00"
        )

    else:
        return (
            "Riesgo por calor extremo. Evita exponerte si no es necesario, mantente en un lugar fresco y toma agua constantemente para mantener la hidratación.",
            "#c62828"
        )


def evaluar_humedad(hum):
    if hum < 30:
        return (
            "Ambiente seco. Puede causar resequedad; toma agua y considera ventilar adecuadamente.",
            "#f9a825"
        )

    elif hum >= 30 and hum <= 60:
        return (
            "Humedad adecuada. El ambiente se encuentra en un rango idóneo.",
            "#2e7d32"
        )

    else:
        return (
            "Humedad alta. Si vas a salir, considera ropa ligera y revisa ventilación en espacios cerrados.",
            "#1565c0"
        )


def comenzar_programa():
    global leyendo

    if arduino is None:
        conexion_exitosa = conectar_arduino()

        if not conexion_exitosa:
            return

    leyendo = True

    boton_comenzar.config(state="disabled")
    estado_lectura.config(text="Lectura iniciada...")

    leer_datos()


def leer_datos():
    global arduino, leyendo

    if not leyendo:
        return

    if arduino is None:
        estado_conexion.config(text="Arduino no conectado", fg="#b00020")
        estado_lectura.config(text="No se puede leer sin conexión")
        return

    try:
        linea = arduino.readline().decode('utf-8', errors='ignore').strip()

        print("Dato recibido:", linea)

        if linea == "":
            estado_lectura.config(text="Esperando datos...")

        elif linea == "ERROR":
            temperatura_label.config(text="-- °C")
            humedad_label.config(text="-- %")
            mensaje_temp.config(text="Error leyendo temperatura", fg="#b00020")
            mensaje_hum.config(text="Error leyendo humedad", fg="#b00020")
            estado_lectura.config(text="Error leyendo el sensor DHT11")

        else:
            datos = linea.split(",")

            if len(datos) == 2:
                temperatura = float(datos[0].strip())
                humedad = float(datos[1].strip())

                texto_temp, color_temp = evaluar_temperatura(temperatura)
                texto_hum, color_hum = evaluar_humedad(humedad)

                temperatura_label.config(
                    text=f"{temperatura:.1f} °C",
                    fg=color_temp
                )

                humedad_label.config(
                    text=f"{humedad:.1f} %",
                    fg=color_hum
                )

                mensaje_temp.config(
                    text=texto_temp,
                    fg=color_temp
                )

                mensaje_hum.config(
                    text=texto_hum,
                    fg=color_hum
                )

                estado_lectura.config(text="Lectura actualizada correctamente")

            else:
                estado_lectura.config(text="Formato no válido")

    except Exception as e:
        estado_lectura.config(text="Error leyendo datos")
        print("Error:", e)

    ventana.after(2000, leer_datos)


def finalizar_programa():
    global arduino, leyendo

    leyendo = False

    if arduino is not None:
        arduino.close()
        arduino = None

    estado_conexion.config(text="Arduino desconectado", fg="#6b7280")
    estado_lectura.config(text="Programa finalizado")

    ventana.destroy()


# Ventana principal
ventana = tk.Tk()
ventana.title("Monitor Ambiental DHT11")
ventana.geometry("560x570")
ventana.resizable(False, False)
ventana.configure(bg="#f4f6f8")

# Título
titulo = tk.Label(
    ventana,
    text="Monitor Ambiental",
    font=("Arial", 22, "bold"),
    bg="#f4f6f8",
    fg="#1f2937"
)
titulo.pack(pady=(25, 5))

subtitulo = tk.Label(
    ventana,
    text="Temperatura y humedad en tiempo real",
    font=("Arial", 11),
    bg="#f4f6f8",
    fg="#6b7280"
)
subtitulo.pack(pady=(0, 15))

# Tarjeta principal
tarjeta = tk.Frame(
    ventana,
    bg="white",
    padx=25,
    pady=20
)
tarjeta.pack(padx=25, pady=10, fill="both")

# Temperatura
texto_temp = tk.Label(
    tarjeta,
    text="Temperatura",
    font=("Arial", 13, "bold"),
    bg="white",
    fg="#374151"
)
texto_temp.pack()

temperatura_label = tk.Label(
    tarjeta,
    text="-- °C",
    font=("Arial", 38, "bold"),
    bg="white",
    fg="#111827"
)
temperatura_label.pack(pady=(5, 0))

mensaje_temp = tk.Label(
    tarjeta,
    text="Presiona 'Comenzar' para iniciar la lectura.",
    font=("Arial", 11),
    bg="white",
    fg="#6b7280",
    wraplength=460,
    justify="center"
)
mensaje_temp.pack(pady=(0, 18))

# Separador visual
separador = tk.Frame(tarjeta, height=1, bg="#e5e7eb")
separador.pack(fill="x", pady=10)

# Humedad
texto_hum = tk.Label(
    tarjeta,
    text="Humedad",
    font=("Arial", 13, "bold"),
    bg="white",
    fg="#374151"
)
texto_hum.pack()

humedad_label = tk.Label(
    tarjeta,
    text="-- %",
    font=("Arial", 38, "bold"),
    bg="white",
    fg="#111827"
)
humedad_label.pack(pady=(5, 0))

mensaje_hum = tk.Label(
    tarjeta,
    text="Esperando inicio del programa...",
    font=("Arial", 11),
    bg="white",
    fg="#6b7280",
    wraplength=460,
    justify="center"
)
mensaje_hum.pack(pady=(0, 5))

# Estado de conexión
estado_conexion = tk.Label(
    ventana,
    text="Arduino sin conectar",
    font=("Arial", 10, "bold"),
    bg="#f4f6f8",
    fg="#6b7280"
)
estado_conexion.pack(pady=(15, 2))

# Estado de lectura
estado_lectura = tk.Label(
    ventana,
    text="Presiona comenzar para iniciar",
    font=("Arial", 10),
    bg="#f4f6f8",
    fg="#6b7280"
)
estado_lectura.pack(pady=(0, 10))

# Botones
frame_botones = tk.Frame(
    ventana,
    bg="#f4f6f8"
)
frame_botones.pack(pady=10)

boton_comenzar = tk.Button(
    frame_botones,
    text="Comenzar",
    command=comenzar_programa,
    width=14,
    font=("Arial", 10, "bold"),
    bg="#1f8f4d",
    fg="white",
    relief="flat",
    padx=10,
    pady=6
)
boton_comenzar.grid(row=0, column=0, padx=8)

boton_finalizar = tk.Button(
    frame_botones,
    text="Finalizar / Salir",
    command=finalizar_programa,
    width=14,
    font=("Arial", 10, "bold"),
    bg="#111827",
    fg="white",
    relief="flat",
    padx=10,
    pady=6
)
boton_finalizar.grid(row=0, column=1, padx=8)

ventana.protocol("WM_DELETE_WINDOW", finalizar_programa)
ventana.mainloop()