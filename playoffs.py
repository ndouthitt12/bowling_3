import random
import csv
import itertools
import numpy as np
import sqlite3
import game_9 as game

Player = game.Player

players = {}


class Playoffs:
    def __init__(self):
        self.matchup_num = 1
        self.results = []

    # Open and read the database
    def playoff_contenders(self):
        conn = sqlite3.connect('03/db/bowling.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Seed, s.Division, Player, Power, Accuracy, Consistency, Curve, Clutch, Fitness, Season
            FROM standings AS s
            INNER JOIN roster AS r
            ON s.Player = r.Name
            WHERE Seed <= 64
        """)
        rows = cursor.fetchall()
        for row in rows:
            seed = row[0]
            division = row[1]
            name = row[2]
            power = row[3]
            accuracy = row[4]
            consistency = row[5]
            curve = row[6]
            clutch = row[7]
            fitness = row[8]
            season = row[9]

            player = Player(division, name, power, accuracy, consistency, curve, clutch, fitness)
            players[seed] = player

        return players, season

    def simulate_series(self, season, round, seed1, seed2, player1, player2, best_of=7, g=1):
        wins1 = 0
        wins2 = 0

        while max(wins1, wins2) < best_of/2:
            game_ = game.Game(player1, player2, True, g)
            game_.play()
            score1, score2, frame_scores1, frame_scores2, ot_rounds, ot_score1, ot_score2, ot_frames1, ot_frames2, rolls1, ot_rolls1, rolls2, ot_rolls2 = game_.calculate_winner()
            
            if game_.winner == player1:
                wins1 += 1
            elif game_.winner == player2:
                wins2 += 1
            
            self.results.append((
                season,
                round, 
                g, 
                seed1, 
                player1.name, 
                seed2, 
                player2.name, 
                score1, 
                score2, 
                frame_scores1, 
                frame_scores2, 
                wins1, 
                wins2, 
                ot_score1, 
                ot_score2, 
                ot_frames1,
                ot_frames2, 
                ot_rounds, 
                rolls1, 
                ot_rolls1, 
                rolls2, 
                ot_rolls2
                ))
            g += 1

        winner = player1 if wins1 > wins2 else player2

        return winner, wins1, wins2, score1, score2, frame_scores1, frame_scores2, self.results


    def simulate_round(self, season, round, seeds, players):
        winners = {}

        for i in range(len(seeds) // 2):
            seed1, seed2 = seeds[i], seeds[len(seeds) - 1 - i]
            player1, player2 = players[seed1], players[seed2]

            winner, wins1, wins2, score1, score2, frame_scores1, frame_scores2, self.results = self.simulate_series(season, round, seed1, seed2, player1, player2)
            winners[seed1 if winner == player1 else seed2] = winner

            # print(f"#{self.matchup_num} [{seed1}] {player1.name} vs {player2.name} [{seed2}] - ({wins1} - {wins2})")
            
            self.matchup_num += 1
        
        return winners, self.results

    def simulate_playoffs(self):
        players, season = self.playoff_contenders()
        seeds = sorted(players.keys())
        results = []
        round_number = 1

        

        while len(seeds) > 1:
            # print(f"\nRound {round_number}\n")
            winners, results = self.simulate_round(season, round_number, seeds, players)
            seeds = sorted(winners.keys())
            players = winners
            round_number += 1

        return seeds[0], players[seeds[0]].name, results  # return the winning seed and player name

    def write_to_csv(self, results, output_file):
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            rounds = ["Opening Round","Round 32","Sweet 16","Elite 8","Final 4","Championship"]

            for i, (season, r, g, s1, p1, s2, p2, score1, score2, frames1, frames2, wins1, wins2, ot_score1, ot_score2, ot_frames1, ot_frames2, ot_rounds, rolls1, ot_rolls1, rolls2, ot_rolls2) in enumerate(results):
                writer.writerow([
                    season,
                    i+1,  # total game num
                    rounds[r-1],  # round
                    g,  # series game num
                    s1,  # seed 1
                    p1,  # player 1
                    score1,  # score 1
                    ot_score1,  # overtime score 1
                    ot_rounds,  # number of overtime rounds
                    ot_score2,
                    score2,  # overtime score 2 and score 2
                    p2,  # player 2
                    s2,  # seed 2
                    str(f"({wins1}-{wins2})"),  # wins
                    str(f"{frames1} {ot_frames1}"),
                    str(f"{frames2} {ot_frames2}"),
                    str(f"{rolls1} {ot_rolls1}"), 
                    str(f"{rolls2} {ot_rolls2}"),
                    p1 if score1 + ot_score1 > score2 + ot_score2 else p2
                ])

                    



if __name__ == "__main__":
    winning_seed, winning_player, results = Playoffs().simulate_playoffs()
    # print(f"\nChampion: [{winning_seed}] {winning_player}")
    Playoffs().write_to_csv(results, '03/csv_files/playoff_results.csv')

    from csv_db_converts import playoffs as p

    p('03/csv_files/playoff_results.csv','03/db/bowling.db')
                                  