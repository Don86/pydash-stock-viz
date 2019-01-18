import dash
import plotly
import plotly.graph_objs as go
import plotly.tools as tls

from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from pandas_datareader import data as web
from datetime import datetime as dt, timedelta
from scipy.signal import savgol_filter

from flask import send_from_directory
import os


app = dash.Dash(__name__)


app.layout = html.Div([
	# link to css
	#html.Link(
    #    rel='stylesheet',
    #    href='/static/style.css'
    #),

	# Title
	html.Div(
		className="app-header",
		children=[html.Div("Index Viz", className="app-header-title")]
		),
	
	# PyDash logo at top right
	html.Img(src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/logo/new-branding/dash-logo-by-plotly-stripe.png",
                style={'height': '100px', 'float': 'right'},),

	# Dropdown list - ticker selection
	dcc.Dropdown(
		id="my-dropdown",
		options=[{"label":"snp500", "value":"^GSPC"},
		{"label":"Tesla", "value":"TSLA"}],
		value="^GSPC"),

	# ========== Date pickers: to and from ==========
	#dcc.DatePickerSingle(
	#	id="to-date",
	#	min_date_allowed=dt(1997, 1, 1),
	#	max_date_allowed=dt.today(),
	#	month_format='MMM Do, YY',
	#	placeholder='MMM Do, YY',
	#	date=dt.today()
	#	),

	dcc.DatePickerRange(
		id="date-picker-range",
		min_date_allowed=dt(1997, 1, 1),
		#start_date_placeholder_text=dt.today(),
		#end_date_placeholder_text=dt.today(),
		start_date=dt.today(),
		end_date=dt.today()
		),

	dcc.Graph(id="my-graph")
	])


@app.callback(Output("my-graph", "figure"), 
	[Input("my-dropdown", "value"), 
	Input("date-picker-range", "start_date"),
	Input("date-picker-range", "end_date"),
	])
def update_graph(selected_dropdown_value, from_date, to_date):
	"""Updates graph according to selected ticker symbol.
	"""
	df = web.DataReader(selected_dropdown_value, 
		data_source="yahoo",
		#start=dt(1997,1,1), 
		start=from_date,
		#end=dt.now())
		end=to_date)

	# Compute column of smoothed values
	#d1 = dt.strptime(from_date, "%Y-%m-%d")
	#d2 = dt.strptime(to_date, "%Y-%m-%d")
	#window = min((dt.strptime(to_date) - dt.strptime(from_date)).days, 61)
	window=61
	df["smoothed"] = savgol_filter(list(df["Close"]), window, 3)

	return {"data":[{"x": df.index, "y": df.Close, "type": "markers", "name": "close_val", 
	"line": dict(color = ('rgb(0, 76, 153)'), width=0.5)}, 
	{"x": df.index, "y": df.smoothed, "type": "line", "name": "smoothed", "line": dict(
        color = ('rgb(205, 12, 24)'),
        width = 0.75)}], 
	"layout":{"title":selected_dropdown_value}}


if __name__ == "__main__":
	app.run_server(debug=True)