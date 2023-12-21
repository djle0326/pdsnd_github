#import package
import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_user_filters():
    """
    Prompts the user to specify a city, month, and day for data analysis.

    This function asks the user to specify a city (from available options), a month, 
    and a day of the week. If the user wishes not to filter by month or day, they can 
    choose 'all' for either option.

    Returns:
        city (str): Name of the city to analyze.
        month (str): Name of the month to filter by, or "all" for no filter.
        day (str): Name of the day of week to filter by, or "all" for no filter.
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    while city not in ['chicago', 'new york city', 'washington']:
        city = input(
            "Enter the city to analyze (chicago, new york city, washington): ").lower()
        if city not in ['chicago', 'new york city', 'washington']:
            print("Invalid input. Please enter a valid city name.")

    # TO DO: get user input for month (all, january, february, ... , june)
    month = ''
    months = ('january', 'february', 'march', 'april', 'may', 'june', 'all')
    while month not in months:
        month = input(
            "Enter the month to filter by (january, february, ... , june, all): ").lower()
        if month not in months:
            print("Invalid input. Please enter a valid month name or 'all'.")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    days = ['monday', 'tuesday', 'wednesday', 'thursday',
            'friday', 'saturday', 'sunday', 'all']
    while day not in days:
        day = input(
            "Enter the day of week to filter by (monday, tuesday, ... sunday, all): ").lower()
        if day not in days:
            print("Invalid input. Please enter a valid day of the week or 'all'.")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # Filter by month if applicable
    if month != 'all':
        # Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_index = months.index(month.lower()) + 1

        # Filter by month using the query method
        df = df.query(f'month == {month_index}')

    # Filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    # Mapping from month number to month name
    month_names = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                   7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    popular_month_name = month_names[popular_month]
    print('Most Popular Month:', popular_month_name)

    # Rest of your code...

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print(f"Most Commonly Used Start Station: {popular_start_station}")

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print(f"Most Commonly Used End Station: {popular_end_station}")

    # TO DO: display most frequent combination of start station and end station trip
    popular_station_combination = df.groupby(
        ['Start Station', 'End Station']).size().idxmax()
    print(
        f"Most Frequent Combination of Start Station and End Station: {popular_station_combination}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"Total Travel Time: {total_travel_time} seconds")

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f"Mean Travel Time: {mean_travel_time} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of User Types:")
    for user_type, count in user_types.items():
        print(f"  {user_type}: {count}")

    # TO DO: Display counts of gender
    # This is wrapped in a try-except block in case the data does not have a Gender column
    try:
        gender_counts = df['Gender'].value_counts()
        print("\nCounts of Gender:")
        for gender, count in gender_counts.items():
            print(f"  {gender}: {count}")
    except KeyError:
        print("\nGender data not available for this city.")

    # TO DO: Display earliest, most recent, and most common year of birth
    # This is also wrapped in a try-except block in case the data does not have a Birth Year column
    try:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        print("\nEarliest Year of Birth:", earliest_year)
        print("Most Recent Year of Birth:", most_recent_year)
        print("Most Common Year of Birth:", most_common_year)
    except KeyError:
        print("\nBirth Year data not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """Displays 5 lines of raw data at a time upon user request."""
    print('\nWould you like to view individual trip data?')
    start_loc = 0
    while input("Type 'yes' to view more raw data, or any other key to continue: ").lower() == 'yes':
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5


def main():
    while True:
        city, month, day = get_user_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Add raw data display
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
