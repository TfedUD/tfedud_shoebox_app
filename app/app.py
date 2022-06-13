import streamlit as st
import streamlit.components.v1 as components
from streamlit_vtkjs import st_vtkjs
from pathlib import Path
import json
import os
from honeybee.model import Model
from honeybee.room import Room
from honeybee_energy.lib.programtypes import STANDARDS_REGISTRY, PROGRAM_TYPES

import honeybee_vtk.model
from honeybee_vtk.model import DisplayMode

from hb_utils.add_aps import add_aps_by_ratio, add_louver_shade
from hb_utils.lib_utils import GetBaseCon, get_room_programs


st.set_page_config(
    page_title='UD Shoebox Study App',
    layout='wide',
    page_icon='./assets/UD_Logo.png'
)

st.sidebar.image('./assets/UD_Logo.png')
st.sidebar.write(""" Going to add the log in/
                 API key thing, as well as
                 'how many runs' the selected
                 will produce""")

with st.expander("Climate Set"):
    show_map = st.button('Show EPW Map')
    epw_url = st.text_input(label='enter epw URL')
    if show_map:
        components.iframe(src="https://www.ladybug.tools/epwmap/",
                          width=900, height=650, scrolling=True)


def add_viewer(model_vtk):
    return st_vtkjs(
        content=model_vtk, key="viewer"
    )


with st.expander("Room, Aperture & Shade Geometry Inputs"):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Room Data")
        wid = st.number_input('Width', value=4.5)
        dep = st.number_input('Depth', value=6.5)
        hei = st.number_input('Height', value=3.5)

    with col2:
        st.subheader("Aperature Data")
        wwr = st.multiselect(
            'WWR', [0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80],
            default=0.50)

        sub_d = st.checkbox('Subdivision', value=True)
        sub_d = True if sub_d == True else False

        win_height = st.multiselect(
            'Window Height', [0.45, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5],
            default=1.0)

        sill_height = st.multiselect(
            'Sill Height', [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
            default=0.2)

        horiz_sep = st.multiselect('Horiz Separation', [1.0, 2.0, 3.0], default=1.0)

        vert_sep = st.multiselect(
            'Vertical Separation', [0.0, 1.0, 2.0, 3.0],
            default=0.0)

    with col3:

        st.subheader("Shade Data")
        louv_d = st.multiselect('Depth', [0.00, 0.10, 0.20, 0.30, 0.40], default=0.00)

        louv_spc = st.multiselect(
            "Shade Spacing", [0.00, 0.15, 0.25, 0.35, 0.45, 0.55],
            default=0.00)

        louv_offset = st.multiselect(
            "Facade offset", [0.00, 0.10, 0.20, 0.30, ],
            default=0.00)

        louv_poz = st.checkbox("Vertical Shades", value=None)
        louv_poz = True if louv_poz == True else False

with st.expander("Baseline Typology Data"):

    col1, col2 = st.columns(2)
    with col1:
        st.write("""#### Construction Set""")
        climate = st.selectbox('Climate Zone',
                               ('1-Very Hot', '2-Hot', '3-Warm',
                                '4-Mixed', '5-Cool', '6-Cold',
                                '7-Very Cold', '8-Subartic')
                               )
        vintage = st.selectbox('Building Vintage',
                               ('ASHRAE 90.1 2019', 'ASHRAE 90.1 2016',
                                'AHSRAE 90.1 2013', 'ASHRAE 90.1 2010', 'ASHRAE 90.1')
                               )
        constr_type = st.selectbox('Baseline Construction Type',
                                   ('SteelFramed', 'WoodFramed',
                                    'Metal Building', 'Mass')
                                   )

    with col2:
        st.write("""#### Zone Program""")
        bldg_typol = st.selectbox(
            'Building Use',
            ['LargeOffice', 'MediumOffice', 'MidriseApartment', 'HighriseApartment',
             'Retail', 'StripMall', 'PrimarySchool', 'SecondarySchool', 'SmallHotel',
             'LargeHotel', 'Hospital', 'Outpatient', 'Laboratory', 'Warehouse',
             'SuperMarket', 'FullServiceResturant', 'QuickServiceResturant',
             'Courthouse', 'LargeDataCenterHighITE', 'LargeDataCenterLowITE',
             'SmallDataCenterHighITE', 'SmallDataCenterLowITE'])

        selected_program = st.selectbox(
            'Zone Program', get_room_programs(bldg_typol, str(vintage)))

        st.write("""***""")


# TODO
our_constr = GetBaseCon(climate, vintage, constr_type)
# TODO

_send_it = st.sidebar.button('Accept Inputs')

if _send_it:
    rm = Room.from_box('Single_Zone', wid, dep, hei)

    wall_faces = [face.duplicate() for face in rm.faces if str(face.type) == 'Wall']
    front_face_ap = add_aps_by_ratio(
        wall_faces[2],
        _ratio=[wwr[0]],
        _subdivide_=[sub_d],
        _win_height_=[win_height[0]],
        _sill_height_=[sill_height[0]],
        _horiz_separ_=[horiz_sep[0]],
        vert_separ_=[vert_sep[0]])

    front_face_ap = add_louver_shade(
        [front_face_ap],
        _depth=[louv_d[0]],
        _dist_between_=[louv_spc[0]],
        _facade_offset_=[louv_offset[0]],
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
