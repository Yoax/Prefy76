# Importation des bibliothèques
import time
import csv
from datetime import datetime, date
#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.by import By
#from selenium.webdriver.chrome.options import Options
#from discord_webhook import DiscordWebhook, DiscordEmbed

# Définition des fonctions
def cocherCondition():
    elem = driver.find_element(By.NAME, "condition")
    elem.send_keys(Keys.SPACE)
def appuyerNextButton():
    elem = driver.find_element(By.NAME, "nextButton")
    elem.send_keys(Keys.SPACE)
def compterLesCreneaux():
    global libre, complet, periodeParsed
    periodeParsed = lireDateCreneau()
    
    trParsed = driver.find_elements(By.XPATH, "/html/body/main/div/div/div/div[2]/form/div[1]/div[4]/table/tbody/tr/td" )
    for td in trParsed:
        td = td.text
        if td == "complet":
            complet = complet + 1
        elif td == "libre":
            libre = libre + 1
        else:
            pass
    
    print("Script  : Il y a " + str(libre) + " créneaux libres et " + str(complet) + " créneaux complets" + " la " + str(periodeParsed))
    return libre, complet, periodeParsed
def lireDateCreneau():
    periodeParsed = driver.find_element(By.XPATH, "/html/body/main/div/div/div/div[2]/form/div[1]/div[4]/table/thead/tr[1]/th[2]").text
    print(periodeParsed)
    return periodeParsed


# Préparer le nécessaire pour les logs et l'export des données
jour = date.today().strftime("%y-%m-%d") #format AA/MM/JJ
heure = datetime.now().strftime("%H:%M") #format HH:MM
jourEtHeure = str(jour) + " " + str(heure)

# Configurer et lancer le WebDriver
options = Options()
options.add_argument("--headless") #permet au webdriver de s'exécuter sans fenêtre
options.add_experimental_option('excludeSwitches', ['enable-logging']) #le webdriver ne va pas envoyer ses logs dans la console
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(tempsAttente) #initialise le comportement d'attente du webdriver pour permettre une exécution plus fluide.

with open('/Users/yoan/Developer/Prefy/Prefy-main/script/conf/liens.csv', newline='') as fichierCSV:
    csvParser = csv.DictReader(fichierCSV)
    for demarche in csvParser:
        driver.get
