import machine
import time

# Configuración de Pines
trigger = machine.Pin(5, machine.Pin.OUT)
echo = machine.Pin(18, machine.Pin.IN)

def get_distance():
    # Asegurar que el trigger esté apagado
    trigger.value(0)
    time.sleep_us(2)
    
    # Enviar un pulso de 10 microsegundos
    trigger.value(1)
    time.sleep_us(10)
    trigger.value(0)
    
    # Medir el tiempo que el pin Echo está en alto (1)
    duracion = machine.time_pulse_us(echo, 1)
    
    # Calcular distancia (Velocidad del sonido / 2)
    distancia = (duracion * 0.0343) / 2
    return distancia

print("Iniciando sensor de proximidad...")

while True:
    d = get_distance()
    print("Distancia: {:.2f} cm".format(d))
    
    # Lógica de robot:
    if d < 20:
        print("¡OBSTÁCULO DETECTADO! Girando...")
    
    time.sleep(0.5)
    
