import numpy as np
import pandas as pd
import os

# Globally set options to display all columns and rows
pd.options.display.max_columns = None
pd.options.display.max_rows = None
pd.options.display.width = 0

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
    # Convert into DataFrame table for display
    data = [col_player.nunique()]
    table = pd.DataFrame(index=[0],
                         columns=['Total Players'],
                         data=[col_player.nunique()])
    print(table)

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
    print("Purchasing Analysis")
    print("--------------------------")
    row_labels = [0]
    data = {
        "Number of Unique Items": num_unique_items,
        "Average Purchase Price": f"${average_purchase_price}",
        "Number of Purchases": total_num_purchases,
        "Total Revenue": f"${total_revenue}"
    }
    data_frame = pd.DataFrame(data=data, index=row_labels)
    print(data_frame)

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
    male_percentage = f"{round((male_count / total_players) * 100, 2)}%"
    female_percentage = f"{round((female_count / total_players) * 100, 2)}%"
    other_percentage = f"{round((other_count / total_players) * 100, 2)}%"

    print("--------------------------")
    print("Gender Demographics")
    print("--------------------------")
    row_labels = [
        "Male",
        "Female",
        "Other / Non-Disclosed"
    ]
    data = {
        "Total Count": [male_count, female_count, other_count],
        "Percentage of Players": [male_percentage, female_percentage, other_percentage]
    }
    data_frame = pd.DataFrame(data=data,
                              index=row_labels)
    print(data_frame)
    return male_count, female_count, other_count

def get_age_demographics(csv_data):
    """
    Returns the following data:
        Bins for ages
        Categories of existing players using age bins
        Numbers and percentages by age group
        Summary data frame to hold results
        Display Age Demographics Table
    :return:
    """
    print("--------------------------")
    print("Age Demographics")
    print("--------------------------")
    # Initialize the data frame with the csv data
    data_frame = pd.DataFrame(data=csv_data)

    # Define bins for ages and add a new column for the Bins
    bins = [-np.inf, 10, 14, 19, 24, 29, 34, 39, np.inf]
    data_frame["Bins"] = pd.cut(data_frame["Age"], bins=bins)

    # Drop duplicates based on SN
    data_frame = data_frame.drop_duplicates(subset="SN", keep="first")
    total_players = len(data_frame.index)

    # Sort data by Bins column and get the counts of each bin
    bin_data = data_frame["Bins"].value_counts().sort_index().to_frame()

    # Calculate percentages for each Bin
    percentages = []
    for count in bin_data["Bins"].unique():
        percentage = f"{round((count / total_players) * 100, 2)}%"
        percentages.append(percentage)

    # Append percentages as a new column
    bin_data["Percentage of Players"] = percentages

    # Rename Bins column to Total Count
    bin_data.rename(columns={"Bins": "Total Count"},
                    inplace=True)
    print(bin_data)

def get_purchasing_analysis_gender(csv_data):
    # Group by SN and Gender and separate into male, female, and other tables
    player_gender_group_by = csv_data.groupby(["SN", "Gender"]).head()
    male = player_gender_group_by[player_gender_group_by["Gender"].str.contains("Male")]
    female = player_gender_group_by[player_gender_group_by["Gender"].str.contains("Female")]
    other = player_gender_group_by[player_gender_group_by["Gender"].str.contains("Other / Non-Disclosed")]

    # Pull out the unique count of male, female, and other
    unique_male_count = male.nunique()["SN"]
    unique_female_count = female.nunique()["SN"]
    unique_other_count = other.nunique()["SN"]

    # Calculations
    purchase_count = [
        female["Price"].count(),
        male["Price"].count(),
        other["Price"].count()
    ]

    average_purchase_price = [
        "${:.2f}".format(female["Price"].mean()),
        "${:.2f}".format(male["Price"].mean()),
        "${:.2f}".format(other["Price"].mean())
    ]

    total_purchase_value = [
        "${:.2f}".format(female["Price"].sum()),
        "${:.2f}".format(male["Price"].sum()),
        "${:.2f}".format(other["Price"].sum())
    ]

    average_purchase_total_per_person_by_gender = [
        "${:.2f}".format(female["Price"].sum() / unique_female_count),
        "${:.2f}".format(male["Price"].sum() / unique_male_count),
        "${:.2f}".format(other["Price"].sum() / unique_other_count)
    ]

    # Convert calculations into a DataFrame
    row_labels = [
        "Female",
        "Male",
        "Other / Non-Disclosed"
    ]
    data = {
        "Purchase Count": purchase_count,
        "Average Purchase Price": average_purchase_price,
        "Total Purchase Value": total_purchase_value,
        "Avg Total Purchase per Person": average_purchase_total_per_person_by_gender
    }

    data_frame = pd.DataFrame(data=data,
                              index=row_labels)
    print(data_frame)

def print_final_report():
    csv_data = read_csv_file()
    get_player_count(csv_data)
    get_purchasing_analysis(csv_data)
    get_gender_demographics(csv_data)
    get_purchasing_analysis_gender(csv_data)
    get_age_demographics(csv_data)


# Entry point where the script will execute
if __name__ == "__main__":
    print_final_report()
