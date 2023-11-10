import time
import logging
import BlynkLib 
from gpiozero import LED
from sensor import Sensor
from email_alert import send_email_alert

 #Blynk Auth Token
BLYNK_TEMPLATE_ID =  "TMPL2oKuWKYP2"
BLYNK_TEMPLATE_NAME =  "First Blynk App"
BLYNK_AUTH_TOKEN = "ythhKjjZZy60pfJ4YjciruymQLKxL-Hw"

blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)

# Email Configuration
SMTP_SERVER = 'smtp.gmail.com.'
SMTP_PORT = 587
EMAIL_USERNAME = 'jiajiaiot@gmail.com'
EMAIL_PASSWORD = 'licd wrtl fzvc odwg '
RECIPIENT_EMAIL = 'jyang5@academic.rrc.ca'

#LED
greenLED = LED(17)
redLED = LED(13)
blueLED = LED(21)

#instance for sensor
pin = 0


#logging config
logging.basicConfig(filename='moisture.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

while True:
    try:
        moisture = Sensor(pin)
        m_value = moisture.moisture()
        if m_value < 500:
            m_level = 'Low'
            redLED.on() #Red LED indicates Low moisture.
            greenLED.off()
            blueLED.off()
            send_email_alert(m_level, EMAIL_USERNAME, RECIPIENT_EMAIL, SMTP_SERVER, SMTP_PORT,EMAIL_PASSWORD) #Notifies user via email when the moisture level goes "Low"
        elif 500 <= m_value and m_value < 610:
            m_level = 'Normal'
            greenLED.on()  #Green LED indicates Normal moisture.
            redLED.off()
            blueLED.off()
        else:
            m_level = 'High'
            blueLED.on()  #Blue LED indicates High moisture.
            redLED.off()
            greenLED.off()
        
        logging.info(f'Moisture Level: {m_level}')
        blynk.run()
        blynk.virtual_write(4, m_value) #Displays current numerical moisture value.
        blynk.virtual_write(5, m_level) #Displays which category moisture level is currently in: Low, Normal, High.
        print('Moisture value: {0}, {1}'.format(m_value, m_level))
        time.sleep(60) ## Check every minute
        
    except Exception as e:
        logging.error(f'Error: {str(e)}')  


