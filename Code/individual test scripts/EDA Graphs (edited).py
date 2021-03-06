import os
import pandas as pd
from matplotlib import pyplot as plt

try:                                                                                                                        #Following code (try/except clauses) searches for this script, and then changes the current working directory to the folder that houses it.
    start = '/Users'                                                                                                        #Code from https://stackoverflow.com/questions/43553742/finding-particular-path-in-directory-in-python
    for dirpath, dirnames, filenames in os.walk(start):
        for filename in filenames:
            if filename == "US_Accidents_Dec19.csv":
                filename = os.path.join(dirpath, filename)
                os.chdir(dirpath)
except:
    pass


try:
    start1 = "C:\\Users"
    for dirpath, dirnames, filenames in os.walk(start1):
        for filename in filenames:
            if filename == "US_Accidents_Dec19.csv":
                filename = os.path.join(dirpath, filename)
                os.chdir(dirpath)
except:
    pass

accidents = pd.read_csv('US_Accidents_Dec19.csv')

accidents.describe()

plt.hist(accidents['Temperature(F)'],bins=50,range=[-10,120]) #fairly evenly distributed histogram; most accidents occur around the 60-70 degree mark
plt.title('Temperature Histogram')
plt.show()

accidents['Start_Time'] = pd.to_datetime(accidents['Start_Time']) #bifurcated histogram, with most accidents occuring during morning and evening rush hour
plt.hist(accidents['Start_Time'].dt.time,bins=100)
plt.title('Accident Times')
plt.show()

accidents.boxplot(column='Temperature(F)',by='Severity',showfliers=False) #accidents all seem to hover around 60-70 degree weather. some of the outlier temperatures seem way too high and way too low, so I excluded from the graph

accidents.boxplot(column='Visibility(mi)',by='Severity') #no clear pattern here

accidents.boxplot(column='Precipitation(in)',by='Severity').set_yscale('log') #no clear pattern here


accidents['End_Time'] = pd.to_datetime(accidents['End_Time'])
accidents['Start_Time'] = pd.to_datetime(accidents['Start_Time'])
accidents['Time_Delta'] = accidents['End_Time']-accidents['Start_Time'] #time elapsed from start of accident to time it was cleared

accidents['Time_Delta'] = accidents['Time_Delta'].astype('timedelta64[m]') #converts time elapsed to minutes

plt.hist(accidents['Time_Delta'],bins=25,range=[0,400]) #most accidents are cleared within an hour. heavily right-skewed data
plt.title('Time Delta Histogram')
plt.show()

accidents.boxplot(column='Time_Delta',by='Severity').set_yscale('log') #the most severe accidents seem to take the longest time to clear

######################### extra
### fill the missing value
df1 = accidents.reindex(list(range(accidents.index.min(), accidents.index.max() + 1)), fill_value=0)
print(df1)

### Sort the df ascending and not ascending
print(df1.sort_index())
print(df1.sort_index(ascending=False))


### start time as the
def get_acc_cnt(df_in, state_name, time_str):
    return df_in.loc[lambda df: df["Start_Time"].str.startswith(time_str) &
                                (df["State"] == state_name), :].shape[0]


print("Ohio in 2016-02-08: ", get_acc_cnt(accidents, 'OH', "2016-02-08"))
print("Ohio in 2016-02: ", get_acc_cnt(accidents, 'OH', "2016-02"))

state_list = accidents['State'].unique()


### acquire car accident information from assigned state on assigned date
def get_acc_timelist(df_in, state_name, select="day"):
    if select == "year":
        strlen = 4
    elif select == "month":
        strlen = 7
    else:
        strlen = 10

    df_state = df_in.loc[accidents["State"] == "OH", :]
    time_list = df_state["Start_Time"].str[0:strlen].unique()
    cnt_list = []
    for time_str in time_list:
        cnt_list.append(get_acc_cnt(df_state, state_name, time_str))

    return time_list, cnt_list


get_acc_timelist(accidents, "OH", "month")

######################### extra
