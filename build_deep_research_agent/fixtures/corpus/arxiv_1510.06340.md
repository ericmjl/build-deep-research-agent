---
title: "A MUSTA-FORCE algorithm for solving partial differential equations of relativistic hydrodynamics"
authors: "J. Porter-Sobieraj, M. Słodkowski, D. Kikoła, J. Sikorski, P. Aszklar"
year: 2015
source: arxiv
source_id: "1510.06340"
url: "http://arxiv.org/abs/1510.06340v5"
domain: scientific-computing
---
A MUSTA-FORCE algorithm for solving
partial diﬀerential equations of relativistic
hydrodynamics
J. Porter-Sobieraj1,M. Słodkowski2, D. Kikoła2,J. Sikorski3
P. Aszklar1
1 Warsaw University of Technology, Faculty of Mathematics and Information
Science, Koszykowa 75, 00-662 Warsaw, Poland
2 Warsaw University of Technology, Faculty of Physics, Koszykowa 75, 00-662
Warsaw, Poland
3 University of Warsaw, Faculty of Physics, Hoża 69, 00-681 Warsaw, Poland,
Abstract
Understanding event-by-event correlations and ﬂuctuations is cru-
cial for the comprehension of the dynamics of heavy ion collisions. Rela-
tivistic hydrodynamics is an elegant tool for modeling these phenomena;
however, such simulations are time-consuming, and conventional CPU
calculations are not suitable for event-by-event calculations. This work
presents a feasibility study of a new hydrodynamic code that employs
graphics processing units together with a general MUSTA-FORCE
algorithm (Multi-Stage Riemann Algorithm - First Order Centered
scheme) to deliver a high-performance yet universal tool for event-by-
event hydrodynamic simulations. We also investigate the performance
of selected slope limiters that reduce the amount of numeric oscillations
and diﬀusion in the presence of strong discontinuities and shock waves.
The numerical results are compared to the exact solutions to assess
the code’s accuracy.
Keywords: relativistic hydrodynamic, simulation of heavy ion collisions,
quark-gluon plasma, high energy nuclear physics, numerical algorithms,
MUSTA-FORCE, parallel computing, CUDA/GPU
1
arXiv:1510.06340v5  [physics.comp-ph]  16 Feb 2018

1
Motivation
Relativistic hydrodynamics simulations are widely used in the modeling of
nuclear processes in high-energy nuclear physics when examining the properties
of the quark gluon plasma (QGP). Detailed information regarding the reactions
that take place at the microscopic level is not required. Hydrodynamic model
formalism treats QGP as a perfect ﬂuid and assumes a single equation of
state. The bulk and hot nuclear system can be described using hydrodynamic
conservation laws and then solved numerically [1, 2]. Hydrodynamic models
are extremely successful in describing experimental results for particles with
low transverse momentum which is a behavior of bulk nuclear matter. On the
other hand, jets (narrow spays of hadrons and other particles produced by
the hadronization of a high energy quark or gluon) are widely used to probe
the properties of the QGP. This is an approach analogous to tomography: an
external, penetrating probe, whose properties (like a production mechanism)
are under experimental and theoretical control, is shot through the medium.
We can then infer the properties of the analyzed system from the modiﬁcation
of the probe’s energy. Jets are such probes - external to the QGP. Because
their production requires a large momentum transfer, they are produced very
early in the collision, in the initial hard interaction, before the QGP phase.
Their production is described well by perturbative quantum chromodynamics
(pQCD) calculations. Thus they are excellent tools for QGP research.
The mechanism involved in energy loss due to interactions with nuclear
matter has been a topic of extensive theoretical and experimental studies over
the last two decades. However, the energy dissipated by jets can also alter
the properties of bulk nuclear matter (for instance, so-called elliptic ﬂow) in
the intermediate transverse momentum range. There is little understanding
of such eﬀects. For such studies, we need to eﬃciently model the soft particle
evolution with a high spatial resolution to capture the jet-induced modiﬁcation
of the characteristics of the bulk nuclear matter. Moreover, the Cartesian
coordinate system is preferred to ensure a high spatial resolution that is
constant throughout the evolution of the system.
Such calculations are
necessary to fully understand the proprieties of this unique state of nuclear
matter.
The main motivation of our work is therefore to develop a new applica-
tion to study the physics of heavy ion collisions, enabling the execution of
hydrodynamic simulations on high-resolution Cartesian grids. The goal is to
combine two areas of heavy ion physics that are usually treated separately:
bulk physics, described by hydrodynamic models, and the physics of jets.
Such an approach will allow us to investigate in detail how energy deposited
by jets aﬀects the behavior of soft particles. In turn, it will help to understand
2

better the properties of nuclear matter under extreme conditions.
Moreover, event-by-event correlations and ﬂuctuations play a signiﬁcant
role in the understanding of heavy ion collision dynamics. Unfortunately,
hydrodynamic simulations are time- and computing-power-consuming, and
event-by-event calculations are challenging when conventional CPU computing
is used. The achievements of hydrodynamic models in high-energy physics
motivated us to work on a new high-performance program that facilitates event-
by-event simulation with high numerical precision using graphics processing
units.
Equations of ideal relativistic hydrodynamics in one spatial dimension can
be solved both analytically and numerically as shown e.g. in [3, 4, 5]. On a
three dimensional grid, however, an analytical solution is diﬃcult to achieve
and the problem needs to be addressed via numerical algorithms. A number of
such algorithms already exist solving relativistic hydrodynamic equations for
ideal and viscous ﬂuid models either directly [6, 7, 8, 9, 10] or retrieving the
solution from a particle-based kinematic model [11]. These solutions, however,
incur a heavy computational cost in 3+1 dimensions.
Hence, to ensure
reasonable performance, the simulation is often done in reduced dimensionality,
or one of the dimensions (usually rapidity) is represented in low resolution,
by only a few layers. This approach is motivated by certain symmetries that
areapproximately held in heavy ion collisions. Full (3+1)-dimensional, high
resolution simulations are currently very time-consuming computations for
traditional, single-threaded software.
This problem can be solved by employing general purpose computing on
graphics processing units (GPGPU). The paper [12] has shown that a GPGPU-
based implementation of the SHASTA algorithm [13] can provide up to two
orders of magnitude improvement in performance. In addition, our previous
work, based on the universal multi-stage (MUSTA-FORCE) algorithm [14,
15] also proved that hydrodynamic computations can be performed within
a reasonable timeframe.
Although the implemented method has a high
numerical cost and complexity, it scales perfectly with parallel computations.
Our implementation turned out to be over 200 times faster than a sequential
implementation on a CPU [16]. It produces good statistics and high spacial
and temporal resolutions at the same time.
The speed-up gained by using a GPU made it possible to develop a valuable
new tool for high energy nuclear science. Our current GPU implementation
allows a device to perform a massive number of simulations, and furthermore,
the MUSTA-FORCE algorithm is a very universal tool. Its strength lies in the
fact that it uses simple central schemes and does not require any knowledge
of the physical process’s details. However, in the case of large gradients it is
necessary to apply a slope limiter to reduce numerical oscillations. Therefore,
3

we focused here on how to improve the accuracy of the MUSTA-FORCE
algorithm. The hydrodynamic simulation results presented in this paper show
that the MUSTA-FORCE method is very sensitive to the choice of slope and
slope limiter, and the way that it is applied. We used such a procedure for
each dimension separately, but in general it could be applied in other ways
(e.g. a common slope limiting value could be chosen for all the variables).
There is no general procedure in a multi-dimensional and non-scalar case,
and always some experimentation is necessary for both a particular system of
equations, and perhaps even a particular problem. Under the conditions of our
simulation the schemes must be especially sensitive to problems containing
both strong discontinuities and smooth solution features.
The paper is organized as follows. The MUSTA-FORCE algorithm, to-
gether with the slope limiters, is described in detail in Section 2. Section 3
presents the results of using such slope limiters for standard benchmarks in
nuclear physics and compares them with known analytical solutions. We
discuss their ability to achieve high order accuracy in smooth regions while
maintaining stable, non-oscillatory and sharp discontinuity transitions. The
last section concludes our paper.
2
Hydrodynamics Simulations
2.1
Mathematical Description
Relativistic hydrodynamics simulations are based on hyperbolic partial diﬀer-
ential equations in the form:
∂U
∂t + ∂F(U)
∂x
+ ∂G(U)
∂y
+ ∂H(U)
∂z
= 0
(1)
and an equation of state:
p = p(e, n)
(2)
U = (E, Mx, My, Mz, R) is a vector of conserved quantities in the laboratory
rest frame; E is the energy density, Mx, My and Mz are the momentum
densities in the x, y and z Cartesian coordinates, respectively, and R is
a conserved charge density. Vectors of ﬂuxes F, G, H in the x, y, and z
4

directions are deﬁned as:
F(U) =


(E + p)vx
Mxvx + p
Myvx
Mzvx
Rvx


G(U) =


(E + p)vy
Mxvy
Myvy + p
Mzvy
Rvy


H(U) =


(E + p)vz
Mxvz
Myvz
Mzvz + p
Rvz


(3)
where v is the velocity, and p is pressure, deﬁned by the energy e and charge
density n in the ﬂuid rest frame, where velocity v vanishes (v = (0, 0, 0)).
Additionally, the following relations occur:
E
=
(ε + p)γ2 −p
Mi
=
(ε + p)γ2vi,
i = x, y, z
(4)
R
=
nγ
where ε is the energy density and γ =
1
√
1−v2 is the Lorentz factor. Eq. 4
deﬁnes the transformation from rest frame variables to conserved variables
used in integration.
2.2
Initial Conditions
To start hydrodynamic evolution, an initial state is required as input.
The most basic is parametrizations based e.g. on Glauber-like models
in the transverse plane (see [17] for a review), and Bjorken’s solution in the
longitudinal direction.
Other approaches involve models based on color glass condensate (CGC),
which describe a Lorentz contracted and slowed down, fast moving particle;
pQCD+saturation model [18], or the string rope model [19].
5

These models describe a smooth, averaged initial state. However, since
the hydrodynamic equations are nonlinear, a solution with an averaged initial
state is not equivalent to the average of solutions with ﬂuctuating initial
conditions. Because of this, event-by-event calculations became a major point
of interest.
Fluctuating initial conditions can be obtained using e.g. Monte–Carlo
Glauber [20, 21, 22] or CGC, SPheRIO, NeXus [23], NeXSPheRIO [24], and
models like EPOS [25] or UrQMD [26].
2.3
Time Integration
For time propagation the standard Runge–Kutta methods are employed [29].
For numerical stability only total variation diminishing methods are used.
In general, a Runge–Kutta method for Eq. 1 can be written in the form:
U n
(0)
=
U n
U n
(i)
=
i−1
X
k=0
(αikU n
(k) + ∆tβikL(U n
(k))),
i = 1, . . . , m
(5)
U n+1
=
U n
(m)
where the upper index without parentheses denotes the time step, the lower
index denotes integration step, L is a numerical recipe to calculate the negative
ﬂux gradient in Eq. 1 and α, β are constant coeﬃcients given for a particular
method.
For second order accuracy the following method is used:
U n
(1)
=
U n + ∆tL(U n)
U n+1
=
1
2(U n + U n
(1) + ∆tL(U n
(1)))
(6)
and for third order accuracy:
U n
(1)
=
U n + ∆tL(U n)
U n
(2)
=
3
4U n + 1
4U n
(1) + 1
4∆tL(U n
(1))
(7)
U n+1
=
1
3U n + 2
3U n
(2) + 2
3∆tL(U n
(2))
It is apparent that apart from the additional computational cost due to more
evaluations of L, these methods introduce the need for an additional storage
register for each of the conserved variables. As this can be an issue for large
resolution simulations, a low storage version of the third order method can
be used.
6

2.4
Hybrid MUSTA-FORCE Algorithm
To obtain a general and accurate solution for Eq. 1 and Eq. 2, we use a
hybrid MUlti–STAge (MUSTA) approach [15, 27]. This utilizes a centered
ﬂux in a predictor–corrector loop, solving the Riemann problem numerically,
i.e. without using a priori information about waves.
In order to calculate ﬂux Fi+ 1
2 the algorithm, in a one dimensional case,
is as follows:
1. Introduce auxiliary variables U (l)
L and U (l)
R and their ﬂuxes F (l)
L and F (l)
R .
2. Set U 0
L = Ui, U 0
R = Ui+1.
3. Calculate F (l)
i+ 1
2 using a centered ﬂux, U (l)
L , U (l)
R , F (l)
L
and F (l)
R .
If l
reached a maximum number of iterations, stop.
4. Solve Riemann problem locally:
U (l+1)
L
= U (l)
L −∆t
∆x

F (l)
i+ 1
2 −F (l)
L

,
U (l+1)
R
= U (l)
R −∆t
∆x

F (l)
R −F (l)
i+ 1
2

.
(8)
5. Go back to step 3.
As a centered ﬂux in step 3, we use the First ORder CEntered (FORCE)
scheme:
F force
i+ 1
2 = 1
2

F lw
i+ 1
2 + F lf
i+ 1
2

(9)
where F lw
i+ 1
2 is the Lax-Wendroﬀtype ﬂux:
F lw
i+ 1
2 = F
 1
2(UL + UR) −α∆t
2∆x(UR −UL)
!
(10)
and F lf
i+ 1
2 is the Lax-Friedrichs type ﬂux:
F lf
i+ 1
2 = 1
2(FL + FR) −∆x
2α∆t(UR −UL)
(11)
In a three-dimensional case α = 3, but other values may also be considered.
To achieve second order accuracy in space and time, we extend our
algorithm with the MUSCL-Hancock scheme. The basic idea of this scheme
is to use more cells to interpolate inter-cell values and evolve them half a time
step:
7

1. Replace cell average values U n
i by a piecewise linear function inside i-th
cell:
Ui(x) = U n
i + (x −xi)
∆x
∆i
(12)
where ∆i is a slope vector and will be deﬁned later.
In the local coordinates the points x = 0 and x = ∆x correspond to
boundaries of the cell xi−1
2 and xi+ 1
2. The values at these points are
U L
i = U n
i −∆i/2 and U R
i = U n
i + ∆i/2.
2. Propagate U L
i and U R
i by a time 1
2∆t:
˜U L
i
=
U L
i + 1
2
∆t
∆x(F(U L
i ) −F(U R
i ))
+1
2
∆t
∆y(G(U L
i ) −G(U R
i ))
+1
2
∆t
∆z(H(U L
i ) −H(U R
i ))
˜U R
i
=
U R
i + 1
2
∆t
∆x(F(U L
i ) −F(U R
i ))
(13)
+1
2
∆t
∆y(G(U L
i ) −G(U R
i ))
+1
2
∆t
∆z(H(U L
i ) −H(U R
i ))
3. Use ˜U L
i and ˜U R
i as U 0
L and U 0
R in MUSTA.
A simple choice for the slope ∆i in Eq. 12 is:
∆i = 1
2(U n
i+1 −U n
i−1)
(14)
which indeed results in a second-order accurate algorithm.
However, as
predicted by Godunov’s theorem, it has the unpleasant eﬀect of producing
spurious oscillations in the case of strong gradients. Complex study of MUSTA
schemes can be found in [28].
2.5
Slope Limiters in the MUSTA-FORCE
To avoid such oscillations and to solve problems that appear in the presence
of shocks, discontinuities or sharp changes, ﬂux limiting and slope limiting
8

methods have been proposed [30, 31]. We employed a slope limiting method;
instead of ∆i as in Eq. 14 we use
˜∆i = ξ(ri)(Ui −Ui−1)
(15)
in Eq. 12, where ξ is called the slope limiter and
ri = Ui+1 −Ui
Ui −Ui−1
.
(16)
Then one can calculate U L
i and U R
i using the following relations
U L
i = Ui −1
2ξ(1/ri)(Ui+1 −Ui),
U R
i = Ui + 1
2ξ(ri)(Ui −Ui−1).
(17)
There are a number of possible choices for ξ, each with its own character-
istics and features. The four diﬀerent limiters investigated in this paper are
Minbee (MB) [32], Superbee (SB) [33], van Albada (VA) [34] and van Leer
(VL) [35]. They are expressed as:
ξMB(r) = max(0, min(1, r))
(18)
ξSB(r) = max(0, min(2r, 1), min(r, 2))
(19)
ξVA(r) = r2 + r
r2 + 1
(20)
ξVL(r) = r + |r|
1 + |r|
(21)
All the four limiters are symmetric, i.e. they meet the symmetry property:
ξ(1
r) = ξ(r)
r
(22)
that provides that forward and backward gradients are treated in the same
manner. Otherwise, the results on the left would diﬀer from those on the
right despite initial symmetry in the system.
The limiters are designed to reduce the scheme to ﬁrst order accuracy near
shocks, and keep higher order in smooth areas. Introducing non–linearity
in this way reduces spurious oscillations and retains good accuracy of the
solution.
The two most extreme slope limiters are Minbee and Superbee. The ﬁrst
one is the most dissipative and the second - the least. Between them lies the
admissible region for second order total variation diminishing (TVD) limiters.
Here it should also be stressed, that results are very sensitive to the choice
of slope in Eq. 14 and the slope limiter—both the formula for ξ, and the way
that it is applied.
9

2.6
Calculating the hydrodynamic ﬂux
To complete the chapter about numerical methods for relativistic hydrody-
namics, one more detail must still be dealt with. It is easy to change from
rest frame variables and velocities to the conserved variables used in the
integration. The inverse transformation, however, is not trivial.
It is needed, however, each time we compute the ﬂux, since the equation
of state (2) is deﬁned as a function of e and n, and not E and R. As in [36],
we can invert equations (4) and get
e
=
E −Mv
n
=
R
√
1 −v2
(23)
v
=
M
E + p(e, n)
=
M
E + p(E −Mv, R
√
1 −v2)
The set of equations (23) can be solved numerically, starting from the last
one as the ﬁxed point equation for v.
3
Discussion and Results
0
1
2
3
4
5
6
7
8
9
10
11
-3
-2
-1
0
1
2
3
4
charge density [GeV/fm3]
distance from center [fm]
simulation
analytic
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
-3
-2
-1
0
1
2
3
4
velocity [c−1]
distance from center [fm]
simulation
analytic
Figure 1: Sod shock tube, charge density in the local rest frame of the ﬂuid
(left) and velocity (right), MUSTA-FORCE with no limiter.
3.1
Implementation Notes
In the case of hydrodynamics simulations, fully (3+1)-dimensional simulations
in space and in time are much-desired, to describe the system’s evolution
10

without any assumptions regarding its symmetries and without decreasing
the dimension of the problem. Moreover, event-by-event calculations become
a major point of interest, with ﬂuctuating initial conditions and with a large
amount of statistics. Such simulations are extremely expensive in terms of
computing power and require an eﬃcient and fast computer code.
Therefore, we implemented the hydrodynamics simulation algorithm on a
GPU using an NVIDIA CUDA framework [37]. Due to the large numerical
grids in the simulations and the complexity of the computations, we used
surface memory to store the simulation data. The state of the system is
saved as 5 single precision ﬂoating-point numbers per lattice cell – the energy
density, conserved charge density, and 3 momenta density; all in the laboratory
reference frame. The maximum grid that ﬁts then within the surface memory
limitations is 2403.
3.2
Numerical Experiments
To verify the simulation reliability, the MUSTA-FORCE algorithm itself was
tested (along with the four slope limiters – Minbee, Superbee, van Albada and
van Leer) against three analytical solutions to relativistic hydrodynamics –
the Sod shock tube [38, 39], the Hubble-like expansion [40] and ellipsoidal ﬂow
[41, 42]. For each of them, plots of chosen variables are presented together
with the theoretical curves.
The number of stages and the order of Runge–Kutta method were ﬁtted
experimentally. In all the presented cases four MUSTA stages guaranteed
stability and good numerical accuracy in acceptable calculation time on GPU.
The third order accurate Runge–Kutta method was used for time integration.
Many numerical experiments for diﬀerent parameters were carried out
1
2
3
4
5
6
7
8
9
10
-3
-2
-1
0
1
2
3
4
charge density [GeV/fm3]
distance from center [fm]
simulation
analytic
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
-3
-2
-1
0
1
2
3
4
velocity [c−1]
distance from center [fm]
simulation
analytic
Figure 2: Sod shock tube, charge density in the local rest frame of the ﬂuid
(left) and velocity (right), MUSTA-FORCE with with Minbee limiter.
11

to verify correctness, convergence and robustness of the MUSTA-FORCE
method. We present here the results for one representative set of parameters
per analytical solution. The initial conditions and parameters like time step
∆t and grid spacing ∆x, ∆y and ∆z were given for each experiment separately.
In all the cases the Courant number was less than 1. More detailed analysis
of CFL numbers and stability limits in the MUSTA approach can be found
in [43].
3.2.1
Sod Shock Tube
The ﬁrst test is a solution to the Riemann problem. This is a one dimensional
solution, whose initial state comprises two regions of stationary ﬂuid with a
charge and pressure discontinuity in the middle.
When the discontinuity is big enough, a relativistic shock wave appears
in the solution. The initial conditions (given in Table 1 together with other
parameters) were chosen to produce such a shock wave.
parameter
value
grid size
500
grid spacing
0.02
time step
0.005
pL
131
3
pR
0
nL
10
nR
1
Table 1: Parameters of the Sod shock tube simulations
0
1
2
3
4
5
6
7
8
9
10
-3
-2
-1
0
1
2
3
4
charge density [GeV/fm3]
distance from center [fm]
simulation
analytic
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
-3
-2
-1
0
1
2
3
4
velocity [c−1]
distance from center [fm]
simulation
analytic
Figure 3: Sod shock tube, charge density in the local rest frame of the ﬂuid
(left) and velocity (right), MUSTA-FORCE with Superbee limiter.
12

1
2
3
4
5
6
7
8
9
10
-3
-2
-1
0
1
2
3
4
charge density [GeV/fm3]
distance from center [fm]
simulation
analytic
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
-3
-2
-1
0
1
2
3
4
velocity [c−1]
distance from center [fm]
simulation
analytic
Figure 4: Sod shock tube, charge density in the local rest frame of the ﬂuid
(left) and velocity (right), MUSTA-FORCE with van Albada limiter.
0
1
2
3
4
5
6
7
8
9
10
-3
-2
-1
0
1
2
3
4
charge density [GeV/fm3]
distance from center [fm]
simulation
analytic
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
-3
-2
-1
0
1
2
3
4
velocity [c−1]
distance from center [fm]
simulation
analytic
Figure 5: Sod shock tube, charge density in the local rest frame of the ﬂuid
(left) and velocity (right), MUSTA-FORCE with van Leer limiter.
The solution is divided into waves: the shock wave, the contact disconti-
nuity, and the rarefaction wave.
The results are presented in Figs. 1–5.
For the no limiter case (Fig. 1) with the MUSTA-FORCE algorithm,
oscillations at the contact points of waves become visible. The shock is also
smeared out from the left side. For Minbee (Fig. 2) the overshoot is almost
entirely gone, at the cost of some visible diﬀusion, especially in the shock
wave region. Superbee in Fig. 3 is the most compressive limiter. The shocks
are sharpened, but additional oscillations are introduced. Also the overshoot
clearly visible in the velocity plot is enhanced. The van Albada limiter in
Fig. 4 trades some sharpness for better rendition of the velocity proﬁle; f and
for van Leer (Fig. 5) the shocks are sharp and the oscillations are gone, but
the overshoot is still signiﬁcant.
To sum up, van Albada and the Minbee limiter seem to be closest to the
13

analytic solution, and those two will be presented in rest of the tests.
3.2.2
Hubble-like Expansion
This is a three-dimensional, spherically symmetrical solution of matter that
expands uniformly. The velocity is proportional to the distance from the
center v =⃗r
t. The energy density is given by:
e = e0

τ0
√
t2 −r2
!3(1+c2
s)
(24)
In our case the solution is well deﬁned for r < t. For the test we set r < t−0.5
fm and put a vacuum (e = v = 0) outside this region. This means that the
solution is exact only in the central area—on the periphery the matter will
expand into the vacuum, so a rarefaction wave is expected. The solution uses
an ultra-relativistic equation of state p = c2
se.
Initial parameters are given in Table 2.
parameter
value
grid size
1203
grid spacing
0.1
time step
0.03
e0
1
c2
s
1
3
τ0
4
t0
2
Table 2: Parameters of the Hubble–like expansion simulations
The results are presented in Fig. 6 and Fig. 7. y = z = 0 sections are
shown through the three dimensional solution.
The results are similar to those in the previous test. The schemes were
accurate in the middle region, and the Minbee limiter has shown less diﬀusion
than van Albada at the sides.
3.2.3
Ellipsoidal Flow
The last test uses the ellipsoidal solution, which is a generalized Hubble–like
solution (with velocity proportional to⃗r), a gaussian proﬁle and vanishing
pressure p = 0. The variables are given by the following equations:
14

0.1
1
10
-6
-4
-2
0
2
4
6
energy density [GeV/fm3]
distance from center [fm]
simulation
analytic
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1
-6
-4
-2
0
2
4
6
velocity [c−1]
distance from center [fm]
simulation
analytic
Figure 6: Hubble-like expansion, energy density in the local rest frame of the
ﬂuid (left) and velocity (right), MUSTA-FORCE with Minbee limiter.
0.1
1
10
-6
-4
-2
0
2
4
6
energy density [GeV/fm3]
distance from center [fm]
simulation
analytic
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1
-6
-4
-2
0
2
4
6
velocity [c−1]
distance from center [fm]
simulation
analytic
Figure 7: Hubble-like expansion, energy density in the local rest frame of the
ﬂuid (left) and velocity (right), MUSTA-FORCE with van Albada limiter.
e
=
Ce
Q
i (t + Ti) exp

−b2
e
t2
τ 2
!
(25)
n
=
Cn
Q
i (t + Ti) exp

−b2
n
t2
τ 2
!
(26)⃗
v
=
 a1(t)x
t
, a3(t)y
t
, a2(t)z
t
!
(27)
where τ =
r
t2 −P
i a2
i x2
i , ai ≡ai(t) = t/(t + Ti) and Ce, Cn, be, bn, Ti are
constants; i = 1, 2, 3.
Initial parameters are given in Table 3.
The results are presented in Fig. 8 and Fig. 9. y = z = 0 sections are
15

parameter
value
grid size
1203
grid spacing
0.1
time step
0.02
t0
2
Ce
2
Cn
0.75
be
1
bn
1
T1
0.4
T2
0.6
T3
0.8
Table 3: Parameters of the ellipsoidal ﬂow simulations
0
0.001
0.002
0.003
0.004
0.005
0.006
0.007
0.008
-6
-4
-2
0
2
4
6
energy density [GeV/fm3]
distance from center [fm]
simulation
analytic
0
0.2
0.4
0.6
0.8
1
-6
-4
-2
0
2
4
6
velocity [c−1]
distance from center [fm]
simulation
analytic
Figure 8: Ellipsoidal ﬂow, energy density in the local rest frame of the ﬂuid
(left) and velocity (right), MUSTA-FORCE with Minbee limiter.
shown through the three dimensional solution. This solution, despite being
pressureless, most resembles a physically relevant situation. The Minbee
limiter has shown again less oscillations than others at the sides.
4
Conclusions
As a result of this paper, we have implemented and tested a MUSTA-FORCE
algorithm dedicated to solving conservative ﬁeld equations. The universal
MUSTA-FORCE algorithm proved to be quite eﬃcient and robust. Despite
promising initial results, it turned out that the MUSTA-FORCE produced
numerical oscillations. Fig. 10 illustrates two dimensional energy density
cross section in the xy plane of the MUSTA-FORCE with Albada limiter.
16

0
0.001
0.002
0.003
0.004
0.005
0.006
0.007
0.008
-6
-4
-2
0
2
4
6
energy density [GeV/fm3]
distance from center [fm]
simulation
analytic
0
0.2
0.4
0.6
0.8
1
-6
-4
-2
0
2
4
6
velocity [c−1]
distance from center [fm]
simulation
analytic
Figure 9: Ellipsoidal ﬂow, energy density in the local rest frame of the ﬂuid
(left) and velocity (right), MUSTA-FORCE with van Albada limiter.
It conﬁrms the clearly visible anisotropy of the numerical oscillations. To
address this issue, we performed a detailed study of universal slope limiters
to reduce oscillations or asymmetric propagation. In all test cases the Minbee
limiter has shown the best numerical properties.
This implementation of a relativistic hydrodynamic code is designed
to run eﬃciently on contemporary graphics processing units, which have
many times more computing power compared to ordinary CPU processors.
Benchmarks and comparison to an equivalent implementation of some of these
algorithms in C show speedups of over 2 orders of magnitude. Thanks to
such performance levels, event-by-event analyses can be conducted eﬃciently
with a relatively low cost, just a few modern workstations. Our work also
provides a framework for implementing other algorithms for high-statistics
event-by-event hydrodynamic simulations.
All the calculations were made as fully (3+1)-dimensional simulations in
space and in time, without any assumptions regarding its symmetries and
without decreasing the dimension of the problem. Such (3+1)-dimensional
numerical simulation on high-resolution Cartesian grids is a novel result. It
allows us to run hydrodynamic simulations, provide information about prop-
erties of the relativistic bulk nuclear matter (QGP) by studying jet-medium
interaction and jet-induced ﬂow. Furthermore event-by-event simulations
allow us to investigate initial condition ﬂuctuation of the heavy ion collision
in the pre-equlibrium stage and it might have an impact on the dynamic in
the nuclear medium.
17

-6
-4
-2
0
2
4
6
x [fm]
-6
-4
-2
0
2
4
6
y [fm]
Figure 10: Ellipsoidal ﬂow in the xy plane, energy density in the local rest
frame of the ﬂuid, MUSTA-FORCE with van Albada limiter.
References
[1] E. Gourgoulhon, "An introduction to relativistic hydrodynamics," EAS
Publications Series, vol. 21, 2008, pp. 43–79.
[2] P. Huovinen and P. V. Ruuskanen, "Hydrodynamic models for heavy ion
collisions," Ann. Rev. Nucl. Part. Sci., vol. 56, 2006, pp. 163–206.
[3] V. Schneider, U. Katscher, D. H. Rischke, B. Waldhauser, J. A. Maruhn
and C.-D. Munz, "New algorithm for ultra-relativistic numerical hydro-
dynamics," Journal of Computational Physics, vol. 105, 1993, pp. 92-107.
[4] D. S. Balsara, "Riemann solver for relativistic hydrodynamics," Journal
of Computational Physics, vol. 114, 1994, pp. 284-297.
[5] H. Cheng, H. Yang, and Y. Zhang, "Riemann problem for the Chaplygin
Euler equations of compressible ﬂuid ﬂow." International Journal of
18

Nonlinear Sciences and Numerical Simulation, 11 no. 11, 2010, pp. 985-
992.
[6] Y. Akamatsu, S. Inutsuka, C. Nonaka and M. Takamoto, "A new scheme
of casual viscous hydrodynamics for relativistic heavy-ion collisions:
a Riemann solver for quark-gluon plasma," Journal of Computational
Physics, vol. 256, 2014, pp. 34-54.
[7] I. A. Karpenko, P. Huovinen and M. Bleicher, "A 3+1 dimensional
viscous hydrodynamic code for relativistic heavy ion collisions," Computer
Physics Communications, vol. 185, no. 11, pp. 3016-3027, 2014.
[8] Y. Tachibana and T. Hirano, "Momentum transport away from a jet in
an expanding nuclear medium," Phys. Rev., vol. C90, no. 2, pp. 021902,
2014.
[9] P. Bożek, "Flow and interferometry in (3 + 1)-dimensional viscous
hydrodynamics," Phys. Rev. C, vol. 85, no. 11, pp. 034901–034909, 2012.
[10] S. V. Akkelin, Y. Hama, Iu. A. Karpenko and Yu. M. Sinyukov, "Hydro-
kinetic approach to relativistic heavy ion collisions," Phys. Rev. C, vol. 78,
no. 3, pp. 034906–034920, 2008.
[11] I. Sagert, W. Bauer, D. Colbry, J. Howell, R. Pickett, A. Staber and T.
Strother, "Hydrodynamic shock wave studies within a kinetic Monte Carlo
approach," Journal of Computational Physics, vol. 266, 2014, pp. 191-213
[12] J. Gerhard, V. Lindenstruth and M. Bleicher, "Relativistic hydrody-
namics on graphic cards," Comput.Phys.Commun., vol. 184, no. 2 2013,
pp. 311-319.
[13] J. P. Boris and D. L. Book, "Flux-corrected transport. I. SHASTA, a
ﬂuid transport algorithm that works," Journal of Computational Physics,
vol. 11, no. 1, pp. 38–69, 1973.
[14] E. F. Toro, Multi-stage predictor-corrector ﬂuxes for hyperbolic equa-
tions, Isaac Newton Institute for Mathematical Sciences Preprint Series
NI03037-NPA, University of Cambridge, UK, 2003.
[15] E. F. Toro, "MUSTA: a multi-stage numerical ﬂux," Appl. Numer. Math.,
vol. 56, no. 10, 2006, pp. 1464–1479.
[16] S. Cygert, J. Porter-Sobieraj, D. Kikola, J. Sikorski and M. Slodkowski,
"Towards an eﬃcient multi-stage Riemann solver for nuclear physics
19

simulations," in Computer Science and Information Systems (FedCSIS),
2013 Federated Conference on , 2013, pp. 441–446.
[17] M. L. Miller, K. Reygers, S. J. Sanders and P. Steinberg, "Glauber
modeling in high energy nuclear collisions," Ann.Rev.Nucl.Part.Sci.,
vol. 57, 2007, pp. 205–243.
[18] K. J. Eskola, H. Niemi and P. V. Ruuskanen, "Elliptic ﬂow from pQCD
+ saturation + hydro model," J. Phys. G35, 2008.
[19] V. K. Magas, L. P. Csernai and D. Strottman, "Eﬀective string rope
model for the initial stages of ultra-relativistic heavy ion collisions,"
Nuclear Physics A, vol. 712, no. 1-2, 2002, pp. 167–204.
[20] B. Alver, M. Baker, C. Loizides and P. Steinberg, "The PHOBOS Glauber
Monte Carlo", 2008, arXiv:0805.4411.
[21] W. Broniowski, M. Rybczynski and P. Bozek, "GLISSANDO: Glauber
initial-state simulation and more," Comput.Phys.Commun., vol. 180,
no. 1, 2009, pp. 69–83.
[22] M. Rybczynski, G. Stefanek, W. Broniowski and P. Bozek, "GLIS-
SANDO 2: Glauber initial-state simulation and more..., ver. 2," Com-
put.Phys.Commun., vol. 185, no. 6, 2014, pp. 1759-1772.
[23] H. J. Drescher, S. Ostapchenko, T. Pierog and K. Werner, "Initial
condition for QGP evolution from NEXUS," Phys.Rev. C, vol. 65:054902,
2002.
[24] R. Derradi de Souza, J. Takahashi and T. Kodama, "Eﬀects of initial
state ﬂuctuations in the ﬁnal state elliptic ﬂow measurements using the
NeXSPheRIO model," Phys. Rev., vol. C85, pp. 054909, 2012.
[25] T. Pierog, Iu. Karpenko, S. Porteboeuf, S. and K. Werner, "New Devel-
opments of EPOS 2," 2010, arXiv:1011.3748.
[26] S. A. Bass, M. Belkacem, M. Bleicher, M. Brandstetter, L. Bravina
et al. "Microscopic models for ultrarelativistic heavy ion collisions,"
Prog.Part.Nucl.Phys., vol. 41, 1998, pp. 255–369.
[27] E. F. Toro, Riemann solvers and numerical methods for ﬂuid dynamics:
A practical introduction, Springer, 1999.
[28] E.F. Toro, and V.A. Titarev, "MUSTA ﬂuxes for systems of conservation
laws" Journal of Computational Physics, 216(2), pp.403-429., 2006.
20

[29] E. Constantinescu and A. Sandu, "Explicit time stepping methods with
high stage order and monotonicity properties," in Proc. of the 9th Inter-
national Conference on Computational Science, 2009, pp. 293–301.
[30] A. Harten and S. Osher, "Uniformly high-order accurate nonoscillatory
schemes," SIAM Journal on Numerical Analysis, 1987, pp. 279–309.
[31] M. Berger, S. M. Murman and M. J. Aftosmis, "Analysis of slope limiters
on irregular grids", In 43rd AIAA Aerospace Sciences Meeting and Exhibit,
2005.
[32] P. K. Sweby and M. J. Baines, "Convergence of Roe’s scheme for the gen-
eral non-linear scalar wave equation," Reading Univ. Numerical Analysis
Report, 1981.
[33] P. L. Roe, "Some contributions to the modelling of discontinuous ﬂows,"
In Proc. AMS/SIAM Seminar, San Diego, 1983.
[34] G. D. van Albada, B. van Leer and W. W. Roberts, "A comparative
study of computational methods in cosmic gas dynamics," Astronomy
and Astrophysics, vol. 108, 1982, pp. 76–84.
[35] B. van Leer, "Towards the ultimate conservative diﬀerence scheme,
Monotonicity and conservation combined in a second order scheme,"
J.Comp.Phys., vol. 14, 1974, pp. 361–370.
[36] D. H. Rischke, "Fluid dynamics for relativistic nuclear collisions," In
Hadrons in Dense Matter and Hadrosynthesis, Springer Verlag, 1999.
[37] NVIDIA Corporation: CUDA C Programming Guide, 2014.
[38] K. W. Thompson, "The special relativistic shock tube," Journal of Fluid
Mechanics, vol. 171, 1986, pp.365–375.
[39] J. M. Martí and E. Müller, "Numerical hydrodynamics in special relativ-
ity," Living Rev. Relativity, vol. 6, 2003.
[40] M. Chojnacki, W. Florkowski and T. Csörgö, "Formation of Hubble-like
ﬂow in little bangs,", Physical Review C, vol. 71, no. 4, pp. 044902, 2005.
[41] Yu. M. Sinyukov and Iu. A. Karpenko, "Quasi-inertial ellipsoidal ﬂows
in relativistic hydrodynamics," 2005, arXiv:nucl-th/0505041.
[42] Y. M. Sinyukov and I. A. Karpenko, "Ellipsoidal ﬂows in relativistic
hydrodynamics of ﬁnite systems" Acta Physica Hungarica Series A, Heavy
Ion Physics, vol. 25, no. 1, pp. 141–147, 2006.
21

[43] P.M. Blakely, N. Nikiforakis, and W.D. Henshaw, "Assessment of the
MUSTA approach for numerical relativistic hydrodynamics" Astronomy
and Astrophysics, 575 (A102), 2015.
22
