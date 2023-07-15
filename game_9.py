import random
import csv
import itertools
import numpy as np


year = 1970

class Player:
    def __init__(self, division, name, power, accuracy, consistency, curve, clutch, fitness):
        self.division = division
        self.name = name
        self.power = int(power)
        self.accuracy = int(accuracy)
        self.consistency = int(consistency)
        self.curve = int(curve)
        self.clutch = int(clutch)
        self.fitness = int(fitness)


# Create a list to store the players
players = []
players_by_division = {}

# Open and read the CSV file
with open('03/csv_files/roster.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)  # Skip the header
    for row in reader:
        # Create a new Player object for each row in the CSV and add it to the players list
        division = row[0]
        player = Player(division, row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        players.append(Player(division, row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

        # If the division isn't already in the dictionary, add it
        if division not in players_by_division:
            players_by_division[division] = []
            
        # Add the player to their division's list
        players_by_division[division].append(player)


class Game:
    def __init__(self, player1, player2, playoffs=False, g=0):
        self.playoffs = playoffs
        self.g = g
        self.player1 = player1
        self.player2 = player2
        self.rolls1 = []
        self.rolls2 = []
        self.overtime_rolls1 = []
        self.overtime_rolls2 = []
        self.strikes1 = 0
        self.strikes2 = 0
        self.spares1 = 0
        self.spares2 = 0
        self.open_frames1 = 0
        self.open_frames2 = 0
        self.current_frame = 0
        self.winner = None

    
    def roll(self, player, pins=10, second_roll=False):
        current_frame = self.current_frame

        seed_advantage = 1.05 #for rolls by higher seed players in the playoffs
        
        power = player.power
        acc = player.accuracy
        con = player.consistency

        if self.g in [1,2,5,7] and player.name == self.player1.name:
            power = min(100,round(power * seed_advantage))
            acc = min(100,round(acc * seed_advantage))
            con = min(100,round(con * seed_advantage))
        elif self.g in [3,4,6] and player.name == self.player2.name:
            power = min(100,round(power * seed_advantage))
            acc = min(100,round(acc * seed_advantage))
            con = min(100,round(con * seed_advantage))
        
        if second_roll and pins < 5:  
            # during second roll, if there are less than 5 pins, account for accuracy
            expected_value = (power / 9 * (100 - acc) + pins * acc) / 100
        else:
            expected_value = min(power / 9, pins)

        roll = min(pins, max(0, round(np.random.normal(
            expected_value,  # power rating
            95 / con  # increased scale factor for inverse consistency rating
        ))))

        if second_roll == False and roll == 10:
            if player == self.player1:
                self.strikes1 += 1
            if player == self.player2:
                self.strikes2 += 1

        # if player.name == "Damien De La Cruz":
        #     print(f"{self.g} {player.name} - ({player.power},{player.accuracy},{player.consistency}")
        #     print(f"{self.g} {player.name} - ({power},{acc},{con}")

        return roll




    def play(self):
        for frame in range(10):
            self.current_frame = frame + 1
            for i, (player, rolls) in enumerate([(self.player1, self.rolls1), (self.player2, self.rolls2)]):
                first_roll = self.roll(player)
                rolls.append(first_roll)
                if first_roll == 10:  # strike
                    if frame == 9:  # extra two rolls in the 10th frame for a strike
                        pins_left = 10
                        for _ in range(2):
                            bonus_roll = self.roll(player, pins_left)
                            rolls.append(bonus_roll)
                            # The following line ensures that if less than 10 pins were knocked down, 
                            # the remaining number of pins for the next roll is adjusted accordingly.
                            pins_left = 10 - (bonus_roll if bonus_roll < 10 else 0)
                else:  # second roll
                    second_roll = self.roll(player, 10 - first_roll, True)
                    rolls.append(second_roll)

                    # spare
                    if first_roll + second_roll == 10:
                        if i == 0:  # player 1
                            self.spares1 += 1
                        else:  # player 2
                            self.spares2 += 1
                        # extra roll in the 10th frame for a spare
                        if frame == 9:
                            bonus_roll = self.roll(player, 10, True)
                            # if bonus_roll == 10:
                                # if i == 0:  # player 1
                                    # self.strikes1 += 1
                                # else:  # player 2
                                    # self.strikes2 += 1
                            rolls.append(bonus_roll)
                    else:  # open frame
                        if i == 0:  # player 1
                            self.open_frames1 += 1
                        else:  # player 2
                            self.open_frames2 += 1

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
                if roll_index < len(rolls) - 3:  # not the final frame
                    # always add the next two rolls regardless of whether they make up a spare, strike or open frame
                    score += sum(rolls[roll_index+1:roll_index+3])
                elif roll_index < len(rolls) - 1:  # final frame
                    # add the scores of the two bonus rolls
                    score += sum(rolls[roll_index+1:roll_index+3])
                roll_index += 1

            elif self.is_spare(rolls, roll_index):  # spare
                score += 10 + rolls[roll_index+2] if roll_index + 2 < len(rolls) else 10
                roll_index += 2
            else:  # open frame
                score += sum(rolls[roll_index:roll_index+2])
                roll_index += 2
            frame_scores.append(score)
        
        
        return score, frame_scores
    

    def overtime(self):
        self.overtime_rolls1 = []
        self.overtime_rolls2 = []
        for frame in range(3):  # 3 extra frames for overtime
            self.current_frame = frame + 1  # we reset the frame count for overtime
            for i, (player, rolls) in enumerate([(self.player1, self.overtime_rolls1), (self.player2, self.overtime_rolls2)]):
                first_roll = self.roll(player)
                rolls.append(first_roll)
                if first_roll == 10:  # strike
                    if frame == 2:  # extra two rolls in the 3rd overtime frame for a strike
                        pins_left = 10
                        for _ in range(2):
                            bonus_roll = self.roll(player, pins_left)
                            rolls.append(bonus_roll)
                            # The following line ensures that if less than 10 pins were knocked down, 
                            # the remaining number of pins for the next roll is adjusted accordingly.
                            pins_left = 10 - (bonus_roll if bonus_roll < 10 else 0)
                else:  # second roll
                    second_roll = self.roll(player, 10 - first_roll, True)
                    rolls.append(second_roll)
                    # spare
                    if first_roll + second_roll == 10:
                        # extra roll in the 6th overtime frame for a spare
                        if frame == 2:
                            bonus_roll = self.roll(player, 10)
                            rolls.append(bonus_roll)


    def overtime_score(self, rolls):
        if not rolls:
            return 0, []
        score = 0
        frame_scores = []
        roll_index = 0
        for frame in range(3):  # changed to consider only 3 frames
            if self.is_strike(rolls, roll_index):  # strike
                score += 10
                if roll_index < len(rolls) - 3:  # not the final frame
                    # always add the next two rolls regardless of whether they make up a spare, strike or open frame
                    score += sum(rolls[roll_index+1:roll_index+3])
                elif roll_index < len(rolls) - 1:  # final frame
                    # add the scores of the two bonus rolls
                    score += sum(rolls[roll_index+1:roll_index+3])
                roll_index += 1
            elif self.is_spare(rolls, roll_index):  # spare
                score += 10 + rolls[roll_index+2] if roll_index + 2 < len(rolls) else 10
                roll_index += 2
            else:  # open frame
                score += sum(rolls[roll_index:roll_index+2])
                roll_index += 2
            frame_scores.append(score)
        return score, frame_scores




    def calculate_winner(self):
        score1, frame_scores1 = self.score(self.rolls1)
        score2, frame_scores2 = self.score(self.rolls2)
        ot_score1, ot_frame_scores1 = 0, []
        ot_score2, ot_frame_scores2 = 0, []
        ot_frame_scores1_rounds = []  # Store all overtime frame scores for player 1
        ot_frame_scores2_rounds = []  # Store all overtime frame scores for player 2
        ot_rounds = 0

        if score1 > score2:
            self.winner = self.player1
        elif score2 > score1:
            self.winner = self.player2
        else:
            while self.winner is None:
                if self.playoffs:
                    self.overtime()  # Trigger overtime
                    ot_rounds += 1
                    ot_score1_round, ot_frame_scores1_round = self.overtime_score(self.overtime_rolls1)
                    ot_score2_round, ot_frame_scores2_round = self.overtime_score(self.overtime_rolls2)
                    ot_score1 += ot_score1_round  # Add the new overtime score to the total
                    ot_score2 += ot_score2_round  # Add the new overtime score to the total
                    ot_frame_scores1_rounds.append(ot_frame_scores1_round)  # Store this round's frame scores
                    ot_frame_scores2_rounds.append(ot_frame_scores2_round)  # Store this round's frame scores
                    self.winner = self.player1 if ot_score1 > ot_score2 else self.player2 if ot_score1 < ot_score2 else None
                    # print(f"{self.player1.name} ({ot_score1}) - ({ot_score2}) {self.player2.name}")
                else:
                    self.winner = None  # It's a tie
                    break  # End the loop in case of a non-playoff tie

        # if self.playoffs and self.player1.name == "Damien De La Cruz":
        #     print(f"{self.player1.name}: {self.rolls1} {self.overtime_rolls1}")

        if score1 == score2:
            return score1, score2, frame_scores1, frame_scores2, ot_rounds, ot_score1, ot_score2, ot_frame_scores1_rounds, ot_frame_scores2_rounds, self.rolls1, self.overtime_rolls1, self.rolls2, self.overtime_rolls2
        else:
            return score1, score2, frame_scores1, frame_scores2, 0, 0, 0, [], [], self.rolls1, [], self.rolls2, []


        



class Season:
    def __init__(self, year, players_by_division):
        self.year = year
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
            score1, score2, frame_scores1, frame_scores2, ot_rounds, ot_score1, ot_score2, ot_frames1, ot_frames2, rolls1, ot_rolls1, rolls2, ot_rolls2 = game.calculate_winner()
            result = [
                self.year,
                game.player1.division, 
                game.player1.name, 
                game.player2.name, 
                score1, 
                score2, 
                game.winner.name if game.winner else "Tie", 
                game.strikes1, 
                game.spares1, 
                game.open_frames1,
                game.rolls1,
                game.strikes2, 
                game.spares2,
                game.open_frames2,
                game.rolls2
            ]
            # Extend result with frame scores
            result.extend(frame_scores1)
            result.extend(frame_scores2)


            self.results.append(result)




    def save_results(self):
        with open('03/csv_files/season_results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Prepare the headers
            headers = ["Season","Division", "P1", "P2", "P1 Score", "P2 Score", "Winner", 
                    "P1 Strikes", "P1 Spares", "P1 OF", "P1 Rolls", "P2 Strikes", "P2 Spares", "P2 OF", "P2 Rolls"]
            # Add headers for frame scores
            headers.extend([f"P1 Frame{i+1}" for i in range(10)])
            headers.extend([f"P2 Frame{i+1}" for i in range(10)])
            
            writer.writerow(headers)
            writer.writerows(self.results)



if __name__ == "__main__":
    
    season = Season(year, players_by_division)
    season.schedule()
    season.play()
    season.save_results()

    import standings
    import csv_db_converts
