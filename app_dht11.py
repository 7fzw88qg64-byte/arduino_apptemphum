import serial
import time

arduino = serial.Serial('COM4', 9600)
time.sleep(2)

print("Leyendo datos del sensor DHT11...")
print("Presiona Ctrl + C para detener.\n")

while True:
    try:
        linea = arduino.readline().decode('utf-8').strip()

        print("Dato recibido:", linea)

        if linea == "ERROR":
            print("Error leyendo el sensor DHT11")
            continue

        datos = linea.split(",")

        if len(datos) == 2:
            temperatura = datos[0]
            humedad = datos[1]

            print(f"Temperatura: {temperatura} °C | Humedad: {humedad} %")

    except KeyboardInterrupt:
        print("\nPrograma detenido.")
        arduino.close()
        break

    except Exception as e:
        print("Dato no válido recibido:", e)