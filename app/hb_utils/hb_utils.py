# placeholder for additional utils modified from grasshopper components
from honeybee.model import Model
from honeybee.room import Room
from honeybee.face import Face
from .add_aps import add_aps_by_ratio, add_louver_shade


def make_hb_model_json(model):
    return model.to_hbjson(folder='temp_assets', indent=3)


def make_model(wid, dep, hei, wwr, louver_depth):
    rm = Room.from_box('Single_Zone', wid, dep, hei)

    wall_faces = [face.duplicate() for face in rm.faces if str(face.type) == 'Wall']
    front_face_ap = add_aps_by_ratio(
        wall_faces[2],
        _ratio=[wwr],
        # _subdivide_=[sub_d],
        # _win_height_=[win_height],
        # _sill_height_=[sill_height],
        # _horiz_separ_=[horiz_sep],
        # vert_separ_=[vert_sep]
    )

    front_face_ap = add_louver_shade(
        [front_face_ap],
        _depth=[louver_depth],
        # _dist_between_=[louv_spc],
        # _facade_offset_=[louv_offset],
        # vertical_=[louv_poz]
    )

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
    return model
