from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time


def simulate_answer():
    time.sleep(5)
    driver.find_element(By.XPATH, "/html/body/input[1]").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/input[6]").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/input[10]").click()
    time.sleep(1)
    slider = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]")
    ActionChains(driver).click_and_hold(slider).perform()
    i = 0
    distance = 358
    while i <= distance:
        ActionChains(driver).move_by_offset(20, 0).perform()
        i += 20
    ActionChains(driver).release().perform()
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/button").click()
    time.sleep(1)


if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get("file:///D:\\work_github\\robot-mouse-track-recognition\\examples\\collect_data.html")
    driver.get("file:///D:\\work_github\\robot-mouse-track-recognition\\examples\\collect_data_ap.html")

    simulate_answer()
    time.sleep(10)
    driver.close()
