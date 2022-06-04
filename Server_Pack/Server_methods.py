import sys
import  random
class Server:

    def send_request_to_client(self,request ,socket):
        """Send the request to the server. First the length of the request (2 digits), then the request itself
        Example: '04EXIT'
        Example: '12DIR c:\cyber'
        """

        length = str(len(request.encode('utf-8')))
        zfill_length = length.zfill(2)
        message = zfill_length + request

        socket.send(message.encode('utf-8'))

    def who_paints(self,client_sockets):
        rand=random.randint(0,len(client_sockets)-1)
        paint=client_sockets[rand]
        return paint

    def recive_request_from_client(self,current_socket):
        length = current_socket.recv(2).decode()
        data = current_socket.recv(int(length)).decode()
        return data

    def paints_now(self,paint,unPainted_list,client_sockets):
        unPainted_list.remove(paint)
        for i in client_sockets:
            if (i != paint):
                self.send_request_to_client('Not painter', i)
        self.send_request_to_client('Painter', paint)

    def chosen_words(self,paintedwords):
        rand1 = random.randint(1, 30)
        rand2 = random.randint(1, 30)
        if rand2==rand1:
            if rand2==29:
                rand2-=1
            elif rand2==0:
                rand2+=1
            else:
                rand2+=1
        for i in paintedwords:
            if (i[1] == rand1):
                word1 = i[0]
            if (i[1] == rand2):
                word2 = i[0]
        return word1, word2

    def check_infor(self,informs,fernet,inf,current_socket,maxPlayers,rigtNow):
        informs = informs.split(' ')
        result = self.getFromDB(inf, fernet, informs)
        if result:
            self.send_request_to_client('suitability '+str(maxPlayers)+' '+str(rigtNow), current_socket)
            print(444)
            return True
        else:
            self.send_request_to_client('unsuitability', current_socket)
            return False

    def getFromDB(self,inf,fernet,informs):
        #mycursor.execute("SELECT * FROM PlayerInfor")
        for x in inf:
            if fernet.decrypt(x[1].encode()).decode()==informs[1] and informs[0]==x[0]:
                return x
        return None

    def removeSocket(self,client_sockets,socket,pw_lst,unpaintLst,max_clients,guess_players):
        if socket in unpaintLst:
            unpaintLst.remove(socket)
            print('yoa')
        for i in pw_lst:
            if i[0]==socket:
                pw_lst.remove(i)
                if len(client_sockets) == 0:
                    sys.exit()
                max_clients-=1
                guess_players-=1
                self.minus(pw_lst)

        return pw_lst,unpaintLst,max_clients,guess_players

    def minus(self,pw_lst):
        for i in pw_lst:
            self.send_request_to_client('minus',i[0])