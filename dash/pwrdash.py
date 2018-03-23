# roychan@: 3/2018
import time
import os
import pandas as pd
import numpy as np
import dash
import dash.dependencies as dep
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from plotly import tools
from mytools import *

UPDATE_INTERVAL_MSEC=1000

def uj2w(t,e):
    w = [(e[1]-e[0])/(t[1]-t[0])/1e6]
    for t0,t1,e0,e1 in zip(t[:-1],t[1:],e[:-1],e[1:]):
        p = (e1-e0)/(t1-t0)/1e6
        if p>100 or p<-100:
            p=0
        w.append(p)
    return np.array(w)

def read(filename):
    with open(filename, 'r') as fd:
        s = fd.readline().rstrip()
        return int(s) if s.isdigit() else s

def init_fig():    
    data =[
        go.Scatter(x=[], y=[], name='BAT0', yaxis='y1',
                   marker=dict(color='orange'), legendgroup='bat0'),
        go.Scatter(x=[], y=[], name='BAT1', yaxis='y1',
                   marker=dict(color='steelblue'), legendgroup='bat1'),
        go.Scatter(x=[], y=[], name='BAT0', yaxis='y2',
                   marker=dict(color='orange'), legendgroup='bat0', showlegend=False),
        go.Scatter(x=[], y=[], name='BAT1', yaxis='y2',
                   marker=dict(color='steelblue'), legendgroup='bat1', showlegend=False),
        go.Scatter(x=[], y=[], name='BAT0', yaxis='y3',
                   marker=dict(color='orange'), legendgroup='bat0', showlegend=False),
        go.Scatter(x=[], y=[], name='BAT1', yaxis='y3',
                   marker=dict(color='steelblue'), legendgroup='bat1', showlegend=False),
        go.Scatter(x=[], y=[], name='PSYS', legendgroup='psys', yaxis='y3'),
        go.Scatter(x=[], y=[], name='CPU', legendgroup='plt', yaxis='y3'),
        go.Scatter(x=[], y=[], name='x86_pkg', yaxis='y4'),
        go.Scatter(x=[], y=[], name='INT3400', yaxis='y4'),
        go.Scatter(x=[], y=[], name='TSR0', yaxis='y4'),
        go.Scatter(x=[], y=[], name='TSR1', yaxis='y4'),
        go.Scatter(x=[], y=[], name='TSR2', yaxis='y4'),
        go.Scatter(x=[], y=[], name='TSR3', yaxis='y4'),
        go.Scatter(x=[], y=[], name='B0D4', yaxis='y4'),
        go.Scatter(x=[], y=[], name='iwlwifi', yaxis='y4')               
    ]
    layout = go.Layout(
        width=1200, 
        height=768, 
        plot_bgcolor="#D0D0D0",
        paper_bgcolor="#F0F0F0",
        margin=dict(l=50, b=40, r=0, t=30),
        xaxis1=dict(title='TIME (SEC)', anchor='y4'),
        yaxis1=dict(title='VOLTAGE (V)',  domain=[0.75375, 1.0]),
        yaxis2=dict(title='CURRENT (A)', domain=[0.5025, 0.7488]),
        yaxis3=dict(title='POWER (W)', domain=[0.25125, 0.4975]),
        yaxis4=dict(title='TEMPERATURE (degC)', domain=[0.0, 0.24625])
    )

    fig = dict(data=data, layout=layout)
    print "==========figure============="
    print fig
    print "============================="
    
    return fig

def _init_fig():    
    trace_v0 = go.Scatter(x=[], y=[], name='BAT0', marker=dict(color='orange'), legendgroup='bat0')
    trace_v1 = go.Scatter(x=[], y=[], name='BAT1', marker=dict(color='steelblue'), legendgroup='bat1')
    trace_i0 = go.Scatter(x=[], y=[], name='BAT0', marker=dict(color='orange'), legendgroup='bat0', showlegend=False)
    trace_i1 = go.Scatter(x=[], y=[], name='BAT1', marker=dict(color='steelblue'), legendgroup='bat1', showlegend=False)
    trace_p0 = go.Scatter(x=[], y=[], name='BAT0', marker=dict(color='orange'), legendgroup='bat0', showlegend=False)
    trace_p1 = go.Scatter(x=[], y=[], name='BAT1', marker=dict(color='steelblue'), legendgroup='bat1', showlegend=False)
    trace_sys = go.Scatter(x=[], y=[], name='PSYS', legendgroup='psys')
    trace_plt = go.Scatter(x=[], y=[], name='CPU', legendgroup='plt')
    trace_t0 = go.Scatter(x=[], y=[], name='x86_pkg')
    trace_t1 = go.Scatter(x=[], y=[], name='INT3400')
    trace_t2 = go.Scatter(x=[], y=[], name='TSR0')
    trace_t3 = go.Scatter(x=[], y=[], name='TSR1')
    trace_t4 = go.Scatter(x=[], y=[], name='TSR2')
    trace_t5 = go.Scatter(x=[], y=[], name='TSR3')
    trace_t6 = go.Scatter(x=[], y=[], name='B0D4')
    trace_t7 = go.Scatter(x=[], y=[], name='iwlwifi')

    fig = tools.make_subplots(rows=4, cols=1, vertical_spacing=0.005, shared_xaxes=True)

    fig.append_trace(trace_v0, 1, 1)
    fig.append_trace(trace_v1, 1, 1)
    fig.append_trace(trace_i0, 2, 1)
    fig.append_trace(trace_i1, 2, 1)
    fig.append_trace(trace_p0, 3, 1)
    fig.append_trace(trace_p1, 3, 1)
    fig.append_trace(trace_sys, 3, 1)
    fig.append_trace(trace_plt, 3, 1)
    fig.append_trace(trace_t0, 4, 1)
    fig.append_trace(trace_t1, 4, 1)
    fig.append_trace(trace_t2, 4, 1)
    fig.append_trace(trace_t3, 4, 1)
    fig.append_trace(trace_t4, 4, 1)
    fig.append_trace(trace_t5, 4, 1)
    fig.append_trace(trace_t6, 4, 1)
    fig.append_trace(trace_t7, 4, 1)
    
    print fig

    fig.layout.update(
        go.Layout(
            autosize=True,
            width=1200, 
            height=768, 
            margin=dict(l=50, b=40, r=0, t=30),
            plot_bgcolor="#D0D0D0",
            paper_bgcolor="#F0F0F0",
            xaxis1=dict(title='TIME (SEC)'),
            yaxis1=dict(title='VOLTAGE (V)'),
            yaxis2=dict(title='CURRENT (A)'),
            yaxis3=dict(title='POWER (W)'),
            yaxis4=dict(title='TEMPERATURE (degC)')
        )
    )
    
    return fig

app = dash.Dash()

@app.server.route('/css/my.css')
def serve_stylesheet(stylesheet):
    return flask.send_from_directory(os.getcwd(), stylesheet)

app.css.append_css({"external_url": "/css/my.css"})
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
#app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})  # noqa: E501

app.layout = html.Div(
    children=[
        html.Div(
            children=[html.Button(
                id='button', 
                n_clicks=0, 
                children='STARTING...')
            ], 
            style={'color':'white'}
        ),
        
        html.Div(
            children=[
                dcc.Graph(
                    id='graph_one', 
                    figure=init_fig()
                )
            ],  
            style={'display': 'inline-block'}
        ),
        
        dcc.Interval(id='live-update', interval=1000),
    
    ], style={'background-color':"#F0F0F0"}
) 

@app.callback(
    dep.Output('graph_one', 'figure'),
    [],
    [dep.State('graph_one', 'figure')],
    [dep.Event('live-update', 'interval')])

def update_plot(fig):
    t=time.time()
    y_data = []
    y_data.append(read('/sys/class/power_supply/BAT0/voltage_now')/1e6)
    y_data.append(read('/sys/class/power_supply/BAT1/voltage_now')/1e6)
    y_data.append(read('/sys/class/power_supply/BAT0/current_now')/1e6)
    y_data.append(read('/sys/class/power_supply/BAT1/current_now')/1e6)
    y_data.append(y_data[0]*y_data[1])
    y_data.append(y_data[2]*y_data[3])
    y_data.append(read('/sys/class/powercap/intel-rapl:1/energy_uj')/1e6)
    y_data.append(read('/sys/class/powercap/intel-rapl:0/energy_uj')/1e6)
    y_data.append(read('/sys/class/thermal/thermal_zone0/temp')/1e3)
    y_data.append(read('/sys/class/thermal/thermal_zone1/temp')/1e3)
    y_data.append(read('/sys/class/thermal/thermal_zone2/temp')/1e3)
    y_data.append(read('/sys/class/thermal/thermal_zone3/temp')/1e3)
    y_data.append(read('/sys/class/thermal/thermal_zone4/temp')/1e3)
    y_data.append(read('/sys/class/thermal/thermal_zone5/temp')/1e3)
    y_data.append(read('/sys/class/thermal/thermal_zone6/temp')/1e3)
    y_data.append(read('/sys/class/thermal/thermal_zone7/temp')/1e3)

    data = fig['data']
        
    for dat, y in zip(data, y_data):
        dat['x'].append(t)
        dat['y'].append(y)
 
    return fig

@app.callback(
     dep.Output('button', 'children'),
    [dep.Input('live-update', 'interval')]
)
def update_button_text(interval):
    if interval==UPDATE_INTERVAL_MSEC:
        return 'STOP UPDATE'
    else:
        return 'AUTO UPDATE'
        
@app.callback(
     dep.Output('live-update', 'interval'),
    [dep.Input('button', 'n_clicks')]
)
def button(n_clicks):
    if n_clicks%2:
        return UPDATE_INTERVAL_MSEC*3600*24
    else:
        return UPDATE_INTERVAL_MSEC

if __name__ == '__main__':
    app.run_server(debug=True)