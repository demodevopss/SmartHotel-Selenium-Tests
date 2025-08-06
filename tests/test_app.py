import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@pytest.fixture
def driver():
    chrome_options = Options()
    # Headless modu tekrar aktif edelim, testler daha hızlı çalışır.
    # Görsel olarak takip etmek isterseniz bu satırı yorumdan çıkarabilirsiniz.
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(5) # Elementleri bulmak için 5 saniyeye kadar bekle
    yield driver
    driver.quit()

def test_title(driver):
    driver.get("file:///Users/serdarselcuk/Desktop/DevOps/Test/SmartHotel/index.html")
    assert "SmartHotel360" in driver.title

def test_switch_tab(driver):
    driver.get("file:///Users/serdarselcuk/Desktop/DevOps/Test/SmartHotel/index.html")
    repositories_tab = driver.find_element(By.ID, "repositories")
    repositories_tab.click()
    repositories_content = driver.find_element(By.ID, "Repositories")
    assert repositories_content.is_displayed()

def test_all_buttons_are_clickable(driver):
    driver.get("file:///Users/serdarselcuk/Desktop/DevOps/Test/SmartHotel/index.html")
    
    # 1. Tüm sekmeleri bul
    # Not: 'Learn More' sekmesi diğerleriyle aynı class'ı paylaşmıyor gibi görünüyor,
    # bu yüzden onu ayrı bir mantıkla ele alabiliriz veya ID'lerini direkt kullanabiliriz.
    tab_ids = ["architecture", "connect2017", "repositories", "demoScripts"]
    
    for tab_id in tab_ids:
        try:
            # 2. Sırayla her sekmeye tıkla
            tab = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, tab_id))
            )
            tab.click()
            
            # JavaScript'in içeriği yüklemesi için kısa bir bekleme
            time.sleep(0.5)

            # 3. O an görünür olan tüm butonları bul
            buttons = driver.find_elements(By.TAG_NAME, "button")
            
            print(f"Sekme '{tab_id}' altında {len(buttons)} adet buton bulundu.")

            for button in buttons:
                # Sadece görünür olan butonları kontrol et
                if button.is_displayed():
                    # 4. Butonun tıklanabilir olduğunu doğrula
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(button))
                    print(f"  - Buton '{button.text}' tıklanabilir.")
                    assert button.is_enabled()

        except Exception as e:
            pytest.fail(f"Sekme '{tab_id}' işlenirken hata oluştu: {e}")