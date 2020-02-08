''' 
Dashboard utilizada pelos alunos para análise de dados dos raios cósmicos
'''
import pandas as pd
import numpy as np
from os.path import join, dirname

from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, Select, Slider
from bokeh.io import show, output_file, curdoc
from bokeh.plotting import figure
from bokeh.tile_providers import get_provider, Vendors   



# Abrindo o dataset (já manipulado para melhor análise)
df = pd.read_csv("data.csv")
schools = {'escola': ['IF-USP', 'IFSP'],
           'latitude':[-2699887, -2695467],
           'longitude':[-5202510,-5190044] }

#Source do Bokeh
events = df[df["day"]==29]["hour"].value_counts(sort=False).to_frame()
events.reset_index(inplace=True)
source = ColumnDataSource(events)

# Menus de seleção
menu_dia = Slider(start=1, end=30, value=29, step=1, title='Dia')
menu_escolas = Select(options= schools['escola'], value='IF_USP', title='Escola')

# Callbacks

def callback(attr, old, new):
    dia = menu_dia.value
    events = df[df["day"]==dia]["hour"].value_counts(sort=False).to_frame()
    events.reset_index(inplace=True)
    source.data = events
menu_dia.on_change('value', callback)


#Histograma de dias
p1 = figure(x_axis_label='Horas', y_axis_label='Quantidade de raios',plot_height=350, title="Histograma",
           toolbar_location=None, tools="hover")

p1.vbar(source = source, x='index', top='hour', width=0.9, hover_color="#718dbf")

p1.xgrid.grid_line_color = None
p1.y_range.start = 0

#Mapa
tile_provider = get_provider(Vendors.CARTODBPOSITRON)

# range bounds supplied in web mercator coordinates
p2 = figure(x_range=(-5209752, -5184148), y_range=(-2710816, -2684103),
           x_axis_type="mercator", y_axis_type="mercator", title="Mapa", x_axis_label="Longitude", y_axis_label="Latitude", tools=["hover",'pan','wheel_zoom'])
p2.add_tile(tile_provider)

# Circulos que representam as escolas
p2.circle(x='longitude', y='latitude', fill_color='blue', size=10, hover_color="red", source=schools)

layout = row(p2, column(menu_escolas, menu_dia), p1)
curdoc().add_root(layout)
