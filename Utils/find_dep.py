import numpy as np
import numpy.polynomial.polynomial as poly
from scipy import stats, signal
import matplotlib.pyplot as plt
from kneed import KneeLocator

class FindDep():
    def __init__(self, start_idx=5, log=True, precision=0.1, abs_limit=150):
        self.precision = precision
        self.abs_limit = abs_limit
        self.start_idx = start_idx

    def smooth_data(self, y_lst):
        y_lst = [1/(y*y) for y in y_lst]
        try:
            return smooth_signal(y_lst, 21, 6, self.start_idx)
        except:
            return False

    def increase_data_granularity(self, x_lst, y_smoothed):
        x_lst = np.array(x_lst)
        coeff = poly.polyfit(x_lst[self.start_idx:], y_smoothed, 16)
        x_new = np.arange(x_lst[self.start_idx], max(x_lst), 1)
        y_fit = poly.polyval(x_new, coeff)
        return x_new, y_fit

    def find_knee(self, x_lst, y_lst):
        x_knee = KneeLocator(x_lst, y_lst, S=10.0,
                             curve='concave', direction='increasing').knee
        # y_smoothed = self.smooth_data(y_lst)
        # x_new, y_fit = self.increase_data_granularity(x_lst, y_smoothed)
        # x_knee = KneeLocator(x_new, y_fit, S=10.0,
        #                      curve='concave', direction='increasing').knee
        if x_knee is None:
            print("Knee could not be located")
            return False
        return x_knee

    def find_line_fits(self, x_new, y_fit):
        x_slope = []
        y_slope = []
        x_flat = []
        y_flat = []
        try:
            for tup in [(x, y) for x, y in zip(x_new, y_fit) if x < check_precision("lower", self.precision, x_knee, self.abs_limit)]:
                x_slope.append(tup[0])
                y_slope.append(tup[1])
            coeff_slope = poly.polyfit(x_slope, y_slope, 1)
            t_slope = np.arange(x_lst[start_idx], x_knee*1.5, 1)
            f_slope = poly.polyval(t_slope, coeff_slope)

            for tup in [(x, y) for x, y in zip(x_new, y_fit) if x > check_precision("upper", self.precision, x_knee, self.abs_limit)]:
                x_flat.append(tup[0])
                y_flat.append(tup[1])
            coeff_flat = poly.polyfit(x_flat, y_flat, 1)
            t_flat = np.arange(x_knee*0.7, x_new[-1]*1.3, 1)
            f_flat = poly.polyval(t_flat, coeff_flat)
        except:
            print("Fit did not converge")
            return False
        return [t_slope, f_slope, t_flat, f_flat]


    def find_intersection(self, lst):
        """Finds intersection from list which looks like
            lst (list): [t_slope, f_slope, t_flat, f_flat]
        """
        vdep, _ = line_intersection([(lst[0][0], lst[1][0]),
                                     (lst[0][-1], lst[1][-1])],
                                    [(lst[2][0], lst[3][0]),
                                     (lst[2][-1], lst[3][-1])])
        return vdep



    def plot_result(self, x_lst, y_lst, x_new, y_fit, t_slope, f_slope, t_flat,
                    f_flat, x_knee, vdep):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(x_lst, y_lst, linewidth=4)
        ax.plot(x_new, y_fit)
        ax.plot(t_slope, f_slope)
        ax.plot(t_flat, f_flat)
        # ax.plot(x_new_2, y_fit_2)
        ax.axvline(x_knee, linestyle="--")
        ax.set_xlabel("Voltage (V)",
                     fontsize=14,
                     fontweight="bold")
        ax.set_ylabel("C$^{-2}$ (F$^{-2}$)",
                     fontsize=14,
                     fontweight="bold")

        if vdep is not None:
            ax.axvline(vdep)
        plt.draw()
        plt.show()
        fig = None

        return vdep, x_knee



def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

def smooth_signal(lst, width=51, grade=3, index=0):
    return signal.savgol_filter(lst[index:], width, grade)

def check_precision(direction, prec, knee, abs_limit=150):
    if direction == "upper":
        if (1 + prec)*knee > knee + abs_limit:
            return knee + abs_limit
        return (1 + prec)*knee
    if direction == "lower":
        if (1 - prec)*knee < knee - abs_limit:
            return knee - abs_limit
        return (1 - prec)*knee
