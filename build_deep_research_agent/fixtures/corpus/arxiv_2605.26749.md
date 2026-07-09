---
title: "Constraining Early Dark Energy cosmological models with Big Bang Nucleosynthesis"
authors: "Teodora M. Matei, Cristian Croitoru, Tiberiu Harko"
year: 2026
source: arxiv
source_id: "2605.26749"
url: "http://arxiv.org/abs/2605.26749v2"
domain: astrophysics
---
Constraining Early Dark Energy cosmological models with Big Bang Nucleosynthesis
Teodora Maria Matei,1, 2, ∗Cristian Croitoru,3, † and Tiberiu Harko2, 1, ‡
1Astronomical Institute of Romanian Academy, Cluj-Napoca Branch,
19 Cire¸silor Street, 400487 Cluj-Napoca, Romania
2Department of Physics, Babe¸s-Bolyai University,
Kog˘alniceanu Street, Cluj-Napoca, 400084, Romania,
3Faculty of Automation and Computer Science, Technical University of Cluj-Napoca,
George Baritiu Street, 400027 Cluj-Napoca, Romania,
The recent cosmological picture contains a signiﬁcant tension indicating that our standard ΛCDM
picture may be incomplete. Early Dark Energy models can alleviate the Hubble tension, by assuming
an early acceleration that could explain the divergence between the early and late-time cosmological
data. We investigate the implications of Early Dark Energy models on the Big Bang Nucleosyn-
thesis processes by considering several cosmological models, including a model assuming a simple
cosmological constant, alongside with varying equations of state dark energy models. We construct
a simulator through a nested sampling algorithm, with the help of which we estimate the upper
bounds for model parameters, and determine the maximum allowable dark energy density contri-
bution during the radiation-dominated era. Our results are obtained through the eden program.
We show that for a linear or polytropic equation of state, the dark energy density is constrained to
less than 10−13 MeV4 and 10−5 MeV4, respectively, at the 95% conﬁdence level. Furthermore, we
identify a temperature-dependent equation of state of dark energy as the most physically compelling
framework, which remains consistent with primordial abundances for coupling parameters ≲10−2.
This model successfully allows for high-temperature deviations from the standard ΛCDM expansion
history, while rapidly diluting to obtain standard general relativistic results in the weak freeze-out
era.
CONTENTS
I. Introduction
1
II. Early Dark Energy models
3
A. Standard Cosmology with a Cosmological Constant 4
B. Varying (Dynamical) Dark Energy
4
1. Linear Equation of State
4
2. Polytropic Equation of State
5
3. Temperature-Dependent Equation of State 5
III. Nucleosynthesis Modeling
5
A. Big Bang Nucleosynthesis Theory
5
B. PRyMordial Framework Integration
6
C. Nested Sampling Algorithm
7
IV. Implementation and Results
8
A. The Cosmological Constant Model
8
B. The Linear EDE Model
10
C. The Polytropic EDE Model
11
D. The Temperature-dependent EDE Model
12
V. Discussions and Final Remarks
14
VI. Acknowledgments
17
∗teodora.matei@acad-cj.ro
† croitoru.lu.cristian@student.utcluj.ro
‡ tiberiu.harko@aira.astro.ro
References
17
I.
INTRODUCTION
The standard cosmological model ΛCDM, relies on the
presence of a cosmological constant denoted Λ, which
drives the late-time accelerated expansion of the Uni-
verse, a phenomenon ﬁrstly conﬁrmed by Type Ia super-
novae observations [1, 2], and more recently by [3, 4].
In the present-day Universe, observations constrain this
constant to Λ ≈10−56 cm−2 [3].
However, recently, the ΛCDM model is facing signiﬁ-
cant challenges from the new BAO measurements of the
ﬁrst data release of the Dark Energy Spectroscopic In-
strument (DESI), with the second data release (DR2)
raising even more questions about the validity of the
standard cosmological paradigm [5, 6]. When DESI DR2
BAO data are combined with the CMB data from Planck,
the Atacama Cosmology Telescope (ACT) [7], and Su-
pernova datasets (whether from Union3, Pantheon Plus,
or DESY5), deviations from the ΛCDM paradigm be-
come apparent, leading to the necessity of considering
Dynamical Dark Energy (DDE) models [8].
For ex-
ample, when using the CMB+DESI+DESY5 data, the
Barboza-Alcaniz (BA) model gives w0 = −0.785 ± 0.047
and wa = −0.43+0.10
−0.09, a result which notably deviates
from the ΛCDM prediction, and provides convincing ev-
idence for DDE at the 4.2σ level [8].
For a review of
the recent results and challenges of the Dynamical Dark
Energy models see [9].
The compelling evidence for Dynamical Dark Energy
models naturally raises the question of the presence, and
arXiv:2605.26749v2  [astro-ph.CO]  4 Jun 2026

2
relevance of the dark energy in the early, and very early
Universe. Did, for example, the value of the cosmologi-
cal constant change in time? Even though late-time con-
straints for the value of the cosmological constant have
been obtained from observations, its value in the early
Universe is not yet known. Hence the natural question
arises of what is the maximum allowed eﬀective value of
Λ during the ﬁrst stages of the cosmological evolution.
Therefore, the study of the inﬂuence of the cosmologi-
cal constant Λ on the dynamics of the early Universe, as
well as the consideration of the dynamically equivalent
candidate models, known as Early Dark Energy (EDE)
models may lead to a new perspective on the early Uni-
verse.
The introduction of an EDE component is primarily
motivated by the Hubble tension, i.e. the discrepancy
between local H0 measurements and those inferred from
the early Universe [10, 11].
Technically, EDE models
postulate the existence of a dynamical component that
contributes a non-negligible fraction to the total energy
density during the early radiation-dominated era, which
can raise the H0 parameter in order to alleviate the ten-
sion, initially handled through quintessential scalar ﬁelds
or high-energy phase transitions [12–14].
This ﬁeld of research was developed by [15, 16], in
which axion-like potentials were proposed, aiming to re-
solve the Hubble tension.
Some other early works in-
cluded Acoustic Dark Energy which treated acoustic os-
cillations in the dark component [17], New Dark Energy
which accounted for a phase transition before recombina-
tion [18] and Rock ’n’ Roll oscillatory and rolling scalar
ﬁeld EDE [19].
For recent reviews of EDE framework
see [20, 21].
In the context of modiﬁed gravity, dy-
namical dark energy was studied in f(R) theories [22],
f(T ) teleparallel gravity [23], and Early Modiﬁed Grav-
ity [24, 25] in which non-minimally coupled scalar ﬁelds
aﬀect the early Universe’s dynamics prior to recombina-
tion.
High-precision results from recent ACT DR6 and DESI
DR2 [6, 7] suggest that in order for the early dark en-
ergy model parameters to be compatible with CMB/LSS
requirements, the dark component is restricted to an en-
ergy fraction fEDE < 0.016. The DESI DR2 observations
favour a late-time dynamical dark energy framework, re-
cently studied through Critically Emergent Dark Energy
[26] and in the early Universe, cosmic birefringence acts
as a parity-violating signature of the dark sector [27, 28].
Other works that constrain EDE components by both
DESI and ACT datasets, are mentioned [29–32].
Besides the CMB data constraints, Big Bang Nucle-
osynthesis (BBN) can impose upper limits by measuring
weak freeze-out deviations from a modiﬁed Hubble ex-
pansion rate, altering the primordial nuclei formation.
Big Bang Nucleosynthesis is a theoretical framework
that predicts light element formation in the early times
of the Universe, such as Hydrogen, Deuterium, Helium
and Lithium (see [33–42] for early works and compre-
hensive review articles), that result in abundance ratios
Yp = He4/H or D/H, which are in agreement with recent
astrophysical measurements [43], up to the theoretical
prediction of Li7/H, which remains in high disagreement
with observations [44].
Any deviation from the GR limit can be restricted
through the abundance ratios provided through nucle-
osynthesis, so that BBN can probe frameworks that de-
part from ΛCDM model. Within such extensions of the
standard framework, scalar-tensor theories [45, 46], vary-
ing gravitational constant scenarios [47], f(R, T ) grav-
ity [48], f(T ) teleparallel gravity and generalized f(T, T )
models [49–51], modiﬁed Gauss-Bonnet gravity [52], and
bimetric gravity [53], were studied and constrained with
the help of nucleosynthesis yields. Recently, these con-
straints have been extended to more complex geometric
and high-energy frameworks, such as [54, 55] which ex-
plored the phenomenological implications of Weyl bound-
ary in the early Universe and space-time noncommuta-
tivity, and also [56], which proved that modiﬁed gravita-
tional couplings during the MeV era must remain highly
suppressed in order to predict primordial deuterium and
helium formation.
Beyond modiﬁed gravity, BBN also probes high-energy
physics and the dark sector, for example neutrino-
extended Eﬀective Field Theories [57] and electron
neutrino-sterile neutrino oscillations [58] were recently
constrained through nuclear abundances.
In the dark
matter sector, both resonantly-enhanced [59] and sub-
GeV hadronic annihilations [60], as well as on the life-
times of heavy QCD axions [61] have been restricted by
the precise astrophysical measurements of the helium and
deuterium mass fractions.
By studying the EDE component in the MeV scale, the
increase of the Hubble rate determines an overproduction
of helium and deuterium, such that BBN serves as a hard
boundary on the permissible energy fraction of the dark
sector. Recent analyses restricted these bounds, for in-
stance EDE-like scalar ﬁelds were limited based on com-
bined BBN and sound-horizon-independent CMB lens-
ing in [62]. The direct impact of an EDE density scaling
as in [63], reconﬁrms that the EDE fraction must re-
main highly subdominant to preserve concordance with
observations.
A principal component analysis was ap-
plied in [64] to impose model-independent constraints on
any dark energy history during BBN. Furthermore, EDE
was constrained alongside varying electron mass scenar-
ios by using the latest DESI DR2, ACT DR6, and BBN
datasets, ﬁnding tight upper limits on the allowed dark
energy fraction [65]. Together, these works require that
any viable EDE solution to late-time cosmological ten-
sions must either remain subdominant during the ﬁrst
three minutes or exist strictly below the energy thresh-
olds provided by primordial nucleosynthesis.
In order to simulate the processes that may have taken
place in the early Universe and compare theory to data,
various packages were constructed such as CLASS [66] or
CAMB [67], which are widely used as Boltzmann solvers
to compute CMB anisotropies and large-scale structure

3
observables.
When evaluating primordial abundances,
these solvers are typically interfaced with dedicated Big
Bang Nucleosynthesis networks like PArthENoPE [68] or
AlterBBN [69].
For parameter estimation, these codes
are integrated into Bayesian inference frameworks such
as Cobaya [70], which frequently employ nested samplers
like PolyChord [71] or standard Metropolis-Hastings al-
gorithms to explore the cosmological parameter space.
While these highly optimized pipelines work well for stan-
dard ΛCDM parameter estimation or global cosmological
ﬁts, they are mainly dedicated to late-time observables.
Consequently, any arbitrary modiﬁcations to the thermal
history in the MeV era, such as dynamical EDE com-
ponents, goes beyond the scope of the aforementioned
computational frameworks, and require a consistent re-
structuring of their coupled diﬀerential equations.
One of the important problems in Bayesian statistical
analysis is that the conﬁdence intervals of the parame-
ters strongly depend on the adopted priors shapes and
ranges [72–74], a dependence that raises the question if
statistical results can be reported in an unbiased and
convincing way. Even though a prior-free assessment of
conﬁdence is not possible in general [72], approaches that
try to circumvent this problem have been proposed and
analyzed in the literature. One such possibility is based
on the consideration of the R function [72], which factor-
izes the experimental evidence and the prior odds, and
which can be interpreted geometrically as the shape dis-
tortion function of the probability density function. In
[73] it was shown that there is a simple way to obtain
prior-independent constraints by using Bayesian analy-
sis, and by using the R function.
The function R is
extremely useful when considering open likelihoods, that
is, when data only constrain the value of the parame-
ters from below or from above.
The obtained formal-
ism was applied to the case of the analysis of neutrino
mass constraints from cosmology. Bayesian model com-
parison permits to consider the constraints coming from
the diﬀerent models, and to ﬁnd prior-independent and
model-marginalized bounds [73]. A novel method, which
provides robust limits that depend only on the considered
dataset was developed in [74]. It was shown that when
considering several possible cosmological models, and by
interpreting the Bayesian preference by using the Gaus-
sian statistical evidence, the preferred model is least pre-
ferred as compared to the two case model analysis. This
approach was applied to the cosmological neutrino mass
bounds, and for establishing the contribution of relic neu-
trinos to the dark matter density.
It is the main goal of the present investigation to con-
sider the implications of Early Dark Energy cosmological
models on the Big Bang Nucleosynthesis processes, and
to obtain robust observational constraints on the free pa-
rameters of the models. In particular, we analyse four
dark energy models, and we estimate their possible im-
pact on the BBN processes. Firstly, we obtain an esti-
mate of the maximum allowable value of the cosmological
constant in the early Universe consistent with the nucle-
osynthesis data. Our results indicate that a much larger
cosmological constant that presently observed may have
existed in the early Universe, a result that strongly sug-
gests that the cosmological constant may be a dynam-
ical, time dependent quantity. Secondly, we investigate
three distinct dark energy models, described with vary-
ing equations of state. The ﬁrst model assumes a simple
linear equation of state for the dark energy, while in a
second model a polytropic equation of state is assumed.
Finally, we consider a theoretical model in which dark
energy is a temperature dependent quantity.
In order to obtain observational constraints on the
Early Dark Energy models we adopt a direct approach
by focusing primarily on the evolution of the primordial
plasma and light element formation through PRyMordial
[75, 76].
Unlike standard BBN codes which treat
beyond-Standard-Model physics as secondary perturba-
tions, PRyMordial is designed to handle non-standard
thermal histories, allowing for any modiﬁcation to the
Friedmann expansion and weak interaction rates. To ex-
plore the EDE parameter space and compare our the-
oretical predictions with recent astrophysical data, we
couple our modiﬁed nucleosynthesis network to a nested
sampling algorithm. We chose to use nested sampling not
only because it can navigate non-Gaussian posterior dis-
tributions characteristic of dynamic dark energy models,
but also because it computes the exact Bayesian evidence
for the models considered. This allows for a consistent
model comparison between the EDE frameworks consid-
ered in this analysis, namely the cosmological constant
model and varying equation of state models, from linear
to polytropic and temperature-dependent systems, and
the standard BBN scenario.
This paper is organized as follows. In Section II, we
present the Early Dark Energy scenarios considered in
this study, together with the associated modiﬁcations to
the ﬁrst Friedmann equation in each framework. We then
introduce the Big Bang Nucleosynthesis regime in Sec-
tion III, where the computational approach is brieﬂy dis-
cussed along with our strategy for estimating upper limits
on model parameters through nucleosynthesis abundance
ratios. Section IV presents the results of our investiga-
tion, and we conclude in Section V with a statistical and
physical discussion of the best-performing Early Dark
Energy model.
II.
EARLY DARK ENERGY MODELS
In the following Section, we present the Early Dark
Energy models considered in this work, emphasising on
the evolution of the energy density and the speciﬁc equa-
tions of state for each candidate.
We begin by deﬁn-
ing the background evolution of a ﬂat and homoge-
neous Friedmann-Lemaˆıtre-Robertson-Walker (FLRW)
universe and subsequently introduce the modiﬁcations
to the Friedmann equations which arise from the inclu-
sion of an early dark energy component. This framework

4
provides the theoretical basis for calculating the Hubble
parameter, whose deviations will aﬀect the temperatures
relevant to the BBN epoch.
A.
Standard Cosmology with a Cosmological
Constant
In the standard framework, the homogeneous and
isotropic Universe is described by the FLRW metric in
ﬂat Cartesian coordinates,
ds2 = dt2 −a(t)2(dx2 + dy2 + dz2),
(1)
where a(t) is the cosmic scale factor. in the following we
adopt the natural system of units with c = 1. The back-
ground dynamics are then governed by the Friedmann
equations,
3H2(t) = 8πGρ(t) + Λ,
(2)
2 ˙H(t) + 3H2(t) = −8πGp(t) + Λ,
(3)
where H(t) = ˙a(t)/a(t) is the Hubble parameter deﬁning
the cosmic expansion rate, G is the Newtonian gravita-
tional constant, ρ(t) is the total energy density, p(t) is the
total thermodynamic pressure, and Λ is the cosmological
constant.
During the radiation-dominated era of the early Uni-
verse, the total energy density ρ and pressure p are domi-
nated by relativistic species. These scale with the plasma
temperature T through the following relations
ρ(t) = 4σ
c T 4(t),
p(t) = 4σ
3c T 4(t),
(4)
where σ denotes the Stefan-Boltzmann constant.
The
temporal evolution of these components is given by the
standard energy conservation equation,
˙ρ(t) + 3H(t) [ρ(t) + p(t)] = 0.
(5)
B.
Varying (Dynamical) Dark Energy
To explore deviations from the standard regime, we
consider models of dynamical dark energy, in which the
dark energy density is not a constant but is a function of
time. The corresponding modiﬁed Friedmann equations
introduce an eﬀective total density ρeff and eﬀective to-
tal pressure peff, which include the dynamic dark energy
components ρDE(t) and pDE(t),
3H2(t) = 8πG [ρ(t) + ρDE(t)] = 8πGρeff(t),
(6)
2 ˙H(t)+3H2(t) = −8πG [p(t) + pDE(t)] = −8πG
c2 peff(t).
(7)
Assuming the standard relations for the radiation bath
hold, the global energy conservation equation becomes
˙ρeff(t) + 3H(t) [ρeff(t) + peff(t)] = 0.
(8)
Expanding this relation results in the following global
conservation equation
˙ρ(t) + 3H(t) [ρ(t) + p(t)]
+
˙ρDE(t) + 3H(t) [ρDE(t) + pDE(t)] = 0. (9)
For the purposes of this study, we assume a non-
interacting model in which the dark energy component
is minimally coupled to the standard plasma, meaning
there is no direct energy-momentum exchange between
ρDE and the radiation bath. The two components inﬂu-
ence each other only through their cumulative contribu-
tion to the gravitational background, meaning through
the Hubble expansion rate. Consequently, the energy of
the radiation and dark energy components are indepen-
dently conserved
˙ρ(t) + 3H(t) [ρ(t) + p(t)] = 0,
(10)
˙ρDE(t) + 3H(t) [ρDE(t) + pDE(t)] = 0.
(11)
The temporal evolution of the dark energy density is
entirely determined by its assumed equation of state. We
consider three distinct theoretical cases to model this dy-
namical behaviour.
1.
Linear Equation of State
The simplest Early Dark Energy extension of the stan-
dard ΛCDM model is obtained by assuming a linear equa-
tion of state for dark energy, where the pressure of the
dark energy component is strictly proportional to its en-
ergy density through a constant equation of state param-
eter w
pDE(t) = wρDE(t),
(12)
where we speciﬁcally restrict w ∈(−1, 0) to explore the
quintessence regimes. In quintessence models, a slowly
rolling scalar ﬁeld acts as the dynamical dark energy,
which requires a negative pressure that departs from a
constant cosmological constant scenario with w = −1.
Substituting the equation of state into the dark energy
conservation equation gives
˙ρDE(t) + 3(1 + w)H(t)ρDE(t) = 0,
(13)
which integrates to provide the scaling of the dark energy
density with the scale factor of the Universe as
ρDE(t) = ρDE,0a−3(1+w)(t).
(14)
Since we do not directly relate this early dark energy
ﬂuid to late-time cosmological constant values, ρDE,0 is

5
considered an unknown density scale parameter of the
model.
Next, we rewrite the radiation energy density
component as a function of the present-day Cosmic Mi-
crowave Background temperature T0,
ρ0 = 4σ
c T 4
0 ,
(15)
so that we rewrite the radiation energy density compo-
nent as a function of the scale factor a(t) as
ρ(t) =
ρ0
a4(t),
T (t) = T0
a(t).
(16)
The modiﬁed cosmological evolution equation becomes,
3H2(t) = 8πGρ0
a4(t) + 8πGρDE,0
a3(1+w)(t).
(17)
2.
Polytropic Equation of State
Alternatively, we consider a polytropic equation of
state for the Early Dark Energy, a formulation frequently
used to model various physical ﬂuids. The pressure de-
pends non-linearly on the energy density, governed by a
polytropic constant K and an index γ,
pDE(t) = Kργ
DE(t).
(18)
Under this assumption the conservation equation for dark
energy leads to the following relation
˙ρDE(t) + 3H(t) [ρDE(t) + Kργ
DE(t)] = 0,
(19)
from which one can easily obtain
Z
dρDE
ρDE + Kργ
DE
= −3 ln a.
(20)
Substituting u = ρ1−γ
DE , the left-hand side evaluates to
1
1−γ ln(ρ1−γ
DE + K), giving
ρ1−γ
DE + K = ˜C a3(γ−1),
(21)
where ˜C is an integration constant. Setting C = 1/ ˜C
and rearranging, the early dark energy density proﬁle
becomes
ρDE(t) =
a3(γ−1)(t)
C
−K
1/(1−γ)
.
(22)
The corresponding Hubble evolution equation is modiﬁed
as
3H2(t) = 8πGρ0
a4(t) + 8πG
a3(γ−1)(t)
C
−K
1/(1−γ)
. (23)
Rather than treating the polytropic index γ as a con-
tinuous free parameter, we ﬁx it to discrete values, so
that we restrict our analysis to the following cases:
• γ = 4/3 – we consider that the dark energy com-
ponent has a radiation-like equation of state, but
which doesn’t interact with the radiative sector
during the BBN era
• γ = 2 – a stiﬀequation of state causes the dark en-
ergy density to dilute faster than the background
radiation, decaying rapidly to avoid late-time cos-
mological constraints violations.
3.
Temperature-Dependent Equation of State
Finally, we explore a scenario where the dark energy
equation of state evolves with temperature T alongside
the thermal bath of particles,
ρDE(T ) = ρDE,0
 T
T0
3(1+w(T ))
,
(24)
with T0 = 2.7255 K being the present-day CMB temper-
ature. The equation of state is parameterized as follows
pDE = w(T )ρDE,
(25)
for which various functional forms can be assumed. We
impose a linear dependence on temperature, given by a
coupling constant α, that can be expressed as
w(T ) = w0 + αT = w0 + αT0
a ,
(26)
where we take w0 = −1 so that in the limit α →0 we
recover the standard cosmological constant regime.
III.
NUCLEOSYNTHESIS MODELING
We revise in the following Section the Big Bang Nucle-
osynthesis process together with the numerical procedure
used for simulating the formation of abundance ratios fol-
lowing the modiﬁcations of the freeze-out temperature.
We describe the integration of our EDE framework into
the standard BBN reaction network and we discuss the
strategy for numerical estimations of upper bounds. We
perform a Bayesian inference through a nested sampling
technique, which allows us to map the multidimensional
posterior distributions of our model parameters against
observed primordial abundances.
A.
Big Bang Nucleosynthesis Theory
Big Bang Nucleosynthesis describes the production
of the lightest elements such as Hydrogen, Deuterium,
Helium-4, and Lithium-7 during the ﬁrst few minutes of
the Universe, which are highly sensitive to the expansion
rate. In the presence of a dark energy component, the

6
Hubble rate H expressed from the ﬁrst Friedmann equa-
tion is modiﬁed to include the eﬀective energy density,
H(T ) =
r
8πG
3c2 ρeff,
(27)
which evolves in dynamic dark energy models. The ex-
pansion rate competes with the weak interaction rates
Γn↔p, which maintain chemical equilibrium between neu-
trons and protons through the nuclear processes
n + νe →p + e−,
n + e+ →p + ¯νe,
n →p + e−+ ¯νe.
(28)
The weak interaction rate scales approximately as
Γn↔p ∝G2
F T 5 and it decreases as the Universe cools,
reaching the so-called freeze-out regime in which the ex-
pansion rate H(T ) exceeds the interaction rate Γ,
Γn↔p(Tf) ≈H(Tf),
(29)
where Tf represents the freeze-out temperature. Due to
the presence of the EDE component, H(T ) can increase
which determines the freeze-out to occur earlier, corre-
sponding to a higher Tf. The neutron-to-proton ratio at
freeze-out is governed by the Boltzmann factor
n
p

f
= exp

−(mn −mp)c2
kBTf

,
(30)
such that a higher Tf results in a larger (n/p)f ratio,
which subsequently increases the ﬁnal primordial helium
mass fraction, approximately given by
Yp ≈
2(n/p)
1 + (n/p).
(31)
Isotope
Observable
Observed Value SBBN Prediction
Helium-4
Yp
0.245 ± 0.003
0.247 ± 0.0001
Deuterium
D/H ×105
2.527 ± 0.030
2.51 ± 0.11
Helium-3
3He/H ×105
1.1 ± 0.2
1.0 ± 0.1
Lithium-7
7Li/H ×1010
1.6 ± 0.3
4.7 ± 0.7
Table I. Primordial abundances from PDG and Standard
BBN predictions.
This detection of the primordial abundances with high
sensitivity in databases such as the Particle Data Group
[43] (see Table I) allows us to determine strict limits on
the EDE density. In this analysis, the parameter estima-
tion process will rely exclusively on the primordial helium
mass fraction Yp, deuterium and 3He abundance. We ex-
clude Lithium-7 from the χ2 likelihood calculations as the
Lithium problem is highly debated in the literature, since
Standard BBN theory currently predicts a 7Li abundance
approximately three times higher than what is observed
in metal-poor halo stars.
To simulate the synthesis of nuclei in the early Uni-
verse, we develop a program onto the PRyMordial pack-
age [75, 76], which integrates the Boltzmann equations
for primordial nuclear species from a high temperature of
10 MeV to 0.001 keV. The code simultaneously evaluates
the evolution of the cosmic scale factor, baryon num-
ber density, and the distinct thermal baths of photons
and neutrinos, solving at each step a stiﬀsystem of cou-
pled ordinary diﬀerential equations describing both the
rapid thermonuclear reaction networks and the macro-
scopic cooling of the expanding Universe. This cosmolog-
ical state vector describes eﬃciently the Standard Model
phenomena, including incomplete neutrino decoupling
and ﬁnite-temperature quantum electrodynamic eﬀects,
which result in accurate abundance predictions.
The advantage of using PRyMordial is that it con-
tains a New Physics interface that can accommodate
diverse modiﬁcations in the background equations and
plasma sector, coming from various theoretical scenar-
ios. Rather than requiring beyond-Standard-Model ex-
tensions to be deﬁned in terms of predeﬁned parameters,
the code allows for a direct modiﬁcation of the thermo-
dynamic quantities driving the integration. By an ex-
plicit deviation of the Hubble expansion rate or injecting
dynamic energy densities into the plasma, the software
computes from the initial nuclear rates the way in which
these high-energy deformations shift the neutron freeze-
out temperature. It then outputs theoretical predictions
for observable light element results, such as the helium
mass fraction deuterium and Helium-3 abundance ratios,
which are the required quantities that allow for direct
statistical comparison against astrophysical data.
B.
PRyMordial Framework Integration
We embed our modiﬁed Friedmann equations directly
into the PRyMordial diﬀerential equation solver, treating
the EDE contribution as an additional energy density
component in the early Universe background.
The radiation energy density at the present epoch, ρ0,
is a known quantity determined from the Cosmic Mi-
crowave Background measurements of temperature T0 ≈
2.725 K. In contrast, the EDE component ρDE,0 in the
linear case or the constant C in the polytropic case can-
not be directly inferred by observational data, which is
due to the non-interacting nature of the models consid-
ered.
As the dark energy is minimally coupled to the
standard plasma, it evolves independently according to
its own equation of state and because this EDE is a tran-
sient phenomenon, its amplitude is not ﬁxed by late-time
Λ constraints and must be searched for as a free param-
eter.
Consequently, for the cosmological constant model we
search for upper bounds for the early Λ parameter, while
in the case of the linear time-varying model, the density
scale ρDE,0 and the equation of state parameter w are
searched for. In the polytropic model, the model parame-
ters are estimated when γ is ﬁxed to two distinct physical
cases. Finally, in the temperature-dependent model, the
α parameters is also constrained by the BBN primordial

7
abundance data.
We integrate through our model interface to PRyM’s
ODE system an additional dynamic scale factor calcu-
lation from an extended background integration.
The
cumulative temperature mapping as a function of cos-
mic time can introduce the dark sector energy den-
sity described as a function of time into the total en-
ergy density calculation in PRyMordial, which is na-
tively temperature-based. This functionality is needed
as the reparametrization of ρEDE in terms of time re-
quires a recalculation of the scale factor a(t), which be-
comes a dynamical variable in the Friedmann equation.
In practice, the cosmological constant and temperature-
dependent equation of state will not need this recompu-
tation of the scale factor, but the linear and polytropic
models will, as a consequence of altering the background
dynamics through an explicit ρEDE(t) evolution.
Within PRyM/PRyM main.py, the background solver de-
ﬁnes the right-hand side of the ODE system dTtotdt,
and evaluates the PRyMini.dynamical a flag, passed
as a model attribute for each EDE instance.
When
enabled, the state vector contains both the scale fac-
tor, and the corresponding evolution equation, da/dt =
a × Hubble(...), so that the Friedmann term can be
evaluated using this dynamic scale factor. Consequently,
the Hubble function computes the total energy den-
sity and incorporates the EDE contribution through the
PRyMthermo.rho EDE(Tg, a) function.
Conversely, if
the dynamical ﬂag is disabled, the scale factor is not
evolved and ρEDE is inherently treated as independent
of a.
The complete implementation of this modiﬁed
framework is publicly available in the eden repository
(https://github.com/croi900/eden), and the imple-
mentation scheme can be visualized in Fig. 1.
EDE model
dynamical a flag
background ODE
Tg, Tν, (a)
Hubble(...)
If dynamical a:
ρEDE(T, a)
If not:
ρEDE(T )
Figure 1. Integration scheme for the EDE models into the
PRyMoridal package.
The parameter estimation is performed by compar-
ing the theoretical mass fractions generated by the
PRyMordial ODE solver against the observed primor-
dial abundances. This comparison is handled by a log-
likelihood function derived from a χ2-test constructed by
summing the squared residuals of the light element abun-
dances θ, weighted by their respective observational un-
certainties σ,
χ2(θ) =
X
i
(Xi,pred(θ) −Xi,obs)2
σ2
i
(32)
where Xi ∈{Yp, D/H,3 He/H}. The ﬁnal log-likelihood
is expressed as
ln L = −0.5 χ2(θ).
(33)
The resulting samples including the physical parame-
ters, predicted abundances and the corresponding log-
likelihood are recorded iteratively to map the posterior
distribution.
C.
Nested Sampling Algorithm
The statistical challenge in constraining early dark
energy parameters arises because the theoretical abun-
dances converge to SBBN values as the dark energy
contribution vanishes, creating a broad χ2 plateau in
the likelihood function.
Because the simulated results
are highly consistent with observational data, standard
Markov Chain Monte Carlo (MCMC) samplers remain
trapped in this plateau, searching the lower prior vol-
ume without identifying a signiﬁcant upper bound. To
eﬃciently evaluate the posterior distribution for precise
parameter limits, a nested sampling approach is further
applied, as it can eﬃciently search over such plateaus.
In Bayesian processes, we draw inferences regarding a
set of parameters θ for a given model M and observed
data D by relying on Bayes’ theorem,
P(θ|D, M) = L(D|θ, M) π(θ|M)
Z(D|M)
(34)
where P(θ|D, M) is the posterior probability distribu-
tion, L(D|θ, M) is the likelihood function, and π(θ|M) is
the prior probability density.
The denominator, Z(D|M), is called the Bayesian ev-
idence or marginal likelihood, serving as a normalization
constant for the posterior. This quantity is deﬁned as the
integral of the likelihood over the entire prior parameter
space,
Z =
Z
L(θ)π(θ)dθ.
(35)
While the evidence is unnecessary for simple parameter
estimation drawn from standard MCMC methods, it is
the fundamental quantity required for Bayesian model
selection, as two competing models can be compared
through the Bayes factor, K = Z1
Z2 .
When dealing with multi-dimensional systems, the evi-
dence integral becomes increasingly hard to estimate us-
ing standard grid or Monte Carlo integration.
Hence,
the nested sampling technique, introduced in [77, 78],
resolves to this issue by mapping the D-dimensional pa-
rameter space onto a one-dimensional domain deﬁned by
the prior volume X(λ), which is the prior mass X with
likelihoods strictly greater than a threshold λ,
X(λ) =
Z
L(θ)>λ
π(θ)dθ,
(36)

8
ranging from 1 denoting the entire prior volume to 0,
where the likelihood is maximal. The evidence integral
is therefore rewritten as a one-dimensional integral over
the prior volume,
Z =
Z 1
0
L(X)dX,
(37)
evaluated through an algorithm which maintains a col-
lection of N so-called live points drawn from the prior
distribution π(θ):
1. At iteration i, identify the live point θi with the
lowest likelihood, denoted as Li.
2. Remove this point from the active set and record
its coordinates and likelihood.
3. Estimate the shrinkage of the prior volume; on av-
erage, the maximum of N random variables drawn
uniformly from [0, Xi−1] shrinks the volume by a
factor of exp(−1/N), so that Xi ≈exp(−i/N).
4. Compute the weight of the removed point, wi =
Xi−1 −Xi, and add its contribution to the numer-
ical approximation of the evidence Z ≈P Liwi.
5. Sample a new point from the prior distribution, im-
posing the strict constraint that its likelihood must
exceed Li.
The iteration continues until a predeﬁned convergence
criterion is met, when the remaining evidence is a negli-
gibly small fraction of the accumulated evidence Z. As
the sequence of prior volumes Xi is probabilistic, nested
sampling contains a statistical uncertainty given as the
log-evidence, ln(Z). The previously presented algorithm
is implemented eﬃciently in the dynesty package [79],
which allows us to estimate the model parameter’s upper
bounds.
IV.
IMPLEMENTATION AND RESULTS
The computational strategy consists of integrating the
Early Dark Energy models into the PRyMordial nucle-
osynthesis solver with a nested sampling framework to
map the early dark energy parameter space, implemented
in eden framework. To perform the multidimensional pa-
rameter estimation and calculate the Bayesian evidence,
we use the dynesty nested sampling package and for
the subsequent posterior analysis and visualizations we
use the GetDist library. In this section, we summarize
the prior distributions and the resulting statistical con-
straints for EDE models.
A.
The Cosmological Constant Model
To ensure the BBN network is computed within physi-
cal and observational boundaries, we impose informative
Gaussian priors on four parameters, which are included
as external constraints from CMB data. The standard
plasma sector is treated identically across all EDE mod-
els and includes the neutron lifetime τn = 879.4 ± 0.6 s,
the baryon density Ωbh2 = 0.02230 ± 0.00015, and two
nuclear reaction rate uncertainty parameters pnpγ = 0±1
and pdp3Heγ = 0 ± 1, which randomize the helium and
deuterium abundance rates. The latter two are dimen-
sionless parameters that shift the thermonuclear reaction
rates n+p →d+γ and d+p →3He+γ within their experi-
mental uncertainty regions from the NACRE II database,
where p = 0 corresponds to the median rate and p = ±1
to a one-sigma deviation [80].
For the CC model, the dark energy sector contains a
single parameter Λ to which we apply a log-uniform prior
to explore its inﬂuence over multiple orders of magnitude,
log10 Λ ∼U(−20, −4).
(38)
We initialized our prior interval over the above scales
with the aim to obtain a maximally allowed value of the
cosmological constant through the evidence Z estima-
tion, and not a Gaussian posterior. Following the nested
sampling evaluation, the Bayesian evidence for the CC
model was calculated as ln ZCC = −1.2905±0.0441. The
evidence uncertainty indicates that there is less than a 5%
probability of obtaining a value for the logarithm of the
evidence that deviates signiﬁcantly from this estimate.
The marginalized posterior constraints for the dark en-
ergy parameter include the 68% and 95% upper limit,
summarized in Table II. The prior ranges for the cur-
rent and following models are chosen based on the com-
putational limits of PRyMordial. All credible intervals
and upper limits are conditioned by the prior ranges and
forms speciﬁed for each EDE model, inﬂuencing the pos-
terior under those assumptions, which are not frequentist
conﬁdence limits independent of the prior support.
Parameter
68% CI
95% CI
Λ [MeV4]
[4.24 × 10−19, 9.30 × 10−13] 9.41 × 10−12
Table II. Marginalized posterior constraints for the CC model.
While the 68% credible interval provides a measure
of the posterior’s central mass, the 95% upper limit is
the preferred metric for setting hard constraints on the
parameter space. For the CC model, the constraint Λ <
9.41 × 10−12 MeV4 represents a physical geometric limit
of Λ < 4.07 × 10−33 cm−2.
The eﬀects of our upper bound on the cosmological
constant Λ are shown in Fig. 2, which tracks the logarith-
mic evolution of both the scale factor (top panel) and the
Hubble rate (bottom panel) against the standard simula-
tion trend obtained with no New Physics contribution in
PRyMordial. At the 95% conﬁdence limit, the scale fac-
tor deviates from standard radiation-dominated growth,
increasing exponentially faster then SBBN as the cosmo-
logical constant component starts to dominate. This be-

9
haviour is conﬁrmed in the second plot, where the Hub-
ble rate reaches a plateau before the standard limit is
achieved, implying that the Universe enters too early a
vacuum-dominated phase. This behaviour implies that
if Λ were any larger than this limit, the weak interac-
tions will freeze out too early, leading to much higher
neutron-to-proton ratio and therefore absurdly large nu-
clei abundances.
−1
1
3
5
7
log
10
(t
[s])
−10
−8
−6
−4
−2
log
10
(a)
95% CI (Λ
=
9.41
×
10
−12
[MeV
4
])
68% CI (Λ
=
9.30
×
10
−13
[MeV
4
])
SBBN
−1
1
3
5
7
log
10
(t
[s])
−6
−4
−2
0
2
log
10
(H
[s
−1
])
95% CI (Λ
=
9.41
×
10
−12
[MeV
4
])
68% CI (Λ
=
9.30
×
10
−13
[MeV
4
])
SBBN
Figure 2. Evolution of the logarithm of the scale factor and
the Hubble rate aﬀected by the Λ parameter estimated at
an upper limit of 68% and 95% CL, compared to the SBBN
predictions.
We can verify that the obtained limits are numerically
stable by computing the nested sampling diagnostics,
shown in Fig.3. As the algorithm compresses the prior
volume from left to right though −ln X, the number of
live points remains constant initially and then decays as
the sampler narrows the parameter search space. The
normalized likelihood increases fast up to a ﬂat plateau,
representing the parameter space that approaches the
standard limit. The real proof of convergence is the im-
portance weight curve, which forms a single peak at the
beginning of the search and ﬂattens at the end, demon-
strating that the Bayesian evidence was successfully lo-
calized.
To quantify the time dependence of light-element pro-
duction, we show in Fig. 4 the log-log evolution of all
light abundances for the CC model at the 95% upper-
limit parameters. While 4He reaches a plateau quickly
due to its high binding energy relative to the other ele-
0.0
1.5
3.0
4.5
6.0
7.5
9.0
ln X
0
200
400
Live Points
0.0
1.5
3.0
4.5
6.0
7.5
9.0
ln X
0.0
0.4
0.8
Likelihood
(normalized)
0.0
1.5
3.0
4.5
6.0
7.5
9.0
ln X
0.0
0.2
0.4
Importance
Weight PDF
0.0
1.5
3.0
4.5
6.0
7.5
9.0
ln X
0.00
0.15
0.30
Evidence
Figure 3. Statistical summary of the nested sampling for the
CC model.
ments, D, 3He, and 7Li display a peak near log10 t ≃2.4
(t ∼102–103 s) followed by a decay because of a high re-
activity, stabilizing at their relic values. This behaviour
is consistent with the standard abundance evolution, as
no strong distortion exists in the nucleosynthesis process.
2
3
4
5
6
log
10
(t
[s])
−15
−13
−11
−9
−7
−5
−3
−1
log
10
(Abundance)
H
4
He
D
3
He
7
Li
Figure 4. The log-log time evolution of light elements for the
CC model.
Finally, the abundance corner plots in Fig.5 show
nearly identical overlap between our constrained early
dark energy models and the standard BBN bounds. This
behaviour is expected as we searched for an upper limit
rather than claiming a bounded estimation.

10
0.0221
0.0225
Ω
b
h
2
5.1
5.2
5.3
5.4
5.5
7
Li/H
1.03
1.04
1.05
1.06
1.07
3
He/H
2.50
2.55
2.60
D/H
0.2468
0.2470
0.2472
Y
P
0.0223 ± 0.000116
0.2468
0.2472
Y
P
0.247 ± 0.000131
2.5
2.6
D/H
2.54 ± 0.0221
1.04
1.06
3
He/H
1.05 ± 0.00891
5.2
5.4
7
Li/H
5.3 ± 0.0799
SBBN
CC
Figure 5. Nuclear abundances together with Ωbh2 for the CC
model overlaid with SBBN results from PRyMordial.
B.
The Linear EDE Model
The Linear model introduces a dynamic ﬂuid charac-
terized by two free parameters, namely the dark energy
density ρDE,0 and a constant equation of state parameter
w. We restrict w to the quintessence regime and apply
log-uniform and uniform priors, respectively
log10 ρDE,0 ∼U(−30, −2),
(39)
w ∼U(−1, 0).
(40)
The nested sampling evaluation calculated a Bayesian
evidence of ln ZLinear = −2.0065 ± 0.0593, with the re-
sulting posterior constraints for the dynamic dark energy
parameters detailed in Table III.
Parameter
68% CI
95% CI
ρDE,0 [MeV4] [9.42 × 10−29, 4.36 × 10−17] 2.45 × 10−13
w
[−0.918, −0.432]
−0.269
Table III. Marginalized posterior constraints for the Linear
equation of state EDE model.
For the Linear model, the 95% upper limit ρDE,0 <
1.06 × 10−34 cm−2 represents the maximum possible en-
ergy density of the dark sector that could have con-
tributed during the BBN epoch without perturbing the
primordial abundances beyond their observational uncer-
tainties.
As the energy density scales as a−3(1+w), an
equation of state parameter closer to zero would cause
the dark sector’s density to act as pressureless matter.
−1
1
3
5
7
log
10
(t
[s])
−10
−8
−6
−4
−2
0
log
10
(a)
95% CI (ρ
DE,
0
=
2.45
×
10
−13
[MeV
4
], w
=
−0.2687)
68% CI (ρ
DE,
0
=
4.36
×
10
−17
[MeV
4
], w
=
−0.4321)
SBBN
−1
1
3
5
7
log
10
(t
[s])
−6
−4
−2
0
2
4
log
10
(H
[s
−1
])
95% CI (ρ
DE,
0
=
2.45
×
10
−13
[MeV
4
], w
=
−0.2687)
68% CI (ρ
DE,
0
=
4.36
×
10
−17
[MeV
4
], w
=
−0.4321)
SBBN
Figure 6. Evolution of the logarithm of the scale factor and
the Hubble rate aﬀected by the Linear equation of state
model with parameters ρDE,0 and w compared to the SBBN
trends.
0.0
1.5
3.0
4.5
6.0
7.5
9.0
10.5
ln X
0
200
400
Live Points
0.0
1.5
3.0
4.5
6.0
7.5
9.0
10.5
ln X
0.0
0.4
0.8
Likelihood
(normalized)
0.0
1.5
3.0
4.5
6.0
7.5
9.0
10.5
ln X
0.0
0.2
0.4
Importance
Weight PDF
0.0
1.5
3.0
4.5
6.0
7.5
9.0
10.5
ln X
0.00
0.06
0.12
Evidence
Figure 7. Statistical summary of the nested sampling for the
Linear equation of state model.

11
The scale factor and Hubble rate evolution is repre-
sented for the Linear case against the standard observa-
tional limit in Fig. 6. We can observe that as this model
allows for a varying equation of state parameter w, the
dark energy ﬂuid causes a quicker expansion of spacetime
than the CC model, deviating from the standard trend
at the 68% bounds at the time of freezeout. At the 95%
upper limit, the initial density ρDE,0 is high enough to
raise the scale factor above the standard expansion curve,
as the Hubble rate decays toward a higher value than the
standard framework.
We can verify that these two limits obtained for the pa-
rameters are numerically stable by studying the nested
sampling diagnostics in Fig. 7. The same qualitative re-
sult as in the CC model are indicating a clear prior volume
exploration in the initial computing time, followed by a
convergence towards a 95% conﬁdence level upper bound.
Figure 8 shows the abundances over time diagnostic
for the Linear model. The evolutions of D, 3He and 7Li
show no peaks and the synthesis timescale is shortened
due to the stronger coupling of ρEDE(a) to the expansion
history in this model.
For the light elements to form
within the required bounds, a faster synthesis process is
needed, which makes this model not recover the SBBN
behaviour.
Moreover, the abundance corner plots in Fig. 9 show
the same strong overlap between the linear equation of
state EDE model and the standard prediction, again
an expected result since the upper bounds are indicat-
ing tiny contributions minimized through the χ-squared
function.
2
3
log
10
(t
[s])
−16
−13
−10
−7
−4
−1
log
10
(Abundance)
H
4
He
D
3
He
7
Li
Figure 8. The log-log time evolution of light elements for the
Linear model.
C.
The Polytropic EDE Model
In the Polytropic equation of state model, the dark
energy ﬂuid is parameterized to explore two physical be-
0.0221
0.0225
Ω
b
h
2
5.1
5.2
5.3
5.4
5.5
7
Li/H
1.02
1.04
1.06
3
He/H
2.50
2.55
2.60
D/H
0.2468
0.2470
0.2472
Y
P
0.0222 ± 0.000124
0.2468
0.2472
Y
P
0.247 ± 0.00014
2.5
2.6
D/H
2.53 ± 0.0236
1.04
1.06
3
He/H
1.04 ± 0.00913
5.2
5.4
7
Li/H
5.31 ± 0.0828
SBBN
Linear
Figure 9. Nuclear abundances and Ωbh2 for the Linear equa-
tion of state model overlaid with SBBN results from PRy-
Mordial.
haviours, for which the polytropic index γ = 4/3 for a
radiation-like component and γ = 2 for a stiﬀﬂuid. The
ﬂuid is assumed to scale as
ρDE =
a3(γ−1)
C
−K

1
1−γ
,
(41)
so that the behaviour of the ﬂuid is determined by the
competing eﬀects of the expanding scale factor and the
polytropic constant K. In the very early Universe, when
the scale factor a is vanishingly small, the polytropic
pressure term dominates since Kργ
DE ≫ρDE, and the
condition a3(γ−1)/C ≪|K| is naturally satisﬁed,
a3(γ−1)
C
≪|K|
⇒
ρDE ≃(−K)
1
1−γ ,
(42)
resembling a constant energy plateau that behaves like a
cosmological constant. On the other hand, at late times
the scale factor grows and the expansion term dominates,
so that K becomes negligible and the ﬂuid reduces to
pressureless dust diluting as,
a3(γ−1)
C
≫|K|
⇒
ρDE ≃C−1/(1−γ) a−3.
(43)
To optimize numerical stability during nested sampling,
we replace the integration constant C with a scale factor
at, deﬁned at the transition between the dynamic and
constant regimes. Moreover, for a real, positive energy
density the polytropic constant is required to be strictly
negative K < 0. The corresponding density plateau is

12
ρt = |K|1/(1−γ), so that we can eliminate both C and K
from the energy density relation, obtaining
ρDE = ρt
" a
at
3(γ−1)
+ 1
#
1
1−γ
.
(44)
For the above reparameterization we apply log-uniform
priors in wide ranges,
log10 at ∼U(−15, −2),
(45)
log10 ρt ∼U(−20, 5),
(46)
initializing the polytropic index with 4/3 and 2, respec-
tively.
The nested sampling evaluation calculated a Bayesian
evidence of ln ZPoly = −1.5206±0.0538 for the radiation-
like ﬂuid and −1.5248 ± 0.0539 for the stiﬀﬂuid, with
the resulting posterior constraints for the dynamic dark
energy parameters detailed in Table IV.
Parameter
68% CI
95% CI
Polytropic (γ = 4/3)
at
[2.17 × 10−14, 1.05 × 10−5] 1.44 × 10−3
ρt [MeV4] [7.63 × 10−18, 2.52 × 10−2] 2.75 × 104
Polytropic (γ = 2)
at
[1.96 × 10−14, 2.19 × 10−5] 1.42 × 10−3
ρt [MeV4] [1.05 × 10−17, 1.76 × 10−2] 8.13 × 103
Table IV. Marginalized posterior constraints for the Poly-
tropic equation of state EDE models.
The eﬀects of the Polytropic dark energy ﬂuid on
the evolution of the scale factor and Hubble function are
shown in Fig. 10. During the early-time regime where
a ≪at, the dark energy density ρt is constant and domi-
nates the early dynamics causing a rapid evolution of the
scale factor, pushing it signiﬁcantly above the standard
history (top panel). Following the transitory regime, the
evolution trend is similar to the SBBN expansion in terms
of the Hubble rate because both models reduce to pres-
sureless dust diluting as ρDE ∝a−3 at late times (bottom
panel), whereas the scale factor achieves the largest value
among all models. In both radiation and stiﬀ-ﬂuid sce-
narios, the dark component loses its pressure early in the
evolution, meaning both quantities log a(t) and log H(t)
show similar behaviours. Therefore, we present only the
evolution plots for the γ = 4/3 radiation-like ﬂuid as a
representative example.
The results from the two separate runs show similar
transition parameters at and ρt, namely for the radiation-
like regime with 95% upper limits of at < 1.44 × 10−3
and ρt < 2.75 × 104 MeV4, and for the stiﬀﬂuid with
at < 1.42 × 10−3 and ρt < 8.13 × 103 MeV4, therefore we
display in Fig. 11 only the nested sampling diagnostics
for the γ = 2 model. The reason for the similarity in
the model evidence, appears as we search for solutions
close to the SBBN limit through our likelihood function,
which is achieved for small enough contributions for the
Polytropic model, so that the polytropic index doesn’t
modify signiﬁcantly the overall ﬁnal abundances, as it is
seen in Fig. 12.
The two Polytropic models are compared directly in
terms of abundances evolution in Fig. 13, where the solid
and dashed curves correspond to γ = 2 and γ = 4/3,
respectively. For these runs the abundances again freeze
out after a very early shift of the nucleosynthesis epoch
due to the strong ρEDE(a) coupling to the background
temperature, and the ﬁnal relic levels are very similar,
with an only diﬀerence between the two polytropes being
the time to reach the maxima. Based on this analysis, we
can conclude that a stiﬀﬂuid requires an earlier freezeout
to recover the standard yields.
Because the posterior
constraints on the two polytropes are otherwise close,
this time evolution is the only method to separate their
BBN dynamics in the present analysis.
−1
1
3
5
7
log
10
(t
[s])
−10
−8
−6
−4
−2
0
2
log
10
(a)
95% CI (a
t
=
1.42
×
10
−3
, ρ
t
=
8.13
×
10
3
[MeV
4
])
68% CI (a
t
=
2.19
×
10
−5
, ρ
t
=
1.76
×
10
−2
[MeV
4
])
SBBN
−1
1
3
5
7
log
10
(t
[s])
−6
−4
−2
0
2
log
10
(H
[s
−1
])
95% CI (a
t
=
1.42
×
10
−3
, ρ
t
=
8.13
×
10
3
[MeV
4
])
68% CI (a
t
=
2.19
×
10
−5
, ρ
t
=
1.76
×
10
−2
[MeV
4
])
SBBN
Figure 10. Evolution of the logarithm of the scale factor and
the Hubble rate aﬀected by the Polytropic equation of state
for the representative radiation-like ﬂuid (γ = 4/3) with pa-
rameters at and ρt at 95% and 68% CI compared to the SBBN
trends.
D.
The Temperature-dependent EDE Model
For this last model, the equation of state for the dark
energy component is varying with temperature, but still
without any coupling assumed with the plasma sector.

13
0.0
1.5
3.0
4.5
6.0
7.5
9.0
ln X
0
200
400
Live Points
0.0
1.5
3.0
4.5
6.0
7.5
9.0
ln X
0.0
0.4
0.8
Likelihood
(normalized)
0.0
1.5
3.0
4.5
6.0
7.5
9.0
ln X
0.0
0.2
0.4
Importance
Weight PDF
0.0
1.5
3.0
4.5
6.0
7.5
9.0
ln X
0.0
0.1
0.2
Evidence
Figure 11. Statistical summary of the nested sampling for the
Polytropic equation of state model for the stiﬀﬂuid (γ = 2)
polytropic index.
0.0221
0.0225
Ω
b
h
2
5.1
5.2
5.3
5.4
5.5
7
Li/H
1.03
1.04
1.05
1.06
3
He/H
2.50
2.55
2.60
D/H
0.2468
0.2470
0.2472
0.2474
Y
P
0.2468
0.2472
Y
P
2.50
2.55
D/H
1.04
1.06
3
He/H
5.2
5.4
7
Li/H
SBBN
γ
=
4/3
γ
=
2
Figure 12. Nuclear abundances and Ωbh2 for the Polytropic
equation of state with both radiation and stiﬀﬂuid models
overlaid with SBBN results from PRyMordial.
This allows us to write a linear temperature dependence
2
3
×
10
1
4
×
10
1
6
×
10
1
log
10
(t
[s])
−16
−13
−10
−7
−4
−1
log
10
(Abundance)
Model
γ
=
2
γ
=
4/3
Species
H
4
He
D
3
He
7
Li
Figure 13. The log-log time evolution of light elements for
the two Polytropic models.
of the equation of state parameter,
ρDE(T ) = ρDE,0
 T
T0
3(1+w(T ))
,
(47)
w(T ) = −1 + αT,
(48)
where α parameterizes the cosmological model. We ini-
tialize the prior volume by the uniform intervals, which
is suﬃciently low to allow for the existence of physical
abundance ratios and provide upper limits,
log ρT,0 ∼U(−40, −12),
(49)
α ∼U(0, 0.095),
(50)
The results of our simulations indicate that the model
evidence ln ZT = −0.7774 ± 0.0309 is achieved for the
upper limit parameters ρT,0 < 5.17 × 10−14 MeV4 and
α < 0.0886, as shown in Table V.
Parameter
68% CI
95% CI
ρDE,0 [MeV4] [7.13 × 10−36, 6.09 × 10−17] 5.17 × 10−14
α
[1.31 × 10−2, 7.77 × 10−2]
8.86 × 10−2
Table
V.
Marginalized
posterior
constraints
for
the
temperature-dependent equation of state model.
The logarithmic plots in Fig 14 show the smallest de-
viation from the SBBN model as the scale factor doesn’t
increase at scales grater than the standard results, as op-
posed to the other time-dependent/constant models in
which the expansion scale increased due to the modi-
ﬁed background dynamics. In terms of the logarithmic
timescale, this model emphasises a greater contribution
of the dark sector at the very begining of the simulation,
as the energy density is directly proportional to the tem-
perature. This causes the ODE solver to prioritize the

14
very early time domain in the integration, where devia-
tions from the SBBN model are observed, which eventu-
ally fade out as the Universe cools. Therefore, the con-
tribution of this particular model to the nucleosynthesis
process fades as temperature drops, so that all abundance
posteriors are well within the SBBN bounds, visible in
Fig. 16. The summary of the model convergence shows
a similar trend as for the other investigated models, dis-
played in Fig. 15.
Finally, Fig. 17 displays the temperature-dependent
model and the CC case are the only scenarios that re-
cover the standard BBN timescale and the characteristic
maxima in abundances, as opposed to the Linear and
Polytropic models, which shift nucleosynthesis to ear-
lier times.
−7
−5
−3
−1
1
3
5
7
log
10
(t
[s])
−11
−10
−9
−8
−7
−6
log
10
(a)
95% CI (ρ
T,
0
=
5.17
×
10
−14
[MeV
4
], α
=
0.0886)
68% CI (ρ
T,
0
=
6.09
×
10
−17
[MeV
4
], α
=
0.0777)
SBBN
−7
−5
−3
−1
1
3
5
7
log
10
(t
[s])
−7
−5
−3
−1
1
3
5
7
log
10
(H
[s
−1
])
95% CI (ρ
T,
0
=
5.17
×
10
−14
[MeV
4
], α
=
0.0886)
68% CI (ρ
T,
0
=
6.09
×
10
−17
[MeV
4
], α
=
0.0777)
SBBN
Figure 14. Evolution of the logarithm of the scale factor and
the Hubble rate aﬀected by the temperature-dependent equa-
tion of state for the Linear w(T) model, at 95% and 68% CI
compared to the SBBN trends.
V.
DISCUSSIONS AND FINAL REMARKS
In the present work, we studied the inﬂuence of a con-
stant and various dynamical Early Dark Energy models
on the nucleosynthesis process which takes place in the
very early Universe. We incorporated the eﬀects of a cos-
mological constant model, one linear, and two polytropic
time-dependent equation of state models, for which a
radiation-like dark component and a stiﬀﬂuid were con-
0.0
1.5
3.0
4.5
6.0
7.5
9.0
ln X
0
200
400
Live Points
0.0
1.5
3.0
4.5
6.0
7.5
9.0
ln X
0.0
0.4
0.8
Likelihood
(normalized)
0.0
1.5
3.0
4.5
6.0
7.5
9.0
ln X
0.0
0.2
0.4
Importance
Weight PDF
0.0
1.5
3.0
4.5
6.0
7.5
9.0
ln X
0.0
0.2
0.4
Evidence
Figure 15.
Statistical summary of the nested sampling for
the Linear w(T) equation of state model with temperature
dependence.
0.0221
0.0225
Ω
b
h
2
5.1
5.2
5.3
5.4
5.5
7
Li/H
1.03
1.04
1.05
1.06
1.07
3
He/H
2.50
2.55
2.60
D/H
0.2468
0.2470
0.2472
Y
P
0.0223 ± 0.000114
0.2468
0.2472
Y
P
0.247 ± 0.000133
2.5
2.6
D/H
2.54 ± 0.0222
1.04
1.06
3
He/H
1.05 ± 0.00897
5.2
5.4
7
Li/H
5.29 ± 0.08
SBBN
Linear w(T)
Figure 16. Nuclear abundances and Ωbh2 for the temperature-
dependent equation of state compared with the SBBN results
from PRyMordial.
sidered. We also studied the temperature evolution for a
linear equation of state model, by including these modi-
ﬁcations into the background equations of PRyMordial’s
modeling of the ﬁrst Friedmann equation. By using a

15
2
3
4
5
6
log
10
(t
[s])
−15
−13
−11
−9
−7
−5
−3
−1
log
10
(Abundance)
H
4
He
D
3
He
7
Li
Figure 17. The log-log time evolution of light elements for
the LinearT model.
nested sampling technique, we extracted robust poste-
rior constraints and upper limits on the energy densities
of these dark sector, establishing the maximum physical
values allowed before violating observed primordial light
element abundances.
In what follows, we evaluate the proposed Early Dark
Energy models by comparing their statistical perfor-
mance against both the standard Big Bang Nucleosyn-
thesis predictions and each other.
The evidence ex-
tracted from the nested sampling algorithm provides a
suﬃciently robust metric for model selection, hence we
establish the relative preference between models using
the Bayes Factor, expressed logarithmically as ∆ln Z =
ln Zmodel−ln ZCC, where we used the Cosmological Con-
stant model as our baseline as it is the simplest one in
terms of the number of degrees of freedom. According to
the Kass and Raftery scale [81], a diﬀerence |∆ln Z| < 1
indicates that the models are statistically indistinguish-
able, whereas values greater than 3 would suggest strong
evidence in favour of one model over the other. The sta-
tistical properties of our EDE models are summarized in
Table VI, and show nearly equal statistical preference.
Model
ln Z
∆ln Z
Cosmological Constant (Λ)
−1.290 ± 0.044
0.000
Linear (w = const.)
−2.006 ± 0.059 −0.716
Polytropic (γ = 4/3)
−1.521 ± 0.054 −0.231
Polytropic (γ = 2)
−1.525 ± 0.054 −0.235
Linear w(T) (w(T ) = −1 + αT ) −0.774 ± 0.031 +0.516
Table VI. Statistical comparison of the EDE models through
Bayes factors ∆ln Z calculated relative to the cosmological
constant model.
We can visualize the upper limits obtained in terms of
the physical energy scales allowed during the BBN epoch.
In the present-day Universe, observations of the cosmo-
logical constant are constrained to ρΛ,0 ≈10−56 cm−2,
and we can place our early-Universe results in this con-
text by comparing our results in geometric density units,
as summarized in Table VII. It is important to note that
in the Polytropic models, the parameter ρt represents
a transient high-redshift density plateau and in order to
compare it against present-day density parameters we
must account for the ﬂuid’s dilution in the late-time limit.
Because both models analytically reduce to an eﬀective
ρDE ≃ρt(a/at)−3 = ρta3
ta−3, the equivalent present-day
density parameter is expressed as the scaled ratio ρta3
t
in Table VII. Even so, the allowed energy density for
the polytropic models remains several orders of magni-
tude larger than the strict limits placed by the Linear
or Cosmological Constant models.
Model
Density Parameter [MeV4]
[cm−2]
CC
Λ < 9.41 × 10−12
4.07 × 10−33
Linear
ρDE,0 < 2.45 × 10−13
1.06 × 10−34
Polytropic (γ = 4
3) ρta3
t < 8.21 × 10−5
3.55 × 10−26
Polytropic (γ = 2) ρta3
t < 2.33 × 10−5
1.01 × 10−26
Linear w(T)
ρT,0 < 5.17 × 10−14
2.24 × 10−35
Table VII. Upper limits for the energy density scale at 95%
CI across the tested EDE models.
To ensure a consistent
baseline comparison, the polytropic models are expressed via
their equivalent present-day density.
Even though the EDE models cannot be ranked in
terms of Bayesian statistical metrics, the physical via-
bility of these models can be understood based on the
kinematic evolution of the Hubble expansion rate, H(t),
which governs the decoupling of weak interactions and
the neutron-to-proton ratio freeze-out at T ∼1 MeV.
The cosmological constant model represents the most
rigid scenario, being characterized by a non-diluting en-
ergy density which interrupts the natural t−1/2 decay of
the Hubble parameter during radiation domination era
prior to recombination. On the other hand, a dynamic
ﬂuid with a linear, time-dependent equation of state di-
lutes as ρDE ∝a−3(1+w), maintaining a slightly higher
Hubble rate relative to the SBBN background through-
out nucleosynthesis.
The polytropic models introduce a diﬀerent kinematic
evolution as they asymptotically reduce to a pressure-
less dust-like ﬂuid at late times. Their resulting physical
behaviours during nucleosynthesis are practically indis-
tinguishable, causing the 95% upper limit Hubble rate
shows slight deviations from the standard BBN curve
during the weak freeze-out epoch compared to the corre-
sponding stagnation of the H(t) rate experienced at 68%
limit. Finally, the temperature-dependent linear model
w(T ) modiﬁes the background expansion strictly at high
temperatures, but the evolution curves remain identical
to the standard SBBN proﬁle, making it hardly notice-
able in the abundance ratios.

16
The EDE contribution to the background dynamics
indirectly aﬀects the neutrino decoupling mechanism by
altering the total eﬀective number of relativistic species
Neﬀthrough the modiﬁed H(t) evolution, which governs
the coupling between the photon plasma and the three
neutrino species. Using the 95% upper limit EDE param-
eters, the CC and temperature-dependent models, whose
EDE energy density does not depend on the scale fac-
tor evolution, recover the standard Neﬀ≃3.044. The
linear and polytropic models, however, require the scale
factor to be recomputed in the background evolution,
which introduces a tighter coupling between ρEDE and
the expansion rate during neutrino decoupling, resulting
in Neﬀ, Linear ≃3.010, Neﬀ, Poly(γ = 4/3) ≃3.017 and
Neﬀ, Poly(γ = 2) ≃3.015.
The average shift ∆Neﬀ≡
Neﬀ−3.044 ≃−0.03 remains well within observational
bounds, given that current BBN and CMB data con-
strain Neﬀ= 2.898±0.141 at the 2σ level [82], conﬁrming
that the EDE contribution to the expansion rate during
neutrino decoupling does not introduce tension with the
measured radiation content at BBN.
To quantify the divergence from General Relativity, we
deﬁne the fractional diﬀerence in cosmic time evaluated
for the photon temperature Tγ as (tGR −tEDE)/tGR. We
perform a model parameter evaluation at the 95% upper
limit for each EDE model, and we make the distinction
between a positive cosmic time ratio, which indicates the
EDE universe reaches a speciﬁc temperature sooner than
the GR limit, and a negative ratio, which conversely, sig-
nals that the expansion history is behind the GR base-
line. By plotting this as a function of Tγ from the hot
BBN onset at 10 MeV toward lower values, we display
the eﬀect of the energy density of the dark sector on the
time evolution in Fig. 18.
10
−3
10
−2
10
−1
10
0
10
1
T
γ
[MeV]
0.0
0.2
0.4
0.6
0.8
1.0
(t
GR
−
t
EDE
)/t
GR
(95% UL EDE vs SBBN)
CC
Linea)
Polyt)opic (γ
=
2)
Polyt)o(ic (γ
=
4/3)
Linea)T
Figure 18. Deviations of the relative time diﬀerence of GR
and EDE models as a function of photon temperature for each
cosmological model considered.
The results show that all EDE models, besides the
temperature-dependent equation of state, start from a
zero deviation from the GR limit at high temperatures,
which indicates that the EDE eﬀects contribute grad-
ually to the total energy density of the background as
time passes. Only the LinearT model representing the
temperature-dependent equation of state starts with a
maximum value associated with the highest temperature,
which then rapidly dilutes as the Universe cools down.
For the Linear and Polytropic equation of state of
the dark components, the relative cosmic time diﬀerence
increases sharply, so that by the time of weak freeze-
out at Tγ ≈0.5 MeV, the relative diﬀerence stabilizes
at the maximally allowed deviation. This is an expected
behaviour reﬂecting the cumulative temporal shift eval-
uated at our 95% upper limit constraints.
For the CC model, we observe a rapid increase in time
deviation from GR only at much lower temperatures,
Tγ ≲10−2 MeV, approaching the nucleosynthesis regime.
This late-time deviation occurs because the cosmological
constant does not dilute, hence as the background radia-
tion energy density drops proportionally to T 4, the con-
stant CC energy density eventually becomes a signiﬁcant
fraction of the total energy of the Universe, modifying the
expansion rate. Similarly, a secondary relative increase
happens in the temperature-based LinearT model, where
at low temperatures, the energy density stops from dilut-
ing as rapidly as the Universe cools, causing it to behave
as a cosmological constant at later times.
Although SBBN predictions are in good agreement
with primordial abundance observations, EDE models
are frequently used to resolve the H0 tension, which
would require a higher early-time Hubble parameter to
reduce the physical comoving sound horizon at recombi-
nation,
rs =
Z ∞
zrec
cs(z)
H(z)dz.
(51)
It should be noted that the scope of the present work
is strictly limited to the nucleosynthesis epoch and the
resulting primordial abundances as simulated by the
PRyMordial framework. While our results provide a nec-
essary validation for early dark energy sectors motivated
by the Hubble tension, we do not explicitly integrate the
sound horizon rs, or perform a full cosmic microwave
background likelihood analysis. Instead, we establish the
maximum allowed limits these ﬂuids can reach without
violating current nuclei data.
Finally, although our analysis targeted only early-time
nucleosynthesis data and lacks a late-time constraining
solution, the viability of an Early Dark Energy model
depends on its capacity to balance both epochs. From
this qualitative perspective, the temperature-dependent
equation of state LinearT emerges as the best candidate
among our models, as it allows for signiﬁcant modiﬁca-
tions to the expansion history at extreme temperatures,
while rapidly diluting its energy density to align with
the General Relativity limit during the weak freeze-out
era Tγ ≈0.5 MeV. Importantly, among all models, the
LinearT and CC are the only scenarios that correctly pre-
dict the BBN timescale and evolution for nucleosynthesis.
Supported by a slight statistical preference in our
Bayesian selection ∆ln Z = +0.516 and its theoret-

17
ical ability to re-emerge as a cosmological constant
at very low temperatures, the temperature-dependent
model manages to eﬃciently satisfy the strict bounds of
primordial element formation, which makes it a physical
scenario worth studying in future works.
VI.
ACKNOWLEDGMENTS
We would like to thank the anonymous referee for com-
ments and suggestions that helped us to signiﬁcantly im-
prove our work.
[1] A. G. Riess et al., Observational Evidence from Super-
novae for an Accelerating Universe and a Cosmological
Constant, Astron. J., 116, 1009, (1998).
[2] S. Perlmutter et al., Measurements of Ωand Λ from
42 High Redshift Supernovae, Astrophys. J., 517, 565,
(1999).
[3] N. Aghanim et al., (Planck Collaboration), Planck 2018
results. VI. Cosmological parameters, Astron. Astrophys.
641, A6 (2020).
[4] S. Alam et al., Completed SDSS-IV extended Baryon Os-
cillation Spectroscopic Survey: Cosmological implications
from two decades of spectroscopic surveys at the Apache
Point Observatory, Phys. Rev. D, 103, 083533, (2021).
[5] A. G. Adame et al. (DESI), DESI 2024 VI: cosmologi-
cal constraints from the measurements of baryon acoustic
oscillations, JCAP 02, 021 (2025).
[6] M. Abdul Karim et al. (DESI), DESI DR2 Results
II: Measurements of Baryon Acoustic Oscillations and
Cosmological Constraints, Phys. Rev. D, 112, 083515,
(2025).
[7] E. Calabrese et al. (ACT), The Atacama Cosmology Tele-
scope: DR6 Constraints on Extended Cosmological Mod-
els, JCAP, 2025, 063, (2025).
[8] T.-N. Li, G.-H. Du, S.-H. Zhou, Y.-H. Li, J.-F. Zhang,
and X. Zhang, Robust evidence for dynamical dark energy
in light of DESI DR2 and joint ACT, SPT, and Planck
data, Physics of the Dark Universe 52, 102254 (2026).
[9] S. Capozziello, H. Chaudhary, T. Harko,and G.Mustafa,
Is dark energy dynamical in the DESI era?
A critical
review, Physics of the Dark Universe 51, 102196 (2026).
[10] E. Di Valentino et al., In the realm of the Hubble tension-
a review of solutions, Class. Quant. Grav., 38, 153001,
(2021).
[11] N. Sch¨oneberg et al., The H0 Olympics: A fair ranking
of proposed models, Phys. Rept., 984, 1, (2022).
[12] C. Wetterich, Phenomenology of early dark energy, Phys.
Lett. B 594, 17 (2004).
[13] M. Doran and J. Robbers, Early dark energy cosmologies,
JCAP 06, 026 (2006).
[14] V. Pettorino, L. Amendola, and C. Wetterich, How early
is early dark energy?, Phys. Rev. D 87, 083009 (2013).
[15] T. Karwal and M. Kamionkowski, Dark energy at early
times, the Hubble parameter, and the string axiverse,
Phys. Rev. D, 94, 103523, (2016).
[16] V.
Poulin,
T.
L.
Smith,
T.
Karwal,
and
M.
Kamionkowski, Early Dark Energy Can Resolve The
Hubble Tension, Phys. Rev. Lett., 122, 22, (2019).
[17] M.-X. Lin, G. Benevento, W. Hu, and M. Raveri, Acous-
tic Dark Energy:
Potential Conversion of the Hubble
Tension, Phys. Rev. D, 100, 063542, (2019).
[18] F. Niedermann and M. S. Sloth, New Early Dark Energy,
Phys. Rev. D, 103, 043504, (2021).
[19] P. Agrawal, F.-Y. Cyr-Racine, D. Pinner, and L. Randall,
Rock ’n’ roll solutions to the Hubble tension, Phys. Dark
Univ., 42, 101347, (2023).
[20] M. Kamionkowski and A. G. Riess, The Hubble Tension
and Early Dark Energy, Ann. Rev. Nucl. Part. Sci., 73,
1, (2023).
[21] V. Poulin, T. L. Smith, and T. Karwal, The Ups and
Downs of Early Dark Energy solutions to the Hubble ten-
sion:
A review of models, hints and constraints circa
2023, Phys. Dark Univ., 42, 101348, (2023).
[22] S. Nojiri, S. D. Odintsov, and V. K. Oikonomou, Modiﬁed
Gravity Theories on a Nutshell: Inﬂation, Bounce and
Late-time Evolution, Phys. Rept., 692, 1, (2017).
[23] Y. Cai, S. Capozziello, M. De Laurentis, and E. N. Sari-
dakis, f(T) teleparallel gravity and cosmology, Rept. Prog.
Phys., 79, 106901, (2016).
[24] M. Braglia, M. Ballardini, F. Finelli, and K. Koyama,
Early modiﬁed gravity in light of the H0 tension and LSS
data, Phys. Rev. D, 103, 043528, (2021).
[25] G. Franco Abell´an et al., Probing early modiﬁcation of
gravity with Planck, ACT and SPT, JCAP, 12, 017,
(2023).
[26] M.
Najaﬁ
et
al.,
When
Dark
Energy
Turns
On:
Constraints on a Critical Emergence Model,
arXiv,
2603.13137, (2026).
[27] J. Kochappan et al., Observational evidence for early
dark energy as a uniﬁed explanation for cosmic birefrin-
gence and the Hubble tension, Phys. Rev. D, 112, 063562
(2025).
[28] L. Yin, G.-H. Du, T.-N. Li, and X. Zhang, Joint
constraints on cosmic birefringence and early dark en-
ergy
from ACT, Planck,
DESI, and PantheonPlus,
arXiv:2601.13624 (2026).
[29] K. Lodha et al., Extended dark energy analysis using
DESI DR2 BAO measurements, Phys. Rev. D 112,
083511 (2025).
[30] E. Chaussidon et al., Early time solution as an alterna-
tive to the late time evolving dark energy with DESI DR2
BAO, Phys. Rev. D 112, 063548 (2025).
[31] F. J. Qu, K. M. Surrao, B. Bolliet, J. C. Hill, B. D.
Sherwin, and H. T. Jense, Accelerated inference on accel-
erated cosmic expansion: New constraints on axionlike
early dark energy with DESI BAO and ACT DR6 CMB
lensing, Phys. Rev. D 111, 123507 (2025).
[32] H.
Wang and
Y.-S. Piao,
Dark energy
after
pre-
recombination early dark energy in light of DESI DR2
and the latest ACT and SPT data, arXiv:2511.16606
(2025).
[33] R. A. Alpher, H. Bethe, and G. Gamow, The Origin of
Chemical Elements, Phys. Rev., 73, 7, (1948).
[34] C. Copi, D. Schramm, M. Turner, Big-bang nucleosynthe-
sis and the baryon density of the universe, Science 5195,
192 (1995).
[35] J. P. Kneller, Gary Steigman, BBN for pedestrians, New
J. Phys. 6, 117 (2004).

18
[36] B. D. Fields, K. A. Olive, Big bang nucleosynthesis, Nu-
clear Physics A 777, 208 (2006).
[37] G. Steigman, Primordial Nucleosynthesis in the Preci-
sion Cosmology Era, Annu. Rev. Nucl. Part. Sci. 57, 463
(2007).
[38] R. H. Cyburt, B. D. Fields, K. A. Olive, and T.-H. Yeh,
Big Bang Nucleosynthesis, Rev. Mod. Phys., 88, 015004,
(2016).
[39] R. J. Cooke, M. Pettini, and C. C. Steidel, One Percent
Determination of the Primordial Deuterium Abundance,
Astrophys. J. 855, 102 (2018).
[40] E. Aver et al., Improving helium abundance determina-
tions with Leo P as a case study, JCAP 03, 027 (2021).
[41] B. D. Fields, K. A. Olive, T.-H. Yeh, and C. Young,
Big-Bang Nucleosynthesis after Planck, JCAP, 03, 010,
(2020).
[42] R. Allahverdi et al., The First Three Seconds: a Review
of Possible Expansion Histories of the Early Universe,
Open J. Astrophys., 4(1), 1, (2021).
[43] S. Navas et al. (Particle Data Group), Phys. Rev. D 110,
030001, (2024).
[44] B. D. Fields, The primordial lithium problem, Ann. Rev.
Nucl. Part. Sci., 61, 47, (2011).
[45] D. I. Santiago, D. Kalligas, and C. W. F. Everitt,
Constraints on the scalar-tensor theories of gravitation
from primordial nucleosynthesis, Phys. Rev. D 54, 3750
(1996).
[46] A. Coc, K. A. Olive, J.-P. Uzan, and E. Vangioni, Big
bang nucleosynthesis constraints on scalar-tensor theories
of gravity, Phys. Rev. D 73, 083525 (2006).
[47] J. Alvey, N. Sabti, M. Escudero, and M. Fairbairn, Im-
proved BBN constraints on the variation of the gravita-
tional constant, Eur. Phys. J. C 80, 148 (2020).
[48] S. Bhattacharjee, P. K. Sahoo, Big bang nucleosynthesis
and entropy evolution in f(R, T ) gravity, Eur. Phys. J.
Plus 135, 350 (2020).
[49] S. Capozziello, G. Lambiase, and E. N. Saridakis, Con-
straining f(T) teleparallel gravity by Big Bang Nucleosyn-
thesis, Eur. Phys. J. C 77, 576 (2017).
[50] S. Bhattacharjee and P. K. Sahoo, Big Bang Nucleosyn-
thesis constraints on f(T,T) gravity, Phys. Lett. B 849,
138391 (2024).
[51] D. F. P. Cruz, D. S. Pereira, F. S. N. Lobo, and J. P. Mi-
moso, Big Bang Nucleosynthesis constraints on f(T, Lm)
gravity, arXiv:2509.20309 (2025).
[52] M. Kusakabe, S. Koh, K. S. Kim, and M.-K. Cheoun,
Constraints on modiﬁed Gauss-Bonnet gravity during big
bang nucleosynthesis, Phys. Rev. D 93, 043511 (2016).
[53] M. H¨og˚as, F. Torsello, and E. M¨ortsell, Constraints on
bimetric gravity from Big Bang nucleosynthesis, JCAP
08, 001 (2021).
[54] T. M. Matei, C. Croitoru, and T. Harko, Big Bang Nucle-
osynthesis constraints on the cosmological evolution in a
Universe with a Weylian Boundary, The European Phys-
ical Journal C 85, 1092 (2025).
[55] T. M. Matei, C. A. Croitoru, and T. Harko, Big Bang
Nucleosynthesis constraints on space-time noncommuta-
tivity, Eur. Phys. J. C 85, 11 (2025).
[56] C. Cook, et al., Constraints on Modiﬁed Gravitational
Couplings During the MeV Era, Phys. Rev. D 109,
083512 (2024).
[57] P. Braat,
J. de
Vries,
J. Groot,
J. Y. G¨unther,
and
J.
Klari´c,
Big
Bang
Nucleosynthesis
and
the
Neutrino-Extended Standard Model Eﬀective Field The-
ory, arXiv:2602.12745 (2026).
[58] D.
Kirilova,
Big
Bang
Nucleosynthesis
Constraints
and Indications for Beyond Standard Model Neutrino
Physics, Symmetry 16, 53 (2024).
[59] P. F. Depta, M. Hufnagel, and K. Schmidt-Hoberg,
Big Bang Nucleosynthesis constraints on resonant DM
annihilations, Journal of Cosmology and Astroparticle
Physics 2025, 02, 032 (2025).
[60] A. Omar and A. Ritz, BBN Constraints on the Hadronic
Annihilation of sub-GeV Dark Matter, Phys. Rev. D 113,
035004 (2026).
[61] T. H. Jung, T. Okui, K. Tobioka, and J. Wang, New
Bounds on Heavy QCD Axions from Big Bang Nucle-
osynthesis, Phys. Rev. D 113, 055002 (2026).
[62] J. A. Kable, S. Gallagher, R. Hloˇzek, and A. MacInnis,
Sound Horizon Independent Constraints on Early Dark
Energy: The Role of Supernova Data, arXiv:2403.11916
(2024).
[63] D. McKeen and A. Omar, Early dark energy during big
bang nucleosynthesis, Phys. Rev. D 110, 103514 (2024).
[64] C. Cook and J. Meyers, Insights for Early Dark Energy
with Big Bang Nucleosynthesis, arXiv:2512.11163 (2025).
[65] O. Seto and T. Toda,
Constraints on the varying
electron mass and early dark energy in light of ACT
DR6 and DESI DR2 and the implications for inﬂation,
arXiv:2508.09025 (2025).
[66] D. Blas, J. Lesgourgues, and T. Tram, The Cosmic Lin-
ear Anisotropy Solving System (CLASS) II: Approxima-
tion schemes, JCAP 07, 034 (2011).
[67] A. Lewis, A. Challinor, and A. Lasenby, Eﬃcient compu-
tation of CMB anisotropies in closed FRW models, As-
trophys. J. 538, 473 (2000).
[68] O. Pisanti, A. Cirillo, S. Esposito, F. Iocco, G. Mangano,
G. Miele, and P. D. Serpico, PArthENoPE: Public Algo-
rithm Evaluating the Nucleosynthesis of Primordial Ele-
ments, Comput. Phys. Commun. 178, 956 (2008).
[69] A. Arbey, J. Auﬃnger, K. P. Hickerson, and E. S.
Jenssen, AlterBBN v2: A public code for calculating Big-
Bang nucleosynthesis constraints in alternative cosmolo-
gies, Comput. Phys. Commun. 248, 106982 (2020).
[70] J. Torrado and A. Lewis, Cobaya:
code for Bayesian
analysis of hierarchical physical models, JCAP 05, 057
(2021).
[71] W. J. Handley, M. P. Hobson, and A. N. Lasenby, poly-
CHORD: next-generation nested sampling, Mon. Not.
Roy. Astron. Soc. 453, 4384 (2015).
[72] G. D’Agostini, Conﬁdence limits: what is the problem?
Is there the solution?, Contribution to the Workshop on
Conﬁdence Limits, CERN, Geneva, 17-18 January 2000,
arXiv:hep-ex/0002055 (2000).
[73] S. Gariazzo, Constraining power of open likelihoods,
made prior-independent, The European Physical Journal
C 80, 552 (2020).
[74] S. Gariazzo and O. Mena, Cosmology-marginalized ap-
proaches in Bayesian model comparison: The neutrino
mass as a case study, Phys. Rev. D 99, 021301 (2019).
[75] C. Pitrou, A. Coc, J. P. Uzan and E. Vangioni, PRyMor-
dial: a Python software for Primordial Nucleosynthesis,
Monthly Notices of the Royal Astronomical Society 515,
2, 2465-2482, (2022).
[76] A.-K. Burns, T. M. P. Tait, and M. Valli, PRyMordial:
the ﬁrst three minutes, within and beyond the standard
model, Eur. Phys. J. C 84, 86 (2024).

19
[77] J. Skilling, Nested Sampling, Bayesian Analysis 1, 4, 833-
859, (2006).
[78] G. Ashton et al., Nested sampling for physical scientists,
Nature Reviews Methods Primers 2, 39, (2022).
[79] J. S. Speagle, dynesty: a dynamic nested sampling pack-
age for estimating Bayesian posteriors and evidences,
Mon. Not. R. Astron. Soc. 493, 3, 3132-3158 (2020).
[80] Y. Xu, K. Takahashi, S. Goriely, M. Arnould, M.
Ohta, H. Utsunomiya, NACRE II: an update of the
NACRE compilation of charged-particle-induced ther-
monuclear reaction rates for nuclei with mass number
A¡16, Nuclear Physics A 918, 61-169 (2013).
[81] R. E. Kass and A. E. Raftery, Bayes Factors, Journal of
the American Statistical Association 90, 430, (1995).
[82] T.-H. Yeh, J. Shelton, K. A. Olive and B. D. Fields, Prob-
ing Physics Beyond the Standard Model:
Limits from
BBN and the CMB Independently and Combined, JCAP,
10, 046, (2022).
