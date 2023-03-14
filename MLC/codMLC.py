import requests
from bs4 import BeautifulSoup
import re
import sqlite3 as sql
from os import system as cmd, name as osname
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

db = sql.connect('database.db')
cur = db.cursor()



cur.execute('CREATE TABLE IF NOT EXISTS accounts(login, password, server, summoner, info)')

servers = ['br', 'na', 'euw', 'oce', 'kr', 'jp', 'las', 'lan', 'ru', 'tr', 'sg', 'ph', 'tw', 'vn', 'th', 'eune']


def clearScreen():
    cmd('cls' if osname == 'nt' else 'clear')


def menu():
    clearScreen()
    print('Lol Account Manager!')
    print('Created by Oblivion- github.com/Devilicht')
    print('and Gabriel -github.com/bielviana\n')
    global op
    op = input('1- Vizualizar suas contas. 2-Adicionar uma nova conta 3-Remover alguma conta. 0 - Sair: ')
    print('')
    if op == '1':
        listAccounts()
    elif op == '2':
        addAccount()
    elif op == '3':
        deleteAccount()
    elif op == '0':
        exit()
    else:
        print('\nOpção inválida, tente novamente!')
        sleep(1.5)
        menu()


def updateStats(server, summoner):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f'https://www.op.gg/summoners/{server}/{summoner}')
    button = driver.find_element(by=By.CLASS_NAME, value='css-4e9tnt')
    button.click()
    driver.close()


def getSummoner(server, summoner):
    # updateStats(server, summoner)
    userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0'
    headers = {'User-Agent': userAgent}
    padrao = r">(.*?)<"
    response = requests.get(f'https://www.op.gg/summoners/{server}/{summoner}', headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    vr = re.findall(padrao, str((soup.find('h2', {'class': 'header__title'}))))
    eloa = re.findall(padrao, str((soup.find('div', {'class': 'tier'}))))
    pdla = re.findall(padrao, str(soup.find('div', {'class': 'lp'})))
    winRatea = re.findall(padrao, str(soup.find('div', {'class': 'ratio'})))
    WLa = re.findall(padrao, str(soup.find('div', {'class': 'win-lose'})))

    separador = " "
    elo = separador.join(eloa)
    pdl = separador.join(pdla)
    winRate = separador.join(winRatea)
    wL = separador.join(WLa)

    elo = " ".join(elo.split())
    pdl = " ".join(pdl.split())
    winRate = " ".join(winRate.split())
    wL = " ".join(wL.split())

    if vr == []:
        if eloa == []:
            pp = (f'a conta {summoner} está sem elo').lower()
        else:
            pp = (f'a conta {summoner} está {elo}-{pdl} e com {wL} {winRate}').lower()
    else:
        pp = None

    return pp


def checkAccount(summoner='', type=''):
    if type == 'fetchone':
        result = cur.execute('SELECT * FROM accounts WHERE summoner=?', (summoner,))
        return result.fetchone()
    elif type == 'fetchall':
        result = cur.execute('SELECT * FROM accounts')
        return result.fetchall()


def listAccounts():
    accounts = checkAccount(type='fetchall')
    i = 1
    for account in accounts:
        info = getSummoner(account[2], account[3])
        cur.execute('UPDATE accounts SET info=?', (info,))
        print(f'[CONTA #{i}]')
        print(f'Login: {account[0]}')
        print(f'Senha: {account[1]}')
        print(f'Server: {account[2]}')
        print(f'Nick: {account[3]}')
        print(f'Info: {info}')
        print('\n')
        i += 1
    input('Pressione uma tecla para voltar ao menu anterior...')


def addAccount():
    clearScreen()
    global servers
    login = input('Login: ').lower()
    password = input('Senha: ').lower()
    server = input('Server: ').lower()
    while server not in servers:
        print('Server inválido!')
        sleep(1.5)
        clearScreen()
        print(f'Login: {login}')
        print(f'Senha: {password}')
        server = input('Server: ').lower()
    summoner = input('Nick: ').lower()[:16]
    info = getSummoner(server, summoner)
    if info == None:
        print(f'O invocador {summoner} não existe!')
    else:
        cur.execute(
            'INSERT INTO accounts (login, password, server, summoner, info) VALUES (?,?,?,?,?)', (login, password, server, summoner, info)
        )
        db.commit()
        print(f'\n Conta {summoner} adicionada com sucesso!')
    sleep(1.5)


def deleteAccount():
    clearScreen()
    summoner = input('Nick da conta a ser removida: ').lower()
    if checkAccount(summoner=summoner, type='fetchone') != None:
        cur.execute('DELETE FROM accounts WHERE summoner=?', (summoner,))
        db.commit()
        print(f'\n Conta {summoner} removida com sucesso!')
    else:
        print(f'Conta "{summoner}" não encontrada!')
    sleep(1.5)


while True:
    menu()


