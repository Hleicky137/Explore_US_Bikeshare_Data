import time
import pandas as pd
import datetime as dt

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
MONTH_DATA = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
DAYS_DATA = ['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'all']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Which city's data would you like to explore? Chicago, New york city or Washington? : ").lower()
        if city not in CITY_DATA:
            print("Please input a valid city name.")
            continue
        else:
            break
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Which Month would you like to explore? January, February, March, April, May, "
                      "June or all : ").lower()
        if month not in MONTH_DATA:
            print("Please enter a valid month.")
            continue
        else:
            break
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input(
            "Which Day would you like to explore ? Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday?"
            " or all : ").lower()
        if day not in DAYS_DATA:
            print("Please enter a valid day.")
            continue
        else:
            break
    print('-' * 40)
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime("%A")

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

        # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month != "all":
        freq_month = month.title()
    else:
        freq_month = df['month'].mode()[0]
    print(f"The most frequent month was: {freq_month}")
    print("\n")
    # display the most common day of week
    if day != "all":
        freq_day = day.title()
    else:
        freq_day = df['day_of_week'].mode()[0]
    print(f"The most frequent day was: {freq_day} ")
    print("\n")
    # display the most common start hour
    # We create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # We get the mode for this column
    freq_hour = df['hour'].mode()[0]
    print(f"The most frequent hour was: {freq_hour}:00")
    print("\n")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    comm_str_stn = df['Start Station'].mode()[0]
    print(f"The Most commonly used start station was :{comm_str_stn}")
    print("\n")
    # display most commonly used end station
    comm_end_stn = df['End Station'].mode()[0]
    print(f"The Most commonly used end station was : {comm_end_stn}")
    print("\n")
    # display most frequent combination of start station and end station trip
    most_freq_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f"The Most Frequent trip was between {most_freq_trip[0]} and {most_freq_trip[1]}")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time = int(df['Trip Duration'].sum())
    # Turn the total travel time to minutes and seconds using timedelta
    total_travel_time = str(dt.timedelta(seconds=travel_time))
    print(f"The total travel time was {total_travel_time}")
    # display mean travel time
    # We convert the mean travel time to minutes and seconds using timedelta
    mean_travel_time_sec = int(df['Trip Duration'].mean())
    mean_travel_time = str(dt.timedelta(seconds=mean_travel_time_sec))
    print(f"The mean travel time was {mean_travel_time}")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)
    print()
    # Display counts of gender
    if 'Gender' in df:
        gender_types = df['Gender'].value_counts()
        print(gender_types)
    else:
        print("No Gender data available")
    print()
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        years = df['Birth Year']
        print(f"The earliest birth year was {years.min()}")
        print(f"While the most recent birth year was {years.max()}")
        print(f"The most common birth year was : {years.mode()}")
        print("\nThis took %s seconds." % (time.time() - start_time))
    else:
        print("No Birth year data available")
        print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        # Prompt user to display raw inputs on screen
        starting_row = 0
        display_raw_data = True
        while display_raw_data:
            user_input = input('Would like to view some of the raw data? please input yes or no: ').lower()
            if user_input == 'yes':
                print(df.iloc[starting_row:starting_row + 5])
                starting_row += 5
            elif user_input == "no":
                display_raw_data = False
            else:
                print("Please enter a valid input. \n")

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
