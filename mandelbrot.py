'''
Plots the Mandelbrot set.

Usage:
    mandelbrot.py [--centre=X,Y] [[--height=HEIGHT] [--width=WIDTH] | --size=WxH] [--escape-limit=LIMIT]

Options:
    -c X,Y --centre=X,Y            The centre point of the plot [default: 0,0]
    -W WIDTH --width=WIDTH         The horizontal size of the plot [default: 8]
    -H HEIGHT --height=HEIGHT      The vertical size of the plot in pixels [default: 8]
    -s WxH --size=WxH              Size of the plot (combines W and H)
    -e LIMIT --escape-limit=LIMIT  The maximum escape time for each point on the plot [default: 20]
    -h --help                      Show this help screen
'''
import matplotlib as mpl
mpl.use('Agg')
from matplotlib.pyplot import figure, imshow, savefig
from numpy import linspace, reshape, transpose, shape, zeros, array, complex256
from itertools import product
from docopt import docopt

def  mandelorder(C, limit):
    '''
    For creating a colour plot which represents the escape time of each
    point.
    '''
    Z = C
    I = zeros(shape(Z))-1
    for i in range(limit):
        Z = Z**2+C
        escaped = (abs(Z)>2) & (I==-1)
        I[escaped] = i
        Z[escaped] = 0 # prevents overflows
        C[escaped] = 0
    I[I==-1] = i # didn't escape: max value
    return I

if __name__=='__main__':
    arguments = docopt(__doc__)

    centre = tuple(float(a) for a in arguments["--centre"].split(","))
    if arguments["--size"]:
        size = tuple(float(a) for a in arguments["--size"].split("x"))
    else:
        size = (float(arguments["--width"]),
                float(arguments["--height"]))
    limit = int(arguments["--escape-limit"])

    xstart = centre[0]-size[0]/2
    xend = centre[0]+size[0]/2
    ystart = centre[1]-size[1]/2
    yend = centre[1]+size[1]/2
    X = linspace(xstart, xend, 200)
    Y = linspace(ystart, yend, 200)
    C = array([complex(x,y) for x,y in product(X, Y)], dtype=complex256)
    print("Size: {}".format(size))
    print("C: {}".format(shape(C)))
    mset = mandelorder(C, limit)
    print("Mset: {}".format(shape(mset)))
    mset2d = transpose(reshape(mset, (200, 200)))
    print("Img: {}".format(shape(mset2d)))
    extent = [xstart, xend, ystart, yend]
    figure(figsize=(16,12), dpi=200)
    imshow(mset2d, origin='lower', extent=extent, cmap="gray_r")
    # xticks([])
    # yticks([])
    savefig('mandelbrot.png')
