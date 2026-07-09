---
title: "High-order gas-kinetic scheme with parallel computation for direct numerical simulation of turbulent flows"
authors: "Guiyu Cao, Liang Pan, Kun Xu"
year: 2020
source: arxiv
source_id: "2005.08736"
url: "http://arxiv.org/abs/2005.08736v1"
domain: scientific-computing
---
High-order gas-kinetic scheme with parallel computation for direct
numerical simulation of turbulent ﬂows
Guiyu Caoa, Liang Panb,∗, Kun Xua,c
aDepartment of Mathematics, Hong Kong University of Science and Technology, Clear Water Bay,
Kowloon, Hong Kong
bSchool of Mathematical Science, Beijing Normal University, Beijing, China
cShenzhen Research Institute, Hong Kong University of Science and Technology, Shenzhen, China
Abstract
The performance of high-order gas-kinetic scheme (HGKS) has been investigated for the
direct numerical simulation (DNS) of isotropic compressible turbulence up to the supersonic
regime [9]. Due to the multi-scale nature and coupled temporal-spatial evolution process,
HGKS provides a valid tool for the numerical simulation of compressible turbulent ﬂow.
Based on the domain decomposition and message passing interface (MPI), a parallel HGKS
code is developed for large-scale computation in this paper. The standard tests from the
nearly incompressible ﬂow to the supersonic one, including Taylor-Green vortex problem,
turbulent channel ﬂow and isotropic compressible turbulence, are presented to validate the
parallel scalability, eﬃciency, accuracy and robustness of parallel implementation.
The
performance of HGKS for the nearly incompressible turbulence is comparable with the high-
order ﬁnite diﬀerence scheme, including the resolution of ﬂow structure and eﬃciency of
computation. Based on the accuracy of the numerical solution, the numerical dissipation
of the scheme in the turbulence simulation is quantitatively evaluated. As a mesoscopic
method, HGKS performs better than both lattice Boltzmann method (LBM) and discrete
uniﬁed gas-kinetic scheme (DUGKS), due to its high-order accuracy. Meanwhile, based on
the kinetic formulation HGKS shows advantage for supersonic turbulent ﬂow simulation
with its accuracy and robustness. The current work demonstrates the capability of HGKS
as a powerful DNS tool from the low speed to supersonic turbulence study, which is less
reported under the framework of ﬁnite volume scheme.
Keywords:
High-order gas-kinetic scheme, direct numerical simulation of turbulence,
parallel computation.
1. Introduction
Turbulence is ubiquitous in natural phenomena and engineering ﬂuid applications [1, 2].
The understanding and prediction of multiscale turbulent ﬂow is one of the most diﬃcult
∗Corresponding author
Email addresses: gcaoaa@connect.ust.hk (Guiyu Cao), panliang@bnu.edu.cn (Liang Pan),
makxu@ust.hk (Kun Xu)
Preprint submitted to Elsevier
May 19, 2020
arXiv:2005.08736v1  [physics.comp-ph]  15 May 2020

problems in both mathematics and physical sciences. Direct numerical simulation (DNS)
solves the Navier-Stokes equations directly, resolve all scales of the turbulent motion (above
Kolmogorov scale), and eliminate modeling entirely [3, 5]. With the advances of numerical
methods and super computers, great success has been achieved by DNS to accurately com-
pute the unsteady turbulent ﬂow, such as DNS of turbulent channel ﬂow up to Reτ ≈5200
[4]. For the incompressible turbulence simulation, the spectral and pseudo-spectral method
[5, 6], and lattice Boltzmann method (LBM) [7, 8] have been established and validated suc-
cessfully. However, for the compressible ﬂow simulation with with discontinuous shocks [9],
both of them fail to capture shocklets and suﬀer from numerical instability. For the com-
pressible turbulence ﬂow [10, 11], the high-order ﬁnite diﬀerence WENO scheme [12, 13, 14]
and the high-order compact method [15] have been widely utilized. Aiming at capturing
shocklets robustly and resolving smooth region accurately, the hybrid scheme combining the
compact scheme and WENO scheme has been developed [16]. However, due to the numeri-
cal instability when encountering strong shocklets, the highest turbulent Mach number for
hybrid scheme is still limited and critical threshold of simulating supersonic ﬂow remains.
Although the second-order ﬁnite volume scheme is the main workhorse in practical engineer-
ing applications, the DNS is reported rarely within the ﬁnite volume framework due to its
over-dissipative nature [17]. Because of the advantage of the ﬁnite volume formulation, such
as the excellent conservative properties and favorable ability in capturing discontinuities, it
is reasonable to develop high-order ﬁnite volume scheme for direct simulation of turbulent
ﬂow in all ﬂow regimes from subsonic to supersonic ones.
In the past decades, the gas-kinetic scheme (GKS) has been developed systematically
based on the Bhatnagar-Gross-Krook (BGK) model [18, 19] under the ﬁnite volume frame-
work, and applied successfully for the computations from low speed ﬂow to hypersonic one
[20, 21]. Diﬀerent from the classical methods with Riemann solvers [22], the gas-kinetic
scheme presents a gas evolution process from kinetic scale to hydrodynamic scale, where
both inviscid and viscous ﬂuxes are recovered from a time-dependent and genuinely multi-
dimensional gas distribution function at a cell interface. In discontinuous shock region, the
kinetic scale particle transport physics takes eﬀect to construct a crisp and stable shock
transition. In smooth ﬂow region, the accurate Navier-Stokes solution can be obtained once
the ﬂow structure is well resolved. Starting from a time-dependent ﬂux function, based on
the two-stage fourth-order formulation [23, 24], a high-order gas-kinetic scheme has been
constructed and applied for the compressible ﬂow simulation [25, 26, 27]. The fourth-order
and even higher-order can be achieved in GKS with the implementation of the traditional
second-order or third-order GKS evolution model. More importantly, the high-order GKS
is as robust as the second-order scheme and works perfectly from the subsonic to hypersonic
viscous heat conducting ﬂows [28]. In recent years, the gas-kinetic scheme has been applied
in the turbulent ﬂow simulation successfully as well. For high-Reynolds number turbulent
ﬂow, the gas-kinetic scheme coupled with traditional eddy viscosity turbulence model has
been developed and implemented in turbulent ﬂow study [29, 30, 31].
Recently, with the implementation of two-stage temporal discretization and WENO re-
construction, high-order gas-kinetic scheme (HGKS) in three dimensional space has been
successfully developed in the DNS for isotropic compressible turbulence [9], which is the
2

ﬁrst attempt by gas-kinetic scheme to the DNS study. The isotropic compressible turbu-
lence with high turbulent Mach number up to supersonic regime has been studied, which
veriﬁes the validity of HGKS for compressible turbulence study, especially in the high speed
regime. In order to resolve the small-scale ﬂow structure and present the results at high
Reynolds number, the development of a parallel HGKS is necessary. Here, the domain de-
composition and message passing interface (MPI) [32] will be implemented in HGKS. Then,
the classical turbulent tests from nearly incompressible ﬂow to the hypersonic one, includ-
ing Taylor-Green vortex, turbulent channel ﬂow, and isotropic compressible turbulence, are
used to validate the parallel scalability, eﬃciency, accuracy, and robustness of HGKS. The
performance of HGKS is compared with the classical methods, including the popular high-
order ﬁnite diﬀerence scheme [33], lattice Boltzmann method (LBM), and discrete uniﬁed
gas-kinetic scheme (DUGKS) [34]. For the nearly incompressible ﬂows, the performance
of HGKS is comparable with the ﬁnite diﬀerence scheme, including the resolution and ef-
ﬁciency of computation. As a mesoscopic method, HGKS performs better than both LBM
and DUGKS. Meanwhile, HGKS shows advantage for supersonic turbulence study due to
its accuracy and robustness. For the isotropic compressible turbulence, the cases with high
turbulent Mach number can be simulated without any special treatment. The current study
provides us conﬁdence on the further investigation of compressible turbulence, such as shock-
boundary interaction and supersonic turbulent boundary layer transition.
This paper is organized as follows. In Section 2, the high-order gas-kinetic scheme and
the strategy of parallelization are introduced. Section 3 includes numerical simulation and
discussions. The last section is the conclusion.
2. High-order GKS and parallel implementation
2.1. High-order GKS
The three-dimensional BGK equation [18, 19] can be written as
ft + ufx + vfy + wfz = g −f
τ
,
(1)
where u = (u, v, w) is the particle velocity, f is the gas distribution function, g is the three-
dimensional Maxwellian distribution and τ is the collision time. The collision term satisﬁes
the compatibility condition
Z g −f
τ
ψdΞ = 0,
(2)
where ψ = (1, u, v, w, 1
2(u2 + v2 + w2 + ξ2))T, ξ2 = ξ2
1 + ... + ξ2
N, dΞ = dudvdwdξ1dξN, γ is
the speciﬁc heat ratio and N = (5 −3γ)/(γ −1) is the internal degree of freedom.
Taking moments of the BGK equation Eq.(1) and integrating with respect to space, the
ﬁnite volume scheme can be expressed as
d(Qijk)
dt
= L(Qijk),
(3)
3

where the operator L is deﬁned as
L(Qijk) = −
1
|Ωijk|
6
X
p=1
Fp(t),
(4)
where Ωijk = xi ×yj ×zk with xi = [xi −∆x/2, xi +∆x/2], yj = [yj −∆y/2, yj +∆y/2], zk =
[zk −∆z/2, zk +∆z/2], Fp(t) is the numerical ﬂux across the cell interface Σp. The numerical
ﬂux in x-direction is given as example
Fp(t) =
ZZ
Σp
F(Q) · ndσ =
2
X
m,n=1
ωmn
Z
ψuf(xi+1/2,jm,kn, t, u, ξ)dΞ∆y∆z,
where n is the outer normal direction. In this paper, the orthogonal Cartesian mesh is con-
sidered, the normal direction is constant for each cell interface. The Gaussian quadrature is
used over the cell interface, where ωmn is the quadrature weight, xi+1/2,m,n = (xi+1/2, yjm, zkn)
and (yjm, zkn) is the Gauss quadrature point of cell interface yj × zk. The gas distribution
function f(xi+1/2,jm,kn, t, u, ξ) in the local coordinate can be given by the integral solution
of BGK equation Eq.(1) as follows
f(xi+1/2,jm,kn, t, u, ξ) = 1
τ
Z t
0
g(x′, t′, u, ς)e−(t−t′)/τdt′ + e−t/τf0(−ut, ξ),
where u = (u, v, w) is the particle velocity, x′ = xi+1/2,jm,kn −u(t −t′) is the trajectory of
particles, f0 is the initial gas distribution function, and g is the corresponding equilibrium
state. With the ﬁrst order spatial derivatives, the second-order gas distribution function at
cell interface can be expressed as
f(xi+1/2,jm,kn, t, u, ξ) =(1 −e−t/τ)g0 + ((t + τ)e−t/τ −τ)(a1u + a2v + a3w)g0
+(t −τ + τe−t/τ) ¯Ag0
+e−t/τgr[1 −(τ + t)(ar
1u + ar
2v + ar
3w) −τAr)]H(u)
+e−t/τgl[1 −(τ + t)(al
1u + al
2v + al
3w) −τAl)](1 −H(u)),
(5)
where the equilibrium state g0 and the corresponding conservative variables Q0 can be
determined by the compatibility condition
Z
ψg0dΞ = Q0 =
Z
u>0
ψgldΞ +
Z
u<0
ψgrdΞ.
With the reconstruction of macroscopic variables, the coeﬃcients in Eq.(5) can be fully
4

determined by the reconstructed derivatives and compatibility condition
⟨ak
1⟩= ∂Qk
∂x , ⟨ak
2⟩= ∂Qk
∂y , ⟨ak
3⟩= ∂Qk
∂z , ⟨ak
1u + ak
2v + ak
3w + Ak⟩= 0,
⟨a1⟩= ∂Q0
∂x , ⟨a2⟩= ∂Q0
∂y , ⟨a3⟩= ∂Q0
∂z , ⟨a1u + a2v + a3w + A⟩= 0,
where k = l, r and ⟨...⟩are the moments of the equilibrium g and deﬁned by
⟨...⟩=
Z
g(...)ψdΞ.
More details of the gas-kinetic scheme can be found in the literatures [20, 21, 35]. Thus,
the gas distribution function is determined, and the numerical ﬂux can be obtained by
taking moments of it. For the high-order spatial accuracy, the ﬁfth-order WENO method
[13, 14] is adopted. For the three-dimensional computation, the dimension-by-dimension
reconstruction is used. More details about spatial reconstruction can be found in previous
work [25, 9], and several remarks are given.
Remark 1. For the low speed ﬂows, such as Taylor-Green vortex problem and turbulent
channel ﬂow, the ﬂow ﬁelds are smooth without strong shocklets, the simpliﬁed smooth
second-order gas-kinetic ﬂux [27] and WENO scheme with linear weights are used to avoid
the numerical dissipation from artiﬁcially created interface discontinuity. For the tangential
reconstruction Ql,r and Q0, the fourth-order polynomials are constructed at the horizontal
and vertical direction. The variables and spatial derivatives can be constructed at the Gaus-
sian quadrature points. For the compressible isotropic turbulence from subsonic to supersonic
regime, the WENO-Z [14] scheme is used. In order to eliminate the spurious oscillation and
improve the stability, the reconstruction can be performed for the characteristic variables in
local coordinate for each Gaussian quadrature point. The characteristic variable is deﬁned as
ω = R−1Q, where Q is variable in the local coordinate, and where R is the right eigenmatrix
of Jacobian matrix (∂F/∂Q)G at Gaussian quadrature point. With the reconstructed vari-
able, the conservative variables can be obtained by the inverse projection. For the tangential
reconstruction of Ql,r and Q0, the variables at the ends of cell interface can be obtained from
the ﬁfth-order WENO method at the horizontal and vertical direction. With reconstructed
variables and the cell averaged variables, the quadratic polynomials can be constructed. The
variables and spatial derivatives can be constructed at the Gaussian quadrature points as
well.
Based on the time-dependent ﬂux function of the generalized Riemann problem solver
(GRP) [23, 24] and gas-kinetic scheme, a two-stage fourth-order time-accurate discretization
was developed for Lax-Wendroﬀtype ﬂow solvers [25, 26].
Consider the following time
dependent equation
∂Q
∂t = L(Q),
5

with the initial condition at tn, i.e.,
Q(t = tn) = Qn,
where L is an operator for spatial derivative of ﬂux, the state Qn+1 at tn+1 = tn + ∆t can
be updated with the following formula
Q∗= Qn + 1
2∆tL(Qn) + 1
8∆t2∂tL(Qn),
Qn+1 =Qn + ∆tL(Qn) + 1
6∆t2∂tL(Qn) + 2∂tL(Q∗)

.
(6)
It can be proved that for hyperbolic equations the above temporal discretization provides a
fourth-order time accurate solution for Qn+1. To implement two-stage fourth-order method
for Eq.(3), a linear function is used to approximate the time dependent numerical ﬂux
Fp(t) ≈Fn
p + ∂tFn
p(t −tn).
(7)
Integrating Eq.(7) over [tn, tn + ∆t/2] and [tn, tn + ∆t], we have the following two equations
Fn
p∆t + 1
2∂tFn
p∆t2 =
Z tn+∆t
tn
Fp(t)dt,
1
2Fn
p∆t + 1
8∂tFn
p∆t2 =
Z tn+∆t/2
tn
Fp(t)dt.
The coeﬃcients Fn
p and ∂tFn
p at the initial stage can be determined by solving the linear
system.
According to Eq.(4), L(Qn
i ) and the temporal derivative ∂tL(Qn
i ) at tn can be
constructed by
L(Qn
i ) = −1
|Ωi|
6
X
p=1
Fn
p,
∂tL(Qn
i ) = −1
|Ωi|
6
X
p=1
∂tFn
p.
The ﬂow variables Q∗at the intermediate stage can be updated. Similarly, L(Q∗
i ), ∂tL(Q∗
i )
at the intermediate state can be constructed and Qn+1 can be updated as well.
2.2. Parallel implementation
Due to the explicit formulation of HGKS, a popular parallel strategy is developed, where
two-dimensional domain decomposition is used. As shown in Fig.1, the total number of cells
is Nx×Ny×Nz, and the computational domain is divided into ny parts in y-direction, nz parts
in z-direction and no division is used in x-direction. The processor Pjk, j = 0, , ny −1, k =
0, ..., nz −1 handles a sub-domain with Nx × nyj × nzk cells, where
(
nyj = [Ny/ny] + 1,
j < mod(Ny, ny),
nyj = [Ny/ny],
j ≥mod(Ny, ny),
6

Figure 1:
Schematic for two-dimensional domain decomposition with ny = 4, nz = 3.
and
(
nzk = [Nz/nz] + 1,
k < mod(Nz, nz),
nzk = [Nz/nz],
k ≥mod(Nz, nz).
The data communication is performed between eight neighboring sub-domains, and the
speciﬁc boundary conditions are performed for the boundary processor. The procedure is
the only data communication of the algorithm, which is handled by the MPI libraries [32].
3. Numerical simulation and discussion
In this section, numerical tests from the nearly incompressible ﬂow to the supersonic one
will be presented to validate our numerical scheme. For the smooth ﬂow without disconti-
nuities, the collision time takes
τ = µ
p.
For the ﬂow with discontinuities, we have
τ = µ
p + C|pl −pr
pl + pr
|∆t,
where pl and pr denote the pressure on the left and right sides of the cell interface, µ is the
dynamic viscous coeﬃcient, C = 1 and p is the pressure at the cell interface. The reason
for including artiﬁcial dissipation through the additional term in the particle collision time
is to enlarge the kinetic scale physics in the discontinuous region for the construction of
a numerical shock structure through the particle free transport and inadequate particle
collision in order to keep the non-equilibrium property.
3.1. Taylor-Green vortex
Taylor-Green vortex is a classical problem in ﬂuid dynamics developed to study vortex
dynamics, turbulent transition, turbulent decay and energy dissipation process [36, 37]. It is
7

given by a simple construction, and contains several key physical processes including vortex
stretching, interaction and dilatation eﬀects. Therefore, this case becomes an excellent case
for the evaluation of turbulent ﬂow simulation methodologies, and has been used by many
authors for high-order method validation [33, 38]. The ﬂow is computed within a periodic
square box deﬁned as −πL ≤x, y, z ≤πL. With a uniform temperature, the initial condition
is given by
U =V0 sin( x
L) cos( y
L) cos( z
L),
V = −V0 cos( x
L) sin( y
L) cos( z
L),
W =0,
p =p0 + ρ0V 2
0
16 (cos(2x
L ) + cos(2y
L ))(cos(2z
L ) + 2).
In the computation, L = 1, V0 = 1, ρ0 = 1, and the Mach number takes M0 = V0/c0 = 0.1,
where c0 is the sound speed. The ﬂuid is a perfect gas with γ = 1.4, Prandtl number is
Pr = 0.71, and Reynolds number Re = 1600. The characteristic convective time tc = L/V0.
This problem is aimed at the performance of high-order gas-kinetic scheme on the direct
numerical simulation of nearly incompressible turbulent ﬂows.
In the computation, the
cases TG1, TG2, TG3 and TG4 with 1283, 2563, 5123 and 10243 uniform cells are tested,
and the numerical results of BB13 dispersion relation preserving (DRP) scheme [39] with
5123 cells are given as reference [33]. The BB13 scheme was originally developed for noise
computations, in which a high-order ﬁnite diﬀerence method equipped with fourth-stage
third-order algorithm for time discretization and 13-point stencils for spatial discretization.
The compressible Navier-Stokes equations are solved by both high-order gas-kinetic scheme
and ﬁnite diﬀerence method.
To test the performance of HGKS, several diagnostic quantities are computed from the
ﬂow as it evolves in time. The volume-averaged kinetic energy is given by
Ek =
1
ρ0Ω
Z
Ω
1
2ρU · UdΩ,
where Ωis the volume of the computational domain. The dissipation rate of kinetic energy
can be computed by the temporal derivative of Ek
ε(Ek) = −dEk
dt ,
which is computed by second order central diﬀerence in the numerical results of Ek. For the
incompressible limit, the dissipation rate is related to the integrated enstrophy by
ε(ζ) = 2 µ
ρ0
ζ,
8

t
kinetic energy
0
5
10
15
20
0.2
0.4
0.6
0.8
1
BB13 DRP
HGKS, TG1
HGKS, TG2
HGKS, TG3
HGKS, TG4
Figure 2:
Taylor-Green vortex: time history of kinetic energy Ek.
t
dissipation rate
0
5
10
15
20
0
0.003
0.006
0.009
0.012
0.015
BB13 DRP
HGKS, TG1
HGKS, TG2
HGKS, TG3
HGKS, TG4
t
enstrophy
0
5
10
15
20
0
0.003
0.006
0.009
0.012
0.015
BB13 DRP
HGKS, TG1
HGKS, TG2
HGKS, TG3
HGKS, TG4
Figure 3:
Taylor-Green vortex: time history of dissipation rate ε(Ek) and enstrophy ε(ζ). The reference
data is ε(Ek) with 5123 cells for two contours [33].
where µ is the coeﬃcient of viscosity, ω = ∇× U and
ζ =
1
ρ0Ω
Z
Ω
1
2ρω · ωdΩ.
The time history of kinetic energy is shown in Fig.2, where the reasonable agreement is
observed with the reference solution except for the simulation with 1283 cells. The kinetic
energy dissipation rates ε(Ek) and the enstrophy integral computed ε(ζ) are shown in Fig.3,
respectively. A large discrepancy is observed in the peak dissipation rate for ε(Ek) and
9

Figure 4:
Taylor-Green vortex: iso-surface of the second invariant of velocity gradient tensor Qv = −0.5
at t = 2.5, 5, 10 and 15 colored by velocity magnitude.
ε(ζ) with 1283 cells and 2563 cells, and an excellent agreement with the reference solution
is obtained with the mesh reﬁnement. Especially, the mesh with 10243 cells is the ﬁnest
resolution for the Taylor-Green vortex problem, and a benchmark results have been provided.
As time evolves, the vortex roll-up, stretch and interact, eventually breaking down into
turbulence. The iso-surface of the second invariant of velocity gradient tensor Qv colored
by velocity magnitude at t = 2.5, 5, 10 and 15 with 5123 cells are shown in Fig.4. Velocity
magnitude ranges from 0 to 0.2 and 20 equivalent levels are used. At the earliest time, the
ﬂow behaves inviscidly as the vortex begin to evolve and roll-up. At t = 10, the coherent
10

structures breakdown. Beyond this breakdown, the ﬂow is fully turbulent and the structures
slowly decay until the ﬂow comes to rest. The results indicate that the resolution of HGKS
is comparable even with the higher-order ﬁnite diﬀerence method, which is widely used in
DNS of turbulence.
t
ε1
0
5
10
15
20
0
0.003
0.006
0.009
0.012
0.015
TG1
TG2
TG3
TG4
t
ε2
0
5
10
15
20
-1E-07
0
1E-07
2E-07
3E-07
4E-07
TG1
TG2
TG3
TG4
t
ε3
0
5
10
15
20
0
0.0001
0.0002
0.0003
TG1
TG2
TG3
TG4
t
εnum
0
5
10
15
20
-0.001
0
0.001
0.002
0.003
0.004
0.005
TG1
TG2
TG3
TG4
Figure 5:
Taylor-Green Vortex: the time history of ε1, ε2, ε3 and εnum.
In the numerical simulation, the ﬁnal dissipative behavior is determined by both phys-
ical and numerical dissipation. For the current study, the quantitative study of numerical
dissipation is presented as well, which is less reported in literatures. For the compressible
ﬂow, the kinetic energy dissipation rate obtained from the Navier-Stokes equations is the
11

sum of three contributions, namely,
ε1 =2 µ
ρ0
1
Ω
Z
Ω
Sd : SddΩ,
ε2 =µb
ρ0
1
Ω
Z
Ω
(∇· U)2dΩ,
ε3 = −
1
ρ0Ω
Z
Ω
p∇· UdΩ,
where Sd is the deviatoric part of the strain rate tensor, µb is the bulk viscosity. In current
scheme, the inherent bulk viscosity [20] reads
µb =
2N
3(N + 3)µ,
where N = 2 for the diatonic gas. The contributions to the dissipation rate based on the
compressible ﬂow assumptions are shown in Fig.5. To eliminate the error from numerical
discretization, all spatial derivatives are computed by sixth order central diﬀerence for three
components of dissipation rate. As excepted, the primary contribution ε1 is almost identical
to ε(ζ) in current nearly incompressible simulation, and the bulk viscosity contribution ε2
and dilatation contribution ε3 can be neglected. It is noted that the magnitude of pressure
dilation term ε3 is on the same order as that of the reference solution [33]. With coarse
mesh resolutions, the total dissipation rate computed from ε1 + ε2 + ε3 is signiﬁcantly lower
than ε(Ek). Therefore, the numerical dissipation can be quantitatively computed by
εnum = ε(Ek) −(ε1 + ε2 + ε3).
The time history of numerical dissipation is given in Fig.5 as well. With the reﬁnement
of grid, the resolution of the vortical structures increases and the eﬀect of the ﬁltering de-
creases, which reduces numerical dissipation. The fact that ε(Ek) is well predicted at all grid
levels indicates that the physical and numerical dissipation work together consistently in the
calculation to get the ﬁnal ”physical” result. In other words, the ﬁltering due to the coarse
mesh correctly mimics the physical dissipation from the unresolved scale dynamics. This
validates the usage of high-order numerical methods for the implicit large-eddy simulations
(iLES) [40]. While the iLES for complex turbulent ﬂows is still under debate, the current
quantitative analysis of numerical dissipation gives the speciﬁc hints on this issue.
3.2. Eﬃciency test of parallel computation
In this section, the eﬃciency of parallel computation is tested in the above Taylor-Green
vortex problem. To give the performance of parallel computation, the speedup is deﬁned as
Sn = Tn
Tnref
,
12

where Tn is the execution time with n cores and Tnref is the execution time on a reference
number of processors. The ideal speedup of parallel computations would be equal to n/nref.
With the log-log plot for n and Tn, an ideal scalability would follow −1 slope. However, this
eﬃciency is not possible due the communication delay among the computational cores and
the idle time of computational nodes associated with load balancing. The scalability of our
MPI code is examined by measuring the wall clock time against the number of processors.
The detailed performance of MPI parallel computing is given in Table.1 and a log-log plot is
also given in Fig.6, where 4, 16 and 64 cores for 2563 cells, and 64, 256, and 1024 cores are
used for 5123 cells. Total 30 steps are computed for each case, and CPU time is the averaged
time for each step. The code was run on the TianHe-II, and the node details are presented
in Table.2. Due to the explicit formulation of HGKS, our MPI code scales properly with
the number of processors used. It is indicated that the data communication crossing nodes
costs a little time and the computation for ﬂow ﬁeld is the dominant one.
Grid size
Cores
CPU time (s/step)
Grid size
Cores
CPU time (s/step)
2563
4
121.01
5123
64
69.00
2563
16
34.08
5123
256
17.29
2563
64
9.09
5123
1024
4.66
Table 1:
Eﬃciency test of parallel strategy: detailed CPU time against number of core.
CPU time
cores
10
1
10
2
10
1
10
2
10
3
256
3 cells
512
3 cells
-1 slope
-1
Figure 6:
Eﬃciency test of parallel strategy: log-log plot for n and Tn.
For most DNS, the high-order ﬁnite diﬀerence method is widely used, and the ﬁnite
volume scheme is rarely applied due to the complicated formulation. Because of the proce-
dure of multidimensional spatial reconstruction and quadrature of numerical ﬂuxes at cell
interface, the ﬁnite volume scheme is considered to be less eﬃcient than the ﬁnite diﬀerence
13

System
Node type
Cache
Host channel adapter
TianHe-II
Intel Xeon E5-2692 (2.2GHz/core)
30MB
InﬁniBand
Pleiades
Intel Xeon E5-2670 (2.6GHz/core)
20MB
InﬁniBand
Table 2:
Eﬃciency test of parallel strategy: node details for TianHe-II and Pleiades supercomputer systems.
method. For the high-order gas-kinetic scheme, the gas-kinetic ﬂux solver Eq.(5) considered
to be even more complicated than Riemann solvers [22], which is usually used in the clas-
sical ﬁnite volume scheme. In this case, the comparison of total computational cost with
the ﬁnite diﬀerence method is also given. The time step and total computational costs of
HGKS are presented in Table.3, in which the current HGKS is running on the TianHe-II
supercomputer system. As reference, the eﬃciency of high-order ﬁnite diﬀerence method
[33] is given in Table.4, in which the cases were run on the NASA Pleaides high performance
computing system. The node details are compared in Table.2, and the total computational
costs of HGKS is around 1.4 times higher than the ﬁnite diﬀerence method. In addition,
considering the processor speed, the HGKS is around 1.2 times higher than the ﬁnite dif-
ference method. Taken the robustness of HGKS into account, such computational cost is
comparable and aﬀordable.
Case
Grid size
Time step
Cores
Hours
Computational costs
TG1
1283
1.785 × 10−3
16
13.3
213 core hours
TG2
2563
8.925 × 10−4
256
13.5
3456 core hours
TG3
5123
4.462 × 10−4
1024
66
67584 core hours
TG4
10243
2.789 × 10−4
1024
730
747062 core hours
Table 3:
Eﬃciency test of parallel strategy: detailed computational parameters for HGKS.
Grid size
Time step
Cores
Hours
Computational costs
2563
8.463 × 10−4
64
40
2560 core hours
5123
4.231 × 10−4
368
130
47840 core hours
Table 4:
Eﬃciency test of parallel strategy: detailed computational parameters for BB13 [33].
3.3. Turbulent channel ﬂow
Considering the simplicity of geometry and boundary conditions, the turbulent channel
ﬂows have been studied to understand the mechanism of wall-bounded turbulent ﬂows. A
large number of computational studies of turbulent channel ﬂows have been carried out
[3, 42, 4]. In the current study, the turbulent channel ﬂow with friction Reynolds number
Reτ = 180 is tested. In the computation, the physical domain is (x, y, z) ∈[0, 2π]×[−1, 1]×
[0, π] and the computational domain takes (ξ, η, ζ) ∈[0, 2π]×[0, 3π]×[0, π]. The coordinate
14

transformation is given by







x = ξ,
y = tanh(bg( η
1.5π −1))/ tanh(bg),
z = ζ,
where bg = 2. The periodic boundary conditions are used in streamwise x-direction and
spanwise z-directions, and the non-slip and isothermal boundary conditions are used in
vertical y-direction. The ﬂuid is initiated with ρ = 1, Ma = 0.1 and the initial streamwise
velocity proﬁle is given by the perturbed Poiseuille ﬂow proﬁle
U(y) = 1.5(1 −y2) + white noise.
White noise is added with 10% amplitude of local streamwise velocity.
With the unit
averaged streamwise velocity, the initial pressure can be given. The friction Reynolds number
is deﬁned as
Reτ = ρuτH/µ,
where H = 1 is the half height of the channel and the frictional velocity uτ is given by
uτ =
rτwall
ρ , τwall = ∂U
∂y

wall.
For the channel ﬂow, the logarithmic formulation is given by
U + = 1
κ ln Y + + B,
(8)
where von Karman constant κ = 0.40 and B = 5.5 for the low Reynolds number turbulent
channel ﬂow [3]. The plus unit and plus velocity are deﬁned as
Y + = ρuτy/µ, U + = U/uτ.
Therefore, the plus velocity U +
c = 18.4823 at center line of the channel according to Eq.(8),
where Y +
c
= 180 at center line. The frictional velocity is determined by uτ = Uc/U +
c
=
0.0541, where Uc = 1 is the centreline line velocity. In this computation, the cases G1 and
G2 are tested, where 963 and 1283 cells are distributed uniformly in computational space.
256 cores and 1024 cores are used to simulate the G1 and G2, respectively. The details of
mesh are given in Table.5, where ∆y+
min and ∆y+
max are the minimum and maximum grid
space in the y-direction. To resolve the viscous layer, there are 11 layers for G1 and 15 layers
for G2 within Y + less than 10, respectively. As reference, the mesh and initial streamwise
velocity in the physical domain for G1 are given in Fig.7.
To excite channel ﬂow from laminar to turbulence, an external force is exerted in the
15

Case
Grid size
∆y+
min/∆y+
max
∆x+
∆z+
G1
963
0.29/7.77
11.77
5.89
G2
1283
0.21/5.83
8.83
4.42
Table 5:
Turbulent channel ﬂow: diﬀerent sets of grids for Reτ = 180 turbulent channel ﬂow.
Figure 7:
Turbulent channel ﬂow: the mesh and initial streamwise velocity distributions for case G2.
streamwise direction. According to the viscous layer U + = Y +, a ﬁxed nondimensional
external force can be approximated by balance of forces
fx = τwall/H = 2.93 × 10−3.
Before transition, the external force fx·∆t and 10fx·∆t are used for G1 and G2, respectively.
∆t is the time step. After transition, the constant moment ﬂux is used to determine the
external force. According to the experiment and previous work [3, 34], the constant bulk
volume is recommended to be set as
ZZZ
Ω
(ρU)n+1
ijk dΩ=
ZZZ
Ω
(ρUb)dΩ,
where Uc/Ub = 1.16 is chosen based on previous DNS [3]. The conservative variables updated
by the two-stage method Eq.(6) are denoted as eQn+1 and the conservative variables with
external force is Qn+1. With the external force, the equation for momentum in streamwise
direction and energy can be written as
∂ρU
∂t
= LρU + ρfx,
∂ρE
∂t
= LρE + ρUfx,
where LρU, LρE are the operator for spatial derivative of momentum and energy ﬂuxes and
16

fx is the external force, which can be given as follows
fx = 1
∆t ·
ZZZ
Ω
(ρU)n+1
ijk dΩ−
ZZZ
Ω
(f
ρU)n+1
ijk dΩ
1
2
ZZZ
Ω
(ρn
ijk + eρn+1
ijk )dΩ
.
and the equation for momentum in streamwise direction and energy can be updated
(ρU)n+1
ijk = (f
ρU)n+1
ijk + 1
2∆t(ρn+1
ijk + ρn
ijk)fx,
(ρE)n+1
ijk = (f
ρE)n+1
ijk + 1
2∆t((ρU)n+1
ijk + (ρU)n
ijk)fx.
Therefore, the momentum ﬂux over the whole domain keeps constant in the computation.
The external force before the transition and after transition with grid G1 and G2 are pre-
sented in Fig.8. After over 500 characteristic periodic time as 500H/Uc, it can be seen that
the initial laminar ﬂow-ﬁelds transit to turbulence. Then, the external force based on the
constant moment ﬂux are used. The total stress is used to test whether the simulated tur-
bulence is statistically stationary [1, 4]. In a statistically stationary turbulent channel, the
total stress, which is the sum of Reynolds stress and mean viscous stress, is linear because
of momentum conservation
dU +
dY + −⟨UV ⟩+ ≈1 −Y +
Reτ
.
When the residual of total stress converging, the 350 periodic time as 350H/Uc is used,
which is comparable to that in the reference paper [41, 42]. As shown in Fig.9, the residual
is less than 2.6% for case G1 and 1.2% for case G2.
Case
Reτ
Rec
Reb
Cf
G1
176.03
3297.78
5720.09
7.58 × 10−3
G2
179.21
3319.22
5730.11
7.82 × 10−3
Table 6:
Turbulent channel ﬂow: mean ﬂow variables for case G1 and G2.
The mean ﬂow variables with diﬀerent sets of grids are presented in Table.6. Reτ is
the averaged friction Reynolds number, Uc is the averaged mean centerline velocity, Ub is
the averaged mean bulk velocity. Rec = UcH/ν, Reb = Ub2H/ν, Cf = τwall/(ρU 2
b /2), and
Cf is the skin friction coeﬃcients. The result on G2 is much closer with Dean’s suggested
correlation of Cf = 0.073Re−0.25
b
= 8.39 × 10−3 [43]. The averaged velocity proﬁles with
grid G1 and G2 are presented in Fig.10. The ﬁrst DNS of fully developed incompressible
turbulent channel ﬂow was performed by the spectral method with 129 × 192 × 160 grids
[3]. As the most popular mesoscopic methods for simulating nearly incompressible ﬂows,
the numerical results of the LBM with 200 × 400 × 200 grids and DUGKS with 1283 grids
17

Figure 8:
Turbulent channel ﬂow: time evolution of the external force for case G1 and G2.
Y
+
Residual
0
50
100
150
-0.03
-0.02
-0.01
0
0.01
0.02
G1
G2
Figure 9:
Turbulent channel ﬂow: distribution of stress residual for case G1 and G2.
are also presented [34], in which the physical accuracy has been demonstrated by comparing
with the Navier-Stokes based spectral methods. The mean ﬂow velocity with a log-linear
plot and a local enlargement are given in Fig.10, where the HGKS result is in reasonable
agreement with the spectral results, LBM and DUGKS results.
The averaged Reynolds shear stress proﬁles are shown in Fig.11 in linear-linear and
log-linear plots.
The sum of Reynolds stress and viscous stress varies linearly from the
channel center to the channel wall. When compared to the spectral result, HGKS results are
clearly better than DUGKS and LBM results, especially in the near-wall region. Turbulence
intensities, i.e., the root-mean-square (rms) velocity proﬁles are shown in Fig.12 as well.
In the near-wall regions, the streamwise rms velocity is the largest and the spanwise rms
velocity is the smallest. DUGKS yields a better result for U +
rms in the near-wall region.
18

Y
+
U
+
10
0
10
1
10
2
0
4
8
12
16
20
24
U
+ = 2.5 In Y
+ + 5.5
U
+ = Y
+
Spectral
LBM
DUGKS
HGKS, G1
HGKS, G2
Y
+
U
+
50
100
150 200
4
8
12
16
20
24
U
+ = 2.5 In Y
+ + 5.5
U
+ = Y
+
Spectral
LBM
DUGKS
HGKS, G1
HGKS, G2
Figure 10:
Turbulent channel ﬂow: mean ﬂow velocity proﬁles and the local enlargement.
Y/(2H)
<-UV>
+
0
0.1
0.2
0.3
0.4
0.5
0
0.2
0.4
0.6
0.8
1
Spectral
LBM
DUGKS
HGKS, G1
HGKS, G2
Y/(2H)
<-UV>
+
10
-3
10
-2
10
-1
0
0.2
0.4
0.6
0.8
1
Spectral
LBM
DUGKS
HGKS, G1
HGKS, G2
Figure 11:
Turbulent channel ﬂow: Reynolds stress proﬁles in linear-linear and log-linear plots.
Meanwhile, for V +
rms and W +
rms, LBM behaves better in the near-center line region, and
DUGKS behaves better in the near-wall region. Considering the good agreement in near-
wall region and the near-center line region with the spectral benchmark, it is clear that HGKS
outweighs LBM and DUGKS. The relative error in DUGKS is due only to the numerical
truncation error, while the relative error in LBM is due to both the domain size eﬀect
and numerical truncation error [34]. Diﬀerent distribution of grid points in the spanwise
direction and diﬀerent grid resolutions should be tested, which could be a topic of HGKS
for turbulent channel ﬂows. Finally, the limiting wall behavior of the Reynolds stresses
is shown in Table.7, where A1 = U +
rms/Y +, B1 = V +
rms/Y +2 × 102, C1 = W +
rms/Y + and
D1 = ⟨−UV ⟩+ /Y +3 × 103.
The y behavior of tangential stresses U +
rms and W +
rms and
19

Y/(2H)
Urms
+
0
0.1
0.2
0.3
0.4
0.5
0
0.5
1
1.5
2
2.5
3
Spectral
LBM
DUGKS
HGKS, G1
HGKS, G2
Y/(2H)
Urms
+
10
-3
10
-2
10
-1
0
0.5
1
1.5
2
2.5
3
Spectral
LBM
DUGKS
HGKS, G1
HGKS, G2
Y/(2H)
Vrms
+
0
0.1
0.2
0.3
0.4
0.5
0
0.2
0.4
0.6
0.8
1
Spectral
LBM
DUGKS
HGKS, G1
HGKS, G2
Y/(2H)
Vrms
+
10
-3
10
-2
10
-1
0
0.2
0.4
0.6
0.8
1
Spectral
LBM
DUGKS
HGKS, G1
HGKS, G2
Y/(2H)
Wrms
+
0
0.2
0.4
0
0.2
0.4
0.6
0.8
1
1.2
Spectral
LBM
DUGKS
HGKS, G1
HGKS, G2
Y/(2H)
Wrms
+
10
-3
10
-2
10
-1
0
0.2
0.4
0.6
0.8
1
1.2
Spectral
LBM
DUGKS
HGKS, G1
HGKS, G2
Figure 12:
Turbulent channel ﬂow: root-mean-square ﬂuctuation velocity proﬁles in linear-linear and
log-linear plots.
20

the y2 behavior of normal stress V +
rms are expected from consideration of no-slip boundary
conditions and continuity equation. Reynolds shear stress ⟨−UV ⟩+ is in the asymptotic
behavior of y3, which is regarded as the benchmark to calibrate the asymptotic near-wall
behavior of eddy-viscosity turbulence models [44]. Currently, the magnitudes of A1, B1, C1
and D1 are in good agreement with the results with spectral method [3].
Y +
A1
B1
C1
D1
0.2124
0.3579
0.8891
0.1839
0.7827
0.6505
0.3624
0.7207
0.1762
0.7046
1.1157
0.3628
0.6568
0.1678
0.7015
1.6096
0.3624
0.6117
0.1594
0.7065
2.1338
0.3614
0.5716
0.1512
0.7088
2.6902
0.3595
0.5343
0.1432
0.7055
3.2807
0.3564
0.4990
0.1353
0.6947
4.5715
0.3518
0.4656
0.1278
0.6756
5.2761
0.3453
0.4339
0.1205
0.6479
Table 7:
Turbulent channel ﬂow: near-wall behavior of Reynolds stresses for case G1.
In summary, the ﬁrst simulation of turbulent channel ﬂow using HGKS shows that the
results are reasonably accurate, and performance is better than the second-order LBM and
DUGKS. More importantly, the HGKS results are obtained with a coarse grid resolution
covering a large domain size compared with LBM. As the equidistant grids are required for
LBM, the grids displacement is limited to an extreme small value to resolve the viscous layer,
i.e., ∆x+ ≈0.3 in the whole computational domain, so the required grids number of LBM will
exceed HGKS dramatically. In the current computation, the spatial reconstruction is based
on the WENO reconstruction on uniform meshes due to the small variation of neighboring
cells, and the order of accuracy may be aﬀected slightly. Currently, we are working on the
genuinely high-order gas-kinetic scheme on the nonuniform and curvilinear meshes, and the
geometrical errors can be excluded in the future simulations.
3.4. Isotropic compressible turbulence
The isotropic compressible turbulence is regarded as one of cornerstones to elucidate
the eﬀects of compressibility for turbulence [10, 45]. Based on the numerical experiments
and theoretical analysis, the isotropic compressible turbulence is divided into four main
dynamical regimes, i.e. the low-Mach number quasi-isentropic regime, the low-Mach number
thermal regime, the nonlinear subsonic regime, and the supersonic regime [11]. High-order
compact ﬁnite diﬀerence method [15] has been widely utilized in the simulation of isotropic
compressible turbulence with moderate turbulent Mach number, i.e. Mat ≤0.8. However,
when simulating the turbulent in supersonic regime, the compact scheme fails to capture
strong shocklets and suﬀers from numerical instability.
In this case, we concentrate on
the decaying isotropic compressible turbulence without external force. The ﬂow domain of
numerical simulation is a cube box 0 ≤x, y, z ≤2π, with periodic boundary conditions in
21

all three Cartesian directions for all ﬂow variables. A three-dimensional solenoidal random
initial velocity ﬁeld U is generated by a speciﬁed spectrum [46]
E(κ) = A0κ4 exp(−2κ2/κ2
0),
(9)
where A0 is a constant to get a speciﬁed initial kinetic energy, κ is the wave number, κ0 is
the wave number at which the spectrum peaks. In this paper, ﬁxed A0 and κ0 in Eq.(9) are
chosen for all cases, which are initialized by A0 = 0.00013 and κ0 = 8. Evolution of this
artiﬁcial system is determined by initial thermodynamic quantities and two dimensionless
parameters, i.e. the initial Taylor microscale Reynolds number and turbulent Mach number
Reλ = (2π)1/4
4
ρ0
µ0
p
2A0κ3/2
0 ,
Mat =
√
3
√γRT0
urms,
where the initial density ρ0 = 1 and Urms is the root mean square of initial velocity ﬁeld
Urms =
U · U
3
1/2
.
With Reλ, Mat and γ = 1.4, the initial viscosity µ0, pressure p0 and temperature T0 can be
determined. The dynamic velocity can be also given by
µ = µ0( T
T0
)0.76.
With current initial strategy, the initial ensemble turbulent kinetic energy K0, ensemble
enstrophy Ω0, ensemble dissipation rate ε0, large-eddy-turnover time τto, Kolmogorov length
scale η0, and the Kolmogorov time scale τ0 are given as
K0 =3A0
64
√
2πκ5
0, Ω0 = 15A0
256
√
2πκ7
0, τto =
r
32
A0
(2π)1/4κ−7/2
0
,
ε0 = 2µ0
ρ0
Ω0, η0 = (ν3
0/ε0)1/4, τ0 = (ν0/ε0)1/2.
(10)
For the compressible isotropic turbulence, starting from the initial ﬂows, the large eddies
transfer their turbulent kinetic energy successively to smaller eddies. The time history of
the root-mean-square density ﬂuctuation ρrms(t), turbulent kinetic energy K(t), skewness
22

factor Su(t) and ﬂatness factor Fu(t) for velocity slope are deﬁned as
ρrms(t) =
p
⟨(ρ −ρ)2⟩,
K(t) = 1
2 ⟨ρU · U⟩,
Su(t) =
X
i
⟨(∂iUi)3⟩
⟨(∂iUi)2⟩3/2,
Fu(t) =
X
i
⟨(∂iUi)4⟩
⟨(∂iUi)2⟩2.
In this process, the evolution of turbulent kinetic energy is of interest since it is a fundamental
benchmark for incompressible and compressible turbulence modeling [47, 2]. The decay of
the ensemble turbulent kinetic energy can be described approximately by [10]
d ⟨K⟩
dt
= ε + ⟨pθ⟩,
ε = εs+εd,
(11)
where εs = ⟨µωiωi⟩is the ensemble solenoidal dissipation rate, εd = 4/3

µθ2
is the ensemble
dilational dissipation rate, ⟨pθ⟩is the ensemble pressure-dilation transfer, ωi = ϵijk∂Uk/∂xj
is the ﬂuctuating vorticity, ϵijk is the alternating tensor and θ = ∇· U is the ﬂuctuating
divergence of velocity.
Case
Mat
dtini/τto
κmaxη0
∆/η0
∆/λ0
R1
0.8
1.04/1000
3.613
0.819
2.551
R2
1.0
1.09/1000
3.613
0.819
2.041
R3
1.2
1.14/1000
3.613
0.819
1.700
R4
1.6
1.19/1000
3.613
0.819
1.275
Table 8:
Isotropic compressible turbulence: parameters for diﬀerent high turbulent Mach number.
Due to the robustness of current scheme, we can simulate this case up to the supersonic
regime, which is seldom reported in literatures. The WENO-Z scheme [14] used for the
spatial reconstruction, no extra special treatment is needed in the code. In this case, the
numerical tests R1, R2, R3 and R4 are presented with a ﬁxed Taylor micro-scale Reynolds
number Reλ = 72 to and the turbulent Mach number form Mat = 0.8 to Mat = 1.6. In
the computation, 256 cores are used for 5123 uniform cells, and more parameters are given
in Table.8, where λ0 is the initial mean free path approximated by µ0 = 1/3ρ0c0λ0 [35], ∆
is the uniform grid size in each direction, η0 is the initial Kolmogorov length scale as in
Eq.(10), κmax =
√
2κ0N/3 is the maximum resolved number wave number, κ0 = 8 as Eq.(9)
and N is the number of grid points in each Cartesian direction. The numerical tests show
that the minimum spatial resolution parameter κmaxη0 ≥2.71 and the maximum temporal
resolution parameter ∆tini/τto ≤5.58/1000 for HGKS is adequate for resolving the isotropic
23

t/τto
ρrms/Mat0
2
0
1
2
3
4
5
0
0.1
0.2
0.3
0.4
R1
R2
R3
R4
t/τto
K/K0
10
-2
10
-1
10
0
0.2
0.4
0.6
0.8
1
R1
R2
R3
R4
t/τto
Skewness
0
1
2
3
4
5
-2.5
-2
-1.5
-1
-0.5
0
R1
R2
R3
R4
t/τto
Flatness
0
1
2
3
4
5
0
3
6
9
12
15
18
21
R1
R2
R3
R4
Figure 13:
Isotropic compressible turbulence: time history of ρrms/Ma2
t, K/K0, Su, and Fu for cases
R1-R4.
compressible turbulence [9]. According to Table.8, the Kolmogorov length scale is still larger
than the mean free path, and each grid always contains more than one mean free path. This
provides the intuitive evidence for controversial issue that smallest eddies in turbulence may
still within the framework of continuum mechanics assumption.
Statistical quantities are provided for these cases, which provide benchmark solutions for
supersonic isotropic compressible turbulence. Time history of ρrms(t)/Ma2
t, K(t)/K0, Su(t)
and Fu(t) are presented in Fig.14, which provides benchmark data for simulating isotropic
compressible turbulence up to supersonic regime. The normalized root-mean-square density
ρrms/Ma2
t decreases monotonically with the increase of initial turbulent Mach number. With
the increase of turbulent Mach number, the peak of skewness and ﬂatness factor deviate from
those of the low-Mach number thermal regime (Mat ≤0.3) severely. These large deviation
24

t/τto
ε
10
-2
10
-1
10
0
0.1
0.2
0.3
0.4
R1
R2
R3
R4
t/τto
εs
0
1
2
3
4
5
0
0.1
0.2
R1
R2
R3
R4
t/τto
εd
0
1
2
3
4
5
0
0.1
R1
R2
R3
R4
t/τto
<pθ>
0
1
2
3
4
5
-0.5
-0.4
-0.3
-0.2
-0.1
0
0.1
R1
R2
R3
R4
Figure 14:
Isotropic compressible turbulence: time history of ε, εs, εd and ⟨pθ⟩for cases R1-R4.
indicates the most signiﬁcant ﬂow structures of isotropic compressible turbulence resulting
from the shocklets. As the initial turbulent Mach number increases, the peak of dissipation
increases as well.
Obviously, ensemble solenoidal dissipation rate εs decreases with the
increase of Mat, while the dilational dissipation rate εd rises with the increase of Mat. In
addition, ⟨pθ⟩changes signs during the evolution and preserves small but positive value
thereafter, which agree with earlier study for subsonic isotropic turbulence [10]. During the
early stage of the decaying supersonic isotropic turbulence, the ensemble pressure-dilation
term can be in the same order of ensemble total dissipation rate. It is reported that the
ratio between the ensemble pressure-dilation term and the right hand side of Eq.(11) becomes
small for solenoidal forced quasi-stationary supersonic isotropic turbulence [48].
To investigate the behavior of supersonic isotropic compressible turbulence, the contours
of normalized dilation θ/ ⟨θ⟩∗on x = 0/y = 0/z = 0 slices are presented in Fig.15 for
25

Figure 15:
Isotropic compressible turbulence: contours of normalized dilation θ/ ⟨θ⟩∗for cases R1-R2 at
t/τto = 1.0, and cases R3-R4 at t/τto = 2.0.
four cases, where ⟨θ⟩∗is root-mean-square dilation. Contours of normalized dilation show
very diﬀerent behavior between the compression motion and expansion motion.
Strong
compression regions θ/ ⟨θ⟩∗≤−3 are usually recognized as shocklets [45]. In current study,
shocklets behave in the shape of narrow and long ribbon, while high expansion regions
θ/ ⟨θ⟩∗≥2 are in the type of localized block.
In addition, strong compression regions
are close to several regions of high expansion. This behavior is consistent with the physical
intuitive that expansion regions can be identiﬁed just downstream of shock waves [49]. These
random distributed shocklets and high expansion region lead to strong spatial gradient in
ﬂow ﬁelds, which pose much greater challenge for high-order schemes when implementing
DNS for isotropic turbulence in supersonic regime. Numerically, few methods survive from
such tough cases. The isotropic compressible turbulence with high turbulent Mach number
26

up to supersonic regime has been studied, which veriﬁes that HGKS provides a valid tool
for numerical and physical studies of compressible turbulence in supersonic regime. More
challenging compressible turbulence problems will be investigated in the future, such as
shock-boundary interaction and supersonic turbulent boundary layer.
4. Conclusion
Based on the multi-scale physical transport and the coupled temporal-spatial gas evolu-
tion, the HGKS provides a useful tool for the numerical study of compressible turbulent ﬂow.
The performance of HGKS has been fully investigated for the DNS of isotropic compress-
ible turbulence up to the supersonic regime. In order to increase the scale of computation,
a parallel code of HGKS has been constructed with domain decomposition and MPI im-
plementation. The resulting scheme is tested for Taylor-Green vortex problem, turbulent
channel ﬂow and isotropic compressible turbulence. It is the ﬁrst successful DNS application
of HGKS for turbulent ﬂow from nearly incompressible to supersonic one. The scalability of
parallel computation is validated, and the computational cost is comparable with the high-
order ﬁnite diﬀerence method. For the nearly incompressible turbulent ﬂow, the performance
of HGKS is also comparable with the ﬁnite diﬀerence method. Based on the accuracy of the
numerical solution, the numerical dissipation of the scheme in the turbulence simulation is
quantitatively evaluated. As a mesoscopic method, the HGKS performs better than both
LBM and DUGKS. More importantly, HGKS shows special advantages for the supersonic
turbulence due to the accuracy and robustness. More challenging examples using HGKS at
higher Reynolds numbers and diﬀerent ﬂow conﬁgurations will be investigated in the future.
Ackonwledgement
This research is supported by National Natural Science Foundation of China (11701038,
11772281, 91852114), the Fundamental Research Funds for the Central Universities, and the
National Numerical Windtunnel project. The authors would like to thank Prof. Xuesheng
Chu for implementation of parallel computation, Prof. Lianping Wang for providing the
channel turbulence data of LBM and DUGKS, and TianHe-II in Guangzhou for providing
high performance computational resources.
References
[1] H. Tennekes, J. L. Lumley, A ﬁrst course in turbulence, MIT press (1972).
[2] S.B. Pope. Turbulent ﬂows, Cambridge, (2001).
[3] J. Kim, P. Moin, R. Moser, Turbulence statistics in fully developed channel ﬂow at low Reynolds
number, J. Fluid. Mech. 177 (1987) 133-166.
[4] M. Lee, R. Moser, Direct numerical simulation of turbulent channel ﬂow up to Reτ ≈5200, J. Fluid.
Mech. 774 (2015) 395-415.
[5] P. Moin, K. Mahesh, Direct numerical simulation: a tool in turbulence research, Annu. Rev. Fluid
Mech. 30 (1998) 539-578.
[6] L.P. Wang, S.Y. Chen, J.G. Brasseur, J.C. Wyngaard, Examination of hypotheses in the kolmogorov
reﬁned turbulence theory through high-resolution simulations. part 1. velocity ﬁeld, J. Fluid Mech. 309
(1996) 113-156.
27

[7] S.Y. Chen, G. D. Doolen, Lattice boltzmann method for ﬂuid ﬂows, Annu. Rev. Fluid Mech. 30 (1998)
329-364.
[8] H.D. Yu, S.S. Girimaji, L.S. Luo, Lattice boltzmann simulations of decaying homogeneous isotropic
turbulence, Phys. Rev. E 71 (2005) 016708.
[9] G.Y. Cao, L. Pan, K. Xu, Three dimensional high-order gas-kinetic scheme for supersonic isotropic
turbulence I: criterion for direct numerical simulation, Computers & Fluids 192 (2019) 104273.
[10] S. Sarkar, G. Erlebacher, M.Y. Hussaini, H.O. Kreiss, The analysis and modelling of dilatational terms
in compressible turbulence, Journal of Fluid Mechanics, 227 (1991) 473-493.
[11] P. Sagaut, C. Cambon, Homogeneous turbulence dynamics, Springer (2008).
[12] X.D. Liu, S. Osher, T. Chan, Weighted essentially non-oscillatory schemes, J. Comput. Phys. 115 (1994)
200-212.
[13] G.S. Jiang, C.W. Shu, Eﬃcient implementation of Weighted ENO schemes, J. Comput. Phys. 126
(1996) 202-228.
[14] M. Castro, B. Costa, W. S. Don, High order weighted essentially non-oscillatory WENO-Z schemes for
hyperbolic conservation laws, J. Comput. Phys. 230 (2011) 1766-1792.
[15] S. K. Lele, Compact ﬁnite diﬀerence schemes with spectral-like resolution, J. Comput. Phys. 103 (1992)
16-42.
[16] J.C. Wang, L.P. Wang, Z.L. Xiao, Y. Shi, S.Y. Chen, A hybrid numerical simulation of isotropic
compressible turbulence, J. Comput. Phys. 229 (2010) 5257-5279.
[17] S. Jeﬀrey, K. Abdollah, A. Juan, D. David, G. William, L. Elizabeth, M. Dimitri, CFD vision 2030
study: a path to revolutionary computational aerosciences, 2014.
[18] P.L. Bhatnagar, E.P. Gross, M. Krook, A Model for Collision Processes in Gases I: Small Amplitude
Processes in Charged and Neutral One-Component Systems, Phys. Rev. 94 (1954) 511-525.
[19] S. Chapman, T.G. Cowling, The Mathematical theory of Non-Uniform Gases, third edition, Cambridge
University Press, (1990).
[20] K. Xu, Gas kinetic schemes for unsteady compressible ﬂow simulations, Lecure Note Ser. 1998-03, Von
Karman Institute for Fluid Dynamics Lecture (1998).
[21] K. Xu, A gas-kinetic BGK scheme for the Navier-Stokes equations and its connection with artiﬁcial
dissipation and Godunov method, J. Comput. Phys. 171 (2001) 289-335.
[22] E.F. Toro, Riemann Solvers and Numerical Methods for Fluid Dynamics, Third Edition, Springer
(2009).
[23] J.Q. Li, Z.F. Du, A two-stage fourth order time-accurate discretization for Lax-Wendroﬀtype ﬂow
solvers I. hyperbolic conservation laws, SIAM J. Sci. Computing, 38 (2016) 3046-3069.
[24] J.Q. Li, Two-stage fourth order: temporal-spatial coupling in computational ﬂuid dynamics (CFD),
Advances in Aerodynamics, (2019) 1:3.
[25] L. Pan, K. Xu, Q.B. Li, J.Q. Li, An eﬃcient and accurate two-stage fourth-order gas-kinetic scheme
for the Navier-Stokes equations, J. Comput. Phys. 326 (2016) 197-221.
[26] L. Pan, K. Xu, Two-stage fourth-order gas-kinetic scheme for three-dimensional Euler and Navier-
Stokes solutions, Int. J. Comput. Fluid Dynamics, 32 (2018) 395-411.
[27] X. Ji, F.X. Zhao, W. Shyy, K. Xu, A family of high-order gas-kinetic schemes and its comparison with
Riemann solver based high-order methods, J. Comput. Phys. 356 (2018) 150-173.
[28] G.Y. Cao, H.L. Liu, K. Xu, Physical modeling and numerical studies of three-dimensional non-
equilibrium multi-temperature ﬂows, Physics of Fluids 30 (2018) 126104.
[29] M. Righi, A gas-kinetic scheme for turbulent ﬂow, Turbul Combust 97 (2016) 121-139.
[30] S. Tan, Q.B. Li, Z.X. Xiao, S. Fu, Gas kinetic scheme for turbulence simulation. Aerospace Science and
Technology 78 (2018) 214-27.
[31] G.Y. Cao, H.M. Su, J.X. Xu, K. Xu, Implicit high-order gas kinetic scheme for turbulence simulation,
Aerospace Science and Technology 92 (2019) 958-971.
[32] M.P.I. Forum, MPI: A Message-Passing Interface Standard, Version 2.2. High Performance Computing
Center Stuttgart (2009).
[33] J. Debonis, Solutions of the Taylor-Green vortex problem using high-resolution explicit ﬁnite diﬀerence
28

methods, AIAA 2013-0382.
[34] Y.T. Bo, P. Wang , Z.L. Guo, L.P. Wang, DUGKS simulations of three-dimensional TaylorGreen vortex
ﬂow and turbulent channel ﬂow, Computers and Fluids 155 (2017) 921.
[35] K. Xu, Direct modeling for computational ﬂuid dynamics: construction and application of uniﬁed gas
kinetic schemes, World Scientiﬁc (2015).
[36] M.E. Brachet, D.I. Meiron, S.A. Orszag, B.G. Nickel, R.H. Morf, U. Frisch, Small-scale structure of
the Taylor-Green vortex, J. Fluid. Mech. 130 (1983) 411-452.
[37] M.A. Gallis, N.P. Bitter, T.P. Koehler, J.R. Torczynski, S.J. Plimpton, and G. Papadakis, Molecular-
level simulations of turbulence and its decay, Phys. Rev. L 118 (2017) 064501.
[38] J. R. Bull, A. Jameson, Simulation of the compressible Taylor-Green vortex using high-order ﬂux
reconstruction schemes, AIAA 2014-3210.
[39] C. Bogey, C. Bailly, A family of low dispersive and low dissipative explicit schemes for ﬂow and noise
computations, J. Comput. Phys. 194 (2004) 194-214.
[40] J. Boris, F.F. Grinstein, E. Oran, R. Kolbe, New insights into large eddy simulation. Fluid Dyn Res
10 (1992) 199-228.
[41] A.W. Vreman, An eddy-viscosity subgrid-scale model for turbulent shear ﬂow: Algebraic theory and
applications, Physics of Fluids, 16 (2004) 3670-3681.
[42] S. Hoyas, J. Jim´enez, Scaling of the velocity ﬂuctuations in turbulent channels up to Reτ = 2003,
Physics of Fluids, 18 (2006) 011702.
[43] R.B. Dean, Reynolds number dependence of skin friction and other bulk ﬂow variables in two-
dimensional rectangular duct ﬂow, Trans, ASME I: J. Fluids Engng (1978).
[44] D.C. Wilcox, Turbulence modeling for CFD, DCW industries La Canada, CA (1998).
[45] R. Samtaney, D.I. Pullin, B. Kosovi´c, Direct numerical simulation of decaying compressible turbulence
and shocklet statistics, Physics of Fluids 13 (2001) 1415-1430.
[46] T. Passot, A. Pouquet, Numerical simulation of compressible homogeneous ﬂows in the turbulent
regime, J. Fluid Mech. 181 (1987) 441-466.
[47] A. Yoshizawa, K. Horiuti, A statistically-derived subgrid-scale kinetic energy model for the large-eddy
simulation of turbulent ﬂows, Journal of the Physical Society of Japan, 54 (1985) 2834-2839.
[48] J.C. Wang, M.P. Wan, S. Chen, S.Y. Chen, Kinetic energy transfer in compressible isotropic turbulence,
Journal of Fluid Mechanics, 841 (2018) 581-613.
[49] J.C. Wang, M.P. Wan, S. Chen, C.Y. Xie, S.Y. Chen, Eﬀect of shock waves on the statistics and scaling
in compressible isotropic turbulence, Phys. Rev. E 97 (2018) 043108.
29
