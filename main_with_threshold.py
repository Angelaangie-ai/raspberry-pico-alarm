import umail
import network
import time
import machine
import utime
from machine import ADC, Pin

#Potentiometer Setup
adc_pin = Pin(26)  
adc = ADC(adc_pin)
threshold = 2048  

# Email details
sender_email = 'youremail@gmail.com'
sender_name = 'yourusername'
sender_app_password = 'yourapppass'
recipient_email ='recipientemail'
email_subject ='subject'

# Network credentials
ssid = 'ssid'
password = 'password'

#Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Wait for connection to establish
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
            break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)
    
# Manage connection errors
if wlan.status() != 3:
    raise RuntimeError('Network Connection has failed')
else:
    print('connected')


   
#Send an email when the reading goes above the threshold  
while True:
    pot_value = adc.read_u16()
    if pot_value > threshold:
        send_email()
        time.sleep(60)  # Delay to prevent rapid repeat emails
    time.sleep(1)  # Check potentiometer value every second
