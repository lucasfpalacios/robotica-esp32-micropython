from machine import Pin, PWM, time_pulse_us
import time

# Configuración Sensor Ultrasonido
trig = Pin(5, Pin.OUT)
echo = Pin(18, Pin.IN)

# Configuración Servomotor (PWM en Pin 13)
# Frecuencia típica de servos: 50Hz
servo = PWM(Pin(13), freq=50)

def set_angle(angle):
    # Convierte grados (0-180) a Duty Cycle para MicroPython
    # El rango suele ser entre 20 y 120 para 50Hz en ESP32
    duty = int((angle / 180) * 100 + 26)
    servo.duty(duty)

def medir_distancia():
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    duracion = time_pulse_us(echo, 1)
    return (duracion * 0.0343) / 2

print("--- Radar con Servo Iniciado ---")

while True:
    dist = medir_distancia()
    print("Distancia: {:.2f} cm".format(dist))
    
    if dist < 20:
        print("¡Obstáculo! Girando servo...")
        set_angle(180) # Mueve el servo a un extremo
    else:
        set_angle(90)  # Vuelve al centro
        
    time.sleep(0.2)
