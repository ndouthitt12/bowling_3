import random
import csv
import itertools
import numpy as np


class Player:
    def __init__(self, division, name, power, accuracy, consistency, curve, clutch):
        self.division = division
        self.name = name
        self.power = int(power)
        self.accuracy = int(accuracy)
        self.consistency = int(consistency)
        self.curve = int(curve)
        self.clutch = int(clutch)


# Create a list to store the players
players = []
players_by_division = {}

# Open and read the CSV file
with open('02/csv_files/roster.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)  # Skip the header
    for row in reader:
        # Create a new Player object for each row in the CSV and add it to the players list
        division = row[0]
        player = Player(division, row[1], row[2], row[3], row[4], row[5], row[6])
        players.append(Player(division, row[1], row[2], row[3], row[4], row[5], row[6]))

        # If the division isn't already in the dictionary, add it
        if division not in players_by_division:
            players_by_division[division] = []
            
        # Add the player to their division's list
        players_by_division[division].append(player)


class FinalFrame:
    def __init__(self, player_rating=50):
        self.player_rating = player_rating

    def roll(self, pins=10):
        # A higher skill rating increases the likelihood of knocking down all the pins
        if random.random() < self.player_rating / 100:  # convert skill rating to a probability
            return pins  # knock down all the pins
        else:
            return random.randint(0, pins)  # knock down a random number of pins

    def play(self):
        # First roll of the final frame
        first_roll = self.roll()

        if first_roll == 10:  # strike
            # Two bonus rolls after a strike in the final frame
            second_roll = self.roll()
            if second_roll == 10:  # another strike
                third_roll = self.roll()
            else:
                third_roll = self.roll(10 - second_roll)
        else:
            second_roll = self.roll(10 - first_roll)
            if first_roll + second_roll == 10:  # spare
                # One bonus roll after a spare in the final frame
                third_roll = self.roll()
            else:
                third_roll = 0

        return first_roll, second_roll, third_roll



class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.rolls1 = []
        self.rolls2 = []
        self.strikes1 = 0
        self.strikes2 = 0
        self.spares1 = 0
        self.spares2 = 0
        self.current_frame = 0
        self.winner = None

    def roll(self, player, pins=10):
        # power influences the range of pins that can potentially be knocked down
        # A player with high power can knock down more pins
        potential_pins = int((player.power / 100) * pins)

        # accuracy and consistency influences the likelihood of knocking down the potential pins
        # A player with high accuracy and consistency is more likely to knock down the potential pins
        if random.random() < (player.accuracy / 100) * (player.consistency / 100):
            knocked_down_pins = potential_pins
        else:
            knocked_down_pins = random.randint(0, potential_pins)

        # curve can add additional pins if the curve is successful
        # A player with high curve has more chances to knock down additional pins
        if random.random() < player.curve / 100:
            knocked_down_pins += random.randint(1, pins - knocked_down_pins)

        # clutch comes into play in the last frame or when the player has fewer than 3 pins left
        # A player with high clutch is more likely to knock down all the pins in these situations
        if (self.current_frame == 10 or pins <= 3) and random.random() < player.clutch / 100:
            knocked_down_pins = pins

        return knocked_down_pins


    def play(self):
        for frame in range(10):
            self.current_frame = frame + 1
            for i, (player, rolls) in enumerate([(self.player1, self.rolls1), (self.player2, self.rolls2)]):
                first_roll = self.roll(player)
                rolls.append(first_roll)
                if first_roll == 10:  # strike
                    if i == 0:  # player 1
                        self.strikes1 += 1
                    else:  # player 2
                        self.strikes2 += 1
                    if frame == 9:  # extra two rolls in the 10th frame for a strike
                        for _ in range(2):
                            bonus_roll = self.roll(player)
                            rolls.append(bonus_roll)
                else:  # second roll
                    second_roll = self.roll(player, 10 - first_roll)
                    rolls.append(second_roll)

                    # spare
                    if first_roll + second_roll == 10:
                        if i == 0:  # player 1
                            self.spares1 += 1
                        else:  # player 2
                            self.spares2 += 1
                        # extra roll in the 10th frame for a spare
                        if frame == 9:
                            bonus_roll = self.roll(player)
                            rolls.append(bonus_roll)

    def is_strike(self, rolls, roll_index):
        return rolls[roll_index] == 10

    def is_spare(self, rolls, roll_index):
        return sum(rolls[roll_index:roll_index+2]) == 10


    def score(self, rolls):
        score = 0
        frame_scores = []
        roll_index = 0
        for frame in range(10):
            if self.is_strike(rolls, roll_index):  # strike
                score += 10
                if roll_index + 1 < len(rolls):  # not the final frame
                    score += rolls[roll_index + 1]
                    if roll_index + 2 < len(rolls): 
                        if frame < 9 or rolls[roll_index + 1] == 10: # second bonus roll is from the next frame or if strike in 10th frame
                            score += rolls[roll_index + 2]
                        elif roll_index + 3 < len(rolls): # Check if roll_index + 3 is a valid index
                            score += rolls[roll_index + 3]

                roll_index += 1
            elif self.is_spare(rolls, roll_index):  # spare
                score += 10 + rolls[roll_index+2] if roll_index + 2 < len(rolls) else 0
                roll_index += 2
            else:  # open frame
                score += sum(rolls[roll_index:roll_index+2])
                roll_index += 2
            frame_scores.append(score)
        return score, frame_scores



    def calculate_winner(self):
        score1, frame_scores1 = self.score(self.rolls1)
        score2, frame_scores2 = self.score(self.rolls2)

        if score1 > score2:
            self.winner = self.player1
        elif score2 > score1:
            self.winner = self.player2
        else:
            self.winner = None  # It's a tie

        return score1, score2




class Season:
    def __init__(self, players_by_division):
        self.players_by_division = players_by_division
        self.games = []
        self.results = []

    def schedule(self):
        for division, players in self.players_by_division.items():
            # Create a round-robin schedule within the division
            for _ in range(3):  # repeat 3 times
                matchups = list(itertools.combinations(players, 2))
                random.shuffle(matchups)  # randomize the schedule
                self.games.extend([Game(matchup[0], matchup[1]) for matchup in matchups])  # create games





    def play(self):
        for game in self.games:
            game.play()
            score1, score2 = game.calculate_winner()
            self.results.append((game.player1.division, game.player1.name, game.player2.name, score1, score2, game.winner.name if game.winner else "Tie", game.strikes1, game.spares1, game.strikes2, game.spares2))

    def save_results(self):
        with open('02/csv_files/season_results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Division","Player 1", "Player 2", "Player 1 Score", "Player 2 Score", "Winner", "Player 1 Strikes", "Player 1 Spares", "Player 2 Strikes", "Player 2 Spares"])
            writer.writerows(self.results)





if __name__ == "__main__":
    for divisions, players in players_by_division.items():
        matchups = list(itertools.combinations(players, 2))
        random.shuffle(matchups)  # randomize the schedule
        player1, player2 = matchups[0]  # Unpack the tuple into two Player objects
        game = Game(player1, player2)
        game.play()  # add this line here
        score1, score2 = game.calculate_winner()
        print(f"{game.player1.name} vs. {game.player2.name}")
        print(f"{score1} - {game.rolls1}")
        print(f"{score2} - {game.rolls2}")
