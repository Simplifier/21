import threading

class Game():

    def __init__(self, player, passw):
        self.admin = player
        self.passw = passw
        self.players = [player]
        self.state = False
        self.reqests = []
        self.round = 0
        self.round_state = False


    def add_player(self, player):
        self.players.append(player)


    def in_game(self):
        return [player for player in self.players if player.state]

    def send(self, message):
        for player in self.players:
            player.send(message)

    def update(self):
        for player in self.players:
            player.update()

        if len(self.in_game())==0:
            self.state = False



    def request(self):
        self.reqests = self.in_game()
        print( "[SYSTEM]" ,self.reqests)

        for player in self.reqests:
            requestT = threading.Thread(target=player.request, args=())
            requestT.start()


    def answer(self, player):
        print("Cutch answer from", player.name)
        self.reqests.remove(player)
        print("[SYSTEM UPDATE]", self.reqests)
        for _ in self.in_game():
            _.send(str(player.name)+" made a choice")

    def show_state(self):
        for p in self.players:
            self.send(str(p.name)+' : '+ str(p.points))
            print(str(p.name)+' : '+ str(p.points))

    def start_round(self):

        self.round_state = True
        self.round +=1
        self.send("ROUND " + str(self.round))
        print("ROUND " + str(self.round))
        self.request()
        while self.round_state:
            #print(len(self.reqests))
            #print(self.reqests)
            if len(self.reqests)==0:
                self.round_state = False

        self.update()








    #timer = datetime.datetime.now().timestamp()

    #print(datetime.datetime.now().timestamp() - timer)










