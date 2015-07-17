#Original file taken from UCSF written by Lin Shao <shaol@janelia.hhmi.org>
#Edit by Ian Dobbie ian.dobbie@bioch.ox.ac.uk to remove Priithon dependence
#so it works on the Oxford python installs.
#v1.0 20150609 IMD



import sys

import numpy as N
import Mrc
import matplotlib.pyplot as plt

def makematrix(nphases):
    sepmat = N.zeros((nphases,nphases)).astype(N.float32)
    if nphases<1 or nphases>5:
        s = raw_input('In makematrix(), nphases is either >5 or <1. Are you sure you want to continue?')
        if s=='y' or s=='Y':
            pass
        else:
            return -1

    norders = (nphases+1)/2
    phi = 2*N.pi/nphases
    for j in range(nphases):
        sepmat[0, j] = 1.0/nphases
        for order in range(1,norders):
            sepmat[2*order-1,j] = 2.0 * N.cos(j*order*phi)/nphases
            sepmat[2*order  ,j] = 2.0 * N.sin(j*order*phi)/nphases

    return sepmat

def doit(indat, peakx, peaky, background=1000, nphases=5):
    '''returns peak, mag, phase, sepArr'''

    nz, ny, nx = indat.shape
    phaseArr = N.sum(N.sum(indat-background, 2),1)
    phaseArr = N.reshape(phaseArr, (-1, nphases)).astype(N.float32)
    sepmat = makematrix(nphases)
    sepArr = N.dot(sepmat, phaseArr.transpose())
    mag = N.zeros((nphases/2+1, nz/nphases)).astype(N.float32)
    phi = N.zeros((nphases/2+1, nz/nphases)).astype(N.float32)
    mag[0] = sepArr[0]
    
    for order in range (1,3):
        mag[order] = N.sqrt(sepArr[2*order-1]**2 + sepArr[2*order]**2)
        phi[order] = N.arctan2(sepArr[2*order], sepArr[2*order-1])
    peak = N.reshape(indat[:,peaky,peakx], (-1, nphases))
    peak = N.average(peak, 1)

    peak -= peak.min()
    peak *= mag[1].max()/peak.max()
    return peak, mag, phi, sepArr

def main():
    try:
        infile=sys.argv[1]
    except IndexError:
        infile = raw_input("Input file = ")

    try:
        indat = Mrc.bindFile(infile)
    except IOError:
        print "File %s does not exist or is no readable.\n Quit" % infile
        sys.exit(1)

    
    nz, ny, nx = indat.shape
    centredat = indat[:,3*ny/8:5*ny/8,3*nx/8:5*nx/8]
    peakpos = N.argmax(centredat)
    slicesize = (nx/4)*(ny/4)
    slicepos = peakpos % slicesize
    xoffset = slicepos % (nx/4)
    xpos = xoffset +(3*nx/8)
    ypos = ((slicepos - xoffset)/ (nx/4))+(3*ny/8)

    peakx = xpos
    peaky = ypos

    st = raw_input("peaks coordinates [%s,%s]= " % (peakx,peaky))
    if (st != "" ):
        try:
            peakx, peaky = map(int, st.split(','))
        except ValueError:
            print "peaks coordinates \"%s\" is invalid" % st
            sys.exit(1)

    #estimate background from the mean in the 4 corners,
    #1/10th of image in each corner
    
    bkg = [N.mean(indat[:,:nx/10,:ny/10]),
           N.mean(indat[:,:-nx/10,:ny/10]),
           N.mean(indat[:,:-nx/10,:-ny/10]),
           N.mean(indat[:,:nx/10,:-ny/10])]
    background= N.min(bkg)
                    
    st = raw_input("background to subtract [%s] = " % background )
    if (st != "" ):
        try:
            background = float(st)
        except ValueError:
            print "background value \"%s\" is invalid" % st
            sys.exit(1)
            
    nphases = 5
    st = raw_input("number of phases [%s]= " % nphases)
    if (st != "" ):
        try:
            nphases = int(st)
        except ValueError:
            print "number of phases \"%s\" is invalid" % st
            sys.exit(1)
            
    
    p, m, ph, separr=doit(indat, peakx, peaky, background, nphases)
    plt.plot(p[1:],'-', hold=1)
    plt.plot(m[1,1:],'-', hold=1)
    plt.plot(m[2,1:],'-', hold=1)
    plt.show()

if  __name__ == '__main__':
    try:
        import wx
        if wx.GetApp():
            main()
        else:
            import sys
            sys.app = wx.PySimpleApp()
            main()
            sys.app.MainLoop()
    except:
        print "Plot window cannot be opened. \n Make sure you're using an X terminal and use 'ssh -Y' if doing this remotely from a Windows or Mac."
