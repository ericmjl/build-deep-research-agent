---
title: "Sequence heterogeneity and the dynamics of molecular motors"
authors: "Yariv Kafri, David R. Nelson"
year: 2005
source: arxiv
source_id: "cond-mat/0506797"
url: "http://arxiv.org/abs/cond-mat/0506797v1"
domain: computational-biology
---
arXiv:cond-mat/0506797v1  [cond-mat.stat-mech]  30 Jun 2005
Sequence heterogeneity and the dynamics of
molecular motors
Yariv Kafri∗† and David R. Nelson‡
† Physicochimie Curie (CNRS-UMR168), Institut Curie, Section de Recherche, 26
rue d’Ulm 75248 Paris Cedex 05, France
‡ Department of Physics, Harvard University, Cambridge, MA 02138
Abstract.
The eﬀect of sequence heterogeneity on the dynamics of molecular motors
is reviewed and analyzed using a set of recently introduced lattice models. First, we
review results for the inﬂuence of heterogenous tracks such as a single-strand of DNA
or RNA on the dynamics of the motors. We stress how the predicted behavior might be
observed experimentally in anomalous drift and diﬀusion of motors over a wide range of
parameters near the stall force and discuss the extreme limit of strongly biased motors
with one-way hopping. We then consider the dynamics in an environment containing
a variety of diﬀerent fuels which supply chemical energy for the motor motion, either
on a heterogeneous or on a periodic track. The results for motion along a periodic
track are relevant to kinesin motors in a solution with a mixture of diﬀerent nucleotide
triphosphate fuel sources.

Sequence heterogeneity and the dynamics of molecular motors
2
1. Introduction
The study of molecular motors has been transformed in recent years with the increasing
use of single molecule experiments [1, 2]. In one key experiment an external force is
applied to a molecular motor opposing its motion [3, 4, 5, 6]. Typically, as the force is
increased, the velocity of the motor decreases until it is completely stalled. The behavior
of the velocity as a function of force provides much information on the chemical cycle
underlying the motion of the motor. For example, the stall force is a direct estimate of
the force exerted by the molecular motor. The experiments have also motivated much
theoretical work on the dynamics of the motors [7, 8, 9, 10]. Fitting the experimentally
obtained velocity-force curves allows extraction of detailed information on the chemical
cycle of the motor [11, 12, 13].
Most theoretical studies have focused on motors which move on featureless, or
periodic linear tracks [7, 8, 9, 11, 12, 13]. Such a description would be appropriate,
for example, for kinesin which moves along a microtubule ﬁlament, which is periodic,
using only ATP for its motion [14, 15]. However, in many cases the assumption of a
periodic medium fails. Examples of motors which move on heterogeneous tracks include
RNA polymerase [4, 5] which moves along DNA, ribosomes which move along mRNA,
helicases [16, 17] which unwind DNA, exonucleases [18, 19] which turn double-stranded
DNA into single-stranded DNA and many others. All these motors move along tracks
which are inherently “disordered” or heterogeneous due to the underlying sequence of the
linear template. Theoretically, molecular motors moving along disordered tracks have
received much less attention [20, 21, 22]. Another form of heterogeneity which has largely
been ignored arises from the diﬀerent chemical fuels which may be used by molecular
motors to move along the track. For example, RNA polymerase uses diﬀerent nucleotide
triphosphates (NTP’s) which build the mRNA it produces, each supplying a diﬀerent
amount of chemical energy, to move along a DNA strand. A diﬀerent “annealed” form
of disorder (in contrast to the “quenched” disorder embodied in a particular nucleotide
sequence) can be present even in molecular motors moving along perfectly periodic
tracks in a solution containing several distinct types of chemical fuels. For example,
it is known that kinesin can move using other nucleotide triphosphates (such as GTP)
instead of ATP, albeit less eﬃciently [23, 24, 25].
Recently, we have introduced a simpliﬁed model for molecular motors which allows
the eﬀects of disorder to be studied in considerable detail [21]. We have focused so far on
heterogeneous tracks and argued that near the stall force the dynamics of the motor is
strongly aﬀected by the heterogeneity embodied in a particular DNA or RNA sequence.
Due to the “sequence disorder” on which the motor is moving (many DNA sequences
have only short range correlations [26]) the displacement of the motor as a function
of time ceases to be linear in time close enough to the stall force. The displacement
becomes sublinear in time, growing as tµ, with µ varying continuously from 1 to 0 as the
stall force is approached. As discussed below there are also anomalies in the diﬀusive
spreading about the average motor position which extend even further below the stall

Sequence heterogeneity and the dynamics of molecular motors
3
force.
In this paper we review some of these results, stressing several experiments which
could be performed to test the predictions of the model. We also explore the eﬀect
of heterogeneous fuels on the motion of molecular motors.
In [21] it was suggested
that inhomogeneous fuel concentrations could enhance signiﬁcantly the regime near the
stall force over which anomalous dynamics is observed.
Here we study this type of
disorder numerically and illustrate the dramatic eﬀect of varying the concentrations of
the diﬀerent fuels used to power the motor. For motors moving along heterogeneous
tracks we also discuss the dynamics in the extreme limit where detailed balance is
violated and motors never take backward steps. Finally, we consider motors moving
along a periodic substrate powered by diﬀerent kinds of fuels. We discuss, for simple
cases, the expected velocity of the motor as the relative proportion of two diﬀerent
types of fuel in the solution is varied. The behavior of more complicated models is also
discussed.
2. The Model
In this section we deﬁne the model used throughout the paper.
We start with a
special case of the general class of n-state models explored by Kolomeisky and Fisher
[11, 12, 13, 27] and consider a “minimal” motor with only two internal states. This
simpliﬁed model reproduces important features of previously studied systems and allows
us to explore generic behavior in new situations in a minimal form. The model is easily
generalized to account for heterogeneous fuels and tracks. When appropriate, we will
mention how results are modiﬁed for general n-state models.
The model has been
introduced and studied in detail in [21] and here we only review its basic properties.
We begin by assuming a perfectly periodic substrate.
The location along the one-
dimensional track, x, is assumed to take a discrete set of values xm, where m = 0, 1, 2 . . .
labels distinct a and b sites. Although not essential, we assume for simplicity that the
distances between xm+1 −xm and xm+2 −xm+1 are equal and set xm+2 −xm = 2a0,
which is the size of a step taken by the motor after completing a chemical cycle such as
hydrolysis of ATP. In general, as discussed in [11], the distance traveled by the motor
between internal states may be diﬀerent for diﬀerent internal transitions. However, we do
not expect such modiﬁcations to aﬀect the long time behavior over a range of parameters
near the stall force. The dynamics embodied in the model is shown schematically in
Fig. 1. Internal states labeled by a have an energy ε = 0 while internal states labeled
by b have a higher energy ε = ∆ε. The local detailed balance condition (in temperature
units such that kB = 1) is satisﬁed by our choice of rate constants,
w→
a = (αe∆µ/T + ω)e−∆ε/T−f/2T
w←
b = (α + ω)ef/2T
w←
a = (α′e∆µ/T + ω′)e−∆ε/T+f/2T
(1)
w→
b = (α′ + ω′)e−f/2T .

Sequence heterogeneity and the dynamics of molecular motors
4
ε
0
1
2
3
4
5





∆ε
a
w
a
w
b
w
b
w
N
2a0
a
b
a
a
b
b
Figure 1. Graphical representation of a simpliﬁed lattice model for molecular motors
and the relevant rates w→
a , w←
a , w→
b , w←
b
and energy diﬀerence ∆ε. The distinct even
and odd sublattices are denoted by a and b respectively.
Following Ref. [7], there are two parallel channels for the motion. The ﬁrst, represented
by contributions containing α and α′, arise from utilization of chemical energy biased
by a chemical potential diﬀerence ∆µ between, say ATP and the products of hydrolysis
ADP and Pi.
The second channel, represented by the terms containing ω and ω′,
correspond to thermal transitions unassisted by the chemical energy. We assume that
the externally applied force F biases the motion in a particularly simple way (consistent
with detailed balance) and deﬁne f = Fa0. If the substrate lacks inversion symmetry
(a necessary condition for directed motion, driven by ∆µ, when f = 0 [7]), we have
α′̸ = α and ω′̸ = ω. If the fuel is ATP, the chemical potential diﬀerence which drives
the motion is [14]
∆µ = T

ln

[ATP]
[ADP][Pi]

−ln

[ATP]eq
[ADP]eq[Pi]eq

,
(2)
where the square brackets [. . .] denote concentrations under experimental conditions and
the brackets [. . .]eq denote the corresponding concentrations at equilibrium.
The rate constants in Eq. 1 deﬁne a set of diﬀerential equations for the probability
Pn(t) of being at site n at time t. For odd n one has
dPn(t)
dt
= w→
a Pn−1(t) + w←
a Pn+1(t) −(w→
b + w←
b )Pn(t) ,
(3)
while for even n
dPn(t)
dt
= w→
b Pn−1(t) + w←
b Pn+1(t) −(w→
a + w←
a )Pn(t) .
(4)
It is illuminating, especially when we consider rate constants which depend on the
position along a heterogenous track, to study two limits of these equations.
In the
ﬁrst the chemical potential diﬀerence ∆µ and the applied force f are small compared
to the energy diﬀerence ∆ε so that b states relax quickly compared to a states. This
condition implies that (w→
b + w←
b ) ≫(w→
a + w←
a ) so that in the long time-limit to a
good approximation the left hand side of Eq. 3 may be set to zero. Upon solving for
Pn(t) with n odd and substituting into Eq. 4, we obtain diﬀerential equations just for
the even sites
dPn(t)
dt
= w←
b w←
a Pn+2(t) + w→
b w→
a Pn−2(t) −(w→
b w→
a + w←
b w←
a )Pn(t)
(w→
b + w←
b )
,

Sequence heterogeneity and the dynamics of molecular motors
5
(n even) .
(5)
Similarly in the limit ∆µ ≫∆ε (with f near the stall force) the motor spends most if
its time in b states. Now, in the long time-limit to a good approximation the left hand
side of Eq. 4 may be set to zero. The remaining diﬀerential equations for the odd sites
read
dPn(t)
dt
= w←
b w←
a Pn+2(t) + w→
b w→
a Pn−2(t) −(w→
b w→
a + w←
b w←
a )Pn(t)
(w→
a + w←
a )
,
(n odd) .
(6)
Note that in both limits the dynamics of the motors on long-times can be described
by a random walker moving on an eﬀective energy landscape associated with what
is in general a non-equilibrium dynamics.
Upon absorbing the denominator factors
(w→
a + w←
a ) and (w→
b + w←
b ) into a rescaling of the rate constants in the numerator,
the eﬀective energy landscape can be read oﬀfrom Eq. 5 or Eq. 6. One ﬁnds that the
eﬀective energy diﬀerence between two sites which are two monomers apart is given by
En+2 −En ≡∆E = T ln
w←
a w←
b
w→
a w→
b

.
(7)
For a periodic track, this leads to a tilted energy landscape (with tilt controlled by
∆µ and f) and an eﬀective energy diﬀerence between 2m-adjacent monomers 2m∆E.
The tilted energy landscape leads to diﬀusion with drift on long time-scales and large
length-scales. The eﬀective energy landscape can also be obtained by assuming detailed
balance and equating the rate asymmetry between two neighboring even sites to an
eﬀective energy diﬀerence ∆E. It is straightforward to verify from Eq. 7 with Eq. 1
that for a periodic substrate no net motion is generated when the external force f = 0
and the chemical potential diﬀerence ∆µ = 0. Also, when there is directional symmetry
in the transition rates, α = α′, ω = ω′, and f = 0 no net motion is generated even when
∆µ̸ = 0. Absent this symmetry, chemical energy can be converted to motion. These
conditions are equivalent to those presented in [7, 10] for continuum models and are
exhibited here in a minimal model. The eﬀect of the externally applied force is simply
to bias the motion of the motor in the direction in which it is applied.
The velocity for a motor moving along a periodic track in the two limits discussed
above can be obtained by taking the continuum limit and yields v = (w→
a w→
b
−
w←
a w←
b )/(w→
b + w←
b ) for the limit speciﬁed by Eq. 5 and v = (w→
a w→
b −w←
a w←
b )/(w→
a +
w←
a ) for the limit speciﬁed by Eq.
6.
More generally, for periodic rates, it is
straightforward to calcualte the velocity, for example using Bloch eigenfunctions |k⟩∼
eikx and expanding the eigenvalues in the wavevector k.
The linear term gives the
velocity and the quadratic part the eﬀective diﬀusion constant. For the velocity one
ﬁnds
v =
w→
a w→
b −w←
a w←
b
w→
a + w→
b + w←
a + w←
b
.
(8)
An alternative to studying the solution of the equations, which will be very useful
throughout this paper, is to use Monte-Carlo simulations. The rates speciﬁed in Eq.

Sequence heterogeneity and the dynamics of molecular motors
6
(1) can be simulated using the following procedure: To make the simulation eﬃcient we
ﬁrst normalize the entering or leaving rates for a site so that the largest one is unity.
Then, at each step we choose with equal probability attempting to move the motor
to the right or left on the lattice. Following this choice a random number is drawn
from a uniform distribution in the interval [0, 1]. The motor is moved in the chosen
direction provided the random number is smaller than the corresponding rate. Thus, if
a motor ﬁnds itself on site a in Fig. 1 and w→
a > w←
a , w→
b , w←
b is the largest rate it will
(after the rescaling) move one step to the right with probability 1/2, one step to the left
with probability 1/2 (w←
a /w→
a ) and it will stay put with probability 1/2[1 −(w←
a /w→
a )].
Note that the probability of actually moving one step (right or left) to the b-sublattice
during a particular attempt is 1/2[1 + (w←
a /w→
a )]. Once the b-sublattice is reached the
procedure is repeated with the rates w→
b
and w←
b
(note that the probabilities are still
obtained by dividing by w→
a ). To compare, for example, velocities for diﬀerent choices
of rates the overall number of attempts is rescaled at the end by the fastest rate (taken
to be w→
a in the above example). The same procedure is followed for both homogeneous
and heterogeneous tracks. For the latter the largest rate is chosen from all possible
hopping rates along the track. This protocol ensures relaxation to equilibrium in the
absence of chemical or mechanics driving forces [28].
In [21] we have analyzed in detail the motion of the model when the track is not
periodic. Such tracks arise naturally, for example, for motors such as RNA polymerase
or helicases which move on DNA which has a well deﬁned sequence. In this case the
energy diﬀerence ∆E(m) now becomes an explicit function of the location m along the
track, due to the dependance of the rates on the location on the track.
To understand the energy which arises for heterogeneous tracks consider the
“integrating out” procedure applied to the three sites shown in Fig. 2, where three
distinct motor binding energies, E1, E2 and E3, are indicated explicitly. We work in the
limit ∆µ ≫∆E, with ∆E = E1 −E2 or ∆E = E3 −E2, and f close to the stall force,
so that the approximation leading to Eq. 6 (“integrating out” site 2) is appropriate. As
rates for the heterogeneous cluster shown in Fig. 2, we take
w→
a (13) = [α(13)e∆µ(13)/T + ω(13)]e−(E2−E1)/T−f/2T
w←
b (13) = [α(13) + ω(13)]ef/2T
w←
a (13) = [α′(13)e∆µ(13)/T + ω′(13)]e−(E2−E3)/T+f/2T
(9)
w→
b (13) = [α′(13) + ω′(13)]e−f/2T .
where the arguments “(13)” appended to the w’s, α’s,α′’s, ω’s and ω′’s simply mean
that these are the heterogenous rates appropriate to the cluster 1 −2 −3. These rates
obey detailed balance conditions for the two channels, and have a similar dependence
on ∆µ(13) and f and various energy diﬀerences as the rates in Eq. 1. The notation
∆µ(13) indicates that the chemical potential diﬀerence could depend on which NTP
(in the case of RNA polymerase) provides the energy for that particular step. Upon

Sequence heterogeneity and the dynamics of molecular motors
7
ε
0
1
2
3
4





a
w
a
w
b
w
N
2a0
b
a
b
b
w
E
E
E
1
3
2
Figure 2. The transition rates and energy levels of three sites, spanning two monomers
corresponding to a motor moving along a heterogenous track. Note that E1̸ = E3 due
to the non-periodicity of the track. The transition rates now depend explicitly on the
location along the track. To avoid cluttering this dependence was suppressed in the
ﬁgure.
assuming fast relaxation of site 2 in Fig. 2, from a formula similar to Eq. 7,
∆E13 = E3 −E1 + 2f −T ln
(α(13)e∆µ/T + ω(13))(α′(13) + ω′(13))
(α′(13)e∆µ/T + ω′(13))(α(13) + ω(13))

,
≡E3 −E1 + 2f + η13
(10)
Eq.
10 illustrates the following important points, applicable to motor molecules on
heterogenous tracks more generally: (a) if ∆µ(13) = 0, then E13 = E3 −E1 +2f, with a
similar formula for all neighboring pairs of odd sites. Thus, in the absence of chemical
energy, we have a “random energy landscape” with bounded energy ﬂuctuations; (b)
if α(13) = α′(13) and ω(13) = ω′(13) (inversion symmetry), chemical energy does
not lead to net motion between sites 1 and 3, as discussed above; (c) in general,
∆E13 = E3 −E1 + 2f + η13, where η13 is a random function of position along the
heterogeneous track. Upon passing to a coarse-grained position η(m), where m is the
position along the track we see that the eﬀective ‘coarse grained’ energy diﬀerence
between two points m1 and m2 = m1 + m which are m-monomers apart is given by
Pm1+m
m′=m1 η(m′). The landscape itself behaves like a random walk with ﬂuctuations which
grow as √m, corresponding to a random-forcing energy landscape (for RNA polymerase,
the diﬀerent chemical potentials of the nucleotides in the transcript also contribute to
a random forcing landscape [21]).
The self-similar structure of the random force landscape leads to interesting
dynamics near the stall force.
As the stall force is approached the dynamics slows
down and becomes dominated by motion between deep minima of the energy landscape
[29].
The minima correspond to speciﬁc locations along the track where the motor
tends to pause. The distribution of dwell times at these minima, P(τ), averaged over

Sequence heterogeneity and the dynamics of molecular motors
8
the diﬀerent locations on the track, is expected to behave as τ −(1+µ), where µ (not
to be confused with a chemical potential!) is related to the force, ﬂuctuations in the
eﬀective energy landscape and temperature. For random forcing energy landscape where
the energy diﬀerence between two points is drawn from a Gaussian distribution with a
variance V = η(m)2, where the overline denotes an average along the sequence, one can
show that [29]
µ(f) = 2T|∆Ef=0 −2f|/V ,
(11)
where ∆Ef=0 is the mean slope of the potential (averaged along the sequence) at zero
force. The exponent µ thus decreases continuously to zero as f increases toward the
stall force of the motor (deﬁned by µ(fs) ≡0). For more general distributions of the
eﬀective energy diﬀerence the value of µ might be diﬀerent from Eq. 11 by factors of
order unity.
Near the stall force the expected distribution of pause times becomes broader as µ
becomes closer to 0. The dynamics of the motors are altered from diﬀusion with drift
when the pause-time distribution becomes very broad. The dynamics then depends on
the numerical value of µ deﬁned in Eq. 11 [21, 22, 29]:
• µ < 1 – Around the stall force, both the drift and diﬀusive behavior of the motor
become anomalous. The displacement of the motor as a function of time increases
as tµ. Thus, in this region the velocity is undeﬁned, in the sense that it depends
on the experimental observation time, tE, through v ∼tµ−1
E
. Moreover, the spread
of the probability distribution of the motor about its mean position also behaves
anomalously with a variance which grows as t2µ
E . Experimentally, for a given tE,
this anomaly should lead to a convex velocity as a function of force curve in the
vicinity of the stall force. The curve will become more and more convex as tE is
increased; the velocity actually vanishes for a range of f’s near the stall force in
the limit tE →∞.
• 1 < µ < 2 – Further away from the stall force the displacement of the motor as a
function of time grows linearly. At long-times the velocity becomes independent of
the averaging window. However, the variance of the probability distribution around
the mean is anomalous and grows as t2/µ
E .
• µ > 2 – Far below the stall force both the displacement and the variance of the
probability distribution around the mean grow linearly in time, as in conventional
diﬀusion with drift.
These results can easily be shown to apply as well to general n-state models.
Moreover, it can be argued that even if several parallel channels exist for moving from
one monomer to another the results are also qualitatively unchanged [21].
Experimentally, the predictions of the model can be tested by measuring the
displacement of the motor as a function of time, averaged over diﬀerent experimental
runs (and, possibly, sequences). Each time trace of the motor position will have an
irregular shape due to pauses, which will increase in duration as the stall force is

Sequence heterogeneity and the dynamics of molecular motors
9
approached, at speciﬁc locations along the track. However, averaged over many time
traces (or sequences) the expected displacement will grows as tµ with µ < 1 close enough
to the stall force.
Note that if one averages over time traces for a ﬁxed sequence,
the displacement is expected to grow as s(t)tµ where s(t) has ﬂuctuations of order
unity, because the sequence information is not completely erased in this case.
An
alternative experimental test would be to measure the distribution of dwell times P(τ).
Because P(τ) ∼1/τ 1+µ for large τ, the distribution becomes wider as the stall force is
approached. Monitoring P(τ) has the advantage of probing the wide distribution even
in regimes which are not very close to the stall force.
We now consider limiting cases of the above model on heterogeneous tracks. These
illustrate a number of interesting features and suggest ways in which the anomalous
dynamics might be observed experimentally.
We will also use the model to explore
heterogeneous chemical energy sources for motors on a periodic track. This situation
may be realized in motors such as kinesin which can use several types of chemical
energy to move along the track. From the two state model described above we deduce
the expected behavior of the velocity as the relative proportions of the diﬀerent fuels is
varied and mention generalizations to more general n-state models.
3. Strongly biased motors
In this section we study motors moving on a heterogeneous substrate in the limit where
one of the transition rates is strongly biased in a certain direction. An extreme limit
occurs when one of the transition rates, in, say, the backward direction, is zero. Although
this limit violates detailed balance, it could be a reasonable approximation for certain
strongly biased experiments. One such model is a special case of the two state model
discussed in Section 2:
w→
a = (αe∆µ/T + ω)e−∆ε/T−f/2T
w←
b = (α + ω)ef/2T
w←
a = ω′ e−∆ε/T+f/2T
(12)
w→
b = ω′ e−f/2T .
Here we have set α′ = 0 so that in the ∆µ ≫T limit the motor will be strongly biased
to move towards the right. Physically, this situation corresponds to a motor which can
use chemical energy only to move in a certain direction. (We expect qualitatively similar
results for a wide variety of strongly biased “one way” models). Next, we assume an
extremely strong bias ∆µ ≫T limit of the model such that αe∆µ/T is very large but
α and ω are so small that w←
b
can be set to be zero. This limit only makes sense far
from the stall force. The stall force of a model with w←
b = 0 (as any other model were
one of the reactions is assumed to be unidirectional) is inﬁnite: The eﬀective energy
landscape, Eq. 7, which describes the dynamics of such a limit has an inﬁnite slope. In
this section we will compare numerically trajectories when w←
b = 0 and when w←
b̸ = 0.

Sequence heterogeneity and the dynamics of molecular motors
10
0.0
5.0x10
7
1.0x10
8
1.5x10
8
2.0x10
8
0
2000
4000
6000
8000
0.0
5.0x10
7
1.0x10
8
1.5x10
8
2.0x10
8
0
50
100
150
200
250
300


x
t(MCS)
 f/T=6.0
 f/T=7.0


x
t(MCS)
 f/T=2.0
 f/T=4.0
 f/T=6.0
 f/T=7.0


Figure 3. Sample trajectories obtained on a heterogeneous track using the model
with w←
b
= 0 for various values of the reduced force f/T . The lower the trajectory the
higher the opposing force. Here we took with equal probability α = 5, ω = 1, ω′ = 2
and α = 0.2, ω = 1, ω′ = 1. In both cases ∆ε = 0 and e∆µ/T = 500. In the inset the
two largest values of the force are presneted in more detail.
Using Eq.
11, the inﬁnite slope of the eﬀective energy landscape implies that
µ = ∞> 2, so that the dynamics is diﬀusion with drift. The linear drift is illustrated
clearly in Fig. 3 where trajectories of the strongly biased model are shown for diﬀerent
forces. Note that even for very large forces the displacement of the motor as a function
of time grows linearly. It can be shown that the dwell time distribution on the track
decays exponentially P(τ) ∼e−τ/τ ∗in contrast to the power law distribution expected
when w←
b̸
= 0. To observe any signiﬁcant pausing clearly one must have f ≃∆µ (see
inset of Fig. 3). In this limit, however, w←
a ≳w→
a , and backwards motion cannot be
neglected (see Eq. 12).
In Fig. 4 we show the very diﬀerent behavior of simulations where we take the
back hopping to be non-zero. Now we do not neglect ω and the backward hopping
rate w←
b
is nonzero!
For forces near the stall force the displacement of the motor
as a function of time seems to saturate even for a trajectory generated by a single
numerical experiment for a particular sequence. Such a behavior is consistent with that
expected from a sublinear displacement of the motor. Note, however, that with the
exception of the largest force, all curves on long enough time scales are expected to
yield, after an average over many thermal realizations, an asymptotically linear curve
(see the corresponding values of µ presented in the ﬁgure). However, even for these

Sequence heterogeneity and the dynamics of molecular motors
11
0.0
5.0x10
7
1.0x10
8
1.5x10
8
2.0x10
8
0
500
1000
1500
2000
2500
3000
3500
4000


x
t(MCS)
 f/T=2.1
 f/T=2.2
 f/T=2.3
 f/T=2.4
 f/T=2.5
Figure 4. Trajectories obtained using the model of Eq. 12 with w←
b
= (α + ω)ef/2T
and w→
a
= (αe∆µ/T + ω)e−∆ε/T −f/2T .
The lower the trajectory the higher the
resisting force.
Here we took with equal probability α = 5, ω = 1, ω′ = 2 and
α = 0.2, ω = 1, ω′ = 1 along the heterogeneous track. In both cases ∆ε = 0 and
e∆µ/T = 500. Anomalous displacement occur for f/T > 2.47 while anomalous diﬀusion
occurs for f/T > 2.38. The stall force is fs = 2.62.
curves, pausing is pronounced despite the fact that for small resisting forces the motor
rarely moves backwards.
4. Eﬀect of heterogeneous fuel concentrations for a motor moving along a
heterogeneous substrate
For some molecular motors the type of fuel which is used to move depends on the speciﬁc
site along the track.
For example, in the case of RNA polymerase, which produces
messenger RNA, the energy from the hydrolysis of the speciﬁc NTP which is added to
the mRNA chain is used for motion. While a random forcing energy landscape would
exist even if the chemical energy released from every NTP were the same (see Sec. 2),
the diﬀerent chemical energies enhance the variance of the slopes, V , of the random
forcing energy landscape (due to the diﬀerent chemical potentials of the nucleotides in
the transcript). This in turn (see Eq. 11) lowers the value of µ as compared to the case
of equal chemical energies.
As suggested in [21] the variance V could be further increased by increasing the
concentration diﬀerence between the diﬀerent NTPs in the solution.
In an extreme

Sequence heterogeneity and the dynamics of molecular motors
12
situation, where one of the NTPs is completely removed from the solution, the motor
will stall at speciﬁc locations where the NTP is needed. This trick is used in experiments
to synchronize and control the motion of RNA polymerases [30]. In this section we
illustrate using the simple model, Eq. 1, the eﬀects of changing NTP concentrations
on motor motion. Although we work within a “minimal model” we expect the same
eﬀects for more complicated models of molecular motors with many internal states (for
an example of such a model for RNA polymerase see [31]).
To this end, we studied motors which can use two kinds of fuels depending on its
location along the track. We hold the concentration of one fuel ﬁxed and lower the
concentration of the other by reducing the chemical potential associated with it. For
reference we also study the case when the fuels have equal chemical potentials. Fig.
5 displays results of numerical simulations of the model deﬁned by Eq. (12). Similar
results were obtained with the more general model of Eq. (1). We show simulations with
f/T = 0 and when for one fuel e∆µ/T = 500 and for the other e∆µ/T = 500, 50 or 5. From
a generalization of Eq. 2, we see that this latter variation corresponds to a change of two
orders of magnitude in the concentration of the second fuel [14]. As can be seen from
Fig. 5, the eﬀect of reducing one of the chemical potentials is to slow down the motion.
However, note that for all fuel concentrations the motor displacement as a function of
time is linear with these parameter values. Since at zero applied force one expects the
motor always to be biased preferentially in a given direction which is independent of the
monomer this behavior will hold even for larger diﬀerences in concentration.
The change in concentration of one of the fuels can make the regime of anomalous
dynamics much larger. In Fig. 6 we show the result of applying a force which opposes
the motion of the motors on the dynamics.
As can be easily seen from the ﬁgure,
the velocity of the motors is, of course, lower in comparison to that when no force
is applied. However, note that the motion of the curve with the largest diﬀerence in
chemical potential (barely visible at the bottom) is very diﬀerent. The motor almost
immediately stalls after it starts moving. This example illustrates clearly how changing
the concentrations of the diﬀerent fuels can make the regime of anomalous dynamics easy
to access at lower forces. In fact, averaged over many thermal and sequence realizations,
the curve with the largest diﬀerence in chemical potentials shows a displacement of the
motor which grows sublinearly in time, indicating that µ < 1.
5. Heterogeneous fuels on periodic tracks
In this section we consider a molecular motor which is moving along a periodic track
in a solution which contains more than one type of molecule which can supply it with
chemical energy. The situation arises for kinesin in the presence of both ATP and, say,
GTP. It is known that, while less eﬃcient, alternative NTP molecules can also be used by
kinesin to move along the track [23, 24, 25]. We consider, for simplicity, a solution with
two types of chemical fuels within the simple two state model (The analysis presented
can easily be generalized to include additional fuel types). In addition, we generalize

Sequence heterogeneity and the dynamics of molecular motors
13
0
1x10
7
2x10
7
3x10
7
4x10
7
0
1000
2000
3000
4000
5000
6000


f/T=0
x
t(MCS)
 500, 5
 500, 50
 500, 500
Figure 5. Motor trajectories obtained using the model deﬁned by Eq. (12). Here,
substrate heterogeneity is incorporated by taking with equal probability {α = 5, ω =
1, ω′ = 2} and {α = 0.2, ω = 1, ω′ = 1}. The corresponding values of e∆µ/T for the two
diﬀerent fuels are denoted in the box. In both cases ∆ε/T = 0 and f/T = 0. Lower
trajectories correspond to a larger diﬀerence in the chemical potentials associated with
the fuels.
our model to treat two separate cases. In the ﬁrst we assume that the internal states
of the motor (i.e., the a and b sites in Fig. 1) are independent of the fuel used so that
the chemical fuels are only used to move between states with fuel-dependent potential
diﬀerences driving the changes. This situation arises when the fuel from the motor is
used and released so quickly that the motor is unbound to the fuel in the “excited”
internal state. In this case the fuel binding to the motor does not deﬁne an internal
state. In the second case we study we allow for additional internal states of the motor,
depending on which type of chemical fuel is bound to it. This situation arises when
internal “excited” states include a fuel bound to the motor. Since the motor bound to the
two fuels deﬁnes two distinct internal states, a direct thermal transition between them
is therefore not possible. While both cases discussed below involve parallel pathways
for transitions across a monomer, they are distinct in the type of internal states.
5.1. Case I: Internal states of the motors are independent of the chemical fuel
This case amounts to a straightforward generalization of the rates in Eq. 1 to allow
for multiple fuels. As mentioned above, we assume the internal states of the motor are
independent of the chemical energy and that chemical energy is only used to assist the

Sequence heterogeneity and the dynamics of molecular motors
14
0
1x10
7
2x10
7
3x10
7
4x10
7
0
200
400
600
800
1000
1200
1400
1600
1800
2000
2200
2400
2600
2800
3000


x
t(MCS)
 500, 5
500, 50
500, 500
f/T=1
Figure 6. Motor trajectories obtained using the model Eq. (12) with an opposing
force. We again took with equal probability {α = 5, ω = 1, ω′ = 2} and {α = 0.2, ω =
1, ω′ = 1}, with the corresponding values of e∆µ/T for the two diﬀerent fuels as
indicated in the ﬁgure. In both cases ∆ε/T = 0 and f/T = 1. Lower trajectories
correspond to a larger diﬀerence in the chemical potential diﬀerences.
transitions. With two diﬀerent chemical fuels, the generalized rates entering Eqs. 3 and
Eq. 4 are now
w→
a = (α1e∆µ1/T + α2e∆µ2/T + ω)e−∆ε/T−f/2T
w←
b = (α1 + α2 + ω)ef/2T
w←
a = (α′
1e∆µ1/T + α′
2e∆µ2/T + ω′)e−∆ε/T+f/2T
(13)
w→
b = (α′
1 + α′
2 + ω′)e−f/2T .
There are now three parallel paths, two assisted by chemical energy, one thermal. The
subscript 1 or 2 refers to whether fuel “1” or “2” is being used for the transition.
Standard relations for the chemical potential diﬀerence [14] imply that e∆µi/T grows
linearly with the concentration of fuel “i” (see Eq. 2). Because the extra channel is
present, when one of the chemical potential diﬀerences is set to zero the model reduces
to the single motor model but with modiﬁed rates as compared to a motor in a solution
where the fuel is completely absent. For example, if ∆µ2 = 0 the model can be written
in terms of Eq. 1 with the identiﬁcations ω →ω + α2 and ω′ →ω′ + α′
2. Note also
that, in contrast to disordered tracks where the motion of the motor is described by
a random walker moving on a random force landscape, here the energy landscape is
periodic except for a well deﬁned tilt given by Eq. 7.

Sequence heterogeneity and the dynamics of molecular motors
15
With the help of Eq.
8, it is straightforward to verify that for this model the
velocity takes the form
v = A + B[x1] + B′[x2]
C + D[x1] + D′[x2] ,
(14)
where [x1] and [x2] are the concentrations of fuel 1 and 2 respectively and
A, B, B′, C, D, D′ are complicated functions of the the coeﬃcients in Eq.
13.
The
velocity thus varies as ratio of two polynomials, each depending linearly on the
concentration of both fuels. Consider, for example, the velocity in an experiment where
one of the fuels is held at constant concentration and the concentration of the other
is varied. The external force is set to f = 0; (varying f did not aﬀect the qualitative
features discussed below). As shown in Fig. 7, the average velocity smoothly crosses
over from a small value to a larger value in a sigmoidal fashion as the concentration of
more energy rich fuel (“fuel 1”) is increased. Note that ∆µ1/T varies logarithmically
with the concentration of fuel number 1 [14]. Thus, the concentration of fuel “1” varies
over many orders of magnitude for the range of ∆µ1/T shown in Fig. 7. In typical
experiments, only a small portion of this crossover may be visible. For small ∆µ1/T,
motor movement is controlled by fuel “2” while for large ∆µ1/T it is controlled by fuel
“1”. An analogous plot for motor velocity vs. ∆µ1/T when fuel 2 is absent entirely is
shown for reference in Fig. 8. As expected, the velocity no longer exhibits a sigmoidal
crossover between two regimes.
5.2. Case II: Internal states of the motors are coupled to the chemical fuel
Next, we consider a diﬀerent model incorporating two fuels. We now assume that the
type of fuel molecule used to move the motor determines the entire chemical cycle which
leads the motor to move across one monomer. An example might be the n = 2 motor
landscape shown in Fig. 1 where one step (e.g.; a site →b site) involves the fuel molecule
binding to the motor. In this case the entire sequence of transitions would be dictated
by the fuel that is used. Thus, the choice of rates (either in the forward or backward
direction) would be dictated by the initial step which is chosen at random, depending
on the type of fuel utilized.
Since the state of the motor is directly coupled to the chemical fuel, a pure thermal
transition between the states is not possible (unless it involves moving across the
monomer through parallel pathways not related to the motor, an eﬀect which is ignored
here). The new feature is that the motor can move across a monomer by choosing one
of two distinct chemical pathways. This is in contrast to the model deﬁned by Eq. 13
where two distinct chemical pathways exist for passing between the internal states of the
motor, but where the transition across the monomer can occur via a mixture diﬀerent
chemical (or thermal) pathways.
An example for such a model, where each fuel is modeled by a distinct channel
which is a special case of the two state model deﬁned by (1) is given by:
w→
a = αe∆µ1/T−f/2T

Sequence heterogeneity and the dynamics of molecular motors
16
0
2
4
6
8
10
0.15
0.16
0.17
0.18
0.19
0.20
0.21
0.22


v
1
Figure 7.
The velocity as a function of the chemical potential diﬀerence ∆µ1/T
of fuel “1”.
The velocity is plotted in units where is size of a monomer (i.e., the
lattice constant 2a0 in Fig. 1) is set to be one and arbitrary time units. We used
a “nearly one way model” based on Eq.
13 where the rates were chosen to be
α1 = 5, α2 = 2, α′
1 = 0.01, α′
2 = 0.02, ω = 0.01, ω′ = 0.2 in arbitrary units of inverse
time and ∆µ2/T = 5, f = 0, ∆ε = 0. For reference the velocity of with only fuel of
type “2” with the same value of ∆µ2/T is v = 0.195.
w←
b = αef/2T
w←
a = ω ef/2T
(15)
w→
b = ω e−f/2T ,
for the ﬁrst channel and
u→
a = γe∆µ2/T−f/2T
u←
b = γef/2T
u←
a = ν ef/2T
(16)
u→
b = ν e−f/2T .
for the second channel. The fuel concentrations enter through the chemical potential
diﬀerences ∆µ1 and ∆µ2 (see Eq. 2). The relative fuel abundances therefore control the
ratio of the rates w→
a and u→
a . The model will be realized physically in a motor which
binds a fuel and uses its chemical energy in the transitions w→
a or u→
a . The transitions
w→
b
and u→
b
involve the release of the corresponding fuel. Here for simplicity we have
set the energy diﬀerence between the states to be zero and neglected parallel thermal
channels. We do not expect the qualitative results described below to be aﬀected by

Sequence heterogeneity and the dynamics of molecular motors
17
0
2
4
6
8
10
0.00
0.04
0.08
0.12
0.16
0.20


v
1
Figure 8. The velocity in arbitrary time units as a function of the chemical potential
diﬀerence ∆µ1/T where the other chemical channel associated with fuel “2” is closed.
The velocity is plotted in units where is size of a monomer is set to be one. The rates
were chosen to be α1 = 5, α2 = 0, α′
1 = 0.01, α′
2 = 0.0, ω = 0.01, ω′ = 0.2, f = 0 in
arbitrary units of inverse time and ∆ε = 0.
such complications.
The velocity of the model can be calculated in a straightforward manner and is
found to be
v =
(u→
b + u←
b )(w→
a w→
b −w←
a w←
b ) + (w→
b + w←
b )(u→
a u→
b −u←
a u←
b )
(u→
b + u←
b )(w→
b + w←
b ) + (u→
b + u←
b )(w→
a + w←
a ) + (u→
a + u←
a )(w→
b + w←
b ) .(17)
Note that as in Case I, the velocity behaves as a ratio of two polynomials which are
linear in the e∆µi/T, and hence with each of the fuel concentrations (similar to Eq. 14).
Also similar is the fact that the presence of a second channel alters the velocity even
when one of the chemical potential diﬀerence is zero. Again, due to the presence of the
second channel the velocity is lower than that of the motor in the presence of a single
fuel. We do not present plots of the resulting velocity as the concentration of one of
the fuels is varied since the qualitative features are similar to those presented in the
previous subsection.
Finally, we comment that more complicated scenarios (for example, the existence of
additional parallel pathways, or more general n-state models) might change the explicit
dependence on the concentrations of the fuels. However, we expect a general form of a
ratio of two polynomials in the concentrations of the fuels even in much more complicated
scenarios. Indeed, with a speciﬁc experiment in mind and some structural information

Sequence heterogeneity and the dynamics of molecular motors
18
on the motor one might be able to use such experiments, coupled with an analysis
similar to that presented above, to deduce the number of steps in the chemical cycle
which depend explicitly on the fuel concentration. For example, we have considered
models where the internal states are independent of the chemical fuel and found that
the general velocity can be a ratio of polynomials of a degree which is related to the
number of steps which depend on the chemical fuel. However, the detailed results were
very dependent on the choice of rates made.
Acknowledgments: We are very grateful to D. K. Lubensky for many stimulating
conversations and the collaboration which led to references [21] and [22]. We also thank
L. Bau, M. D. Wang and K. C. Neuman for useful conversations and J. Gelles and N.
Guydosh for interesting us in the problem of diﬀerent fuels for kinesin on periodic tracks
like microtubules. D.R.N was supported by the National Science Foundation through
Grant No. DMR-0231631 and the Harvard Materials Research Laboratory via Grant
No. DMR-0213805. Y.K was supported by the Human Frontiers Science Program.
∗Permanent address: Department of Physics, Technion, Haifa 32000, Israel.
[1] C. Bustamante, Z. Bryant and S. B. Smith, Nature, 42, 423 (2003).
[2] C. Bustamante, J. C. Macosko, G. J. L. Wuite, Nature Reviews of Molecular Cell Biology, 1, 130
(2000).
[3] K. Visscher, M. J. Schnitzer and S. M. Block, Nature, 400, 184 (1999).
[4] R. J. Davenport, G. J. L. Wuite, R. Landick and C. Bustamante, Science 287, 2497 (2000).
[5] M. D. Wang, M. J. Schnitzer, H. Yin, R. Landick, J. Gelles and S. M. Block, Science, 282, 902
(1998).
[6] T. T. Perkins, R. V. Dalal, P. G. Mitsis and S. M. Block, Science, 301, 1914 (2003).
[7] F. J¨ulicher, A. Ajdari and J. Prost, Rev. Mod. Phys., 69, 1269 (1997).
[8] A. Ajdari, Europhys. Lett., 31, 69 (1995).
[9] A. Parmeggiani, F. Julicher, L. Peliti and J. Prost, Europhys. Lett., 56, 603 (2001).
[10] J. Prost, J.-F. Chauwin, L. Peliti and A. Ajdari, 72, 2652 (1994).
[11] M. E. Fisher and A. B. Kolomeisky, Proc. Natl. Acad. Sci. USA, 96, 6597 (1999).
[12] See also A. B. Kolomeisky and M. E. Fisher, Physica A, 279, 1 (2000).
[13] A. B. Kolomeisky and M. E. Fisher, Biophys. J., 84, 1642 (2003).
[14] J. Howard, Mechanics of Motor Proteins and the Cytoskeleton, Sinauer, Sunderland (2001).
[15] W. Hua, E. C. Young, M. L. Fleming, J. Gelles, Nature, 388, 390 (1997).
[16] T. Ha, I. Rasnik, W. Cheng, H. P. Babcock, G. H. Gauss, T. M. Lohman and S. Chu, Nature,
419, 638 (2002).
[17] P. R. Bianco, L. R. Brewer, M. Corzett, R. Balhorn, Y. Yeh, S. C. Kowalczykowski, R. J. Baskin,
Nature, 409, 374 (2001).
[18] A. M. van Oijen, P. C. Blainey, D. J. Crampton, C. C. Richardson, T. Ellenberger, and X. Sunney
Xie, Science, 301, 1235 (2003).
[19] T. T. Perkins, R. V. Dalal, P. G. Mitsis, S. M. Block, Nature, 301, 1914 (2003).
[20] T. Harms amd R. Lipowsky, Phys. Rev. Lett., 79, 2895 (1997).
[21] Y. Kafri, D. K. Lubensky and D. R. Nelson, Biophys. J., 86, 3373 (2004).
[22] Y. Kafri, D. K. Lubensky, D. R. Nelson, Phys. Rev. E, 71, 041906 (2005).
[23] T. Shimizu, K. Furusawa, S. Ohashi, Y. Y. Toyoshima, M. Okuno, F. Malik and R. D. Vale, J.
Cell. Biol. 112, 1189 (1991).
[24] T. M. Kapoor and T. J. Mitchison, Proc. Natl. Acad. Sci. U. S. A., 96, 9106 (1999).
[25] S. C. Kuo and M. P. Sheetz, Science, 260, 232 (1993).

Sequence heterogeneity and the dynamics of molecular motors
19
[26] C. K. Peng, S. V. Buldyrev, A. L. Goldberger, S. Havlin, F. Sciortino, M. Simons and H. E. Stanley
Nature, 356, 168 (1992).
[27] A. B. Kolomeisky and B. and Widom, J. Stat. Phys. 93, 633 (1998).
[28] M. E. J. Newman and G. T. Barkema, Monte Carlo Methods in Statistical Physics, (Oxford, 1999).
[29] For a review of random forcing energy landscapes see J. P. Bouchaud, A. Comtet, A. Georges and
P. Le Doussal, Ann. Phys. (N.Y.), 201, 285 (1990).
[30] H. Matsuzaki, G. A. Kassavetis and E. P. Geiduschek, J. Mol. Biol., 235, 1173 (1994).
[31] L. Bai, A. Shundrovsky and M.D. Wang, J. Mol. Biol., 344, 335 (2004).
