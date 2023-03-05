import random
import os
from os import name, system
import time

invervalo = 2
arq1 = 'escola.txt'
arq2 = 'fruit.txt'
arq3 = 'animals.txt'

#  função para limpar tela
def limpartela():

    # Windows
    if name == 'nt':
        _ = system('cls')
    # Mac ou Linux    
    else:
        _ = system('clear')



def game():
    limpartela()



    while True:
        try:
            changtype = int(input(
                'Bem-Vindo ao jogo da Forca, fofos e fofas.\nEscolha a categoria da palavra\n1- Escola de samba / 2- Fruta / 3- Animais: '))

            if changtype == 1:
                caminho = os.path.join(arq1)
                openTxt = open(caminho, 'r')
                palavra = openTxt.read()
                break
            elif changtype == 2:
                caminho = os.path.join(arq2)
                openTxt = open(caminho, 'r')
                palavra = openTxt.read()
                break
            elif changtype == 3:
                caminho = os.path.join(arq3)
                openTxt = open(caminho, 'r')
                palavra = openTxt.read()
                break
            else:
                print('Categoria inválida. Digite um número inteiro de 1 a 3.\n')
                time.sleep(invervalo)
                limpartela()

        except ValueError:
            print('Categoria inválida. Digite um número inteiro de 1 a 3.\n')
            time.sleep(invervalo)
            limpartela()

    conteudo = palavra.split(',')
    randomWord = random.choice(conteudo).lower()
    letraDescoberta = ['_' for letra in randomWord]
    chances = len(randomWord)
    adiv = int(40/100 * len(randomWord))
    letrasErradas = []

    while chances > 0:
        if changtype == 1 :
            escolha = 'Escola de samba.'
        elif changtype == 2 :
            escolha = 'fruta.'
        elif changtype == 3 :
            escolha = 'animais.'
        
        print('\nCategoria: {}'.format(escolha))
        
        keyLetraDesc = "" "".join(letraDescoberta)
        print(keyLetraDesc)
        print('\nChances restantes :', chances)
        print('letras erradas :', "" "".join(letrasErradas))
        volum = keyLetraDesc.count('_')
        if volum <= adiv:
                decision = ''
                while decision != 'n' or decision != 's':
                        decision = input('\nQuer tentar adivinhar a palavra (s/n): ')
                        if decision == 's' :
                            chute =input('Por favor,digite a palavra: ') 
                            if chute == randomWord :
                                limpartela()
                                print('Categoria {}'.format(escolha))
                                print('\nVocê venceu, a palavra era:', randomWord)
                                exit()
                            else:
                                print('\nVoce errou, a palavra era ',randomWord,'.')    
                                exit()     
                        elif decision == 'n':
                            break 
                    
                        else :
                            print('Digite uma opção valida...') 
                                    
        
        try:
            tentativa = input("\nDigite uma letra: ").lower()
            if tentativa.isalpha():
                if tentativa in randomWord:
                    index = 0
                    for letra in randomWord:
                        if tentativa == letra:
                            letraDescoberta[index] = letra
                            limpartela()
                        index += 1

                else:
                    chances -= 1
                    letrasErradas.append(tentativa)
                    limpartela()

            else:
                print('Por favor, digite apenas letras.')
                time.sleep(invervalo)
                limpartela()
        except TypeError:
            print('Por favor, digite apenas letras.')
            time.sleep(invervalo)
        if "_" not in letraDescoberta:
            print('Categoria {}'.format(escolha))
            print("" "".join(letraDescoberta))
            print('\nVocê venceu, a palavra era:', randomWord)
            break

        else:
            if chances == 0:
                print('\nVocê perdeu,a palavra era:', randomWord)



if __name__ == "__main__":
    game()