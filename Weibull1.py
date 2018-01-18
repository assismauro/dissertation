import scipy.stats as ss
import matplotlib
matplotlib.use("Qt4Agg")
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from laspy import file
import argparse
import sys
from math import floor
import Tkinter as Tk

def ParseCmdLine():
    parser = argparse.ArgumentParser(description="Some useful features to deal with LiDAR files.",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("inputfname", help="las file to be process.")
    parser.add_argument("-n", "--numberofbins", type=int, help="number of bins (classes) to be used.", default=30)
    parser.add_argument("-v", "--verbose", help="show processing messages.", default=False, action='store_false')
    try:
        args = parser.parse_args()
    except Exception as e:
        print("Unexpected error: ",e)
        sys.exit(1)
    return args

def main():
    args = ParseCmdLine()
    N=args.numberofbins
    '''
    las=file.File(args.inputfname,mode="r")
    Z=las.Z[las.Z > 0]
    binwidth=int((np.max(Z)-np.min(Z))/N)
    counts=dict()
    for val in Z:
        binname = int(floor(val / binwidth) * binwidth)
        if binname not in counts:
            counts[binname] = 0
        counts[binname] += 1
    print counts
    '''
    x = []
    header=True
    with open(r"D:\metrics\NP_T-0482_dn_g_n_ch1_5.csv") as fd:
        for line in fd:
            if header:
                header = False
                continue
            v=line.split(',')[3]
            if (v == '-'):
                continue
            x.append(int(v))

    counts, bins = np.histogram(x, bins=N)
    counts = counts[1:]
    bins = bins[1:]
    bin_width = bins[1]-bins[0]
    total_count = float(sum(counts))

    f, ax = plt.subplots(1, 1)
    f.suptitle("")

    ax.bar(bins[:-1]+bin_width/2., counts, align='center', width=.85*bin_width)
    ax.grid('on')
    def fit_pdf(x, name='lognorm', color='r'):
        dist = getattr(ss, name)  # params = shape, loc, scale
        # dist = ss.gamma  # 3 params

        params = dist.fit(x, loc=0)  # 1-day lag minimum for shipping
        y = dist.pdf(bins, *params)*total_count*bin_width
        sqerror_sum = np.log(sum(ci*(yi - ci)**2. for (ci, yi) in zip(counts, y)))
        ax.plot(bins, y, color, lw=3, alpha=0.6, label='%s   err=%3.2f' % (name, sqerror_sum))
        return y

    colors = ['r-', 'g-', 'r:', 'g:']

    for name, color in zip(['exponweib', 't', 'gamma'], colors): # 'lognorm', 'erlang', 'chi2', 'weibull_min',
        y = fit_pdf(x, name=name, color=color)

    ax.legend(loc='best', frameon=False)
    plt.show()
    Tk.mainloop()

# In[ ]:

if __name__ == "__main__":
    main()
