from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
import time
from tkinter import *

driver = webdriver.Firefox()
driver.get('https://www.chess.com/play/computer')

# Define the button click action
def button_click():
    # Perform some action when the button is clicked
    downloadBtn = driver.find_elements(By.XPATH, '//button[@class="small-controls-btn"]')
    print(downloadBtn)
    downloadBtn[1].click()
    print('Button clicked!')
    


if __name__ == "__main__":
    # Create the GUI window
    root = Tk()
    root.title('Selenium WebDriver GUI')

    # Create the webdriver and open a webpage


    # Create the button
    button = Button(root, text='Click me', command=button_click)
    button.pack()

    # Start the GUI event loop
    root.mainloop()


# time.sleep(10)
# while True :
#     input()  
#     print("Refreshing")
#     refresh = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.ID, 'aim-random-btn')))
#     refresh.click()

#     time.sleep(5)
    
#     print("Saving")
#     saveMeme = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="aim-preview-wrap"]/button[1]')))
#     saveMeme.click()

#   #  input()
#     time.sleep(5)

#     linkElem = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="done-share"]/div[1]')))
#     link = linkElem.get_attribute("data-url")
#     print(link)

    
#     returnButton = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="done-btns"]/button[1]')))
#     returnButton.click()

# driver.close()