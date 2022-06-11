import streamlit as st
from honeybee.model import Model
from honeybee.room import Room


from honeybee_vtk.model import Model

from hb_utils.add_aps import add_aps_by_ratio

st.set_page_config(
    page_title='UD Shoebox Study App',
    layout='wide',
    page_icon='./assets/UD_Logo.png'
)

st.sidebar.image('./assets/UD_Logo.png')

wid = st.sidebar.number_input('Space Width')
dep = st.sidebar.number_input('Space Depth')
hei = st.sidebar.number_input('Space Height')
wwr = st.sidebar.number_input('Glazing Ratio')


_send_it = st.sidebar.button('Accept Inputs')

if _send_it:
    rm = Room.from_box('Single_Zone', wid, dep, hei)
    rm = add_aps_by_ratio

    model = Model('Single_Zone_Model', [rm])

    model_json = model.to_hbjson(folder='temp_assets')
