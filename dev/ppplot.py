import chart_studio
chart_studio.tools.set_credentials_file(username='onesixx6', api_key='xql6q8ohmp')

import chart_studio.plotly as py
import plotly.graph_objs as go

trace0 = go.Scatter(
    x=[1, 2, 3, 4],
    y=[10, 15, 13, 17]
)
trace1 = go.Scatter(
    x=[1, 2, 3, 4],
    y=[16, 5, 11, 9]
)
data = [trace0, trace1]

# help(py.plot)
# py.plot(data, filename = 'basic-line', auto_open=True)
py.plot(data)
py.iplot(data)





import chart_studio.plotly as py
import plotly.express as px

df = px.data.iris()
fig = px.scatter (df,
    x='sepal_length', y='sepal_width', 
    color= 'species'
)
fig.show()

py.iplot(fig)

# ERROR 
#PlotlyRequestError: No message