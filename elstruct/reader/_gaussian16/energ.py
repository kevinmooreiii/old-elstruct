""" electronic energy readers
"""
import autoread as ar
from autoparse import cast as _cast
import autoparse.pattern as app
import autoparse.find as apf
import elstruct.par

PROG = elstruct.par.Program.GAUSSIAN09

DOUB_HYB_DFT = [
    'b2plypd3'
]


def _hf_energy(output_string):
    ene = ar.energy.read(
        output_string,
        app.one_of_these([
            app.escape('E(RHF) ='),
            app.escape('E(UHF) ='),
            app.escape('E(ROHF) =')]))
    return ene


def _mp2_energy(output_string):
    ene_d_str = ar.energy.read(
        output_string,
        app.escape('EUMP2 = '),
        val_ptt=app.EXPONENTIAL_FLOAT_D)
    ene = _cast(apf.replace('d', 'e', ene_d_str, case=False))
    return ene


def _dft_energy(output_string):
    e_pattern = app.escape('E(') + app.VARIABLE_NAME + app.escape(')')
    ene = ar.energy.read(
        output_string,
        start_ptt=app.LINESPACES.join([
            'SCF Done:', e_pattern, '=']))
    return ene


def _doub_hyb_dft_energy(output_string):
    e_pattern = (
        app.escape('E') + app.maybe('2') + app.escape('(') +
        app.one_of_these([dft.upper() for dft in DOUB_HYB_DFT]) +
        app.escape(')')
    )
    dft_pattern = (
        e_pattern + app.SPACES + '=' + app.SPACES +
        app.EXPONENTIAL_FLOAT_D + app.SPACES +
        e_pattern + app.SPACES + '='
    )

    ene = ar.energy.read(
        output_string,
        start_ptt=dft_pattern
        )
    return ene


# a dictionary of functions for reading the energy from the output, by method
ENERGY_READER_DCT = {
    elstruct.par.Method.HF[0]: _hf_energy,
    elstruct.par.Method.Corr.MP2[0]: _mp2_energy,
}

METHODS = elstruct.par.program_methods(PROG)
for METHOD in METHODS:
    if elstruct.par.Method.is_standard_dft(METHOD):
        if METHOD not in DOUB_HYB_DFT:
            ENERGY_READER_DCT[METHOD] = _dft_energy
        else:
            ENERGY_READER_DCT[METHOD] = _doub_hyb_dft_energy


assert all(method in ENERGY_READER_DCT for method in METHODS)


def energy(method, output_string):
    """ get total energy from output
    """

    # get the appropriate reader and call it
    if elstruct.par.Method.is_nonstandard_dft(method):
        if method not in DOUB_HYB_DFT:
            energy_reader = _dft_energy
        else:
            energy_reader = _doub_hyb_dft_energy
    else:
        energy_reader = ENERGY_READER_DCT[method]

    return energy_reader(output_string)


if __name__ == '__main__':
    with open('rb2.out', 'r') as f:
        RF = f.read()
    print(energy('b2plypd3', RF))
