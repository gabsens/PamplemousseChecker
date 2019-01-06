from requests import session
import smtplib
import threading

#Identifiants à remplir
pamplemousse_user = "XXXXXX"
pamplemousse_pass = "XXXXXX"
gmail_user = 'XXXXXX@gmail.com'  
gmail_password = 'XXXXXXX'

payload = {
	"sph_org_location": '/',
	"sph_username": pamplemousse_user, 
	"sph_password": pamplemousse_pass, 
}

#Authentification et requête de la page de notes
with session() as c:
    c.post('https://pamplemousse.ensae.fr/site_publishing_helper/login_check/0', data=payload)
    response = c.get('https://pamplemousse.ensae.fr/index.php?p=105')

sent_from = gmail_user  
to = [gmail_user]  
email_text = 'Changement dans les notes'

old = response.text

def check():
    threading.Timer(300.0, check).start() #intervalle de temps pour la vérification
    global old
    with session() as c:
    	c.post('https://pamplemousse.ensae.fr/site_publishing_helper/login_check/0', data=payload)
    	response = c.get('https://pamplemousse.ensae.fr/index.php?p=105')
    if response.text != old:
    	server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    	server.ehlo()
    	server.login(gmail_user, gmail_password)
    	server.sendmail(sent_from, to, email_text)
    	server.close()
    	old = response.text


check()