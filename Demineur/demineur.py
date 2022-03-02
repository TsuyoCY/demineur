import random
import os


class Game(object):
    # Permet de gérer la partie
    def __init__(self):
        self.TheBoardGame = BoardGame()
        self.GameDuring = True
        while self.Play() == True:
            self.Play()
            self.TheBoardGame.CreateGrille()
        else:
            print("\nAlors, tu as perdu !! Dommage ! \n>")
            regame = input(
                "\nTu veux retenter ta chance quand même ? <o> = oui et <n> = Non. Fait bien ton choix...\n>"
            )
            if regame.upper() == "O":
                self.GameDuring == True
                self.__init__()
                os.system("CLS")
            if regame.upper() == "N":
                self.GameDuring == False

    def Rules(self):
        print("\n")
        print(
            """Le but du jeu du démineur est de trouver toutes les mines présentes sur le terrain.
Le terrain est chiffré, et chaque chiffre indique le nombre de bombes présentes dans les huit cases qui l'entoure:
Pour choisir une case, il faut d'abord rentrer la <lines> puis la <colonne> sous forme de chiffres, allant de 0 à 4.
Tout chiffre supérieur ou inférieur à ce nombre, ne sera pas accepté, de même si c'est autre qu'un chiffre.
Si vous creusez 2 fois la même case, c'est perdu alors soyez vigilant ^^
Si vous creusez sur une bombe, BOOOOOOOM!! Vous êtes mort. 

               Bon Jeu et bonne chance et surtout amusez-vous bien ^^ !."""
        )

        input("\n\nAppuyez sur ENTREE pour commencer:>")
        os.system("CLS")

    def Play(self):
        if self.GameDuring == True:
            self.Rules()
            bombe = input(
                "\n Il faut choisir le nombre de bombes à placer entre 2 et 5. Seras-tu assez courageux pour en mettre 5 ? : "
            )
        while self.GameDuring == True:
            self.TheBoardGame.CreateGrille()
            if bombe == "2":
                self.TheBoardGame.TwoBombs()
            elif bombe == "3":
                self.TheBoardGame.ThreeBombs()
            elif bombe == "4":
                self.TheBoardGame.FourBombs()
            elif bombe == "5":
                self.TheBoardGame.FiveBombs()
            self.TheBoardGame.HideGrille()

            while self.GameDuring is True and self.TheBoardGame.MinesNumber > 0:
                self.Action()
                self.Show()

                if self.Win() == False:
                    self.GameDuring = False
                    break

    def Win(self):
        if (
            self.TheBoardGame.MinesNumber <= 0
            or self.TheBoardGame.Map == self.TheBoardGame.MapHide
        ):
            print("\n\nBravo, Congratulations, Félicitations !!! Vous avez gagné!!!!")
            regame = input(
                "\nVoulez-vous rejouer ? <o> = oui et <n> = Non. Faites bien votre choix...\n>"
            )
            if regame.upper() == "O":
                self.GameDuring = True
                self.__init__()
                os.system("CLS")
            else:
                self.GameDuring = False
                return False

    def Show(self):
        print("Nombres de mines restantes:", self.TheBoardGame.MinesNumber)
        for i in self.TheBoardGame.MapHide:
            print(i, end="" + "\n")

    def Action(self):

        while True:
            lines = input("\n\nligne N°: ")
            if len(lines) == 1:
                try:
                    lines = int(lines)
                except ValueError:
                    print(
                        "\nAllez sois sympa, mets un nombre (c'est entre 0 et 4 si t'as oublié)"
                    )
                    continue

                if not lines in range(self.TheBoardGame.long):
                    continue

            colonne = input("Colonne N°: ")
            if len(colonne) == 1:
                try:
                    colonne = int(colonne)
                except ValueError:
                    print("\nC'est toujours un nombre entre 0 et 4 !")
                    continue

                if not colonne in range(self.TheBoardGame.long):
                    continue
                else:
                    break
        while True:
            choice = input(
                "\nc = Dig; d = Flag: Quel est ton choice jeune padawan ? : >"
            )
            print("\n")
            if choice.upper() == "C":
                self.GameDuring = self.TheBoardGame.Dig(lines, colonne)
                break
            elif choice.upper() == "D":
                self.GameDuring = self.TheBoardGame.Flag(lines, colonne)
                break
            else:
                continue


class BoardGame(object):
    def __init__(self):

        self.Map = []
        self.long = 5
        self.MapHide = []
        self.MinesNumber = 0

    def CreateGrille(self):
        for _ in range(self.long):
            self.Map.append([0] * self.long)

    def TwoBombs(self):
        self.Map = self.PlaceBomb()
        self.Map = self.PlaceBomb()

    def ThreeBombs(self):
        self.Map = self.PlaceBomb()
        self.Map = self.PlaceBomb()
        self.Map = self.PlaceBomb()

    def FourBombs(self):
        self.Map = self.PlaceBomb()
        self.Map = self.PlaceBomb()
        self.Map = self.PlaceBomb()
        self.Map = self.PlaceBomb()

    def FiveBombs(self):
        self.Map = self.PlaceBomb()
        self.Map = self.PlaceBomb()
        self.Map = self.PlaceBomb()
        self.Map = self.PlaceBomb()
        self.Map = self.PlaceBomb()

    def PlaceBomb(self):
        self.MinesNumber += 1
        self.col, self.lines, self.bombe = (
            random.randrange(0, self.long),
            random.randrange(0, self.long),
            9,
        )

        self.Map[self.col][self.lines] = self.bombe
        self.Map = self.NearBombs(self.col, self.lines)

        return self.Map

    def HideGrille(self):
        # On construit un tableau de '0' de /long/²
        for _ in range(self.long):
            self.MapHide.append(["*"] * self.long)

    def NearBombs(self, col, lines):
        for i in range(self.long):
            for j in range(self.long):
                newL = []

                for ii in range(max(0, i - 1), min(i + 2, self.long)):
                    for jj in range(max(0, j - 1), min(j + 2, self.long)):
                        newL.append(self.Map[ii][jj])

                if self.Map[i][j] != 9:
                    self.Map[i][j] = newL.count(9)
        newL = []
        return self.Map

    def Dig(self, lines, colonne):
        var = self.Map[lines][colonne]

        if self.MapHide[lines][colonne] == str(var):
            return

        elif var == 9:
            return
        else:
            self.MapHide[lines][colonne] = str(var)

        if var == 0:
            for ii in range(max(0, lines - 1), min(lines + 2, self.long)):
                for jj in range(max(0, colonne - 1), min(colonne + 2, self.long)):
                    self.Dig(ii, jj)

        return True

    def Flag(self, lines, colonne):
        var = self.MapHide[lines][colonne]

        if var == "*":
            var = "D"
            self.MinesNumber -= 1
        elif var == "D":
            var = "*"
            self.MinesNumber += 1
        else:
            pass

        self.MapHide[lines][colonne] = str(var)

        return True


if __name__ == "__main__":
    p = Game()
    p.Play()
