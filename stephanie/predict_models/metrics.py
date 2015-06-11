# coding=UTF-8
import matplotlib.pyplot as plt
import numpy as np

def relative_error(real, predicted):
    errors = (real - predicted) / real
    return errors

def data_compare(test, predict):
    plt.plot(test, label='real data')
    plt.plot(predict, label='predict data')
    plt.legend()
    plt.title('data compare')
    plt.grid()
    plt.show()
    
def error_plot(test, predict, title):
    relative_errors = relative_error(test, predict)
    plt.plot(relative_errors, label='errors')
    plt.axhline(y=.3)
    plt.axhline(y=-.3)
    plt.legend()
    plt.title(str(title))
    plt.grid()
#     plt.show()
    print "sum of squared relative errors: ", (relative_errors * relative_errors).sum()
    print "mean of absolute errors: ", np.mean(np.abs(relative_errors))
    print "std of errors: ", np.std(relative_errors)
    
if __name__ == '__main__':
    pass