from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.edge.options import Options
import pyperclip
import random
import string
import time


def start_driver(url):
	edge_options = Options()
	edge_options.add_extension('ublock.crx')
	edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.ChromiumEdge(options=edge_options)
	driver.set_window_size(1920, 1080)
	driver.minimize_window()
	driver.implicitly_wait(10)
	driver.get(url)
	return driver


def generate_creds():
	print("Gerando credenciais...")
	global mail_website, mail, password
	mail_website = start_driver("https://10minutemail.net/?lang=pt-br") 
	time.sleep(5)
	try:
		mail_website.find_element(By.ID, "copy-button").click() #Botão de copiar endereço de email
	except:
		print("Não foi possível gerar um email temporário. O site está offline ou seu IP sofreu um softban.")
		exit()
	else:
		pass
	mail = pyperclip.paste()
	password = ''.join(random.choice(string.ascii_letters) for i in range(10))
	create_AliAcc(mail, password)
	return mail_website


def create_AliAcc(mail, password):
	print("Criando conta AliExpress...")
	aliexpress = start_driver("https://login.aliexpress.com")
	aliexpress.find_element(By.CLASS_NAME, "comet-tabs-nav-item").click() #Botão de registrar
	aliexpress.find_element(
		By.XPATH, "/html/body/div[2]/div/div/div[1]/div[2]/div[1]/div/div/div[3]/span/span[1]/input").send_keys(mail) #Caixa de texto pro email
	aliexpress.find_element(
		By.XPATH, "/html/body/div[2]/div/div/div[1]/div[2]/div[1]/div/div/div[4]/div/span/span[1]/input").send_keys(password) #Caixa de texto pra senha
	print("Aguardando verificação de captcha...")
	time.sleep(5)
	captcha = aliexpress.find_element(By.ID, 'baxia-join-check-code') #Captcha
	action_chains = ActionChains(aliexpress)
	for x in range(10):
		action_chains.move_to_element_with_offset(
			captcha, -160, 0).click_and_hold().move_by_offset(x*50, 0).release().perform()
	time.sleep(5)
	try:
		aliexpress.find_element(By.CLASS_NAME, "error-text") #Mensagem do captcha
	except:
		aliexpress.find_element(
			By.XPATH, "/html/body/div[2]/div/div/div[1]/div[2]/div[1]/div/div/button").click() #Botão criar conta
	else:
		print("Falha ao resolver captcha. Possível softban de IP.")
		exit()

	print("Captcha resolvido com sucesso.")

	got_mail = False

	print("Aguardando email de verificação...")

	while got_mail == False:
		try:
			mail_website.find_element(
				By.XPATH, "/html/body/div[1]/div[4]/div/table/tbody/tr[3]") #Primeiro email da lista
		except:
			time.sleep(10)
			mail_website.find_element(
				By.XPATH, "/html/body/div[1]/div[3]/div[5]/ul/li[1]/a").click() #Botão atualizar página
		else:
			mail_website.find_element(By.CLASS_NAME, "row-link").click()
			get_code = mail_website.find_element(
				By.XPATH, "/html/body/div[1]/div[4]/div/div/div[4]/div[1]/div[2]/div[1]/table/tbody/tr/td/div[3]/table/tbody/tr/td/div/table/tbody/tr/td/div/div/div[4]").text #Código aliexpress
			got_mail = True

	code = [char for char in get_code]

	#Caixas para inserir os dígitos do código aliexpress
	aliexpress.find_element(
		By.XPATH, "/html/body/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/input[1]").send_keys(code[0]) 
	aliexpress.find_element(
		By.XPATH, "/html/body/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/input[2]").send_keys(code[1])
	aliexpress.find_element(
		By.XPATH, "/html/body/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/input[3]").send_keys(code[2])
	aliexpress.find_element(
		By.XPATH, "/html/body/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/input[4]").send_keys(code[3])
	aliexpress.find_element(
		By.XPATH, "/html/body/div[2]/div/div/div/div[2]/div[1]/div/div/button").click()
	time.sleep(2)
	pyperclip.copy("{mail}:{password}".format(mail=mail, password=password))
	print("Conta criada com sucesso. As credênciais estão no seu CTRL-C.\n\nEmail: {mail} \nSenha: {senha}".format(
		mail=mail, senha=password))
	time.sleep(2)
	save_account(mail, password)


def save_account(mail, password):

	f = open("contas.txt", "a")
	f.write("{mail}:{password}\n".format(mail=mail, password=password))
	f.close()
	print("As credênciais acima foram salvas no arquivo contas.txt.")


generate_creds()
