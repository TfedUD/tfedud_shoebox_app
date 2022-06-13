from honeybee_energy.lib.programtypes import STANDARDS_REGISTRY, PROGRAM_TYPES
from honeybee_energy.lib.constructionsets import construction_set_by_identifier
from honeybee_energy.constructionset import ConstructionSet
from honeybee_energy.lib.constructionsets import construction_set_by_identifier
import pandas as pd


class GetBaseCon():
    """A simple class to return baseline construction set"""

    def __init__(self, _clim, _vint, _con_type):
        self.clim = _clim
        self.vint = _vint
        self.con_type = _con_type

    @property
    def climate(self):
        return self._clean_clim(self.clim)

    @staticmethod
    def _clean_clim(obj) -> int:
        """returns the first char of input string"""
        return(obj[0])

    @property
    def vintage(self):
        return self._clean_vint(self.vint)

    @staticmethod
    def _clean_vint(obj) -> int:
        """returns the year from the input string"""
        return(obj[-4:])

    @property
    def construction_type(self) -> str:
        return self.con_type

    @property
    def baseline_construction(self):
        return self._get_baseline(self.climate, self.vintage, self.construction_type)

    @staticmethod
    def _get_baseline(c, v, cns):
        """ Get the baseline construction set from the standards lib"""
        cz = 'ClimateZone'
        constr_set = '{}::{}{}::{}'.format(str(v), str(cz), str(c), str(cns))
        return(construction_set_by_identifier(constr_set))

    @property
    def detailed_cons_set(self):
        return self._deconstruct_constr(self.baseline_construction)

    @staticmethod
    def _deconstruct_constr(_constr_set):
        cons_dict = {
            'exterior_wall': _constr_set.wall_set.exterior_construction.to_dict(),
            'exterior_roof': _constr_set.roof_ceiling_set.exterior_construction.to_dict(),
            'exposed_floor': _constr_set.floor_set.exterior_construction.to_dict(),
            'ground_wall': _constr_set.wall_set.ground_construction.to_dict(),
            'ground_roof': _constr_set.roof_ceiling_set.ground_construction.to_dict(),
            'ground_floor': _constr_set.floor_set.ground_construction.to_dict(),
            'window': _constr_set.aperture_set.window_construction.to_dict(),
            'skylight': _constr_set.aperture_set.skylight_construction.to_dict(),
            'operable': _constr_set.aperture_set.operable_construction.to_dict(),
            'exterior_door': _constr_set.door_set.exterior_construction.to_dict(),
            'overhead_door': _constr_set.door_set.overhead_construction.to_dict(),
            'glass_door': _constr_set.door_set.exterior_glass_construction.to_dict()}
        return(cons_dict)


def get_room_programs(bldg_prog, vintage):
    """Simple function to enable functionality
    found in 'HB Search Programs"""

    vintage_subset = STANDARDS_REGISTRY[vintage[-4:]]
    room_programs = vintage_subset[bldg_prog]
    room_prog = ['{}::{}::{}'.format(vintage, bldg_prog, rp) for rp in room_programs]
    return sorted(room_prog)
