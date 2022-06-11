import streamlit as st
from streamlit_vtkjs import st_vtkjs
from pathlib import Path
import json
import os
from honeybee.model import Model
from honeybee.room import Room


import honeybee_vtk.model
from honeybee_vtk.model import DisplayMode

from hb_utils.add_aps import add_aps_by_ratio, add_louver_shade


st.set_page_config(
    page_title='UD Shoebox Study App',
    layout='centered',
    page_icon='./assets/UD_Logo.png'
)

st.sidebar.image('./assets/UD_Logo.png')


def add_viewer(model_vtk):
    return st_vtkjs(
        content=model_vtk, key="viewer"
    )


st.sidebar.subheader("Room Data")
wid = st.sidebar.number_input('Width', value=4.5)
dep = st.sidebar.number_input('Depth', value=6.5)
hei = st.sidebar.number_input('Height', value=3.5)
st.sidebar.subheader("Aperature Data")
wwr = st.sidebar.number_input('WWR', value=0.55)
sub_d = st.sidebar.checkbox('Subdivision', value=True)
sub_d = True if sub_d == True else False
win_height = st.sidebar.number_input('Window Height', value=2.00)
sill_height = st.sidebar.number_input('Sill Height', value=0.8)
horiz_sep = st.sidebar.number_input('Horiz Separation', value=3.0)
vert_sep = st.sidebar.number_input('Vertical Separation', value=0.0)

st.sidebar.subheader("Shade Data")
louv_d = st.sidebar.number_input("Depth", value=0.15)
louv_spc = st.sidebar.number_input("Shade Spacing", value=0.50)
louv_offset = st.sidebar.number_input("Facade offset", value=0.0)
louv_poz = st.sidebar.checkbox("Vertical Shades", value=None)
louv_poz = True if louv_poz == True else False

_send_it = st.sidebar.button('Accept Inputs')

if _send_it:
    rm = Room.from_box('Single_Zone', wid, dep, hei)

    wall_faces = [face.duplicate() for face in rm.faces if str(face.type) == 'Wall']
    front_face_ap = add_aps_by_ratio(
        wall_faces[2],
        _ratio=[wwr],
        _subdivide_=[sub_d],
        _win_height_=[win_height],
        _sill_height_=[sill_height],
        _horiz_separ_=[horiz_sep],
        vert_separ_=[vert_sep])

    front_face_ap = add_louver_shade(
        [front_face_ap],
        _depth=[louv_d],
        _dist_between_=[louv_spc],
        _facade_offset_=[louv_offset],
        vertical_=[louv_poz])

    left_face = wall_faces[1]
    back_face = wall_faces[0]
    right_face = wall_faces[3]

    roof_face = [face.duplicate() for face in rm.faces
                 if str(face.type) == 'RoofCeiling'][0]
    floor_face = [face.duplicate() for face in rm.faces
                  if str(face.type) == 'Floor'][0]

    modded_room = Room(
        'modRoom',
        faces=[front_face_ap, left_face, back_face, right_face, roof_face, floor_face])

    model = Model(
        'Single_Zone_Bldg', [modded_room]
    )

    model_vtk = honeybee_vtk.model.Model.from_hbjson(
        model.to_hbjson('temp_assets\\my_model', '.', 3))

    model_vtk.to_vtkjs(folder='temp_assets', config=None,
                       model_display_mode=DisplayMode.Shaded)

add_viewer(Path('temp_assets\\model.vtkjs').read_bytes())
