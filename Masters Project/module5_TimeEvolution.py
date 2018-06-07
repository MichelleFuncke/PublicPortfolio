#-------------------------------------------------------------------------------
# Name:        module5_TimeEvolution
# Purpose:
#
# Author:      Michelle
#
# Created:     15/11/2013
# Copyright:   (c) Michelle 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import Global_variables as Gv
import numpy as np
import module2_TimeDependentFunctions as TDFunctions
import module1_SetFourierSpace as SFS
import module3_Plotting as plot
import Unit_Tester
import random
import module8_savingtocsv as Saving

def derivative(ktemp,gridtemp):
    """
    This function does the derivative in fourier space
    ktemp will be the required direction derivative ie kx or ky

    @type     ktemp: np.array
    @param    ktemp: these are the wavenumbers. Usually M{[0,1,\ldots,\frac{N}{2}-1,\frac{N}{2},-\frac{N}{2}+1,\ldots,-1]} in 1D.
                     To stop the higher frequencies the M{\frac{N}{2}} position is made zero
    @type  gridtemp: np.array
    @param gridtemp: function we want the derivative of. In fourier space

    @rtype:          np.array
    @return:         the derivative of gridtemp in fourier space
    """
    if len(ktemp) == len(gridtemp):
        return np.multiply(1j*ktemp,gridtemp)
    else:
        print("ktemp and gridtemp aren't the same size check module5 line 37")
        return gridtemp


def DotTerm(vtemp,kxtemp,kytemp,kztemp,index,Ltemp):
    """
    Does the M{u_1*\partial_x u_1 + u_2*\partial_y u_1 + u_3*\partial_z u_1}

    @type   vtemp: np.array
    @param  vtemp: (vx,vy,vz)
    @type  kxtemp: np.array
    @param kxtemp: these are the x components of the wavenumbers.
                   Usually M{[0,1,\ldots,\frac{N}{2}-1,\frac{N}{2},-\frac{N}{2}+1,\ldots,-1]} in 1D.
    @type  kytemp: np.array
    @param kytemp: these are the y components of the wavenumbers.
                   Usually M{[0,1,\ldots,\frac{N}{2}-1,\frac{N}{2},-\frac{N}{2}+1,\ldots,-1]} in 1D.
    @type  kztemp: np.array
    @param kztemp: these are the z components of the wavenumbers.
                   Usually M{[0,1,\ldots,\frac{N}{2}-1,\frac{N}{2},-\frac{N}{2}+1,\ldots,-1]} in 1D.
    @type   index: integer
    @param  index: which of the velocity terms we want. 0 -> M{u_x},1 -> M{u_y}, 2 -> M{u_z}

    @rtype:        np.array
    @return:       M{u_1*\partial_x u_1 + u_2*\partial_y u_1 + u_3*\partial_z u_1}
    """
    diff_x = derivative(kxtemp,vtemp[index])
    diff_y = derivative(kytemp,vtemp[index])
    diff_z = derivative(kztemp,vtemp[index])

    temp1 = Convolution(diff_x,vtemp[0],Ltemp)
    temp2 = Convolution(diff_y,vtemp[1],Ltemp)
    temp3 = Convolution(diff_z,vtemp[2],Ltemp)

    return temp1 + temp2 + temp3

def Convolution_deltav(vtemp,delta,Ltemp):
    """
    This assumes vtemp has 3 components of 3D arrays and delta is a 3D array
    Also, they must be in fourier form

    @type  vtemp: np.array
    @param vtemp: M{(v_x,v_y,v_z)}
    @type  delta: np.array
    @param delta: the fourier transform of delta

    @rtype:       np.array
    @return:      M{(v_x*\delta,v_y*\delta,v_z*\delta)}
    """
    temp = np.copy(delta)

    x = Convolution(temp,vtemp[0],Ltemp)
    y = Convolution(temp,vtemp[1],Ltemp)
    z = Convolution(temp,vtemp[2],Ltemp)

    return np.array([x,y,z])

def Convolution(firsterm,Secondterm,Ltemp):
    """
    Doing the convolution I forgot about

    @type    firsterm: np.array
    @param   firsterm:
    @type  Secondterm: np.array
    @param Secondterm:

    @rtype:            np.array
    @return:           the convolution of the firsterm and the secondterm
    """
#   Have to be careful of the factors of N
    Spacial1 = np.real(np.fft.ifftn(firsterm))*pow(2*np.pi,-3.0/2.0)
    Spacial2 = np.real(np.fft.ifftn(Secondterm))*pow(2*np.pi,-3.0/2.0)

    Multiply = np.multiply(Spacial1,Spacial2)
    Spacial1 = None
    Spacial2 = None
    Const = np.size(firsterm)*pow(2*np.pi,-3.0/2.0)#*pow(Ltemp/(2*np.pi),-3)#pow(Ltemp,-3)
    temp = np.multiply(np.fft.fftn(Multiply),Const)
##    temp = np.fft.fftn(Multiply)
    return temp


def FunctionD(TempAll,kxtemp,kytemp,kztemp,tau,Ltemp,nonlinear,Phitemp):
    """
    This is where I evolve delta using
    M{v dt = -Hv -1/a*(v \cdot \nabla)*v -1/a*(dx + dy + dz)*\Phi} - no pressure term
    M{\delta dt = -1/a*(dx + dy + dz)*((1+\delta)*v)}

    @type  TempAll: np.array
    @param TempAll: [velocity_x,velocity_y,velocity_z,delta]
    @param  kxtemp: these are the x components of the wavenumbers.
                    Usually M{[0,1,\ldots,\frac{N}{2}-1,\frac{N}{2},-\frac{N}{2}+1,\ldots,-1]} in 1D.
    @type   kytemp: np.array
    @param  kytemp: these are the y components of the wavenumbers.
                    Usually M{[0,1,\ldots,\frac{N}{2}-1,\frac{N}{2},-\frac{N}{2}+1,\ldots,-1]} in 1D.
    @type   kztemp: np.array
    @param  kztemp: these are the z components of the wavenumbers.
                    Usually M{[0,1,\ldots,\frac{N}{2}-1,\frac{N}{2},-\frac{N}{2}+1,\ldots,-1]} in 1D.
    @type      tau: float
    @param     tau: the time in dimensionless units, contained in [0,1] where 0
                    represents the beginning of the universe and 1 represents the
                    present day
    @type    Ktemp: float
    @param   Ktemp:
    @type    Gtemp: float
    @param   Gtemp: Gravitational constant. Usually made =1 to simplify calculations
    @type    wtemp: float
    @param   wtemp: pressureless matter M{\omega=0.0}, radiation M{\omega=\frac{1}{3}}

    @rtype:         np.array
    @return:        new [velocity_x,velocity_y,velocity_z,delta]
    """
#   Creating all the terms, taking copies to be sure it's okay
    factor = 1#10**(-1)
    v_hat = [np.copy(TempAll[0]),np.copy(TempAll[1]),np.copy(TempAll[2])]
    a = TDFunctions.a_tau(tau,0)
    if nonlinear:
        convolved_hat = Convolution_deltav(v_hat,TempAll[3],Ltemp)

    #   Getting all the necessary derivatives
        deltav_x = derivative(kxtemp,convolved_hat[0])
        deltav_y = derivative(kytemp,convolved_hat[1])
        deltav_z = derivative(kztemp,convolved_hat[2])
        convolved_hat = None
##        Saving.save3Darray(-(1/a)*deltav_x,"Datafiles\\grad_delta_vx_witha")
##        Saving.save3Darray(-(1/a)*deltav_y,"Datafiles\\grad_delta_vy_witha")
##        Saving.save3Darray(-(1/a)*deltav_z,"Datafiles\\grad_delta_vz_witha")


    vx_x = derivative(kxtemp,v_hat[0])
    vy_y = derivative(kytemp,v_hat[1])
    vz_z = derivative(kztemp,v_hat[2])
##    Saving.save3Darray(-(1/a)*vx_x,"Datafiles\\grad_vx_witha")
##    Saving.save3Darray(-(1/a)*vy_y,"Datafiles\\grad_vy_witha")
##    Saving.save3Darray(-(1/a)*vz_z,"Datafiles\\grad_vz_witha")

#   Setting the time dependent quantities
    Ht0 = (2.0/3.0)/tau
    constantterm = (4*np.pi*SFS.c)/(3*Ltemp*SFS.H0)

    #   Getting the new density contrast
    delta_t = - (1.0/a)*(vx_x + vy_y + vz_z) #np.zeros((N,N,N),complex)
    vx_x = None
    vy_y = None
    vz_z = None
    if nonlinear:
        delta_t += (deltav_x + deltav_y + deltav_z)*(-1.0/a)
        deltav_x = None
        deltav_y = None
        deltav_z = None

##    kmagtemp = pow(kxtemp,2) + pow(kytemp,2) + pow(kztemp,2)
##    Phi_hat = SFS.SFS_PoissonEquation_Phi(TempAll[3],kmagtemp,Ltemp,tau)
    Phi_hat = np.copy(Phitemp)
##    kmagtemp = None

    Phi_x = derivative(kxtemp,Phi_hat)
    Phi_y = derivative(kytemp,Phi_hat)
    Phi_z = derivative(kztemp,Phi_hat)
    Phi_hat = None

#   Getting the new velocity for each component
    var1 = np.multiply(Ht0,v_hat[0])
##    Saving.save3Darray(var1,"Datafiles\\Ht0_vx")
    var2 = np.multiply((1.0/a)*pow(constantterm,2),Phi_x)
##    Saving.save3Darray(var2,"Datafiles\\Phi_x")
    vcordx_t = -(var1 + var2)
    if nonlinear:
        var3 = np.multiply((factor)*(1.0/a),DotTerm(v_hat,kxtemp,kytemp,kztemp,0,Ltemp))
##        Saving.save3Darray(var3,"Datafiles\\v_grad_vx")
        vcordx_t -= var3

    var1 = np.multiply(Ht0,v_hat[1])
##    Saving.save3Darray(var1,"Datafiles\\Ht0_vy")
    var2 = np.multiply((1.0/a)*pow(constantterm,2),Phi_y)
##    Saving.save3Darray(var2,"Datafiles\\Phi_y")
    vcordy_t = -(var1 + var2)
    if nonlinear:
        var3 = np.multiply((factor)*(1.0/a),DotTerm(v_hat,kxtemp,kytemp,kztemp,1,Ltemp))
##        Saving.save3Darray(var3,"Datafiles\\v_grad_vy")
        vcordy_t -= var3

    var1 = np.multiply(Ht0,v_hat[2])
##    Saving.save3Darray(var1,"Datafiles\\Ht0_vz")
    var2 = np.multiply((1.0/a)*pow(constantterm,2),Phi_z)
##    Saving.save3Darray(var2,"Datafiles\\Phi_z")
    vcordz_t = -(var1 + var2)
    if nonlinear:
        var3 = np.multiply((factor)*(1.0/a),DotTerm(v_hat,kxtemp,kytemp,kztemp,2,Ltemp))
##        Saving.save3Darray(var3,"Datafiles\\v_grad_vz")
        vcordz_t -= var3

##    filterarray = SFS.create_filterarray(54,"step",2./3.)
    

##    Saving.save3Darray(delta_t,"Datafiles\\delta_t")
##    Saving.save3Darray(vcordx_t,"Datafiles\\vx_t")
##    Saving.save3Darray(vcordy_t,"Datafiles\\vy_t")
##    Saving.save3Darray(vcordz_t,"Datafiles\\vz_t")

    return np.array([vcordx_t,vcordy_t,vcordz_t,delta_t])

def RungeKutta4(functionstemp,tempkx,tempky,tempkz,timestep,tau,Ltemp,nonlinear,Phitemp):
    """
    Fourth order Runge-Kutta using Fourier

    @type  functionstemp: np.array
    @param functionstemp: [velocity_x,velocity_y,velocity_z,delta]
    @param        kxtemp: these are the x components of the wavenumbers.
                          Usually M{[0,1,\ldots,\frac{N}{2}-1,\frac{N}{2},-\frac{N}{2}+1,\ldots,-1]} in 1D.
    @type         kytemp: np.array
    @param        kytemp: these are the y components of the wavenumbers.
                          Usually M{[0,1,\ldots,\frac{N}{2}-1,\frac{N}{2},-\frac{N}{2}+1,\ldots,-1]} in 1D.
    @type         kztemp: np.array
    @param        kztemp: these are the z components of the wavenumbers.
                          Usually M{[0,1,\ldots,\frac{N}{2}-1,\frac{N}{2},-\frac{N}{2}+1,\ldots,-1]} in 1D.
    @type       timestep: float
    @param      timestep:
    @type            tau: float
    @param           tau: the time in dimensionless units, contained in [0,1] where 0
                          represents the beginning of the universe and 1 represents the
                          present day
    @type          Ktemp: float
    @param         Ktemp:
    @type          Gtemp: float
    @param         Gtemp: Gravitational constant. Usually made =1 to simplify calculations
    @type          wtemp: float
    @param         wtemp: pressureless matter M{\omega=0.0}, radiation M{\omega=\frac{1}{3}}

    @rtype:               np.array
    @return:              new [velocity_x,velocity_y,velocity_z,delta]
    """
    v1 = np.copy(functionstemp)

    Dv1 = FunctionD(v1,tempkx,tempky,tempkz,tau,Ltemp,nonlinear,Phitemp)
    v2 = v1 + np.multiply(timestep/2.0,Dv1)

    Dv2 = FunctionD(v2,tempkx,tempky,tempkz,tau + timestep/2.0,Ltemp,nonlinear,Phitemp)
    v2 = None
    v3 = v1 + np.multiply(timestep/2.0,Dv2)

    Dv3 = FunctionD(v3,tempkx,tempky,tempkz,tau + timestep/2.0,Ltemp,nonlinear,Phitemp)
    v3 = None
    v4 = v1 + np.multiply(timestep,Dv3)

    Dv4 = FunctionD(v4,tempkx,tempky,tempkz,tau + timestep,Ltemp,nonlinear,Phitemp)
    v4 = None

    templist = (Dv1 + np.multiply(2.0,Dv2) + np.multiply(2.0,Dv3) + Dv4)
    Final = v1 + np.multiply((timestep/6.0),templist)
    
    temp1 = Gv.filter_variables
    filterarray = SFS.create_filterarray(tempkx,tempky,tempkz,temp1[0],temp1[1])
    #slicefilter = filterarray[0][0]
    #plot.Plot2D('','x','filter',tempkx[0][0],slicefilter,0,'test')
    Final2 = []
    Final2.append(np.multiply(filterarray,Final[0]))
    Final2.append(np.multiply(filterarray,Final[1]))
    Final2.append(np.multiply(filterarray,Final[2]))
    Final2.append(np.multiply(filterarray,Final[3]))
    temp1 = None
    
    return Final2


def main():
    N = 50

##    # testing Convolution works
##    x = np.arange(0.0,1.0,1./N)
##
##    k_positive = np.arange(0,N/2+1,1)
##    k_negative = np.arange(-N/2+1,0,1)
##    k_int = np.concatenate((k_positive,k_negative))
##
##    fy,fz,fx = np.meshgrid(x,x,x)
##    function = np.cos(2*np.pi*fx)
##    function_hat = np.fft.fftn(function)
##    functionN_hat = function_hat/pow(N,3)
##    function2 = np.cos(2*np.pi*fx)
##    function2_hat = np.fft.fftn(function2)
##    function2N_hat = function2_hat/pow(N,3)
##
##    px,py = np.meshgrid(x,x)
##    multiply = np.multiply(function,function2)
##    multiply2 = np.multiply(multiply,function)
##    multiply3 = np.multiply(multiply2,function)
##    multiply4 = np.multiply(multiply3,function)
##    plot.Plot3D(multiply4,0,px,py,'x','y','Expected','expected')
##    convolved_hat = Convolution(functionN_hat,function2N_hat)
##    convolved_hat2 = Convolution(convolved_hat,functionN_hat)
##    convolved_hat3 = Convolution(convolved_hat2,functionN_hat)
##    convolved_hat4 = Convolution(convolved_hat3,functionN_hat)
##
##    convolved = np.real(np.fft.ifftn(convolved_hat4*pow(N,3)))
##    plot.Plot3D(convolved,0,px,py,'x','y','Convolution result','convolution_result')
##    Unit_Tester.vaugeTest(convolved,multiply4,10)
##
##    kx,ky = np.meshgrid(k_int,k_int)
##    plot.Plot3D(np.abs(convolved_hat4),0,kx,ky,'kx','ky','after convolution','convolution_fourier')
##    expected = np.multiply(y,y)
##    calculated_hat = Convolution(yN_hat,yN_hat)
##    calculated = np.real(np.fft.ifft(calculated_hat*pow(N,1)))
##    Unit_Tester.vaugeTest(expected,calculated,10)
##
##    v_hat = np.zeros(N,complex)
##    v_hat[1] = 0.5
##    v_hat[-1] = 0.5
##    convoluted_hat = Convolution(v_hat,v_hat)
##    convoluted = np.real(np.fft.ifft(convoluted_hat*pow(N,1)))
##    Unit_Tester.vaugeTest(expected,convoluted,10)

##    # Testing functionD
##    z = 10
##    beginningtime = TDFunctions.start_tau(z,0.0)
##    sizeofbox = 1.0
##    h = (sizeofbox)/(N*1.0)
##    grid_factor = 2.0*np.pi/sizeofbox
##    # All the k's I need
##    k_positive = np.arange(0,N/2+1,1)
##    k_negative = np.arange(-N/2+1,0,1)
##    k_int = np.concatenate((k_positive,k_negative))
##    k_real = np.multiply(k_int,grid_factor)
##
##    # k for differentiating
##    k = np.copy(k_real)
##    k[N//2] = 0.0
##    ky,kz,kx = np.meshgrid(k,k,k)
##
##    Phi_hat = np.zeros((N,N,N),complex)
##    CurlyP = 2*pow(10,-9)*pow(1.0,0.9603)
##    Sigma = CurlyP*pow(np.pi,2)*pow(1.0,-3)
##    Phi = random.gauss(0.0,np.sqrt(Sigma))
##
##    Phi_hat[0,0,1] = Phi*1.0
##    Phi_hat[0,0,-1] = Phi*1.0
##    plot.Plot3D(np.abs(Phi_hat),0,k_int,k_int,'kx','ky','Phi_hat','Phi_hat')
##
##    Delta_hat = SetUp.SFS_Delta_growing(Phi_hat,kx,ky,kz,beginningtime,0.0,False)
##    plot.Plot3D(np.abs(Delta_hat),0,k_int,k_int,'kx','ky','Delta_hat','Delta_hat')
##
##    normk = np.sqrt(pow(kx,2)+pow(ky,2)+pow(kz,2))
##    Velocityx_hat = SetUp.SFS_Velocity_growing(Phi_hat,beginningtime,0.0,kx,normk)
##    Velocityy_hat = SetUp.SFS_Velocity_growing(Phi_hat,beginningtime,0.0,ky,normk)
##    Velocityz_hat = SetUp.SFS_Velocity_growing(Phi_hat,beginningtime,0.0,kz,normk)
##    plot.Plot3D(np.abs(Velocityx_hat),0,k_int,k_int,'kx','ky','v_x_hat','v_x_hat')
##    plot.Plot3D(np.abs(Velocityy_hat),0,k_int,k_int,'kx','ky','v_y_hat','v_y_hat')
##    plot.Plot3D(np.abs(Velocityz_hat),0,k_int,k_int,'kx','ky','v_z_hat','v_z_hat')
##
##    All = [Velocityx_hat,Velocityy_hat,Velocityz_hat,Delta_hat]
##    Next = FunctionD(All,kx,ky,kz,beginningtime,0.0,1.0,0.0)
##
##    plot.Plot3D(np.abs(Next[3]),0,k_int,k_int,'kx','ky','Delta_hat','Delta_hat_2')
##    plot.Plot3D(np.abs(Next[0]),0,k_int,k_int,'kx','ky','v_x_hat','v_x_hat_2')
##    plot.Plot3D(np.abs(Next[1]),0,k_int,k_int,'kx','ky','v_y_hat','v_y_hat_2')
##    plot.Plot3D(np.abs(Next[2]),0,k_int,k_int,'kx','ky','v_z_hat','v_z_hat_2')

    N = 50
    h = (1)/(N*1.0)
    x = np.arange(0.0,1,h)

    fy,fz,fx = np.meshgrid(x,x,x)
    Phi = np.cos(2*np.pi*(fy+fx))+np.cos(4*np.pi*fx)
    plot.Plot3D(Phi,0,x,x,'','','','test')
    Phi_hat = np.divide(np.fft.fftn(Phi),N**3)

    k_positive = np.arange(0,N/2+1,1)
    k_negative = np.arange(-N/2+1,0,1)
    k_int = np.concatenate((k_positive,k_negative))
    ky,kz,kx = np.meshgrid(k_int*2*np.pi,k_int*2*np.pi,k_int*2*np.pi)

    Phi_hat_derivative = derivative(kx,Phi_hat)

    Phi_derivative = np.real(np.fft.ifftn(np.multiply(Phi_hat_derivative,N**3)))
    plot.Plot3D(Phi_derivative,0,x,x,'','','','test2')
    Unit_Tester.vaugeTest(Phi_derivative,-2*np.pi*np.sin((fy+fx)*2*np.pi)-4*np.pi*np.sin(4*np.pi*fx),10)


if __name__ == '__main__':
    main()
