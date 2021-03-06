""" status checkers
"""
import elstruct.par
import autoparse.pattern as app
import autoparse.find as apf


# Exit message for the program
def has_normal_exit_message(output_string):
    """ does this output string have a normal exit message?
    """
    pattern = app.padded(app.NEWLINE).join([
        app.escape('Molpro calculation terminated'),
        app.escape('Variable memory released')])
    return apf.has_match(pattern, output_string, case=False)


# Parsers for convergence success messages
def _has_scf_convergence_message(output_string):
    """ does this output string have a convergence success message?
    """
    scf_str1 = (
        'Initial convergence to {} achieved.  Increase integral accuracy.' +
        app.LINE_FILL + app.NEWLINE + app.LINE_FILL + app.escape('SCF Done:')
    ).format(app.EXPONENTIAL_FLOAT_D)
    scf_str2 = app.escape('Rotation gradient small -- convergence achieved.')
    scf_str3 = app.escape('The problem occurs in Multi')
    scf_str4 = app.escape('The problem occurs in cipro')
    pattern = app.one_of_these([scf_str1, scf_str2, scf_str3, scf_str4])
    return apf.has_match(pattern, output_string, case=False)


def _has_opt_convergence_message(output_string):
    """ does this output string have a convergence success message?
    """
    pattern = (
        app.escape('Optimization completed.') +
        app.LINE_FILL + app.NEWLINE + app.LINE_FILL +
        app.escape('-- Stationary point found.')
    )
    return apf.has_match(pattern, output_string, case=False)


# Parsers for various error messages
def _has_scf_nonconvergence_error_message(output_string):
    """ does this output string have an SCF non-convergence message?
    """
    pattern = app.escape('No convergence') + app.not_followed_by(
        app.padded('in max. number of iterations'))
    return apf.has_match(pattern, output_string, case=False)


def _has_opt_nonconvergence_error_message(output_string):
    """ does this output string have an optimization non-convergence message?
    """
    # First check for scf convergence issues
    if _has_scf_nonconvergence_error_message(output_string):
        error = True
    else:
        pattern = app.escape('No convergence in max. number of iterations')
        error = apf.has_match(pattern, output_string, case=False)
    return error


ERROR_READER_DCT = {
    elstruct.par.Error.SCF_NOCONV: _has_scf_nonconvergence_error_message,
    elstruct.par.Error.OPT_NOCONV: _has_opt_nonconvergence_error_message,
}
SUCCESS_READER_DCT = {
    elstruct.par.Success.SCF_CONV: _has_scf_convergence_message,
    elstruct.par.Success.OPT_CONV: _has_opt_convergence_message,
}


def error_list():
    """ list of errors that be identified from the output file
    """
    return tuple(sorted(ERROR_READER_DCT.keys()))


def success_list():
    """ list of successs that be identified from the output file
    """
    return tuple(sorted(SUCCESS_READER_DCT.keys()))


def has_error_message(error, output_string):
    """ does this output string have an error message?
    """
    assert error in error_list()
    # get the appropriate reader and call it
    error_reader = ERROR_READER_DCT[error]
    return error_reader(output_string)


def check_convergence_messages(error, success, output_string):
    """ check if error messages should trigger job success or failure
    """
    assert error in error_list()
    assert success in success_list()

    job_success = True
    #print('check conv test:', error, error_list, ERROR_READER_DCT)
    #print('success in check_conv:', success, success_list)
    has_error = ERROR_READER_DCT[error](output_string)
    if has_error:
        job_success = False

    return job_success
