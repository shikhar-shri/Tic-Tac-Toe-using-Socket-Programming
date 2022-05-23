import socket

HOST_IP=socket.gethostbyname(socket.gethostname())
HOST_PORT=5050


class TicTacToe():

    def __init__(self) -> None:
        self.board = [[" "," "," "],[" "," "," "],[" "," "," "]]
        self.turn="X"
        self.you="X"
        self.opponent="O"
        self.winner= None
        self.gameOver= False
        self.counter=0
    
    def host_game(self,host,port):
        server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind((host,port))
        server.listen(1)

        client,addr=server.accept()

        self.you="X" #the client that hosts the game is "X"
        self.opponent="O" #opponent is given "O"
        self.handle_conn(client)
        server.close() #close the server socket
    
    def connect_to_game(self,host,port):
        client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect((host,port))

        self.you="O" #the client that connects to the game host is "O"
        self.opponent="X"
        self.handle_conn(client)
        

    def handle_conn(self,client):
        while not self.gameOver:  # run the loop while the game is not over
            if self.turn == self.you:  #if current turn is yours
                move=input("Enter your move(row,column): ")
                if self.is_valid_move(move.split(',')):        #checking if the move is valid and can be taken
                    client.send(move.encode('utf-8'))
                    self.take_move(move.split(','),self.you)   #take the move with your symbol 'X' or 'O'
                    self.turn=self.opponent
                else:
                    print("Invalid Move!!")
                    exit()
            else:
                data=client.recv(1024)
                if not data:
                    break
                else:
                    self.take_move(data.decode('utf-8').split(','),self.opponent)
                    self.turn=self.you

        client.close()


    def take_move(self,move,symbol):
        if self.gameOver:
            return
        
        self.counter+=1
        self.board[int(move[0])][int(move[1])]=symbol
        self.print_board()
        if self.check_if_Won():
            if self.winner==self.you:
                print("You Win!")
                exit()
            elif self.winner==self.opponent:
                print("You Lose!")
                exit()
        else:
            if self.counter==9:
                print("TIE!")
                exit()

    def is_valid_move(self,move):
        return self.board[int(move[0])][int(move[1])]==" " and (int(move[0])>=0 and int(move[0])<=2) and (int(move[1])>=0 and int(move[1])<=2)
 
    def check_if_Won(self):

        for row in range(3):
            if self.board[row][0]==self.board[row][1]==self.board[row][2]!=" ":
                self.winner=self.board[row][0]
                self.gameOver=True
                return True
        
        for col in range(3):
            if self.board[0][col]==self.board[1][col]==self.board[2][col]!=" ":
                self.winner=self.board[0][col]
                self.gameOver=True
                return True
        
        if self.board[0][0]==self.board[1][1]==self.board[2][2]!=" ":
            self.winner=self.board[0][0]
            self.gameOver=True
            return True
        
        if self.board[0][2]==self.board[1][1]==self.board[2][0]!=" ":
            self.winner=self.board[0][2]
            self.gameOver=True
            return True
        
        return False
    
    def print_board(self):
        print()
        for row in range(3):
            print(" | ".join(self.board[row]))
            if(row!=2):
                print("----------")


game=TicTacToe()
game.host_game(HOST_IP,HOST_PORT) #hosting the game from our machine on port 5050