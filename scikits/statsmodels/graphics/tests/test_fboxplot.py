import numpy as np
from numpy.testing import assert_allclose, dec, assert_equal

from scikits.statsmodels.graphics.fboxplot import banddepth, fboxplot


try:
    import matplotlib.pyplot as plt
    have_matplotlib = True
except:
    have_matplotlib = False


def test_banddepth_BD2():
    xx = np.arange(500) / 150.
    y1 = 1 + 0.5 * np.sin(xx)
    y2 = 0.3 + np.sin(xx + np.pi/6)
    y3 = -0.5 + np.sin(xx + np.pi/6)
    y4 = -1 + 0.3 * np.cos(xx + np.pi/6)

    data = np.asarray([y1, y2, y3, y4])
    depth = banddepth(data, method='BD2')
    expected_depth = [0.5, 5./6, 5./6, 0.5]
    assert_allclose(depth, expected_depth)

    ## Plot to visualize why we expect this output
    #fig = plt.figure()
    #ax = fig.add_subplot(111)
    #for ii, yy in enumerate([y1, y2, y3, y4]):
    #    ax.plot(xx, yy, label="y%s" % ii)

    #ax.legend()
    #plt.show()


def test_banddepth_MBD():
    xx = np.arange(5001) / 5000.
    y1 = np.zeros(xx.shape)
    y2 = 2 * xx - 1
    y3 = np.ones(xx.shape) * 0.5
    y4 = np.ones(xx.shape) * -0.25

    data = np.asarray([y1, y2, y3, y4])
    depth = banddepth(data, method='MBD')
    expected_depth = [5./6, (2*(0.75-3./8)+3)/6, 3.5/6, (2*3./8+3)/6]
    assert_allclose(depth, expected_depth, rtol=5e-4)


@dec.skipif(not have_matplotlib)
def test_fboxplot():
    """"""
    def harmfunc(t):
        """Test function, combination of a few harmonic terms."""
        # Constant, 0 with p=0.9, 1 with p=1 - for creating outliers
        ci = int(np.random.random() > 0.9)
        a1i = np.random.random() * 0.05
        a2i = np.random.random() * 0.05
        b1i = (0.15 - 0.1) * np.random.random() + 0.1
        b2i = (0.15 - 0.1) * np.random.random() + 0.1

        func = (1 - ci) * (a1i * np.sin(t) + a2i * np.cos(t)) + \
               ci * (b1i * np.sin(t) + b2i * np.cos(t))

        return func

    np.random.seed(1234567)
    # Some basic test data, Model 6 from Sun and Genton.
    t = np.linspace(0, 2 * np.pi, 250)
    data = []
    for ii in range(20):
        data.append(harmfunc(t))

    # Create a plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    _, depth, depth_ix = fboxplot(data, wfactor=2, ax=ax)
    ax.set_xlabel(r'$t$')
    ax.text(100, 0.16, r'$(1-c_i)\{a_{1i}sin(t)+a_{2i}cos(t)\}+...$')
    ax.set_ylabel(r'$y(t)$')

    expected_ix = np.array([13, 4, 15, 19, 8, 6, 3, 16, 9, 7, 1, 5, 2,
                            12, 17, 11, 14, 10, 0, 18])
    assert_equal(depth_ix, expected_ix)

    plt.close(fig)