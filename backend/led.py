import paho.mqtt.client as mqtt
import time
from colorama import init, Fore


# Initialize colorama
init(autoreset=True)


# State control
led_on = False


def show_leds():
    print(Fore.RED + "LED 0: Red")
    print(Fore.GREEN + "LED 1: Green")
    print(Fore.BLUE + "LED 2: Blue")
    print(Fore.YELLOW + "LED 3: Yellow")
    print(Fore.MAGENTA + "LED 4: Magenta")
    print("-----")


def clear_leds():
    print("LEDs OFF")
    print("-----")


# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe("led/control")


def on_message(client, userdata, msg):
    global led_on
    command = msg.payload.decode().strip().lower()
    print(f"Message Received on {msg.topic}: {command}")


    if command == "on":
        led_on = True
    elif command == "off":
        led_on = False


# MQTT Setup
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


# 🔁 Set to your Raspberry Pi IP address
client.connect("192.168.1.9", 1883, 60)


# Main loop
client.loop_start()
print("LED MQTT Simulator Started...")


try:
    while True:
        if led_on:
            show_leds()
        else:
            clear_leds()
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopped by user.")
    client.loop_stop()
    client.disconnect()






	
