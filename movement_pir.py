import grovepi
import time

pir_sensor = 8
led_green = 5
led_red = 6

grovepi.pinMode(pir_sensor, "INPUT")
grovepi.pinMode(led_green, "OUTPUT")
grovepi.pinMode(led_red, "OUTPUT")

while True:
    try:
        if grovepi.digitalRead(pir_sensor):
            print "Motion"
            grovepi.digitalWrite(led_red, 1)
            grovepi.digitalWrite(led_green, 0)
        else:
            grovepi.digitalWrite(led_red, 0)
            grovepi.digitalWrite(led_green, 1)
            print "-"
        time.sleep(2)

    except IOError:
        print "Error"