import httplib
import picamera
import time
import smtplib
import sys
from datetime import datetime
from smtplib import SMTP
from smtplib import SMTPException
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from twython import Twython
from termcolor import colored
import urllib3

urllib3.disable_warnings()

CONSUMER_KEY = ' '
CONSUMER_SECRET = ' '
ACCESS_KEY = ' '
ACCESS_SECRET = ' '
REMOTE_SERVER = "www.google.com"

twitterapi = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)



def is_connected():
    conn = httplib.HTTPConnection("www.google.com")
    try:
        conn.request("HEAD", "/")
        return True
    except:
        return False

hecho = "n"

FechaDeInicio = datetime.now()
HoraDeInicio = FechaDeInicio.hour
HoraDeIrACasa = HoraDeInicio + 4
HoraActual = HoraDeInicio
print "************************************************************************************************************************************************"
print "************************************************************************************************************************************************"
print "/$$$$$$$$ /$$           /$$                           /$$$$$$$                                /$$            "                                  
print "| $$_____/| $$          |__/                          | $$__  $$                              | $$              "                                
print "| $$      | $$ /$$   /$$ /$$ /$$$$$$$   /$$$$$$       | $$  \ $$  /$$$$$$   /$$$$$$$  /$$$$$$ | $$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$  /$$   /$$"
print "| $$$$$   | $$| $$  | $$| $$| $$__  $$ /$$__  $$      | $$$$$$$/ |____  $$ /$$_____/ /$$__  $$| $$__  $$ /$$__  $$ /$$__  $$ /$$__  $$| $$  | $$"
print "| $$__/   | $$| $$  | $$| $$| $$  \ $$| $$  \ $$      | $$__  $$  /$$$$$$$|  $$$$$$ | $$  \ $$| $$  \ $$| $$$$$$$$| $$  \__/| $$  \__/| $$  | $$"
print "| $$      | $$| $$  | $$| $$| $$  | $$| $$  | $$      | $$  \ $$ /$$__  $$ \____  $$| $$  | $$| $$  | $$| $$_____/| $$      | $$      | $$  | $$"
print "| $$      | $$|  $$$$$$$| $$| $$  | $$|  $$$$$$$      | $$  | $$|  $$$$$$$ /$$$$$$$/| $$$$$$$/| $$$$$$$/|  $$$$$$$| $$      | $$      |  $$$$$$$"
print "|__/      |__/ \____  $$|__/|__/  |__/ \____  $$      |__/  |__/ \_______/|_______/ | $$____/ |_______/  \_______/|__/      |__/       \____  $$"
print "               /$$  | $$               /$$  \ $$                                    | $$                                               /$$  | $$"
print "              |  $$$$$$/              |  $$$$$$/                                    | $$                                              |  $$$$$$/"
print "               \______/                \______/                                     |__/                                               \______/ "
print "************************************************************************************************************************************************"
print "************************************************************************************************************************************************"
                                                                                                                                                                                                                                                   
                                                                                                                                                
                                                                                                                                                
                                                                                                                                                
                                                                                                                                    

print colored('[**RELOJ**]  ','green'), "Empezamos a las :", HoraDeInicio,"H"
print colored('[**RELOJ**]  ','green'), "Terminaremos a las:", HoraDeIrACasa,"H"

i = 1

while (HoraActual != HoraDeIrACasa):
    name = 'photo' + str(i) + '.jpg'
    print colored('[**CAMARA**] ','yellow'), "Haciendo foto:", colored(name, 'magenta')
    with picamera.PiCamera() as camera:
	camera.start_preview()
	time.sleep(2)
        camera.led = False
	camera.resolution = (2592, 1944)
	camera.capture(name)
	camera.led = False
	camera.resolution = (640, 480)
	camera.capture('sd_' + name)

    print colored('[**RELOJ**]  ', 'green'), "Hora actual: ", HoraActual,"H"
    print colored('[**RELOJ**]  ', 'green'), "Hora fin: ", HoraDeIrACasa,"H"

    print colored("[**PING**]   ", 'green'), "Hay conexion: ", colored(is_connected(),'green')
    if(is_connected() == True):
        f_time = datetime.now().strftime('%a %d %b @ %H:%M')


        toaddr = ' '    # redacted
        me = ' ' # redacted
        subject = 'Foto ' + f_time

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = me
        msg['To'] = toaddr
        msg.preamble = "Foto @ " + f_time

        fp = open(name, 'rb')
        img = MIMEImage(fp.read())
        fp.close()
        msg.attach(img)

        try:
            s = smtplib.SMTP('smtp.gmail.com',587)
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(user = ' ',password = ' ')
            s.sendmail(me, toaddr.split(","), msg.as_string())
            s.quit()
            print colored("[**SMTP**]   ", 'green'), "Correo enviado"
        except SMTPException as error:
            print colored("[**SMTP**]   ", 'red'), "Error: no se pudo enviar el correo :  {err}".format(err=error)


	FechaActual = datetime.now()
        HoraActual = FechaActual.hour
        MinutoActual = FechaActual.minute
	if(hecho != MinutoActual):
#        if((MinutoActual % 2) == 0) and (hecho != MinutoActual):
	    hecho = MinutoActual
	    print colored("[**TWITTER**]", 'cyan'), "Asignando foto"	
	    LeFoto = open(name,'rb')
	    response = twitterapi.upload_media(media=LeFoto)
	    print colored("[**TWITTER**]", 'cyan'), "Enviando tweet"	
	    try:   
	        twitterapi.update_status(status='Mirad donde estoy! -->', media_ids=[response['media_id']])      
		print colored("[**TWITTER**]", 'cyan') ,"Tweet enviado"
		LeFoto.close()
	    except:
		print colored("[**TWITTER**]", 'red'), "Error al enviar el tweet"
	i = i + 1
	print colored("**************************************",'grey')      
    else:
	print colored("[**PING**]   ", 'green'), "Hay conexion: ", colored(is_connected(),'red')

        i = i + 1
        pass
	print colored("**************************************",'grey')
 
    
   
