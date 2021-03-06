""" property readers
"""

from autoparse import pattern as app
from autoparse import find as apf


def dipole_moment(output_string):
    """
    Reads the dipole moment
    """
    pattern = app.padded(
        (app.LINESPACES.join([
            app.escape('Dipole moment [Debye]:'), app.FLOAT])) +
        app.NEWLINE +
        app.padded('x=') + app.capturing(app.FLOAT) +
        app.padded('y=') + app.capturing(app.FLOAT) +
        app.padded('z=') + app.capturing(app.FLOAT))
    vals = [float(val)
            for val in apf.last_capture(pattern, output_string)]
    return vals
