import pandas as pd 
import plotly.express as px

url = "https://github.com/byuidatascience/data4names/raw/master/data-raw/names_year/names_year.csv"
mpg = pd.read_csv(url)


# How does your name at your birth year compare to its use historically?
chart1 = px.line(mpg.query('name == "Rebekah" or name == "Rebecca" or name == "Rebecka" or name == "Rebeca" or name == "Rebeccah" or name == "Rebekka"'),
    x = "year",
    y = "Total",
    color = "name"
    )

chart1.add_vline(
    x=2003,
    line_width= 3,
    line_dash="dash",
    annotation_text= "My Birth"
    )


chart12 = px.bar(mpg.query('name == "Rebekah" or name == "Rebecca" or name == "Rebecka" or name == "Rebeca" or name == "Rebeccah" or name == "Rebekka"'),
    x = "name",
    y = "Total",
    color = "name"
    )



chart2 = px.line(mpg.query('name == "Rebecca"'),
    x = "year",
    y = "WA",
    color = "name",
    )

chart2.add_vline(
    x=2003,
    line_width= 3,
    line_dash="dash",
    annotation_text= "My Birth"
    )



"""
class beccaStates:
    def __init__(self, states):
        self.graph = []
        self.states = [
            "AK", "AL", "AR", "AZ",
            "CA", "CO", "CT",
            "DC", "DE",
            "FL", "GA", "HI",
            "IA", "ID", "IL", "IN",
            "KS", "KY",
            "LA",
            "MA", "MD", "ME", "MI", "MO", "MS", "MT", 
            "NC", "ND", "NE", "NH", "NJ", "NM", "NV", "NY",
            "OH", "OK", "OR",
            "PA", "RI",
            "SC", "SD",
            "TN", "TX",
            "UT", 
            "VA", "VT",
            "WA", "WI", "WV", "WY"]

    def make_graph(self, states):
        for i in states:
            chart = px.line(mpg.query('name == "Rebecca"'),
                x = "year",
                y = i,
            )
            self.graph.append(chart)

print(mpg.query('name == "Rebecca"').head())
"""
# If you talked to someone named Brittany on the phone, what is your guess of his or her age? What ages would you not guess?
chart2 = px.line(mpg.query('name == "Brittany"'),
    x = "year",
    y = "Total",
    title = "Uses of Brittany Throughout Time",
    labels={"year": "Year",
        "Total": "Total Uses of Name"},
    )

chart2.add_hline(
    y=6827,
    line_width= 3,
    line_dash="dash",
    annotation_text= "Average Line"
    )

chart2.add_hline(
    y=1353,
    line_width= 3,
    line_dash="dash",
    annotation_text= "Median Line"
    )

chart2.add_hrect(
    y0 = 27000,
    y1 = 33000,
    line_width=0,
    fillcolor = "red",
    opacity=0.2
)
chart2.add_hrect(
    y0 = 12000,
    y1 = 27000,
    line_width=0,
    fillcolor = "orange",
    opacity=0.2
)
chart2.add_hrect(
    y0 = 12000,
    y1 = 1353,
    line_width=0,
    fillcolor = "yellow",
    opacity=0.2
)
chart2.add_hrect(
    y0 = 1353,
    y1 = 640,
    line_width=0,
    fillcolor = "green",
    opacity=0.2
)
chart2.add_hrect(
    y0 = 640,
    y1 = 5,
    line_width=0,
    fillcolor = "blue",
    opacity=0.2
)
chart2.add_hrect(
    y0 = 5,
    y1 = -100,
    line_width=0,
    fillcolor = "purple",
    opacity=0.2
)


brittany = mpg.query('name == "Brittany"')
brittany_m = brittany['Total'].median()
print(brittany_m)
chart3 = px.box(mpg.query('name == "Brittany"'),
    y = "Total",
    title = "Uses of Brittany Throughout Time",
    labels={"year": "Year",
        "Total": "Total Uses of Name"},)
#chart3.show()

# Mary, Martha, Peter, and Paul are all Christian names. From 1920 - 2000, compare the name usage of each of the four names. What trends do you notice?
chart4 = px.line(mpg.query('name == "Mary" or name == "Martha" or name == "Peter" or name == "Paul"'),
    x = "year",
    y = "Total",
    color = "name",
    title = "Uses of Biblical Names by Year",
    labels={"year": "Year",
        "Total": "Total Uses of Name"},
    )

chart4.add_vline(
    x=1956,
    line_width= 3,
    line_dash="dash",
    )

# Think of a unique name from a famous movie. Plot the usage of that name and see how changes line up with the movie release. Does it look like the movie had an effect on usage?
# Luke, Leia, Anakin, Glinda, Dorothy, Neo, Luna, 
# Belle, Flynn (Rider), Elsa, Violet, Ariel, Tiana, Jasmine, Aurora, 
disney = px.line(mpg.query('name == "Flynn" or name == "Elsa" or name == "Ariel" or name == "Tiana"'),
    x = "year",
    y = "Total",
    color = "name",
    facet_col="name",
    facet_col_wrap=2
    )
#disney.show()

aurora = px.line(mpg.query('name == "Belle"'),
    x = "year",
    y = "Total",
    title = "Uses of Belle's name by Year",
    labels={"year": "Year",
        "Total": "Total Uses of Name"},
    )

aurora.add_vline(
    x=1991,
    line_width= 3,
    line_dash="dash",
    annotation_text= "1991"
    )

#aurora.show()

#print(mpg.query('name == "Oliver"').sum())
felisha = px.line(mpg.query('name == "Felisha"'),
    x = "year",
    y = "Total"
                  )

felisha.show()