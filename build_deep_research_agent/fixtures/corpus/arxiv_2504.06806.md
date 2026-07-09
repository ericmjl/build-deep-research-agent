---
title: "Mass Balance Approximation of Unfolding Improves Potential-Like Methods for Protein Stability Predictions"
authors: "Ivan Rossi, Guido Barducci, Tiziana Sanavia, Paola Turina, Emidio Capriotti, Piero Fariselli"
year: 2025
source: arxiv
source_id: "2504.06806"
url: "http://arxiv.org/abs/2504.06806v1"
domain: computational-biology
---
1

Mass Balance Approximation of Unfolding Improves
Potential-Like Methods for Protein Stability
Predictions



Ivan Rossi1, Guido Barducci1, Tiziana Sanavia1, Paola Turina2,
Emidio Capriotti2*, Piero Fariselli1*

1 Department of Medical Sciences, University of Torino, Via Santena 19, 10126 Torino, Italy
2 Department of Pharmacy and Biotechnology (FaBiT), University of Bologna, Bologna, Italy
* Corresponding authors: emidio.capriotti@unibo.it, piero.fariselli@unito.it



Abstract
The prediction of protein stability changes following single-point mutations plays a pivotal
role in computational biology, particularly in areas like drug discovery, enzyme
reengineering, and genetic disease analysis. Although deep-learning strategies have pushed
the field forward, their use in standard workflows remains limited due to resource demands.
Conversely, potential-like methods are fast, intuitive, and efficient. Yet, these typically
estimate Gibbs free energy shifts without considering the free-energy variations in the
unfolded protein state, an omission that may breach mass balance and diminish accuracy.
This study shows that incorporating a mass-balance correction (MBC) to account for the
unfolded state significantly enhances these methods. While many machine learning models
partially model this balance, our analysis suggests that a refined representation of the
unfolded state may improve the predictive performance.

Availability: The Python codes and the data used in this study can be downloaded from
Github at https://github.com/compbiomed-unito/ddMBC





2

Introduction
Predicting protein stability changes upon single-point mutations is a longstanding
challenge in computational biology1–3, with significant implications in drug design,
enzyme engineering, and understanding disease mechanisms4. Protein stability is
typically quantified by measuring the Gibbs free energy change (ΔG) between the
folded and unfolded states as

𝛥𝐺= 𝐺𝐹−𝐺𝑈




 [1]

However, mutations can dramatically alter this delicate balance. Destabilizing
mutations are often linked to diseases5, such as cancer6, while stabilizing mutations
can enhance protein function and resilience, especially in industrial and therapeutic
settings7,8.
From the experimental point of view, the measure of interest is the difference of the
unfolding free energy between the mutated and wild-type proteins (ΔΔG), calculated
as

𝛥𝛥𝐺= (𝐺𝐹(𝑚) −𝐺𝐹(𝑤)) −(𝐺𝑈(𝑚) −𝐺𝑈(𝑤))


[2]

where m and w stands for mutant and wild-type (Fig. 1)

𝑃𝐹(𝑤) + 𝑃𝑈(𝑚) ⇌
𝑃𝐹(𝑚) + 𝑃𝑈(𝑤)


[3]

Where P represents the concentration of the protein either in the wild-type (w) or
mutant (m) forms both in the folded (F) or unfolded (U) states. It can be noticed that
this kind of “reaction” corresponds to that used in Free-Energy Perturbation (FEP)
calculations9,10,  a widely-used method to calculate ΔG differences in molecular
modeling and drug design.

The folding free energy difference between two protein variants depends on both the
folded and unfolded states of each sequence. Studies using molecular dynamics,
based on Alchemical Free Energy Perturbation10,11, have demonstrated that
accurately modeling the unfolded state is crucial for achieving high predictive
performance11, though such approaches require computationally expensive
methods. Similar statistical-mechanics approaches describing the contribution of the
unfolded-state have been presented by Bastolla and coworkers12–14.

In recent years, deep learning-based approaches have significantly advanced the
field of protein stability prediction. Despite their success, these models require
substantial computational resources and are sometimes inaccessible for routine or
high-throughput applications2.

3

In contrast, potential-like methods, such as those utilizing empirical energy functions
like FoldX15 structure-based protein-language models such as ProteinMPNN16 and
ESM-IF117, and methods that directly address the calculation of ΔΔG upon mutation
using deep neural networks, such as Pythia18, offer faster and more accessible
alternatives. These methods estimate stability changes by calculating either
atomistic interactions or the likelihood of an amino acid in a given structural context
of the protein. Pythia, for example, employs a self-supervised learning framework to
perform zero-shot ΔΔG predictions across a large protein sequence space, offering
ultrafast computational performance.



Fig.1 Thermodynamics of the Variation of the folding free energy upon single point mutation,
considering mutated (m) and wild-type (w) states. In box [1] the relation between probability and free
energy of folding is reported. In box [2], the correct measure of the difference of the unfolding free
energy between the mutated and wild-type proteins, considering  the difference between the folded
and unfolded state is reported (first equation); however, some potential-like methods approximate it
using the difference of the folding state free energy, neglecting the effect of the unfolded states (box
[2], second equation). A first approximation can be obtained by adding a mass-balance correction
(also a kind of solvation term) to the folding free energy difference (box [2], third equation).


However, one fundamental limitation of the potential-like methods is their simplified
approach to Gibbs free energy calculations, where only the folded states {𝐺𝐹(𝑥)} (i.e.,
the protein structure) are considered. This simplification leads to the following
approximation for the mutant (m) and wild-type (w):

4

𝛥𝛥𝐺
= (𝐺𝐹(𝑚) −𝐺𝐹(𝑤))



[4]

Under this approximation, the second term of Eq. 2, describing the ΔG between the
unfolded states of the two protein sequences, is typically neglected due to the
difficulty of properly defining and measuring it. However, this approximation might
not always hold, since, for example, different inter-residue interactions and degrees
of freedom between wild-type and mutant might persist in the unfolded state. An
additional contribution might be the difference in free-energy of solvation for the
amino acids involved in the mutation26. It should also be observed that the ΔΔG
expression is a difference between two terms, and neglecting one could lead to
significant deviations from the correct solution. Furthermore, neglecting this second
term also implicitly means violating the mass-conservation for the process, as Gibbs
free energy is defined for closed systems where mass is conserved.

Considering the extreme flexibility of the neural-networks in implicitly modeling all
terms of Eq. 1, the approximation of ΔG between the unfolded states of the two
protein sequences equal to zero should not affect, in principle, models that explicitly
incorporate the protein-sequence composition change among their input features
(e.g. I-mutant19, ACDC-NN20, Stability Oracle21). However, as previously mentioned,
this approximation  might become relevant for models that do not compensate for it,
such as most “potential-like” methods.

To address this gap, we propose a novel correction that incorporates “mass balance”
back into potential-like scoring methods, improving the accuracy of protein stability
predictions without compromising their usually high computational efficiency. By
retrofitting these potential-like models with this extra term, which we call mass-
balance correction (MBC), our approach adjusts for a key flaw in the evaluation of
ΔΔG, significantly enhancing the prediction accuracy without any reparameterization
of the original model.
Furthermore, the obtained performance for some of these modified methods are
comparable, or even better, to those of state-of-the-art models such as Stability
Oracle, providing a valuable tool for researchers needing rapid stability
assessments.

Results
Incorporating Mass-Balance Information as a First Approximation of the
Unfolded State
We first evaluated the performance of three different potential-like methods,
representing three different approaches to ΔΔG calculation, with and without the
MBC correction. Then we compared them to the results of the DDGun3D22,23

5
“untrained” benchmark model. DDGun3D explicitly incorporates a form of  MBC by
considering the hydrophobicity difference between mutated and wild-type residues,
establishing it as a suitable reference benchmark. We also derived the data-driven
MBC term, referred to as MBC(dd) hereafter, by fitting it to the training set using
ridge regression implemented in Scikit-learn24 with default parameters.
The MBC(dd) term was then compared with the Kyte-Doolittle25 and Rose26 scales to
score the difference between hydrophobicity and solvation, respectively, as first
approximations of the unfolded state. Additionally, we included a comparison with
the Stability Oracle model, a recent state-of-the-art deep learning-based method. We
used the S461 dataset27 as the test set to perform comparisons.

The three potential-like methods considered are:
1. ESM-IF1, a large protein-language model (PLM) trained to predict a protein
sequence likelihood from its backbone atom coordinates;
2. FoldX, a widely-used all-atom knowledge-based potential for fast and
quantitative estimation of the importance of the interactions contributing to the
stability of proteins;
3. Pythia, a self-supervised graph neural network tailored for zero-shot ∆∆G
predictions, large-scale residue scanning and missing-residue probability
prediction.

On the S461 test set, all methods showed visible performance boosts, with
increased Pearson correlation coefficients (PCC) compared to the original methods
and with Pythia/MBC(dd) being the top-performer.

Although we used PDB structures to train our model, we observed that the
performance of both the baseline ESM-IF1 and Pythia models noticeably depends
on the type of structure used. Namely, the performance of both of these methods is
higher if AlphaFold28 models are used instead of experimental X-ray structures from
PDB. This is probably due to the way these methods have been parameterized: for
both ESM-IF1 and Pythia training sets, the percentage of AlphaFold structure
exceeds 90%, thus any bias that may be introduced by using models instead of
experimental structures is captured by the methods. Nonetheless, the MBC(dd)
validity is not affected by the choice of the model origin (Table S2): using the
MBC(dd) correction derived from the PDB structures on the same test sets, but
giving in input the AlphaFold structures, instead of those from PDB, results in models
that are even better-performing. Both Stability Oracle and Pythia/MBC(dd)-AF
achieve a PCC higher than the one obtained by the benchmark DDGun3D method
(PCC: 0.62), whose performance on the S461 data set is very strong (Figure 2). We
also computed the MBC(dd) correction for Stability Oracle and DDGun3D
benchmarks, and, as expected, the result is worse for both methods (Figuure 2).
This supports our expectation that these methods, which already account for
descriptors of the unfolded state in their input, such as the stoichiometry of the

6
mutation process, are effectively capturing the correct underlying physics without
requiring any posterior corrections.

Comparison between residue specific-coefficients and experimental
solvation scales

We performed a Pearson correlation analysis among the residue-specific parameters
fitted using the VBS3322 dataset (see Methods section) to assess their consistency
across different methods. Additionally, we included solvation and hydrophobicity
scale values in the correlation comparison to evaluate their relationship with the fitted
parameters. As shown in Fig. 3, the amino acid-specific parameters (a1 to a20) exhibit
strong correlations across the potential-like methods. Furthermore, these fitted
parameters show a notable correlation with Kyte and Doolittle hydrophobicity scale
and an even stronger correlation with the experimentally-derived Rose scale, which
was specifically designed to predict the average change in solvent accessible
surface area of amino acids upon folding.
In agreement with these observations, we then computed a new MBC based on the
Rose scale, referred to as MBC(Rose). This correction was derived using a two-
parameter linear combination between the original-method delta and the Rose-scale
delta (see Eq. 8), with results summarized in Fig. 2. The performance of MBC(Rose)
is consistent with, or in some cases superior to, that obtained by the MBC(dd)
approach.
As a further validation, we computed the Pythia/MBC(dd) and Pythia/MBC(Rose)
scores using the parameters derived from our VBS3322 training set and tested them
on the independent mega-scale dataset29, which was not used in the parameter
derivation. The results show an improvement (PCC: +0.07) over the original Pythia
score, achieving a PCC close to 0.70 and an RMSE of 1.43 kcal/mol.

7


Fig.2 Comparison of Pearson correlation Coefficient obtained on S461 dataset between the original
method (pink bar) and its adjusted version with Mass-Balance Correction, using bothMBC(dd) (green
bar) and Rose scale (blue bar). ddMMBC_only represents the prediction made using only the fitted
mutation coefficients without incorporating a method.  *KD25 and *Rose26  and are the scale difference
values without any fitting.

Generalization of the Mass-Balance Correction Across Different Methods

Reeves and Kalyaanamoorthy30 recently highlighted that structure-based and
sequence-based PLMs can be linearly combined to improve the performance,
indicating that these two methodological classes provide complementary information.
They further noted that “...PSLMs can be reliably augmented with physicochemical
properties to exceed the median performance of the benchmark stability predictor..”.
This aligns with our model, since

𝛥𝛥𝐺= (𝐺𝐹(𝑚) −𝐺𝐹(𝑤)) −(𝐺𝑈(𝑚) −𝐺𝑈(𝑤)) = 𝛥𝛥𝐻𝐹−𝑇𝛥𝛥𝑆𝐹

[5]

Thus, it is reasonable to think that both sequence and structure-based terms
correspond to the ΔΔG term for the unfolded and folded states, respectively.
Additionally, the molecular volume and the solvent-accessible surface area (SASA)
play a crucial role in estimating the solvation energy changes (a large part of ΔΔS𝐹)
when a molecule interacts with a solvent. This concept has been widely applied in
different implicit solvation models, such as the GBSA family of models31,32.
From this perspective, the MBC can be seen as a proxy of this information. Our
model provides a simple, yet effective, way to estimate the Gibbs free energy
difference between wild-type and mutated proteins in their unfolded states.

8
Alternatively, it can be interpreted as describing the differences in the entropy of
folding (which is largely dictated by solvation effects), while the potential-like
methods primarily approximate the enthalpic contribution to the folding.

We thus tested whether our approach is able to generalize across different methods,
considering the predictions of 48 methods on S461 dataset taken from Reeves and
Kalyaanamoorthy30 and supplemented by the Pythia data. To fit the two scale values
related to the method and to the Rose scale (see Methods equation 8) we used the
prediction reported by the same authors on the Ssym dataset33.
Fig. 4 reports the obtained results, grouping the methods into MBC-aware (i.e.
trained with some mass-balance correction) and non-MBC-aware approaches (such
as PLMs, which does not account for the mass balance). As expected, the MBC
approach notably improved the performance of non-MBC-aware methods.


Fig.3 Correlation among the residue coefficients of the different methods and two hydrophobicity
scales (Kyte-Doolittle25 and Rose26). DDGun3D contains explicitly the difference of the Kyte-Doolittle
values. ddmbc_aa_ridge is highly correlated with the Rose scale



9


Fig.4 Comparison with methods that directly include a mass-balance correction (MBC Aware) with
those that compute only a difference between the folding states (Non MBC Aware). The plot reports
the  distribution of the difference between the Pearson’s correlation after and before the mass-
balance term is added. The data are from Reeves and Kalyaanamoorthy30

Conclusions
The mass-balance correction (MBC), whether data-driven or based on an
experimentally derived scale, demonstrates broad applicability, enhancing the
performance of various potential-like methods developed through different
approaches. These include knowledge-based potentials, sequence- and structure-
based protein language models (PLMs), and a self-supervised deep graph-neural
network. Notably, MBC achieves these improvements without requiring any re-
parameterization of the base methods and with negligible additional computational
cost.
In several cases, the enhancement of the performance due to MBC is substantial.
Specifically, in the case of Pythia, the results are particularly notable, bringing
Pythia-MBC close to state-of-the-art performance while also addressing the method's

10
poor antisymmetry (from -0.53 to -0.68 of antisymmetry in Ssym). More generally,
MBC preserves the antisymmetry of the improved methods whenever the original
methods exhibit this property.
This finding strongly supports our hypothesis that a better description of the unfolded
state of the proteins might be a necessary step to improve the current state-of-the-art
protein stability-change predictions. The MBC correction is just a simple, yet
effective, zero-order correction. Thus, it is clearly possible to envision more
sophisticated and, eventually, better-performing methods. Nonetheless, we believe
that the simplicity of our approach has its own merits per se, since it allows the
retrofitting of several existing approaches, achieving  good performance and
avoiding extra computational costs.

Materials and Methods
Datasets composition
The main training set used in this work, namely VBS3322, consists of 3,322
mutations obtained by combining the VariBench35 and the S264834 data sets. In the
cases where the same mutation is reported in both data sets, the VariBench value is
considered. We also augmented the dataset by including the antisymmetric
complement of each mutation, as suggested in a previous work36.
The test set used for the benchmarking is the S461. For all the structures that
showed missing backbone atoms, we preprocessed the structure using the
PDBFixer utility37.
The FoldX results used for both training and evaluation have already been
published38, while Stability Oracle results for the S461 dataset have been computed
from
the
data
provided
by
its
authors
on
Github
(https://github.com/danny305/StabilityOracle)

Mass balance Correction
The simplest approach to calculate the ΔΔG for the sequence-mutation process is to
assume that the second term of equation [1] depends only on the amino acids
involved in the mutation.
This simplification leads to the following reaction, considering the wild-type (𝑤) and
mutated  (𝑚) residues:

𝑃𝑟𝑜𝑡𝑒𝑖𝑛(𝑤, 𝑖) + 𝑅𝑒𝑠𝑖𝑑𝑢𝑒(𝑚) ⇄𝑃𝑟𝑜𝑡𝑒𝑖𝑛(𝑚, 𝑖) + 𝑅𝑒𝑠𝑖𝑑𝑢𝑒(𝑤)

[6]

where 𝑃𝑟𝑜𝑡𝑒𝑖𝑛(𝑥, 𝑖) represents a protein with residue 𝑥 in position 𝑖, while 𝑅𝑒𝑠𝑖𝑑𝑢𝑒(𝑥)
refers to a single amino acid. Conceptually, this corresponds to estimating the
difference in the (effective) Gibbs free energy of solvation for two amino acids in

11
solution and within the field of the protein. From another perspective, this approach
approximates the free energy of the unfolded state as the sum of independent
contributions from each amino acid. Physically, these contributions may arise from
the conformational entropy of both the side chain and main chain, as well as their
interactions with the solvent. Under this approximation, all terms disappear except
for the contributions of the wild-type and mutated amino acids, significantly
simplifying the calculation.


Input encoding
We encode the mutation in the sequence as a twenty-elements array, one element
for each of the natural amino acids, and we encode their occurrence (O) as -1 for the
wild-type amino acid and +1 for the substitution.

The modified expression to calculate ΔΔG is then expressed as a linear combination
of the original-method score (S) for the wild-type and the mutated protein:

𝛥𝛥𝐺= 𝑎0(𝑆(𝑚) −𝑆(𝑤)) + ∑
𝑎𝑖𝑂𝑖
20
𝑖=1



[7]

the first term represents the original method's (scaled) output and the second term
represents the pseudo-ΔΔG of solvation for the amino acids involved in the mutation
(the data-driven MBC).
The first term 𝑆(𝑥) thus corresponds to the ΔΔG predicted by the original method,
while the second term depends on amino acid-related parameters.
It should also be observed that equation [7], being antisymmetric by definition,
preserves the antisymmetry in the prediction of the original methods, if present.
The 21 coefficients for the linear model above can be easily derived via a simple
linear regression with respect to the training set.

Similarly, the MBC(Rose) correction is computed as a two-parameter linear
combination of the original-method score (S) and Rose-scale delta

𝛥𝛥𝐺= 𝑎0(𝑆(𝑚) −𝑆(𝑤)) + 𝑎1(𝑅(𝑚) −𝑅(𝑤))

[8]

where 𝑅(𝑚) ∧𝑅(𝑤) are the values of the Rose scale for the mutated- and wild-type
amino acid respectively.

Measures of performance
To evaluate the performance of the methods in the regression task, we compared
the predicted (p) and experimental (e) values of the variation of unfolding free energy
change upon mutation (ΔΔG). The standard scoring values calculated in our

12
assessment are the Pearson correlation coefficients (PCC) and the root mean
square error (RMSE), defined as follows:









 



[9]
















[10]



where 𝛥𝛥𝐺𝑝 and 𝛥𝛥𝐺𝑒 are the average predicted and experimental ΔΔG values,
respectively.

Acknowledgments
The authors thank the Italian Ministry for Education, University and Research under
the programme “Ricerca Locale ex-60%” and PNRR M4C2 HPC—1.4 “CENTRI
NAZIONALI”- Spoke 8 for fellowship support. In addition, the authors thank the
European Union’s Horizon 2020 projects Brainteaser (Grant Agreement ID:
101017598) and GenoMed4All (Grant Agreement ID:101017549:). IR would like to
dedicate this work to his past supervisor Prof. Donald G. Truhlar.




13
References

1. Pucci F, Schwersensky M, Rooman M (2022) Artificial intelligence challenges for
predicting the impact of mutations on protein stability. Curr Opin Struct Biol 72:161–168.
2. Sanavia T, Birolo G, Montanucci L, Turina P, Capriotti E, Fariselli P (2020) Limitations and
challenges in protein stability prediction upon genome variations: towards future applications
in precision medicine. Comput Struct Biotechnol J 18:1968–1979.
3. Benevenuta S, Birolo G, Sanavia T, Capriotti E, Fariselli P (2022) Challenges in predicting
stabilizing variations: An exploration. Front Mol Biosci 9:1075570.
4. Thomas PJ, Qu BH, Pedersen PL (1995) Defective protein folding as a basis of human
disease. Trends Biochem Sci 20:456–459.
5. Martelli PL, Fariselli P, Savojardo C, Babbi G, Aggazio F, Casadio R (2016) Large scale
analysis of protein stability in OMIM disease related human protein variants. BMC Genomics
17 Suppl 2:397.
6. Petrosino M, Novak L, Pasquo A, Chiaraluce R, Turina P, Capriotti E, Consalvi V (2021)
Analysis and Interpretation of the Impact of Missense Variants in Cancer. Int J Mol Sci
22:5416.
7. Coluzza I (2017) Computational protein design: a review. J Phys Condens Matter
29:143001.
8. Korendovych IV, DeGrado WF (2020) De novo protein design, a retrospective. Q Rev
Biophys 53:e3.
9. Zwanzig RW (1954) High‐ Temperature Equation of State by a Perturbation Method. I.
Nonpolar Gases. The Journal of Chemical Physics 22:1420–1426.
10. York DM (2023) Modern Alchemical Free Energy Methods for Drug Discovery Explained.
ACS Phys Chem Au 3:478–491.
11. Kurniawan J, Ishida T (2023) Comparing Supervised Learning and Rigorous Approach
for Predicting Protein Stability upon Point Mutations in Difficult Targets. J Chem Inf Model
63:6778–6788.
12. Minning J, Porto M, Bastolla U (2013) Detecting selection for negative design in proteins
through an improved model of the misfolded state. Proteins 81:1102–1112.
13. Bastolla U (2014) Detecting selection on protein stability through statistical mechanical
models of folding and evolution. Biomolecules 4:291–314.
14. Arenas M, Weber CC, Liberles DA, Bastolla U (2017) ProtASR: An Evolutionary
Framework for Ancestral Protein Reconstruction with Selection on Folding Stability. Syst Biol
66:1054–1064.
15. Schymkowitz J, Borg J, Stricher F, Nys R, Rousseau F, Serrano L (2005) The FoldX web
server: an online force field. Nucleic Acids Res 33:W382-8.
16. Dauparas J, Anishchenko I, Bennett N, Bai H, Ragotte RJ, Milles LF, Wicky BIM,
Courbet A, de Haas RJ, Bethel N, et al. (2022) Robust deep learning-based protein

14
sequence design using ProteinMPNN. Science 378:49–56.
17. Hsu C, Verkuil R, Liu J, Lin Z, Hie B, Sercu T, Lerer A, Rives A Learning inverse folding
from millions of predicted structures. In: Proceedings of the 39th International Conference on
Machine Learning. PMLR; 2022. pp. 8946–8970. Available from:
https://proceedings.mlr.press/v162/hsu22a.html
18. Sun J, Zhu T, Cui Y, Wu B (2025) Structure-based self-supervised learning enables
ultrafast protein stability prediction upon mutation. Innovation (Camb) 6:100750.
19. Capriotti E, Fariselli P, Casadio R (2005) I-Mutant2.0: predicting stability changes upon
mutation from the protein sequence or structure. Nucleic Acids Res 33:W306-10.
20. Pancotti C, Benevenuta S, Repetto V, Birolo G, Capriotti E, Sanavia T, Fariselli P (2021)
A Deep-Learning Sequence-Based Method to Predict Protein Stability Changes Upon
Genetic Variations. Genes (Basel) 12:911.
21. Diaz DJ, Gong C, Ouyang-Zhang J, Loy JM, Wells J, Yang D, Ellington AD, Dimakis AG,
Klivans AR (2024) Stability Oracle: a structure-based graph-transformer framework for
identifying stabilizing mutations. Nat Commun 15:6170.
22. Montanucci L, Capriotti E, Frank Y, Ben-Tal N, Fariselli P (2019) DDGun: an untrained
method for the prediction of protein stability changes upon single and multiple point
variations. BMC Bioinformatics [Internet] 20. Available from:
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6606456/
23. Montanucci L, Capriotti E, Birolo G, Benevenuta S, Pancotti C, Lal D, Fariselli P (2022)
DDGun: an untrained predictor of protein stability changes upon amino acid variants. Nucleic
Acids Res:gkac325.
24. Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel,
M., Prettenhofer, P., Weiss, R., Dubourg, V., et al. (2011) Scikit-learn: Machine Learning in
Python. JMLR 12:2825–2830.
25. Kyte J, Doolittle RF (1982) A simple method for displaying the hydropathic character of a
protein. J Mol Biol 157:105–132.
26. Rose GD, Geselowitz AR, Lesser GJ, Lee RH, Zehfus MH (1985) Hydrophobicity of
amino acid residues in globular proteins. Science 229:834–838.
27. Hernández IM, Dehouck Y, Bastolla U, López-Blanco JR, Chacón P (2023) Predicting
protein stability changes upon mutation using a simple orientational potential. Bioinformatics
39:btad011.
28. Jumper J, Evans R, Pritzel A, Green T, Figurnov M, Ronneberger O, Tunyasuvunakool
K, Bates R, Žídek A, Potapenko A, et al. (2021) Highly accurate protein structure prediction
with AlphaFold. Nature 596:583–589.
29. Tsuboyama K, Dauparas J, Chen J, Laine E, Mohseni Behbahani Y, Weinstein JJ,
Mangan NM, Ovchinnikov S, Rocklin GJ (2023) Mega-scale experimental analysis of protein
folding stability in biology and design. Nature 620:434–444.
30. Reeves S, Kalyaanamoorthy S (2024) Zero-shot transfer of protein sequence likelihood
models to thermostability prediction. Nat Mach Intell 6:1063–1076.

15
31. Godschalk F, Genheden S, Söderhjelm P, Ryde U (2013) Comparison of MM/GBSA
calculations based on explicit and implicit solvent simulations. Phys Chem Chem Phys
15:7731–7739.
32. Onufriev AV, Case DA (2019) Generalized Born Implicit Solvent Models for
Biomolecules. Annu Rev Biophys 48:275–296.
33. Pucci F, Bernaerts KV, Kwasigroch JM, Rooman M (2018) Quantification of biases in
predictions of protein stability changes upon mutations. Bioinformatics 34:3659–3665.
34. Dehouck Y, Grosfils A, Folch B, Gilis D, Bogaerts P, Rooman M (2009) Fast and
accurate predictions of protein stability changes upon mutations using statistical potentials
and neural networks: PoPMuSiC-2.0. Bioinformatics 25:2537–2543.
35. Sasidharan Nair P, Vihinen M (2013) VariBench: a benchmark database for variations.
Hum Mutat 34:42–49.
36. Capriotti E, Fariselli P, Rossi I, Casadio R (2008) A three-state prediction of single point
mutations on protein stability changes. BMC Bioinformatics 9 Suppl 2:S6.
37. Eastman P, Swails J, Chodera JD, McGibbon RT, Zhao Y, Beauchamp KA, Wang L-P,
Simmonett AC, Harrigan MP, Stern CD, et al. (2017) OpenMM 7: Rapid development of high
performance algorithms for molecular dynamics. PLoS Comput Biol 13:e1005659.
38. Pancotti C, Benevenuta S, Birolo G, Alberini V, Repetto V, Sanavia T, Capriotti E,
Fariselli P (2022) Predicting protein stability changes upon single-point mutation: a thorough
comparison of the available tools on a new dataset. Brief Bioinform 23:bbab555.



























16














.


.
