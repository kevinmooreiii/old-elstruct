""" elstruct parameters
"""
from elstruct import pclass
from elstruct import option


def standard_case(name):
    """ return name with standard capitalization
    """
    return name.lower()


class Module():
    """ elstruct module names """
    WRITER = 'writer'
    READER = 'reader'


class Program():
    """ Programs to be called """
    CFOUR2 = 'cfour2'
    GAUSSIAN09 = 'gaussian09'
    GAUSSIAN16 = 'gaussian16'
    MOLPRO2015 = 'molpro2015'
    MRCC2018 = 'mrcc2018'
    NWCHEM6 = 'nwchem6'
    ORCA4 = 'orca4'
    PSI4 = 'psi4'


def programs():
    """ list the available electronic structure backend programs
    """
    return pclass.all_values(Program)


def is_program(prog):
    """ is this a possible backend program?
    """
    prog = standard_case(prog)
    return prog in programs()


class Method():
    """ electronic structure methods

    (name, {program: singlet name,
                     multiplet name,
                     singlet orb restrictions,
                     multiplet orb restrictions})
    """
    HF = ('hf',
          {Program.CFOUR2: (
              'rhf', 'hf',
              (True,), (False, True)),
           Program.GAUSSIAN09: (
               'hf', 'hf',
               (True,), (False, True)),
           Program.GAUSSIAN16: (
               'hf', 'hf',
               (True,), (False, True)),
           Program.MOLPRO2015: (
               'hf', 'hf',
               (True,), (False, True)),
           Program.MRCC2018: (
               'hf', 'hf',
               (True,), (False, True)),
           Program.ORCA4: (
               'hf', 'uhf',
               (True,), (False, True)),
           Program.PSI4: (
               'hf', 'uhf',
               (True,), (False, True))})

    class Corr():
        """ correlated method names """
        MP2 = ('mp2',
               {Program.CFOUR2: (
                   'mp2', 'mp2',
                   (True,), (False, True)),
                Program.GAUSSIAN09: (
                    'mp2', 'mp2',
                    (True,), (False, True)),
                Program.GAUSSIAN16: (
                    'mp2', 'mp2',
                    (True,), (False, True)),
                Program.MOLPRO2015: (
                    'mp2', 'ump2',
                    (True,), (False, True)),
                Program.MRCC2018: (
                    'mp2', 'mp2',
                    (True,), (False, True)),
                Program.ORCA4: (
                    'mp2', 'mp2',
                    (True,), (False, True)),
                Program.PSI4: (
                    'mp2', 'mp2',
                    (True,), (False, True))})
        CCSD = ('ccsd',
                {Program.CFOUR2: (
                    'ccsd', 'ccsd',
                    (True,), (True,)),
                 Program.MOLPRO2015: (
                     'ccsd', 'uccsd',
                     (True,), (True, True))})
        CCSD_T = ('ccsd(t)',
                  {Program.CFOUR2: (
                      'ccsd(t)', 'ccsd(t)',
                      (True,), (True,)),
                   Program.MOLPRO2015: (
                       'ccsd(t)', 'uccsd(t)',
                       (True,), (True,)),
                   Program.MRCC2018: (
                       'ccsd(t)', 'ccsd(t)',
                       (True,), (True, True))})
        CCSDT = ('ccsdt',
                 {Program.MOLPRO2015: (
                     'mrcc,method=ccsdt', 'mrcc,method=ccsdt',
                     (True,), (False, True)),
                  Program.MRCC2018: (
                      'ccsdt', 'ccsdt',
                      (True,), (True, True))})
        CCSDT_Q = ('ccsdt(q)',
                   {Program.MOLPRO2015: (
                       'mrcc,method=ccsdt(q)', 'mrcc,method=ccsdt(q)',
                       (True,), (False, True)),
                    Program.MRCC2018: (
                        'ccsdt(q)', 'ccsdt(q)',
                        (True,), (True, True))})
        CCSD_T_F12 = ('ccsd(t)-f12',
                      {Program.MOLPRO2015: (
                          'ccsd(t)-f12', 'uccsd(t)-f12',
                          (True,), (True,))})

    class MultiRef():
        """ multireference electronic structure methods
        """
        CASSCF = ('casscf',
                  {Program.MOLPRO2015: (
                      'casscf', 'casscf',
                      (True,), (True, True))})
        CASPT2 = ('caspt2',
                  {Program.MOLPRO2015: (
                      'rs2', 'rs2',
                      (True,), (True, True))})
        CASPT2I = ('caspt2i',
                  {Program.MOLPRO2015: (
                      'rs2', 'rs2',
                      (True,), (True, True))})
        CASPT2C = ('caspt2c',
                   {Program.MOLPRO2015: (
                       'rs2c', 'rs2c',
                       (True,), (True, True))})
        MRCISDQ = ('mrcisd_q',
                   {Program.MOLPRO2015: (
                       'mrci', 'mrci',
                       (True,), (True, True))})

    class Dft():
        """ DFT method names """
        B3LYP = ('b3lyp',
                 {Program.PSI4: (
                     'B3LYP', 'B3LYP',
                     (True,), (False,)),
                  Program.GAUSSIAN09: (
                      'b3lyp', 'b3lyp',
                      (True,), (False,)),
                  Program.GAUSSIAN16: (
                      'b3lyp', 'b3lyp',
                      (True,), (False,))})
        WB97XD = ('wb97xd',
                  {Program.PSI4: (
                      'WB97X-D', 'WB97X-D',
                      (True,), (False,)),
                   Program.GAUSSIAN09: (
                       'wb97xd', 'wb97xd',
                       (True,), (False,)),
                   Program.GAUSSIAN16: (
                       'wb97xd', 'wb97xd',
                       (True,), (False,))})
        M062X = ('m062x',
                 {Program.PSI4: (
                     'M06-2X', 'M06-2X',
                     (True,), (False,)),
                  Program.GAUSSIAN09: (
                      'm062x', 'm062x',
                      (True,), (False,)),
                  Program.GAUSSIAN16: (
                      'm062x', 'm062x',
                      (True,), (False,))})
        B2PLYPD3 = ('b2plypd3',
                    {Program.GAUSSIAN09: (
                        'b2plypd3', 'b2plypd3',
                        (True,), (False,)),
                     Program.GAUSSIAN16: (
                         'b2plypd3', 'b2plypd3',
                         (True,), (False,))})

    @classmethod
    def contains(cls, name):
        """ does this parameter class contain this value?
        """
        name = standard_case(name)
        names = [row[0] for row in pclass.all_values(cls)]
        return name in names

    @classmethod
    def is_correlated(cls, name):
        """ is this a single-reference correlated method?
        """
        name = standard_case(name)
        corr_names = [row[0] for row in pclass.all_values(cls.Corr)]
        return name in corr_names

    @classmethod
    def is_multiref(cls, name):
        """ is this a mulitreference method?
        """
        name = standard_case(name)
        multiref_names = [row[0] for row in pclass.all_values(cls.MultiRef)]
        return name in multiref_names

    @classmethod
    def is_casscf(cls, name):
        """ is the method casscf?
        """
        name = standard_case(name)
        return name == 'casscf'

    @classmethod
    def is_standard_dft(cls, name):
        """ is this a DFT method?
        """
        name = standard_case(name)
        dft_names = [row[0] for row in pclass.all_values(cls.Dft)]
        return name in dft_names

    @staticmethod
    def is_nonstandard_dft(name):
        """ is this a non-standard DFT method?

        (indicated by 'dft:<name>')
        """
        return name.lower().startswith('dft:')

    @classmethod
    def is_dft(cls, name):
        """ is this a (standard or non-standard) DFT method?
        """
        return cls.is_standard_dft(name) or cls.is_nonstandard_dft(name)

    @classmethod
    def nonstandard_dft_name(cls, name):
        """ extract the name of a non-standard basis set

        (indicated by 'dft:<name>')
        """
        assert cls.is_nonstandard_dft(name)
        return name[4:]


def program_methods_info(prog):
    """ list the methods available for a given program, with their information
    """
    prog = standard_case(prog)
    return {row[0]: row[1][prog] for row in pclass.all_values(Method)
            if prog in row[1]}


def program_methods(prog):
    """ list the methods available for a given program
    """
    return tuple(sorted(program_methods_info(prog)))


def program_dft_methods(prog):
    """ list the DFT methods available for a given program
    """
    prog_methods = program_methods(prog)
    return tuple(method for method in prog_methods
                 if Method.is_standard_dft(method))


def program_nondft_methods(prog):
    """ list the DFT methods available for a given program
    """
    prog_methods = program_methods(prog)
    return tuple(method for method in prog_methods
                 if not Method.is_standard_dft(method))


def program_method_name(prog, method, singlet=True):
    """ list the name of a method for a given program
    """
    prog = standard_case(prog)

    if Method.is_nonstandard_dft(method):
        method = Method.nonstandard_dft_name(method)
    else:
        method = standard_case(method)
        prog_method_dct = program_methods_info(prog)
        assert method in prog_method_dct
        name = (prog_method_dct[method][0] if singlet else
                prog_method_dct[method][1])
        method = method if name is None else name

    return method


def program_method_orbital_restrictions(prog, method, singlet):
    """ list the possible orbital restrictions for a given method and program
    """
    prog = standard_case(prog)
    method = standard_case(method)
    prog_method_dct = program_methods_info(prog)
    assert method in prog_method_dct
    orb_restrictions = (prog_method_dct[method][2] if singlet else
                        prog_method_dct[method][3])
    return orb_restrictions


def is_program_method(prog, method):
    """ is this a valid method for this program?
    """
    prog = standard_case(prog)
    method = standard_case(method)
    return method in program_methods(prog)


def is_program_method_orbital_restriction(prog, method, singlet,
                                          orb_restricted):
    """ is this a valid method for this program?
    """
    prog = standard_case(prog)
    method = standard_case(method)
    assert isinstance(singlet, bool)
    return (orb_restricted
            in program_method_orbital_restrictions(prog, method, singlet))


class Basis():
    """ electronic structure basis sets

    (name, {program: name})
    """
    STO3G = ('sto-3g', {Program.CFOUR2: None,
                        Program.GAUSSIAN09: None,
                        Program.GAUSSIAN16: None,
                        Program.MOLPRO2015: None,
                        Program.MRCC2018: None,
                        Program.NWCHEM6: None,
                        Program.ORCA4: None,
                        Program.PSI4: None})

    class Pople:
        """ Pople basis sets """
        P321 = ('3-21g', {Program.CFOUR2: None,
                          Program.GAUSSIAN09: None,
                          Program.GAUSSIAN16: None,
                          Program.MOLPRO2015: None,
                          Program.MRCC2018: None,
                          Program.NWCHEM6: None,
                          Program.ORCA4: None,
                          Program.PSI4: None})
        P631 = ('6-31g', {Program.CFOUR2: None,
                          Program.GAUSSIAN09: None,
                          Program.GAUSSIAN16: None,
                          Program.MOLPRO2015: None,
                          Program.MRCC2018: None,
                          Program.NWCHEM6: None,
                          Program.ORCA4: None,
                          Program.PSI4: None})
        P631S = ('6-31g*', {Program.CFOUR2: None,
                            Program.GAUSSIAN09: None,
                            Program.GAUSSIAN16: None,
                            Program.MOLPRO2015: None,
                            Program.MRCC2018: None,
                            Program.NWCHEM6: None,
                            Program.ORCA4: None,
                            Program.PSI4: None})
        P631PS = ('6-31+g*', {Program.CFOUR2: None,
                              Program.GAUSSIAN09: None,
                              Program.GAUSSIAN16: None,
                              Program.MOLPRO2015: None,
                              Program.MRCC2018: None,
                              Program.NWCHEM6: None,
                              Program.ORCA4: None,
                              Program.PSI4: None})

    class Dunning():
        """ Dunning basis sets """
        D = ('cc-pvdz', {Program.CFOUR2: None,
                         Program.GAUSSIAN09: None,
                         Program.GAUSSIAN16: None,
                         Program.MOLPRO2015: None,
                         Program.MRCC2018: None,
                         Program.NWCHEM6: None,
                         Program.ORCA4: None,
                         Program.PSI4: None})
        T = ('cc-pvtz', {Program.CFOUR2: None,
                         Program.GAUSSIAN09: None,
                         Program.GAUSSIAN16: None,
                         Program.MOLPRO2015: None,
                         Program.MRCC2018: None,
                         Program.NWCHEM6: None,
                         Program.ORCA4: None,
                         Program.PSI4: None})
        Q = ('cc-pvqz', {Program.CFOUR2: None,
                         Program.GAUSSIAN09: None,
                         Program.GAUSSIAN16: None,
                         Program.MOLPRO2015: None,
                         Program.MRCC2018: None,
                         Program.NWCHEM6: None,
                         Program.ORCA4: None,
                         Program.PSI4: None})
        P = ('cc-pv5z', {Program.CFOUR2: None,
                         Program.GAUSSIAN09: None,
                         Program.GAUSSIAN16: None,
                         Program.MOLPRO2015: None,
                         Program.MRCC2018: None,
                         Program.NWCHEM6: None,
                         Program.ORCA4: None,
                         Program.PSI4: None})

        class Aug():
            """ augmented Dunning basis sets """
            AD = ('aug-cc-pvdz', {Program.CFOUR2: None,
                                  Program.GAUSSIAN09: None,
                                  Program.GAUSSIAN16: None,
                                  Program.MOLPRO2015: None,
                                  Program.MRCC2018: None,
                                  Program.NWCHEM6: None,
                                  Program.ORCA4: None,
                                  Program.PSI4: None})
            AT = ('aug-cc-pvtz', {Program.CFOUR2: None,
                                  Program.GAUSSIAN09: None,
                                  Program.GAUSSIAN16: None,
                                  Program.MOLPRO2015: None,
                                  Program.MRCC2018: None,
                                  Program.NWCHEM6: None,
                                  Program.ORCA4: None,
                                  Program.PSI4: None})
            AQ = ('aug-cc-pvqz', {Program.CFOUR2: None,
                                  Program.GAUSSIAN09: None,
                                  Program.GAUSSIAN16: None,
                                  Program.MOLPRO2015: None,
                                  Program.MRCC2018: None,
                                  Program.NWCHEM6: None,
                                  Program.ORCA4: None,
                                  Program.PSI4: None})
            A5 = ('aug-cc-pv5z', {Program.CFOUR2: None,
                                  Program.GAUSSIAN09: None,
                                  Program.GAUSSIAN16: None,
                                  Program.MOLPRO2015: None,
                                  Program.MRCC2018: None,
                                  Program.NWCHEM6: None,
                                  Program.ORCA4: None,
                                  Program.PSI4: None})

        class F12():
            """ Dunning F12 basis sets """
            DF = ('cc-pvdz-f12', {Program.MOLPRO2015: None})
            TF = ('cc-pvtz-f12', {Program.MOLPRO2015: None})
            QF = ('cc-pvqz-f12', {Program.MOLPRO2015: None})

    @classmethod
    def contains(cls, name):
        """ does this parameter class contain this value?
        """
        name = standard_case(name)
        names = [row[0] for row in pclass.all_values(cls)]
        return name in names

    is_standard_basis = contains

    @staticmethod
    def is_nonstandard_basis(name):
        """ is this a non-standard basis set?

        (indicated by 'basis:<name>')
        """
        return name.lower().startswith('basis:')

    @classmethod
    def nonstandard_basis_name(cls, name):
        """ extract the name of a non-standard basis set

        (indicated by 'basis:<name>')
        """
        assert cls.is_nonstandard_basis(name)
        return name[6:]


def program_bases(prog):
    """ list the methods available for a given program
    """
    prog = standard_case(prog)
    return {row[0]: row[1][prog] for row in pclass.all_values(Basis)
            if prog in row[1]}


def program_basis_name(prog, basis):
    """ list the name of a basis for a given program
    """
    prog = standard_case(prog)

    if Basis.is_nonstandard_basis(basis):
        basis = Basis.nonstandard_basis_name(basis)
    else:
        basis = standard_case(basis)
        prog_bases = program_bases(prog)
        assert basis in prog_bases
        name = prog_bases[basis]
        basis = basis if name is None else name

    return basis


def is_program_basis(prog, basis):
    """ is this a valid basis for this program?
    """
    prog = standard_case(prog)
    basis = standard_case(basis)
    return basis in program_bases(prog)


class Job():
    """ The type of job
    """
    ENERGY = 'energy'
    GRADIENT = 'gradient'
    HESSIAN = 'hessian'
    OPTIMIZATION = 'optimization'
    VPT2 = 'vpt2'
    IRC = 'irc'
    PROPERTIES = 'properties'

    @classmethod
    def contains(cls, name):
        """ does this parameter class contain this value?
        """
        name = standard_case(name)
        names = [row for row in pclass.all_values(cls)]
        return name in names


class Error():
    """ Job errors
    """
    SCF_NOCONV = 'scf_noconv'
    CC_NOCONV = 'cc_noconv'
    OPT_NOCONV = 'opt_noconv'
    IRC_NOCONV = 'irc_noconv'


class Success():
    """ Job successes
    """
    SCF_CONV = 'scf_conv'
    CC_CONV = 'cc_conv'
    OPT_CONV = 'opt_conv'
    IRC_CONV = 'irc_conv'



class Option():
    """ Writer option values
    """

    class Scf():
        """ SCF options (passed to `scf_options`) """
        MAXITER_ = option.create('scf_maxiter', ['num'])
        DIIS_ = option.create('scf_diis', ['bool'])

        class Guess():
            """ _ """
            CORE = option.create('scf_guess_core')
            HUCKEL = option.create('scf_guess_huckel')
            MIX = option.create('scf_guess_mix')

    class Casscf():
        """ CASSCF options to set active space (passed to `casscf_options`) """
        OCC_ = option.create('casscf_occ', ['num'])
        CLOSED_ = option.create('casscf_closed', ['num'])
        WFN_ = option.create(
            'casscf_wavefunction', ['nelec', 'sym', 'spin', 'charge'])

    class MRCorr():
        """ Correlated multiref method options (passed to `corr_options`) """
        SHIFT_ = option.create('level_shift', ['num'])

    class Opt():
        """ optimization options (passed to `job_options`) """
        MAXITER_ = option.create('opt_maxiter', ['num'])

        class Coord():
            """ optimization coordinate system """
            CARTESIAN = option.create('opt_coord_cartesian')
            ZMATRIX = option.create('opt_coord_zmatrix')
            REDUNDANT = option.create('opt_coord_redundant')
