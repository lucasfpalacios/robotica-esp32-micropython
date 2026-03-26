from machine import Pin, PWM, time_pulse_us
import time

# --- CONFIGURACIÓN ---
trig = Pin(5, Pin.OUT)
echo = Pin(18, Pin.IN)
servo = PWM(Pin(13), freq=50)
led_alerta = Pin(12, Pin.OUT)
# Configuración del Buzzer en pin 14
buzzer = PWM(Pin(14))

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

def sonar_alarma():
    """Hace sonar el buzzer y parpadear el LED"""
    for _ in range(2):
        led_alerta.value(1)
        buzzer.freq(1000) # Tono agudo
        buzzer.duty(512)  # Volumen al 50%
        time.sleep(0.1)
        
        led_alerta.value(0)
        buzzer.duty(0)    # Silencio
        time.sleep(0.1)

print("--- SISTEMA DE SEGURIDAD TOTAL ACTIVADO ---")

while True:
    for angulo in range(0, 181, 15):
        set_angle(angulo)
        dist = medir_distancia()
        
        print(f"Ángulo: {angulo}° | Distancia: {dist:.1f} cm")
        
        if dist < 20:
            print(">>> ¡INTRUSO DETECTADO! <<<")
            sonar_alarma()
        else:
            led_alerta.value(0)
            buzzer.duty(0)
            
        time.sleep(0.05)
