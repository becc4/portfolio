import pandas as pd 
import plotly.express as px
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB, CategoricalNB, ComplementNB, GaussianNB, MultinomialNB
from sklearn.metrics import accuracy_score

from sklearn import metrics
import matplotlib.pyplot as plt

url = "https://github.com/byuidatascience/data4dwellings/raw/master/data-raw/dwellings_ml/dwellings_ml.csv"
data = pd.read_csv(url)

"""
Normalization
"""
all_columns = [
    'abstrprd', 'livearea', 'finbsmnt',
    'basement', 'yrbuilt', 'totunits',
    'stories', 'nocars', 'numbdrm',
    'numbaths', 'sprice', 'deduct',
    'netprice', 'tasp', 'smonth',
    'syear', 'condition_AVG', 'condition_Excel',
    'condition_Fair', 'condition_Good', 'condition_VGood',
    'quality_A', 'quality_B', 'quality_C', 'quality_D',
    'quality_X', 'gartype_Att', 'gartype_Att/Det',
    'gartype_CP', 'gartype_Det', 'gartype_None',
    'gartype_att/CP', 'gartype_det/CP', 'arcstyle_BI-LEVEL',
    'arcstyle_CONVERSIONS', 'arcstyle_END UNIT', 'arcstyle_MIDDLE UNIT',
    'arcstyle_ONE AND HALF-STORY', 'arcstyle_ONE-STORY', 'arcstyle_SPLIT LEVEL',
    'arcstyle_THREE-STORY', 'arcstyle_TRI-LEVEL', 'arcstyle_TRI-LEVEL WITH BASEMENT',
    'arcstyle_TWO AND HALF-STORY', 'arcstyle_TWO-STORY', 'qualified_Q',
    'qualified_U', 'status_I', 'status_V'
    ]
std_scale = preprocessing.StandardScaler().fit(data[all_columns])
df_std = std_scale.transform(data[all_columns])

minmax_scale = preprocessing.MinMaxScaler().fit(data[all_columns])
df_minmax = minmax_scale.transform(data[all_columns])

"""
1. 
    Create 2-3 charts that evaluate potential relationships 
    between the home variables and before1980
"""
#print(data.info())
data = data.assign(before1980 = lambda x: x.yrbuilt > 1980)
#print(data.filter(["before1980", "yrbuilt"]).head())

"""
'condition_AVG', 'condition_Excel', 'condition_Fair', 
'condition_Good', 'condition_VGood', 
"""

condition = [
    'abstrprd', 'livearea', 'finbsmnt',
    'basement', 'yrbuilt', 'totunits',
    'stories', 'nocars', 'numbdrm',
    'numbaths', 'sprice', 'deduct',
    'netprice', 'tasp', 'smonth',
    'syear', 'condition_AVG', 'condition_Excel',
    'condition_Fair', 'condition_Good', 'condition_VGood',
    'quality_A', 'quality_B', 'quality_C', 'quality_D',
    'quality_X', 'gartype_Att', 'gartype_Att/Det',
    'gartype_CP', 'gartype_Det', 'gartype_None',
    'gartype_att/CP', 'gartype_det/CP', 'arcstyle_BI-LEVEL',
    'arcstyle_CONVERSIONS', 'arcstyle_END UNIT', 'arcstyle_MIDDLE UNIT',
    'arcstyle_ONE AND HALF-STORY', 'arcstyle_ONE-STORY', 'arcstyle_SPLIT LEVEL',
    'arcstyle_THREE-STORY', 'arcstyle_TRI-LEVEL', 'arcstyle_TRI-LEVEL WITH BASEMENT',
    'arcstyle_TWO AND HALF-STORY', 'arcstyle_TWO-STORY', 'qualified_Q',
    'qualified_U', 'status_I', 'status_V', 
]
for i in condition:
    qualA = px.histogram(data,
        x = i,
        color = "before1980",
        facet_col = "before1980",
        title = i
        )
    #qualA.show()
#arcstyle = [
#'arcstyle_BI-LEVEL', 'arcstyle_CONVERSIONS', 'arcstyle_END UNIT', 
#'arcstyle_MIDDLE UNIT', 'arcstyle_ONE AND HALF-STORY', 
#'arcstyle_ONE-STORY', 'arcstyle_SPLIT LEVEL', 'arcstyle_THREE-STORY', 
#'arcstyle_TRI-LEVEL', 'arcstyle_TRI-LEVEL WITH BASEMENT', 
#'arcstyle_TWO AND HALF-STORY', 'arcstyle_TWO-STORY'
#]
#for i in arcstyle:
#    bi_level = px.histogram(data,
#        x = i,
#        color = "before1980",
#        facet_col = "before1980",
#        title = i
#        )
#    #bi_level.show()

"""
Others
'livearea', 'finbsmnt', 'basement', 'yrbuilt', 'totunits', 
'stories', 'nocars', 'numbdrm', 'numbaths', 'sprice', 'deduct', 
'netprice', 'tasp', 'smonth', 'syear'
"""
#others = ['livearea', 'finbsmnt', 'basement', 'totunits', 
#'stories', 'nocars', 'numbdrm', 'numbaths', 'deduct']
#for i in others:
#    net = px.scatter(data,
#        x = "netprice",
#        y = i,
#        color = "before1980",
#        facet_col = "before1980",
#        title = i
#        )
#    net.show()

# totunits, stories, netprice, numbdrm, 
#stories = px.pie(data,
#    values = "stories",
#    names = "stories",
#    color = "stories",
#    facet_col = "before1980",
#    title = "Stories by year"
#    )
##stories.show()
#newlist = ['totunits', 'stories', 'netprice', 'numbdrm']
#for i in newlist:
#    netprices = px.histogram(data,
#        x = i,
#        facet_col = "before1980",
#        title = i
#        )
#    #netprices.show()

# 
"""
2. 
Build a classification model labeling houses as being built 
“before 1980” or “during or after 1980”.
"""
#features = ['stories', 'quality_C', 'numbdrm', 'netprice', 'numbaths', 'gartype_Att', 'arcstyle_ONE-STORY']
features = data.filter([
    'arcstyle_ONE-STORY', 'quality_C', 'gartype_Att'
    ])
#targets = np.ravel(data.filter(['before1980']).to_numpy())
targets = data.filter(['before1980'])

train_data, test_data, train_targets, test_targets = train_test_split(features, targets, test_size=0.3)
print(test_data)
#BernoulliNB, CategoricalNB, ComplementNB, GaussianNB, MultinomialNB
classifier = BernoulliNB()
classifier.fit(train_data, train_targets)

targets_predicted = classifier.predict(test_data)
accuracy = accuracy_score(test_targets, targets_predicted)
print(accuracy)

#print("targets_predicted", targets_predicted, "test_targets", test_targets)

print(classifier.score(test_data, test_targets))

confusion_matrix = metrics.confusion_matrix(test_targets, targets_predicted)
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = [False, True])
cm_display.plot()
plt.show()
"""
BernoulliNB - 0.848
CategoricalNB -
ComplementNB - 0.826
GaussianNB - 8.43
MultinomialNB - 0.836
"""