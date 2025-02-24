import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = ['chicago', 'new york city', 'washington']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

def get_filters():
    """Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print("Hello! Let's explore some US bikeshare data!")

    # get user input for city (chicago, new york city, washington). Use a while loop to handle invalid inputs.
    while True:
        city =input("Please enter the city you'd like to display data for:\n Choices: Chicago, New York City, Washington\n").lower()
        if city in cities:
            break
        else:
            print('Please enter valid city')

    # get user input for month (all, january, february, ... , june)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        choice = input("Would you like to filter the data by month, day, none?\n").lower()
        if choice == 'month':
            month = input("Please enter the month you'd like to display data for. If you do not want to filter by month enter 'all'. \nChoices: All, January, February, March, April, May, June\n").lower()
            day = 'all'
            if month in months:
                break
            else:
                print('Please enter a valid month')
        elif choice == 'day':
            day = input("Please enter the day of the week you'd like to display data for. If you do not want to filter by day enter 'all'. \nChoices: All, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday\n").lower()#PB
            month = 'all'
            if day in days:
                break
            else:
                print('Please enter a valid day')
        elif choice == 'none':
            month = 'all'
            day = 'all'
            break
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
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

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


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Popular Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month from start time column to create month column
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]

    # change number to months
    if popular_month == 1:
        popular_month = "January"
    elif popular_month == 2:
        popular_month = "February"
    elif popular_month == 3:
        popular_month = "March"
    elif popular_month == 4:
        popular_month = "April"
    elif popular_month == 5:
        popular_month = "May"
    elif popular_month == 6:
        popular_month = "June"
    print('Most Common Month: \n', popular_month)

    # display the most common day of the week
    # extract day from the Start Time column to create a day column
    popular_day = df['day_of_week'].mode()[0]
    print('Most Common Day of the Week: \n', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour #PB
    popular_hour = df['hour'].mode()[0] #PB
    if popular_hour < 12:
        print('Most Common Start Hour: \n', popular_hour, ' AM')
    elif popular_hour >= 12:
        if popular_hour > 12:
            popular_hour -= 12
        print('Most Common Start Hour: \n', popular_hour, ' PM')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("Most Common Start Station: \n", popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("Most Common End Station: \n", popular_end_station)

    # display most frequent combination of start station and end station trip
    combo_station = df['Start Station'] + " to " +  df['End Station']
    common_combo_station = combo_station.mode()[0]
    print("Most Common Trip from Start to End:\n {}".format(common_combo_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    minute, second = divmod(total_duration, 60)
    hour, minute = divmod(minute, 60)
    print("The Total Travel Time is {} Hr, {} Min, and {} Sec.".format(hour, minute, second))

    # display mean travel time
    average_duration = round(df['Trip Duration'].mean())
    minute, second = divmod(average_duration, 60)
    if minute> 60:
        hour, minute = divmod(minute, 60)
        print('The Average Travel Time is {} Hr, {} Min, and {} Sec.'.format(hour, minute, second))
    else:
        print('The Average Trip Duration is {} Min and {} Sec.'.format(minute, second))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    user_types = df['User Type'].value_counts()
    print("User Type Counts:\n", user_types)

    # display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print(' ' * 40)
        print('User Gender Counts:')
        print(gender)
    except:
        print('User Gender Counts:\nSorry, no gender data available for {} City'.format(city.title()))

    # display earliest, most recent, and most common year of birth
    try:
        earliest = df['Birth Year'].min() #Oldest birth year
        recent = df['Birth Year'].max() #Youngest birth Year
        common = df['Birth Year'].mode() #This gives the Common Birth Year
        print(' ' * 40)
        print('User Birth Year Counts:')
        print('Oldest User(s) Birth Year: ', int(earliest))
        print('Youngest User(s) Birth Year: ', int(recent))
        print('Most Common Birth Year: ', int(common))
    except:
        print('User Birth Year Counts:\nSorry, no birth year data available for {} City'.format(city.title()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def individual_data(df):
    # ask user if they want to see individual trip data.
    start_data = 0
    end_data = 5
    df_length = len(df.index)

    while start_data < df_length:
        raw_data = input("\nWould you like to see individual trip data? Enter 'yes' or 'no'.\n")
        if raw_data.lower() == 'yes':

            print("\nDisplaying only 5 rows of data.\n")
            if end_data > df_length:
                end_data = df_length
            print(df.iloc[start_data:end_data])
            start_data += 5
            end_data += 5
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        print("You selected {}, {}, and {}.".format(city.title(), month.title(), day.title()))

        df = load_data(city, month, day)
        # print(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        individual_data(df)

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
