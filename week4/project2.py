import pandas as pd 
import plotly.express as px
import numpy as np
from scipy import stats

import altair as alt

# url = "https://github.com/byuidatascience/data4missing/raw/master/data-raw/flights_missing/flights_missing.json"
file = open("./flights_missing.json")
data = pd.read_json(file)

# 1 - Find missing values 
"""
I found out all the blank values are from the airport_name (56 of them) 
so I only have to find the blank values from airport_name
"""
print(data.query('airport_name == ""').filter(["airport_name", "num_of_delays_late_aircraft", "month"]).head())
print(data.query('num_of_delays_late_aircraft == -999').filter(["airport_name", "num_of_delays_late_aircraft", "month"]).head())
print(data.query('month == "n/a"').filter(["airport_name", "num_of_delays_late_aircraft", "month"]).head())

data.airport_name = data.airport_name.replace({"": "NaN"})
data.num_of_delays_late_aircraft = data.num_of_delays_late_aircraft.replace({-999: "NaN"})
data.month = data.month.replace({"n/a": "NaN"})


print(data.filter(["airport_name", "num_of_delays_late_aircraft", "month"]).head())

# 2 - Which airport has the worst delays?
data = data.assign(num_of_delays_total_ratio = lambda x: x.num_of_delays_total / x.num_of_flights_total)
airport_data = data.groupby(["airport_code"])[['num_of_flights_total','num_of_delays_total']].sum().reset_index()
airport_data = airport_data.assign(proportion_delayed_flights = lambda x: x.num_of_delays_total / x.num_of_flights_total)
print(airport_data.value_counts())

#airport_delay_time = data.groupby(["airport_code"])['minutes_delayed_total'].mean().reset_index()
#airport_delay_time.rename(columns={"minutes_delayed_total": "minutes_delayed_mean"}, inplace=True)
#airport_delay_time = airport_delay_time.assign(hours_delayed_mean = lambda x: x.minutes_delayed_mean / 60)
#print(airport_delay_time.value_counts())

data = data.assign(minutes_delayed_total_ratio = lambda x: x.minutes_delayed_total / x.num_of_flights_total)
data = data.assign(hours_delayed_total_ratio = lambda x: (x.minutes_delayed_total / x.num_of_flights_total) / 60)

time_delay = px.box(data,
    x = "airport_code",
    y = "minutes_delayed_total_ratio",
    color = "airport_code",
    title = "Boxplot of Minutes Delayed",
    labels= {
        "airport_code":"Airport Code",
        "minutes_delayed_total_ratio":"Minutes Delayed per Flight"
    }
)
#time_delay.show()

delay2 = px.box(data,
    x = "airport_code",
    y = "num_of_delays_total_ratio",
    color = "airport_code",
    title = "Boxplot of delays at Airports by total flights",
    labels= {
        "airport_code":"Airport Code",
        "num_of_delays_total_ratio":"Total Delays by Total Flights Ratio"
    }
)

#delay2.show()

delay1 = px.box(data,
    x = "airport_code",
    y = "num_of_delays_total",
    color = "airport_code",
    title = "Boxplot of Total Delays at Airports",
    labels= {
        "airport_code":"Airport Code",
        "num_of_delays_total":"Total Delays"
    }
)
#delay1.show()

total_flights = px.bar(data,
    x = "airport_code",
    y = "num_of_flights_total",
    color = "airport_code",
    title = "Boxplot of Total Flights at Airports",
    labels= {
        "airport_code":"Airport Code",
        "num_of_flights_total":"Total Flights"
    }
)
#total_flights.show()

delay2 = px.box(data,
    x = "airport_code",
    y = "minutes_delayed_total",
    color = "airport_code",
    title = "Boxplot of Total Delays at Airports",
    labels= {
        "airport_code":"Airport Code",
        "minutes_delayed_total":"Total Minutes Delayed"
    }
)
#delay2.show()

# 3 - Month to fly
months = px.histogram(data.query('month != "NaN"'),
    x = "minutes_delayed_total_ratio",
    y = "num_of_delays_total_ratio",
    facet_col="month",
    facet_col_wrap=4,
    color = "month",
    title = "Boxplot of Total Delays at Airports",
    labels= {
        "minutes_delayed_total_ratio":"Minutes Delayed",
        "month": "Months",
        "num_of_delays_total_ratio":"Total Delays per Flight"
    }
)
#months.show()

months2 = px.histogram(data.query('month != "NaN"'),
    x = "minutes_delayed_total_ratio",
    y = "num_of_delays_total_ratio",
    facet_col="month",
    facet_row="airport_code",
    color = "airport_code",
    title = "Boxplot of Total Delays at Each Airport",
    labels= {
        "minutes_delayed_total_ratio":"",
        "month": "Months",
        "num_of_delays_total_ratio":"",
        "airport_code": "Airport Code",
        "months=":""
    }
)
#months2.show()

# 4 - Total weather
data.rename(columns={"num_of_delays_weather": "num_of_delays_severe_weather"}, inplace=True)

def mw_calc(x): 
    if x.num_of_delays_late_aircraft == "NaN":
        if x.month in ["April", "May", "June", "July", "August"]:
            return x.num_of_delays_nas * 0.4 
        else:
            return x.num_of_delays_nas * 0.65
    else:
        if x.month in ["April", "May", "June", "July", "August"]:
            return x.num_of_delays_nas * 0.4 + x.num_of_delays_late_aircraft * 0.3
        else:
            return x.num_of_delays_nas * 0.65 + x.num_of_delays_late_aircraft * 0.3

data["num_of_delays_mild_weather"] = data.apply(mw_calc, axis=1)
data = data.assign(num_of_delays_total_weather = lambda x: x.num_of_delays_mild_weather + x.num_of_delays_severe_weather)
data["num_of_delays_late_aircraft"] = data.apply(lambda x: (x.num_of_delays_mild_weather + x.num_of_delays_severe_weather) / 2 if x.num_of_delays_late_aircraft == "NaN" else x.num_of_delays_late_aircraft, axis=1)

print(data.filter(["airport_code", "num_of_delays_total_weather", "num_of_delays_mild_weather", "num_of_delays_late_aircraft"]).head())


# 5 - Show weather
data = data.assign(num_of_delays_total_weather_proportion = lambda x: x.num_of_delays_total_weather / x.num_of_flights_total)
weather_graph = px.bar(data,
    x = "airport_code",
    y = "num_of_delays_total_weather_proportion",
    color = "airport_code",
    title = "Airport Delays by Mild Weather",
    labels= {
        "num_of_delays_total_weather_proportion": "Delays by Total Weather",
        "airport_code": "Airport Code"
    }
)
#weather_graph.show()

weather_graph2 = px.bar(data,
    x = "airport_code",
    y = "num_of_delays_total_weather",
    color = "airport_code",
    title = "Airport Delays by Total Weather per Flight",
    labels= {
        "num_of_delays_total_weather": "Delays by Total Weather",
        "airport_code": "Airport Code"
    }
)
#weather_graph2.show()
print("Mean: ")
print(data.query('airport_code == "SFO"').filter(["num_of_delays_total_weather", "num_of_delays_total"]).mean())
print("\nMedian: ")
print(data.query('airport_code == "SFO"').filter(["num_of_delays_total_weather", "num_of_delays_total"]).median())

weather_median = 1142.05
total_median = 3143.50

print("\nRatio:")
print(f"{round(((weather_median / total_median) * 100), 2)}% of delays in SFO are caused by Weather")

file.close()