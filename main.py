import network
import urequests
import time
import random
from machine import Pin, PWM, I2C, time_pulse_us
from machine_i2c_lcd import I2cLcd

# --- CONFIGURACIÓN DE TELEGRAM ---
TOKEN = "8639210783:AAEjcxjxyhhygBRdkJn30FUindPriE9V2bE" 
CHAT_ID = "6206022332"

i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)
trig = Pin(5, Pin.OUT); echo = Pin(18, Pin.IN)
servo = PWM(Pin(13), freq=50)
led_alerta = Pin(12, Pin.OUT); buzzer = PWM(Pin(14))

def conectar_wifi():
    lcd.clear(); lcd.putstr("WiFi Connect...")
    wlan = network.WLAN(network.STA_IF); wlan.active(True)
    wlan.connect('Wokwi-GUEST', '')
    while not wlan.isconnected(): time.sleep(0.1)
    lcd.clear(); lcd.putstr("WiFi: Online"); time.sleep(1)

def enviar_telegram(distancia):
    # Lógica de rangos ajustada para que el "Amarillo" tenga más espacio
    if distancia < 6:
        nivel, accion = "🔴 CRITICO", "¡INTRUSO SOBRE EL SENSOR!"
    elif 6 <= distancia < 15:
        nivel, accion = "🟡 ADVERTENCIA", "Objeto acercandose rapido."
    else:
        nivel, accion = "🔵 AVISO", "Presencia detectada lejos."

    texto = f"{nivel}\nDistancia: {distancia:.1f} cm\n{accion}"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={texto.replace(' ', '%20').replace('\n', '%0A')}"
    
    try:
        res = urequests.get(url, timeout=2)
        res.close()
        print(f"Enviado: {nivel} ({distancia:.1f} cm)")
    except:
        print("Error de red")

# --- INICIO ---
conectar_wifi()
lcd.clear()
ultimo_envio = 0

while True:
    for angulo in range(0, 181, 30):
        servo.duty(int((angulo / 180) * 97 + 26))
        
        # --- GENERADOR ALEATORIO PURO ---
        # Tira un número entre 2 y 35 en cada movimiento del servo
        dist_v = random.uniform(2, 35) 
        
        lcd.move_to(0, 0); lcd.putstr(f"Ang: {angulo:3} deg")
        lcd.move_to(0, 1); lcd.putstr(f"V-Dist: {dist_v:4.1f}cm")
        
        # Si la distancia aleatoria cae en zona de alerta (menos de 20)
        if dist_v < 20:
            # Feedback físico
            led_alerta.value(1)
            buzzer.freq(1500); buzzer.duty(512)
            time.sleep(0.1)
            led_alerta.value(0); buzzer.duty(0)
            
            # Control de tiempo de envío
            ahora = time.time()
            if ahora - ultimo_envio > 5:
                enviar_telegram(dist_v)
                ultimo_envio = ahora
        else:
            led_alerta.value(0)
            time.sleep(0.1)

        time.sleep(0.2)
