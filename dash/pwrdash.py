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
    try:
        with open(filename, 'r') as fd:
            s = fd.readline().rstrip()
            return int(s) if s.isdigit() else s
    except:
        return 0

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
        plot_bgcolor="#C0C0C0",
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

def init_histo():    
    data =[
        go.Histogram(
            x=[], y=[], 
            histnorm='probability', 
            nbinsx=128, 
            name='BAT0',
            marker = dict(color='orange'), 
            showlegend=False,
            cumulative=dict(enabled=True),
            xaxis='x1',
            yaxis='y1'
        ),
        go.Histogram(
            x=[],
            histnorm='probability', 
            nbinsx=128, 
            name='BAT1',
            marker = dict(color='steelblue'),  
            showlegend=False,
            cumulative=dict(enabled=True),
            xaxis='x2',
            yaxis='y1'
        )     
    ]
    layout = go.Layout(
        width=1070, 
        height=240, 
        plot_bgcolor="#C0C0C0",
        paper_bgcolor="#F0F0F0",
        margin=dict(l=50, b=40, r=0, t=10),
        xaxis1=dict(title='BAT0 POWER (W)', domain=[0,0.495]),
        xaxis2=dict(title='BAT1 POWER (W)', domain=[0.505, 1])
    )

    fig = dict(data=data, layout=layout)
    print "==========figure============="
    print fig
    print "============================="
    
    return fig

def make_annotation_item(x, y):
    return dict(xref='x1', yref='y1',
                x=7, y=0.5,
                font=dict(color='black'),
                xanchor='left',
                yanchor='middle',
                text='Annotation',
                showarrow=True)

app = dash.Dash()

@app.server.route('/css/my.css')
def serve_stylesheet(stylesheet):
    return flask.send_from_directory(os.getcwd(), stylesheet)

app.css.append_css({"external_url": "/css/my.css"})
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
#app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})  # noqa: E501

def serve_layout():
    return html.Div(
        children=[
            html.Div(
                children=[
                    html.Button(
                        id='button', 
                        n_clicks=0, 
                        children='STARTING...',
                        style={
                            'margin':'10px', 
                            'font-family': 'verdana', 
                            'font-size':'120%'
                        }
                    ),
                    html.Span(
                        id='text_status',
                        children='',
                        style={'font-size':'120%', 'padding':'20px'}
                    )
                ]

            ),

            html.Div(
                children=[
                    dcc.Graph(
                        id='graph_one', 
                        figure=init_fig()
                    ),
                    dcc.Graph(
                        id='histogram', 
                        figure=init_histo()
                    )

                ],  
                style={'display': 'inline-block'}
            ),

            dcc.Interval(id='live-update', interval=1000),

            html.Div(id='time0', children=time.time(), style={'display':'none'})

        ], style={'background-color':"#F0F0F0"}
    )

app.layout = serve_layout

@app.callback(
    dep.Output('text_status', 'children'),
    [],
    [],
    [dep.Event('live-update', 'interval')]
)
def update_text():
    return 'BAT0({}): {:.2f}V, {:.2f}A, {}% - BAT1({}): {:.2f}V, {:.2f}A, {}%'.format(
        read('/sys/class/power_supply/BAT0/status'),
        read('/sys/class/power_supply/BAT0/voltage_now')/1e6,
        read('/sys/class/power_supply/BAT0/current_now')/1e6,
        read('/sys/class/power_supply/BAT0/capacity'),
        read('/sys/class/power_supply/BAT1/status'),
        read('/sys/class/power_supply/BAT1/voltage_now')/1e6,
        read('/sys/class/power_supply/BAT1/current_now')/1e6,
        read('/sys/class/power_supply/BAT1/capacity')
    )

@app.callback(
    dep.Output('histogram', 'figure'),
    [],
    [dep.State('graph_one', 'figure'),
     dep.State('histogram', 'figure')],
    [dep.Event('live-update', 'interval')])

def update_histo(fig, histo):
    pwr_bat0 = np.array(fig['data'][4]['y'])
    pwr_bat1 = np.array(fig['data'][5]['y'])
    histo['data'][0]['x'] = pwr_bat0[pwr_bat0>0]
    histo['data'][1]['x'] = pwr_bat1[pwr_bat1>0]
    print pwr_bat0
    i=np.where(pwr_bat0>=0.9)[0][0]
    x=pwr_bat0[i]
    y=0.9
    
    print "======={}======".format(x)
    
    fig['layout'].update(
        {'annotations':[make_annotation_item(7,0.5)]}
    )
    
    return histo
    
@app.callback(
    dep.Output('graph_one', 'figure'),
    [],
    [dep.State('graph_one', 'figure'),
     dep.State('time0', 'children')],
    [dep.Event('live-update', 'interval')])

def update_plot(fig,time0):
    y_data = []
    t0 = time.time()
    sys0 = read('/sys/class/powercap/intel-rapl:1/energy_uj')/1e6
    cpu0 = read('/sys/class/powercap/intel-rapl:0/energy_uj')/1e6
    
    v0 = read('/sys/class/power_supply/BAT0/voltage_now')/1e6
    v1 = read('/sys/class/power_supply/BAT1/voltage_now')/1e6
    
    i0 = read('/sys/class/power_supply/BAT0/current_now')/1e6
    i1 = read('/sys/class/power_supply/BAT1/current_now')/1e6
    
    if read('/sys/class/power_supply/BAT0/status')=='Charging':
        i0=-i0
    if read('/sys/class/power_supply/BAT1/status')=='Charging':
        i1=-i1
        
    t = time.time() - time0

    y_data.append(v0)
    y_data.append(v1)
    y_data.append(i0)
    y_data.append(i1)
    y_data.append(v0*i0)
    y_data.append(v1*i1)    
    y_data.append(0)
    y_data.append(0)
    y_data.append(read('/sys/class/thermal/thermal_zone0/temp')/1e3)
    y_data.append(read('/sys/class/thermal/thermal_zone1/temp')/1e3)
    y_data.append(read('/sys/class/thermal/thermal_zone2/temp')/1e3)
    y_data.append(read('/sys/class/thermal/thermal_zone3/temp')/1e3)
    y_data.append(read('/sys/class/thermal/thermal_zone4/temp')/1e3)
    y_data.append(read('/sys/class/thermal/thermal_zone5/temp')/1e3)
    y_data.append(read('/sys/class/thermal/thermal_zone6/temp')/1e3)
    y_data.append(read('/sys/class/thermal/thermal_zone7/temp')/1e3)

    time.sleep(0.1)
    dt = time.time() - t0
    sys1 = read('/sys/class/powercap/intel-rapl:1/energy_uj')/1e6
    cpu1 = read('/sys/class/powercap/intel-rapl:0/energy_uj')/1e6
    y_data[6] = (sys1-sys0)/dt
    y_data[7] = (cpu1-cpu0)/dt
    
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
        return 'STOP'
    else:
        return 'RUN'
        
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
    app.run_server(debug=True, port=9001)