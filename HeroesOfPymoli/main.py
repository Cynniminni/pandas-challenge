import pandas as pd
import os

def read_csv_file():
    """
    Use the pandas module to read the csv file and return it as a DataFrame variable.
    :return:
    """
    current_working_directory = os.getcwd()
    file_path = os.path.join(current_working_directory, "Resources", "purchase_data.csv")
    if os.path.exists(file_path):
        # Read csv file and save it as a DataFrame
        return pd.read_csv(file_path)
    else:
        raise FileNotFoundError(f"File not found at: {file_path}")

def get_player_count(csv_data):
    """
    Returns total number of players.
    :param csv_data:
    :return:
    """
    col_player = csv_data["SN"]
    print("--------------------------")
    print("Player Count")
    print("--------------------------")
    print(f"Total Players: {col_player.nunique()}")

def get_purchasing_analysis(csv_data):
    """
    Returns the following data:
        Number of Unique Items
        Average Purchase Price
        Total Number of Purchases
        Total Revenue
    :return:
    """
    col_item_name = csv_data["Item Name"]
    col_price = csv_data["Price"]

    num_unique_items = col_item_name.nunique()
    average_purchase_price = round(col_price.mean(), 2)
    total_num_purchases = len(col_item_name.index)
    total_revenue = col_price.sum()

    print("--------------------------")
    print("Purchasing Analysis:")
    print("--------------------------")
    print(f"Number of Unique Items: {num_unique_items}")
    print(f"Average Purchase Price: ${average_purchase_price}")
    print(f"Number of Purchases: {total_num_purchases}")
    print(f"Total Revenue: ${total_revenue}")

def get_gender_demographics(csv_data):
    """
    Returns the following data:
        Percentage and Count of Male Players
        Percentage and Count of Female Players
        Percentage and Count of Other / Non-Disclosed
    :param csv_data:
    :return:
    """
    # Get total number of unique players and list of player screen names
    col_player = csv_data["SN"]
    total_players = col_player.nunique()

    # Go through each row and get the player and gender
    player_and_genders = []
    for index, row in csv_data.iterrows():
        player = row["SN"]
        gender = row["Gender"]
        if (player, gender) not in player_and_genders:
            player_and_genders.append((player, gender))

    # Get total counts of male / female / other players
    male_count = 0
    female_count = 0
    other_count = 0
    for player, gender in player_and_genders:
        if gender == "Male":
            male_count += 1
        elif gender == "Female":
            female_count += 1
        elif gender == "Other / Non-Disclosed":
            other_count += 1
        else:
            raise ValueError(f"Invalid gender value: {gender}")

    # Get percentages of male / female / other players
    male_percentage = round((male_count / total_players) * 100, 2)
    female_percentage = round((female_count / total_players) * 100, 2)
    other_percentage = round((other_count / total_players) * 100, 2)

    print("--------------------------")
    print("Gender Demographics")
    print("--------------------------")
    print(f"Male: {male_count} ({male_percentage}%)")
    print(f"Female: {female_count} ({female_percentage}%)")
    print(f"Other / Non-Disclosed: {other_count} ({other_percentage}%)")

def get_purchasing_analysis_gender(csv_data):
    """
    Return the following data by gender (male/female/other):
        Purchase Count
        Average Purchase Price
        Total Purchase Value
        Average Purchase Total per Person by Gender
    :param csv_data:
    :return:
    """
    # Purchase count by gender
    male_purchase_count = None
    female_purchase_count = None
    other_purchase_count = None

    # Average purchase price by gender
    male_average_price = None
    female_average_price = None
    other_average_price = None

    # Total purchase value by gender
    male_total_purchase = None
    female_total_purchase = None
    other_total_purchase = None

    # Average total purchase per person, by gender
    male_average_person = None
    female_average_person = None
    other_average_person = None


def print_final_report():
    csv_data = read_csv_file()
    get_player_count(csv_data)
    get_purchasing_analysis(csv_data)
    get_gender_demographics(csv_data)
    get_purchasing_analysis_gender(csv_data)

# Entry point where the script will execute
if __name__ == "__main__":
    print_final_report()
