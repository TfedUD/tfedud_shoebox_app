try:  # import the core honeybee dependencies
    from honeybee.boundarycondition import Outdoors
    from honeybee.facetype import Wall
    from honeybee.room import Room
    from honeybee.face import Face
    from honeybee.orientation import check_matching_inputs, angles_from_num_orient, \
        face_orient_index, inputs_by_index
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))


def can_host_apeture(face):
    """Test if a face is intended to host apertures (according to this component)."""
    return isinstance(face.boundary_condition, Outdoors) and \
        isinstance(face.type, Wall)


def assign_apertures(face, sub, rat, hgt, sil, hor, vert, op):
    """Assign apertures to a Face based on a set of inputs."""
    if sub:
        face.apertures_by_ratio_rectangle(rat, hgt, sil, hor, vert, 0.001)
    else:
        face.apertures_by_ratio(rat, tolerance)

    # try to assign the operable property
    if op:
        for ap in face.apertures:
            ap.is_operable = op


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
