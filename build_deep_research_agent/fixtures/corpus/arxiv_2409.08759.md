---
title: "Dark Energy Survey: 2.1% measurement of the Baryon Acoustic Oscillation scale from the final dataset"
authors: "Juan Mena-Fernández, Dark Energy Survey Collaboration"
year: 2024
source: arxiv
source_id: "2409.08759"
url: "http://arxiv.org/abs/2409.08759v1"
domain: astrophysics
---
Dark Energy Survey: 2.1% measurement of the Baryon Acoustic Oscillation scale
from the final dataset
Juan Mena-Fern´andez on behalf of the Dark Energy Survey Collaboration
LPSC Grenoble - 53, Avenue des Martyrs 38026 Grenoble, France
Here, we present the angular diameter distance measurement obtained from the measurement
of the Baryonic Acoustic Oscillation (BAO) feature using the completed Dark Energy Survey
(DES) data, summarizing the main results of 1 and 2. We use a galaxy sample optimized for
BAO science in the redshift range 0.6 < z < 1.2, with an effective redshift of zeff = 0.85. Our
consensus measurement constrains the ratio of the angular distance to the sound horizon scale
to DM(zeff)/rd = 19.51±0.41. This measurement is found to be 2.13σ below the angular BAO
scale predicted by Planck-2018. To date, it represents the most precise measurement from
purely photometric data, and the most precise from any Stage-III experiment at such high
redshift. The analysis was performed blinded to the BAO position and is shown to be robust
against analysis choices, data removal, redshift calibrations and observational systematics.
1
Introduction
The Dark Energy Surveya (DES) is a Stage-III photometric galaxy survey designed to constrain
the properties of dark energy and other cosmological parameters from multiple probes. DES has
performed state-of-the-art analyses of weak gravitational lensing, galaxy clustering and galaxy
cluster counts. These probes have also been combined with external cosmic microwave back-
ground data. The DES Supernova (SN) program has also broken new grounds in constraining
cosmology from ∼1,500 type Ia SN 3.
In addition to that, the large data sets and catalogs
produced by DES represent a unique source for other cosmological and astronomical analyses.
In this work, we use the complete DES data set, which includes 6 years of observations
(2013-2019), to constrain the angular BAO distance scale, summarizing the main outcomes of
1. We follow a similar methodology to previous DES analyses, with three main changes. First,
in 2 we re-optimize the galaxy sample and extend it up to redshift 1.2. Second, we reinforce
the redshift validation, considering several independent calibrations and quantifying its possible
impact on the BAO measurement.
Third, we provide BAO measurements from three types
of two-point clustering statistics: angular correlation function (ACF), angular power spectrum
(APS) and projected correlation function (PCF). Our reported consensus result comes from the
ahttps://www.darkenergysurvey.org/
arXiv:2409.08759v1  [astro-ph.CO]  13 Sep 2024

statistical combination of those three measurements, following a strict blinding policy.
2
The BAO-Optimized Sample
The galaxy sample used to measure the BAO signal is a subset of the DES data set selected
using the griz bands and a photometric redshift estimate, zph. The selection cuts applied are
1.7 < i −z + 2(r −i)
(color selection),
(1)
17.5 < i < 19.64 + 2.894zph
(flux selection),
(2)
i < 22.5
(i −mag limit),
(3)
0.6 < zph < 1.2
(photo-z range).
(4)
The sample has 15.93 million galaxies, its angular mask covers 4,273 deg2, it is divided into 6
redshift bins with ∆zph = 0.1 and its effective redshift is zeff = 0.85. The cut specified by Eq.
(2) was optimized using a Fisher forecast algorithm, as detailed in 2.
3
Methodology
3.1
Simulations
We created a set of 1,952 mock catalogs based on ICE-COLA fast simulations 4. They reproduce
with high accuracy the main properties of the data: observational volume, abundance of galaxies,
redshift distributions, photo-z errors and clustering as a function of redshift. Mock catalogs are
key to validating the modeling and quantifying how likely some features we find in the data are.
3.2
The BAO Fit
Our approach to measuring the BAO distance scale is based on a template fitting method.
We start from the linear power spectrum generated using CAMB, Plin(k), and then isolate the
no-wiggle component, Pnw(k), as
P(k, µ) = (b + µ2f)2 h
(Plin −Pnw)e−k2Σ2 + Pnw
i
,
(5)
where b is the linear galaxy bias, µ2f accounts for redshift-space distortions, and Σ models
the broadening of the BAO peak due to non-linearities. From this P(k, µ), we compute the
theoretical template, TBAO(x), for our three estimators (ACF, APS and PCF). For the template,
we use Planck-2018 5 as the reference cosmology and assume ΛCDM. The model fitted to the
data is given by
M(x) = BTBAO(x′) + A(x),
(6)
where the position of the BAO feature is given in terms of the BAO-scaling parameter, α. x′ is
given by αθ, ℓ/α and s⊥α for ACF, APS and PCF, respectively. By definition,
α(zeff) = DM(zeff)
rd
Dref
M (zeff)
rref
d
−1
,
(7)
where DM(z) is the comoving angular diameter distance and rd is the sound horizon scale at
recombination. “ref” refers to quantities evaluated at the reference cosmology (Planck-2018).
3.3
Systematics
We mitigate the impact of observational systematics by applying correcting weights obtained
with the Iterative Systematics Decontamination method6 to our galaxy sample (see2 for details).

1
2
3
4
5
θ(deg)
0
2
4
6
8
10
103(w −wnoBAO) (+oﬀset)
0.6 < zph < 0.7
0.7 < zph < 0.8
0.8 < zph < 0.9
0.9 < zph < 1.0
1.0 < zph < 1.1
1.1 < zph < 1.2
0
100 200 300 400 500 600 700
Multipole, ℓ
1.0
1.5
2.0
2.5
3.0
3.5
4.0
4.5
Cℓ/CnoBAO
ℓ
(+oﬀset)
0.6 < zph < 0.7
0.7 < zph < 0.8
0.8 < zph < 0.9
0.9 < zph < 1.0
1.0 < zph < 1.1
1.1 < zph < 1.2
40
60
80
100
120
140
s⊥(Mpc/h)
−10
0
10
20
30
40
50
60
70
80
s2
⊥(ξp −ξp,NoBAO) (+oﬀset)
0.6 < zph < 0.7
0.7 < zph < 0.8
0.8 < zph < 0.9
0.9 < zph < 1.0
1.0 < zph < 1.1
1.1 < zph < 1.2
Figure 1 – Isolated BAO feature, measured using the ACF (left), APS (center) and PCF (right). Measurements
are shown as markers with error bars, while the best-fit model is shown as solid lines. For each estimator, the fit
is performed using the clustering signal of the 6 redshift bins together (accounting for their covariances).
3.4
Pre-Unblinding Tests
The analysis and most of the paper writing were performed blind. Before unblinding, we require
our data to pass a battery of tests. Some of these include whether we have a detection of the
BAO feature in the combined fit and each redshift bin individually or not, if our measurement
is robust against analysis choices, and if our three estimators give consistent results. All these
tests pointed to the robustness of our measurement, so we unblinded (see 1 for more details).
4
Results
In Fig. 1, we show the clustering measurements for our different estimators and the best-fit
model. Our fiducial results are α = 0.9517 ± 0.0227, 0.9617 ± 0.0224 and 0.9553 ± 0.0201 for
ACF, APS and PCF, respectively. Our consensus measurement (combination of the three) is
α(zeff) = 0.9571 ± 0.0196
[stat.],
(8)
± 0.0041
[sys.],
(9)
α(zeff) = 0.9571 ± 0.0201
[tot.],
(10)
where the [sys.] contribution comes from modeling and redshift calibration, see 1. This result
has a fractional error of 2.1% (the smallest for a photometric survey ever), and is consistent
with Planck-2018 (α = 1) at 2.13σ. It can also be expressed as DM(zeff)/rd = 19.51 ± 0.41.
In Fig. 2, we show our main measurement, together with the results obtained with several
variations of the analysis. We find that it is robust against variations in the fiducial settings,
different clustering estimators and data calibration (systematics). Finally, in Fig. 3 we show
the angular BAO distance ladder at the end of Stage III. We find that our measurement is
competitive with the results from the Sloan Digital Sky Survey (SDSS), and is the most precise
one at z > 0.75 at the end of Stage III.
References
1. Dark Energy Survey Collaboration. Phys. Rev. D, 110:063515, Sep 2024.
2. J. Mena-Fern´andez et al. Phys. Rev. D, 110:063514, Sep 2024.
3. Dark Energy Survey Collaboration. arXiv preprint arXiv:2401.02929, 2024.
4. I. Ferrero et al. Astronomy & Astrophysics, 656:A106, 2021.
5. Planck Collaboration. A&A, 641:A6, September 2020.
6. M. Rodr´ıguez-Monroy et al. MNRAS, 511(2):2665–2687, April 2022.

w(θ) + Cℓ+ ξp
w(θ)
w(θ) no-wsys
w(θ) mocks-Cov
w(θ) DNF n(znn)
w(θ) VIPERS n(z)
w(θ) MICE ×0.9616
w(θ) θmin = 1◦
w(θ) ∆θ = 0.1◦
Cℓ
Cℓno-wsys
Cℓmocks-Cov
CℓDNF n(znn)
CℓVIPERS n(z)
CℓMICE ×0.9616
Cℓℓmax
Cℓ∆ℓ= 10
Cℓ∆ℓ= 30
ξp
ξp no-wsys
ξp mocks-Cov
ξp DNF n(znn)
ξp VIPERS n(z)
ξp MICE ×0.9616
ξp s ∈[70, 130]h−1Mpc
ξp ∆s = 10h−1Mpc
ξp ∆s = 2h−1Mpc
ξp Nz = 1
ξp Nz = 3
ξp Nz = 1, 0.7 < z < 1.2
0.92
0.94
0.96
0.98
1.00
α
Figure 2 – Main BAO measurement shown with an orange star and an orange shaded area, together with several
variations of the analysis. Variations of the ACF, APS and PCF analyses are presented in blue, green and purple,
respectively, with the fiducial settings being represented by the first entry for each of them.
0.35
0.55
0.75
0.95
0.90
0.95
1.00
1.05
1.10
BAO Measurement/Planck ΛCDM reference
BOSS DR12
LRGs
DES Y1
eBOSS DR16
ELGs (inc. RSD)
eBOSS+BOSS
DR16 LRGs
DES Y3
DES Y6
(this work)
DES Y6
(this work)
DES Y6
(this work)
DES Y6
(this work)
DES Y6
(this work)
1.45
eBOSS
DR16 QSO
2.35
eBOSS
DR16 Ly-α
Redshift
Figure 3 – Ratio between the DM(z)/rd measured using the BAO feature at different redshifts for several galaxy
surveys and the prediction from the cosmological parameters determined by Planck-2018, assuming ΛCDM.
We include a series of measurements by SDSS, and also the DES Y1 and Y3 results. Our DES final data set
measurement is shown as an orange star. This represents the most updated angular BAO distance ladder at the
closure of Stage III.
