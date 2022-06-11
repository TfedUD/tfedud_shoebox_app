from honeybee.face import Face
from honeybee import face
import honeybee_energy
import ladybug_geometry
from ladybug_geometry.geometry3d.pointvector import Point3D
from ladybug_geometry.geometry3d.face import Face3D
from ladybug_geometry.geometry3d.pointvector import Point3D, Vector3D
from ladybug_geometry.geometry3d.plane import Plane
from honeybee.face import Face
from honeybee.facetype import face_types, Wall
from honeybee.boundarycondition import boundary_conditions, Outdoors
from honeybee.aperture import Aperture
from honeybee.door import Door
from honeybee.shade import Shade


class FaceObj():
    def __init__(self, _vertx, _vertz):
        self.vx = _vertx
        self.vz = _vertz

    @property
    def my_face(self):
        return(self._makeface(self.vx, self.vz))

    @staticmethod
    def _makeface(_x, _z):
        verts = [Point3D(0, 0, 0), Point3D(_x, 0, 0),
                 Point3D(_x, 0, _z), Point3D(0, 0, _z)]

        obj = Face.from_vertices('my_wall', verts)
        return(obj)
