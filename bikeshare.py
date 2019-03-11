import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ['chicago', 'new york', 'washington']
    city = input("Please select one from Chicago, New York, or Washington to explore.\n").lower()
    while city not in cities:
        print("Please input the correct city name.")
        city = input().lower()

    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    month = input("Please tell me the month you would like to explore from January to June. Input all if you want to explore data from all months\n").lower()
    while month not in months:
        print("Please input the month from january to june correctly or all.")
        month = input().lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday','all']
    day = input("Please tell me the day of week you would like to explore. Input all if you want to explore all days\n").lower()
    while day not in days:
        print("Please input the day of week correctly or all.")
        day = input().lower()

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['Month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    months = ['january', 'february', 'march', 'april', 'may', 'june']

    # display the most common month
    popular_month_digit = df['Month'].mode()[0]
    popular_month = months[popular_month_digit-1].title()
    popular_month_count = max(df['Month'].value_counts())
    print('The most common month:{}, Count:{}'.format(popular_month, popular_month_count))

    # display the most common day of week
    popular_day = df['Day_of_week'].mode()[0]
    popular_day_count = max(df['Day_of_week'].value_counts())
    print('The most common day of week:{}, Count:{}'.format(popular_day, popular_day_count))

    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['Hour'] = df['Start Time'].dt.hour
    # find the most popular hour
    popular_hour = df['Hour'].mode()[0]
    popular_hour_count = max(df['Hour'].value_counts())
    print('The most popular hour:{}, Count:{}'.format(popular_hour, popular_hour_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['Trip'] = 'From ' + df['Start Station'] + ' to ' + df['End Station']
    popular_trip = df['Trip'].mode()[0]
    print('The most frequent trip:', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Travel Time'] = df['End Time'] - df['Start Time']
    print('total travel time: ', df['Travel Time'].sum())
    # display mean travel time
    print('The mean of travel time: ', df['Travel Time'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The distribution of user type:\n', user_types)

    try:
        # Display counts of gender
        gender = df['Gender'].value_counts()
        print('\nThe distribution of user gender:\n', gender)

        # Display earliest, most recent, and most common year of birthS
        print("\nThe earliest year of birth: ", df['Birth Year'].min())
        print("The most recent year of birth: ", df['Birth Year'].max())
        print("The most common year of birth: ", df['Birth Year'].mode()[0])

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    except KeyError:
        pass


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_raw_data = input('Would you like to see 5 lines of raw data?\n').lower()
        if show_raw_data == 'yes':
            print(df.head())
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
