from ladybug_geometry.geometry2d.pointvector import Vector2D
try:  # import the core honeybee dependencies
    from honeybee.boundarycondition import Outdoors
    from honeybee.facetype import Wall
    from honeybee.room import Room
    from honeybee.face import Face
    from honeybee.orientation import check_matching_inputs, angles_from_num_orient, \
        face_orient_index, inputs_by_index
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))

try:  # import the honeybee-energy extension
    from honeybee_energy.lib.constructions import shade_construction_by_identifier
except ImportError as e:
    if len(ep_constr_) != 0:
        raise ValueError('ep_constr_ has been specified but honeybee-energy '
                         'has failed to import.\n{}'.format(e))

try:  # import the honeybee-radiance extension
    from honeybee_radiance.lib.modifiers import modifier_by_identifier
except ImportError as e:
    if len(rad_mod_) != 0:
        raise ValueError('rad_mod_ has been specified but honeybee-radiance '
                         'has failed to import.\n{}'.format(e))


def can_host_apeture(face):
    """Test if a face is intended to host apertures (according to this component)."""
    return isinstance(face.boundary_condition, Outdoors) and \
        isinstance(face.type, Wall)


def add_aps_by_ratio(_obj, _ratio=[], _subdivide_=[], _win_height_=[], _sill_height_=[],
                     _horiz_separ_=[], vert_separ_=[], operable_=[]):
    # duplicate the initial objects
    obj = _obj.duplicate()

    _subdivide_ = _subdivide_ if len(_subdivide_) != 0 else [True]
    _win_height_ = _win_height_ if len(_win_height_) != 0 else [2.0]
    _sill_height_ = _sill_height_ if len(_sill_height_) != 0 else [
        0.8]
    _horiz_separ_ = _horiz_separ_ if len(_horiz_separ_) != 0 else [
        3.0]
    vert_separ_ = vert_separ_ if len(vert_separ_) != 0 else [0.0]
    operable_ = operable_ if len(operable_) != 0 else [False]

    # gather all of the inputs together
    all_inputs = [_subdivide_, _ratio, _win_height_, _sill_height_, _horiz_separ_,
                  vert_separ_, operable_]
    # ensure matching list lengths across all values
    all_inputs, num_orient = check_matching_inputs(all_inputs)

    # get a list of angles used to categorize the faces
    angles = angles_from_num_orient(num_orient)

    # loop through the input objects and add apertures

    if isinstance(obj, Room):
        for face in obj.faces:
            if can_host_apeture(face):
                orient_i = face_orient_index(face, angles)
                sub, rat, hgt, sil, hor, vert, op = inputs_by_index(
                    orient_i, all_inputs)
                assign_apertures(face, sub, rat, hgt, sil, hor, vert, op)
    return obj


def can_host_apeture(face):
    """Test if a face is intended to host apertures (according to this component)."""
    return isinstance(face.boundary_condition, Outdoors) and \
        isinstance(face.type, Wall)


def assign_apertures(face, sub, rat, hgt, sil, hor, vert, op):
    """Assign apertures to a Face based on a set of inputs."""
    tolerance = 0.000
    if sub:
        face.apertures_by_ratio_rectangle(rat, hgt, sil, hor, vert, 0.001)
    else:
        face.apertures_by_ratio(rat, tolerance)

    # try to assign the operable property
    if op:
        for ap in face.apertures:
            ap.is_operable = op


def can_host_louvers(face):
    """Test if a face is intended to host louvers (according to this component)."""
    return isinstance(face.boundary_condition, Outdoors) and \
        isinstance(face.type, Wall)


def assign_louvers(ap, depth, count, dist, off, angle, vec, flip, indr, ep, rad):
    tolerance = 0.000
    """Assign louvers to an Aperture based on a set of inputs."""
    if depth == 0 or count == 0:
        return None
    if dist is None:
        louvers = ap.louvers_by_count(
            count, depth, off, angle, vec, flip, indr, tolerance)
    else:
        louvers = ap.louvers_by_distance_between(
            dist, depth, off, angle, vec, flip, indr, tolerance, max_count=count)

    # try to assign the energyplus construction
    if ep is not None:
        for shd in louvers:
            shd.properties.energy.construction = ep
    # try to assign the radiance modifier
    if rad is not None:
        for shd in louvers:
            shd.properties.radiance.modifier = rad


def add_louver_shade(
        objs, _depth, _shade_count_=[],
        _dist_between_=[None],
        _facade_offset_=[0],
        _angle_=[0],
        vertical_=[False],
        flip_start_=[False],
        indoor_=[False],
        ep_constr_=[], rad_mod_=[]):

    hb_objs = [obj.duplicate() for obj in objs]

    # set defaults for any blank inputs
    _facade_offset_ = _facade_offset_ if len(_facade_offset_) != 0 else [0.0]
    _angle_ = _angle_ if len(_angle_) != 0 else [0.0]
    flip_start_ = flip_start_ if len(flip_start_) != 0 else [False]
    indoor_ = indoor_ if len(indoor_) != 0 else [False]

    # process the defaults for _shade_count_ vs _dist_between
    if len(_shade_count_) != 0 and len(_dist_between_) != 0:
        pass
    elif len(_shade_count_) == 0 and len(_dist_between_) == 0:
        _shade_count_ = [1]
        _dist_between_ = [None]
    elif len(_shade_count_) != 0:
        _dist_between_ = [None]
    else:
        _shade_count_ = [None]

    # process the vertical_ input into a direction vector
    if len(vertical_) != 0:
        vertical_ = [Vector2D(1, 0) if vert else Vector2D(0, 1)
                     for vert in vertical_]
    else:
        vertical_ = [Vector2D(0, 1)]

    # process the input constructions
    if len(ep_constr_) != 0:
        for i, constr in enumerate(ep_constr_):
            if isinstance(constr, str):
                ep_constr_[i] = shade_construction_by_identifier(constr)
    else:
        ep_constr_ = [None]

    # process the input modifiers
    if len(rad_mod_) != 0:
        for i, mod in enumerate(rad_mod_):
            if isinstance(mod, str):
                rad_mod_[i] = modifier_by_identifier(mod)
    else:
        rad_mod_ = [None]

    # gather all of the inputs together
    all_inputs = [_depth, _shade_count_, _dist_between_, _facade_offset_, _angle_,
                  vertical_, flip_start_, indoor_, ep_constr_, rad_mod_]

    # ensure matching list lengths across all values
    all_inputs, num_orient = check_matching_inputs(all_inputs)

    # get a list of angles used to categorize the faces
    angles = angles_from_num_orient(num_orient)

    # loop through the input objects and add apertures
    for obj in hb_objs:
        if isinstance(obj, Room):
            for face in obj.faces:
                if can_host_louvers(face):
                    orient_i = face_orient_index(face, angles)
                    depth, count, dist, off, angle, vec, flip, indr, con, mod = \
                        inputs_by_index(orient_i, all_inputs)
                    for ap in face.apertures:
                        assign_louvers(ap, depth, count, dist, off, angle, vec,
                                       flip, indr, con, mod)
        elif isinstance(obj, Face):
            if can_host_louvers(obj):
                orient_i = face_orient_index(obj, angles)
                depth, count, dist, off, angle, vec, flip, indr, con, mod = \
                    inputs_by_index(orient_i, all_inputs)
                for ap in obj.apertures:
                    assign_louvers(ap, depth, count, dist, off, angle, vec,
                                   flip, indr, con, mod)
        elif isinstance(obj, Aperture):
            orient_i = face_orient_index(obj, angles)
            depth, count, dist, off, angle, vec, flip, indr, con, mod = \
                inputs_by_index(orient_i, all_inputs)
            assign_louvers(obj, depth, count, dist, off, angle, vec, flip,
                           indr, con, mod)
        else:
            raise TypeError(
                'Input _hb_objs must be a Room, Face, or Aperture. Not {}.'.format(
                    type(obj)))

    return hb_objs[0]
