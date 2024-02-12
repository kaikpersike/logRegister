import os
import smtplib
from email.message import EmailMessage 
import sqlite3

endereco_email = '' # email de envio
senha_email = '' # senha do email de envio

os.chdir('13-1 - Logs') # acesso a pasta

# ------------------ INICIO DO PACOTE DE MENSAGEM ------------------
mensagem = "" # mensagem de envio

dic_ocorrencias = dict() # dicionario de ocorrencias dos tipos-log
dic_data = dict() # dicionario de ocorrencias das datas 

lista_ocorrencias = [] # lista de ocorrencia dos tipos-log
lista_data = [] # lista de correncias das datas

arquivos = list(os.listdir(os.getcwd()))
arquivos.sort()

for i in arquivos:
    arq = open(i, "r")
    linhas = arq.readlines() # funcao que lê linhas do arquivo em questao
    
    for i in linhas: # passando linha por linha dentro da funcao que lê linhas
        print(i.strip().split(" ")) # printando ao criar uma lista separada por " "
    
    for i in linhas: # passando linha por linha dentro da funcao que lê linhas
        data = i.split(" ")[0] # selecionando o primeiro elemento da lista, que no caso é a data
        log = i.split(" ")[3] # selecionando o quarto elemetno da lista, que no caso é o tipo-log

        if log not in dic_ocorrencias: # condicao de existencia pra ocorrencias de tipo-log no dicionario: se existir soma +1, senão, é 1
            dic_ocorrencias[log] = 1
        else:
            dic_ocorrencias[log] += 1
        
        if data not in dic_data: # condicao de existencia pra ocorrencias de data tipo-log no dicionario: se existir soma +1, senão, é 1
            dic_data[data] = 1
        else:
            dic_data[data] += 1
        
    print() #quebrando linha

    for k, v in sorted(dic_ocorrencias.items()): # colocando os valores em primeiro, dentro de uma tupla, a ser adicionada numa lista
        lista_ocorrencias.append((v,k))
    
    lista_ocorrencias.sort(reverse=True) # revertendo a ordem, para que com mais ocorrencia fique em primeiro

    for i in lista_ocorrencias:
        mensagem = mensagem + "\n{}: {}".format(i[1], i[0]) # Tipo log e a quantidade de tipo log. Adiconando tudo numa mensagem, criando uma especia de "pacote"

    for k, v in dic_data.items(): # colocando os valores em primeiro, dentro de uma tupla, a ser adicionada numa lista
        lista_data.append((v,k))
    
    lista_data.sort(reverse=True) # revertendo a ordem, para que com mais ocorrencia fique em primeiro

    mensagem = mensagem + "\n" + "\n{}:{}\n".format(lista_data[0][1], lista_data[0][0]) # data e a quantidade de data sendo adicionadas no pacote

    print(mensagem) #mostrando o pacote completo

    """Aqui zera os dicinarios e as listas para receberem novos valores sem interferencia, e, assim, adicionados novamente no pacote de 'mensagem', que já abriga os valores do resultado anterior"""
    dic_ocorrencias = dict()
    dic_data = dict()

    lista_ocorrencias = []

    lista_data = []

arq.close()

# ------------------ INICIO DO ENVIO DE EMAIL ------------------
mensagem_email = EmailMessage() # criando mensagem de email
mensagem_email['Subject'] = 'Atividade de Programacao: Tratamento de Logs' # titulo da mensagem
mensagem_email['From'] = '' # e-mail de origem da mensagem
mensagem_email['To'] = '' # e-mail de destino da mensagem
mensagem_email.set_content(mensagem) # conteudo da mensagem

sending = smtplib.SMTP_SSL('smtp.gmail.com',465) # canal de envio de mensagem
sending.login(endereco_email,senha_email) # login do seu email
sending.send_message(mensagem_email) # envio da mensagem do email

os.chdir('..') # saindo da pasta atual

# ------------------ INICIO DO BANCO DE DADOS ------------------
banco = sqlite3.connect("db_log.db") #conectando ao banco de dados

tabela = banco.cursor()# manipulando banco
tabela.execute("CREATE TABLE tb_log (ds_data text, ds_log, nr_num_log integer)") # criando tabela dentro do banco com as respectivas colunas

contador_data = 0 # contador de quantidade de data limitador, para separar do "pacote de mensagem"
log_data = [] # lista que vai receber as datas com maior ocorrencia, em consonância 

for i in mensagem.split("\n"):
    contador_data += 1
    if i != '' and contador_data%8==0:
        for _ in range(5):
            log_data.append(i)

contador_log = 0 # delimitador de log
contador_data2 = -1 # para selecionar as datas dentro do log data

for i in mensagem.split("\n"):
    contador_log += 1

    if i != '' and contador_log%8!=0:
        contador_data2 += 1
        tabela.execute("INSERT INTO tb_log VALUES ('"+log_data[contador_data2]+"', '"+i[:i.find(":")]+"', '"+i[i.find(":")+2:]+"')") # aqui está ocorrendo a inserção dos valores tratados na tabela

banco.commit()

tabela.execute("SELECT * FROM tb_log") # selecao de tabela com respectivos dados
print("-------------------------------------")
print("|    Data    |   Tipo    |   Qtd    |")
print("-------------------------------------")
for i in tabela.fetchall():
    print("{} | {} | {}".format(i[0],i[1],i[2])) # exibindo dados da tabela...
print("-------------------------------------")