from machine import Pin, PWM, time_pulse_us
import time

# --- CONFIGURACIÓN DE PINES ---
trig = Pin(5, Pin.OUT)
echo = Pin(18, Pin.IN)
servo = PWM(Pin(13), freq=50)
led_alerta = Pin(12, Pin.OUT) # El nuevo LED de alarma

def set_angle(angle):
    duty = int((angle / 180) * 97 + 26)
    servo.duty(duty)

def medir_distancia():
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    duracion = time_pulse_us(echo, 1)
    return (duracion * 0.0343) / 2

print("--- SISTEMA DE RADAR CON ALERTA VISUAL ---")

while True:
    for angulo in range(0, 181, 15): # Barrido de 15 en 15 grados
        set_angle(angulo)
        distancia = medir_distancia()
        
        print(f"Ángulo: {angulo}° | Distancia: {distancia:.1f} cm")
        
        # Lógica de Alerta
        if distancia < 20:
            print("¡PELIGRO! Objeto detectado.")
            led_alerta.value(1)  # Enciende el LED
            time.sleep(0.5)      # Pausa para que se note la detección
        else:
            led_alerta.value(0)  # Apaga el LED
            
        time.sleep(0.1)
