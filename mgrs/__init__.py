import ctypes
from typing import Self

from . import core

__version__ = "1.5.0"


class MGRS:
    def __init__(self, mgrs: str):
        self.mgrs = mgrs

    def __str__(self):
        return f"MGRS:{self.mgrs}"

    def __repr__(self):
        return str(self)

    @property
    def precision(self) -> int:
        return (len(self.mgrs) - 5) // 2

    @classmethod
    def from_utm(
        cls,
        zone: int,
        hemisphere: str,
        easting: float,
        northing: float,
        precision: int = 5,
    ) -> Self:
        """Computes the MGRS coordinate of a point given in UTM coordinates.

        Parameters
        ----------
        zone : int
            The UTM zone number.
        hemisphere : str
            The UTM hemisphere. Either 'N' for north or 'S' for south.
        easting : float
            Easting coordinate.
        northing : float
            Northing coordinate.
        precision : int
            The MGRS precision scale, from 0 (least precise) to 5 (most precise). Default is 5.

        Returns
        -------
        mgrs: MGRS
        """
        mgrs = ctypes.create_string_buffer(80)

        hemisphere_encoded = hemisphere.encode("utf-8")

        hemisphere_c = ctypes.c_char(hemisphere_encoded)
        core.rt.Convert_UTM_To_MGRS(
            zone,
            hemisphere_c,
            ctypes.c_double(easting),
            ctypes.c_double(northing),
            precision,
            mgrs,
        )

        return cls(mgrs.value.decode("utf-8"))

    @classmethod
    def from_lat_lon(
        cls,
        latitude: float,
        longitude: float,
        in_degrees: bool = True,
        precision: int = 5,
    ) -> Self:
        """Convert lat/lon coordinates to the encapsulating MGRS zone.

        Parameters
        ----------
        latitude, longitude : float
            Coordinates in degrees or radian.
        in_degrees : bool
            True if coordinates are given in degrees, False if they are in radian. Default is True.
        precision : int = 5
            The MGRS precision scale, from 0 (least precise) to 5 (most precise). Default is 5.

        Returns
        -------
        mgrs: MGRS
            The MGRS zone.
        """
        if in_degrees:
            lat = core.TO_RADIANS(latitude)
            lon = core.TO_RADIANS(longitude)
        else:
            lat = latitude
            lon = longitude

        p = ctypes.create_string_buffer(80)
        core.rt.Convert_Geodetic_To_MGRS(lat, lon, precision, p)
        c = ctypes.string_at(p)
        return cls(mgrs=c.decode("utf-8"))

    def to_latlon(self, in_degrees: bool = True) -> tuple[float, float]:
        """Compute the center of a MGRS in lat/lon coordinate.

        Parameters
        ----------
        in_degrees : bool
            If True, coordinates are given in degrees. If False, they are given in radian. Default is True.

        Returns
        -------
        tuple[float, float]
            Latitude/longitude coordinate.
        """
        plat = ctypes.pointer(ctypes.c_double())
        plon = ctypes.pointer(ctypes.c_double())

        mgrs = self.mgrs.encode("utf-8")

        c = ctypes.string_at(mgrs)
        core.rt.Convert_MGRS_To_Geodetic(c, plat, plon)

        if in_degrees:
            lat = core.TO_DEGREES(plat.contents.value)
            lon = core.TO_DEGREES(plon.contents.value)
        else:
            lat = plat.contents.value
            lon = plon.contents.value
        return (lat, lon)

    def to_utm(self) -> tuple[int, str, float, float]:
        """Convert a MGRS tile to UTM coordinates.

        Returns
        -------
        zone: int
            The UTM zone number.
        hemisphere: str
            The UTM hemisphere. Values are 'N' for north and 'S' for south.
        easting: float
            Easting coordinates in the UTM zone.
        northing: float
            Northing coordinates in the UTM zone.
        """
        mgrs = self.mgrs.encode("utf-8")
        mgrs = ctypes.string_at(mgrs)
        zone = ctypes.pointer(ctypes.c_long())
        hemisphere = ctypes.pointer(ctypes.c_char())
        easting = ctypes.pointer(ctypes.c_double())
        northing = ctypes.pointer(ctypes.c_double())

        core.rt.Convert_MGRS_To_UTM(mgrs, zone, hemisphere, easting, northing)

        return (
            zone.contents.value,
            hemisphere.contents.value.decode("utf-8"),
            easting.contents.value,
            northing.contents.value,
        )
