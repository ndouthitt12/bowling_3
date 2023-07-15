import csv
from collections import defaultdict

# Create defaultdicts to track wins, losses, and ties
wins = defaultdict(int)
losses = defaultdict(int)
ties = defaultdict(int)
own_score = defaultdict(int)
opp_score = defaultdict(int)
own_strikes = defaultdict(int)
own_spares = defaultdict(int)
div_ = defaultdict(int)
own_of = defaultdict(int)



def standings():
    # Open the CSV file and read its contents
    with open('03/csv_files/season_results.csv', 'r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            season = row['Season']
            div = row['Division']
            player1 = row['P1']
            player2 = row['P2']
            score1 = int(row['P1 Score'])
            score2 = int(row['P2 Score'])
            winner = row['Winner']
            strikes1 = int(row['P1 Strikes'])
            spares1 = int(row['P1 Spares'])
            open_frames1 = int(row['P1 OF'])
            rolls1 = row['P1 Rolls']
            strikes2 = int(row['P2 Strikes'])
            spares2 = int(row['P2 Spares'])
            open_frames2 = int(row['P2 OF'])
            rolls2 = row['P2 Rolls']

            frame_scores1 = [int(row[f'P1 Frame{i}']) for i in range(1, 11)]
            frame_scores2 = [int(row[f'P2 Frame{i}']) for i in range(1, 11)]

            # print(f"{player1}: [{stk_rating_1}] [{spr_rating_1}]")
            # print(f"{player2}: [{stk_rating_2}] [{spr_rating_2}]")

            div_[player1] = div
            div_[player2] = div

            own_score[player1] += int(score1)
            opp_score[player1] += int(score2)
            own_score[player2] += int(score2)
            opp_score[player2] += int(score1)


            own_strikes[player1] += int(strikes1)
            own_spares[player1] += int(spares1)

            own_strikes[player2] += int(strikes2)
            own_spares[player2] += int(spares2)

            own_of[player1] += int(open_frames1)
            own_of[player2] += int(open_frames2)

            if winner == "Tie":
                ties[player1] += 1
                ties[player2] += 1
            elif winner == player1:
                wins[player1] += 1
                losses[player2] += 1
            else:  # winner == player2
                wins[player2] += 1
                losses[player1] += 1

    # Open a new CSV file and write the results
    with open('03/csv_files/standings.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["Season","Division", "Player", "Wins", "Losses", "Ties", "Pins", "Opp Pins", "Avg. Pins", "Opp. Avg. Pins", "Diff", "Strikes", "Spares", "Open Frames"])
        # Include every player who played at least one game
        all_players = set(wins.keys()).union(losses.keys()).union(ties.keys())
        
        # Sort the players by number of wins
        sorted_players = sorted(all_players, key=lambda player: (wins[player],-losses[player], own_score[player]), reverse=True)

        
        for i, player in enumerate(sorted_players, 1):
            avg_pins = own_score[player]/(wins[player] + losses[player])
            avg_opp_pins = opp_score[player]/(wins[player] + losses[player])
            diff = avg_pins - avg_opp_pins
            # print(f"{player}: [{own_stk_rating}] [{own_spr_rating}]")
            writer.writerow([
                season, #season
                i, #seed
                div_[player], #division
                player, #name
                wins[player], #wins 
                losses[player], #losses
                ties[player], #ties
                own_score[player], # pins
                opp_score[player], # opp pins
                round(avg_pins,1), #avg pins scored
                round(avg_opp_pins,1), #avg pins scored against
                round(diff,1), #differential
                own_strikes[player], #total strikes
                own_spares[player], #total spares
                own_of[player] #open frames
                ])

if __name__ == "__main__":
    standings()