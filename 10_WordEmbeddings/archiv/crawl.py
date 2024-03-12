from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

from tqdm import tqdm

# URL der Curia Vista-Seite


# Initialisiere den WebDriver (verwende Chrome oder Firefox)
driver = webdriver.Edge(
    r"C:\Users\lukas\Downloads\msedgedriver.exe")  # Du kannst auch Firefox verwenden: webdriver.Firefox()

# Gehe zur Seite

seen = set()
# Extrahiere die URLs von allen Seiten (von 1 bis 73971)
with open('../urls.txt', 'w') as f:
    for page_number in tqdm(range(0, int(73972/10)), desc='Scraping', total=int(73972/10)):
        i = page_number*10+1
        url = f"https://www.parlament.ch/de/ratsbetrieb/suche-curia-vista#k=#l=1033#s={i}"
        driver.refresh()
        wait = WebDriverWait(driver, 10)
        driver.get(url)  # Warte auf das Laden der Ergebnisse
        result_container = wait.until(EC.presence_of_element_located((By.ID, "Result")))

        # Extrahiere die URLs
        links = result_container.find_elements(By.TAG_NAME, "a")
        for link in links:
            try:
                href = link.get_attribute("href")
                if href and href not in seen and "javascript:void" not in href:
                    f.write(f"{href}\n")
                    seen.add(href)
            except StaleElementReferenceException:
                print(f"StaleElementReferenceException for {link}")
                pass

        # Navigiere zur nächsten Seite (falls vorhanden)
        """
        next_page_button = driver.find_element(By.LINK_TEXT, "Weiter")
        if driver.current_url == "https://www.parlament.ch/de/ratsbetrieb/suche-curia-vista#k=#s=73971":
            break
        next_page_button.click()
        """

driver.quit()


