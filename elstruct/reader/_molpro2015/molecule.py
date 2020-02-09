""" molecular geometry and structure readers
"""
import numpy
import autoread as ar
import autoparse.pattern as app
import autoparse.find as apf
import automol


MOLPRO_ENTRY_START_PATTERN = (
    'SETTING' + app.not_followed_by(app.padded('MOLPRO_ENERGY'))
)


def opt_geometry(output_string):
    """ get optimized geometry from output
    """
    ptt = app.padded(app.NEWLINE).join([
        app.escape('Current geometry (xyz format, in Angstrom)'),
        '',
        app.UNSIGNED_INTEGER,
        (app.one_or_more(app.NONNEWLINE) + app.SPACES +
         'ENERGY=' + app.FLOAT),
        ''
    ])
    # app.padded(app.NEWLINE).join([
    #     app.escape('ATOMIC COORDINATES'),
    #     app.LINE, app.LINE, app.LINE, '']),

    syms, xyzs = ar.geom.read(
        output_string,
        start_ptt=ptt)
        # line_start_ptt=(app.LETTER + app.maybe(app.LETTER)))
    geo = automol.geom.from_data(syms, xyzs, angstrom=True)
    return geo


def hess_geometry(output_string):
    """ get the geometry associated with a hessian calculation
        so that the two are in the same coordinate system.
        this is needed to project properly
    """
    syms, xyzs = ar.geom.read(
        output_string,
        start_ptt=app.padded(app.NEWLINE).join([
            app.escape('ATOMIC COORDINATES'),
            app.LINE, app.LINE, app.LINE, '']),
        line_start_ptt=app.UNSIGNED_INTEGER,
        line_sep_ptt=app.FLOAT,)
    geo = automol.geom.from_data(syms, xyzs, angstrom=False)
    return geo


def opt_zmatrix(output_string):
    """ get optimized z-matrix geometry from output
    """
    # read the matrix from the beginning of the output
    syms, key_mat, name_mat = ar.zmatrix.matrix.read(
        output_string,
        start_ptt=app.maybe(app.SPACES).join([
            'geometry', app.escape('='), app.escape('{'), '']),
        entry_start_ptt=app.maybe(','),
        entry_sep_ptt=',',
        last=False,
        case=False)

    # read the initial z-matrix values from the beginning out the output
    if len(syms) == 1:
        val_dct = {}
    else:
        val_dct = ar.zmatrix.setval.read(
            output_string,
            # name_ptt=MOLPRO_VAR_NAME_PATTERN,
            entry_start_ptt=MOLPRO_ENTRY_START_PATTERN,
            val_ptt=app.one_of_these([app.EXPONENTIAL_FLOAT_D, app.NUMBER]),
            last=True,
            case=False)
        print('val_dct:', val_dct)

    names = sorted(set(numpy.ravel(name_mat)) - {None})
    caps_names = list(map(str.upper, names))
    name_dct = dict(zip(caps_names, names))
    assert set(caps_names) <= set(val_dct)
    val_dct = {name_dct[caps_name]: val_dct[caps_name]
               for caps_name in caps_names}

    # read optimized z-matrix values from the end of the output
    VAR_STRING = app.one_of_these([
        app.padded('Optimized variables'),
        app.padded('Current variables')
    ])
    opt_val_dct = ar.zmatrix.setval.read(
        output_string,
        start_ptt=VAR_STRING + app.NEWLINE,
        entry_end_ptt=app.one_of_these(['ANGSTROM', 'DEGREE']),
        last=True,
        case=False)
    opt_val_dct = {name_dct[caps_name]: opt_val_dct[caps_name]
                   for caps_name in opt_val_dct.keys()}
    assert set(opt_val_dct) <= set(val_dct)
    val_dct.update(opt_val_dct)

    # call the automol constructor
    zma = automol.zmatrix.from_data(
        syms, key_mat, name_mat, val_dct,
        one_indexed=True, angstrom=True, degree=True)
    return zma


if __name__ == '__main__':
    # with open('output.dat') as f:
    #     out_str = f.read()
    # geo = opt_geometry(out_str)
    # print(automol.geom.string(geo))
    with open('run.out') as f:
        out_str = f.read()
    zmat = opt_zmatrix(out_str)
    print(automol.zmatrix.string(zmat))
