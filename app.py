import dash
import plotly
import plotly.graph_objs as go
import plotly.tools as tls

from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from pandas_datareader import data as web
from datetime import datetime as dt
from scipy.signal import savgol_filter
from collections import deque


app = dash.Dash()

app.layout = html.Div([
	# Title
	html.H1("Index Viz", 
		# This should really be in a CSS
		style={"display": "inline",
		"float": "left", 
		"font-size": "2.65em",
		"margin-left": "7px",
		"font-weight": "bolder",
		"font-family": "Product Sans",
		"color": "rgba(117, 117, 117, 0.95)",
		"margin-top" :"20px",
		"margin-bottom": "0"
		}),
	
	# PyDash logo at top right
	html.Img(src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/logo/new-branding/dash-logo-by-plotly-stripe.png",
                style={'height': '100px', 'float': 'right'},),

	# Dropdown list - ticker selection
	dcc.Dropdown(
		id="my-dropdown",
		options=[{"label":"snp500", "value":"^GSPC"},
		{"label":"Tesla", "value":"TSLA"}],
		value="^GSPC"),


	html.Div(id='my-graph')
	])

@app.callback(Output("my-graph", "children"), [Input("my-dropdown", "value")])
def update_graph(selected_dropdown_value):
	"""Updates graph according to selected ticker symbol.
	"""
	df = web.DataReader(selected_dropdown_value, 
		data_source="yahoo",
		start=dt(1997,1,1), 
		end=dt.now())
	return {"data":[{"x": df.index, "y": df.Close}], "layout":{"title":selected_dropdown_value}}
	#return dcc.Graph(id="my-graph", 
	#	figure={
	#	"data": [{"x": df.index, "y":df.Close, "type": "line", "name": selected_dropdown_value}],
	#	"layout": {"title": selected_dropdown_value}
	#	})


if __name__ == "__main__":
	app.run_server(debug=True)