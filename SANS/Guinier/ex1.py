import numpy as np
import matplotlib.pyplot as plt

filenames = [
"/HFIR/CG2/IPTS-0828/exp158/Shared/CG2_exp158_scan0039_0001_Iq.txt",
"/HFIR/CG2/IPTS-0828/exp184/Shared/Reduced/CG2_exp184_scan0022_0001_Iq.txt",
"/HFIR/CG2/IPTS-0828/exp184/Shared/Reduced/CG2_exp184_scan0029_0001_Iq.txt",
"/HFIR/CG2/IPTS-0828/exp184/Shared/Reduced/CG2_exp184_scan0023_0001_Iq.txt",
"/HFIR/CG2/IPTS-0828/exp184/Shared/Reduced_ric/CG2_exp184_scan0022_0001_Iq.txt",
]

for f in filenames:
    data = np.genfromtxt(
        #"Si_8m12A_abs_1.txt",
        f,
        skip_header=2,
        #delimiter=",",
    )

    # let's just get the interval: 20-30 first points
    # x = data[20:30, 0]
    # y = data[20:30, 1]
    
    print(f)
    print(data)
    x = data[:, 0]
    y = data[:, 1]


    plt.figure("Raw data")
    plt.plot(x, y)


    # I(Q) = I0 * exp(-Q^2*Rg^2 / 3)
    # log(I(Q)) = log(I0) + (-Q^2*Rg^2 / 3) <=>
    # log(I(Q)) = log(I0) - Rg^2/3 * Q^2
    # => Rg = np.sqrt( 3 * b )

    x_guinier = np.square(x)
    y_guinier = np.log(y)

    # fit data with a polynomial of degree 1: ax+b=0
    # p = [a, b]
    p = np.polyfit(x_guinier, y_guinier, 1)
    y_fitted = np.polyval(p, x_guinier)


    plt.figure("Guinier plot")
    plt.plot(x_guinier, y_guinier, 'o', label="raw")
    plt.plot(x_guinier, y_fitted, label="fitted")

    print("Rg = {}".format(np.sqrt(3 * p[1])))

    plt.show()
