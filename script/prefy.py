# Importation des bibliothèques
import csv
from datetime import datetime, date
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from discord_webhook import DiscordWebhook, DiscordEmbed

# Définition des fonctions
def cocherCondition():
    elem = driver.find_element(By.NAME, "condition")
    elem.send_keys(Keys.SPACE)
def appuyerNextButton():
    elem = driver.find_element(By.NAME, "nextButton")
    elem.send_keys(Keys.SPACE)
def compterLesCreneaux():
    global creneauxLibres, creneauxComplets, periodeTableauCreneaux
    creneauxLibres = creneauxComplets = 0
    periodeTableauCreneaux = lireDateCreneau()
    
    trParsed = driver.find_elements(By.XPATH, "/html/body/main/div/div/div/div[2]/form/div[1]/div[4]/table/tbody/tr/td" )
    for td in trParsed:
        td = td.text
        if td == "complet":
            creneauxComplets = creneauxComplets + 1
        elif td == "libre":
            creneauxLibres = creneauxLibres + 1
        else:
            pass
    
    print("Script  : Il y a " + str(creneauxLibres) + " créneaux libres et " + str(creneauxComplets) + " créneaux complets" + " la " + str(periodeTableauCreneaux))
    return creneauxLibres, creneauxComplets, periodeTableauCreneaux
def lireDateCreneau():
    periodeTableauCreneaux = driver.find_element(By.XPATH, "/html/body/main/div/div/div/div[2]/form/div[1]/div[4]/table/thead/tr[1]/th[2]").text
    print(periodeTableauCreneaux)
    return periodeTableauCreneaux
def notifierSurDiscord(demarcheURL, webhookURL, creneauxLibres, creneauxComplets, compteurGuichet, periodeTableauCreneaux): ## https://github.com/lovvskillz/python-discord-webhook
    print("Discord : Il y a " + str(creneauxLibres) + " créneaux libres et " + str(creneauxComplets) + " créneaux complets au guichet " + str(compteurGuichet+1) + ". La semaine parsée est la " + str(periodeTableauCreneaux) +  "\n")
    webhook = DiscordWebhook(url=webhookURL)

    ## Formation de l'embed
    embed = DiscordEmbed(
		title = str(creneauxLibres) + " RDV disponible(s)",
        description = "sur "  + str(creneauxLibres+creneauxComplets) + " créneaux au total.",
		color = '6300ab' ## decimal (color=242424)  hex (color="03b2f8")
	)
    embed.add_embed_field(name= "GUICHET", value = "N°" + str(compteurGuichet+1))
    embed.add_embed_field(name= "PREMIERS CRENEAUX", value = str(periodeTableauCreneaux))
    embed.set_author(
		name = "Cliquez ici pour aller sur le site.",
		url =  demarcheURL,
		icon_url="https://upload.wikimedia.org/wikipedia/fr/thumb/e/ee/Pr%C3%A9fet_de_la_Seine-Maritime.svg/171px-Pr%C3%A9fet_de_la_Seine-Maritime.svg.png"
    )
    embed.set_footer(text = "Prefy76 • Version " + versionScript)
    embed.set_timestamp()

    webhook.add_embed(embed) ## ajoute l'embed au webhook
    response = webhook.execute() ## envoie le webhook
def exporterResultatsEnCSV(creneauxLibres, creneauxComplets):
    with open('statistiques.csv', 'a') as statistiquesCSV: #header du CSV : timestamp, numeroDepartement, sousPrefecture, nomDemarche, creneauxLibres, creneauxComplets, totalCreneaux
        statistiquesCSV.write("\n"+str(datetime.now().timestamp())+","+str(ligneCSV['numeroDepartement'])+","+str(ligneCSV['sousPrefecture'])+","+str(ligneCSV['nomDemarche'])+","+str(creneauxLibres)+","+str(creneauxComplets)+","+str(creneauxLibres+creneauxComplets))

# Préparer le nécessaire pour les logs et l'export des données
versionScript =  "2.6"
jour = date.today().strftime("%y-%m-%d") #format AA/MM/JJ
heure = datetime.now().strftime("%H:%M") #format HH:MM
jourEtHeure = str(jour) + " " + str(heure)

# Configurer et lancer le WebDriver
options = Options()
options.add_argument("--headless") #permet au webdriver de s'exécuter sans fenêtre
options.add_experimental_option('excludeSwitches', ['enable-logging']) #le webdriver ne va pas envoyer ses logs dans la console
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(120) #initialise le comportement d'attente du webdriver pour permettre une exécution plus fluide.

print("Prefy76 : " + jourEtHeure)

with open('dictionnaire.csv', newline='') as fichierCSV:
    csvParser = csv.DictReader(fichierCSV)
    for ligneCSV in csvParser:
        print("Vérification de " + ligneCSV['nomDemarche'])
        compteurGuichet = 0
        driver.get(ligneCSV['urlDemarche'])
        cocherCondition()
        appuyerNextButton()

        elem = driver.find_element(By.XPATH, "/html/body/main/div/div/div/div[2]/h2").text # récupère le titre de la page pour ensuite la comparer avec les valeurs connues
        if elem == "Vérification de disponibilité": # titre de la page  quand il n'y a aucun RDV disponibles et que nous sommes invités à revenir plus tard
            print("Aucun RDV disponible.")
            exporterResultatsEnCSV(0, 0)
            pass
        elif elem == "Description de la nature du rendez-vous": # titre de la page qui annonce les modalités de RDV. Elle n'apparaît que s'il y a des créneaux disponibles.
            appuyerNextButton()
            elem = driver.find_element(By.XPATH, "/html/body/main/div/div/div/div[2]/h2").text #récupère ici le titre de la page qui suit afin de s'assurer de la validité de la page.
            if elem != "Choix d'une plage horaire":
                pass
            else:
                compterLesCreneaux()
                exporterResultatsEnCSV(creneauxLibres, creneauxComplets)
                notifierSurDiscord(ligneCSV['urlDemarche'], ligneCSV['urlWebhookDiscord'], creneauxLibres, creneauxComplets, compteurGuichet, periodeTableauCreneaux)
        elif elem == "Choix de la nature du rendez-vous": #ce texte signifie qu'il existe plusieurs guichets et que l'utilisateur va devoir choisir en activant un bouton radio. Nous allons donc compter le nombre de guichets, terminer cette itération et en lancer le nombre suffisant pour refaire le parcours pour chaque guichet. Je garde le nombre de guichets dans la communication afin d'envoyer également quel guichet est concerné.
            totalCreneauxLibres = totalCreneauxComplets = 0 #pour les statistiques, les guichets n'ont aucun intérêt. J'initialise donc des variables qui garderont le total
            radioParsed = driver.find_elements(By.XPATH, "/html/body/main/div/div/div/div[2]/form/fieldset/p")
            for p in radioParsed:
                compteurGuichet = compteurGuichet +1 # Jusqu'ici, le code compte le nombre de boutons radio afin de déterminer combien de page il va devoir chercher.
            print("Il y a " + str(compteurGuichet) + " guichets.")
            elem = driver.find_element(By.XPATH, "/html/body/main/div/div/div/div[2]/form/fieldset/p[" + str(compteurGuichet) + "]/input") #sélectionne le bouton radio.
            appuyerNextButton()
            # nous allons vérifier si le parcours entamé se conclue sur des créneaux dispos.
            if elem == "Description de la nature du rendez-vous":
                    elem = driver.find_element(By.NAME, "nextButton")
                    elem.send_keys(Keys.SPACE)
                    compterLesCreneaux()
                    notifierSurDiscord(ligneCSV['urlDemarche'], ligneCSV['urlWebhookDiscord'], creneauxLibres, creneauxComplets, compteurGuichet, periodeTableauCreneaux)
                    totalCreneauxLibres = totalCreneauxLibres + creneauxLibres
                    totalCreneauxComplets = totalCreneauxComplets + creneauxComplets
            else: print("- Guichet " + str(compteurGuichet) + " : pas de RDV")
            compteurGuichet = compteurGuichet - 1
            while compteurGuichet != 0:
                driver.get(ligneCSV['urlDemarche'])
                cocherCondition()
                appuyerNextButton()
                elem = driver.find_element(By.XPATH, "/html/body/main/div/div/div/div[2]/form/fieldset/p[" + str(compteurGuichet) + "]/input")
                elem.send_keys(Keys.SPACE)
                appuyerNextButton()
                elem = driver.find_element(By.XPATH, "/html/body/main/div/div/div/div[2]/h2").text
                if elem == "Description de la nature du rendez-vous":
                    appuyerNextButton()
                    compterLesCreneaux()
                    notifierSurDiscord(ligneCSV['urlDemarche'], ligneCSV['urlWebhookDiscord'], creneauxLibres, creneauxComplets, compteurGuichet, periodeTableauCreneaux)
                    totalCreneauxLibres = totalCreneauxLibres + creneauxLibres
                    totalCreneauxComplets = totalCreneauxComplets + creneauxComplets
                else: print("- Guichet " + str(compteurGuichet) + " : pas de RDV")
                compteurGuichet = compteurGuichet - 1
            exporterResultatsEnCSV(totalCreneauxLibres,totalCreneauxComplets)
        else:
            print("ça n'a pas fonctionné.\n")

        driver.close
