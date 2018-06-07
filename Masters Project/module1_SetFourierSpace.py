#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Michelle
#
# Created:     18/06/2014
# Copyright:   (c) Michelle 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import numpy as np
import random
import module3_Plotting as plot
import Unit_Tester as Utest

squareOn = False
fraction = 3.0

G = 6.674*10**(-20)                 # km^3.kg^(-1).s^(-2)
c = 3*10**5                         # Speed of light in km/s
H0 = 72                             # km.s^(-1).Mpc^(-1)

# makes sure it is the same random numbers evertime
random.setstate((3, (2147483648, 3635087714, 254740388, 2427586259, 2845298747, 1566649629, 884720386, 2012695761, 1197704598, 2026693099, 4213099081, 329010995, 2884189532, 2140859029, 3907692585, 3255238408, 3432540858, 2850834246, 322774062, 3703845368, 2213162561, 2128282436, 1183835041, 2809216415, 200698136, 1311580225, 490368730, 3477593773, 1146828278, 4157404385, 210529283, 3484201408, 3040189033, 446220540, 2191484059, 1790493970, 3043078026, 3733184292, 2557856245, 1351603915, 1032011690, 2199155968, 43973342, 3735887082, 1198289365, 4194472920, 2235801796, 1144858786, 2017593581, 241476923, 2307404378, 1983704267, 1585121771, 3902160927, 3381940301, 1500129619, 1765937128, 1984463733, 4258656443, 705032042, 1154418762, 2800899199, 69380699, 523353853, 1772576905, 1620971444, 2472452330, 3156838244, 1081972634, 966952790, 2691965645, 3456930430, 2442230249, 3307736275, 3970497504, 926957784, 815478737, 1494114967, 3489385029, 933388427, 1541489294, 2293526305, 956873058, 1037311254, 214545396, 731148115, 3585685130, 4148891301, 458807542, 2174709736, 3007101423, 3200537321, 460430774, 4225448753, 2150676339, 201590152, 4007321241, 3589882450, 253621166, 1096540076, 4273300170, 1378983339, 3893595231, 1598294395, 1978345643, 2634892683, 3987620594, 1646614730, 3088529466, 566408908, 427319141, 435787579, 3847006146, 2292469795, 1739281616, 82491753, 1699172277, 904070678, 2266493307, 2923877526, 4128136261, 3899770609, 1287560356, 1460439758, 317681039, 3789711895, 2929059954, 1643978533, 4244613016, 3620962746, 4079850000, 1809048054, 3540145886, 333558699, 489757713, 3931539848, 787198436, 154964963, 2639865052, 3461783598, 2970544436, 999599687, 3039804159, 4101850358, 1834492149, 699734157, 37365304, 2264960498, 3828999133, 3387537074, 2498692241, 1678000276, 293849528, 3013457857, 1079602890, 3939228568, 2337264326, 2326425875, 114086610, 3546128216, 3515273327, 1669767221, 1264873875, 2835818654, 3231392964, 2022429530, 918182049, 704838310, 4235316050, 476788896, 1358547450, 748972970, 1414726854, 3510530082, 1077674666, 243323698, 3415607171, 952198716, 1379117178, 3333698380, 1446698245, 183913800, 512804276, 3489911250, 910016328, 465068671, 3456844685, 1222578716, 831081899, 1527140304, 3678876454, 3481716730, 561919243, 3075279285, 2620790211, 301297114, 107206769, 805982664, 3875201108, 2017487924, 3906662872, 1405257535, 285443098, 1180176041, 2535849004, 2069675399, 3029475168, 2864981010, 2656596976, 3913176512, 974802891, 3739662983, 252090435, 2882526313, 1396733314, 751764535, 1368431236, 3946704068, 84261454, 3124664136, 2200457601, 1444446356, 4282313124, 799265189, 1874017078, 121216719, 1264485181, 1167531568, 2038117436, 1337786294, 3894174011, 4108467422, 918388605, 4150596355, 3549316186, 1373580924, 1900285196, 3228208187, 1799756611, 2190799258, 4157545266, 408854099, 3737897404, 345540181, 2072688262, 3405860947, 472911027, 2053655410, 1278991256, 597408504, 816870873, 875203388, 603343273, 843329526, 2103454738, 3059866428, 2717903719, 2059757191, 3460316926, 949376064, 676235050, 336669064, 3946965323, 2626411435, 3761090055, 2220976701, 1688714956, 2479077751, 1191731818, 775879525, 1242272628, 359220726, 2455176361, 3408977283, 1068500923, 3815320179, 2450809657, 3649254675, 1814560518, 3668669288, 1489168057, 3300998375, 2678766188, 1971330683, 748305686, 2937149223, 1571645523, 3221231320, 1018393560, 2451151667, 690066011, 2305541742, 2995593897, 2207392236, 3860894579, 2533891348, 1940395146, 2451861061, 3499508683, 1297478502, 3232963415, 518316617, 442831113, 3916214926, 4040295890, 860500815, 4097041631, 1186678903, 3028412972, 4049363271, 1984386477, 620181101, 2744926587, 3965886890, 1941372576, 3066556901, 2425775241, 2421926777, 2460083712, 1285753299, 1288595452, 141530051, 3529853041, 3435137752, 36262451, 3814373240, 932789013, 912124853, 2740596106, 2107903798, 1728415053, 2023150859, 2713133114, 3123104446, 1331565798, 2193499190, 1613101893, 2087944800, 1067777866, 3620264913, 1863135694, 3642215747, 2057516231, 1185144587, 1000585078, 4185327933, 1302234540, 2726705887, 3539837885, 1966786250, 454863592, 2233952867, 3004780813, 1648877958, 892614256, 1877146747, 2231867912, 502097697, 187345447, 3473138646, 1377691720, 1140006581, 2816418268, 330295963, 1507560194, 697536394, 3087258469, 989802417, 962477763, 2645596839, 3914422082, 284113074, 1397845623, 2803890766, 1011538729, 3130178596, 3192636833, 4149399166, 3741356248, 1464527823, 193013269, 427546896, 1467176874, 2217146582, 3168440364, 702708805, 3939022313, 2110073471, 2831251760, 2327966908, 3604565305, 3938484067, 4236533974, 1356617351, 3955231669, 35523844, 597620844, 1783517301, 3905302930, 1955812330, 3800323154, 3383679861, 3969203658, 2226149289, 3945504712, 2903519891, 2048598847, 1333304727, 2205062966, 1662817126, 1921397338, 4190592989, 3461361592, 3250128035, 3846667321, 4219767731, 2720428051, 3379103949, 790048384, 831498987, 2653524891, 3031157405, 412676099, 1519196036, 2900953065, 3719196544, 3930916988, 378965513, 2319645826, 4185396287, 2963308720, 457606264, 2623044701, 2990258597, 2616851670, 887250349, 3058732645, 139780354, 1638755138, 1056392788, 3200741939, 2531122898, 3013306739, 1924239001, 439443895, 4160330084, 4065494861, 2236933934, 2493441230, 2538771418, 1137558515, 3751517049, 2831131349, 1846318068, 1811855633, 1883929655, 2814196567, 4167731981, 3468892190, 3823214347, 2185886860, 624877724, 3944440646, 4105762681, 2429038025, 300617681, 3798638377, 3618799445, 813172634, 1569187504, 1046406500, 2516411652, 1586446299, 277411852, 4154309310, 753383125, 252463315, 3265972188, 682437423, 3142482144, 2903477439, 167187984, 1007266805, 3910822177, 3299898746, 4002937149, 2406654937, 2395496641, 2138714049, 3097436562, 3127726163, 2749361608, 2591438966, 3014290886, 2684842440, 1894324878, 3725364939, 492340603, 1594563123, 4158547082, 3420470043, 3032118314, 2255373718, 3715704975, 1417993918, 1940502380, 2730872020, 879976465, 3184835406, 4056470905, 3100412526, 1824747989, 1010824977, 2114114069, 2410158947, 1813264498, 568313666, 183180288, 3205998490, 3770156250, 807807345, 4260985313, 4078085530, 3378505305, 194112775, 2721314436, 2351348275, 732119869, 2923681725, 102070356, 1519814872, 318687026, 860985440, 3088431898, 1441201816, 951535178, 2786556640, 231515611, 2476573388, 3792581487, 333007395, 1929177157, 2952019443, 3974678581, 1867282049, 2636109925, 3311710639, 3061481580, 1010891648, 1924770577, 4177140059, 3531022340, 3815175327, 2610963627, 862827206, 1857405017, 3314164113, 1864922489, 2760254699, 4112665759, 1556331904, 1841926086, 3281385168, 1817432199, 1223579047, 2681322571, 358272562, 1110680734, 1012886765, 206529117, 3370409068, 3538568918, 3882768786, 316799840, 3633162943, 276104546, 3491974044, 2751911999, 506964455, 2257901841, 2675843175, 243263810, 1071443533, 2382163422, 570043048, 449190322, 2027961845, 3217220395, 922590461, 127688287, 1676617344, 1889623436, 2369890773, 1172929728, 39682273, 7394901, 3568115189, 4017844139, 824813809, 3892626790, 3443782148, 3249914614, 106635595, 314042550, 349630598, 3263853214, 2708853877, 3920395837, 1952471523, 3330720902, 3494177787, 25920659, 3168118191, 2406082531, 2677609929, 3344711265, 2037113270, 2966819858, 2225144373, 3266705917, 203036065, 565096471, 3751954769, 837704880, 624), None))

def create_filterarray(kx,ky,kz,ftype="step",variable=2./3.):
    N = len(kx[0][0])
    ratio = np.divide(np.sqrt(pow(kx,2)+pow(ky,2)+pow(kz,2)),(N/2*1.0))
    if (ftype == "exp")or(ftype == 2):
        temp = np.exp(-variable[0]*pow(ratio,variable[1])) 
    elif (ftype == "expS")or(ftype == 3):
        temp = np.exp(-variable[0]*pow(ratio+1./3.,variable[1]))
    else: # ftype == "step"
        temp = np.zeros((N,N,N))
        temp[np.where(ratio<=(variable[0]))] = 1.0     
    return temp 
    
def create_filterfactor(ktemp,Ntemp,ftype="step",variable=2./3.):
    ratio = ktemp / (Ntemp/2*1.0)
    temp = 0.0
    if (ftype == "exp")or(ftype == 2):
        temp = np.exp(-variable[0]*pow(ratio,variable[1])) 
    elif (ftype == "expS")or(ftype == 3):
        temp = np.exp(-variable[0]*pow(ratio+1./3.,variable[1]))
    else: # ftype == "step"
        if ratio<=(variable[0]):
            temp = 1.0
    return temp


def Phi(sigma2temp,howmany):
    """
    Chooses bold P of phi using a gaussian

    @type    meantemp: float
    @param   meantemp:
    @type  sigma2temp: float
    @param sigma2temp:

    @rtype:            float
    @return:
    """
##    return random.gauss(meantemp,sigma2temp)
    if sigma2temp == 0.0:
        return 0.0
    else:
        return np.random.rayleigh(sigma2temp,1)


def SFS_Phi(Ntemp,radii,k_real,Sigmatemp,boolRayleigh,Ltemp,boolNotrandom=False):
    """
    my latest attempt to fix this function

    @type      Ntemp: integer
    @param     Ntemp:
    @type      radii: np.array
    @param     radii:
    @type     k_real: np.array
    @param    k_real:
    @type  Sigmatemp: np.array
    @param Sigmatemp:

    @rtype:           np.array
    @return:
    """
    # I want waves going out of zero with a frequency of p
    term = pow(2*np.pi,-3)#pow(Ntemp,-3)#pow(Ltemp/(2*np.pi),-3)#pow(Ltemp,-3)#pow(2*np.pi,-3)

    if boolRayleigh:
        Phi_hat = np.zeros((Ntemp,Ntemp,Ntemp))
        for i in range(Ntemp//2+1):
            for k in range(Ntemp):
                for l in range(Ntemp):
                    r = np.sqrt(pow(k_real[i],2)+pow(k_real[k],2)+pow(k_real[l],2))
                    index = np.where(r==radii)
                    if boolNotrandom:
                        if r == 0:
                            temp = 0.0
                        else:
                            temp = 10**(-6)

                    else:
                        sigma_rayleigh = 1.0*Sigmatemp[index]#*term
                        temp = Phi(np.sqrt(sigma_rayleigh),1)
                    Phi_hat[i,k,l] = temp
                    Phi_hat[-i,-k,-l] = np.copy(Phi_hat[i,k,l])

        Angle = np.zeros((Ntemp,Ntemp,Ntemp))
        for i in range(int(Ntemp/2)):
            for k in range(Ntemp):
                for l in range(Ntemp):
                    Angle[i][k][l] =  random.random()*2*np.pi
                    Angle[-i][-k][-l] = -np.copy(Angle[i][k][l])
        temp3 = np.multiply(Phi_hat,np.cos(Angle)+1j*np.sin(Angle))
    else:
        Phi_hat = np.zeros((Ntemp,Ntemp,Ntemp),complex)
        for i in range(int(Ntemp//2+1)):
            for k in range(Ntemp):
                for l in range(Ntemp):
                    r = np.sqrt(pow(k_real[i],2)+pow(k_real[k],2)+pow(k_real[l],2))
                    index = np.where(r==radii)
                    if boolNotrandom:
                        if r == 0:
                            temp = 0.0
                        else:
                            temp = 1.0/r * 10**(-6)
                    else:
                        sigma_gauss = 1.0*Sigmatemp[index[0][0]]#*term
                        temp = random.gauss(0,np.sqrt(sigma_gauss)) + 1j*random.gauss(0,np.sqrt(sigma_gauss))

                    Phi_hat[i,k,l] = temp
                    Phi_hat[-i,-k,-l] = np.conjugate(Phi_hat[i,k,l])
        temp3 = np.copy(Phi_hat)

    return temp3


def SFS_PoissonEquation_Phi(deltatemp,kmagtemp,Ltemp,tautemp):
    """
    Using triangle M{\Phi = 4*\pi*\rho*a^2*H_0^{-2}*\delta} to get Phi

    @type  deltatemp: np.array
    @param deltatemp: M{\delta (kx,ky,kz)}
    @type      kmagtemp: np.array
    @param     kmagtemp: (|k|^2) = kx^2 + ky^2 + kz^2
                         Usually M{[0,1,\ldots,\frac{N}{2}-1,\frac{N}{2},-\frac{N}{2}+1,\ldots,-1]} in 1D.
    @type       tautemp: float
    @param      tautemp: the time in dimensionless units, contained in [0,1] where 0
                         represents the beginning of the universe and 1 represents the
                         present day
    @type         Ltemp: float
    @param        Ltemp: the physical size of the box in Mpc

    @rtype:           np.array
    @return:
    """
    dimensionlessterm = -(3.0/2.0)*pow((Ltemp*H0)/(2*np.pi*c),2)
    tauterm = pow(tautemp,-2.0/3.0)
    temp = np.divide(dimensionlessterm*tauterm*deltatemp,kmagtemp)

    temp[np.isnan(temp)] = 0.0
    temp[np.isinf(temp)] = 0.0
    return temp


def SFS_Delta_growing(Phiofk3Dtemp,tautemp,kmagtemp,Ltemp):
    """
    This sets the initial Delta in Fourier space

    @type  Phiofk3Dtemp: np.array
    @param Phiofk3Dtemp: M{\Phi (kx,ky,kz)}
    @type      kmagtemp: np.array
    @param     kmagtemp: (|k|^2) = kx^2 + ky^2 + kz^2
                         Usually M{[0,1,\ldots,\frac{N}{2}-1,\frac{N}{2},-\frac{N}{2}+1,\ldots,-1]} in 1D.
    @type       tautemp: float
    @param      tautemp: the time in dimensionless units, contained in [0,1] where 0
                         represents the beginning of the universe and 1 represents the
                         present day
    @type         Ltemp: float
    @param        Ltemp: the physical size of the box in Mpc

    @rtype:              np.array
    @return:
    """
    dimensionedterm = pow((2*np.pi*c)/(Ltemp*H0),2)
    tauterm = pow(tautemp,2.0/3.0)
    temp = np.multiply(-(2.0/3.0)*dimensionedterm*tauterm*kmagtemp,Phiofk3Dtemp)
    return temp


def SFS_Alpha(Phiofk3Dtemp,atemp):
    """
    Returns M{\alpha=a*(1+\Phi)}

    @type  Phiofk3Dtemp: np.array
    @param Phiofk3Dtemp: M{\Phi (kx,ky,kz)}
    @type         atemp: float
    @param        atemp:

    @rtype:              np.array
    @return:
    """
    temp = np.copy(Phiofk3Dtemp)
    temp[0][0][0] += 1.0
    temp = np.multiply(atemp,temp)
    return temp


def SFS_Velocity_growing(Phiofk3Dtemp,tautemp,diffcoord,Ltemp):
    """
    This sets the initial velocity in Fourier space such that the decaying mode is zero

    @type  Phiofk3Dtemp: np.array
    @param Phiofk3Dtemp: M{\Phi (kx,ky,kz)}
    @type       tautemp: float
    @param      tautemp: the time in dimensionless units, contained in [0,1] where 0
                         represents the beginning of the universe and 1 represents the
                         present day
    @type     diffcoord: np.array
    @param    diffcoord: these are the wavenumbers. Usually M{[0,1,\ldots,\frac{N}{2}-1,\frac{N}{2},-\frac{N}{2}+1,\ldots,-1]} in 1D.
                         To stop the higher frequencies the N/2 position is made zero
    @type         Ltemp: float
    @param        Ltemp: the physical size of the box in Mpc

    @rtype:              np.array
    @return:
    """
    dimensionlessterm = pow((4*np.pi*c)/(3*Ltemp*H0),2)
    tauterm = pow(tautemp,1.0/3.0)
    temp = np.multiply(-dimensionlessterm*tauterm*1j*diffcoord,Phiofk3Dtemp)
    return temp

def main():
    N=54

    # All the k's I need
    k_positive = np.arange(0,N/2+1,1)
    k_negative = np.arange(-N/2+1,0,1)
    k_int = np.concatenate((k_positive,k_negative))

    # k for differentiating
    k = np.copy(k_int)
    ky,kz,kx = np.meshgrid(k,k,k)
    kmag = pow(kx,2) + pow(ky,2) + pow(kz,2)

    Phi = np.ones((N,N,N))*10**(-6)
    Delta = SFS_Delta_growing(Phi,kmag,0.5,4166)
    Phi2 = SFS_PoissonEquation_Phi(Delta,kmag,4166,0.5)
    Delta2 = SFS_Delta_growing(Phi2,kmag,0.5,4166)
    Utest.vaugeTest(Delta,Delta2,10)
##    for i in range(N):
##        for j in range(N):
##            for h in range(N):
##                if Phi[i,j,h] != Phi2[i,j,h]:
##                    print('Point:',i,j,h,'Phi_1',Phi[i,j,h],'Phi_2',Phi2[i,j,h])
    print(Phi[np.where(Phi != Phi2)])
    print(Phi2[np.where(Phi != Phi2)])
    print(Phi[0,0,3],Phi2[0,0,3])
##    print(Phi2)


if __name__ == '__main__':
    main()