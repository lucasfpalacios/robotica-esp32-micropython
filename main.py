from machine import Pin, PWM, time_pulse_us
import time

# --- CONFIGURACIÓN ---
trig = Pin(5, Pin.OUT)
echo = Pin(18, Pin.IN)
servo = PWM(Pin(13), freq=50)
led_alerta = Pin(12, Pin.OUT)

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

print("--- RADAR ACTIVO: MODO ALERTA INTERMITENTE ---")

while True:
    for angulo in range(0, 181, 15):
        set_angle(angulo)
        dist = medir_distancia()
        
        print(f"Ángulo: {angulo}° | Distancia: {dist:.1f} cm")
        
        if dist < 20:
            print(">>> ¡OBJETO DETECTADO! <<<")
            # Efecto de titileo (Blink)
            for _ in range(3): 
                led_alerta.value(1)
                time.sleep(0.1)
                led_alerta.value(0)
                time.sleep(0.1)
        else:
            led_alerta.value(0)
            
        time.sleep(0.05)
