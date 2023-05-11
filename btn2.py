from sys import exit
import cv2
import pytesseract
import pyttsx3
import RPi.GPIO as GPIO

# Set up GPIO
button_pin = 18  # GPIO pin number for the button
exit_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(exit_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
cam = cv2.VideoCapture(0)

while True:
    ret, img = cam.read()
    cv2.imshow("Test", img)

    if not ret:
        break

    button_state = GPIO.input(button_pin)
    exit_state = GPIO.input(exit_pin)

    if button_state == GPIO.LOW:
        # Button pressed
        print("Image saved")
        file = '/home/pi/dim-github/img.jpg'
        cv2.imwrite(file, img)
        print("Close")
        break

    if exit_state == GPIO.LOW:
        print("Exiting...")
        exit()
        break

cam.release()
cv2.destroyAllWindows()

img = cv2.imread('img.jpg')
text = pytesseract.image_to_string(img)
print(text)

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Speed of speech
    engine.say(text)
    engine.runAndWait()

speak(text)