#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from datetime import datetime
from time import sleep

# boxe
adresse = "https://wo.unistra.fr/app/WebObjects/SUAPSWeb.woa/wa/afficherDetails?ongletSelectionne=Cours&activite=10.0&sousOngletSelectionne=Horaires"
# natation
#adresse = "https://wo.unistra.fr/app/WebObjects/SUAPSWeb.woa/wa/afficherDetails?ongletSelectionne=Cours&activite=45.0&sousOngletSelectionne=Horaires"

#identifiants ernest
username = "martic"
password = "Subotica_15!"
#liste des jours désirés en majuscule
desired_days = ["MERCREDI", "VENDREDI"]

verbose = False

def connection(driver):
    driver.find_element_by_class_name("btIdentifier").click()
    select = Select(driver.find_element_by_id("etab"))
    select.select_by_value("UDS") #UDS = Univ De Strasbourg
    driver.find_element_by_name("inscriptionEtablissement").click()
    username_s = driver.find_element_by_id("username")
    password_s = driver.find_element_by_id("password")
    username_s.send_keys(username)
    password_s.send_keys(password)
    driver.find_element_by_id("login-btn").click()

matched = False
while(not matched):
    options = Options()
#    options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=options)
    driver.get(adresse)
    connection(driver)
    driver.get(adresse)
    current_time = datetime.now().strftime("%H:%M:%S")
    print("Executed@" + current_time)
    try:
        for el in driver.find_elements_by_xpath("//div[contains(@class, 'listeCreneaux')]"):
            if(el.find_elements_by_class_name("ajouterPanier") == []):
                jour_training = str(el.find_element_by_class_name("jour").text)
                horaires_training = str(el.find_element_by_class_name("horaires").text)
                if(verbose):
                    print('Créneau du ' + jour_training + ' à ' + horaires_training)

                if(jour_training in desired_days):
                    el.find_element_by_tag_name("input").click()
                    if(verbose):
                        print("  IT'S A MATCH")
                    matched = True
                places_restantes = int(el.find_element_by_class_name("placesDispo").text[:2])
                print("  => {} places dispo".format(places_restantes))
    except NoSuchElementException:
        pass
    if(matched):
        el.find_element_by_class_name("btAjouterPanier").click()

        try:
            driver.find_element_by_id("certif").click()

            driver.find_element_by_class_name("btValiderPanier").click()
            print("Séance(s) validée(s)")
        except NoSuchElementException:
            pass
    else:
        print("Aucune séance ne correspond")
    sleep(60)
    driver.quit()

print("bye byee")
