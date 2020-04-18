import os
import sys
import time
import pandas as pd
import matplotlib.pyplot as plt
from bokeh.plotting import figure, output_file, show
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import threading

def get_last_data(i_s):
    i_s['Fecha'] =  pd.to_datetime(i_s['Fecha'], format='%Y-%m-%d %H:%M:%S.%f')
    i0      = i_s.loc[0, 'Fecha']
    ilast   = i_s.loc[len(i_s)-1,'Fecha']
    ilimit = ilast - timedelta(hours=36)
    i_s = i_s[i_s.Fecha > ilimit].reset_index()
    return i_s

def is_it_updated(i_s):
    ilast   = i_s.loc[len(i_s)-1,'Fecha']
    delay = (datetime.now() - ilast).total_seconds()
    if delay > 300:
        print('ERROR:\tDatos no actualizados. Ultima muestra de hace '+ str(round(delay/60,2)) + 'min' )
        return False
    else:
        return True
def get_file():
    os.popen('ssh pi@192.168.0.111 cp sensordata.dat sensordata.exp')
    time.sleep(0.5)
    remote_hash = get_remote_hash()
    os.popen('scp pi@192.168.0.111:sensordata.exp .')
    local_hash = get_local_hash()
    while not local_hash == remote_hash:
        local_hash = get_local_hash()
        remote_hash = get_remote_hash()
        time.sleep(1)

def get_remote_hash():
    a = os.popen('ssh pi@192.168.0.111 md5sum sensordata.exp')
    a = a.readline()
    return a
def get_local_hash():
    a = os.popen('md5sum sensordata.exp')
    a = a.readline()
    return a
def clean():
    os.popen('ssh pi@192.168.0.111 rm sensordata.exp')
    os.popen('rm -f sensordata.exp')

get_file()

internal_sensors = pd.read_csv(r"sensordata.exp", header=None)
internal_sensors.columns = ['Temperatura','Humedad','Temperatura_CPU','Temperatura_GPU','Uso_Disco','Fecha']
internal_sensors.Temperatura_CPU = internal_sensors.Temperatura_CPU.round(2)
internal_sensors = get_last_data(internal_sensors)
up_to_date = is_it_updated(internal_sensors)


cpu_temp = list(internal_sensors.Temperatura_CPU)
gpu_temp = list(internal_sensors.Temperatura_GPU)
disk_use = list(internal_sensors.Uso_Disco)
_date    = list(internal_sensors.Fecha)
disk_last= disk_use[-1]
disk     = pd.DataFrame([[disk_last,'Usado','blue'],
                        [100-disk_last,'Libre','green']],
                        columns=['datos','Estado','Color'])

fig_temp = px.line(internal_sensors,x = "Fecha", y = "Temperatura", line_shape='spline')
fig_temp.update_yaxes(title_text="Temperatura (ºC)",range=[0, 30])
fig_temp.update_layout(
    autosize=False,
    width= 640,
    height=230,
    margin=dict(
        l=10,
        r=10,
        b=10,
        t=10,
        pad=4
    ),
    paper_bgcolor="LightSteelBlue",)

fig_temp.write_html("static/temp_chart.html")

fig_hum = px.line(internal_sensors,x = "Fecha", y = "Humedad", line_shape='spline')
fig_hum.update_yaxes(title_text="Humedad (%)",range=[0, 100])
fig_hum.update_layout(
    autosize=False,
    width=640,
    height=230,
    margin=dict(
        l=10,
        r=10,
        b=10,
        t=10,
        pad=4
    ),
    paper_bgcolor="LightSteelBlue",)

fig_hum.write_html("static/hum_chart.html")

fig_cpu = go.Figure()
fig_cpu.add_trace(go.Scatter(x=_date, y=cpu_temp,
                    mode='lines',
                    name='CPU'))
fig_cpu.add_trace(go.Scatter(x=_date, y=gpu_temp,
                    mode='lines',
                    name='GPU'))
fig_cpu.update_yaxes(title_text="Temperatura CPU/GPU(ºC)",range=[20, 105])

fig_cpu.update_layout(
    autosize=False,
    width=640,
    height=230,
    margin=dict(
        l=10,
        r=10,
        b=10,
        t=10,
        pad=4
    ),
    paper_bgcolor="LightSteelBlue",)

fig_cpu.write_html("static/cpu_chart.html")

fig_disk = px.pie(disk,values='datos', names='Estado', title='Espacio en disco', color='Estado',
             color_discrete_map={'Usado':'royalblue',
                                 'Libre':'lightgreen'})
fig_disk.update_layout(
    autosize=False,
    width=230,
    height=230,
    margin=dict(
        l=5,
        r=10,
        b=1,
        t=30,
        pad=4
    ),
    paper_bgcolor="LightSteelBlue",)
fig_disk.write_html("static/disk_pie.html")

clean()