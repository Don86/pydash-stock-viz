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

from flask import send_from_directory
import os


app = dash.Dash()
server = app.server
app.config.suppress_callback_exceptions = True
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

# CSS Not working!

app.layout = html.Div([
	# link to css
	html.Link(
        rel='stylesheet',
        href='/static/style.css'
    ),

	# Title
	html.H1("Index Viz", id="my-title"),
	
	# PyDash logo at top right
	html.Img(src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/logo/new-branding/dash-logo-by-plotly-stripe.png",
                style={'height': '100px', 'float': 'right'},),

	# Dropdown list - ticker selection
	dcc.Dropdown(
		id="my-dropdown",
		options=[{"label":"snp500", "value":"^GSPC"},
		{"label":"Tesla", "value":"TSLA"}],
		value="^GSPC"),

	# Date picker
	dcc.DatePickerSingle(
		id="from-date",
		min_date_allowed=dt(1997, 1, 1),
		max_date_allowed=dt.now(),
		month_format='MMM Do, YY',
		placeholder='MMM Do, YY',
		date=dt.now()
		),

	dcc.DatePickerSingle(
		id="to-date",
		min_date_allowed=dt(1997, 1, 1),
		max_date_allowed=dt.now(),
		month_format='MMM Do, YY',
		placeholder='MMM Do, YY',
		date=dt.now()
		),

	#html.Div(id='my-graph')
	dcc.Graph(id="my-graph")
	])


@app.callback(Output("my-graph", "figure"), [Input("my-dropdown", "value")])
def update_graph(selected_dropdown_value):
	"""Updates graph according to selected ticker symbol.
	"""
	df = web.DataReader(selected_dropdown_value, 
		data_source="yahoo",
		start=dt(1997,1,1), 
		end=dt.now())

	# Compute column of smoothed values
	df["smoothed"] = savgol_filter(list(df["Close"]), 61, 3)

	return {"data":[{"x": df.index, "y": df.Close, "type": "markers", "name": "close_val", 
	"line": dict(color = ('rgb(0, 76, 153)'), width=0.5)}, 
	{"x": df.index, "y": df.smoothed, "type": "line", "name": "smoothed", "line": dict(
        color = ('rgb(205, 12, 24)'),
        width = 0.75)}], 
	"layout":{"title":selected_dropdown_value}}


@app.server.route('/static/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'static')
    return send_from_directory(static_folder, path)


if __name__ == "__main__":
	app.run_server(debug=True)