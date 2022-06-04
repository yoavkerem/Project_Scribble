import time
import socket
from Server_Pack import Server_methods
from cryptography.fernet import Fernet
import mysql.connector
import smtplib
import select
import requests

def main():
    s=Server_methods.Server()
    with open('datas.txt', 'r') as f:
        data_list = []
        for line in f:
            print(line)
            data_list.append(line.split(' ')[1][:-1])

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER_PORT = int(data_list[1])
    SERVER_IP = "0.0.0.0"
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()
    client_sockets = []

    unPainted_list=[]
    countTimeOver=0
    numClients=0
    maxClients=int(data_list[2])

    EMAIL_ADDRESS = "yoavker@hadarim.edum.org.il"
    EMAIL_PASSWORD = "yoavkay25"

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    subject = "Registered successfully to DRAWIO"
    body = "You have successfully logged in to DRAWIO game, welcome!!"
    msg = f'Subject: {subject}\n\n{body}'

    print("Server is up and running")
    mydb = mysql.connector.connect(host="localhost", user="Yoav Kerem", password="yoavkay25", database="wordsdb")
    mycursor = mydb.cursor()
    paintedWords = []
    guess_players=maxClients-1
    guess_points=maxClients-1
    paint=0
    guessWord=''
    pw_list=[]
    left=False

    mycursor.execute("SELECT * FROM PaintedWords")
    for x in mycursor:
        paintedWords.append(x)
    word1, word2 = s.chosen_words(paintedWords)
    inf=[]
    mycursor.execute("SELECT * FROM PlayerInfor")
    for x in mycursor:
        inf.append(x)

    # 2gsTN-tzEllR1IdyV4KxCpdhi_qh2kCW5DDrUMSTZtk=
    key = '2gsTN-tzEllR1IdyV4KxCpdhi_qh2kCW5DDrUMSTZtk='.encode()
    # Instance the Fernet class with the key
    fernet = Fernet(key)

    full=False

    while True:
        rlist, wlist, xlist = select.select([server_socket] + client_sockets, [], [])
        for current_socket in rlist:
            if current_socket is server_socket:
                connection, client_address = current_socket.accept()
                print("New client joined!", client_address)
                client_sockets.append(connection)
            else:
                try:
                    data=s.recive_request_from_client(current_socket)
                except:
                    data=''
                if data == "":
                    print("Connection closed", )
                    client_sockets.remove(current_socket)
                    pw_list, unPainted_list, maxClients, guess_players = s.removeSocket(client_sockets, current_socket,
                                                                                        pw_list, unPainted_list,
                                                                                        maxClients, guess_players)
                    current_socket.close()
                elif data[0]=='L':
                    informs = data[1:]
                    if full==True:
                        s.send_request_to_client('full',current_socket)
                        client_sockets.remove(current_socket)
                    else:
                        success=s.check_infor(informs,fernet,inf,current_socket,maxClients,numClients)
                        if success:
                            informs = informs.split(' ')
                            pw_list.append((current_socket,informs[0],informs[1],0))
                elif data[0]=='S':
                    informs = data[1:]
                    informs=informs.split(' ')
                    if informs[0]=='' or informs[1]=='':
                        s.send_request_to_client("empty",current_socket)
                    else:
                        result = s.getFromDB(inf, fernet,informs )
                        if result==None:
                            informs = data[1:]

                            informs = informs.split(' ')
                            print(informs[2])

                            response = requests.get("https://isitarealemail.com/api/email/validate",
                                                    params={'email': informs[2]})
                            status = response.json()['status']
                            if status == "valid":
                                print(7)
                                #smtp.sendmail(EMAIL_ADDRESS, informs[2], msg)
                                cryptPw = fernet.encrypt(informs[1].encode())
                                mycursor.execute(
                                    "insert into PlayerInfor values ('" + informs[0] + "','" + cryptPw.decode() + "','" +
                                    informs[2] + "',0,0,0)")
                                mydb.commit()
                                inf.append((informs[0],cryptPw.decode(),informs[2]))

                                s.send_request_to_client("valid", current_socket)
                            else:
                                s.send_request_to_client("not valid", current_socket)

                elif data=="logged in":
                    for i in pw_list:
                        s.send_request_to_client("plus",i[0])
                    numClients+=1

                elif data[0]=='w':
                    guessWord=data[1:]
                    for i in client_sockets:
                        if i!=paint:
                            s.send_request_to_client("starTime",i)
                elif data.split(' ')[0]=='end':
                    print(1)
                    data=data.split(' ')


                    for i in range(len(pw_list)):
                        if current_socket==pw_list[i][0]:
                            x=list(pw_list[i])
                            x[3]=int(data[1])
                            pw_list[i]=tuple(x)

                            result = s.getFromDB(inf, fernet, [pw_list[i][1],pw_list[i][2]])
                            games = result[5]
                            sql = "UPDATE PlayerInfor SET games = %s WHERE password = %s"
                            val = (games + 1, result[1])
                            mycursor.execute(sql, val)
                            mydb.commit()

                    countTimeOver += 1

                    if countTimeOver==maxClients:
                        max = pw_list[0]
                        for i in pw_list:
                            if int(i[3]) > int(max[3]):
                                max = i

                        result = s.getFromDB(inf, fernet, [max[1],max[2]])
                        wins = result[4]
                        sql = "UPDATE PlayerInfor SET wins = %s WHERE password = %s"
                        val = (wins + 1, result[1])
                        mycursor.execute(sql, val)
                        mydb.commit()

                        for j in client_sockets:
                            for i in pw_list:
                                print(i)
                                result = s.getFromDB(inf, fernet, [i[1],i[2]])
                                print(result)
                                s.send_request_to_client(result[0]+' '+str(i[3]),j)
                        for i in pw_list:
                            result = s.getFromDB(inf, fernet, [i[1],i[2]])
                            s.send_request_to_client(str(result[3])+' '+str(result[4])+' '+str(result[5]),i[0])
                elif data=="clear":
                    for i in client_sockets:
                        if i!=paint:
                            s.send_request_to_client("clear",i)
                elif data=="Time over":
                    countTimeOver+=1
                    if countTimeOver==maxClients:
                        guess_points = maxClients-1
                        countTimeOver=0
                        guess_players = len(client_sockets) - 1
                        paint = s.who_paints(unPainted_list)
                        s.paints_now(paint,unPainted_list,client_sockets)
                        word1, word2 = s.chosen_words(paintedWords)
                        s.send_request_to_client(word1 + '&' + word2, paint)
                else:
                    if current_socket == paint:
                        for i in client_sockets:
                            if i!=paint:
                                s.send_request_to_client(data,i)

                    else:
                        if data == guessWord:
                            for i in pw_list:
                                if i[0]==current_socket:
                                    result = s.getFromDB(inf, fernet, [i[1],i[2]])
                            new_pts=result[3]+guess_points
                            sql = "UPDATE PlayerInfor SET points = %s WHERE password = %s"
                            val = (new_pts, result[1])
                            mycursor.execute(sql, val)
                            mydb.commit()

                            guess_players -= 1
                            s.send_request_to_client('true ' + str(guess_points), current_socket)
                            guess_points -= 1
                            if guess_players == 0:
                                for i in client_sockets:
                                    s.send_request_to_client("done", i)
                                guess_players = maxClients-1
                        else:
                            s.send_request_to_client("wrong", current_socket)
                if numClients==maxClients:
                    full=True
                    numClients = 0
                    time.sleep(1)
                    for i in client_sockets:
                        s.send_request_to_client("start ",i)
                    guess_players= maxClients-1

                    paint=s.who_paints(client_sockets)
                    for i in client_sockets:
                        if i!=paint:
                            s.send_request_to_client('Not painter',i)
                            unPainted_list.append(i)


                    s.send_request_to_client('Painter',paint)
                    s.send_request_to_client(word1 + '&' + word2, paint)
