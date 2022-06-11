import streamlit as st
from streamlit_vtkjs import st_vtkjs
from pathlib import Path
import json
import os
from honeybee.model import Model
from honeybee.room import Room


import honeybee_vtk.model
from honeybee_vtk.model import DisplayMode

from hb_utils.add_aps import add_aps_by_ratio
from hb_utils.hb_utils import make_hb_model_json, make_model

st.set_page_config(
    page_title='UD Shoebox Study App',
    layout='wide',
    page_icon='./assets/UD_Logo.png'
)

st.sidebar.image('./assets/UD_Logo.png')


def add_viewer(model_vtk):
    return st_vtkjs(
        content=model_vtk, key="viewer"
    )


st.sidebar.write("Units: Metric")
wid = st.sidebar.number_input('Space Width', value=5.0)
dep = st.sidebar.number_input('Space Depth', value=8.0)
hei = st.sidebar.number_input('Space Height', value=3.0)
wwr = st.sidebar.number_input('Glazing Ratio', value=0.5)
louver_depth = st.sidebar.number_input('Louver Depth', value=0.1)


_send_it = st.sidebar.button('Accept Inputs')

if _send_it:
    model = make_model(wid, dep, hei, wwr, louver_depth)
    model_json = make_hb_model_json(model)

    model_vtk = honeybee_vtk.model.Model.from_hbjson(model_json)

    vtk_path = model_vtk.to_vtkjs(folder='temp_assets', config=None,
                                  model_display_mode=DisplayMode.Shaded)

add_viewer(Path(vtk_path).read_bytes())
