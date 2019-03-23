from table import Table
from player import Player

class Environment():
    def __init__(self, data):
        self.round = data["round"]
        self.playerName = data["playerName"]
        table = data["table"]
        players = data["players"]
        self.table = Table(table)

        assert len(players) == 3, "Number of Players should be %d, not %d!" % (int(3), len(players))

        for player in players:
            if player["name"] == self.playerName:
                self.player1 = Player(player)
            else:
                if not hasattr(self, 'player2'):
                    self.player2 = Player(player)
                else:
                    self.player3 = Player(player)
        if hasattr(self, 'player1') is None:
            print("Player: %s, not in players!" % self.playerName)
            exit()