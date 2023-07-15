import sqlite3
import csv
import os
import numpy as np
import game_9 as game
import playoffs as po
import standings as st

import csv_db_converts as cdc



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

def db_connect(db_file):
    conn = sqlite3.connect(db_file)
    return conn, conn.cursor()


def get_max_season(db_file):
    conn, cursor = db_connect(db_file)
    cursor.execute("""
    SELECT
     max(Season)
    FROM 
        playoffs 
     """)
    for row in cursor:
        max_season = row[0]
    # print(max_season)
    conn.close()

    return max_season

def main(year, sim_years):
    db_file_path = '03/db/bowling.db'
    
    # print(year)
    
    

    for i in range(sim_years):
        season = game.Season(year, players_by_division) 
        season.schedule()
        season.play()
        season.save_results()

        st.standings()

        cdc.standings('03/csv_files/standings.csv','03/db/bowling.db')
        cdc.season_results('03/csv_files/season_results.csv','03/db/bowling.db')
        cdc.roster('03/csv_files/roster.csv','03/db/bowling.db')

        winning_seed, winning_player, results = po.Playoffs().simulate_playoffs()
        print(f"\n[{year}] Champion: [{winning_seed}] {winning_player}")
        po.Playoffs().write_to_csv(results, '03/csv_files/playoff_results.csv')

        # from csv_db_converts import playoffs as p

        cdc.playoffs('03/csv_files/playoff_results.csv','03/db/bowling.db')

        # p('03/csv_files/playoff_results.csv','03/db/bowling.db')
        
        year = get_max_season(db_file_path)
        year += 1


if __name__ == "__main__":
    main(1994, 12)
