from machine import Pin, PWM, time_pulse_us
import time

# --- CONFIGURACIÓN ---
trig = Pin(5, Pin.OUT)
echo = Pin(18, Pin.IN)
servo = PWM(Pin(13), freq=50)

def set_angle(angle):
    # Mapeo de 0-180 grados a duty cycle (26 a 123 aprox)
    duty = int((angle / 180) * 97 + 26)
    servo.duty(duty)

def medir_distancia():
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    duracion = time_pulse_us(echo, 1)
    dist = (duracion * 0.0343) / 2
    return dist

print("--- MODO EXPLORACIÓN ACTIVADO ---")

while True:
    # Barrido de 0 a 180 grados
    for angulo in range(0, 181, 10): # Salta de 10 en 10 grados
        set_angle(angulo)
        distancia = medir_distancia()
        
        print("Ángulo: {}° | Distancia: {:.1f} cm".format(angulo, distancia))
        
        if distancia < 30:
            print(">>> ¡OBJETO DETECTADO A {} CM! <<<".format(distancia))
            # Podés agregar una pausa o un sonido aquí
            time.sleep(1) 
            
        time.sleep(0.1)
