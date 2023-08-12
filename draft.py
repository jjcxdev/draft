import pandas as pd

# Load the data
data = pd.read_csv("data.csv")
data = data.rename(
    columns={"Player": "Name", "FPts": "fantasy_points", "Position": "Position"}
)
data = data.sort_values(by=["fantasy_points"], ascending=False)


def get_required_positions(selected_players_df, format_dict):
    required_positions = {}
    for pos, count in format_dict.items():
        selected_in_position = selected_players_df[
            selected_players_df["Position"].str.contains(pos)
        ].shape[0]
        required_positions[pos] = count - selected_in_position
    return required_positions


def form_best_team_from_pool(players_df):
    positions = ["G", "D", "M", "F"]
    starting_XI_format = [1, 3, 4, 3]
    reserves_format = [0, 2, 2, 2]

    best_starting_XI = []
    best_reserves = []
    already_selected = []

    for pos, start_count, res_count in zip(
        positions, starting_XI_format, reserves_format
    ):
        eligible_players = players_df[players_df["Position"].str.contains(pos)]
        eligible_players = eligible_players[
            ~eligible_players["Name"].isin(already_selected)
        ]

        best_for_position = eligible_players.nlargest(start_count, "fantasy_points")
        best_starting_XI.append(best_for_position)
        already_selected.extend(best_for_position["Name"].tolist())

    for pos, res_count in zip(positions, reserves_format):
        eligible_players = players_df[players_df["Position"].str.contains(pos)]
        eligible_players = eligible_players[
            ~eligible_players["Name"].isin(already_selected)
        ]

        best_reserves_for_position = eligible_players.nlargest(
            res_count, "fantasy_points"
        )
        best_reserves.append(best_reserves_for_position)
        already_selected.extend(best_reserves_for_position["Name"].tolist())

    return pd.concat(best_starting_XI), pd.concat(best_reserves)


def suggest_next_player(player_pool, selected_players_df):
    starting_XI_format = {"G": 1, "D": 3, "M": 4, "F": 3}
    reserves_format = {"G": 0, "D": 2, "M": 2, "F": 2}

    # Calculate how many more players are needed for each position
    required_positions = get_required_positions(selected_players_df, starting_XI_format)

    if sum(required_positions.values()) == 0:
        required_positions = get_required_positions(
            selected_players_df, reserves_format
        )
    else:
        for pos, count in reserves_format.items():
            required_positions[pos] += count

    # Sort player pool by points
    sorted_pool = player_pool.sort_values(by="fantasy_points", ascending=False)

    # Find the next player
    for _, player in sorted_pool.iterrows():
        player_positions = player["Position"].split(",")
        for position in player_positions:
            if required_positions[position] > 0:
                required_positions[position] -= 1
                return player

    return None


def display_best_team(player_pool):
    best_starting_XI, best_reserves = form_best_team_from_pool(player_pool)

    print("\nBest possible starting XI:")
    for _, player in best_starting_XI.iterrows():
        print(
            f"{player['Position']}, {player['Name']}, {player['fantasy_points']} points"
        )

    print("\nBest possible reserves:")
    for _, player in best_reserves.iterrows():
        print(
            f"{player['Position']}, {player['Name']}, {player['fantasy_points']} points"
        )


def display_current_team(selected_players_df):
    starting_positions_format = {"G": 1, "D": 3, "M": 4, "F": 3}
    reserves_positions_format = {"G": 0, "D": 2, "M": 2, "F": 2}
    displayed_players = []

    print("\nYour current starting XI:")
    for position, count in starting_positions_format.items():
        position_players = selected_players_df[
            selected_players_df["Position"].str.contains(position)
        ]
        position_players = position_players[
            ~position_players["Name"].isin(displayed_players)
        ].nlargest(count, "fantasy_points")

        for _, player in position_players.iterrows():
            print(
                f"{player['Position']}, {player['Name']}, {player['fantasy_points']} points"
            )
            displayed_players.append(player["Name"])

        for _ in range(count - len(position_players)):
            print(f"{position}, ***")

    print("\nYour current reserves:")
    for position, count in reserves_positions_format.items():
        position_players = selected_players_df[
            selected_players_df["Position"].str.contains(position)
        ]
        position_players = position_players[
            ~position_players["Name"].isin(displayed_players)
        ].nlargest(count, "fantasy_points")

        for _, player in position_players.iterrows():
            print(
                f"{player['Position']}, {player['Name']}, {player['fantasy_points']} points"
            )
            displayed_players.append(player["Name"])

        for _ in range(count - len(position_players)):
            print(f"{position}, ***")


# Main Execution

# Display the initial best starting XI and reserves
display_best_team(data)

selected_players = pd.DataFrame(columns=data.columns)
other_managers_choices = []

while len(selected_players) < 18:
    other_choices = input(
        "Enter names of players chosen by other managers, separated by comma: "
    )
    other_managers_choices.extend(
        [choice.strip() for choice in other_choices.split(",") if choice.strip()]
    )
    data = data[~data["Name"].isin(other_managers_choices)]

    display_best_team(data)

    recommended_player = suggest_next_player(data, selected_players)

    if recommended_player is not None:
        print(
            f"\nRecommended player for you to select: {recommended_player['Position']}, {recommended_player['Name']}, {recommended_player['fantasy_points']} points"
        )
    else:
        print("No suitable players left to recommend.")

    valid_choice = False
    while not valid_choice:
        player_choice = input(
            "Enter the name of the player you've selected (or press Enter to select the recommended player): "
        )
        if not player_choice:
            player_choice = recommended_player["Name"]
            valid_choice = True
        elif player_choice.lower() in data["Name"].str.lower().tolist():
            valid_choice = True
        else:
            print(f"{player_choice} is not a recognized player name. Please try again.")

    selected_player_data = data[data["Name"] == player_choice].iloc[0]
    selected_players = selected_players.append(selected_player_data, ignore_index=True)
    data = data[data["Name"] != player_choice]

    display_current_team(selected_players)

# Final output
current_starting_XI, current_reserves = form_best_team_from_pool(selected_players)

print("\nYour final starting XI:")
for _, player in current_starting_XI.iterrows():
    print(f"{player['Position']}, {player['Name']}, {player['fantasy_points']} points")

print("\nYour final reserves:")
for _, player in current_reserves.iterrows():
    print(f"{player['Position']}, {player['Name']}, {player['fantasy_points']} points")

print("\nCongratulations, your team is now complete!")
