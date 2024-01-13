import pandas as pd 
import plotly.express as px

#px.data_transformers.enable('json')

url = "https://github.com/byuidatascience/data4python4ds/raw/master/data-raw/mpg/mpg.csv"
mpg = pd.read_csv(url)

chart = px.scatter(mpg,  
    x="displ", 
    y="hwy",
    title = "Car's Engine size and Car's Fuel Efficiency",
    color = "class",
    labels ={"displ": "Car Engine Size, litres", 
             "hwy": "Miles per Gallon (mpg)", 
             "class": "Kind"},
)

chart.show()

print(mpg
  .head(5)
  .filter(["manufacturer", "model","year", "hwy"])
  .to_markdown(index=False))