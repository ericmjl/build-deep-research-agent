---
title: "Protein 3D Graph Structure Learning for Robust Structure-based Protein Property Prediction"
authors: "Yufei Huang, Siyuan Li, Jin Su, Lirong Wu, Odin Zhang, Haitao Lin, Jingqi Qi, Zihan Liu, Zhangyang Gao, Yuyang Liu, Jiangbin Zheng, Stan. ZQ. Li"
year: 2023
source: arxiv
source_id: "2310.11466"
url: "http://arxiv.org/abs/2310.11466v2"
domain: computational-biology
---
Protein 3D Graph Structure Learning for Robust Structure-based
Protein Property Prediction
Yufei Huang*1,2, Siyuan Li*1,2, Lirong Wu1,2, Jin Su1,2, Odin Zhang2,
Haitao Lin1,2, Jingqi Qi3, Zihan Liu1,2, Zhangyang Gao1,2, Yuyang Liu2, Jiangbin Zheng1,2,
Stan Z. Li2†
1 Zhejiang University, Hangzhou
2 AI Lab, Research Center for Industries of the Future, Westlake University
huangyufei, lisiyuan, sujin, wulirong, linhaitao, zhengjiangbin, Stan.ZQ.Li@westlake.edu.cn,
liuyuyang@gmail.com, jingqq@uw.edu
Abstract
Protein structure-based property prediction has emerged as
a promising approach for various biological tasks, such as
protein function prediction and sub-cellular location estima-
tion. The existing methods highly rely on experimental pro-
tein structure data and fail in scenarios where these data are
unavailable. Predicted protein structures from AI tools (e.g.,
AlphaFold2) were utilized as alternatives. However, we ob-
served that current practices, which simply employ accu-
rately predicted structures during inference, suffer from no-
table degradation in prediction accuracy. While similar phe-
nomena have been extensively studied in general fields (e.g.,
Computer Vision) as model robustness, their impact on pro-
tein property prediction remains unexplored. In this paper,
we first investigate the reason behind the performance de-
crease when utilizing predicted structures, attributing it to
the structure embedding bias from the perspective of struc-
ture representation learning. To study this problem, we iden-
tify a Protein 3D Graph Structure Learning Problem for Ro-
bust Protein Property Prediction (PGSL-RP3), collect bench-
mark datasets, and present a protein Structure embedding
Alignment Optimization framework (SAO) to mitigate the
problem of structure embedding bias between the predicted
and experimental protein structures. Extensive experiments
have shown that our framework is model-agnostic and ef-
fective in improving the property prediction of both pre-
dicted structures and experimental structures. The benchmark
datasets and codes will be released to benefit the community.
1
Introduction
Proteins are workhorses of the cell, involved in various bio-
logical processes, such as immune response and DNA repli-
cation. Understanding the properties of proteins is important
for deciphering the mystery of life (Degn et al. 2023; Hu
et al. 2022) and treating various diseases (Rossi Sebastiano
et al. 2022; Zheng et al. 2023). As most protein properties
are governed by their folded structures, protein structure-
based property prediction has emerged as a promising ap-
proach for various biological tasks, such as protein function
*These authors contributed equally.
†Corresponding Author
Copyright © 2023, Association for the Advancement of Artificial
Intelligence (www.aaai.org). All rights reserved.
prediction (Huang et al. 2023), sub-cellular location estima-
tion (Zhang et al. 2022), structure-based drug design (Lin
et al. 2022a, 2023a), and antibody design (Kong, Huang, and
Liu 2022).
The existing methods’ reliance on experimental protein
structures poses a challenge when such structures are un-
available. Predicted protein structures from tools like Al-
phaFold2 have been utilized as alternatives. However, for
various structure-based protein property prediction methods,
even if these predicted structures are accurate, using them
during inference also results in a notable decrease in prop-
erty prediction accuracy. (as illustrated in Fig.1(a)). This
suggests that there is a deeper factor behind the accuracy
of predicted structures that misleads structure-based predic-
tors. Similar phenomena also occur in other fields where new
samples with small and hidden differences from the orig-
inal ones can easily fool networks in making predictions
for downstream tasks. In Computer Vision, when we apply
small and invisible perturbations to a panda picture, the neu-
ral network misclassifies it to gibbon (Goodfellow, Shlens,
and Szegedy 2015). Graph Neural Network is also known
to be vulnerable to small perturbations like adding or delet-
ing a few edges (Jin et al. 2020). While developing robust
algorithms(e.g., Graph Structure Learning, GSL (Liu et al.
2022; Jin et al. 2020)) to resist permutations has been well
studied in general domains, model robustness in structure-
based protein property predictions remains unexplored.
Therefore, in this paper, we investigate the decrease in
prediction accuracy when using accurately predicted protein
structures. It is attributed to the structure embedding bias
of predictors from the perspective of structure representa-
tion learning, i.e., a distribution gap between embedding of
accurately predicted structure and that of experimental struc-
ture as shown in Fig.1(b). We further formulate this problem
as Protein 3D Graph Structure Learning for Robust Protein
Property Prediction (PGSL-RP3). Improved predicted struc-
tures don’t necessarily lead to better prediction results due
to the structure embedding bias; the strategy of structure re-
finement, i.e., further improving the structure prediction ac-
curacy, can’t completely alleviate the performance decrease.
To address these issues, we propose to align the represen-
tation of the predicted structure to that of the experimental
arXiv:2310.11466v2  [cs.LG]  19 Oct 2023

Exp. Struct.
Property
Predictor
F1-score:
0.756 
AlphaFold
Protein Sequence
Pred. Struct.
Property
Predictor
F1-score:
0.584 
Perf. Drop:
-0.172
Avg.
TM-Score:
0.929
Why did it drop so much?
(a) Performance Drop
Experimental
Structure
Predicted
Structure
Bias
Vanilla
SAO
(b) Embedding Bias
Figure 1: The illustration of our finding problem. (a) Per-
formance drop on EC task. TM-score is a widely used met-
ric for structure prediction accuracy (b) The illustration of
vanilla and our learned protein structure embedding of a
subset of GOCC dataset by t-SNE. The Red is experimen-
tal structure embedding, and the blue is predicted structure
embedding. There is a clear bias between the predicted and
experimental structures in embeddings from vanilla encoder
but embeddings from SAO-pretrained encoder tend to be
smoother and bias-free.
structure rather than directly improving the similarity (e.g.,
structure prediction accuracy) between predicted and exper-
imental structures in data space. To achieve this, we present
the protein Structure embedding Alignment Optimization
framework (SAO). In SAO, we create pairs of predicted and
experimental structures and train the encoder to align the
predicted structure representation with the corresponding
experimental structure representation using a bootstrap and
denoising approach. One advantage of our alignment-based
framework is its ability to leverage paired information from
both predicted and experimental structures, resulting in im-
proved representation learning performance compared to us-
ing a single data source alone. Additionally, our framework
can utilize low-precision predicted structures that are often
overlooked, further enhancing its effectiveness.
Our contributions can list as follows:
• We identify and formulate the problem of predicted
structure embedding bias as Protein 3D Graph Structure
Learning. To help further solve the problem, we collected
relevant predicted structures and designed a comprehen-
sive benchmark test. Datasets and codes will be released
to benefit the community.
• We propose the protein Structure embedding Alignment
Optimization framework (SAO) to alleviate the structure
embedding bias.
• We conduct extensive experiments in our designed
benchmark test. The results show our superior perfor-
mance over various baselines and the ability to improve
the property prediction of both predicted structures and
experimental structures.
2
Related Work
Protein Structure Representation Model. Graph neural
networks (Wu et al. 2022b, 2023a) were applied to protein
structure representation (Baldassarre et al. 2021; Gligori-
jevi´c et al. 2021), with promising results in protein structure
design (Ingraham et al. 2019; Dauparas et al. 2022). With the
rise of geometric deep learning (Lin et al. 2023b; Wu et al.
2022a, 2023b), Equivariant Neural Networks(ENN) began
to be applied to protein representation, allowing us to di-
rectly learn protein structures end-to-end and achieve more
powerful results (Hsu et al. 2022; Jing et al. 2020; Wu and
Cheng 2022). Inspired by AlphaFold (Jumper et al. 2021),
many works have tried to combine sequence and structure
representation, expecting that co-modeling can combine the
advantages of both modalities (Lin et al. 2022b; Mansoor
et al. 2021; You and Shen 2022; Wu et al. 2023a).
Protein Data Mining with Predicted Structure. With the
introduction of AlphaFold2, many unknown structures have
been solved predictively, which has fuelled the enthusiasm
to transform large amounts of predicted structure into valu-
able knowledge (Shi et al. 2019; Degn et al. 2023). Some
progress has been made in certain areas (Al-Masri et al.
2022; Rossi Sebastiano et al. 2022; Degn et al. 2023). In
particular, areas with less mainstream attention, such as
rare disease research, are expected to benefit greatly from
AlphaFold2’s predicted structures (Rossi Sebastiano et al.
2022). At the same time, there is also a growing interest
in the quality of knowledge generated by predictive struc-
tures, and there are now a number of relevant evaluation
studies (Shi et al. 2019; Degn et al. 2023; Pan et al. 2022).
However, current studies still focus on the accuracy of the
prediction and ignore the structure embedding bias that
the predicted structure itself may carry. EquiPPIS (Roche
et al. 2022) has considered the problem of generalization
to predicted structures and designed an equivariant neural
network-based model for a specific task to alleviate this is-
sue. We go further to reveal the nature of the problem and
formulate it as the PGSL problem, thus proposing a more
efficient and universal framework for its solution. More re-
lated work can be referred to the Appendix A.
3
Preliminaries
Notions Protein data can be modeled at multiple levels:
sequence, amino acid level, full atom level, etc. Here we
model proteins uniformly as an Attributed Relational Graph:
G = (V, E, N, R), where V represents the ordered set of
graph nodes (can be amino acids or atoms) and E ∈V × V
represents the corresponding set of edges connecting the
nodes (some relationship between nodes, e.g., distance less
than 4 ˚A). Every vertex v ∈V in G can have both scalar
and vector attributes nv = (Sv, Vv) ∈N, where Sv ∈RS
and Vv ∈R3×V . Similarly, each edge e ∈E have attributes
rv = (Se, Ve) ∈R, where Se ∈RN and Ve ∈R3×T . G can
contain empty sets. When the sets E and R are empty sets,
G degenerates to a single sequence representation. Further-
more, if N contains only amino acid composition, G degen-
erates to the amino acid sequence.
PGSL for Protein Property Prediction. The aim of
structure-based protein property prediction is to predict
(classify or regress) the property of a protein given its struc-
ture. The Protein 3D Graph Structure Learning problem
(PGSL) extends protein structures from experimental to pre-
dicted structures. Its goal is to enable protein structure rep-
resentation models to align predicted structures to exper-
imental structures, thus enabling representation models to

better handle large numbers of predicted protein structures
and improve humanity’s understanding of unknown pro-
teins. Specifically for Protein Property Prediction, PGSL for
Robust Protein Property Prediction (PGSL-RP3) requires
that structure-based protein property prediction models can
make correct annotations on predicted protein structures and
experimental structures.
We propose two different views for understanding PGSL-
RP3 in Fig.2, which also correspond to two types of solution
ideas. The second one is adopted in our SAO framework.
Further preliminaries can be found in Appendix B.
Structure
Refinement
Property
Predictor
Embedding
Alignment
Property
Predictor
(n,d)
(n,d)
Structure
View
Embedding
View
Predicted Structure
Experimental Structure
Predicted Structure
Embedding
Experimental Structure
 Embedding
Figure 2: An illustration of PGSL-RP3 and two different
views for understanding the problem. The alignment (or pro-
tein 3D graph structure learning) from the predicted struc-
ture to the experimental structure can occur in either the
structure space or the embedding space.
4
Protein Structure Embedding Alignment
Optimization Framework
Problem Analysis and Motivation
The comparisons between PGSL and GSL motivate us to
analyze PGSL from the perspective of embedding. PGSL is
similar to GSL in that they both expect a cleaner graph struc-
ture to improve performance on downstream tasks. GSL
usually focuses on node classification tasks on 2D graphs,
where the modifications of the graph structure are gener-
ally discrete operations such as the addition and deletion of
edges. Different from GSL, PGSL focuses on graph classifi-
cation tasks on 3D graphs, similar to 3D point clouds, where
the modifications of the graph structure are continuous op-
erations, such as the modification of node coordinates. As
a result, it is difficult to migrate methods directly from the
GSL domain to PSGL. However, the idea of node embed-
ding alignment in unsupervised graph structure learning in-
spires us to explore PGSL from the embedding view.
As a result, we propose the SAO framework for align-
ment in Embedding Space as illustrated in Fig.3(a). Instead
of optimizing the structure directly, our framework used the
idea of representation learning to move the embedding of
predicted structures toward that of the experimental struc-
tures. In practice, we first pretrain the protein encoder based
on the SAO framework to give it the ability to migrate rep-
resentations of predicted structures towards that of experi-
mental structures. Then, by fine-tuning the encoder on spe-
cific tasks, as in Fig.3(b), the model learns to associate rep-
resentations and labels together. Since the property predic-
tion problem is essentially carried out based on the struc-
ture embedding, such an idea can instead improve the model
robustness more directly. Our proposed framework will be
discussed in the following subsections.
Directional Embedding Alignment
The motivation of the first module is to help the model
achieve Direction Embedding Alignment. Noting that there
is actually only some natural mapping relationship between
the experimental protein structure and its properties, we
should learn the correlation between protein structure and
properties based on the experimental structure. Therefore,
we need to align the embedding of the predicted structure
with the embedding of the experimental structure.
To achieve this, we propose a one-way embedding align-
ment method, drawing on bootstrap-based contrastive learn-
ing methods (Grill et al. 2020; Chen and He 2020). Our
method is based on the student-teacher architecture, where
the parameters ϕ of the teacher network (a.k.a. Target net-
work) are the exponential moving average of the parameters
θ of the student network (also known as Online network)
and only the parameters of the student encoder are trainable.
More precisely, given a target decay rate λ, the following
updates are performed after each training iteration,
ϕ ←λϕ + (1 −λ)θ.
(1)
The online network is comprised of three stages: an encoder
fθ, a projector gθ, and a predictor qθ. The target network
and online network have the same architecture, except that
there is no predictor. The embedding outputs of both the stu-
dent encoder and teacher encoder are fed into an embedding
projector as shown in Figure 3(a).
Given a set S of paired protein structures, a protein struc-
ture pair sampled uniformly from S, the teacher network
takes the experimental structure as input and outputs a rep-
resentation zϕ of the experimental structure as the prediction
target. The student network takes the predicted structure as
input. It outputs a representation zθ of the predicted struc-
ture that goes through the predictor qθ to be aligned with the
experimental structure representation. We can ℓ2-normalize
both qθ(zθ) and zϕ to qθ(zθ) ≜qθ(zθ)/ ∥qθ(zθ)∥2 and
zϕ ≜(zϕ)/ ∥(zϕ)∥2. The loss function is as follow:
Lθ,ϕ
align ≜∥qθ(zθ) −zϕ∥2
2 = 2−2·
⟨qθ(zθ), zϕ⟩
∥qθ(zθ)∥2 · ∥zϕ∥2
, (2)
where the first part (i.e., ℓ2-norm loss) is equal to cosine
similarity loss.
The loss Lθ,ϕ
align is asymmetric to ensure directional em-
bedding alignment, and the network always uses the repre-
sentation of the predicted structure to predict the representa-
tion of the experimental structure. It is worth noting that we
only optimize the loss Lθ,ϕ
align according to θ, for the target
network with ϕ we use a gradient-stopping technique. Af-
ter pretraining, we only keep the online encoder as shown in
Figure 3(b).

Online
Encoder
Target
Encoder
?
Projector
Predictor
Projector
Denoise
Decoder
Mask Pred.
Head
Pred. Struct.
Masked. Struct.
Exp. Struct.
Recon. Struct
Denoised. Struct
EMA
EMA
stop-grad
alignment loss
①
②
③
AlphaFold
Protein Sequence
(a) The SAO Framework
Online
Encoder
Exp. Struct.
(pretrained->fine-tuned)
Task Head
Training
Inference
Structures of
interest
Pred. Struct.
Exp. Struct.
Mixed Sources
Structures
with labels
Task-specific
losses
Knowledge
or
(b) The finetuning and inference scheme
Figure 3: The illustration of SAO Framework. (a) We first pretrain the encoder in SAO framework for the ability of directional
embedding alignment (b). Then we finetune the encoder on specific downstream tasks. Finally, we can turn structures of interest
(predicted or experimental) into new knowledge(predict its various properties) to guide scientific discovery.
Embedding Bootstrap Mechanism
To give the encoder
persistent guidance and avoid over-fitting in the experimen-
tal representation, we use the embedding bootstrap mecha-
nism to provide a self-enhanced experimental structure em-
bedding as the learning target. Considering that the embed-
ding is ultimately reflected in the parameters, our core idea is
to update the target encoder with an exponential moving av-
erage of the learned online encoder as in equation 1 instead
of keeping it unchanged.
Mask View as Embedding Augmentation
The feasible solutions in the above framework include col-
lapsed representation (e.g., constant representation across
sources is always fully predictive of itself). However, Lθ,ϕ
align
is not a loss such that SAO’s dynamics is a gradient descent
on L jointly over θ, ϕ. There is, therefore, no a priori rea-
son why SAO’s parameters would converge to an undesirable
minimum of Lθ,ϕ
align (Grill et al. 2020).
Furthermore, to avoid the undesirable equilibria in SAO’s
dynamics, we introduce the Mask view as Embedding Aug-
mentation (as shown in Fig.3(a)). We mask the protein se-
quence of the experimental structure and keep the structure
visible to create a mask view. Then we align the embed-
ding of the masked structure toward that of the experimental
structure following the same procedure we operate on the
predicted structure. It has the following two advantages.
Increase Variability for Avoiding Collapse
The techni-
cal consideration behind this is to propagate new sources of
variability captured by the online projection into the target
projection. As shown in (Grill et al. 2020), increasing vari-
ability across sources could make these collapsed constant
equilibria unstable. The variability between the predicted
and experimental structure is limited because, as we men-
tioned above, the difference between the two is mainly in
embedding bias when the prediction accuracy is high.
Embedding Augmentation for Better Alignment
An-
other motivation behind introducing the mask view is to in-
crease the ability of the framework to align embedding from
other sources to the experimental structural embedding. Due
to the small variability between the predicted and experi-
mental structures, the model is more prone to overfitting and
loss of generalizability. The predicted structure mainly car-
ries global variability, so we consider proposing augmen-
tation with contextual variability to enhance the ability of
directional embedding alignment of our framework.
Structure Denoising Guidance
To ensure meaningful representations that can be decoded
into cleaner structures and guide the directional embedding
alignment, we incorporate a structure denoising task.
Instead of reducing the amino acid molecule to a single
Cα atom, we pursued a finer-grained modeling, so we con-
sidered all the amino acid backbone atoms (C, N, O, Cα).
Considering physical plausibility (the bond lengths and bond
angles between backbone atoms are relatively fixed, i.e., the
relative positions between backbone atoms can be consid-
ered fixed), we modeled the backbone atoms as a frame, such
that an amino acid backbone structure is determined by two
vector properties: translation t (coordinates of the Cα atom)
and orientation O (which determines the final coordinates):
P = {(ti, Oi)}i=N
i=1
and xa
i = Oixa
stand + ti·
(3)
where P is the protein backbone structure, N is the length
of the protein sequence, xa
i is the a-type backbone atom of
residue i (a ∈C, N, O, Cα). xa
stand is the standard coor-
dinate of the a-type amino acid backbone atom when the
Cα atom is at the origin and under the unit orthogonal
group (Jumper et al. 2021).
Given a predicted protein structure P, the online encoder
maps it into embedding. A denoise decoder head predicts the
direction of conformational change for further optimization.

Models
Inference Setting
EC
GO-MF
GO-CC
GO-BP
Fmax
AUPR
Fmax
AUPR
Fmax
AUPR
Fmax
AUPR
IPA-Encoder
Predicted (TM ≥0.5)
0.568 (+0.156)
0.505 (+0.187)
0.492 (+0.055)
0.493 (+0.071)
0.383 (+0.061)
0.174 (+0.072)
0.311 (+0.039)
0.194 (+0.027)
Predicted (pLDDT ≥70)
0.579 (+0.158)
0.521 (+0.203)
0.494 (+0.056)
0.491 (+0.068)
0.362 (+0.084)
0.167 (+0.082)
0.312 (+0.040)
0.198 (+0.037)
Experimental Structure
0.711 (+0.054)
0.707 (+0.046)
0.522 (+0.025)
0.518 (+0.040)
0.433 (+0.024)
0.248 (+0.015)
0.338 (+0.023)
0.218 (+0.016)
The Performance Gap
-0.132 (+0.104)
-0.186 (+0.157)
-0.028 (+0.031)
-0.027 (+0.028)
-0.071 (+0.060)
-0.081 (+0.067)
-0.026 (+0.017)
-0.02 (+0.021)
Uni-Mol
Predicted (TM ≥0.5)
0.520 (+0.315)
0.475 (+0.341)
0.385 (+0.195)
0.385 (+0.184)
0.333 (+0.078)
0.152 (+0.083)
0.267 (+0.115)
0.149 (+0.107)
Predicted (pLDDT ≥70)
0.528 (+0.305)
0.486 (+0.332)
0.397 (+0.187)
0.391 (+0.176)
0.343 (+0.068)
0.162 (+0.077)
0.267 (+0.115)
0.151 (+0.108)
Experimental Structure
0.657 (+0.155)
0.643 (+0.150)
0.415 (+0.156)
0.398 (+0.142)
0.402 (+0.030)
0.203 (+0.056)
0.314 (+0.070)
0.203 (+0.049)
The Performance Gap
-0.129 (+0.150)
-0.157 (+0.182)
-0.018 (+0.031)
-0.007 (+0.034)
-0.059 (+0.038)
-0.041 (+0.021)
-0.047 (+0.045)
-0.052 (+0.059)
REINet
Predicted (TM ≥0.5)
0.584 (+0.147)
0.506 (+0.193)
0.519 (+0.028)
0.521 (+0.033)
0.337 (+0.105)
0.171 (+0.054)
0.340 (+0.032)
0.227 (+0.020)
Predicted (pLDDT ≥70)
0.599 (+0.153)
0.546 (+0.184)
0.526 (+0.030)
0.518 (+0.039)
0.335 (+0.104)
0.177 (+0.048)
0.340 (+0.033)
0.229 (+0.024)
Experimental Structure
0.756 (+0.038)
0.755 (+0.026)
0.535 (+0.013)
0.540 (+0.011)
0.427 (+0.021)
0.251 (-0.010)
0.360 (+0.019)
0.248 (+0.007)
The Performance Gap
-0.157 (+0.115)
-0.209 (+0.158)
-0.009 (+0.017)
-0.022 (+0.028)
-0.092 (+0.083)
-0.074 (+0.058)
-0.020 (+0.014)
-0.019 (+0.017)
Table 1: Downstream task performance of three inference settings across three encoders. Results in parentheses (bold) are
performance gain training with SAO framework, the performance gap is calculated by values of Predicted(Plddt ≥70) - values
of Experimental Structure. Results clearly show SAO is effective across tasks and model-agnostic.
Formally, we can formulate this process as follows:
{(∆ti, ∆Oi)}i=N
i=1 = E(P),
ti = ti + ∆ti and Oi = Oi ◦∆Oi·
(4)
where E is the equivariant neural network and ◦corresponds
to the composition of elements in SO(3) group. we use the
MSE loss under the local frame (Jumper et al. 2021) as the
training objective:
Lmse = Meani,j
q
∥T −1
i
◦xj −T true−1
i
◦xtrue
j
∥2·
(5)
where i ∈{1, · · · , Nres}, j ∈{C, N, O, Cα}, Ti and T true
i
corresponds to the predicted and ground truth frame (O, t)
of residue i. And T −1
i
◦xj = O−1
i
(xj −ti) converts the co-
ordinates of backbone atoms from the global to local frame.
More details can be referred to Appendix. C.
Overall Framework
In this subsection, we first illustrate the training process
of SAO, and then briefly introduce our model architecture.
Model training. In our training process, we first pretrain
the protein structure encoder in SAO framework on the cor-
responding downstream task dataset (i.e., no new sample is
added during pretrain). The overall pretraining objective is
LSAO = γ1Lalign+γ2Lmlm+γ3Lmse as figure 3(a) shows.
Lmlm is the standard mask language modeling loss (De-
vlin et al. 2019), and γ is the loss weight (value setups are
shown in Appendix. E). Then we fine-tune the encoder on
the downstream task using task-specific losses(as shown in
fig.3(b)). The algorithmic description and more details, in-
cluding the mask ratio, are provided in Appendix E.
Frame-Aware 3D Graphformer. Our SAO framework is
model-agnostic, allowing for compatibility with various
models. Additionally, we propose a simple yet effective en-
coder named REInet that can co-model the 3D geometry of
amino acid coordinates and the 1D protein sequences. As
the model architecture is not our main concern, we defer its
detailed introduction to the Appendix. D.
5
Experiments
In this section, we first introduce the experimental setup for
four standard protein property prediction tasks, including
Enzyme Commission number prediction, and Gene Ontol-
ogy term prediction following
(Gligorijevi´c et al. 2021),
model architectures, and robust training framework base-
lines. We then conduct empirical experiments to demon-
strate the effectiveness of the proposed framework SAO. We
aim to answer five research questions as follows: Q1: Does
the protein structure embedding bias problem generally exist
in various protein property prediction tasks across different
predictors? Q2: Are our proposed framework SAO model-
agnostic? Q3: How effective is SAO for PGSL-RPA? Q4:
How do key framework components impact the performance
of SAO? Q5: How robust is SAO to less accurate or non-
AlphaFold predicted protein structures?
Experimental Setups
Downstream tasks for evaluation
We adopt four tasks
proposed in (Gligorijevi´c et al. 2021) as downstream tasks
for evaluation. Enzyme Commission (EC) number predic-
tion aims to forecast the EC numbers of various proteins,
which describe their catalysis of biological activities in a
tree structure. It’s a multi-label classification task with 538
categories. Gene Ontology(GO) term prediction aims to an-
notate a protein with GO terms that describe the Molecular
Function (MF) of gene products, the Biological Processes
(BP) in which those actions occur, and the Cellular Compo-
nent (CC) where they are present. Thus, GO term prediction
is actually composed of three different sub-tasks: GO-MF,
GO-BP, GO-CC. And two metrics are employed, includ-
ing the maximum F-score (Fmax) and AUPR (Zhang et al.
2022).
Inference Setting
To evaluate SAO in realistic scenarios,
we choose three inference settings: 1) inference with the
experimental structure; 2) inference with predicted protein
structure with TMScore ≥0.5 3) inference with predicted
protein structure with pLDDT ≥70. TMscore and pLDDT

Inference Setting
Robust Training
Framework
EC
GO-MF
GO-CC
GO-BP
Fmax
AUPR
Fmax
AUPR
Fmax
AUPR
Fmax
AUPR
TMscore ≥0.5
Vanilla
0.584
0.506
0.519
0.521
0.337
0.171
0.340
0.227
TonP
0.731
0.693
0.537
0.547
0.414
0.266
0.371
0.263
Mixed
0.667
0.620
0.534
0.537
0.440
0.234
0.365
0.257
RefthenPred
0.562
0.616
0.524
0.524
0.341
0.184
0.345
0.231
RefandPred
0.667
0.623
0.501
0.505
0.396
0.194
0.337
0.224
SAO(ours)
0.731
0.699
0.547
0.554
0.442
0.225
0.372
0.247
pLDDT ≥70
Vanilla
0.599
0.546
0.526
0.518
0.335
0.177
0.340
0.229
TonP
0.750
0.716
0.544
0.547
0.419
0.273
0.371
0.269
Mixed
0.675
0.635
0.542
0.534
0.433
0.224
0.366
0.265
RefthenPred
0.627
0.587
0.531
0.523
0.336
0.188
0.347
0.235
RefandPred
0.680
0.644
0.511
0.508
0.400
0.212
0.337
0.229
SAO(ours)
0.752
0.730
0.556
0.557
0.439
0.225
0.373
0.253
Experimental
Structure
Vanilla
0.746
0.745
0.535
0.540
0.427
0.251
0.360
0.248
TonP
0.543
0.430
0.388
0.357
0.334
0.165
0.279
0.173
Mixed
0.676
0.575
0.520
0.510
0.432
0.215
0.364
0.247
RefthenPred
0.746
0.745
0.535
0.54
0.427
0.251
0.36
0.248
RefandPred
0.742
0.730
0.512
0.506
0.425
0.221
0.345
0.227
SAO(ours)
0.784
0.771
0.548
0.551
0.448
0.241
0.379
0.255
Table 2: Performance comparison across different robust training framework baselines. Our SAO surpasses most baselines
across different tasks and inference settings, which shows its effectiveness and advantage of using paired protein structure data.
The best and second results are marked by bold and underline.
are commonly used criteria for selecting accurately pre-
dicted protein structures for downstream applications.
Model architectures
We explore the PGSL-RAP prob-
lem in various protein structure encoder architectures, in-
cluding graph neural network-based GearNet Edge (Zhang
et al. 2022), graphormer-based Uni-Mol (Zhou et al. 2022),
equivariant neural network IPA (Jumper et al. 2021) and
3D Graphormer REInet. Implementation and training details
can be referred to Appendix. D and E. For simplicity, we use
REInet as the encoder in subsequent experiments unless oth-
erwise specified.
Baselines and Training
We mainly compare SAO with
two categories of methods, including three directly training-
based methods: 1. vanilla method of training on experi-
mental protein structures of downstream tasks(Vanilla); 2.
training on predicted protein structure(TonP); 3. training on
the mixture of predicted and experimental protein structure
for direct adaptation(Mixed). And two protein structure re-
finement(e.g., improving the similarity of the predicted and
experimental structures directly in Euclidean space) based
methods are further included: 1. RefthenPred which refine
the protein structure before predicting its property; 2. Re-
fandPredict which refine the protein structure while predict-
ing its property. The RefthenPred is like unsupervised GSL,
which obtains clean graph structure without supervision sig-
nals; we use the SOTA protein structure refinement method
ATOMRefine (Wu and Cheng 2022) for refinement. And the
RefandPred is like supervised GSL, which refines the graph
structure under supervision. We add one layer of simplified
Structure Module (Jumper et al. 2021) after the structure en-
coder to refine the protein structure while predicting protein
properties.
Following (Gligorijevi´c et al. 2021), we use the multi-
cutoff split methods for EC and GO tasks to guarantee the
test set contains only PDB chains with sequence identity less
than 95% to the training set. We pretrain encoders under
SAO for 400 epochs on structures of corresponding down-
GearNet_Edge
IPA-Encoder
Uni-Mol
Inference Setting
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
Fmax
Experimental
Plddt>70
TMScore>0.5
(a) EC
GearNet_Edge
IPA-Encoder
Uni-Mol
Inference Setting
0.20
0.25
0.30
0.35
0.40
0.45
0.50
Fmax
Experimental
Plddt>70
TMScore>0.5
(b) GO-CC
Figure 4: Fmax on EC and GO-CC tasks across different
encoder architectures in different inference settings. Repre-
sentative encoders suffer from performance degradation on
predicted structures.
stream tasks and then fine-tune them on downstream tasks
for specific epochs (EC: 100 epochs, GO-CC: 45 epochs,
GO-MF and GO-BP: 100 epochs). Warmup and the expo-
nential learning rate decay schedule are used with a start
learning rate of 0.0, a max learning rate of 1e-4, and a de-
cay factor of 0.99. For other experimental details, interested
readers can refer to the Appendix.
Empirical studies (Q1)
Fig.4 shows how well different methods predict cer-
tain properties of proteins in various tasks. The methods
are trained on experimental protein structures, following
(Zhang et al. 2022). Then, they are tested in three differ-
ent inference settings, including two settings with predicted
protein structures. As can be observed, all three models per-
form worse when making predictions with predicted protein
structures. This suggests that there is a general issue of pro-
tein structure embedding bias, which affects protein prop-
erty prediction tasks across different prediction methods. In-
terested readers can find numerical results on more tasks in

Appendix. F.
Performance of SAO across different encoders (Q2)
Table 1 shows the performance of SAO framework across
different protein structure encoders. It indicates that SAO
framework is model-agnostic and effective in improving
the prediction accuracy of both experimental and predicted
structures. With SAO, encoders can learn to align the embed-
dings of predicted structures to that of experimental struc-
tures and output meaningful embeddings. It’s worth not-
ing that the property prediction performance with predicted
protein structures surpasses that with experimental protein
structures in some settings, which shows the value of the
idea of directional embedding alignment.
Performance Comparison (Q3)
Table 2 reports the classification performance of our frame-
work and other baselines in experimental and predicted pro-
tein structure inference scenarios. We can observe that our
proposed SAO outperforms all baselines on 8 out of 8 met-
rics ( 2 for each property prediction task). This superior per-
formance benefits from the novel idea of guiding PGSL in
embedding space with a self-enhanced learning target by di-
rectional embedding alignment.
We make other observations as follows. Firstly, the perfor-
mances of training predictors on experimental or predicted
protein structures are both notably biased. It is even worse
when training on predicted protein structures. This obser-
vation provides another evidence of protein structure em-
bedding bias. Secondly, SAO can surpass all three directly
training-based baselines, indicating SAO can make better use
of paired experimental-predicted data. Thirdly, compared to
refinement-based baselines (whether supervised or not), our
unsupervised embedding-based methods also achieve better
results, which shows our effectiveness.
Inference Setting
Robust Training Framework
GO-CC
Fmax
AUPR
TMscore ≥0.5
Vanilla
0.337
0.171
SAO
0.442
0.226
w/o structure denoising guidance
0.429
0.206
w/o mask view augumentation
0.388
0.201
w/o embedding alignment
0.389
0.203
w/o mask language modeling
0.422
0.209
Experimental
Structure
Vanilla
0.427
0.251
SAO
0.449
0.252
w/o structure denoising guidance
0.432
0.218
w/o mask view augumentation
0.412
0.240
w/o embedding alignment
0.438
0.234
w/o mask language modeling
0.419
0.238
Table 3: Ablation study for designed components in two in-
ference scenarios. The best metrics are marked by bold.
Ablation Study (Q4)
To study the importance of every component in SAO, we
perform an ablation study on every loss term. As shown in
Table 3, without structure denoising guidance, the classifi-
cation performance decrease by 2% on average, indicating
this component helps improve the quality of learned embed-
ding and the alignment from predicted embeddings to ex-
perimental embeddings. Without embedding alignment, we
can find obvious drops in classification performance, espe-
cially when performing inference on predicted protein struc-
tures. It shows the effectiveness of our directional embed-
ding alignment mechanisms. We can further notice a clear
decline without the mask view augmentation component,
indicating its effectiveness in avoiding embedding collapse
and improving directional alignment as embedding augmen-
tation. Finally, it is unsurprising that mask language model-
ing tasks can improve performance on experimental protein
structures. Due to the page limit, more ablation studies, in-
cluding task weights, can be referred to the Appendix F.
Experimental
Plddt > 70
AtomRefine
70 >= Plddt >= 30
Inference Setting
0.20
0.25
0.30
0.35
0.40
0.45
Fmax
Vanilla
TonP
Mixed
RefandPred
SAO
Figure 5: Fmax on GO-CC task in different inference set-
tings. AtomRefine refers to inferencing with ATOMRefine-
predicted protein structures. Encoders trained under SAO
framework can better handle less accurately predicted pro-
tein structures and non-AlphaFold predicted structures.
More results on predicted structure (Q5)
Figure 5 shows the performance under less accurate pre-
dicted protein structure and non-AlphaFold predicted struc-
ture. The results indicate that SAO can make the encoder
more robust to less accurate predicted protein structures and
generalize well to non-AlphaFold predicted structures.
We attribute its comparative performance to our design
of directional embedding alignment. Directly training-based
baselines may struggle to generalize to other inference set-
tings, although have comparative performances in accurate
AF-predicted structures.
6
Conclusion
This paper investigates 3D protein graph structure learning
and designs a novel framework, SAO, which is capable of
leveraging pair data to perform directional embedding align-
ment. To learn the optimal alignment, we employ bootstrap-
based contrastive learning to maximize the agreement be-
tween predicted structure embeddings and self-enhanced
learning targets. Extensive experiments demonstrate the su-
periority of SAO.
Social Impact and Limitations This paper identifies an un-
derlying problem of current common practices(i.e., using

predicted protein structures from tools like AlphaFold2 as
alternatives when experimental protein structures are miss-
ing). It might help the community to rethink the usage of
massive AlphaFold2 predicted structures. Our study helps
improve the property prediction on predicted protein struc-
tures. It contributes to the global efforts to transform large
amounts of predicted structures into high-quality and valu-
able knowledge for human well-being. Limitations still ex-
ist, including insufficient exploration of Protein 3D Graph
Structure Learning on non-classification tasks and limited
sources of predicted protein structures.
References
Al-Masri, C.; Trozzi, F.; Patek, M.; Cicho´nska, A.; Raviku-
mar, B.; and Rahman, R. 2022. Investigating the confor-
mational landscape of AlphaFold2-predicted protein kinase
structures. bioRxiv.
Baldassarre, F.; Men´endez Hurtado, D.; Elofsson, A.; and
Azizpour, H. 2021. GraphQA: protein model quality assess-
ment using graph convolutional networks. Bioinformatics,
37(3): 360–366.
Chen, X.; and He, K. 2020. Exploring Simple Siamese Rep-
resentation Learning. arXiv:2011.10566.
Dauparas, J.; Anishchenko, I.; Bennett, N.; Bai, H.; Ragotte,
R. J.; Milles, L. F.; Wicky, B. I.; Courbet, A.; de Haas, R. J.;
Bethel, N.; et al. 2022. Robust deep learning–based protein
sequence design using ProteinMPNN. Science, 378(6615):
49–56.
Degn, K.; Beltrame, L.; Tiberti, M.; and Papaleo, E. 2023.
PDBminer to Find and Annotate Protein Structures for Com-
putational Analysis. bioRxiv.
Devlin, J.; Chang, M.-W.; Lee, K.; and Toutanova, K. 2019.
BERT: Pre-training of Deep Bidirectional Transformers for
Language Understanding. arXiv:1810.04805.
Gligorijevi´c, V.; Renfrew, P. D.; Kosciolek, T.; Leman, J. K.;
Berenberg, D.; Vatanen, T.; Chandler, C.; Taylor, B. C.; Fisk,
I. M.; Vlamakis, H.; et al. 2021.
Structure-based protein
function prediction using graph convolutional networks. Na-
ture communications, 12(1): 1–14.
Goodfellow, I. J.; Shlens, J.; and Szegedy, C. 2015.
Explaining
and
Harnessing
Adversarial
Examples.
arXiv:1412.6572.
Grill, J.-B.; Strub, F.; Altch´e, F.; Tallec, C.; Richemond,
P. H.; Buchatskaya, E.; Doersch, C.; Pires, B. A.; Guo, Z. D.;
Azar, M. G.; Piot, B.; Kavukcuoglu, K.; Munos, R.; and
Valko, M. 2020. Bootstrap your own latent: A new approach
to self-supervised Learning. arXiv:2006.07733.
Hsu, C.; Verkuil, R.; Liu, J.; Lin, Z.; Hie, B.; Sercu, T.; Lerer,
A.; and Rives, A. 2022. Learning inverse folding from mil-
lions of predicted structures. ICML.
Hu, B.; Xia, J.; Zheng, J.; Tan, C.; Huang, Y.; Xu, Y.; and
Li, S. Z. 2022. Protein Language Models and Structure Pre-
diction: Connection and Progression. arXiv:2211.16742.
Huang, Y.; Wu, L.; Lin, H.; Zheng, J.; Wang, G.; and Li,
S. Z. 2023. Data-Efficient Protein 3D Geometric Pretraining
via Refinement of Diffused Protein Structure Decoy. arXiv
preprint arXiv:2302.10888.
Ingraham, J.; Garg, V.; Barzilay, R.; and Jaakkola, T. 2019.
Generative models for graph-based protein design.
Ad-
vances in neural information processing systems, 32.
Jin, W.; Ma, Y.; Liu, X.; Tang, X.; Wang, S.; and Tang, J.
2020. Graph Structure Learning for Robust Graph Neural
Networks. In Proceedings of the 26th ACM SIGKDD Inter-
national Conference on Knowledge Discovery & Data Min-
ing, KDD ’20, 66–74. New York, NY, USA: Association for
Computing Machinery. ISBN 9781450379984.
Jing, B.; Eismann, S.; Suriana, P.; Townshend, R. J.; and
Dror, R. 2020. Learning from protein structure with geomet-
ric vector perceptrons. arXiv preprint arXiv:2009.01411.
Jumper, J.; Evans, R.; Pritzel, A.; Green, T.; Figurnov, M.;
Ronneberger, O.; Tunyasuvunakool, K.; Bates, R.; ˇZ´ıdek,
A.; Potapenko, A.; et al. 2021. Highly accurate protein struc-
ture prediction with AlphaFold. Nature, 596(7873): 583–
589.
Kong, X.; Huang, W.; and Liu, Y. 2022. Conditional an-
tibody design as 3d equivariant graph translation.
arXiv
preprint arXiv:2208.06073.
Lin, H.; Huang, Y.; Liu, M.; Li, X.; Ji, S.; and Li, S. Z.
2022a. DiffBP: Generative Diffusion of 3D Molecules for
Target Protein Binding. arXiv preprint arXiv:2211.11214.
Lin, H.; Huang, Y.; Zhang, H.; Wu, L.; Li, S.; Chen, Z.;
and Li, S. Z. 2023a.
Functional-Group-Based Diffusion
for Pocket-Specific Molecule Generation and Elaboration.
arXiv:2306.13769.
Lin, H.; Wu, L.; Xu, Y.; Huang, Y.; Li, S.; Zhao, G.; and
Li, S. Z. 2023b. Non-equispaced Fourier Neural Solvers for
PDEs. arXiv:2212.04689.
Lin, Z.; Akin, H.; Rao, R.; Hie, B.; Zhu, Z.; Lu, W.;
Smetanin, N.; dos Santos Costa, A.; Fazel-Zarandi, M.;
Sercu, T.; Candido, S.; et al. 2022b. Language models of
protein sequences at the scale of evolution enable accurate
structure prediction. bioRxiv.
Liu, Y.; Zheng, Y.; Zhang, D.; Chen, H.; Peng, H.; and
Pan, S. 2022. Towards Unsupervised Deep Graph Structure
Learning. In Proceedings of the ACM Web Conference 2022,
WWW ’22, 1392–1403. New York, NY, USA: Association
for Computing Machinery. ISBN 9781450390965.
Mansoor, S.; Baek, M.; Madan, U.; and Horvitz, E. 2021.
Toward more general embeddings for protein design: Har-
nessing joint representations of sequence and structure.
bioRxiv.
Pan, Q.; Nguyen, T. B.; Ascher, D. B.; and Pires, D. E. V.
2022. Systematic evaluation of computational tools to pre-
dict the effects of mutations on protein stability in the ab-
sence of experimental structures. Briefings in Bioinformat-
ics, 23(2): bbac025.
Roche, R.; Moussad, B.; Shuvo, M. H.; and Bhattacharya, D.
2022. E(3) equivariant graph neural networks for robust and
accurate protein–protein interaction site prediction. bioRxiv.
Rossi Sebastiano, M.; Ermondi, G.; Hadano, S.; and Caron,
G. 2022. AI-based protein structure databases have the po-
tential to accelerate rare diseases research: AlphaFoldDB
and the case of IAHSP/Alsin. Drug Discovery Today, 27(6):
1652–1660.

Shi, Q.; Chen, W.; Huang, S.; Wang, Y.; and Xue, Z. 2019.
Deep learning for mining protein data. Briefings in Bioin-
formatics, 22(1): 194–218.
Wu, L.; Huang, Y.; Lin, H.; Liu, Z.; Fan, T.; and Li, S. Z.
2022a.
Automated Graph Self-supervised Learning via
Multi-teacher Knowledge Distillation. arXiv:2210.02099.
Wu, L.; Lin, H.; Huang, Y.; Fan, T.; and Li, S. Z. 2023a.
Extracting Low-/High- Frequency Knowledge from Graph
Neural Networks and Injecting it into MLPs: An Effective
GNN-to-MLP Distillation Framework. arXiv:2305.10758.
Wu, L.; Lin, H.; Huang, Y.; and Li, S. Z. 2022b. Knowl-
edge Distillation Improves Graph Structure Augmentation
for Graph Neural Networks.
In Koyejo, S.; Mohamed,
S.; Agarwal, A.; Belgrave, D.; Cho, K.; and Oh, A., eds.,
Advances in Neural Information Processing Systems, vol-
ume 35, 11815–11827. Curran Associates, Inc.
Wu, L.; Lin, H.; Huang, Y.; and Li, S. Z. 2023b. Quantifying
the Knowledge in GNNs for Reliable Distillation into MLPs.
arXiv:2306.05628.
Wu, T.; and Cheng, J. 2022. Atomic protein structure re-
finement using all-atom graph representations and SE (3)-
equivariant graph neural networks. bioRxiv.
You, Y.; and Shen, Y. 2022.
Cross-modality and self-
supervised protein embedding for compound–protein affin-
ity and contact prediction.
Bioinformatics, 38(Supple-
ment 2): ii68–ii74.
Zhang, Z.; Xu, M.; Jamasb, A.; Chenthamarakshan, V.;
Lozano, A.; Das, P.; and Tang, J. 2022. Protein represen-
tation learning by geometric structure pretraining.
arXiv
preprint arXiv:2203.06125.
Zheng, J.; Wang, G.; Huang, Y.; Hu, B.; Li, S.; Tan, C.;
Fan, X.; and Li, S. Z. 2023. Lightweight Contrastive Protein
Structure-Sequence Transformation. arXiv:2303.11783.
Zhou, G.; Gao, Z.; Ding, Q.; Zheng, H.; Xu, H.; Wei, Z.;
Zhang, L.; and Ke, G. 2022.
Uni-Mol: A Universal 3D
Molecular Representation Learning Framework. ChemRxiv.
