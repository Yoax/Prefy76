# Importation des bibliothèques
## Général
import time
from datetime import datetime, date
## Pour le parse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
## Pour le webhook Discord
from discord_webhook import DiscordWebhook, DiscordEmbed

# Déclaration des variables
## Général
version = "2.5"
tempsAttente = 120 ###en secondes
jour = date.today().strftime("%y-%m-%d") ###format AA/MM/JJ
heure = datetime.now().strftime("%H:%M") ###format HH:MM
jourEtHeure = str(jour) + " " + str(heure)
nbRadio = 0
## Pour le parse
dictionnairePref = {
    "depot_1er_TDS":"https://www.seine-maritime.gouv.fr/booking/create/50382/0",
    "renouvellement_TDS":"https://www.seine-maritime.gouv.fr/booking/create/50389/0",
    "renouvellement_carte_resident" : "https://www.seine-maritime.gouv.fr/booking/create/50396",
    "retrait_TDS":"https://www.seine-maritime.gouv.fr/booking/create/50420/0",
    "retrait_recepisse":"https://www.seine-maritime.gouv.fr/booking/create/50416/0",
    "retrait_DCEM_TVR_TIV":"https://www.seine-maritime.gouv.fr/booking/create/51406/0",
    "regularisation_sejour":"https://www.seine-maritime.gouv.fr/booking/create/47116/0",
}

## Pour le webhook Discord
dictionnaireWebhooksDiscord = { 
    "depot_1er_TDS": "",
    "renouvellement_TDS": "",
    "renouvellement_carte_resident" : "",
    "retrait_TDS": "",
    "retrait_recepisse": "",
    "retrait_DCEM_TVR_TIV": "",
    "regularisation_sejour": "",
}
dictionnaireNomCompletDemarche = {
    "depot_1er_TDS":"dépôt d'un premier titre de séjour",
    "renouvellement_TDS":"renouvellement d'un titre de séjour",
    "renouvellement_carte_resident" : "renouvellement d'une carte de résident",
    "retrait_TDS":"retrait d'un titre de séjour ou d'une carte de résident",
    "retrait_recepisse":"renouvellement d'un récépissé",
    "retrait_DCEM_TVR_TIV":"retrait d'un document de voyage (DCEM, TVR ou TIV)",
    "regularisation_sejour":"régulariser un séjour",
}

# Création de fonctions
def notifierSurDiscord(demarcheURL, webhookURL, libre, complet, guichet, periodeParsed): ## https://github.com/lovvskillz/python-discord-webhook
    print("Discord : Il y a " + str(libre) + " créneaux libres et " + str(complet) + " créneaux complets au guichet " + str(guichet) + ". La semaine parsée est la " + str(periodeParsed) +  "\n")
    webhook = DiscordWebhook(url=webhookURL)

    ## Formation de l'embed
    embed = DiscordEmbed(
		title = str(libre) + " RDV disponible(s)",
        description = "sur "  + str(libre+complet) + " créneaux au total.",
		color = '6300ab'
	)
    embed.add_embed_field(name= "GUICHET", value = "N°" + str(guichet))
    embed.add_embed_field(name= "PREMIERS CRENEAUX", value = str(periodeParsed))
    embed.set_author(
		name = "Cliquez ici pour aller sur le site.",
		url =  demarcheURL,
		icon_url="https://upload.wikimedia.org/wikipedia/fr/thumb/e/ee/Pr%C3%A9fet_de_la_Seine-Maritime.svg/171px-Pr%C3%A9fet_de_la_Seine-Maritime.svg.png"
    )
    embed.set_footer(text = "Prefy76 • Version " + version)
    embed.set_timestamp()

    webhook.add_embed(embed) ## ajoute l'embed au webhook
    response = webhook.execute() ## envoie le webhook

def compterCreneaux():
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

print("Prefy76 (Version " + version + ") : " + jourEtHeure + "\n")
webhook = DiscordWebhook(url="", content='Prefy lancé !' + ' @ ' + str(jourEtHeure))
response = webhook.execute()


# Lancement du WebDriver sans tête
options = Options()
options.add_argument("--headless")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(tempsAttente)

for i in dictionnairePref:
    ## Nouveau tour
    nomDemarche = str(i)
    urlDemarche = str(dictionnairePref.get(i))
    urlWebhook = str(dictionnaireWebhooksDiscord.get(i))
    nomCompletDemarche = str(dictionnaireNomCompletDemarche.get(i))

    libre = 0
    complet = 0
    nbRadio = 0
    guichet = 1
    periodeParsed = "vide"

    print("\nVérification de " + nomDemarche + " en cours...")
    driver.get(urlDemarche)
    ## Coche le bouton d'acceptation
    elem = driver.find_element(By.NAME, "condition")
    elem.send_keys(Keys.SPACE)
    ## Appuie sur le bouton pour aller à la page suivante
    elem = driver.find_element(By.NAME, "nextButton")
    elem.send_keys(Keys.SPACE)
    ## Récupère et compare le texte
    elem = driver.find_element(By.XPATH, "/html/body/main/div/div/div/div[2]/h2").text
    if elem == "Vérification de disponibilité":
        print("Aucun RDV disponible.")
        pass
    elif elem == "Description de la nature du rendez-vous":
        elem = driver.find_element(By.NAME, "nextButton")
        elem.send_keys(Keys.SPACE)
        elem = driver.find_element(By.XPATH, "/html/body/main/div/div/div/div[2]/h2").text
        if elem != "Choix d'une plage horaire":
            pass
        else:
            compterCreneaux()
            notifierSurDiscord(urlDemarche, urlWebhook, libre, complet, guichet, periodeParsed)
    elif elem == "Choix de la nature du rendez-vous":
        radioParsed = driver.find_elements(By.XPATH, "/html/body/main/div/div/div/div[2]/form/fieldset/p")
        for p in radioParsed:
            nbRadio = nbRadio +1
        print("Il y a " + str(nbRadio) + " guichets.")
        elem = driver.find_element(By.XPATH, "/html/body/main/div/div/div/div[2]/form/fieldset/p[" + str(nbRadio) + "]/input")
        elem.send_keys(Keys.SPACE)
        elem = driver.find_element(By.XPATH, "/html/body/main/div/div/div/div[2]/form/div/input")
        elem.send_keys(Keys.SPACE)
        elem = driver.find_element(By.XPATH, "/html/body/main/div/div/div/div[2]/h2").text
        if elem == "Description de la nature du rendez-vous":
            elem = driver.find_element(By.NAME, "nextButton")
            elem.send_keys(Keys.SPACE)
            compterCreneaux()
            notifierSurDiscord(urlDemarche, urlWebhook, libre, complet, nbRadio, periodeParsed)
        else: print("- Guichet " + str(nbRadio) + " : pas de RDV")
        nbRadio = nbRadio - 1
        while nbRadio != 0:
            driver.get(urlDemarche)
            libre = 0
            complet = 0

            ## Coche le bouton d'acceptation
            elem = driver.find_element(By.NAME, "condition")
            elem.send_keys(Keys.SPACE)

            ## Appuie sur le bouton pour aller à la page suivante
            elem = driver.find_element(By.NAME, "nextButton")
            elem.send_keys(Keys.SPACE)
            elem = driver.find_element(By.XPATH, "/html/body/main/div/div/div/div[2]/form/fieldset/p[" + str(nbRadio) + "]/input")
            elem.send_keys(Keys.SPACE)
            elem = driver.find_element(By.XPATH, "/html/body/main/div/div/div/div[2]/form/div/input")
            elem.send_keys(Keys.SPACE)
            elem = driver.find_element(By.XPATH, "/html/body/main/div/div/div/div[2]/h2").text
            if elem == "Description de la nature du rendez-vous":
                elem = driver.find_element(By.NAME, "nextButton")
                elem.send_keys(Keys.SPACE)
                compterCreneaux()
                notifierSurDiscord(urlDemarche, urlWebhook, libre, complet, nbRadio, periodeParsed)
            else: print("- Guichet " + str(nbRadio) + " : pas de RDV")
            nbRadio = nbRadio - 1
    else:
        print("ça n'a pas fonctionné.\n")

driver.close
jour = date.today().strftime("%y-%m-%d") ###format AA/MM/JJ
heure = datetime.now().strftime("%H:%M") ###format HH:MM
jourEtHeure = str(jour) + " " + str(heure)
print("Terminé à : " + jourEtHeure + "\n")
webhook = DiscordWebhook(url="", content='Prefy terminé !' + ' @ ' + str(jourEtHeure))
response = webhook.execute()
