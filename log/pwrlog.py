import time
import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

app = dash.Dash()

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

app.layout = html.Div([
    html.Button('UPDATE', id='button'),
    html.Div([
        dcc.Graph(id='graph_voltage'),
        dcc.Graph(id='graph_current'),
        dcc.Graph(id='graph_power')
    ], style={'display': 'inline-block'})
    
]) 

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

@app.callback(   
    dash.dependencies.Output('graph_voltage', 'figure'),
    [dash.dependencies.Input('button', 'id')])
def update_graph0(id):
    df = pd.read_csv('/tmp/mon.csv')

    plt_w = uj2w(df['time'],df['cpu_uj'])
    sys_w = uj2w(df['time'],df['sys_uj'])*2

    #t = df['time']
    t = np.arange(len(df['time'])).astype(float)
    t = (t - t[0])/60/60

    trace_v0 = go.Scatter(x=t, y=df.v0/1e6, line = dict(width=1.5), name='BAT0', 
                    marker = dict(symbol='circle', color='orange'),
                    legendgroup='bat0', xaxis='TIME')
    trace_v1 = go.Scatter(x=t, y=df.v1/1e6, line = dict(width=1.5), name='BAT1',
                    marker = dict(symbol='circle', color='steelblue'), 
                    legendgroup='bat1')
    return dict(
        data=[trace_v0, trace_v1],
        layout=dict(width=1200, height=200, margin=dict(t=25,b=0,r=0,l=45),yaxis=dict(title='VOLTAGE (V)'))
    )

@app.callback(   
    dash.dependencies.Output('graph_current', 'figure'),
    [dash.dependencies.Input('button', 'n_clicks')])
def update_graph1(n_clicks):
    df = pd.read_csv('/tmp/mon.csv')

    plt_w = uj2w(df['time'],df['cpu_uj'])
    sys_w = uj2w(df['time'],df['sys_uj'])*2

    #t = df['time']
    t = np.arange(len(df['time'])).astype(float)
    t = (t - t[0])/60/60

    trace_i0 = go.Scatter(x=t, y=df.i0/1e6, line = dict(width=1.5), name='BAT0',
                    marker = dict(symbol='circle', color='orange'),
                    legendgroup='bat0')
    trace_i1 = go.Scatter(x=t, y=df.i1/1e6, line = dict(width=1.5), name='BAT1',
                    marker = dict(symbol='circle', color='steelblue'), 
                    legendgroup='bat1')
    return dict(
        data=[trace_i0, trace_i1],
        layout=dict(width=1200, height=200, margin=dict(t=25,b=0,r=0,l=45),yaxis=dict(title='CURRENT (A)'))
    )

@app.callback(   
    dash.dependencies.Output('graph_power', 'figure'),
    [dash.dependencies.Input('button', 'n_clicks')])

def update_graph2(n_clicks):
    df = pd.read_csv('/tmp/mon.csv')

    plt_w = uj2w(df['time'],df['cpu_uj'])
    sys_w = uj2w(df['time'],df['sys_uj'])*2

    #t = df['time']
    t = np.arange(len(df['time'])).astype(float)
    t = (t - t[0])/60/60

    pbat0 = df.i0*df.v0/1e12
    pbat1 = df.i1*df.v1/1e12

    trace_p0 = go.Scatter(x=t, y=pbat0, line = dict(width=1.5), name='BAT0',
                    marker = dict(symbol='circle', color='orange'),
                    legendgroup='bat0')
    trace_p1 = go.Scatter(x=t, y=pbat1, line = dict(width=1.5), name='BAT1',
                    marker = dict(symbol='circle', color='steelblue'), 
                    legendgroup='bat1')
    trace_sys = go.Scatter(x=t, y=sys_w, line = dict(width=1.5), name='PSYS', 
                    legendgroup='psys')
    trace_plt = go.Scatter(x=t, y=plt_w, line = dict(width=1.5), name='SOC',
                    legendgroup='plt')
    trace_rop = go.Scatter(x=t, y=sys_w-plt_w, line = dict(width=1.5), name='ROP',
                    legendgroup='rop')
    return dict(
        data=[trace_p0, trace_p1, trace_sys, trace_plt, trace_rop],
        layout=dict(width=1200, height=200, margin=dict(t=25,b=0,r=0,l=45),yaxis=dict(title='POWER (W)'))
    )

if __name__ == '__main__':
    app.run_server(debug=True)