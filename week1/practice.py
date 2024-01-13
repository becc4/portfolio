# We are using plotly Express
import plotly.express as px
data = px.data.iris()
#print(data.head())

px.scatter(data,  x="sepal_width", y="sepal_length", title = "The relationship between sepal width and sepal length").show()