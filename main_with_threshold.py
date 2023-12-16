import umail
import network
import time
import machine
import utime
from machine import ADC, Pin

# Potentiometer Setup
adc_pin = Pin(26)
adc = ADC(adc_pin)
threshold = 0.2

# Email details
sender_email = 'angela.busheska@gmail.com'
sender_name = 'Angela Busheska'
sender_app_password = 'jixy uvhu cqtt ryem'
recipient_email = 'angela.busheska@gmail.com'
email_subject = 'Email from RPi Pico'

# Network credentials
ssid = 'Mojo-2.45GHz'
password = 'samster123'

# Connect to Wi-Fi
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

# Function to read voltage from the potentiometer
def read_voltage(adc):
    reading = adc.read_u16()   # Read ADC value
    voltage = reading * 3.3 / 65535  # Convert ADC reading to voltage
    return voltage

# Function to send email
def send_email(message):
    smtp = umail.SMTP('smtp.gmail.com', 465, ssl=True)
    smtp.login(sender_email, sender_app_password)
    smtp.to(recipient_email)
    smtp.write("From:" + sender_name + "<" + sender_email + ">\n")
    smtp.write("Subject:" + email_subject + "\n")
    smtp.write(message)
    smtp.send()
    smtp.quit()
    print("Email sent")

# Main loop
last_daily_update = utime.time()
while True:
    current_time = utime.time()
    voltage = read_voltage(adc)
    print("Voltage at the junction: ", voltage)

    if voltage < threshold:
        send_email("Potentiometer value is below the threshold\n")
        utime.sleep(60)  # Delay for 1 minute before checking again
    else:
        # Send a daily email if everything is fine
        if current_time - last_daily_update > 86400:  
            send_email("Everything is working great!\n")
            last_daily_update = current_time

    utime.sleep(1)  # Delay for 1 second

