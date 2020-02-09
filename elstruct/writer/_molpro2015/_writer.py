""" molpro2015 writer module """
import os
import automol
import autowrite as aw
import elstruct.par
import elstruct.option
from elstruct import template
from elstruct.writer._molpro2015 import par

PROG = elstruct.par.Program.MOLPRO2015

# set the path to the template files
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_DIR = os.path.join(THIS_DIR, 'templates')


# mako template keys
class Molpro2015Reference():
    """ _ """
    RHF = 'rhf'
    UHF = 'uhf'


class Molpro2015MultiReference():
    """ _ """
    CASSCF = 'casscf'
    CASPT2 = 'rs2'
    CASPT2I = 'rs2'
    CASPT2C = 'rs2c'
    MRCI_Q = 'mrci'


class JobKey():
    """ _ """
    ENERGY = 'energy'
    OPTIMIZATION = 'optimization'
    GRADIENT = 'gradient'
    HESSIAN = 'hessian'


class TemplateKey():
    """ mako template keys """
    # machine
    COMMENT = 'comment'
    MEMORY_MW = 'memory_mw'
    MACHINE_OPTIONS = 'machine_options'
    # theoretical method
    BASIS = 'basis'
    SCF_METHOD = 'scf_method'
    SCF_OPTIONS = 'scf_options'
    ISMULTIREF = 'ismultiref'
    CASSCF_OPTIONS = 'casscf_options'
    CORR_METHOD = 'corr_method'
    CORR_OPTIONS = 'corr_options'
    # molecule / state
    MOL_OPTIONS = 'mol_options'
    CHARGE = 'charge'
    SPIN = 'spin'
    GEOM = 'geom'
    ZMAT_VALS = 'zmat_vals'
    # job
    COMMENT = 'comment'
    JOB_KEY = 'job_key'
    JOB_OPTIONS = 'job_options'
    GEN_LINES_1 = 'gen_lines_1'
    GEN_LINES_2 = 'gen_lines_2'


def energy(geom, charge, mult, method, basis,
           # molecule options
           mol_options=(),
           # machine options
           memory=1, comment='', machine_options=(),
           # theory options
           orb_restricted=None,
           scf_options=(), casscf_options=(), corr_options=(),
           # generic options
           gen_lines=None):
    """ energy input string
    """
    job_key = JobKey.ENERGY
    fill_dct = _fillvalue_dictionary(
        job_key=job_key, method=method, basis=basis, geom=geom, mult=mult,
        charge=charge, orb_restricted=orb_restricted,
        mol_options=mol_options,
        memory=memory, comment=comment, machine_options=machine_options,
        scf_options=scf_options, casscf_options=casscf_options,
        corr_options=corr_options,
        gen_lines=gen_lines,
    )
    inp_str = template.read_and_fill(TEMPLATE_DIR, 'all.mako', fill_dct)
    return inp_str


def gradient(geom, charge, mult, method, basis,
             # molecule options
             mol_options=(),
             # machine options
             memory=1, comment='', machine_options=(),
             # theory options
             orb_restricted=None,
             scf_options=(), casscf_options=(), corr_options=(),
             # generic options
             gen_lines=None,
             # job options
             job_options=()):
    """ gradient input string
    """
    job_key = JobKey.GRADIENT
    fill_dct = _fillvalue_dictionary(
        job_key=job_key, method=method, basis=basis, geom=geom, mult=mult,
        charge=charge, orb_restricted=orb_restricted, mol_options=mol_options,
        memory=memory, comment=comment, machine_options=machine_options,
        scf_options=scf_options, casscf_options=casscf_options,
        corr_options=corr_options,
        job_options=job_options, gen_lines=gen_lines,
    )
    inp_str = template.read_and_fill(TEMPLATE_DIR, 'all.mako', fill_dct)
    return inp_str


def hessian(geom, charge, mult, method, basis,
            # molecule options
            mol_options=(),
            # machine options
            memory=1, comment='', machine_options=(),
            # theory options
            orb_restricted=None,
            scf_options=(), casscf_options=(), corr_options=(),
            # generic options
            gen_lines=None,
            # job options
            job_options=()):
    """ hessian input string
    """
    job_key = JobKey.HESSIAN
    fill_dct = _fillvalue_dictionary(
        job_key=job_key, method=method, basis=basis, geom=geom, mult=mult,
        charge=charge, orb_restricted=orb_restricted, mol_options=mol_options,
        memory=memory, comment=comment, machine_options=machine_options,
        scf_options=scf_options, casscf_options=casscf_options,
        corr_options=corr_options,
        job_options=job_options, gen_lines=gen_lines,
    )
    inp_str = template.read_and_fill(TEMPLATE_DIR, 'all.mako', fill_dct)
    return inp_str


def optimization(geom, charge, mult, method, basis,
                 # molecule options
                 mol_options=(),
                 # machine options
                 memory=1, comment='', machine_options=(),
                 # theory options
                 orb_restricted=None,
                 scf_options=(), casscf_options=(), corr_options=(),
                 # generic options
                 gen_lines=None,
                 # job options
                 job_options=(), frozen_coordinates=(), saddle=False):
    """ optimization input string
    """
    job_key = JobKey.OPTIMIZATION
    fill_dct = _fillvalue_dictionary(
        job_key=job_key, method=method, basis=basis, geom=geom, mult=mult,
        charge=charge, orb_restricted=orb_restricted, mol_options=mol_options,
        memory=memory, comment=comment, machine_options=machine_options,
        scf_options=scf_options, casscf_options=casscf_options,
        corr_options=corr_options,
        gen_lines=gen_lines,
        frozen_coordinates=frozen_coordinates, job_options=job_options,
        saddle=saddle
    )
    inp_str = template.read_and_fill(TEMPLATE_DIR, 'all.mako', fill_dct)
    return inp_str


# helper functions
def _fillvalue_dictionary(job_key, method, basis, geom, mult, charge,
                          orb_restricted, mol_options, memory, comment,
                          machine_options,
                          scf_options, casscf_options, corr_options,
                          job_options=(), frozen_coordinates=(),
                          saddle=False,
                          gen_lines=None):

    # Set the spin
    singlet = (mult == 1)
    spin = mult - 1

    # Set the reference
    molpro_scf_method = (Molpro2015Reference.RHF if orb_restricted else
                         Molpro2015Reference.UHF)

    # set correlated method; check if multiref
    molpro_corr_method, ismultiref = _set_method(method, singlet)

    # Set the basis
    molpro_basis = elstruct.par.program_basis_name(PROG, basis)

    # Set the geometry
    geom_str, zmat_val_str = _geometry_strings(geom)

    # Set the memory; convert from GB to MW
    memory_mw = int(memory * (1024.0 / 8.0))

    # Set the job directives and options
    scf_options = _evaluate_options(scf_options)
    casscf_options = _evaluate_options(casscf_options)
    corr_options = _evaluate_options(corr_options)
    job_options = _evaluate_options(job_options)

    # Make no scf method if calling a multiref method
    if ismultiref:
        molpro_scf_method = ''
        scf_options = []

    if saddle:
        job_options += ('root=2',)

    job_directives = [','.join(job_options)]
    if frozen_coordinates:
        job_directives.append('inactive,' + ','.join(frozen_coordinates))

    if job_key == 'hessian':
        job_directives.append('print,hessian,low=5')

    # Set the gen lines blocks
    if gen_lines is not None:
        gen_lines_1 = '\n'.join(gen_lines[1]) if 1 in gen_lines else ''
        gen_lines_2 = '\n'.join(gen_lines[2]) if 2 in gen_lines else ''
    else:
        gen_lines_1 = ''
        gen_lines_2 = ''

    # Create a dictionary to fille the template
    fill_dct = {
        TemplateKey.JOB_KEY: job_key,
        TemplateKey.COMMENT: comment,
        TemplateKey.MEMORY_MW: memory_mw,
        TemplateKey.MACHINE_OPTIONS: '\n'.join(machine_options),
        TemplateKey.MOL_OPTIONS: '\n'.join(mol_options),
        TemplateKey.GEOM: geom_str,
        TemplateKey.ZMAT_VALS: zmat_val_str,
        TemplateKey.CHARGE: charge,
        TemplateKey.SPIN: spin,
        TemplateKey.BASIS: molpro_basis,
        TemplateKey.SCF_METHOD: molpro_scf_method,
        TemplateKey.SCF_OPTIONS: ','.join(scf_options),
        TemplateKey.ISMULTIREF: ismultiref,
        TemplateKey.CASSCF_OPTIONS: '\n'.join(casscf_options),
        TemplateKey.CORR_METHOD: molpro_corr_method,
        TemplateKey.CORR_OPTIONS: ','.join(corr_options),
        TemplateKey.JOB_OPTIONS: ';'.join(job_directives),
        TemplateKey.GEN_LINES_1: gen_lines_1,
        TemplateKey.GEN_LINES_2: gen_lines_2
    }

    return fill_dct


def _set_method(method, singlet):
    # Check if MultiReference Method; then check if casscf
    if elstruct.par.Method.is_multiref(method):
        ismultiref = True
        if elstruct.par.Method.is_casscf(method):
            corr_method = ''
        else:
            corr_method = elstruct.par.program_method_name(
                PROG, method, singlet)
    # Set methods if single reference
    else:
        ismultiref = False
        if elstruct.par.Method.is_correlated(method):
            corr_method = elstruct.par.program_method_name(
                PROG, method, singlet)
        else:
            corr_method = ''

    return corr_method, ismultiref


def _geometry_strings(geom):
    if automol.geom.is_valid(geom):
        geom_str = automol.geom.string(geom)
        zmat_val_str = ''
    elif automol.zmatrix.is_valid(geom):
        zma = geom
        syms = automol.zmatrix.symbols(zma)
        key_mat = automol.zmatrix.key_matrix(zma, shift=1)
        name_mat = automol.zmatrix.name_matrix(zma)
        val_dct = automol.zmatrix.values(zma, angstrom=True, degree=True)

        geom_str = aw.zmatrix.matrix_block(syms, key_mat, name_mat, delim=', ')
        zmat_val_str = aw.zmatrix.setval_block(val_dct)
    elif geom == 'GEOMETRY':
        geom_str = geom
        zmat_val_str = ''
    else:
        raise ValueError("Invalid geometry value:\n{}".format(geom))

    return geom_str, zmat_val_str


def _evaluate_options(opts):
    opts = list(opts)
    for idx, opt in enumerate(opts):
        if elstruct.option.is_valid(opt):
            name = elstruct.option.name(opt)
            assert name in par.OPTION_NAMES
            opts[idx] = par.MOLPRO2015_OPTION_EVAL_DCT[name](opt)
    return tuple(opts)
