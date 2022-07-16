import network, time, urequests   # Cómo se trabaja con APIs hay que manejar esta libreria que ya la tiene machine para peticiones de recursos en APIs
from machine import Pin, ADC
from utelegram import Bot  # Utilizamos el módulo utelegram para que funcione
from machine import Pin, I2C, sleep
import mpu6050 #Modulo de trabajo de Gyroscopio o acelerometro

i2c = I2C(scl=Pin(22), sda=Pin(21))  #initializing the I2C method for ESP32

ledRed= Pin(13, Pin.OUT)  # Pin del Led Rojo
ledBlue=Pin(12, Pin.OUT)  # Pin del Led Blue
ledGreen=Pin(14,Pin.OUT)  # Pin del Led Green
ledBlue2=Pin(26, Pin.OUT) # Pin del Led Blue Posición niño 
ledRed2=Pin(27, Pin.OUT)  # Pin del Led Red Posición niño 
ledWhite=Pin(33, Pin.OUT) # Pin del Led White Posición giro 
ledRed3=Pin(25, Pin.OUT)  # Pin del Led Red Posición  giro
mpu= mpu6050.accel(i2c)

def conectaWifi (red, password):
      global miRed
      miRed = network.WLAN(network.STA_IF)     
      if not miRed.isconnected():              #Si no está conectado…
          miRed.active(True)                   #activa la interface
          miRed.connect(red, password)         #Intenta conectar con la red
          print('Conectando a la red', red +"…")
          timeout = time.time ()
          while not miRed.isconnected():           #Mientras no se conecte..
              if (time.ticks_diff (time.time (), timeout) > 10):
                  return False
      return True

if conectaWifi ("Julian", "camilo1205"):

    print ("Conexión exitosa!")
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
    
def send_msg(text):
    token = "5438347693:AAGWAbYVt4LmBtF132m71mBMrr7GRvWL62A"
    chat_id="1712677947"
    
    request_url="https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" +chat_id+ "&text=" + text
    res= urequests.get(request_url)
    return res.json()
    
#send_msg("Ahora si sirve")
while True:  
  
  temps =(mpu.get_values())

  tem=float(temps["Tmp"] )# Temperatura giroscopio
  zacelerometro=temps["AcZ"] # Acelerometro Eje Z
    
  if tem < 36:
    send_msg("Revisa la temperatura de tu bebé, está muy bajita.")
    print("Revisa la temperatura de tu bebé, está muy bajita." , tem)  
    ledBlue.value(1)
    ledGreen.value(0)
    ledRed.value(0)
  
  elif tem >= 36 and tem <= 38:
    send_msg("La temperatura de tu bebé, es normal.")
    print("La temperatura de tu bebé, es normal." , tem)  
    ledBlue.value(0)
    ledGreen.value(1)
    ledRed.value(0)
    
  else:
    send_msg("Revisa la temperatura de tu bebé, está muy alta.")  
    print("Revisa la temperatura de tu bebé, está muy alta." , tem)  
    ledBlue.value(0)
    ledGreen.value(0)
    ledRed.value(1)