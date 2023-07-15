import sqlite3
import csv
# import os
# import numpy as np


def standings(csv_file, db_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create the players table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS standings (
            Season INTEGER,
            Seed INTEGER,
            Division TEXT,
            Player TEXT,
            Wins INTEGER,
            Losses INTEGER,
            Ties INTEGER,
            Pins INTEGER,
            OppPins INTEGER,
            AvgPins DOUBLE,
            OppAvgPins DOUBLE,
            Diff DOUBLE,
            Strikes INTEGER,
            Spares INTEGER,
            OpenFrames INTEGER
        )
    """)

    # Load the CSV file
    with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for row in reader:
            # Check if player already exists
            cursor.execute("""
                INSERT INTO standings
                (Season,Seed, Division, Player, Wins, Losses, Ties, Pins, OppPins, AvgPins, OppAvgPins, Diff, Strikes, Spares, OpenFrames)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, row)

    # Commit the changes and close the database connection
    conn.commit()
    cursor.close()
    conn.close()


def season_results(csv_file, db_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create the players table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS season_results (
            Season INTEGER,
            Division TEXT,
            P1 TEXT,
            P2 TEXT,
            P1_Score INTEGER,
            P2_Score INTEGER,
            Winner TEXT,
            P1_Strikes INTEGER,
            P1_Spares INTEGER,
            P1_OF INTEGER,
            P1_Rolls INTEGER,
            P2_Strikes INTEGER,
            P2_Spares INTEGER,
            P2_OF INTEGER,
            P2_Rolls INTEGER,
            P1_Frame1 INTEGER,
            P1_Frame2 INTEGER,
            P1_Frame3 INTEGER,
            P1_Frame4 INTEGER,
            P1_Frame5 INTEGER,
            P1_Frame6 INTEGER,
            P1_Frame7 INTEGER,
            P1_Frame8 INTEGER,
            P1_Frame9 INTEGER,
            P1_Frame10 INTEGER,
            P2_Frame1 INTEGER,
            P2_Frame2 INTEGER,
            P2_Frame3 INTEGER,
            P2_Frame4 INTEGER,
            P2_Frame5 INTEGER,
            P2_Frame6 INTEGER,
            P2_Frame7 INTEGER,
            P2_Frame8 INTEGER,
            P2_Frame9 INTEGER,
            P2_Frame10 INTEGER
        )
    """)


    # Load the CSV file
    with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for row in reader:
            # Check if player already exists
            cursor.execute("""
                INSERT INTO season_results
                (
                    Season,
                    Division,
                    P1,
                    P2,
                    P1_Score,
                    P2_Score,
                    Winner,
                    P1_Strikes,
                    P1_Spares,
                    P1_OF,
                    P1_Rolls,
                    P2_Strikes,
                    P2_Spares,
                    P2_OF,
                    P2_Rolls,
                    P1_Frame1,
                    P1_Frame2,
                    P1_Frame3,
                    P1_Frame4,
                    P1_Frame5,
                    P1_Frame6,
                    P1_Frame7,
                    P1_Frame8,
                    P1_Frame9,
                    P1_Frame10,
                    P2_Frame1,
                    P2_Frame2,
                    P2_Frame3,
                    P2_Frame4,
                    P2_Frame5,
                    P2_Frame6,
                    P2_Frame7,
                    P2_Frame8,
                    P2_Frame9,
                    P2_Frame10
                )
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, row)

    # Commit the changes and close the database connection
    conn.commit()
    cursor.close()
    conn.close()



def roster(csv_file, db_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create the players table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS roster (
            Division TEXT,
            Name TEXT,
            Power INTEGER,
            Accuracy INTEGER,
            Consistency INTEGER,
            Curve INTEGER,
            Clutch INTEGER,
            Fitness INTEGER
        )
    """)

    # Load the CSV file
    with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for row in reader:
            # Check if player already exists
            cursor.execute("""
                INSERT INTO roster
                (Division,Name,Power,Accuracy,Consistency,Curve,Clutch,Fitness)
                VALUES (?,?,?,?,?,?,?,?)
            """, row)

    # Commit the changes and close the database connection
    conn.commit()
    cursor.close()
    conn.close()



def playoffs(csv_file, db_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create the players table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS playoffs (
            Season INTEGER,
            MatchupNum INTEGER,
            Round TEXT,
            GameNum INTEGER,
            Seed1 INTEGER,
            P1 TEXT,
            Score1 INTEGER,
            OT1 INTEGER,
            OT INTEGER,
            OT2 INTEGER,
            Score2 INTEGER,
            P2 TEXT,
            Seed2 INTEGER,
            Series TEXT,
            Frames1 TEXT,
            Frames2 TEXT,
            Rolls1 TEXT,
            Rolls2 TEXT,
            Winner TEXT
        )
    """)

    # Load the CSV file
    with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        # next(reader)  # Skip header row
        for row in reader:
            # Check if player already exists
            cursor.execute("""
                INSERT INTO playoffs
                (Season,MatchupNum,Round,GameNum,Seed1,P1,Score1,OT1,OT,OT2,Score2,P2,Seed2,Series,Frames1,Frames2,Rolls1,Rolls2,Winner)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, row)

    # Commit the changes and close the database connection
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":

    standings('03/csv_files/standings.csv','03/db/bowling.db')
    season_results('03/csv_files/season_results.csv','03/db/bowling.db')
    roster('03/csv_files/roster.csv','03/db/bowling.db')
    # playoffs('03/csv_files/playoff_results.csv','03/db/bowling.db')