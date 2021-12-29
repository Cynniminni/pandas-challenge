import pandas
import pandas as pd
import os

# Globally set options to display all columns and rows
pandas.options.display.max_columns = None
pandas.options.display.max_rows = None
pandas.options.display.width = 0

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
    table = pandas.DataFrame(index=[0],
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
    data_frame = pandas.DataFrame(data=data, index=row_labels)
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
    data_frame = pandas.DataFrame(data=data,
                                  index=row_labels)
    print(data_frame)
    return male_count, female_count, other_count

def get_purchasing_analysis_gender(csv_data, male_count, female_count, other_count):
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
    male_purchase_count = 0
    female_purchase_count = 0
    other_purchase_count = 0

    # Total purchase value by gender
    male_total_purchase = 0
    female_total_purchase = 0
    other_total_purchase = 0

    for index, row in csv_data.iterrows():
        gender = row["Gender"]
        price = row["Price"]

        if gender == "Male":
            male_purchase_count += 1
            male_total_purchase += price
        elif gender == "Female":
            female_purchase_count += 1
            female_total_purchase += price
        elif gender == "Other / Non-Disclosed":
            other_purchase_count += 1
            other_total_purchase += price

    # Average purchase price by gender
    total_purchase_all = male_total_purchase + female_total_purchase + other_total_purchase
    male_average_price = f"${round(male_total_purchase / male_purchase_count, 2)}"
    female_average_price = f"${round(female_total_purchase / female_purchase_count, 2)}"
    other_average_price = f"${round(other_total_purchase / other_purchase_count, 2)}"

    # Average total purchase per person, by gender
    male_average_person = f"${round(male_total_purchase / male_count, 2)}"
    female_average_person = f"${round(female_total_purchase / female_count, 2)}"
    other_average_person = f"${round(other_total_purchase / other_count, 2)}"

    # Formatting
    male_total_purchase = f"${round(male_total_purchase, 2)}"
    female_total_purchase = f"${round(female_total_purchase, 2)}"
    other_total_purchase = f"${round(other_total_purchase, 2)}"

    print("--------------------------")
    print("Purchase Analysis")
    print("--------------------------")
    row_labels = [
        "Female",
        "Male",
        "Other / Non-Disclosed"
    ]
    data = {
        "Purchase Count": [female_purchase_count, male_purchase_count, other_purchase_count],
        "Average Purchase Price": [female_average_price, male_average_price, other_average_price],
        "Total Purchase Value": [female_total_purchase, male_total_purchase, other_total_purchase],
        "Avg Total Purchase per Person": [female_average_person, male_average_person, other_average_person]
    }
    data_frame = pandas.DataFrame(data=data,
                                  index=row_labels)
    print(data_frame)

def get_age_demographics():
    """
    Returns the following data:
        Bins for ages
        Categories of existing players using age bins
        Numbers and percentages by age group
        Summary data frame to hold results
        Display Age Demographics Table
    :return:
    """
    pass

def print_final_report():
    csv_data = read_csv_file()
    get_player_count(csv_data)
    get_purchasing_analysis(csv_data)
    male_count, female_count, other_count = get_gender_demographics(csv_data)
    get_purchasing_analysis_gender(csv_data, male_count, female_count, other_count)
    get_age_demographics()


# Entry point where the script will execute
if __name__ == "__main__":
    print_final_report()
