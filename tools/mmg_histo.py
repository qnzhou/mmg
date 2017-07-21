#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import sys,re

xmin_qual=0.
xmax_qual=1

xmin_len=0.
xmax_len=2.3

# Plot the quality histogram of input binned data with y as weights and x as
# abscisses. Save this histo in the casename_qual.png file.
def plotQualHisto(x,y,wrst,mean,best,casename):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plt.xlim([xmin_qual,xmax_qual+0.1])
    plt.ylim([0,100])
    plt.locator_params(axis='y', nticks=10)
    plt.locator_params(axis='x', nticks=20)

    ax1.set_title(casename + " element qualities")
    ax1.set_xlabel('Quality')
    ax1.set_ylabel('% Elements')
    plt.xticks(np.arange(xmin_qual,xmax_qual,(xmax_qual-xmin_qual)/10))

    bins = []
    for i in range(len(x)):
        bins.append(list(x[i]))
        bins[i].append(xmax_qual)

    # plot histo
    for i in range(len(x)):
        ax1.hist(x[i],bins[i],range=(xmin_qual,xmax_qual),weights=y[i],alpha=0.5)

        # plot wrst, mean,best
        ax1.axvline(x=wrst[i], linewidth=2, color='r')
        ax1.axvline(x=mean[i], linewidth=2, color='g')
        ax1.axvline(x=best[i], linewidth=2, color='b')
        mystr = "stat"+str(i)+":\n"+str(wrst[i])
        ax1.annotate(mystr,xy=(wrst[i]+0.01,45+i*10),color='r',fontsize=8)
        mystr = "stat"+str(i)+":\n"+str(mean[i])
        ax1.annotate(mystr,xy=(mean[i]+0.01,60+i*10),color='g',fontsize=8)
        mystr = "stat"+str(i)+":\n"+str(best[i])
        ax1.annotate(mystr ,xy=(best[i]+0.01,75+i*10),color='b',fontsize=8)

    # save fig
    fig.savefig(casename+"_qual.png")
    plt.close()

# Plot the lengths histogram of input binned data with y as weights and x as
# abscisses. Save this histo in the casename_len.png file.
def plotLenHisto(x,y,small,mean,large,casename):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    maxlarge = 0
    for val in large:
        maxlarge = max(maxlarge,val)

    plt.xlim([xmin_len,int(maxlarge)+1])
    plt.ylim([0,100])
    ax1.set_title(casename + " edge length")

    ax1.set_xlabel('Lengths')
    ax1.set_ylabel('% Edges')
    plt.xticks(np.arange(xmin_len,maxlarge,(maxlarge-xmin_len)/10))

    bins = []
    for i in range(len(x)):
        bins.append(list(x[i]))
        bins[i].append(xmax_len)

    for i in range(len(x)):
        ax1.hist(x[i],bins[i],range=(xmin_len,xmax_len),weights=y[i],alpha=0.5)

        # plot wrst, mean,best
        ax1.axvline(x=small[i], linewidth=2, color='r')
        ax1.axvline(x=mean[i] , linewidth=2, color='g')
        ax1.axvline(x=large[i], linewidth=2, color='b')
        mystr = "stat"+str(i)+":\n"+str(small[i])
        ax1.annotate(mystr,xy=(small[i]+0.01,45+i*10),color='r',fontsize=8)
        mystr = "stat"+str(i)+":\n"+str(mean[i])
        ax1.annotate(mystr,xy=(mean[i]+0.01,60+i*10),color='g',fontsize=8)
        mystr = "stat"+str(i)+":\n"+str(large[i])
        ax1.annotate(mystr,xy=(large[i]+0.01,75+i*10),color='b',fontsize=8)

        if ( large > 5.25 ):
            mystr = "stat"+str(i)+":lrgst\n"+str(small[i])
            ax1.annotate(mystr,xy=(4.,75+i*10),fontsize=8)

    fig.savefig(casename+"_len.png")
    plt.close()

# Plot the lengths histogram of input binned data with y as weights and x as
# abscisses. Save this histo in the casename_len.png file.
def plotCurve(y,dataname):

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    ax1.set_title(dataname)

    ax1.set_ylabel(dataname)
    ax1.set_xlabel("Test cases")

    for i in range(len(y)):
        nbtests = len(y[i])

        ax1.plot(y[i])

        # plot mean
        mean = np.mean(y[i])
        max  = np.max(y[i])
        min  = np.min(y[i])

        ax1.axhline(y=mean, linewidth=2,color='g')
        mystr = "stat"+str(i)+":\n"+str(mean)
        if mean > (max-min)/2:
            ax1.annotate(mystr,xy=(nbtests/4+i*(nbtests/4), mean-10),fontsize=12)
        else:
            ax1.annotate(mystr,xy=(nbtests/4+i*(nbtests/4), mean+5),fontsize=12)

    fig.savefig(dataname+".png")
    plt.close()

###############################################################################
#
# main: plot quality/length histograms for all the tests lists in
# "stat_remesh.txt" and plot the histogram of the mean qualities/lengths of all
# this test cases
def main (argv):

    nargs    = len(sys.argv)
    args     = sys.argv

    if ( nargs < 2 ) :
        print "Usage: ",args[0]," stat_file1 [stat_file2...]"

    filelist        = []
    timelist        = []
    nbeltslist      = []
    bestquallist    = []
    meanquallist    = []
    wrstquallist    = []
    quallist        = []
    nbedgslist      = []
    largestlenlist  = []
    meanlenlist     = []
    smallestlenlist = []
    lenlist         = []
    keepedlist      = []
    xqual           = []
    xlen            = []

    for nfile in range(0,nargs-1):
        file = args[nfile+1]
        f = open(file,"r")
        lines = f.readlines()

        tmpfilelist = []
        tmptimelist = []
        tmpnbeltslist = []
        tmpbestquallist = []
        tmpmeanquallist = []
        tmpwrstquallist = []
        tmpquallist = []
        tmpnbedgslist = []
        tmplargestlenlist = []
        tmpmeanlenlist = []
        tmpsmallestlenlist = []
        tmplenlist = []
        tmpkeepedlist = []

        #filelist.append([])
        #timelist.append([])
        #nbeltslist.append([])
        #bestquallist.append([])
        #meanquallist.append([])
        #wrstquallist.append([])
        #quallist.append([])
        #nbedgslist.append([])
        #largestlenlist.append([])
        #meanlenlist.append([])
        #smallestlenlist.append([])
        #lenlist.append([])
        #keepedlist.append([])

        for curline in lines:
            tmpfilelist.append        ( curline.strip().split("\t")[0].strip() )
            tmptimelist.append        ( curline.strip().split("\t")[1].strip() )
            tmpnbeltslist.append      ( curline.strip().split("\t")[2].strip() )
            tmpbestquallist.append    ( curline.strip().split("\t")[3].strip() )
            tmpmeanquallist.append    ( curline.strip().split("\t")[4].strip() )
            tmpwrstquallist.append    ( curline.strip().split("\t")[5].strip() )
            tmpquallist.append        ( [s.strip() for s in curline.strip().split("\t")[6:26]] )
            tmpnbedgslist.append      ( curline.strip().split("\t")[26].strip() )
            tmplargestlenlist.append  ( curline.strip().split("\t")[27].strip() )
            tmpmeanlenlist.append     ( curline.strip().split("\t")[28].strip() )
            tmpsmallestlenlist.append ( curline.strip().split("\t")[29].strip() )
            tmplenlist.append         ( [s.strip() for s in  curline.strip().split("\t")[30:46]] )
            tmpkeepedlist.append      ( curline.strip().split("\t")[46].strip() )

            #filelist[nfile].append(        curline.strip().split("\t")[0])
            #timelist[nfile].append(        curline.strip().split("\t")[1])
            #nbeltslist[nfile].append(      curline.strip().split("\t")[2])
            #bestquallist[nfile].append(    curline.strip().split("\t")[3])
            #meanquallist[nfile].append(    curline.strip().split("\t")[4])
            #wrstquallist[nfile].append(    curline.strip().split("\t")[5])
            #quallist[nfile].append(        curline.strip().split("\t")[6:26])
            #nbedgslist[nfile].append(      curline.strip().split("\t")[26])
            #largestlenlist[nfile].append(  curline.strip().split("\t")[27])
            #meanlenlist[nfile].append(     curline.strip().split("\t")[28])
            #smallestlenlist[nfile].append( curline.strip().split("\t")[29])
            #lenlist[nfile].append(         curline.strip().split("\t")[30:46])
            #keepedlist[nfile].append(      curline.strip().split("\t")[46])

            #timelist       [nfile]  = map( float, timelist[nfile][1:]        )
            #nbeltslist     [nfile]  = map( float, nbeltslist[nfile][1:]      )
            #bestquallist   [nfile]  = map( float, bestquallist[nfile][1:]    )
            #meanquallist   [nfile]  = map( float, meanquallist[nfile][1:]    )
            #wrstquallist   [nfile]  = map( float, wrstquallist[nfile][1:]    )
            #nbedgslist     [nfile]  = map( float, nbedgslist[nfile][1:]      )
            #largestlenlist [nfile]  = map( float, largestlenlist[nfile][1:]  )
            #smallestlenlist[nfile]  = map( float, smallestlenlist[nfile][1:] )
            #meanlenlist    [nfile]  = map( float, meanlenlist[nfile][1:]     )
            #keepedlist     [nfile]  = map( float, keepedlist[nfile][1:]      )
            #
            #quallist[nfile][0] = map(float, quallist[nfile][0])
            #xqual.append(quallist[nfile][0])
            #
            #lenlist[nfile][0] = map(float, lenlist[nfile][0])
            #xlen.append(lenlist[nfile][0])

        tmptimelist         = map( float, tmptimelist[1:]        )
        tmpnbeltslist       = map( float, tmpnbeltslist[1:]      )
        tmpbestquallist     = map( float, tmpbestquallist[1:]    )
        tmpmeanquallist     = map( float, tmpmeanquallist[1:]    )
        tmpwrstquallist     = map( float, tmpwrstquallist[1:]    )
        tmpnbedgslist       = map( float, tmpnbedgslist[1:]      )
        tmplargestlenlist   = map( float, tmplargestlenlist[1:]  )
        tmpsmallestlenlist  = map( float, tmpsmallestlenlist[1:] )
        tmpmeanlenlist      = map( float, tmpmeanlenlist[1:]     )
        tmpkeepedlist       = map( float, tmpkeepedlist[1:]      )

        tmpquallist[0] = map(float, tmpquallist[0])
        tmpxqual = tmpquallist[0]

        tmplenlist[0] = map(float, tmplenlist[0])
        tmpxlen = tmplenlist[0]

        filelist.append(        tmpfilelist )
        timelist.append(        tmptimelist )
        nbeltslist.append(      tmpnbeltslist )
        bestquallist.append(    tmpbestquallist )
        meanquallist.append(    tmpmeanquallist )
        wrstquallist.append(    tmpwrstquallist )
        quallist.append(        tmpquallist )
        nbedgslist.append(      tmpnbedgslist )
        largestlenlist.append(  tmplargestlenlist )
        meanlenlist.append(     tmpmeanlenlist )
        smallestlenlist.append( tmpsmallestlenlist )
        lenlist.append(         tmplenlist )
        keepedlist.append(      tmpkeepedlist )

        xqual.append(tmpxqual)
        xlen.append(tmpxlen)

    # plot the histos for each test case
    for i in range ( len(filelist[0])-1 ):
        repname     = str(filelist[0][i+1].split("/")[-2])
        filename    = str(filelist[0][i+1].split("/")[-1])
        filelist[0][i+1] = repname + "-" + filename
        print filelist[0][i+1], " post-treatment"

        y    = []
        wrst = []
        mean = []
        best = []
        for k in range(nargs-1):
            quallist[k][i+1]=map(float,quallist[k][i+1])
            y.append(quallist[k][i+1])
            wrst.append(wrstquallist[k][i])
            mean.append(meanquallist[k][i])
            best.append(bestquallist[k][i])
        #plotQualHisto(xqual,y,wrst,mean,best,filelist[0][i+1])

        y     = []
        small = []
        mean  = []
        large = []
        for k in range(nargs-1):
            lenlist[k][i+1]=map(float,lenlist[k][i+1])
            y.append(lenlist[k][i+1])
            small.append( smallestlenlist[k][i])
            mean .append( meanlenlist[k][i])
            large.append( largestlenlist[k][i])
        #plotLenHisto(xlen,y,small, mean, large,filelist[0][i+1])

    meanqual     = []
    meanmeanqual = []
    meanbestqual = []
    meanwrstqual = []
    for k in range(nargs-1):
        # plot the histos of the mean qualities/length
        meanqual.append ( np.mean(quallist[k][1:], axis=0))
        meanmeanqual.append ( np.mean(meanquallist[k]) )
        meanbestqual.append ( np.mean(bestquallist[k]) )
        meanwrstqual.append ( np.mean(wrstquallist[k]) )

    plotQualHisto(xqual,meanqual,meanwrstqual,meanmeanqual,meanbestqual,"mean")

    meanlen         = []
    meanmeanlen     = []
    meanlargestlen  = []
    meansmallestlen = []

    for k in range(nargs-1):
        meanlen        .append ( np.mean(lenlist[k][1:], axis=0) )
        meanmeanlen    .append ( np.mean(meanlenlist[k]) )
        meanlargestlen .append ( np.mean(largestlenlist[k]) )
        meansmallestlen.append ( np.mean(smallestlenlist[k]) )
    plotLenHisto(xlen,meanlen,meansmallestlen,meanmeanlen,meanlargestlen,"mean")

    # Plot curves for the other data
    plotCurve(timelist         ,"Time")
    plotCurve(nbeltslist       ,"Number-of-Elements")
    plotCurve(bestquallist     ,"Best-Qualities")
    plotCurve(meanquallist     ,"Mean-Qualities")
    plotCurve(wrstquallist     ,"Wrst-Qualities")
    plotCurve(nbedgslist       ,"Number-of-Edges")
    plotCurve(largestlenlist   ,"Largest-Edges")
    plotCurve(meanlenlist      ,"Mean-Edges")
    plotCurve(smallestlenlist  ,"Smallest-Edges")
    plotCurve(keepedlist       ,"Keeped-Elements")

if __name__ == "__main__":
   main(sys.argv[1:])
