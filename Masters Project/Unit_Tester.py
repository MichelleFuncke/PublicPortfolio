import sys
import numpy as np

def vaugeTest(actual, expected, accuracy):
    """ Compare the actual to the expected value,
        and print a suitable message.
    """
    linenum = sys._getframe(1).f_lineno   # Get the caller's line number.
    if (vaugeTestBody(actual, expected, accuracy)):
        msg = "Test on line {0} passed.".format(linenum)
    else:
        msg = ("Test on line {0} failed. Expected '{1}', but got '{2}'."
                .format(linenum, expected, actual))
    print(msg)


def vaugeTestBody(actual, expected, accuracy):
    """need to cut "actual" down...but still be generic enough to accept any input
    """
    if(isinstance(actual, float)):
        return vaugeEquivalence(actual,expected,accuracy)
    elif(isinstance(actual, int)):
        return actual == expected
    elif(isinstance(actual, complex)):
        real = vaugeEquivalence(float(np.real(actual)),float(np.real(expected)),accuracy)
        imag = vaugeEquivalence(float(np.imag(actual)),float(np.imag(expected)),accuracy)
        return real and imag
    else:
        for i in range(len(actual)):
            if(len(actual) != len(expected) or vaugeTestBody(actual[i],expected[i],accuracy) == False):
                return False
    return True

def vaugeEquivalence(elem1, elem2, accuracy):
    roundingResult1 = round(elem1 , accuracy);
    roundingResult2 = round(elem2 , accuracy);
    return roundingResult1 == roundingResult2

def test(actual, expected):
    """ Compare the actual to the expected value,
        and print a suitable message.
    """
    linenum = sys._getframe(1).f_lineno   # Get the caller's line number.
    if (expected == actual):
        msg = "Test on line {0} passed.".format(linenum)
    else:
        msg = ("Test on line {0} failed. Expected '{1}', but got '{2}'."
                .format(linenum, expected, actual))
    print(msg)
