import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# 1 målet
# Öppna en webläsare som vi har kontroll över och gå till www.chalmers.se



# Några problem med testfunktioner skrivna så här.
# 1. Hårdkodad data i testfunktionen. Exempelvis hur vi hittar olika element. Om systemet vi testar förändras måste vi manuellt rätta varje test
# 2. Setup av webläsare och upplösning inne i testfunktionen. Vill vi testa på flera webläsare och upplösnignar får vi skapa fler testfunktioner med dubblering av kod som följd
def test_nav_it():
    browser = webdriver.Edge() # Starta en webläsare och ge mig en referens till den så att jag kan styra den
    browser.set_window_size(1920, 1080)
    browser.get("https://www.chalmers.se") # Navigera till chalmers.se
    browser.find_element(By.LINK_TEXT, "Utbildning").click() # hitta länk baserat på länktext och klicka på
    browser.find_element(By.LINK_TEXT, "Program på grundnivå").click()
    browser.find_element(By.LINK_TEXT, "Elektro, Data, IT och Medicinteknik").click()
    browser.find_element(By.CSS_SELECTOR, ".orange li:nth-child(5) .title").click()


def test_nav_data_civ():
    browser = webdriver.Edge() # Starta en webläsare och ge mig en referens till den så att jag kan styra den
    browser.set_window_size(1920, 1080)
    browser.get("https://www.chalmers.se") # Navigera till chalmers.se
    browser.find_element(By.LINK_TEXT, "Utbildning").click() # hitta länk baserat på länktext och klicka på
    browser.find_element(By.LINK_TEXT, "Program på grundnivå").click()
    browser.find_element(By.LINK_TEXT, "Elektro, Data, IT och Medicinteknik").click()
    browser.find_element(By.CSS_SELECTOR, ".orange li:nth-child(1) .title").click()