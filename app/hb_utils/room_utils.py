from dataclasses import dataclass
from honeybee.room import Room
from honeybee.face import Face
from honeybee.facetype import get_type_from_normal
from honeybee.typing import clean_and_id_string
from honeybee_energy.lib.programtypes import program_type_by_identifier, \
    building_program_type_by_identifier, office_program
from honeybee_energy.lib.constructionsets import construction_set_by_identifier
from honeybee_radiance.lib.modifiersets import modifier_set_by_identifier

from .add_aps import add_aps_by_ratio


@dataclass
class ShoeBoxModel:
    """ A class for streamlined modification and setup
    of shoebox energy models"""

    room: Room
    front_face: Face
    left_face: Face
    back_face: Face
    right_face: Face
    roof_face: Face
    floor_face: Face

    @property
    def ap_front_face(self):
        return None

    @classmethod
    def from_hb_room(cls, room: Room):
        room = room
        faces = [face for face in room.faces]
        wall_faces = [face for face in faces if str(face.type) == 'Wall']
        roof_f = [face for face in faces if str(face.type) == 'RoofCeiling']
        floor_f = [face for face in faces if str(face.type) == 'Floor']

        return cls(room=room, front_face=wall_faces[2], left_face=wall_faces[1],
                   back_face=wall_faces[0], right_face=wall_faces[3],
                   roof_face=roof_f[0], floor_face=floor_f[0])

    def add_aps(
            self, face=None, _ratio=[0.5],
            subdivide_=[],
            win_height_=[2],
            sill_height_=[0.8],
            horiz_separ_=[3],
            vert_separ_=[],
            operable_=[]):
        """ Function to manage modification of the rooms aperatures """
        if face is None:
            face = self.front_face

        self.ap_front_face = add_aps_by_ratio(
            face, _ratio=_ratio, _subdivide_=subdivide_, _win_height_=win_height_,
            _sill_height_=sill_height_, _horiz_separ_=horiz_separ_,
            vert_separ_=vert_separ_, operable_=operable_)

    @property
    def simable_shoebox(self):
        return self._make_shoebox(
            faceobjs=[self.ap_front_face, self.left_face, self.back_face, self.right_face,
                      self.roof_face, self.floor_face])

    @staticmethod
    def _make_shoebox(faceobjs):

        simable_room = Room(identifier='sb_modded_room', faces=faceobjs)
        return simable_room
