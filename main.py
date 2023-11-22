 import umail
import network
import time

# Email details
sender_email = 'username@gmail.com'
sender_name = 'username'
sender_app_password = 'yourapppass'
recipient_email ='youremail'
email_subject ='yoursubject'

# Network credentials
ssid = 'yourssid'
password = 'yourpassword'

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


# Send email once after MCU boots up
smtp = umail.SMTP('smtp.gmail.com', 465, ssl=True)
smtp.login(sender_email, sender_app_password)
smtp.to(recipient_email)
smtp.write("From:" + sender_name + "<"+ sender_email+">\n")
smtp.write("Subject:" + email_subject + "\n")
smtp.write("This is an email from Raspberry Pi Pico")
smtp.send()
smtp.quit()
