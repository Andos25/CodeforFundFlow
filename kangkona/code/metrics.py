# coding=UTF-8
import matplotlib.pyplot as plt
import numpy as np

def relative_error(real, predicted):
    errors = (predicted - real) / real
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
    plt.show()
    print "sum of squared relative errors: ", (relative_errors * relative_errors).sum()
    print "mean of absolute errors: ", np.mean(np.abs(relative_errors))
    print "std of errors: ", np.std(relative_errors)
    
def get_metrics(test, predict):
    relative_errors = relative_error(test, predict)
    return [(relative_errors * relative_errors).sum(), np.mean(np.abs(relative_errors)), np.std(relative_errors)]

def residual_analysis(test, predict):
    residual = test - predict
    
if __name__ == '__main__':
    print np.array([1,2]) * np.array([1,2])