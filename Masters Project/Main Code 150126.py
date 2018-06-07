#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Michelle
#
# Created:     05/08/2014
# Copyright:   (c) Michelle 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import Global_variables as Gv
from os.path import exists
import numpy as np
from scipy import interpolate
import Unit_Tester
import GUI_new as GUI
import winsound             # to make a beep when the code is done

import module1_SetFourierSpace as SFS
import module2_TimeDependentFunctions as TDFunctions
import module3_Plotting as plot
import module4_Powerspectrum as PS
import module5_TimeEvolution as TE
import module6_newinterpolation as Interpolate
import module7_binningmethod as Binning
import module8_savingtocsv as Saving
import module9_initialspectrum as IS
import csvShuffle as Shuffle

name = plot.folderlocator
filename = 'Info.txt'

def compareTuple(Tone,Ttwo):
    if (Tone[0]==-Ttwo[0])and(Tone[1]==-Ttwo[1])and(Tone[2]==-Ttwo[2]):
        return False
    elif (Tone[0]==Ttwo[0])and(Tone[1]==Ttwo[1])and(Tone[2]==Ttwo[2]):
        return False
    else:
        return True

def Overflow(temp):
    """Checks whether any of the arrays sent in have become nan"""
    # Check for nans
    nans = np.isnan(temp)
    index = np.where(nans==True)
    if len(index[0]) > 0:
        return True
    else:
        return False

def strTobool(thestring):
    return thestring[0].upper()=='T'



def variance(powerspectrum,Ltemp):
    """
    This is where I take my calculated power spectrum and calculate the sigma value
    sigma^2 = P/L^3
    """
    return np.multiply(powerspectrum,pow(sizeofbox,-3)*0.5)

def CurlyPfromP(powerspectrum,radii):
    """
    CurlyP = k^3/2pi^2 * P
    """
    return np.multiply(powerspectrum,pow(radii,3))*pow(np.pi,-2)*0.5



def CallingInterpolation(radiitemp,ktemp,Ntemp,Phitemp,Ltemp):
    """
    This function is just here to call the interplation procedure for the grid

    @type
    @param

    @rtype:             np.array
    @return:            the power spectrum for each k on the templist
    """
    print('Interpolation: started')
##    number = [2**8,int(2**8.5),2**9]
    powerspectrum = []
    absolute_phi = np.abs(Phitemp)
    for l in radiitemp:
        i = int(2**8)
        Allpoints = Interpolate.Interpolation_Procedure(l,absolute_phi,1,ktemp,i)
        powerspectrum.append(PS.PowerSpectrum(Allpoints,Ltemp))
    print('Interpolation: ended')
    return powerspectrum

def testingInterpolation(Phirandom,radii_real,k_real,Ntemp,Sigma,CurlyP,runint):
    # Interpolation
    print('Testing Interpolation: started')

    radii_interpolate = radii_real[np.where(radii_real<((Ntemp/2-1)))]
    plotstoplot = [[],[],[],[],[],[],[],[],[]]
    ks = []

    for l in radii_interpolate[1::]:
        average = [[],[]]
        average2 = []
        powerspectrum = []

        # want to divide by the expected
        Sigma2_expected = Sigma[np.where(l==radii_real)][0]
        CurlyP_expected = CurlyP[np.where(l==radii_real)]

        for power in [1.,2.,3.,4.,5.,6.,7.,8.,9.]:
            numberofpoints = pow(2,power)
            Allpoints = Interpolate.Interpolation_Procedure(l,abs(Phirandom),1,k_real,int(numberofpoints))

            average[0].append(numberofpoints)
            average[1].append(abs(PS.average(Allpoints)))
            average2.append(pow(abs(PS.average(Allpoints)),2))
            # change Phirandom to abs(Phirandom) if you want the correct PS
#            print("Not the correct PS, it's setup for correct average^2-line 112")
            powerspectrum.append(PS.PowerSpectrum(Allpoints,sizeofbox))

        CurlyP_calc = CurlyPfromP(powerspectrum,l)
        Sigma2 = variance(powerspectrum,sizeofbox)

        ratio_curlyP = np.multiply(CurlyP_calc,1/CurlyP_expected)
        ratio_Sigma2 = np.multiply(Sigma2,1/Sigma2_expected)

        error_curlyP = np.multiply(np.abs(CurlyP_calc-CurlyP_expected),1/CurlyP_expected)*100
        error_Sigma2 = np.multiply(np.abs(Sigma2-Sigma2_expected),1/Sigma2_expected)*100

        plotstoplot[0].append(average[1])
        plotstoplot[1].append(powerspectrum)
        plotstoplot[2].append(average2)
        plotstoplot[3].append(CurlyP_calc)
        plotstoplot[4].append(Sigma2)
        plotstoplot[5].append(ratio_curlyP)
        plotstoplot[6].append(ratio_Sigma2)
        plotstoplot[7].append(error_curlyP)
        plotstoplot[8].append(error_Sigma2)
        ks.append('|k|='+str(round(l,2)))

    print('Testing Interpolation: ended')
    # Now to plot
    list_titles = ['average vs number of points','powerspectrum vs number of points','average^2 vs number of points','Curly P','Sigma^2','Curly P ratio','Sigma^2 ratio']
    list_yaxis = ['average','powerspectrum','average^2','Curly P','Sigma^2','Curly P ratio','Sigma^2 ratio']

    plot.Graphs_PStestingInter(list_titles,list_yaxis,plotstoplot,average[0],ks,runint)

    u = np.where((radii_interpolate<(N/3)))
    for i in range(len(radii_interpolate[u])//10):
        plot.Plot2D_2on1('Percentage error in $\mathcal{P}(k)$','number of points','error %',ks[i*10:11+(i*10)],average[0],plotstoplot[7][i*10:11+(i*10)],'percent error CurlyP_all_'+str(i))
        plot.Plot2D_2on1('Percentage error in Sigma^2','number of points','error %',ks[i*10:11+(i*10)],average[0],plotstoplot[8][i*10:11+(i*10)],'percent error Sigma^2_all_'+str(i))

    plot.Plot2D_2on1('Percentage error in $\mathcal{P}(k)$','number of points','error %','',average[0],plotstoplot[7],'percent error CurlyP_all')
    plot.Plot2D_2on1('Percentage error in $\mathcal{P}(k)$','number of points','error %',ks[0:6],average[0],plotstoplot[7][0:6],'percent error CurlyP_first6')
    plot.Plot2D_2on1('Percentage error in $\sigma^2$','number of points','error %','',average[0],plotstoplot[8],'percent error Sigma^2_all')
    plot.Plot2D_2on1('Percentage error in $\sigma^2$','number of points','error %',ks[0:6],average[0],plotstoplot[8][0:6],'percent error Sigma^2_first6')

    myfile = open(name+filename,"a")
    myfile.write('Testing the Interpolation:\n')

    # getting C and n
    temp2 = [[] for j in range(9)]
    
    for i in range(9):
        for j in range(len(radii_interpolate[5:u[0][-1]:])):
            temp2[i].append(plotstoplot[3][j][i])
        slope_CurlyP,intercept_CurlyP = np.polyfit(np.log(radii_interpolate[5:u[0][-1]:]),np.log(temp2[i][:u[0][-1]:]),1)
        myfile.write("Number of points:"+str(pow(2,i+1))+'\n')
        myfile.write("CurlyP_calc[power,constant] = ["+str(slope_CurlyP)+","+str(np.exp(intercept_CurlyP))+"]\n")

##    for l in range(len(radii_interpolate[1::])):
##        myfile.write('Radii: '+str(radii_interpolate[l+1])+"\n")
##        myfile.write('Number of points: '+str(average[0])+"\n")
##        myfile.write('Average: '+str(plotstoplot[0][int(l)])+"\n")
##        myfile.write('Average^2: '+str(plotstoplot[2][int(l)])+"\n")
##        myfile.write('Power Sprectrum: '+str(plotstoplot[1][int(l)])+"\n")
##        temp = []
##        for i in range(9):
##            if plotstoplot[2][int(l)][i] < plotstoplot[1][int(l)][i]:
##                temp.append(True)
##            else:
##                temp.append(False)
##        myfile.write('Which is bigger '+str(temp)+"\n")
##        myfile.write('CurlyP: '+str(plotstoplot[3][int(l)])+"\n")
##        myfile.write('Sigma^2: '+str(plotstoplot[4][int(l)])+"\n")
##        myfile.write('CurlyP ratio: '+str(plotstoplot[5][int(l)])+"\n")
##        myfile.write('Sigma^2 ratio: '+str(plotstoplot[6][int(l)])+"\n")

    myfile.close()
    
    temp2 = [[] for j in range(9)]
    labels = [str(i) for i in average[0]]
    for i in range(9):
        for j in range(len(radii_interpolate[1::])):
            temp2[i].append(plotstoplot[1][j][i])
    plot.Plot2D_2on1('Power spectrum vs radius','|k|','Power Spectrum',labels,radii_interpolate[1::],temp2,'PS wrt Radius')  
    plot.Plot2D_2on1('Power spectrum vs radius','|k|','Power Spectrum',labels,radii_interpolate[1::],temp2,'PS wrt Radius_loglog',graph_type="loglog")  

    temp2 = [[] for j in range(9)]
    labels = [str(i) for i in average[0]]
    for i in range(9):
        for j in range(len(radii_interpolate[1::])):
            temp2[i].append(plotstoplot[3][j][i])
    plot.Plot2D_2on1('$\mathcal{P}(k)$ vs radius','|k|','$\mathcal{P}(k)$',labels,radii_interpolate[1::],temp2,'CurlyP wrt Radius')
    plot.Plot2D_2on1('$\mathcal{P}(k)$ vs radius','|k|','$\mathcal{P}(k)$',labels,radii_interpolate[1::],temp2,'CurlyP wrt Radius_loglog',graph_type="loglog")

    temp2 = [[] for j in range(9)]
    labels = [str(i) for i in average[0]]
    for i in range(9):
        for j in range(len(radii_interpolate[1::])):
            temp2[i].append(plotstoplot[4][j][i])
    plot.Plot2D_2on1('$\sigma^2$ vs radius','|k|','$\sigma^2$',labels,radii_interpolate[1::],temp2,'Sigma2 wrt Radius')
    plot.Plot2D_2on1('$\sigma^2$ vs radius','|k|','$\sigma^2$',labels,radii_interpolate[1::],temp2,'Sigma2 wrt Radius_loglog',graph_type="loglog")



def CallingBinning(templist,radii,ktemp,Ntemp,binsize,bincentre,method):
    if method == 1:
        temp = Binning.binning_procedure(templist,radii,ktemp,Ntemp,binsize,bincentre)
    else:
        temp = Binning.binning_procedure_weighted(templist,radii,ktemp,Ntemp,binsize,bincentre)
    return temp
##    temp = Binning.binning_procedure_log(templist,radii,ktemp,Ntemp,4166,binsize,bincentre)
##    return temp

def testingBinning(templist,radii,ktemp,Ntemp,Ltemp,bincentre,PSmethod,runint):
    CurlyP_expected = IS.Spectrum(bincentre,C,n,PSmethod)
    Sigma_expected = IS.SigmaNSquared(bincentre,CurlyP_expected)
    method = 2
    if method == 2:
        bin_sizes = np.arange(0.1,2,0.1)
    else:
        bin_sizes = np.arange(0,2,0.1)
##    bin_sizes = [0,grid_factor/5,grid_factor/4,grid_factor/3,grid_factor/2,grid_factor,grid_factor*6/5,grid_factor*5/4,grid_factor*4/3,grid_factor*3/2,2*grid_factor]
    bin_labels = [str(round(i,2)) for i in bin_sizes]
    average = np.zeros((len(bin_sizes),len(bincentre)),complex)
    collect = np.zeros((len(bin_sizes),len(bincentre)))
    P = np.zeros((len(bin_sizes),len(bincentre)))
    CurlyP = np.zeros((len(bin_sizes),len(bincentre)))
    Sigma = np.zeros((len(bin_sizes),len(bincentre)))
    error_CurlyP = np.zeros((len(bin_sizes),len(bincentre)))
    error_Sigma = np.zeros((len(bin_sizes),len(bincentre)))
    
    for i in range(len(bin_sizes)):
        average[i] = CallingBinning(templist,radii,ktemp,Ntemp,bin_sizes[i],bincentre,method)
        collect[i] = CallingBinning(pow(abs(templist),2),radii,ktemp,Ntemp,bin_sizes[i],bincentre,method)
        P[i] = np.multiply(collect[i],pow(Ltemp,3))
        CurlyP[i] = CurlyPfromP(P[i],bincentre)
        Sigma[i] = variance(P[i],Ltemp)
        error_CurlyP[i] = np.multiply(np.abs(CurlyP[i]-CurlyP_expected),1/CurlyP_expected)*100
        error_Sigma[i] = np.multiply(np.abs(Sigma[i]-Sigma_expected),1/Sigma_expected)*100
    averagesquared = pow(average,2)

    plot.Plot2D_2on1('The error for different bin sizes','radius [|k|]','% error',bin_labels,bincentre,error_CurlyP,'Error bin test_'+str(runint))
    middle = len(bin_labels)/2
    plot.Plot2D_2on1('The error for different bin sizes','radius [|k|]','% error',bin_labels[middle-5:middle+6],bincentre,error_CurlyP[middle-5:middle+6],'Error bin test_around middle_1_'+str(runint))
    plot.Plot2D_2on1('The error for different bin sizes','radius [|k|]','% error',bin_labels[middle-3:middle+4],bincentre,error_CurlyP[middle-3:middle+4],'Error bin test_around middle_2_'+str(runint),mark=['','','','.','','',''])    
    plot.Plot2D_2on1('The error for different bin sizes','radius [|k|]','% error','',bincentre,error_CurlyP,'Error bin test_no legend_'+str(runint))

    plot.Plot2D_2on1('average','radius [|k|]','average','',bincentre,abs(average),'Average_'+str(runint))
    plot.Plot2D_2on1('average squared','radius [|k|]','average squared','',bincentre,abs(averagesquared),'Averagesquared_'+str(runint))
    plot.Plot2D_2on1('average squared','radius [|k|]','average squared','',bincentre,abs(averagesquared),'Averagesquared_loglog_'+str(runint),graph_type="loglog")
    
    plot.Plot2D_2on1('$\mathcal{P}$','radius [|k|]','$\mathcal{P}(k)$','',bincentre,CurlyP,'CurlyP_'+str(runint))
    plot.Plot2D_2on1('$\mathcal{P}$','radius [|k|]','$\mathcal{P}(k)$','',bincentre,CurlyP,'CurlyP_loglog_'+str(runint),graph_type="loglog")
    plot.Plot2D_2on1('$\mathcal{P}$','radius [|k|]','$\mathcal{P}(k)$',bin_labels[middle-5:middle+6],bincentre,CurlyP[middle-5:middle+6],'CurlyP_loglog_middle_1_'+str(runint),graph_type="loglog")
    plot.Plot2D_2on1('$\mathcal{P}$','radius [|k|]','$\mathcal{P}(k)$',bin_labels[middle-3:middle+4],bincentre,CurlyP[middle-3:middle+4],'CurlyP_loglog_middle_2_'+str(runint),graph_type="loglog",mark=['','','','.','','',''])    
    
    plot.Plot2D_2on1('collect','radius [|k|]','collect','',bincentre,collect,'Collect_'+str(runint))
    plot.Plot2D_2on1('collect','radius [|k|]','collect','',bincentre,collect,'Collect_loglog_'+str(runint),graph_type="loglog")
    plot.Plot2D_2on1('collect','radius [|k|]','collect',bin_labels[middle-5:middle+6],bincentre,collect[middle-5:middle+6],'Collect_loglog_middle_1_'+str(runint),graph_type="loglog")
    plot.Plot2D_2on1('collect','radius [|k|]','collect',bin_labels[middle-3:middle+4],bincentre,collect[middle-3:middle+4],'Collect_loglog_middle_2_'+str(runint),graph_type="loglog",mark=['','','','.','','',''])
    
    for i in range(int(len(bin_sizes)/5+1)):
        plot.Plot2D_2on1('average','radius [|k|]','average',bin_labels[5*i:5+5*i],bincentre,abs(average[5*i:5+5*i]),'Average_'+str(i)+'_'+str(runint))
        plot.Plot2D_2on1('average squared','radius [|k|]','average squared',bin_labels[5*i:5+5*i],bincentre,abs(averagesquared[5*i:5+5*i]),'Averagesquared_'+str(i)+'_'+str(runint))
        plot.Plot2D_2on1('$\mathcal{P}$','radius [|k|]','$\mathcal{P}(k)$',bin_labels[5*i:5+5*i],bincentre,CurlyP[5*i:5+5*i],'CurlyP_'+str(i)+'_'+str(runint))
        plot.Plot2D_2on1('collect','radius [|k|]','collect',bin_labels[5*i:5+5*i],bincentre,collect[5*i:5+5*i],'Collect_'+str(i)+'_'+str(runint))
        plot.Plot2D_2on1('$\mathcal{P}$','radius [|k|]','$\mathcal{P}(k)$',bin_labels[5*i:5+5*i],bincentre,CurlyP[5*i:5+5*i],'CurlyP_'+str(i)+'_loglog_'+str(runint),graph_type="loglog")
        plot.Plot2D_2on1('collect','radius [|k|]','collect',bin_labels[5*i:5+5*i],bincentre,collect[5*i:5+5*i],'Collect_'+str(i)+'_loglog_'+str(runint),graph_type="loglog")

##    for i in range()
    # splitting it up
    plotstoplot = []
    bincentre_labels = ['|k|='+str(round(i,2)) for i in bincentre]
    for i in range(len(bincentre)):
        temp2 = error_CurlyP[:,i]
        plotstoplot.append(temp2)
##    print(len(plotstoplot[0]),len(bin_sizes))
    plot.Plot2D_2on1('error for the different bin centres','bin sizes','% error','',bin_sizes,plotstoplot,'Error bin test 2_'+str(runint))
    plot.Plot2D_2on1('error for the different bin centres','bin sizes','% error',bincentre_labels[:6],bin_sizes,plotstoplot[:6],'Error bin test 2_first 6_'+str(runint))

    # splitting it up
    plotstoplot = []
    for i in range(len(bincentre)):
        temp2 = averagesquared[:,i]
        plotstoplot.append(temp2)
##    print(len(plotstoplot[0]),len(bin_sizes))
    plot.Plot2D_2on1('average squared','bin sizes','average^2','',bin_sizes,plotstoplot,'average square_'+str(runint))
    plot.Plot2D_2on1('average squared','bin sizes','average^2',bincentre_labels[:6],bin_sizes,plotstoplot[:6],'average square_first 6_'+str(runint))

    # splitting it up
    plotstoplot = []
    for i in range(len(bincentre)):
        temp2 = collect[:,i]
        plotstoplot.append(temp2)
##    print(len(plotstoplot[0]),len(bin_sizes))
    plot.Plot2D_2on1('collect','bin sizes','collect','',bin_sizes,plotstoplot,'Collect_binsize_'+str(runint))
    plot.Plot2D_2on1('collect','bin sizes','collect',bincentre_labels[:6],bin_sizes,plotstoplot[:6],'Collect_binsize_first 6_'+str(runint))

    myfile = open(name+filename,"a")
    myfile.write('Testing the Binning:\n')
    u = np.where((bincentre<(N/3))&(bincentre>5))
    for i in range(len(bin_sizes)):
        slope_CurlyP,intercept_CurlyP = np.polyfit(np.log(bincentre[u]),np.log(CurlyP[i][u]),1)
        myfile.write("Bin size:"+str(round(bin_sizes[i],4))+'\n')
        myfile.write("CurlyP_calc[power,constant] = ["+str(round(slope_CurlyP,4))+","+str(np.exp(intercept_CurlyP))+"]\n")
    myfile.close()

#===============================================================================
# Choose constants
labels = ['z','N','L (Mpc)','Rayleigh',['method to get PS','bin','inter','non'],'test: bin','test: inter',['timesteps:','all','non','other'],'other:','growing mode','Run code:',['initial PS:','Ck^n','Ck^(n-1)','Ck^(1-n)','not random: 1/r'],'non-linear terms','file location',['filter:','step','exp','expS'],'filter variables']
default = ['10','54','4166',1,3,0,0,3,3,1,1,2,1,'Datafiles\\',2,'36,36'] #10^(-6) with random angles N54
listgui = ['tbx','tbx','tbx','cbx','rbn','cbx','cbx','rbn','tbx','cbx','tbx','rbn','cbx','tbx','rbn','tbx']

inputvalues = GUI.getInputsList(labels,default,listgui)
# whether the power spectrum should be calculated using interpolation or binning
methods = [inputvalues[4]-1,bool(inputvalues[5]),bool(inputvalues[6])]
nonlinear = bool(inputvalues[12])
datalocation = inputvalues[13]
if inputvalues[14] == 1:
    if inputvalues[15] == '2/3':
        Gv.filter_variables = [inputvalues[14],[2./3.]]
    else:
        Gv.filter_variables = [inputvalues[14],[float(inputvalues[15])]]
elif (inputvalues[14] == 2) or (inputvalues[14] == 3):
    filterconstants = [float(i) for i in inputvalues[15].split(',')]
    Gv.filter_variables = [inputvalues[14],filterconstants]
K = 0.0
##w = 1.0/3.0                         # setting it up with radiation first
w = 0.0                             # setting it up with pressureless matter first
G = SFS.G
c = SFS.c
global z
z = float(inputvalues[0])           # Red-shift

##==============================================================================
tau_start = TDFunctions.start_tau(z,w)
a_tau = TDFunctions.a_tau(tau_start,w)
H_tau = TDFunctions.H_tau(tau_start,w)
density_tau = TDFunctions.density_tau(tau_start,w,K)
H0 = TDFunctions.H_tau(1.0,w)

#===============================================================================
# Number of sample points
N = int(inputvalues[1])

sizeofbox = np.pi*2
Lbox = int(inputvalues[2])     # Mpc
h = (sizeofbox)/(N*1.0)

# Power spectrum constants
##n = 0.0                             # Choosing the power of the power law
##C = 2*(10**(-9))                    # Choosing the amplitude of the power law
##pivot_k = 1                         # Choosing the pivot wavenumber
n = 0.968                             # Choosing the power of the power law
C = 2.42*(10**(-9))                      # Choosing the amplitude of the power law
pivot_k = 0.002*Lbox/(np.pi*2)        # Choosing the pivot wavenumber
PS_type = inputvalues[11]

# dt must be set by something smaller than h, and smaller than tau_start. tau_start < h, therefore if dt=fraction of tau_start then it will be smaller than h
tau_start_z10 = TDFunctions.start_tau(10.0,w)
factor = 10.0
dt = tau_start/factor

if inputvalues[7] == 1:
    number = (int((1.0-tau_start)/dt+1))#*2
elif inputvalues[7] == 2:
    number = -1
else:
    number = int(inputvalues[8])

#===============================================================================
# Creating and saving the textfile
myfile = open(name+filename,"a")

myfile.write("Number of points = "+str(N)+"\n")
myfile.write("L box = "+str(Lbox)+"\n")
myfile.write("K,w,z,G,c = "+str(K)+","+str(w)+","+str(z)+","+str(G)+","+str(c)+"\n")
myfile.write("PowerSpectrum [C,n] = ["+str(C)+","+str(n)+"]\n")
myfile.write("Square shape = "+str(SFS.squareOn)+"\n")
myfile.write("Non-linear terms = "+str(nonlinear)+"\n")
myfile.write("dt = "+str(dt)+"\n")
myfile.write("tau_start = "+str(tau_start)+"\n")
myfile.write("initial data from "+datalocation+"\n")
filt = ['filter:','step','exp','expS']
myfile.write("filter = "+filt[inputvalues[14]]+", constants = "+inputvalues[15]+"\n")

myfile.close()

print("L box = "+str(Lbox)+" Mpc")
print("z = "+str(z))
print("Number of points = "+str(N))
print("filter = "+filt[inputvalues[14]]+", constants = "+inputvalues[15]) 
print("Non-linear terms = "+str(nonlinear))
print("time-step factor = "+str(factor))
#===============================================================================
# All the k's I need
k_positive = np.arange(0,N/2+1,1)
k_int = np.fft.fftfreq(N, 1./N)
k_int[N/2] = abs(k_int[N/2])
radii_int = IS.Radius(N,1.0)

# k for differentiating
k = np.copy(k_int)
ky,kz,kx = np.meshgrid(k,k,k)

x = np.arange(0.0,sizeofbox,h)
#===============================================================================
# Magnitude of k
radii_real_h = np.multiply(radii_int,2*np.pi/(Lbox*0.7))
wavelength = np.divide(2*np.pi,radii_real_h)

CurlyP = IS.Spectrum(np.copy(radii_int),C,n,pivot_k,inputvalues[11])
plot.Plot2D('$\mathcal{P}_{\Phi}(k)$','$k$','$\mathcal{P}_{\Phi}(k)$',radii_int,CurlyP,0,'CurlyP')
plot.Plot2D('$\mathcal{P}_{\Phi}(k)$','$k$ [h.Mpc$^{-1}$]','$\mathcal{P}_{\Phi}(k)$',radii_real_h,CurlyP,0,'CurlyP_realwithh')
plot.Plot2D('$\mathcal{P}_{\Phi}(\lambda)$','$\lambda$ [Mpc.h$^{-1}$]','$\mathcal{P}_{\Phi}(\lambda)$',wavelength,CurlyP,0,'CurlyP_wavelengthwithh')
Sigma = IS.SigmaNSquared(np.copy(radii_int),np.copy(CurlyP))
plot.Plot2D('$\sigma^{2}_n(k)$','$k$','$\sigma^{2}_n(k)$',radii_int,Sigma,0,'Sigma')
plot.Plot2D('$\sigma^{2}_n(k)$','$k$ [h.Mpc$^{-1}$]','$\sigma^{2}_n(k)$',radii_real_h,Sigma,0,'Sigma_realwithh')
plot.Plot2D('$\sigma^{2}_n(\lambda)$','$\lambda$ [Mpc.h$^{-1}$]','$\sigma^{2}_n(\lambda)$',wavelength,Sigma,0,'Sigma_wavelengthwithh')

#===============================================================================
# Real
Real_k = k_int * 2*np.pi/Lbox
Real_lambda = 1/Real_k
Real_lambda[np.isnan(Real_lambda)] = 0.0
#===============================================================================

def main(runint):
    print("tau_start =",tau_start)
    z = float(inputvalues[0])           # Red-shift

    myfile = open(name+filename,"a")
    myfile.write("Run: "+str(runint)+"\n")
    myfile.close()

    # if Phi file doesn't exist then the rest can't
    extension = str(z)+"N"+str(N)+"L"+str(Lbox)+"n"+str(n)+"PS"+str(PS_type)
    if not(exists(datalocation+"Phiatz"+extension+".csv")):
        # create the files
        if inputvalues[11] == 4:
            Phiofk3D = SFS.SFS_Phi(N,radii_int,k_int,Sigma,bool(inputvalues[3]),Lbox,True)
        else:
            Phiofk3D = SFS.SFS_Phi(N,radii_int,k_int,Sigma,bool(inputvalues[3]),Lbox)
##        Phiofk3D = np.divide(Phiofk3D,pow(N,3))
        Saving.save3Darray(Phiofk3D,datalocation+"Phiatz"+extension)

        kmag_int = pow(kx,2) + pow(ky,2) + pow(kz,2)
        Deltaofk3D = SFS.SFS_Delta_growing(Phiofk3D,tau_start,kmag_int,Lbox)
        Saving.save3Darray(Deltaofk3D,datalocation+"deltaatz"+extension)
        kmag_int = None

        Velocityk3D_x = SFS.SFS_Velocity_growing(Phiofk3D,tau_start,kx,Lbox)
        Saving.save3Darray(Velocityk3D_x,datalocation+"Velocityxatz"+extension)
        Velocityk3D_y = SFS.SFS_Velocity_growing(Phiofk3D,tau_start,ky,Lbox)
        Saving.save3Darray(Velocityk3D_y,datalocation+"Velocityyatz"+extension)
        Velocityk3D_z = SFS.SFS_Velocity_growing(Phiofk3D,tau_start,kz,Lbox)
        Saving.save3Darray(Velocityk3D_z,datalocation+"Velocityzatz"+extension)
    else: # read them
        Phiofk3D = Shuffle.read3Darray(datalocation+"Phiatz"+extension)
        Deltaofk3D = Shuffle.read3Darray(datalocation+"deltaatz"+extension)
        Velocityk3D_x = Shuffle.read3Darray(datalocation+"Velocityxatz"+extension)
        Velocityk3D_y = Shuffle.read3Darray(datalocation+"Velocityyatz"+extension)
        Velocityk3D_z = Shuffle.read3Darray(datalocation+"Velocityzatz"+extension)

    # apply filter

    filterarray = SFS.create_filterarray(kx,ky,kz,Gv.filter_variables[0],Gv.filter_variables[1])
    np.multiply(filterarray,Phiofk3D,Phiofk3D)
    np.multiply(filterarray,Deltaofk3D,Deltaofk3D)
    np.multiply(filterarray,Velocityk3D_x,Velocityk3D_x)
    np.multiply(filterarray,Velocityk3D_y,Velocityk3D_y)
    np.multiply(filterarray,Velocityk3D_z,Velocityk3D_z)
    
#    term = np.where(abs(Deltaofk3D[0][0])<(10**(-8)))
    half_filter = np.where(filterarray[0][0]<0.97)
    term =  min(N//3,k_int[int(half_filter[0][0])-1]) #N/3 #27.0
    filterarray = None # don't need it saved in memory after this point
    half_filter = None


##    plot.Graphs_FourierSpace([Phiofk3D],['Phi_hat_initial'],k_int,k_int,N,z,runint)

    plotstoplot = [Phiofk3D,Deltaofk3D,Velocityk3D_x,Velocityk3D_y,Velocityk3D_z]
    plot.Graphs_FourierSpace(plotstoplot,['Phi_hat','delta_hat','Velocity_x_hat','Velocity_y_hat','Velocity_z_hat'],k_int,k_int,N,z,runint)

    #===============================================================================
    # Interpolation to reconstruct sigma and curlyP
    if (methods[0] == 1):
        maxk = N/2
        index = np.where(radii_int<(maxk-1))
        radii_interpolate_int = radii_int[index]
        PowerSpectrum_Phi = CallingInterpolation(radii_interpolate_int[1::],k_int,N,Phiofk3D,sizeofbox)
        PowerSpectrum_Delta = []
        PowerSpectrum_Delta.append(CallingInterpolation(radii_interpolate_int[1::],k_int,N,Deltaofk3D,sizeofbox))

        CurlyP_calc = CurlyPfromP(np.copy(PowerSpectrum_Phi),radii_interpolate_int[1::])
        percentage_error_CurlyP = np.multiply(np.abs(CurlyP_calc-CurlyP[1:index[0][-1]+1]),pow(CurlyP[1:index[0][-1]+1],-1))*100

        plot.Graphs_PowerSpectrum(radii_interpolate_int[1::],[PowerSpectrum_Phi,PowerSpectrum_Phi,PowerSpectrum_Delta[0],PowerSpectrum_Delta[0],CurlyP_calc,CurlyP_calc],['Phi','Phi','delta','delta','CurlyP','CurlyP'],['$\hat{\Phi}$','$\hat{\Phi}$','$\hat{\delta}$','$\hat{\delta}$','$\mathcal{P}(k)$','$\mathcal{P}(k)$'],['','loglog','sci','loglog','','loglog'],False,'Interpolation',runint)

        plot.Plot2D('calc-expected/expected','$k$','Error %',radii_interpolate_int[1::],percentage_error_CurlyP,0,'Interpolation_'+'Error in CurlyP_'+str(runint))
        plot.Plot2D('$\mathcal{P}_{calc} / \mathcal{P}$','$k$','',radii_interpolate_int[1::],CurlyP_calc/CurlyP[1:(index[0][-1]+1)],0,'Interpolation_'+'ratio of CurlyP_'+str(runint))

        Sigma_calc = variance(np.copy(PowerSpectrum_Phi),sizeofbox)
        difference = Sigma_calc/Sigma[1:(index[0][-1]+1)]
        percentage_error_Sigma2 = np.multiply(np.abs(Sigma_calc-Sigma[1:index[0][-1]+1]),pow(Sigma[1:index[0][-1]+1],-1))*100
        plot.Plot2D('$\sigma^{2}_{calc} / \sigma^{2}$','$k$','',radii_interpolate_int[1::],difference,0,'Interpolation_'+'ratio of sigmas_'+str(runint))
        plot.Plot2D('calc-expected/expected','$k$','Error %',radii_interpolate_int[1::],percentage_error_Sigma2,0,'Interpolation_'+'Error in Sigma^2_'+str(runint))

        u = np.where((radii_interpolate_int<(N/3))&(radii_interpolate_int>5))
        slope_CurlyP_calc,intercept_CurlyP_calc = np.polyfit(np.log(radii_interpolate_int[u[0][0]:u[0][-1]]),np.log(CurlyP_calc[u[0][0]:u[0][-1]]),1)
        slope_CurlyP,intercept_CurlyP = np.polyfit(np.log(radii_int[1::]),np.log(np.copy(CurlyP[1::])),1)
        slope_Delta,intercept_Delta = np.polyfit(np.log(radii_interpolate_int[u[0][0]:u[0][-1]]),np.log(PowerSpectrum_Delta[0][u[0][0]:u[0][-1]]),1)

        myfile = open(name+filename,"a")
        myfile.write("Interpolation:\n")
        myfile.write("Delta[power,constant] = ["+str(slope_Delta)+","+str(np.exp(intercept_Delta))+"]\n")
        myfile.write("CurlyP[power,constant] = ["+str(slope_CurlyP)+","+str(np.exp(intercept_CurlyP))+"]\n")
        myfile.write("CurlyP_calc[power,constant] = ["+str(slope_CurlyP_calc)+","+str(np.exp(intercept_CurlyP_calc))+"]\n")
        myfile.close()

    #===============================================================================
        # Graphs for Julien
        radii_interpolate_physical = radii_interpolate_int*2*np.pi/Lbox
        plot.Graphs_PowerSpectrum(radii_interpolate_physical[1::],[PowerSpectrum_Phi,PowerSpectrum_Phi,PowerSpectrum_Delta[0],PowerSpectrum_Delta[0],CurlyP_calc,CurlyP_calc],['Phi','Phi','delta','delta','CurlyP','CurlyP'],['$\hat{\Phi}$','$\hat{\Phi}$','$\hat{\delta}$','$\hat{\delta}$','$\mathcal{P}(k)$','$\mathcal{P}(k)$'],['','loglog','','loglog','','loglog'],True,'Interpolation',runint)

        plot.Plot2D('calc-expected/expected','$k$ [Mpc$^{-1}$]','Error %',radii_interpolate_physical[1::],percentage_error_CurlyP,0,'REAL_'+'Interpolation_'+'Error in CurlyP_'+str(runint))

        plot.Plot2D('$\sigma^{2}_{calc} / \sigma^{2}$','$k$ [Mpc$^{-1}$]','',radii_interpolate_physical[1::],difference,0,'REAL_'+'Interpolation_'+'ratio of sigmas_'+str(runint))
        plot.Plot2D('$\mathcal{P}_{calc} / \mathcal{P}$','$k$ [Mpc$^{-1}$]','',radii_interpolate_physical[1::],CurlyP_calc/CurlyP[1:(index[0][-1]+1)],0,'REAL_'+'Interpolation_'+'ratio of CurlyP_'+str(runint))
        plot.Plot2D('calc-expected/expected','$k$ [Mpc$^{-1}$]','Error %',radii_interpolate_physical[1::],percentage_error_Sigma2,0,'REAL_'+'Interpolation_'+'Error in Sigma^2_'+str(runint))
        
    #===============================================================================
        # Graphs with h
        radii_interpolate_physical = radii_interpolate_int*2*np.pi/Lbox/0.7
        plot.Graphs_PowerSpectrum_h(radii_interpolate_physical[1::],[PowerSpectrum_Phi,PowerSpectrum_Phi,PowerSpectrum_Delta[0],PowerSpectrum_Delta[0],CurlyP_calc,CurlyP_calc],['Phi','Phi','delta','delta','CurlyP','CurlyP'],['$\hat{\Phi}$','$\hat{\Phi}$','$\hat{\delta}$','$\hat{\delta}$','$\mathcal{P}(k)$','$\mathcal{P}(k)$'],['','loglog','','loglog','','loglog'],'Interpolation',runint)

        plot.Plot2D('calc-expected/expected','$k$ [h.Mpc$^{-1}$]','Error %',radii_interpolate_physical[1::],percentage_error_CurlyP,0,'REALwithh_'+'Interpolation_'+'Error in CurlyP_'+str(runint))

        plot.Plot2D('$\sigma^{2}_{calc} / \sigma^{2}$','$k$ [h.Mpc$^{-1}$]','',radii_interpolate_physical[1::],difference,0,'REALwithh_'+'Interpolation_'+'ratio of sigmas_'+str(runint))
        plot.Plot2D('$\mathcal{P}_{calc} / \mathcal{P}$','$k$ [h.Mpc$^{-1}$]','',radii_interpolate_physical[1::],CurlyP_calc/CurlyP[1:(index[0][-1]+1)],0,'REALwithh_'+'Interpolation_'+'ratio of CurlyP_'+str(runint))
        plot.Plot2D('calc-expected/expected','$k$ [h.Mpc$^{-1}$]','Error %',radii_interpolate_physical[1::],percentage_error_Sigma2,0,'REALwithh_'+'Interpolation_'+'Error in Sigma^2_'+str(runint))
        
    #===============================================================================
        # Graphs in wavelength
        """wavelength = np.divide(2*np.pi,radii_interpolate_physical)
        print('this next line gives an error')
        plot.Graphs_PowerSpectrum_wavelength(wavelength[1::],[PowerSpectrum_Phi,PowerSpectrum_Phi,PowerSpectrum_Delta[0],PowerSpectrum_Delta[0],CurlyP_calc,CurlyP_calc],['Phi','Phi','delta','delta','CurlyP','CurlyP'],['$\hat{\Phi}$','$\hat{\Phi}$','$\hat{\delta}$','$\hat{\delta}$','$\mathcal{P}(k)$','$\mathcal{P}(k)$'],['','loglog','','loglog','','loglog'],'Interpolation',runint)

        print('these lines dont give an error')
        plot.Plot2D('calc-expected/expected','$\lambda$ [Mpc.h$^{-1}$]','Error %',wavelength[1::],percentage_error_CurlyP,0,'REALwithwavelength_'+'Interpolation_'+'Error in CurlyP_'+str(runint))
        plot.Plot2D('$\sigma^{2}_{calc} / \sigma^{2}$','$\lambda$ [Mpc.h$^{-1}$]','',wavelength[1::],difference,0,'REALwithwavelength_'+'Interpolation_'+'ratio of sigmas_'+str(runint))
        plot.Plot2D('$\mathcal{P}_{calc} / \mathcal{P}$','$\lambda$ [Mpc.h$^{-1}$]','',wavelength[1::],CurlyP_calc/CurlyP[1:(index[0][-1]+1)],0,'REALwithwavelength_'+'Interpolation_'+'ratio of CurlyP_'+str(runint))
        plot.Plot2D('calc-expected/expected','$\lambda$ [Mpc.h$^{-1}$]','Error %',wavelength[1::],percentage_error_Sigma2,0,'REALwithwavelength_'+'Interpolation_'+'Error in Sigma^2_'+str(runint))        
        
        # to save on RAM usage
        wavelength = None"""
        radii_interpolate_physical = None
        radii_interpolate_int = None
    #===============================================================================
    # Binning to reconstruct sigma and curlyP
    if (methods[0] == 0):
##        largest = np.log(radii_interpolate_int[-1])//1
##        centres = np.arange(1,largest,1)
        maxk = N/2
        centres = k_positive[1:maxk:]

        index = np.where(radii_int<=(maxk-0.5))
        index2 = np.where(radii_int<=(maxk-1))
        CurlyP_pos_real = CurlyP[1:index2[0][-1]+1]
        Sigma_pos_real = Sigma[1:index2[0][-1]+1]

        radii_interpolate_int = radii_int[1:index[0][-1]+1]
        
        type_bin = 1

        variance_Phi = CallingBinning(pow(abs(Phiofk3D),2),radii_interpolate_int,k_int,N,1,centres,type_bin)
        PowerSpectrum_Phi = np.multiply(variance_Phi,pow(sizeofbox,3))
        variance_Delta = CallingBinning(pow(abs(Deltaofk3D),2),radii_interpolate_int,k_int,N,1,centres,type_bin)
        PowerSpectrum_Delta = []
        PowerSpectrum_Delta.append(np.multiply(variance_Delta,pow(sizeofbox,3)))

        f_Phi = interpolate.interp1d(np.log(centres),np.log(PowerSpectrum_Phi))
        PowerSpectrum_Phi_all = np.exp(f_Phi(np.log(radii_interpolate_int[:index2[0][-1]:])))
        PowerSpectrum_Phi_all[np.isnan(PowerSpectrum_Phi_all)] = 0.0
        f_Delta = interpolate.interp1d(np.log(centres),np.log(PowerSpectrum_Delta[0]))
        PowerSpectrum_Delta_all = np.exp(f_Delta(np.log(radii_interpolate_int[:index2[0][-1]:])))
        PowerSpectrum_Delta_all[np.isnan(PowerSpectrum_Delta_all)] = 0.0

        CurlyP_calc = CurlyPfromP(PowerSpectrum_Phi_all,radii_interpolate_int[:index2[0][-1]:])
        percentage_error_CurlyP = np.multiply(np.abs(CurlyP_calc-CurlyP_pos_real),pow(CurlyP_pos_real,-1))*100

        plot.Graphs_PowerSpectrum(centres,[PowerSpectrum_Phi,PowerSpectrum_Phi,PowerSpectrum_Delta[0],PowerSpectrum_Delta[0]],['Phi','Phi','delta','delta'],['$\hat{\Phi}$','$\hat{\Phi}$','$\hat{\delta}$','$\hat{\delta}$'],['','loglog','','loglog'],False,'Binning',runint)
        plot.Graphs_PowerSpectrum(radii_interpolate_int[:index2[0][-1]:],[CurlyP_calc,CurlyP_calc],['CurlyP','CurlyP'],['$\mathcal{P}(k)$','$\mathcal{P}(k)$'],['','loglog'],False,'Binning',runint)

        plot.Plot2D('calc-expected/expected','$k$','Error [%]',radii_interpolate_int[:index2[0][-1]:],percentage_error_CurlyP,0,'Binning_'+'Error in CurlyP_'+str(runint))
        plot.Plot2D('$\mathcal{P}_{calc} / \mathcal{P}$','$k$','',radii_interpolate_int[:index2[0][-1]:],CurlyP_calc/CurlyP_pos_real,0,'Binning_'+'ratio of CurlyP_'+str(runint))

        Sigma_calc = variance(PowerSpectrum_Phi_all,sizeofbox)
        difference = Sigma_calc/Sigma_pos_real
        percentage_error_Sigma2 = np.multiply(np.abs(Sigma_calc-Sigma_pos_real),pow(Sigma_pos_real,-1))*100
        plot.Plot2D('$\sigma^{2}_{calc} / \sigma$','$k$','',radii_interpolate_int[:index2[0][-1]:],difference,0,'Binning_'+'ratio of sigmas_'+str(runint))
        plot.Plot2D('calc-expected/expected','$k$','Error [%]',radii_interpolate_int[:index2[0][-1]:],percentage_error_Sigma2,0,'Binning_'+'Error in Sigma^2_'+str(runint))

        u = np.where((radii_interpolate_int<(N/3))&(radii_interpolate_int>5))
        slope_CurlyP_calc,intercept_CurlyP_calc = np.polyfit(np.log(radii_interpolate_int[u]),np.log(CurlyP_calc[u]),1)
        slope_CurlyP,intercept_CurlyP = np.polyfit(np.log(radii_interpolate_int[:index2[0][-1]:]),np.log(np.copy(CurlyP_pos_real)),1)
        slope_Delta,intercept_Delta = np.polyfit(np.log(radii_interpolate_int[u]),np.log(PowerSpectrum_Delta_all[u]),1)

        myfile = open(name+filename,"a")
        myfile.write("Binning:\n")
        myfile.write("Delta[power,constant] = ["+str(slope_Delta)+","+str(np.exp(intercept_Delta))+"]\n")
        myfile.write("CurlyP[power,constant] = ["+str(slope_CurlyP)+","+str(np.exp(intercept_CurlyP))+"]\n")
        myfile.write("CurlyP_calc[power,constant] = ["+str(slope_CurlyP_calc)+","+str(np.exp(intercept_CurlyP_calc))+"]\n")
        myfile.close()
    #===============================================================================
        # Graphs for Julien
        radii_interpolate_physical = radii_interpolate_int[:index2[0][-1]:]*2*np.pi/Lbox
        centres_physical = centres*2*np.pi/Lbox
        
        plot.Graphs_PowerSpectrum(centres_physical,[PowerSpectrum_Phi,PowerSpectrum_Phi,PowerSpectrum_Delta[0],PowerSpectrum_Delta[0]],['Phi','Phi','delta','delta'],['$\hat{\Phi}$','$\hat{\Phi}$','$\hat{\delta}$','$\hat{\delta}$'],['','loglog','','loglog'],True,'Binning',runint)
        plot.Graphs_PowerSpectrum(radii_interpolate_physical,[CurlyP_calc,CurlyP_calc],['CurlyP','CurlyP'],['$\mathcal{P}(k)$','$\mathcal{P}(k)$'],['','loglog'],True,'Binning',runint)

        plot.Plot2D('calc-expected/expected','$k$ [Mpc$^{-1}$]','Error [%]',radii_interpolate_physical,percentage_error_CurlyP,0,'REAL_'+'Binning_'+'_Error in CurlyP_'+str(runint))

        plot.Plot2D('$\sigma^{2}_{calc} / \sigma$','$k$ [Mpc$^{-1}$]','',radii_interpolate_physical,difference,0,'REAL_'+'Binning_'+'ratio of sigmas_'+str(runint))
        plot.Plot2D('$\mathcal{P}_{calc} / \mathcal{P}$','$k$ [Mpc$^{-1}$]','',radii_interpolate_physical,CurlyP_calc/CurlyP_pos_real,0,'REAL_'+'Binning_'+'ratio of CurlyP_'+str(runint))
        plot.Plot2D('calc-expected/expected','$k$ [Mpc$^{-1}$]','Error [%]',radii_interpolate_physical,percentage_error_Sigma2,0,'REAL_'+'Binning_'+'Error in Sigma^2_'+str(runint))

    #===============================================================================
        # Graphs with h
        radii_interpolate_physical = radii_interpolate_int[:index2[0][-1]:]*2*np.pi/Lbox/0.7
        centres_physical = centres*2*np.pi/Lbox/0.7
        
        plot.Graphs_PowerSpectrum_h(centres_physical,[PowerSpectrum_Phi,PowerSpectrum_Phi,PowerSpectrum_Delta[0],PowerSpectrum_Delta[0]],['Phi','Phi','delta','delta'],['$\hat{\Phi}$','$\hat{\Phi}$','$\hat{\delta}$','$\hat{\delta}$'],['','loglog','','loglog'],'Binning',runint)
        plot.Graphs_PowerSpectrum_h(radii_interpolate_physical,[CurlyP_calc,CurlyP_calc],['CurlyP','CurlyP'],['$\mathcal{P}(k)$','$\mathcal{P}(k)$'],['','loglog'],'Binning',runint)

        plot.Plot2D('calc-expected/expected','$k$ [h.Mpc$^{-1}$]','Error [%]',radii_interpolate_physical,percentage_error_CurlyP,0,'REALwithh_'+'Binning_'+'_Error in CurlyP_'+str(runint))

        plot.Plot2D('$\sigma^{2}_{calc} / \sigma$','$k$ [h.Mpc$^{-1}$]','',radii_interpolate_physical,difference,0,'REALwithh_'+'Binning_'+'ratio of sigmas_'+str(runint))
        plot.Plot2D('$\mathcal{P}_{calc} / \mathcal{P}$','$k$ [h.Mpc$^{-1}$]','',radii_interpolate_physical,CurlyP_calc/CurlyP_pos_real,0,'REALwithh_'+'Binning_'+'ratio of CurlyP_'+str(runint))
        plot.Plot2D('calc-expected/expected','$k$ [h.Mpc$^{-1}$]','Error [%]',radii_interpolate_physical,percentage_error_Sigma2,0,'REALwithh_'+'Binning_'+'Error in Sigma^2_'+str(runint))
        
        # Graphs in wavelength    
        wavelength = np.divide(2*np.pi,radii_interpolate_physical)
        centres_wavelength = np.divide(2*np.pi,centres_physical)
        plot.Graphs_PowerSpectrum_wavelength(centres_wavelength,[PowerSpectrum_Phi,PowerSpectrum_Phi,PowerSpectrum_Delta[0],PowerSpectrum_Delta[0]],['Phi','Phi','delta','delta'],['$\hat{\Phi}$','$\hat{\Phi}$','$\hat{\delta}$','$\hat{\delta}$'],['','loglog','','loglog'],'Binning',runint)
        plot.Graphs_PowerSpectrum_wavelength(wavelength,[CurlyP_calc,CurlyP_calc],['CurlyP','CurlyP'],['$\mathcal{P}(\lambda)$','$\mathcal{P}(\lambda)$'],['','loglog'],'Binning',runint)

        plot.Plot2D('calc-expected/expected','$\lambda$ [Mpc.h$^{-1}$]','Error [%]',wavelength,percentage_error_CurlyP,0,'REALwithwavelength_'+'Binning_'+'_Error in CurlyP_'+str(runint))

        plot.Plot2D('$\sigma^{2}_{calc} / \sigma$','$\lambda$ [Mpc.h$^{-1}$]','',wavelength,difference,0,'REALwithwavelength_'+'Binning_'+'ratio of sigmas_'+str(runint))
        plot.Plot2D('$\mathcal{P}_{calc} / \mathcal{P}$','$\lambda$ [Mpc.h$^{-1}$]','',wavelength,CurlyP_calc/CurlyP_pos_real,0,'REALwithwavelength_'+'Binning_'+'ratio of CurlyP_'+str(runint))
        plot.Plot2D('calc-expected/expected','$\lambda$ [Mpc.h$^{-1}$]','Error [%]',wavelength,percentage_error_Sigma2,0,'REALwithwavelength_'+'Binning_'+'Error in Sigma^2_'+str(runint))
        
        # to save on RAM usage
        radii_interpolate_physical = None
        radii_interpolate_int = None
        wavelength = None
        centres_wavelength = None
    #===============================================================================
    # Initialising Cartesian Space
    plot.Graphs_CartesianSpace([Phiofk3D,Deltaofk3D,Velocityk3D_x,Velocityk3D_y,Velocityk3D_z],['Phi','delta','vx','vy','vz'],x,x,N,z,runint,Lbox) #['$\Phi$','$\delta$','vx','vy','vz']

    #===============================================================================
    # WHICH k's DO WE WANT???
    # Do we need to test whether the growing mode is working correctly?
    if (bool(inputvalues[9]))and(number != -1):
        magk = np.sqrt(pow(kx,2)+pow(ky,2)+pow(kz,2))
        kswewant = []
#        cutoff = radii_int[np.where(radii_int<=(term[0][1]-1))]
        for i in k_positive[1:(term+1):]:
            ktemp = np.where(magk==i)
            ktemp = [(k_int[ktemp[0][j]],k_int[ktemp[1][j]],k_int[ktemp[2][j]]) for j in range(len(ktemp[0]))]
            ktemp1 = [ktemp[0]]
            for l in range(len(ktemp)):
                compare = True
                for j in range(len(ktemp1)):
                    compare = compare and compareTuple(ktemp1[j],ktemp[l])
                if compare:
                    ktemp1.append(ktemp[l])
            kswewant = kswewant + ktemp1

        delta_at_k = []
        for j in kswewant:
            delta_at_k.append(abs(Deltaofk3D[j]))
        Saving.appendHeader(kswewant,'Delta')
        Saving.appendTimeStep(tau_start,delta_at_k,'Delta')
        delta_at_k = None

        velocity_x_at_k = []
        velocity_y_at_k = []
        velocity_z_at_k = []
        kswewant_velocity_x = []
        kswewant_velocity_y = []
        kswewant_velocity_z = []
        for j in kswewant:
            if j[2] != 0:
                kswewant_velocity_x.append(j)
            if j[1] != 0:
                kswewant_velocity_y.append(j)
            if j[0] != 0:
                kswewant_velocity_z.append(j)

        for j in kswewant_velocity_x:
            velocity_x_at_k.append(abs(Velocityk3D_x[j]))
        for j in kswewant_velocity_y:
            velocity_y_at_k.append(abs(Velocityk3D_y[j]))
        for j in kswewant_velocity_z:
            velocity_z_at_k.append(abs(Velocityk3D_z[j]))
        Saving.appendHeader(kswewant_velocity_x,'Velocityx')
        Saving.appendTimeStep(tau_start,velocity_x_at_k,'Velocityx')
        velocity_x_at_k = None
        Saving.appendHeader(kswewant_velocity_y,'Velocityy')
        Saving.appendTimeStep(tau_start,velocity_y_at_k,'Velocityy')
        velocity_y_at_k = None
        Saving.appendHeader(kswewant_velocity_z,'Velocityz')
        Saving.appendTimeStep(tau_start,velocity_z_at_k,'Velocityz')
        velocity_z_at_k = None

    #===============================================================================
    # The actual time stepping
    if number != -1:
        timestepsleft = number
        Velocityk3D_x_OLD = [np.copy(Velocityk3D_x)]
        Velocityk3D_y_OLD = [np.copy(Velocityk3D_y)]
        Velocityk3D_z_OLD = [np.copy(Velocityk3D_z)]
        Deltaofk3D_OLD = [np.copy(Deltaofk3D)]

        time = [tau_start]
        a_at_k1 = [TDFunctions.a_tau(time[-1],w)]

##        z = TDFunctions.a_tau(1.0,w)/TDFunctions.a_tau(time[-1],w) - 1
##        plotstoplot = [Deltaofk3D_OLD[0],Velocityk3D_x_OLD[0],Velocityk3D_y_OLD[0],Velocityk3D_z_OLD[0]]
##        plot.Graphs_FourierSpace(plotstoplot,['delta_hat','vx_hat','vy_hat','vz_hat'],k_int,k_int,N,z) #['$\delta$','vx','vy','vz']

        # The actual time stepping
        while(True):
            i = number - timestepsleft
            flag = not(Overflow([Velocityk3D_x,Velocityk3D_y,Velocityk3D_z,Deltaofk3D]))
            if(flag and timestepsleft > 0):

                temp = np.array([Velocityk3D_x_OLD[-1],Velocityk3D_y_OLD[-1],Velocityk3D_z_OLD[-1],Deltaofk3D_OLD[-1]])
                Total = TE.RungeKutta4(temp,kx,ky,kz,dt,time[-1],Lbox,nonlinear,Phiofk3D)

                Velocityk3D_x = np.copy(Total[0])
                Velocityk3D_y = np.copy(Total[1])
                Velocityk3D_z = np.copy(Total[2])
                Deltaofk3D = np.copy(Total[3])

                if len(Deltaofk3D_OLD)<4:
                    Velocityk3D_x_OLD.append(np.copy(Velocityk3D_x))
                    Velocityk3D_y_OLD.append(np.copy(Velocityk3D_y))
                    Velocityk3D_z_OLD.append(np.copy(Velocityk3D_z))
                    Deltaofk3D_OLD.append(np.copy(Deltaofk3D))
                else: # if There are 2 elements
                    del Velocityk3D_x_OLD[0]
                    del Velocityk3D_y_OLD[0]
                    del Velocityk3D_z_OLD[0]
                    del Deltaofk3D_OLD[0]

                    Velocityk3D_x_OLD.append(np.copy(Velocityk3D_x))
                    Velocityk3D_y_OLD.append(np.copy(Velocityk3D_y))
                    Velocityk3D_z_OLD.append(np.copy(Velocityk3D_z))
                    Deltaofk3D_OLD.append(np.copy(Deltaofk3D))

                time.append(tau_start+dt*(i+1))

                if abs(time[-1] - 0.25) < dt:
                    print("t =",time[-1])
                if abs(time[-1] - 0.5) < dt:
                    print("t =",time[-1])
                if abs(time[-1] - 0.75) < dt:
                    print("t =",time[-1])
                if abs(time[-1] - 1.0) < dt:
                    print("t =",time[-1])

                a_at_k1.append(TDFunctions.a_tau(time[-1],w))
                timestepsleft -= 1

                if (bool(inputvalues[9])):
                    delta_at_k = []
                    velocity_x_at_k = []
                    velocity_y_at_k = []
                    velocity_z_at_k = []
                    for j in kswewant:
                        delta_at_k.append(abs(Deltaofk3D[j]))
                    Saving.appendTimeStep(time[-1],delta_at_k,'Delta')
                    delta_at_k = None
                    for j in kswewant_velocity_x:
                        velocity_x_at_k.append(abs(Velocityk3D_x[j]))
                    Saving.appendTimeStep(time[-1],velocity_x_at_k,'Velocityx')
                    velocity_x_at_k = None
                    for j in kswewant_velocity_y:
                        velocity_y_at_k.append(abs(Velocityk3D_y[j]))
                    Saving.appendTimeStep(time[-1],velocity_y_at_k,'Velocityy')
                    velocity_y_at_k = None
                    for j in kswewant_velocity_z:
                        velocity_z_at_k.append(abs(Velocityk3D_z[j]))
                    Saving.appendTimeStep(time[-1],velocity_z_at_k,'Velocityz')
                    velocity_z_at_k = None

            else:
                if (flag):
                    y = 0
                else:
                    y = 2

                z = TDFunctions.a_tau(1.0,w)/TDFunctions.a_tau(time[-1-y],w) - 1
                plotstoplot = [Deltaofk3D_OLD[2-y],Velocityk3D_x_OLD[2-y],Velocityk3D_y_OLD[2-y],Velocityk3D_z_OLD[2-y]]
                plot.Graphs_FourierSpace(plotstoplot,['delta_hat','vx_hat','vy_hat','vz_hat'],k_int,k_int,N,z,runint) #['$\delta$','vx','vy','vz']
                print("tau_end =",time[-1-y])

                myfile = open(name+filename,"a")
                myfile.write("tau_end = "+str(time[-1])+"\n")
                myfile.close()
                break
            
#    # 36,36
#    ret = 21
#    expected_initial = np.multiply(abs(Deltaofk3D_OLD[-1]),pow(time[-1]/time[0],-2./3.))
#    expected_initial_2 = np.multiply(abs(Deltaofk3D_OLD[-2]),pow(time[-2]/time[0],-2./3.))
#    delta_ratio = np.divide(expected_initial,abs(Deltaofk3D_OLD[0]))
#    delta_ratio_2 = np.divide(expected_initial_2,abs(Deltaofk3D_OLD[0]))
#    
#    print '|k|=',ret,':',(delta_ratio[0][0][ret]), (delta_ratio_2[0][0][ret])
#    print '|k|=',ret+4,':',(delta_ratio[0][0][ret+4]), (delta_ratio_2[0][0][ret+4])
#    print np.exp(-36*((ret*2.0)/N)**36), np.exp(-36*((ret*2.0)/N)**36)**2, np.exp(-36*((ret*2.0)/N)**36)**3
#    print np.exp(-36*(((ret+4)*2.0)/N)**36), np.exp(-36*(((ret+4)*2.0)/N)**36)**2, np.exp(-36*(((ret+4)*2.0)/N)**36)**3

    #===============================================================================
    ### testing interpolation
    if (number == -1)and(methods[2]):
        # do the interpolation tests
        testingInterpolation(np.copy(Phiofk3D),radii_int[1::],k_int,N,Sigma,CurlyP,runint)

    #===============================================================================
    # testing the binning
    if (number == -1)and(methods[1]):
        # do the binning tests
        testingBinning(np.copy(Phiofk3D),radii_int[1::],k_int,N,sizeofbox,k_positive[1:-1:],inputvalues[11],runint)

    #===============================================================================
    if (number != -1):
##        z = TDFunctions.a_tau(1.0,w)/TDFunctions.a_tau(time[-1-y],w) - 1
        kmag_int = pow(kx,2) + pow(ky,2) + pow(kz,2)
        Phiofk3D = SFS.SFS_PoissonEquation_Phi(np.copy(Deltaofk3D_OLD[2-y]),kmag_int,Lbox,time[-1-y])
        plot.Graphs_CartesianSpace([Phiofk3D,Deltaofk3D_OLD[2-y],Velocityk3D_x_OLD[2-y],Velocityk3D_y_OLD[2-y],Velocityk3D_z_OLD[2-y]],['Phi','delta','vx','vy','vz'],x,x,N,z,runint,Lbox) #['$\Phi$','$\delta$','vx','vy','vz']

    if (number != -1):
        z = round(TDFunctions.a_tau(1.0,w)/TDFunctions.a_tau(time[-1-y],w) - 1,4)
        extension = str(z)+"N"+str(N)+"L"+str(Lbox)+"n"+str(n)+"PS"+str(PS_type)

        Saving.save3Darray(Deltaofk3D_OLD[2-y],name+"deltaatz"+extension)
        Saving.save3Darray(Velocityk3D_x_OLD[2-y],name+"Velocityxatz"+extension)
        Saving.save3Darray(Velocityk3D_y_OLD[2-y],name+"Velocityyatz"+extension)
        Saving.save3Darray(Velocityk3D_z_OLD[2-y],name+"Velocityzatz"+extension)

    #===============================================================================
    # Getting ready to draw the graphs for the growing mode  
    if (bool(inputvalues[9]))and(number != -1):
        Shuffle.flipCSVTable('Delta'+"_Growing mode.csv")
        Shuffle.flipCSVTable('Velocityx'+"_Growing mode.csv")
        Shuffle.flipCSVTable('Velocityy'+"_Growing mode.csv")
        Shuffle.flipCSVTable('Velocityz'+"_Growing mode.csv")
        
        if (inputvalues[14]==1):
            print("Growing mode without filter - START")
            Shuffle.graphing_procedure('Delta','Info.txt',k_int,k_positive,term,runint)
            #Shuffle.graphing_procedure('Velocityx','Info.txt',k_int,k_positive,term,runint)
            #Shuffle.graphing_procedure('Velocityy','Info.txt',k_int,k_positive,term,runint)
            #Shuffle.graphing_procedure('Velocityz','Info.txt',k_int,k_positive,term,runint)
            print("Growing mode without filter - END")

        if (inputvalues[14]==2)or(inputvalues[14]==3):
            print("Growing mode with filter - START")        
            Shuffle.graphing_procedure_filter('Delta','Info.txt',k_int,k_positive,term,runint)
            #Shuffle.graphing_procedure_filter('Velocityx','Info.txt',k_int,k_positive,term,runint)
            #Shuffle.graphing_procedure_filter('Velocityy','Info.txt',k_int,k_positive,term,runint)
            #Shuffle.graphing_procedure_filter('Velocityz','Info.txt',k_int,k_positive,term,runint)
            print("Growing mode with filter - END")
    
    #===============================================================================

for thing in range(int(inputvalues[10])):
    print('CODE RUN',thing)
    main(thing)
    print('DONE')


#===============================================================================
##Freq = 2500 # Set Frequency To 2500 Hertz
##Dur = 1000 # Set Duration To 1000 ms == 1 second
##winsound.Beep(Freq,Dur)