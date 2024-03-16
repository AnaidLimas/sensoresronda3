from machine import Pin, ADC, I2C
import ssd1306
from time import sleep
import network
from umqtt.simple import MQTTClient

# Configuración de pines
PIN_SENSOR = 34  # Por ejemplo, puedes usar el pin 34 de la ESP32



# Inicialización del ADC
adc = ADC(Pin(PIN_SENSOR))

# Configuración del I2C para la pantalla OLED
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

MQTT_BROKER = "192.168.43.135"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_TOPIC = "utng/alm/ky-028"
MQTT_PORT = 1883

def conectar_wifi():
    print("Conectando WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('Adrian', '123456ad')
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.3)
    print("WiFi Conectada!")

def display_value(value):
    oled.fill(0)  # Limpiar pantalla
    oled.text("Valor del", 0, 0)
    oled.text("TEMPERATURA VALOR:", 0, 10)
    oled.text(str(value), 0, 30)
    oled.show()

def publicar_mensaje(msg):
    client.publish(MQTT_TOPIC, msg)

def verificar_funcionamiento():
    while True:
        valor_analogico = adc.read() 
        publicar_mensaje(str(valor_analogico))  # Publicar valor analógico
        print(valor_analogico)
        display_value(valor_analogico)
        sleep(15)
        

# Bucle principal
print('Programa iniciado. Presiona CTRL+C para salir.')
conectar_wifi()
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASSWORD, keepalive=0)
client.connect()

verificar_funcionamiento()