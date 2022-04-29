from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

url = 'https://noveltop1.com/book/dungeon-of-pride-laplace/chronicle'
#url = 'https://noveltop1.com/book/dungeon-of-pride-laplace/chapter-256-fight-against-the-bandits-2'
# inizializzo chrome driver
chrome_driver = ChromeDriverManager().install()
driver = Chrome(service=Service(chrome_driver))

# massimizzo la finestra e apro il sito
driver.maximize_window()
driver.get(url)

next_chapter_id = 'next_chap'
chapter_content_id = 'chr-content'

# seleziono il bottone per procedere al prossimo capitolo
next_chapter_button = driver.find_element(By.ID, next_chapter_id)

before_url = driver.current_url

next_chapter_button.click()

after_url = driver.current_url

if before_url == after_url:
	print('LAST CHAPTER')
	exit()
else:
	print('not last chapter')

chapter_content = driver.find_element(By.ID, chapter_content_id)

print('\n' * 50)
print(chapter_content.text)

input()