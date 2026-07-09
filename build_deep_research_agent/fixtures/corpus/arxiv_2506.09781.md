---
title: "On the Similarities of Embeddings in Contrastive Learning"
authors: "Chungpa Lee, Sehee Lim, Kibok Lee, Jy-yong Sohn"
year: 2025
source: arxiv
source_id: "2506.09781"
url: "http://arxiv.org/abs/2506.09781v2"
domain: ai
---
On the Similarities of Embeddings in Contrastive Learning
Chungpa Lee 1 Sehee Lim 1 Kibok Lee 1 Jy-yong Sohn 1
Abstract
Contrastive learning operates on a simple yet ef-
fective principle: Embeddings of positive pairs
are pulled together, while those of negative pairs
are pushed apart. In this paper, we propose a
unified framework for understanding contrastive
learning through the lens of cosine similarity, and
present two key theoretical insights derived from
this framework. First, in full-batch settings, we
show that perfect alignment of positive pairs is
unattainable when negative-pair similarities fall
below a threshold, and this misalignment can be
mitigated by incorporating within-view negative
pairs into the objective. Second, in mini-batch
settings, smaller batch sizes induce stronger sep-
aration among negative pairs in the embedding
space, i.e., higher variance in their similarities,
which in turn degrades the quality of learned rep-
resentations compared to full-batch settings. To
address this, we propose an auxiliary loss that re-
duces the variance of negative-pair similarities in
mini-batch settings. Empirical results show that
incorporating the proposed loss improves perfor-
mance in small-batch settings.
1. Introduction
Contrastive learning (CL) has emerged as a powerful ap-
proach to representation learning (Chen & He, 2021; Chen
et al., 2020; He et al., 2020; Radford et al., 2021; Zhai et al.,
2023; Khosla et al., 2020). In CL, an embedding model is
trained to produce similar representations for two different
views of the same data instance—referred to as a positive
pair—and dissimilar representations for views from differ-
ent data instances—referred to as negative pairs. Recent
empirical studies have shown that representations learned by
these objectives, i.e., aligning positive pairs while separat-
1Department of Statistics and Data Science, Yonsei Uni-
versity, Seoul, Korea.
Correspondence to:
Jy-yong Sohn
<jysohn1108@yonsei.ac.kr>.
Proceedings of the 42 nd International Conference on Machine
Learning, Vancouver, Canada. PMLR 267, 2025. Copyright 2025
by the author(s).
ing negative pairs, achieve remarkable performance across
various downstream tasks (Wang & Isola, 2020).
In parallel, several theoretical studies have analyzed the
embeddings obtained by CL in full-batch settings. Lu &
Steinerberger (2022) showed that the widely used InfoNCE
loss (Oord et al., 2018) achieves its minimum value when
positive pairs are perfectly aligned, and negative pairs are
uniformly separated with the cosine similarity of −
1
n−1,
where n is the size of the training dataset. Lee et al. (2024)
further extended this optimality analysis to other contrastive
losses, including the SigLIP loss (Zhai et al., 2023).
Due to computational constraints, CL methods are typically
implemented using mini-batches rather than full batches
in practical scenarios. This has motivated recent studies
on understanding whether the property of the optimal state
observed in full-batch settings, i.e., perfect alignment of
positive pairs and uniform separation of negative pairs with
the similarity of −
1
n−1, also holds under mini-batch settings.
Cho et al. (2024) partially addressed this by showing that, for
the InfoNCE loss, the optimal embeddings of mini-batch set-
tings are identical to those of full-batch settings, only when
the sum of all possible mini-batch losses is minimized. Ko-
romilas et al. (2024) explored embeddings learned through
kernel-based contrastive losses (Li et al., 2021; Waida et al.,
2023) in mini-batch settings. While these studies provide
valuable insights into understanding CL, their analyses are
limited to specific forms of contrastive losses.
To address this limitation, we propose a unified framework
for analyzing the embeddings obtained by both full-batch
and mini-batch settings. Our analysis centers on the cosine
similarity of embeddings of both positive and negative pairs.
By characterizing the statistical properties of similarities of
these embeddings, we reveal how different contrastive losses
influence the structure of the learned embedding space under
various training conditions.
Our key contributions are summarized as follows:
• In full-batch settings, we identify a fundamental trade-off
between the alignment of positive pairs and the separation
of negative pairs. Specifically, we show that the perfect
alignment of positive pairs is not feasible when the av-
erage similarity of negative pairs falls below the certain
threshold −
1
n−1. We demonstrate that such misalignment
1
arXiv:2506.09781v2  [cs.LG]  15 Jul 2025

On the Similarities of Embeddings in Contrastive Learning
arises in a class of existing contrastive losses, which can
be mitigated by incorporating within-view negative pairs
into the contrastive loss.
• In mini-batch settings, we demonstrate that negative pairs
within the same batch exhibit stronger separation com-
pared to those from different batches. As a result, we
show that smaller batch sizes induce a higher variance in
the similarities of negative pairs in the embedding space.
We identify this increased variance as a distinctive feature
of mini-batch settings that is absent in full-batch settings.
• Motivated by prior studies that full-batch settings often
outperform their mini-batch counterparts, we hypothesize
that the increased variance may underlie this performance
gap. To explore this, we propose an auxiliary loss that
can be integrated into contrastive losses to reduce this
variance. Empirical results show that incorporating the
proposed term improves the performance of CL methods,
especially in small-batch settings.
2. Related Work
Contrastive Loss.
The InfoNCE loss (Gutmann &
Hyv¨arinen, 2010; Oord et al., 2018) is a widely adopted con-
trastive loss that has been applied to various tasks (Wu et al.,
2018; Hjelm et al., 2019; Bachman et al., 2019; Chi et al.,
2021; Gao et al., 2021; Qian et al., 2021). SimCLR (Chen
et al., 2020) modifies the InfoNCE loss to improve robust-
ness to augmentations by treating different augmented views
of the same instance as positives and all other augmented
instances in the batch as negatives. However, SimCLR si-
multaneously optimizes both positive and negative pairs
in the normalization, which can introduce conflicts during
optimization. To address this issue, Decoupled Contrastive
Loss (DCL) (Yeh et al., 2022) modifies the normalization so
that the selection of negative pairs is restricted. Building on
DCL, Decoupled Hyperspherical Energy Loss (DHEL) (Ko-
romilas et al., 2024) further refines the selection by focusing
on negative pairs between augmented views of the same
instance, which are more challenging than those between
different instances. Figure 5 visualizes which pairs are in-
cluded as positives and negatives for each method.
Meanwhile, Zhai et al. (2023) raised concerns about the
softmax function in the InfoNCE loss, noting that it causes
all instances to be dependent on each other through normal-
ization. To address this limitation, they propose replacing
the softmax with a sigmoid function, which allows each in-
stance to be processed independently in an additive manner.
Understanding CL Through Embedding Structures.
Several studies have examined how optimal embeddings
should be structured to minimize contrastive loss (Lee et al.,
2025). Lu & Steinerberger (2022) showed that the optimal
embeddings that minimize the InfoNCE loss form a simplex
Equiangular Tight Frame (ETF) (Papyan et al., 2020; Sustik
et al., 2007), where each positive pair is perfectly aligned
and negative pairs are equally separated at the same angle,
resulting in maximal separation among representations. Lee
et al. (2024) further showed that the sigmoid-based con-
trastive loss, a variant of the softmax-based InfoNCE loss,
also achieves the same simplex ETF optimum when the
temperature parameter of the loss is sufficiently large. This
optimal simplex ETF structure still holds even in mini-batch
settings, provided that optimization is performed over all
possible mini-batch combinations, rather than a single batch
at a time (Cho et al., 2024). Building on these findings, we
introduce a unified theoretical analysis of the similarities of
embedding pairs.
Effect of Batch Size in CL.
CL shows outstanding
performance, particularly when trained with large batch
sizes (Chen et al., 2020; Radford et al., 2021; Pham et al.,
2023; Tian et al., 2020b; Jia et al., 2021). However, large
batch sizes require substantial memory resources, which
poses practical challenges and often necessitates the use of
smaller batches. This compromise in batch size typically
leads to performance degradation, motivating several the-
oretical studies to investigate its causes (Cho et al., 2024;
Koromilas et al., 2024). For example, Yuan et al. (2022)
demonstrate that the optimization error in SimCLR (Chen
et al., 2020) is upper bounded by a function inversely propor-
tional to the batch size, indicating that smaller batches yield
larger optimization errors. Additionally, Chen et al. (2022)
show that contrastive losses exhibit increasing discrepan-
cies between the true gradients and those estimated during
training as the batch size decreases. While previous studies
have primarily focused on optimization error and gradient
estimation, we prove that training with small batch sizes
leads to increased variance in the similarities of negative
pairs in learned embeddings.
3. Problem Setup
Let (x, y) denote a pair of data points used for model train-
ing, where x and y correspond to two distinct views of
instances. This formulation provides a unified framework
for CL in both unimodal (Chen et al., 2020) and multi-
modal (Radford et al., 2021) settings. In the unimodal case,
x and y are two randomly augmented views. In the mul-
timodal case, x and y are views from different modalities.
For clarity, we present our analysis in the unimodal setting,
but the findings also apply to the multimodal case.
In CL, an encoder f(·) ∈Rd is trained to map inputs into
d-dimensional embedding vectors, thereby representing the
data. The encoder is assumed to produce normalized em-
beddings such that ∥u∥2 = 1 for all embeddings u. This
2

On the Similarities of Embeddings in Contrastive Learning
normalization is commonly adopted in related works for
mathematical simplicity (Wang et al., 2017; Wu et al., 2018;
Tian et al., 2020a; Wang & Isola, 2020; Zimmermann et al.,
2021; Cho et al., 2024; Lee et al., 2024), and is widely used
in practice, as experimental results consistently demonstrate
its effectiveness in improving performance (Chen et al.,
2020; Chen & He, 2021; Xue et al., 2024).
The encoder produces outputs u = f(x) and v = f(y),
which together form an embedding pair (u, v). When the
embedding pair is generated from augmented views of the
same instance, it is called a positive embedding pair and is
encouraged to be similar. In contrast, a negative embedding
pair, where each embedding comes from different instances,
is encouraged to be dissimilar. For simplicity, we refer to
positive embedding pairs as positive pairs and similarly to
negative pairs, when there is no risk of confusion.
Formally, ppos(x, y) denotes the distribution of positive
pairs, and pneg(x, y) represents the distribution of nega-
tive pairs. As in prior work (Wang & Isola, 2020), the
marginal distribution of augmented view x is denoted by
px, and similarly use py to denote the marginal distribution
for y. These marginals satisfy the following conditions:
px(x) =
R
ppos(x, y)dy =
R
pneg(x, y)dy for all x, and
py(y) =
R
ppos(x, y)dx =
R
pneg(x, y)dx for all y. Note
that the randomness in these distributions arises from the
data augmentation process used to generate different views.
Let n be the size of the training dataset. For any positive
integers a and b with a ≤b ≤n, define the index sets [a :
b] := {a, a + 1, · · · , b} and [a] := [1 : a], where index i ∈
[n] refers to the i-th instance in the dataset. For i ∈[n], let
ˆpi
pos(x, y) denote the empirical distribution of positive pairs
derived from the i-th instance. We assume that the supports
of ˆpi
pos and ˆpj
pos are disjoint for i̸ = j, as each instance is
distinct. Moreover, we assume that each instance is used
equally for training. Therefore, the empirical distribution of
all positive pairs, denoted as ˆppos(x, y), can be written as
ˆppos(x, y) = 1
n
P
i∈[n] ˆpi
pos(x, y). Similarly, the empirical
distribution of all negative pairs is denoted by ˆpneg(x, y).
Following the notations introduced in Koromilas et al.
(2024), we denote the element-wise pushforward measures
induced by the encoder f as f♯ˆpx, f♯ˆpy, f♯ˆppos, and f♯ˆpneg.
For example, f♯ˆpneg(u, v) represents the empirical distri-
bution of negative embedding pairs, i.e., the distribution of
(u, v) = (f(x), f(y)) where (x, y) comes from ˆpneg.
Contrastive Loss.
For any a ≤b with a, b ∈[n], let
(U[a:b], V[a:b]) := {(ui, vi) : i ∈[a : b]} be the set of
embedding pairs for instances whose indices range from a
to b. The notation (U[a:b], V[a:b]) ∼f♯ˆp[a:b]
pos indicates that
each positive pair (ui, vi) is sampled from f♯ˆpi
pos for all
i ∈[a : b]. Note that ui and vi are random variables, as
they are the encoder outputs of randomly augmented views.
For simplicity, the subscript is omitted for the set of all n
pairs, i.e., (U, V ) := (U[n], V[n]).
Let f ⋆be the optimal encoder that minimizes the expected
contrastive loss, given by
f ⋆:= arg min
f
E(U,V )∼f♯ˆp[n]
pos [L (U, V )] ,
(1)
where L (U, V ) denotes the contrastive loss for a given
sample (U, V ). In this work, we focus on two specific
forms of contrastive losses used in practice:
Definition 3.1 (InfoNCE-Based Contrastive Loss). For
a given index set I
⊆
[n],
the contrastive loss
Linfo-sym (UI, VI) is defined in its symmetric form as
Linfo-sym(UI, VI):= 1
2 Linfo(UI, VI)+1
2 Linfo(VI, UI) ,
(2)
where the asymmetric component Linfo (UI, VI) is
Linfo(UI, VI) := 1
|I|
X
i∈I
ψ

c1
X
j∈I\{i}
ϕ
(vj −vi)⊤ui

+ c2
X
j∈I\{i}
ϕ
(uj −vi)⊤ui

,
for some constants (c1, c2) ∈{(0, 1), (1, 0), (1, 1)} and
some convex and increasing functions ϕ, ψ : R →R.
Definition 3.2 (Independently Additive Contrastive Loss).
For a given index set I
⊆
[n], the contrastive loss
Lind-add(UI, VI) is defined as
Lind-add(UI, VI) := −1
|I|
X
i∈I
ϕ(u⊤
i vi)
(3)
+
c1
|I|(|I| −1)
X
i̸=j∈I
ψ(u⊤
i vj)
+
c2
2|I|(|I| −1)
X
i̸=j∈I
ψ(u⊤
i uj) + ψ(v⊤
i vj)

for some constants (c1, c2) ∈{(0, 1), (1, 0), (1, 1)}, where
ϕ : R →R is a differentiable, concave, and increasing
function, and ψ : R →R is a differentiable, convex, and
increasing function. Here, i̸ = j ∈I is a simplified notation
representing i ∈I and j ∈I \ {i}.
The constants (c1, c2) ∈{(0, 1), (1, 0), (1, 1)} in both loss
formulations determine which types of negative pairs are
included in the contrastive loss. The cross-view negatives re-
fer to pairs of embeddings from different views of different
instances, i.e., (ui, vj) with i̸ = j, whereas within-view neg-
atives are pairs from the same view but different instances,
i.e., (ui, uj) or (vi, vj) with i̸ = j (Shen et al., 2016). Set-
ting c1 = 1 includes cross-view negatives, while c2 = 1
3

On the Similarities of Embeddings in Contrastive Learning
u1
u2
un
...
u1 u2
un
1_base64="IHq0ZrT73VfJ
AYZ6CbXUyCvMbw0=">AC
yXicjVHLSsNAFD2Nr1pfVZ
dugkVwFRKR6rLgRnBTwT6gL
ZJMpzU2LzMTsRZX/oBb/TH
xD/QvDNGUIvohCRnzr3nz
Nx7vSTwhbTtl4IxMzs3v1B
cLC0tr6yuldc3miLOUsYbL
A7itO25gd+xBvSlwFvJyl3
Qy/gLW90pOKta54KP47O5D
jhvdAdRv7AZ64kqtl/ViK
83LFtmy9zGng5KCfNXj8j
O6CMGQ4YQHBEk4QAuBD0dO
LCRENfDhLiUkK/jHcokTa
jLE4ZLrEj+g5p18nZiPbKU
2g1o1MCelNSmtghTUx5KWF
1mqnjmXZW7G/eE+2p7jamv5
d7hcRKXBD7l+4z8786VYvE
AIe6Bp9qSjSjqmO5S6a7om
5ufqlKkNCnMJ9iqeEmVZ+
9tnUGqFrV71dfxVZypW7Vm
em+FN3ZIG7Pwc5zRo7lO1
aqe7ldqVj7qIrawjV2a5wF
qOEYdDfK+xAMe8WScGFfGj
XH7kWoUcs0mvi3j/h3t/5G
n</latexit>· · ·
v1
v2
it sha1_bas
e64="WRZgxq
+lEM61KeRub
HmfgwfRK5s="
>ACyXicjV
HLSsNAFD2Nr
1pfVZdugkVw
FRKR6rLgRnB
TwT6gLZKk0z
o2TeJkUqzFl
T/gVn9M/AP9
C+MKahFdEK
SM+fec2buvV4
c8ETa9mvOmJ
tfWFzKLxdWV
tfWN4qbW/Uk
SoXPan4URKL
puQkLeMhqks
uANWPB3KEXs
IY3OFHxoiJ
hEfhRzHrDN0
+yHvcd+VRNX
bo24k8tiyb
ZsvcxZ4GSgh
GxVo+IL2ugi
go8UQzCEkIQ
DuEjoacGBjZ
i4DibECUJcx
xnuUSBtSlmM
MlxiB/Tt06V
sSHtlWei1T6
dEtArSGlijz
QR5QnC6jRTx
1PtrNjfvCfa
U91tTH8v8xo
SK3F7F+6ae
Z/daoWiR6Od
Q2cao1o6rzM
5dUd0Xd3PxS
lSHmDiFuxQ
XhH2tnPbZ1J
pE1656+r4m
85UrNr7W6K
d3VLGrDzc5y
zoH5gOWrfH
5YqljZqPYw
S72aZ5HqOAUV
dTI+xqPeMKz
cWbcGLfG3We
qkcs02/i2jI
cPG3qRug=<
/latexit>...
vn
v1 v2
· · ·
vn
pos.
neg.
neg.
pos.
neg.
neg.
u1
u2
un
...
u1 u2
un
Mbw0=">ACyXicjVHLSsNAFD2Nr1pfVZdugkVwFRKR6rLgRnBTwT6gLZJMpzU2LzMTsRZX/oBb/THxD/QvDNGUI
vohCRnzr3nzNx7vSTwhbTtl4IxMzs3v1BcLC0tr6yuldc3miLOUsYbLA7itO25gd+xBvSlwFvJyl3Qy/gLW90pOK
ta54KP47O5DjhvdAdRv7AZ64kqtl/ViK83LFtmy9zGng5KCfNXj8jO6CMGQ4YQHBEk4QAuBD0dOLCRENfDhLiU
kK/jHcokTajLE4ZLrEj+g5p18nZiPbKU2g1o1MCelNSmtghTUx5KWF1mqnjmXZW7G/eE+2p7jamv5d7hcRKXBD7l
+4z8786VYvEAIe6Bp9qSjSjqmO5S6a7om5ufqlKkNCnMJ9iqeEmVZ+9tnUGqFrV71dfxVZypW7Vmem+FN3ZIG7P
wc5zRo7lO1aqe7ldqVj7qIrawjV2a5wFqOEYdDfK+xAMe8WScGFfGjXH7kWoUcs0mvi3j/h3t/5Gn</latexit>· · ·
v1
v2
RZgxq+lEM61KeRubHmfgwfRK5s=">ACyXicjVHLSsN
AFD2Nr1pfVZdugkVwFRKR6rLgRnBTwT6gLZKk0zo2TeJk
UqzFlT/gVn9M/AP9C+MKahFdEKSM+fec2buvV4c8ETa
9mvOmJtfWFzKLxdWVtfWN4qbW/UkSoXPan4URKLpuQkLe
MhqksuANWPB3KEXsIY3OFHxoiJhEfhRzHrDN0+yHvc
d+VRNXbo24k8tiybZsvcxZ4GSghGxVo+IL2ugigo8UQz
CEkIQDuEjoacGBjZi4DibECUJcxnuUSBtSlmMlxiB/
Tt06VsSHtlWei1T6dEtArSGlijzQR5QnC6jRTx1PtrN
jfvCfaU91tTH8v8xoSK3F7F+6aeZ/daoWiR6OdQ2cao
1o6rzM5dUd0Xd3PxSlSHmDiFuxQXhH2tnPbZ1JpE165
6+r4m85UrNr7W6Kd3VLGrDzc5yzoH5gOWrfH5YqljZ
qPYwS72aZ5HqOAUVdTI+xqPeMKzcWbcGLfG3Weqkcs0
2/i2jIcPG3qRug=</latexit>...
vn
v1 v2
· · ·
vn
pos.
neg.
neg.
pos.
neg.
neg.
u1
u2
un
...
u1 u2
un
Mbw0=">ACyXicjVHLSsNAFD2Nr1pfVZdugkVwFRKR6rLgRnBTwT6gLZJMpzU2LzMTsRZX/oBb/THxD/QvDNGUI
vohCRnzr3nzNx7vSTwhbTtl4IxMzs3v1BcLC0tr6yuldc3miLOUsYbLA7itO25gd+xBvSlwFvJyl3Qy/gLW90pOK
ta54KP47O5DjhvdAdRv7AZ64kqtl/ViK83LFtmy9zGng5KCfNXj8jO6CMGQ4YQHBEk4QAuBD0dOLCRENfDhLiU
kK/jHcokTajLE4ZLrEj+g5p18nZiPbKU2g1o1MCelNSmtghTUx5KWF1mqnjmXZW7G/eE+2p7jamv5d7hcRKXBD7l
+4z8786VYvEAIe6Bp9qSjSjqmO5S6a7om5ufqlKkNCnMJ9iqeEmVZ+9tnUGqFrV71dfxVZypW7Vmem+FN3ZIG7P
wc5zRo7lO1aqe7ldqVj7qIrawjV2a5wFqOEYdDfK+xAMe8WScGFfGjXH7kWoUcs0mvi3j/h3t/5Gn</latexit>· · ·
v1
v2
RK5s=">ACyXicjVHLSsNAFD2Nr1pfVZdugkVwFRKR6rLgRnBTwT6gLZKk0zo2TeJkUqzFlT/gVn9M/AP9C+MKa
hFdEKSM+fec2buvV4c8ETa9mvOmJtfWFzKLxdWVtfWN4qbW/UkSoXPan4URKLpuQkLeMhqksuANWPB3KEXsIY3OFH
xoiJhEfhRzHrDN0+yHvcd+VRNXbo24k8tiybZsvcxZ4GSghGxVo+IL2ugigo8UQzCEkIQDuEjoacGBjZi4DibE
CUJcxnuUSBtSlmMlxiB/Tt06VsSHtlWei1T6dEtArSGlijzQR5QnC6jRTx1PtrNjfvCfaU91tTH8v8xoSK3F7
F+6aeZ/daoWiR6OdQ2cao1o6rzM5dUd0Xd3PxSlSHmDiFuxQXhH2tnPbZ1JpE1656+r4m85UrNr7W6Kd3VLGr
Dzc5yzoH5gOWrfH5YqljZqPYwS72aZ5HqOAUVdTI+xqPeMKzcWbcGLfG3Weqkcs02/i2jIcPG3qRug=</latex
it>...
vn
v1 v2
· · ·
vn
pos.
neg.
neg.
neg.
neg.
pos
neg.
neg.
pos.
neg.
neg.
(a) (c1, c2) = (1, 0)
(b) (c1, c2) = (0, 1)
(c) (c1, c2) = (1, 1)
Figure 1. Illustration of negative pair considered in the loss formulations defined in Def. 3.1 and Def. 3.2, which depends on the choice of
(c1, c2). Each grid shows all possible pairs of embeddings in U[n] and V[n], and each cell represents one pair. Green regions represent
positive pairs, and blue-striped regions indicate which negative pairs are included in the loss.
includes within-view negatives. Figure 1 summarizes which
types of negatives are incorporated for each configuration
of (c1, c2). Further discussion on the distinction between
cross-view and within-view negatives in the single-modal
case are provided in Appendix B, emphasizing that their key
difference lies in how they are structurally incorporated into
the loss, not in how they are generated.
Remark 3.3. The first form of losses in Def. 3.1 encom-
passes a variety of contrastive losses such as InfoNCE (Oord
et al., 2018; Radford et al., 2021), SimCLR (Chen et al.,
2020), DCL (Yeh et al., 2022), and DHEL (Koromilas et al.,
2024), see Appendix A.1. The second form in Def. 3.2
includes contrastive losses such as SigLIP (Zhai et al., 2023)
and Spectral CL (HaoChen et al., 2021), see Appendix A.2.
The difference between the two forms of losses lies in com-
putational efficiency. The first form in Def. 3.1 necessitates
simultaneous computation based on pairwise similarities
across the entire set of embeddings due to the need for nor-
malization, which becomes impractical for extremely large
batch sizes. In contrast, the second form in Def. 3.2 is in-
dependently additive, allowing it to compute components
of each pairwise similarity individually and aggregate them,
making it applicable to larger datasets.
4. Similarities of Embedding Pairs
In CL, the encoder is trained to bring positive embedding
pairs closer together while pushing negative embedding
pairs further apart. Accordingly, the cosine similarities of
embedding pairs provide a straightforward way to evalu-
ate how well representation achieves its objective. These
similarities are formally defined as follows.
Definition 4.1 (Similarities of Positive/Negative Pairs). The
similarity of embeddings of a positive pair is defined as
s(f; ˆppos) := f(x)⊤f(y)
for
(x, y) ∼ˆppos,
dubbed as the positive-pair similarity for the encoder f.
Similarly, the similarity of embeddings of a negative pair is
defined as
s(f; ˆpneg) := f(x)⊤f(y)
for
(x, y) ∼ˆpneg,
dubbed as the negative-pair similarity for the encoder f. We
call both similarities as embedding similarities.
Note that the similarities of embeddings in Def. 4.1, de-
noted by s(f; ˆppos) and s(f; ˆpneg), are random variables,
where randomness arises from data sampling and augmenta-
tion. Specifically, a positive pair is generated by selecting
an instance from a dataset of size n and applying two ran-
dom augmentations. Similarly, a negative pair is generated
by randomly selecting an instance pair from the n(n −1)
possible combinations and independently applying random
augmentations to each instance.
Expectation & Variance of Negative-pair Similarities.
Recall that the negative-pair similarity s(f; ˆpneg) is a
random variable.
Here we investigate how the expec-
tation and the variance of s(f; ˆpneg) affect the learned
embeddings. First, as the expectation E [s(f; ˆpneg)] in-
creases, the negative pairs are less separated, which typ-
ically degrades the representation quality.
Second, the
high variance Var [s(f; ˆpneg)] implies that some negative
pairs are mapped unusually close, while others are mapped
much farther apart.
Figure 2 shows the effect of the
variance Var [s(f; ˆpneg)] of the negative-pair similarities.
Here, we have three different cases of learned embeddings
{ui, vi}i∈[4] in three dimensional space. While all three
cases have same expectation E [s(f; ˆpneg)], the geometry
4

On the Similarities of Embeddings in Contrastive Learning
Mini-batch loss: arg min

L
U[1:2], V[1:2]

+ L
U[3:4], V[3:4]

Full-batch loss: arg min

L
U[1:4], V[1:4]

𝑢! = 𝑣!
= 𝑢" = 𝑣"
𝑢" = 𝑣"
𝑢# = 𝑣#
𝑢! = 𝑣!
𝑢$ = 𝑣$
𝑢# = 𝑣#
𝑢" = 𝑣"
𝑢$ = 𝑣$
= 𝑢# = 𝑣#
𝑢! = 𝑣!
𝑢$ = 𝑣$
(a) Ei̸=j∈[4][u⊤
i vj] = −1
3, Vari̸=j∈[4][u⊤
i vj] = 8
9
(b) Ei̸=j∈[4][u⊤
i vj] = −1
3, Vari̸=j∈[4][u⊤
i vj] = 2
9
(c) Ei̸=j∈[4][u⊤
i vj] = −1
3, Vari̸=j∈[4][u⊤
i vj] = 0
Figure 2. Visualization of three different cases of eight embeddings on the three-dimensional unit sphere. Positive embedding pairs are
represented in the same color and share the same subscript, while negative pairs refer to any two embeddings with different subscripts.
In (a) and (b), embeddings minimize the fixed mini-batch contrastive loss described in Theorem 5.5, with the batches partitioned as
{u1, v1, u2, v2} and {u3, v3, u4, v4}. In (c), the embeddings minimize the full-batch contrastive loss described in Theorem 5.1. In all
cases, the expectation of negative-pair similarities, Ei̸=j∈[4][u⊤
i vj], remains the same. However, the variance of negative-pair similarities,
Vari̸=j∈[4][u⊤
i vj], increases in mini-batch settings, indicating that some negative pairs are much more similar to each other while others
are more dissimilar.
of embeddings significantly changes depending on the vari-
ance Var [s(f; ˆpneg)]. One can confirm that the rightmost
case having equi-distant embeddings {ui}i∈[4] achieves the
zero variance of negative-pair similarities.
Comparison with Existing Metrics.
The similarities of
embeddings in Def. 4.1 are related with metrics proposed in
previous work. For example, the alignment metric used in
(Wang & Isola, 2020) can be represented as
E(u,v)∼f♯ˆppos
h
∥u −v∥2
2
i
= −2E [s(f; ˆppos)] + 2,
(4)
which is related with the positive-pair similarity s(f; ˆppos).
Here, the higher alignment value indicates that representa-
tions are largely invariant to random noise factors introduced
by augmentations.
On the other hand, the uniformity metric used in (Wang
& Isola, 2020) is related with the negative-pair similarity
s(f; ˆpneg), since it is defined by the logarithm of the Gaus-
sian potential function (Cohn & Kumar, 2007) as
log Eu∼f♯ˆpx
v∼f♯ˆpy
h
exp

−∥u −v∥2
2
i
(5)
≈2 (E [s(f; ˆpneg)] + Var [s(f; ˆpneg)] −1) , (6)
where the approximation in (6) is detailed in Appendix C.1.
The uniformity metric measures how representations are
uniformly distributed on the unit hypersphere, and thus a
lower uniformity value indicates that the representations
preserve more information from the data.
5. Behavior of Learned Embeddings
In this section, we interpret the behavior of embeddings
trained by contrastive learning, through the lens of similar-
ities of positive/negative pairs, denoted by s(f; ˆppos) and
s(f; ˆpneg), defined in Sec. 4. We begin by examining the
full-batch CL and subsequently extend our analysis to the
mini-batch CL. Proofs for all statements in Sec. 5.1 and
Sec. 5.2 are provided in Appendix C.3 and C.4, respectively.
5.1. Full-Batch Contrastive Learning
Recall that we consider various contrastive losses which
can be categorized into two parts: the InfoNCE-based con-
trastive loss in Def. 3.1 and the independently additive con-
trastive loss in Def. 3.2. Our first main result below provides
the similarities of positive/negative pairs for the two types
of contrastive losses, when the encoder is full-batch trained.
Theorem 5.1. Suppose d ≥n −1. Let the contrastive loss
L(U,V ) be one of the following forms:
i. Linfo-sym(U,V ) in Def. 3.1.
ii. Lind-add(U,V ) in Def. 3.2, where (c1, c2)∈{(0,1), (1,1)}.
iii. Lind-add(U,V ) in Def. 3.2, where (c1,c2) = (1,0) and
ϕ′ (1) >
n−2
2(n−1) · ψ′
−
1
n−1

.
Then, in full-batch settings, the embedding similarities for
the optimal encoder f ⋆in (1) are
s(f ⋆; ˆppos) = 1,
s(f ⋆; ˆpneg) = −
1
n −1.
5

On the Similarities of Embeddings in Contrastive Learning
According to Theorem 5.1, all positive pairs achieve the
perfect alignment, while all negative pairs are uniformly
separated with the cosine similarity of −
1
n−1. This is a
generalized version of previous studies (Lu & Steinerberger,
2022; Cho et al., 2024; Lee et al., 2024; Koromilas et al.,
2024), where we extend in two directions. First, the CL loss
formulations (Def. 3.1 and Def. 3.2) we considered are a
much broader class of losses compared with existing work.
Second, we consider the randomness of n embedding pairs
in the optimization, where this randomness is introduced
through augmentations. Now we analyze the behavior of
embeddings for arbitrary encoder f, that is not necessarily
in the optimal status f ⋆. The below result provides the
relationship between the positive-pair similarity and the
negative-pair similarity.
Theorem 5.2. For any normalized encoder f,
E [s (f; ˆppos)] ≤1 +

E [s (f; ˆpneg)] +
1
n −1

,
(7)
where
the
equality
in
(7)
holds
if
and
only
if
tr
Var(u,v)∼f♯ˆppos[u −v]

= 0 and Eu∼f♯ˆpx
v∼f♯ˆpy
[u + v] = 0.
Theorem 5.2 highlights the relationship between the expec-
tation of positive-pair similarities, E [s (f; ˆppos)], and that
of negative-pair similarities, E [s (f; ˆpneg)]. When the av-
erage of negative-pair similarities drops below −
1
n−1, the
positive pairs cannot be fully aligned, which is not desired.
We call such phenomenon as the excessive separation of
negative pairs in full-batch CL, since the average of negative-
pair similarities drops below −
1
n−1 when negative pairs are
more separated compared with the optimal status specified
in Theorem 5.1. This issue may arise when certain losses
are used, as shown in the following theorem.
Theorem 5.3 (Excessive Separation in Full-Batch CL). Sup-
pose that d ≥n. Consider the contrastive loss L (U, V ) in
the form of Lind-add (U, V ) in Def. 3.2, where (c1, c2) =
(1, 0) and
ϕ′ (1) <
n −2
2(n −1) · ψ′

−
1
n −1

.
(8)
Then, under full-batch settings, the embedding similarities
for the optimal encoder f ⋆in (1) satisfy
s(f ⋆; ˆppos) < 1,
s(f ⋆; ˆpneg) < −
1
n −1.
The inequality condition on ϕ and ψ in (8) explains why
the loss Lind-add(U, V ) in Def. 3.2 causes the excessive
separation of negative pairs. Specifically, Lind-add(U, V )
is formulated as the sum of ψ(·) over negative pairs and
−ϕ(·) over positive pairs. Therefore, ψ′(−
1
n−1) indicates
how much the loss decreases if the negative-pair similarity
falls below −
1
n−1, while ϕ′(1) measures how much the loss
increases if the positive-pair similarity drops below 1. When
the condition in (8) is satisfied, ignoring the scaling factor,
the loss reduction from separating negative pairs beyond the
similarity threshold of −
1
n−1 can be greater than the loss
increase from reducing positive-pair similarity below 1. As
a result, the optimization process favors pushing negative
pairs even further apart, leading to the excessive separation.
We provide a specific loss where this issue arises:
Example 5.4. Consider the sigmoid contrastive loss
Lsig(U, V ) (Zhai et al., 2023), defined as
Lsig(U, V ):= 1
n
X
i∈[n]
log
1 + exp
−tu⊤
i vi

· exp(b)

+ 1
n
X
i̸=j∈[n]
log
1+exp
tu⊤
i vj

·exp(−b)

,
(9)
where t > 0 and b ∈R are hyperparameters. This loss
follows the form of Lind-add (U, V ) in Def. 3.2, where
(c1, c2) = (1, 0), ϕ(x) = −log(1 + exp(−tx + b)), and
ψ(x) = (n −1) · log(1 + exp(tx −b)). If hyperparameters
t and b are chosen such that
1 + exp

t
n−1 + b

1 + exp(t −b)
< n −2
2
,
(10)
then embedding similarities for the full-batch optimal en-
coder f ⋆in (1) satisfy
s(f ⋆; ˆppos) < 1,
s(f ⋆; ˆpneg) < −
1
n −1.
Note that (10) is just a rephrase of (8) by plugging in ϕ and
ψ for the sigmoid contrastive loss. When the hyperparame-
ter b of the sigmoid contrastive loss is sufficiently small, the
condition in (10) is satisfied, thus the learned embedding
suffers from the excessive separation issue. This can be also
explained by the sigmoid contrastive loss formula. In (9),
the relative weight of second term (compared to the first
term) increases as b decreases. In such case, minimizing
the negative-pair similarity becomes more important. Con-
sequently, decreasing b induces the excessive separation of
negative pairs.
Mitigating Excessive Separation.
A natural question that
arises is whether the excessive separation of negative pairs in
full-batch CL can be mitigated. According to Theorem 5.1
and Theorem 5.3, this issue depends on the specific form of
the contrastive loss. In particular, under the independently
additive loss Lind-add(U, V ), the optimal embeddings do
not suffer from excessive separation when c2 = 1 (i.e., case
(ii) of Theorem 5.1), whereas the issue arises when c2 = 0
and condition (8) holds.
6

On the Similarities of Embeddings in Contrastive Learning
This observation suggests two potential solutions to the
excessive separation problem. The first is to set c2 = 1
in the loss, effectively incorporating within-view negative
pairs. The second is to tune hyperparameters such that condi-
tion (8) does not hold, i.e., case (iii) in Theorem 5.1. While
both approaches are theoretically valid, the former offers a
more principled and practical remedy. In contrast, the latter
lacks clear guidance for selecting suitable hyperparameters
and may incur significant computational overhead. There-
fore, we advocate including within-view negative pairs as
a straightforward and effective strategy to avoid excessive
separation in full-batch CL.
5.2. Mini-Batch Contrastive Learning
In Sec. 5.1, we show that when a proper contrastive loss
is chosen for full-batch settings, the learned embedding
satisfies the following behavior: all negative pairs have the
cosine similarity of −
1
n−1 and all positive pairs are perfectly
aligned. What about the practical scenarios when we use
mini-batches for training? Suppose n training samples are
partitioned into b mini-batches where each batch contains
m := n/b samples. Consider training the embeddings by
under the fixed mini-batch configuration, where k-th mini-
batch contains the samples with indices in Ik = {m(k −
1) + 1, m(k −1) + 2, · · · , mk}. Under this scenario, the
below theorem analyzes the behavior of embeddings learned
by mini-batch training.
Theorem 5.5 (Excessive Separation in Mini-Batch CL).
Suppose d ≥m −1. Let the contrastive loss L (U, V )
be one of the forms in Theorem 5.1. Define f ⋆
batch as the
optimal encoder that minimizes the fixed mini-batch loss,
given by
f ⋆
batch := arg min
f
E(U,V )∼f♯ˆp[n]
pos

X
k∈[b]
L (UIk, VIk)

,
where Ik := [m(k −1) + 1 : mk] for k ∈[b]. Then, em-
bedding similarities for the optimal encoder f ⋆
batch satisfy
s(f ⋆
batch; ˆppos) = 1,
E [s(f ⋆
batch; ˆpneg)] = −
1
n −1,
Var [s(f ⋆
batch; ˆpneg)] ∈
h
n−m
(m−1)(n−1)2 ,
n (n−m)
(m−1)(n−1)2
i
.
(11)
A necessary condition for attaining the minimum variance
of negative-pair similarities in (11) is d ≥b(m −1).
According to Theorem 5.5, the embeddings learned by
mini-batch settings have the following behaviors. First,
the positive-pair similarity is equal to 1, i.e., all positive
pairs are fully aligned. Second, the expectation of negative-
pair similarities is equal to −
1
n−1, which happens for full-
batch settings as well. Third, unlike full-batch settings, the
negative-pair similarity is not uniform across the pairs, i.e.,
the variance is positive when the mini-batch size m is strictly
less than the sample size n. Thus, the effect of using mini-
batch (compared with using full-batch) is in the increased
variance of negative-pair similarities. Throughout the paper,
we call such phenomenon as the excessive separation of
negative pairs in mini-batch CL.
Figure 2 visualizes the effect of using mini-batches, com-
pared with full-batch settings, when n = 4 and m = 2. For
full-batch settings, shown in (c) of Figure 2, the variance of
negative-pair similarities is zero, indicating that all negative
pairs are equi-distant. In contrast, (a) and (b) of Figure 2
illustrate the embeddings learned by mini-batch settings,
where the fixed mini-batches are specified as
U[1:2], V[1:2]

and
U[3:4], V[3:4]

. For both (a) and (b), the variance of
negative-pair similarities is positive, where (a) represents
the case that achieves the highest variance in (11), and (b)
corresponds to the case that achieves the lowest variance.
Effect of Batch Size.
Note that the variance of negative-
pair similarities in (11) depends on the batch size m. For
example, in the full-batch case where m = n, the upper
bound in (11) is zero, which is consistent with Theorem 5.1.
One can confirm that the upper and lower bounds on the
variance is a monotonically decreasing function of m, which
implies that smaller batch sizes inherently exacerbates the
excessive separation of negative pairs in mini-batch settings.
The below theorem analyzes the effect of batch size on the
training dynamics, when a popular CL loss is used:
Theorem
5.6.
Consider
the
InfoNCE
loss
LInfoNCE (U, V ) (Oord et al., 2018),
which corre-
sponds to the loss Linfo-sym (U, V ) in Def. 3.1 where
ϕ(x) = exp(x/t) for some t > 0, ψ(x) = log(1 + x),
and (c1, c2) = (1, 0). For any two integers m1, m2 ∈[n]
satisfying m1 ≤m2, the gradient of the InfoNCE loss with
respect to the negative-pair similarity satisfies
0 ≤
∂
∂
u⊤
i vj
LInfoNCE
U[m2], V[m2]

≤
∂
∂
u⊤
i vj
LInfoNCE
U[m1], V[m1]

(12)
for any distinct indices i̸ = j ∈[m]. Moreover, the equality
in (12) holds if and only if m1 = m2.
According to Theorem 5.6, the gradient of the loss with
respect to the negative-pair similarity is always non-negative,
implying that gradient descent decreases the similarities of
negative pairs, thereby pushing them further apart. Notably,
the magnitude of this gradient increases as the batch size
gets smaller. As a result, negative pairs within each batch
exhibit greater separation the batch size gets smaller.
7

On the Similarities of Embeddings in Contrastive Learning
Proposed Variance Reduction Method.
Prior empirical
studies on CL have shown that mini-batch settings often
underperform compared to full-batch settings (Chen et al.,
2020; Radford et al., 2021). This naturally raises a question:
What is the main factor contributing to this performance
degradation in mini-batch settings, and how can it be ad-
dressed? According to Theorem 5.5, from the perspective
of cosine similarity of embeddings, the key difference intro-
duced by mini-batch settings lies in the increased variance
of negative-pair similarities. Motivated by this theoretical
insight, we propose an approach to improve mini-batch
contrastive learning by introducing an auxiliary loss term,
LVRNS(U, V), which explicitly reduces the variance of
negative-pair similarities:
Definition 5.7 (Reducing Variance of Negative-Pair Simi-
larities). Let m be the mini-batch size. Define
LVRNS(U[m], V[m]):=
1
m(m−1)
X
i̸=j∈[m]

u⊤
i vj+
1
n−1
2
as the auxiliary loss for reducing the variance of negative-
pair similarities.
One can combine arbitrary conventional mini-batch loss
L
U[m], V[m]

with the proposed auxiliary loss to get the
modified loss, given by
L
U[m], V[m]

+ λ · LVRNS
U[m], V[m]

,
where λ > 0 is a hyperparameter. By including the proposed
term into the mini-batch loss, we encourage all negative-pair
similarities to be close to −
1
n−1, the ideal value achieved in
full-batch settings in Theorem 5.1. As a result, the proposed
loss controls the variance of negative-pair similarities.
6. Empirical Validation
In this section, we empirically validate the impact of our
theoretical results discussed in Sec. 5, especially for the
practical scenarios of mini-batch settings. First, we empiri-
cally observe that the excessive separation of negative pairs
(proven in Theorem 5.5) actually happens in experiments on
benchmark datasets. Second, we empirically confirm that
such excessive separation issue can be mitigated by using
the proposed loss in Def. 5.7 which reduces the variance
of the negative-pair similarities. Third, we observe such
variance reduction improves the quality of learned represen-
tations in various real-world experiments.
6.1. Excessive Separation of Negative Pairs
To investigate the excessive separation of negative pairs in
CL, we evaluate the variance of the negative-pair similarities
of embeddings learned by real-world experiments. Follow-
ing prior works on contrastive learning (Chen et al., 2020;
Table 1. Variance of the similarities of embeddings of negative
pairs, obtained from models trained with different batch sizes.
Each model is trained using either the SimCLR loss alone or jointly
with our auxiliary loss in Def. 5.7, which is proposed to reduce this
variance. One can confirm that the variance is effectively reduced
by using the proposed auxiliary loss.
Batch size
Variance of negative-pair similarities
SimCLR
SimCLR + Ours
32
0.1649
0.1008
64
0.1505
0.0952
128
0.1444
0.0929
256
0.1404
0.0921
512
0.1396
0.0917
Koromilas et al., 2024), we use a ResNet-18 encoder (He
et al., 2016) followed by a two-layer projection head. The
models are pretrained on CIFAR-100 (Krizhevsky et al.,
2009) by minimizing the SimCLR loss with the temperature
parameter of t = 0.2. Five models are trained with mini-
batches sampled uniformly at random, with batch sizes of
32, 64, 128, 256, and 512, respectively. Additional details
of the experimental setup are provided in Appendix D.
Based on these pretrained models, we generate 5,000 posi-
tive embedding pairs by applying random augmentations to
the training data and extracting the corresponding outputs
from the projection head. We then compute the cosine sim-
ilarities of negative pairs, and report the variance of these
similarities in Table 1. As shown in the table, training with
smaller batch sizes leads to higher variance in negative-pair
similarities, which aligns with the result in Theorem 5.5.
To evaluate the effectiveness of our proposed auxiliary
loss, we train five models for each batch size by min-
imizing the SimCLR loss combined with the auxiliary
loss LVRNS(U, V) in Def. 5.7 with the hyperparameter
of λ = 30. The variances of negative-pair similarities from
these additional models are shown in the last column of
Table 1, and are consistently reduced across all batch sizes.
This indicates that our proposed loss effectively mitigates
excessive separation of negative pairs in mini-batch settings.
6.2. Effect of Variance Reduction on Performance
We further investigate whether reducing the variance of
negative-pair similarities improves the quality of learned
representations in terms of the downstream performances.
Experimental Setup.
We pretrain models on CIFAR-10,
CIFAR-100 (Krizhevsky et al., 2009), and ImageNet (Deng
et al., 2009) using various contrastive losses that follow
the formulation in Def. 3.1, including SimCLR, DCL, and
DHEL. For all methods, we compare models trained with
and without incorporating the auxiliary loss LVRNS(U, V)
8

On the Similarities of Embeddings in Contrastive Learning
0.07 0.10
0.50
1.00
2.00
temperature parameter
40
50
60
70
80
90
top-1 accuracy (%)
SimCLR + Ours (CIFAR 10)
SimCLR (CIFAR 10)
SimCLR + Ours (CIFAR 100)
SimCLR (CIFAR 100)
Figure 3. Classification accuracy on CIFAR datasets. Models are
trained by minimizing the SimCLR loss with and without the
auxiliary loss proposed in Def. 5.7, using various temperature
parameters in the SimCLR loss.
in Def. 5.7. The hyperparameter λ for the proposed loss
is tuned over {0.1, 0.3, 1, 3, 10, 30, 100}. Unless otherwise
specified, the other settings follow those in Sec. 6.1.
Performance Gains from Variance Reduction.
The qual-
ity of the representations learned through CL is known to be
sensitive to the choice of the temperature parameter in con-
trastive losses, as it influences the distribution of similarities
among embeddings (Wang & Liu, 2021). To investigate
this sensitivity, we train models using the SimCLR loss
with temperature values ranging from 0.07 to 2.00. We
compare the standard SimCLR loss against our proposed
variant, which incorporates the auxiliary loss introduced in
Def. 5.7 to reduce the variance of negative-pair similarities.
As shown in Figure 3, incorporating the proposed term leads
to a consistently higher and more stable classification accu-
racy across all temperature settings, alleviating the need for
careful temperature tuning.
We further evaluate the auxiliary loss in Def. 5.7 on existing
CL methods, including DCL and DHEL. Experiments are
conducted on the CIFAR datasets with various batch sizes.
As shown in Figure 4, incorporating the proposed term leads
to improved classification accuracy, with the effect being
more pronounced at smaller batch sizes. Additional results
on the ImageNet dataset are presented in Appendix E.
Caveats of Variance Reduction.
While the auxiliary loss
proposed in Def. 5.7 effectively reduces the variance of
negative-pair similarities, this reduction can influence both
desirable and undesirable sources of variance. On the posi-
tive side, it helps reduce variance introduced by mini-batch
sampling, which can degrade the representation quality.
However, it may also suppress the variance that captures
meaningful structure in the data. Further discussion of the
limitations of the proposed loss is provided in Appendix F.
32
64
128
256
512
85
86
87
88
89
32
64
128
256
512
batch size
55
56
57
58
59
60
61
62
CIFAR-10
CIFAR-100
top-1 accuracy (%)
SimCLR
DCL
DHEL
+ Ours
Figure 4. Effect of the auxiliary loss proposed in Def. 5.7 on top-1
classification accuracy when combined with various baseline meth-
ods (SimCLR, DCL, and DHEL) on CIFAR datasets. The gray
bars highlight the performance gains achieved by incorporating the
proposed term across various batch sizes. The proposed auxiliary
loss consistently improves the model performance.
7. Conclusion
To understand contrastive learning (CL), we mathematically
analyze the distributions of similarities of embeddings, mea-
sured for positive pairs and negative pairs. Our theoretical
results in full-batch settings demonstrate that misalignment
of positive pairs becomes inevitable when the average sim-
ilarity of negative pairs falls below its optimal value, a
situation that can arise with existing contrastive losses. In
mini-batch settings, we prove that the variance of negative-
pair similarities increases as the batch size decreases—a
distinctive characteristic absent in full-batch settings and
a potential contributor to the performance degradation ob-
served in mini-batch settings. To address this, we propose an
auxiliary loss that explicitly reduces the variance of negative-
pair similarities. Empirical results show that incorporating
the proposed loss improves the performance of CL methods,
especially in small-batch settings.
Promising directions for future work include extending this
work in two directions. First, disentangling the variance of
negative-pair similarities that reflects intrinsic data structure
from that caused by mini-batching could enable targeting
only the variance that degrades representation quality. Sec-
ond, analyzing the behavior of embedding similarities not
only during pretraining but also during fine-tuning may pro-
vide deeper insights into its dynamics throughout different
stages of training.
9

On the Similarities of Embeddings in Contrastive Learning
Acknowledgements
This work was partially supported by the National Research
Foundation of Korea (NRF) grant funded by the Ministry
of Science and ICT (MSIT) of the Korean government (RS-
2024-00341749, RS-2024-00345351, RS-2024-00408003),
under the ICT Challenge and Advanced Network of HRD
(ICAN) support program (RS-2023-00259934, RS-2025-
02283048), supervised by the Institute for Information &
Communications Technology Planning & Evaluation (IITP).
This research was also supported by the Yonsei University
Research Fund (2025-22-0025).
We sincerely thank the anonymous reviewers for their criti-
cal reading and constructive feedback enhancing this paper.
Impact Statement
This paper presents work whose goal is to theoretically
understand CL through embedding similarities. There are
many potential societal consequences of our work, none
which we feel must be specifically highlighted here.
References
Bachman, P., Hjelm, R. D., and Buchwalter, W. Learning
representations by maximizing mutual information across
views. In Advances in Neural Information Processing
Systems, volume 32, 2019.
Chen, C., Zhang, J., Xu, Y., Chen, L., Duan, J., Chen, Y.,
Tran, S. D., Zeng, B., and Chilimbi, T. Why do we
need large batchsizes in contrastive learning? a gradient-
bias perspective. In Advances in Neural Information
Processing Systems, 2022.
Chen, T., Kornblith, S., Norouzi, M., and Hinton, G. A
simple framework for contrastive learning of visual rep-
resentations. In International conference on machine
learning, pp. 1597–1607. PMLR, 2020.
Chen, X. and He, K. Exploring simple siamese represen-
tation learning. In IEEE/CVF conference on Computer
Vision and Pattern Recognition, pp. 15750–15758, 2021.
Chi, Z., Dong, L., Wei, F., Yang, N., Singhal, S., Wang,
W., Song, X., Mao, X.-L., Huang, H., and Zhou, M.
InfoXLM: An information-theoretic framework for cross-
lingual language model pre-training. In Conference of
the North American Chapter of the Association for Com-
putational Linguistics, June 2021.
Cho, J., Sreenivasan, K., Lee, K., Mun, K., Yi, S., Lee, J.-G.,
Lee, A., yong Sohn, J., Papailiopoulos, D., and Lee, K.
Mini-batch optimization of contrastive loss. Transactions
on Machine Learning Research, 2024.
Cohn, H. and Kumar, A. Universally optimal distribution of
points on spheres. Journal of the American Mathematical
Society, 20(1):99–148, 2007.
da Costa, V. G. T., Fini, E., Nabi, M., Sebe, N., and Ricci, E.
solo-learn: A library of self-supervised methods for visual
representation learning. Journal of Machine Learning
Research, 23(56):1–6, 2022.
Deng, J., Dong, W., Socher, R., Li, L.-J., Li, K., and Fei-Fei,
L. Imagenet: A large-scale hierarchical image database.
In IEEE/CVF Conference on Computer Vision and Pat-
tern Recognition, pp. 248–255. Ieee, 2009.
Gao, T., Yao, X., and Chen, D. SimCSE: Simple contrastive
learning of sentence embeddings. In Conference on Em-
pirical Methods in Natural Language Processing, 2021.
Gutmann, M. and Hyv¨arinen, A. Noise-contrastive esti-
mation: A new estimation principle for unnormalized
statistical models. In International Conference on Artifi-
cial Intelligence and Statistics, pp. 297–304, 2010.
HaoChen, J. Z., Wei, C., Gaidon, A., and Ma, T. Provable
guarantees for self-supervised deep learning with spec-
tral contrastive loss. In Advances in Neural Information
Processing Systems, volume 34, pp. 5000–5011, 2021.
He, K., Zhang, X., Ren, S., and Sun, J. Deep residual
learning for image recognition. In IEEE/CVF Conference
on Computer Vision and Pattern Recognition, 2016.
He, K., Fan, H., Wu, Y., Xie, S., and Girshick, R. Mo-
mentum contrast for unsupervised visual representation
learning. In IEEE/CVF Conference on Computer Vision
and Pattern Recognition, pp. 9729–9738, 2020.
Hjelm, R. D., Fedorov, A., Lavoie-Marchildon, S., Grewal,
K., Bachman, P., Trischler, A., and Bengio, Y. Learning
deep representations by mutual information estimation
and maximization. In International Conference on Learn-
ing Representations, 2019.
Horn, R. A. and Johnson, C. R. Matrix analysis. Cambridge
university press, 2012.
Jia, C., Yang, Y., Xia, Y., Chen, Y.-T., Parekh, Z., Pham, H.,
Le, Q., Sung, Y.-H., Li, Z., and Duerig, T. Scaling up
visual and vision-language representation learning with
noisy text supervision. In International Conference on
Machine Learning, 2021.
Khosla, P., Teterwak, P., Wang, C., Sarna, A., Tian, Y., Isola,
P., Maschinot, A., Liu, C., and Krishnan, D. Supervised
contrastive learning. In Advances in Neural Information
Processing Systems, volume 33, pp. 18661–18673, 2020.
10

On the Similarities of Embeddings in Contrastive Learning
Kornblith, S., Shlens, J., and Le, Q. V. Do better imagenet
models transfer better?
In IEEE/CVF Conference on
Computer Vision and Pattern Recognition, 2019.
Koromilas, P., Bouritsas, G., Giannakopoulos, T., Nicolaou,
M., and Panagakis, Y. Bridging mini-batch and asymp-
totic analysis in contrastive learning: From InfoNCE to
kernel-based losses. In International Conference on Ma-
chine Learning, 2024.
Krizhevsky, A., Hinton, G., et al. Learning multiple layers
of features from tiny images. Technical report, University
of Toronto, 2009.
Lee, C., Chang, J., and Sohn, J.-y. Analysis of using sigmoid
loss for contrastive learning. In International Conference
on Artificial Intelligence and Statistics, 2024.
Lee, C., Oh, J., Lee, K., and Sohn, J.-y. A theoretical
framework for preventing class collapse in supervised
contrastive learning. In International Conference on Arti-
ficial Intelligence and Statistics, 2025.
Lee, H., Lee, K., Lee, K., Lee, H., and Shin, J. Improving
transferability of representations via augmentation-aware
self-supervision. In Advances in Neural Information Pro-
cessing Systems, volume 34, pp. 17710–17722, 2021.
Li, Y., Pogodin, R., Sutherland, D. J., and Gretton, A. Self-
supervised learning with kernel dependence maximiza-
tion. In Advances in Neural Information Processing Sys-
tems, 2021.
Lu, J. and Steinerberger, S. Neural collapse under cross-
entropy loss. Applied and Computational Harmonic Anal-
ysis, 59:224–241, 2022.
Oord, A. v. d., Li, Y., and Vinyals, O. Representation learn-
ing with contrastive predictive coding. arXiv preprint
arXiv:1807.03748, 2018.
Papyan, V., Han, X., and Donoho, D. L. Prevalence of
neural collapse during the terminal phase of deep learn-
ing training. Proceedings of the National Academy of
Sciences, 117(40):24652–24663, 2020.
Pham, H., Dai, Z., Ghiasi, G., Kawaguchi, K., Liu, H.,
Yu, A. W., Yu, J., Chen, Y.-T., Luong, M.-T., Wu, Y.,
et al. Combined scaling for zero-shot transfer learning.
Neurocomputing, 555:126658, 2023.
Qian, R., Meng, T., Gong, B., Yang, M.-H., Wang, H.,
Belongie, S., and Cui, Y. Spatiotemporal contrastive
video representation learning. In IEEE/CVF Conference
on Computer Vision and Pattern Recognition, 2021.
Radford, A., Kim, J. W., Hallacy, C., Ramesh, A., Goh, G.,
Agarwal, S., Sastry, G., Askell, A., Mishkin, P., Clark, J.,
et al. Learning transferable visual models from natural
language supervision. In International conference on
machine learning, pp. 8748–8763. PMLR, 2021.
Shen, X., Sun, Q.-S., and Yuan, Y.-H. Semi-paired hashing
for cross-view retrieval. Neurocomputing, 213:14–23,
2016.
Sustik, M. A., Tropp, J. A., Dhillon, I. S., and Heath Jr, R. W.
On the existence of equiangular tight frames. Linear
Algebra and its applications, 426(2-3):619–635, 2007.
Tian, Y., Krishnan, D., and Isola, P. Contrastive multiview
coding. In European Conference on Computer Vision,
2020a.
Tian, Y., Sun, C., Poole, B., Krishnan, D., Schmid, C., and
Isola, P. What makes for good views for contrastive
learning? In Advances in Neural Information Processing
Systems, volume 33, pp. 6827–6839, 2020b.
Waida, H., Wada, Y., And´eol, L., Nakagawa, T., Zhang, Y.,
and Kanamori, T. Towards understanding the mechanism
of contrastive learning via similarity structure: A theoret-
ical analysis. In Joint European Conference on Machine
Learning and Knowledge Discovery in Databases, 2023.
Wang, F. and Liu, H. Understanding the behaviour of con-
trastive loss. In IEEE/CVF Conference on Computer
Vision and Pattern Recognition, pp. 2495–2504, 2021.
Wang, F., Xiang, X., Cheng, J., and Yuille, A. L. Normface:
L2 hypersphere embedding for face verification. In ACM
international conference on Multimedia, 2017.
Wang, T. and Isola, P. Understanding contrastive represen-
tation learning through alignment and uniformity on the
hypersphere. In International Conference on Machine
Learning, pp. 9929–9939. PMLR, 2020.
Wu, Z., Xiong, Y., Yu, S. X., and Lin, D. Unsupervised
feature learning via non-parametric instance discrimina-
tion. In IEEE/CVF Conference on Computer Vision and
Pattern Recognition, pp. 3733–3742, 2018.
Xue, Y., Gan, E., Ni, J., Joshi, S., and Mirzasoleiman, B.
Investigating the benefits of projection head for represen-
tation learning. In International Conference on Learning
Representations, 2024.
Yeh, C.-H., Hong, C.-Y., Hsu, Y.-C., Liu, T.-L., Chen, Y.,
and LeCun, Y. Decoupled contrastive learning. In Euro-
pean Conference on Computer Vision, 2022.
Yuan, Z., Wu, Y., Qiu, Z.-H., Du, X., Zhang, L., Zhou,
D., and Yang, T. Provable stochastic optimization for
global contrastive learning: Small batch does not harm
performance. In International Conference on Machine
Learning, pp. 25760–25782. PMLR, 2022.
11

On the Similarities of Embeddings in Contrastive Learning
Zhai, X., Mustafa, B., Kolesnikov, A., and Beyer, L. Sig-
moid loss for language image pre-training. In IEEE/CVF
International Conference on Computer Vision, 2023.
Zimmermann, R. S., Sharma, Y., Schneider, S., Bethge,
M., and Brendel, W. Contrastive learning inverts the
data generating process. In International Conference on
Machine Learning, pp. 12979–12990. PMLR, 2021.
12

On the Similarities of Embeddings in Contrastive Learning
A. Contrastive Losses
We outline how various losses commonly used in CL can be instantiated by the general formulation provided in Def. 3.1 and
Def. 3.2. For each case, we specify the corresponding choices of functions and parameters.
A.1. Contrastive Losses Following Def. 3.1
DCL
pos
u1
u2
un
...
u1 u2
un
· · ·
v1
v2
...
vn
v1 v2
· · ·
vn
InfoNCE
SimCLR
DHEL
pos
u1
u2
un
gwfRK5s=">ACyXicjVHLSsNAFD2Nr1pfVZdugkVwFRKR6rLgRnBTwT6gLZKk0zo2TeJkUqzFlT/gVn9M/A
P9C+MKahFdEKSM+fec2buvV4c8ETa9mvOmJtfWFzKLxdWVtfWN4qbW/UkSoXPan4URKLpuQkLeMhqksuAN
WPB3KEXsIY3OFHxoiJhEfhRzHrDN0+yHvcd+VRNXbo24k8tiybZsvcxZ4GSghGxVo+IL2ugigo8UQzCEk
IQDuEjoacGBjZi4DibECUJcxnuUSBtSlmMlxiB/Tt06VsSHtlWei1T6dEtArSGlijzQR5QnC6jRTx1Pt
rNjfvCfaU91tTH8v8xoSK3F7F+6aeZ/daoWiR6OdQ2cao1o6rzM5dUd0Xd3PxSlSHmDiFuxQXhH2tnPb
Z1JpE1656+r4m85UrNr7W6Kd3VLGrDzc5yzoH5gOWrfH5YqljZqPYwS72aZ5HqOAUVdTI+xqPeMKzcWb
cGLfG3Weqkcs02/i2jIcPG3qRug=</latexit>...
u1 u2
un
· · ·
v1
v2
...
vn
v1 v2
· · ·
vn
pos
u1
u2
un
...
u1 u2
un
· · ·
v1
v2
...
vn
"raBctOoguL/Rv4l90Re5oai2rE=">ACz3icjVH
LSsNAFD2Nr1pfVZdugkVwFRKR6rLgxmUL9gFtKUk6b
YfmRTKplFJx6w+41b8S/0D/wjtjCmoRnZDkzLn3nJl
7rxN5PBGm+ZrTVlbX1jfym4Wt7Z3dveL+QSMJ09hl
dTf0wrjl2AnzeMDqguPtaKY2b7jsaYzvpLx5oTFCQ
+DGzGNWNe3hwEfcNcWRHU6vi1GzmA2mfesXrFkGqZa
+jKwMlBCtqph8QUd9BHCRQofDAEYQ82EnrasGAiI
q6LGXExIa7iDHMUSJtSFqMm9gxfYe0a2dsQHvpmSi
1S6d49Mak1HFCmpDyYsLyNF3FU+Us2d+8Z8pT3m1Kf
yfz8okVGBH7l26R+V+drEVgEtVA6eaIsXI6tzMJV
dkTfXv1QlyCEiTuI+xWPCrlIu+qwrTaJql721VfxN
ZUpW7t0sN8W7vCUN2Po5zmXQODOslGunZcqRjbqPI
5wjFOa5wUquEYVdfKO8IgnPGs17Va70+4/U7VcpjnE
t6U9fABrlJQ2</latexit>v1 v2
· · ·
vn
pos
u1
u2
un
...
u1 u2
un
· · ·
v1
v2
...
vn
5oai2rE=">ACz3icjVHLSsNAFD2Nr1pfVZdugkVwFRKR6rLgxmUL9gFtKUk6bYfmRTKplFJx6w+41b8S/0
D/wjtjCmoRnZDkzLn3nJl7rxN5PBGm+ZrTVlbX1jfym4Wt7Z3dveL+QSMJ09hldTf0wrjl2AnzeMDqguPt
aKY2b7jsaYzvpLx5oTFCQ+DGzGNWNe3hwEfcNcWRHU6vi1GzmA2mfesXrFkGqZa+jKwMlBCtqph8QUd9BHCR
QofDAEYQ82EnrasGAiIq6LGXExIa7iDHMUSJtSFqMm9gxfYe0a2dsQHvpmSi1S6d49Mak1HFCmpDyYsLy
NF3FU+Us2d+8Z8pT3m1Kfyfz8okVGBH7l26R+V+drEVgEtVA6eaIsXI6tzMJVdkTfXv1QlyCEiTuI+xWP
CrlIu+qwrTaJql721VfxNZUpW7t0sN8W7vCUN2Po5zmXQODOslGunZcqRjbqPI5wjFOa5wUquEYVdfKO8Ig
nPGs17Va70+4/U7VcpjnEt6U9fABrlJQ2</latexit>v1 v2
· · ·
vn
Figure 5. Illustration comparing four different contrastive losses, all following the form of Def. 3.1. The green area represents the positive
pair, while the blue-striped regions indicate the negative pairs that are normalized together with the positive pair for each loss.
Table 2. Function and parameter selections in Def. 3.1 that correspond to contrastive losses.
ϕ(x)
ψ(x)
c1
c2
InfoNCE (Oord et al., 2018)
exp(x/t)
log(1 + x)
1
0
SimCLR (Chen et al., 2020)
exp(x/t)
log(1 + x)
1
1
DCL (Yeh et al., 2022)
exp(x/t)
log(x)
1
1
DHEL (Koromilas et al., 2024)
exp(x/t)
log(x)
0
1
13

On the Similarities of Embeddings in Contrastive Learning
1. InfoNCE (Oord et al., 2018), CLIP (Radford et al., 2021):
LInfoNCE(U, V ) = −1
2n
X
i∈[n]
log

exp
u⊤
i vi/t

P
j∈[n] exp
u⊤
i vj/t

!
−1
2n
X
i∈[n]
log

exp
u⊤
i vi/t

P
j∈[n] exp
u⊤
j vi/t

!
(13)
= 1
2n
X
i∈[n]
log

1 +
X
j∈[n]\{i}
exp
(vj −vi)⊤ui/t



+ 1
2n
X
i∈[n]
log

1 +
X
j∈[n]\{i}
exp
(uj −ui)⊤vi/t


,
where t > 0 is the temperature parameter.
2. SimCLR (Chen et al., 2020):
LSimCLR(U, V ) = −1
2n
X
i∈[n]
log

exp
u⊤
i vi/t

P
j∈[n] exp
u⊤
i vj/t

+ P
j∈[n]\{i} exp
u⊤
i uj/t

!
−1
2n
X
i∈[n]
log

exp
u⊤
i vi/t

P
j∈[n] exp
u⊤
j vi/t

+ P
j∈[n]\{i} exp
v⊤
j vi/t

!
= 1
2n
X
i∈[n]
log

1 +
X
j∈[n]\{i}
exp
(vj −vi)⊤ui/t

+
X
j∈[n]\{i}
exp
(uj −vi)⊤ui/t



+ 1
2n
X
i∈[n]
log

1 +
X
j∈[n]\{i}
exp
(uj −ui)⊤vi/t

+
X
j∈[n]\{i}
exp
(vj −ui)⊤vi/t


,
where t > 0 is the temperature parameter.
3. DCL (Yeh et al., 2022):
LDCL(U, V ) = −1
2n
X
i∈[n]
log

exp
u⊤
i vi/t

P
j∈[n]\{i} exp
u⊤
i vj/t

+ P
j∈[n]\{i} exp
u⊤
i uj/t

!
−1
2n
X
i∈[n]
log

exp
u⊤
i vi/t

P
j∈[n]\{i} exp
u⊤
j vi/t

+ P
j∈[n]\{i} exp
u⊤
j ui/t

!
= 1
2n
X
i∈[n]
log


X
j∈[n]\{i}
exp
(vj −vi)⊤ui/t

+ exp
(uj −vi)⊤ui/t



+ 1
2n
X
i∈[n]
log


X
j∈[n]\{i}
exp
(uj −ui)⊤vi/t

+ exp
(vj −ui)⊤vi/t


,
where t > 0 is the temperature parameter.
4. DHEL (Koromilas et al., 2024):
LDHEL(U, V ) = −1
2n
X
i∈[n]
log

exp
u⊤
i vi/t

P
j∈[n]\{i} exp
u⊤
i uj/t

!
−1
2n
X
i∈[n]
log

exp
u⊤
i vi/t

P
j∈[n]\{i} exp
u⊤
j ui/t

!
= 1
2n
X
i∈[n]
log


X
j∈[n]\{i}
exp
(uj −vi)⊤ui/t


+ 1
2n
X
i∈[n]
log


X
j∈[n]\{i}
exp
(vj −ui)⊤vi/t


,
where t > 0 is the temperature parameter.
14

On the Similarities of Embeddings in Contrastive Learning
A.2. Contrastive Losses Following Def. 3.2
Table 3. Function and parameter selections in Def. 3.2 that correspond to contrastive losses.
ϕ(x)
ψ(x)
c1
c2
SigLIP (Zhai et al., 2023)
−log(1+exp (−tx+b))
(n−1)·log (1+exp (tx−b))
1
0
Spectral Contrastive Loss (HaoChen et al., 2021)
x
x2
1
0
1. SigLIP (Zhai et al., 2023) :
LSigLIP(U, V ) = 1
n
X
i∈[n]
log
1 + exp
−tu⊤
i vi + b

+ 1
n
X
i∈[n]
X
j∈[n]\{i}
log
1 + exp
tu⊤
i vj −b

= −1
n
X
i∈[n]
−log
1+exp
−tu⊤
i vi+b

+
1
n(n −1)
X
i∈[n]
X
j∈[n]\{i}
(n −1)·log
1+exp
tu⊤
i vj−b

,
where t > 0 is the temperature parameter and b ∈R is the bias term.
2. Spectral Contrastive Loss (HaoChen et al., 2021) :
LSpectral(U, V ) = −1
n
X
i∈[n]
u⊤
i vj +
1
n(n −1)
X
i∈[n]
X
j∈[n]\{i}
u⊤
i vj
2 .
B. Distinction Between Cross-View and Within-View Negative Pairs
u1
u1
1_base64="Mplwcon4WtOG6m
245S71Z0UKiJU=">ACz3ic
jVHLSsNAFD2Nr1pf9bETIVgE
VyVxUXVXcOyBfuAtpQknba
heZFMlFIqbv0Bt/o7foG4V9C
v0DvTFNQiOiHJmXPvOTP3XjN
w7Ihr2nNKmZtfWFxKL2dWVt
fWN7KbW9XIj0OLVSzf8cO6aU
TMsT1W4TZ3WD0ImeGaDquZgz
MRr12yMLJ974IPA9ZyjZ5nd2
3L4EQ1m67B+2Z3FI/bejub0
/KaXOos0BOQK65/vD7u7byU/
OwTmujAh4UYLhg8cMIODET0N
KBDQ0BcCyPiQkK2jDOMkSFtT
FmMgxiB/Tt0a6RsB7thWck
1Rad4tAbklLFAWl8ygsJi9NU
GY+ls2B/8x5JT3G3If3NxMsl
lqNP7F+6aeZ/daIWji5OZA0
21RIRlRnJS6x7Iq4ufqlKk4
OAXECdygeErakctpnVWoiWbv
orSHjbzJTsGJvJbkx3sUtacD
6z3HOgupRXi/kC2Wa9CkmK4
1d7OQ5nmMIs5RQoW8A9zhHg
9KWblSrpWbSaqSjTb+LaU20
9gI5hM</latexit>u1
lwcon4WtOG6m245S71Z0UKiJU=">ACz3icjVHLSsNAFD2N
r1pf9bETIVgEVyVxUXVXcOyBfuAtpQknbaheZFMlFIqbv0
Bt/o7foG4V9Cv0DvTFNQiOiHJmXPvOTP3XjNw7Ihr2nNKmZt
fWFxKL2dWVtfWN7KbW9XIj0OLVSzf8cO6aUTMsT1W4TZ3WD
0ImeGaDquZgzMRr12yMLJ974IPA9ZyjZ5nd23L4EQ1m67B+
2Z3FI/bejub0/KaXOos0BOQK65/vD7u7byU/OwTmujAh4UYL
hg8cMIODET0NKBDQ0BcCyPiQkK2jDOMkSFtTFmMgxiB/Tt
0a6RsB7thWck1Rad4tAbklLFAWl8ygsJi9NUGY+ls2B/8x5J
T3G3If3NxMslqNP7F+6aeZ/daIWji5OZA021RIRlRnJS6
x7Iq4ufqlKk4OAXECdygeErakctpnVWoiWbvorSHjbzJTsGJ
vJbkx3sUtacD6z3HOgupRXi/kC2Wa9CkmK41d7OQ5nmMIs
5RQoW8A9zhHg9KWblSrpWbSaqSjTb+LaU209gI5hM</late
xit>u1
u1
u1
u2
1_base64="U/2VBzuwovn9R
CKl2rpNksVY=">ACz3ic
jVHLSsNAFD2Nr1q1sdOhGAR
XJW0i6q7ghuXLdgHtKUk6bQ
NzYtkopRScesPuNXf8QvEvYJ
+hd6ZpqAW0QlJzpx7z5m59xq
+bYVc054TysLi0vJKcjW1tr
6R3sxsbdCLwpMVjU92wsah
4y23JZlVvcZg0/YLpj2KxuDM
9EvH7JgtDy3As+8lnb0fu1b
NMnRPVajk6Hxi9cTpFDqZr
JbT5FLnQT4G2VL64/Vxf/el7
GWe0EIXHkxEcMDghO2oSOkp
4k8NPjEtTEmLiBkyTjDBCnSR
pTFKEMndkjfPu2aMevSXniG
Um3SKTa9ASlVHJLGo7yAsDhN
lfFIOgv2N+x9BR3G9HfiL0c
YjkGxP6lm2X+Vydq4ejhRNZ
gU2+ZER1ZuwSya6Im6tfquL
k4BMncJfiAWFTKmd9VqUmlLW
L3uoy/iYzBSv2Zpwb4V3ckga
c/znOeVAr5PLFXLFCkz7FdC
WxhwMc0TyPUcI5yqiSt4873O
NBqShXyrVyM01VErFmB9+Wcv
sJYoOYTQ=</latexit>u2
u2
u2
1_base64="U/2VBzuwovn9R
CKl2rpNksVY=">ACz3ic
jVHLSsNAFD2Nr1q1sdOhGAR
XJW0i6q7ghuXLdgHtKUk6bQ
NzYtkopRScesPuNXf8QvEvYJ
+hd6ZpqAW0QlJzpx7z5m59xq
+bYVc054TysLi0vJKcjW1tr
6R3sxsbdCLwpMVjU92wsah
4y23JZlVvcZg0/YLpj2KxuDM
9EvH7JgtDy3As+8lnb0fu1b
NMnRPVajk6Hxi9cTpFDqZr
JbT5FLnQT4G2VL64/Vxf/el7
GWe0EIXHkxEcMDghO2oSOkp
4k8NPjEtTEmLiBkyTjDBCnSR
pTFKEMndkjfPu2aMevSXniG
Um3SKTa9ASlVHJLGo7yAsDhN
lfFIOgv2N+x9BR3G9HfiL0c
YjkGxP6lm2X+Vydq4ejhRNZ
gU2+ZER1ZuwSya6Im6tfquL
k4BMncJfiAWFTKmd9VqUmlLW
L3uoy/iYzBSv2Zpwb4V3ckga
c/znOeVAr5PLFXLFCkz7FdC
WxhwMc0TyPUcI5yqiSt4873O
NBqShXyrVyM01VErFmB9+Wcv
sJYoOYTQ=</latexit>u2
u2
u2
Q=">ACz3icjVHLSsNAFD2Nr1q1sdOhGARXJVUoequ4MZlC/YBbSlJOm1D8yKZKVU3PoDbvV3/AJxr6BfoXemKahFdEK
SM+fec2buvYZvWyHXtOeEMje/sLiUXE6trK6l1zMbm9XQiwKTVUzP9oK6oYfMtlxW4Ra3Wd0PmO4YNqsZgzMRr12yILQ894
IPfdZy9J5rdS1T50Q1m47O+0Z3FI3bR+1MVstpcqmzIB+DbDH98fq4u/1S8jJPaKIDyYiOGBwQnb0BHS0AeGnziWhgRF
xCyZJxhjBRpI8pilKETO6Bvj3aNmHVpLzxDqTbpFJvegJQq9knjUV5AWJymyngknQX7m/dIeoq7DelvxF4OsRx9Yv/STP/
qxO1cHRxImuwqCZfMqI6M3aJZFfEzdUvVXFy8IkTuEPxgLApldM+q1ITytpFb3UZf5OZghV7M86N8C5uSQPO/xznLKge5v
KFXKFMkz7FZCWxgz0c0DyPUcQ5SqiQt4873ONBKStXyrVyM0lVErFmC9+WcvsJZOYTg=</latexit>u3
1_base64="0wah9tXgAmA+52
+ZeJGua9twAuQ=">ACz3ic
jVHLSsNAFD2Nr1q1sdOhGAR
XJVUoequ4MZlC/YBbSlJOm1
D8yKZKVU3PoDbvV3/AJxr6B
foXemKahFdEKSM+fec2buvYZ
vWyHXtOeEMje/sLiUXE6trK
6l1zMbm9XQiwKTVUzP9oK6oY
fMtlxW4Ra3Wd0PmO4YNqsZgz
MRr12yILQ894IPfdZy9J5rdS
1T50Q1m47O+0Z3FI3bR+1MV
stpcqmzIB+DbDH98fq4u/1S8
jJPaKIDyYiOGBwQnb0BHS0
0AeGnziWhgRFxCyZJxhjBRpI
8pilKETO6Bvj3aNmHVpLzxD
qTbpFJvegJQq9knjUV5AWJym
yngknQX7m/dIeoq7DelvxF4O
sRx9Yv/STP/qxO1cHRxImu
wqCZfMqI6M3aJZFfEzdUvVXF
y8IkTuEPxgLApldM+q1ITytp
Fb3UZf5OZghV7M86N8C5uSQP
O/xznLKge5vKFXKFMkz7FZC
Wxgz0c0DyPUcQ5SqiQt4873O
NBKStXyrVyM0lVErFmC9+Wcv
sJZOYTg=</latexit>u3
u3
u3
u3
u3
ah9tXgAmA+52+ZeJGua9twAuQ=">ACz3icjVHLSsNAFD2N
r1q1sdOhGARXJVUoequ4MZlC/YBbSlJOm1D8yKZKVU3Po
DbvV3/AJxr6BfoXemKahFdEKSM+fec2buvYZvWyHXtOeEMje
/sLiUXE6trK6l1zMbm9XQiwKTVUzP9oK6oYfMtlxW4Ra3Wd
0PmO4YNqsZgzMRr12yILQ894IPfdZy9J5rdS1T50Q1m47O+
0Z3FI3bR+1MVstpcqmzIB+DbDH98fq4u/1S8jJPaKIDyYiO
GBwQnb0BHS0AeGnziWhgRFxCyZJxhjBRpI8pilKETO6Bv
j3aNmHVpLzxDqTbpFJvegJQq9knjUV5AWJymyngknQX7m/dI
eoq7DelvxF4OsRx9Yv/STP/qxO1cHRxImuwqCZfMqI6M3a
JZFfEzdUvVXFy8IkTuEPxgLApldM+q1ITytpFb3UZf5OZghV
7M86N8C5uSQPO/xznLKge5vKFXKFMkz7FZCWxgz0c0DyPUc
Q5SqiQt4873ONBKStXyrVyM0lVErFmC9+WcvsJZOYTg=</
latexit>u3
1_base64="HPGP2B/jEfLEqN
rftSgfE3FTeg=">ACz3ic
jVHLSsNAFD2Nr1q1sdOhKAI
rkriouqu4MZlC/YBbSlJOm1
D8yKZVEqpuPUH3Orv+AXiXkG
/Qu9MU/CB6IQkZ86958zce83
AsSOuaU8pZW5+YXEpvZxZWV
3Lruc2NquRH4cWq1i+4d104
iY3uswm3usHoQMsM1HVYzB2
ciXhuyMLJ974KPAtZyjZ5nd2
3L4EQ1m67B+2Z3PJy09XZuX
8trcqk/gZ6A/WL2/eVhd/u5
Oce0UQHPizEcMHgRN2YCip
wEdGgLiWhgTFxKyZxhgxpY
8pilGEQO6Bvj3aNhPVoLzwj
qboFIfekJQqDkjU15IWJym
yngsnQX7m/dYeoq7jehvJl4u
sRx9Yv/SzTL/qxO1cHRxImu
wqaZAMqI6K3GJZVfEzdVPVXF
yCIgTuEPxkLAlbM+q1ITydp
Fbw0Zf5WZghV7K8mN8SZuSQP
Wv4/zJ6ge5fVCvlCmSZ9iut
LYwR4OaZ7HKOIcJVTIO8At7n
CvlJVL5Uq5nqYqUSzhS9Luf
kAYoaYTQ=</latexit>v1
v1
v1
v1
v1
v1
v2
1_base64="IR1gsnzusUSv3
nr+PW3FuKvl9M=">ACz3ic
jVHLSsNAFD2Nr1pf9bETIVgE
VyXtouqu4MZlC/YBbSlJOm1
D8yKZVEqpuPUH3Orv+AXiXkG
/Qu9MU1CL6IQkZ86958zcew3
ftkKuac8JZWFxaXkluZpaW9
/Y3Epv71RDLwpMVjE92wvqh
4y23JZhVvcZnU/YLpj2KxmDM
5FvDZkQWh57iUf+azl6D3X6l
qmzolqNh2d943ueDhp59vpj
JbV5FLnQS4GmeLmx+vjwd5Ly
Us/oYkOPJiI4IDBSdsQ0dIT
wM5aPCJa2FMXEDIknGCVKkj
SiLUYZO7IC+Pdo1YtalvfAM
pdqkU2x6A1KqOCKNR3kBYXGa
KuORdBbsb95j6SnuNqK/EXs5
xHL0if1LN8v8r07UwtHFqaz
Bop8yYjqzNglkl0RN1e/VMX
JwSdO4A7FA8KmVM76rEpNKGs
XvdVl/E1mClbszTg3wru4JQ0
493Oc86Caz+YK2UKZJn2G6U
piH4c4pnmeoIgLlFAhbx93uM
eDUlaulGvlZpqJGLNLr4t5f
YTZOaYTg=</latexit>v2
v2
v2
v2
1gsnzusUSv3nr+PW3FuKvl9M=">ACz3icjVHLSsNAFD2N
r1pf9bETIVgEVyXtouqu4MZlC/YBbSlJOm1D8yKZVEqpuPU
H3Orv+AXiXkG/Qu9MU1CL6IQkZ86958zcew3ftkKuac8JZWF
xaXkluZpaW9/Y3Epv71RDLwpMVjE92wvqh4y23JZhVvcZn
U/YLpj2KxmDM5FvDZkQWh57iUf+azl6D3X6lqmzolqNh2d9
43ueDhp59vpjJbV5FLnQS4GmeLmx+vjwd5LyUs/oYkOPJiI4
IDBSdsQ0dITwM5aPCJa2FMXEDIknGCVKkjSiLUYZO7IC+
Pdo1YtalvfAMpdqkU2x6A1KqOCKNR3kBYXGaKuORdBbsb95j
6SnuNqK/EXs5xHL0if1LN8v8r07UwtHFqazBop8yYjqzNg
lkl0RN1e/VMXJwSdO4A7FA8KmVM76rEpNKGsXvdVl/E1mClb
szTg3wru4JQ0493Oc86Caz+YK2UKZJn2G6UpiH4c4pnmeoI
gLlFAhbx93uMeDUlaulGvlZpqJGLNLr4t5fYTZOaYTg=</
latexit>v2
v2
v3
v3
v3
v3
o=">ACz3icjVHLSsNAFD2Nr1q1sdOhGARXJVUoequ4MZlC/YBbZEknbaheZFMKqVU3PoDbvV3/AJxr6BfoXemKahFdEK
SM+fec2buvYZvWyHXtOeEMje/sLiUXE6trK6l1zMbm9XQiwKTVUzP9oK6oYfMtlxW4Ra3Wd0PmO4YNqsZ/TMRrw1YEFqe8
GHPms5ete1Opapc6KaTUfnPaMzGowvjy4zWS2nyaXOgnwMsX0x+vj7vZLycs8oYk2PJiI4IDBSdsQ0dITwN5aPCJa2FEX
EDIknGMVKkjSiLUYZObJ+Xdo1YtalvfAMpdqkU2x6A1Kq2CeNR3kBYXGaKuORdBbsb94j6SnuNqS/EXs5xHL0iP1LN838
r07UwtHBiazBop8yYjqzNglkl0RN1e/VMXJwSdO4DbFA8KmVE7rEpNKGsXvdVl/E1mClbszTg3wru4JQ04/3Ocs6B6mM
sXcoUyTfoUk5XEDvZwQPM8RhHnKFC3j7ucI8HpaxcKdfKzSRVScSaLXxbyu0nZ0aYTw=</latexit>v3
KmQkfMV6xh+1ibGc6tyGE2+o=">ACz3icjVHLSsNAFD2N
r1q1sdOhGARXJVUoequ4MZlC/YBbZEknbaheZFMKqVU3Po
DbvV3/AJxr6BfoXemKahFdEKSM+fec2buvYZvWyHXtOeEMje
/sLiUXE6trK6l1zMbm9XQiwKTVUzP9oK6oYfMtlxW4Ra3Wd
0PmO4YNqsZ/TMRrw1YEFqe8GHPms5ete1Opapc6KaTUfnP
aMzGowvjy4zWS2nyaXOgnwMsX0x+vj7vZLycs8oYk2PJiI4
IDBSdsQ0dITwN5aPCJa2FEXEDIknGMVKkjSiLUYZObJ+
Xdo1YtalvfAMpdqkU2x6A1Kq2CeNR3kBYXGaKuORdBbsb94j
6SnuNqS/EXs5xHL0iP1LN838r07UwtHBiazBop8yYjqzNg
lkl0RN1e/VMXJwSdO4DbFA8KmVE7rEpNKGsXvdVl/E1mClb
szTg3wru4JQ04/3Ocs6B6mMsXcoUyTfoUk5XEDvZwQPM8Rh
HnKFC3j7ucI8HpaxcKdfKzSRVScSaLXxbyu0nZ0aYTw=</
latexit>v3
o=">ACz3icjVHLSsNAFD2Nr1q1sdOhGARXJVUoequ4MZlC/YBbZEknbaheZFMKqVU3PoDbvV3/AJxr6BfoXemKahFdEK
SM+fec2buvYZvWyHXtOeEMje/sLiUXE6trK6l1zMbm9XQiwKTVUzP9oK6oYfMtlxW4Ra3Wd0PmO4YNqsZ/TMRrw1YEFqe8
GHPms5ete1Opapc6KaTUfnPaMzGowvjy4zWS2nyaXOgnwMsX0x+vj7vZLycs8oYk2PJiI4IDBSdsQ0dITwN5aPCJa2FEX
EDIknGMVKkjSiLUYZObJ+Xdo1YtalvfAMpdqkU2x6A1Kq2CeNR3kBYXGaKuORdBbsb94j6SnuNqS/EXs5xHL0iP1LN838
r07UwtHBiazBop8yYjqzNglkl0RN1e/VMXJwSdO4DbFA8KmVE7rEpNKGsXvdVl/E1mClbszTg3wru4JQ04/3Ocs6B6mM
sXcoUyTfoUk5XEDvZwQPM8RhHnKFC3j7ucI8HpaxcKdfKzSRVScSaLXxbyu0nZ0aYTw=</latexit>v3
v1
u1
u1
g=">ACz3icjVHLSsNAFD2Nr1q1sdOhKAIrkriouqu4MZlC/YBbSlJOm1D8yKZVEqpuPUH3Orv+AXiXkG/Qu9MU/CB6IQ
kZ86958zce83AsSOuaU8pZW5+YXEpvZxZWV3Lruc2NquRH4cWq1i+4d104iY3uswm3usHoQMsM1HVYzB2ciXhuyMLJ974
KPAtZyjZ5nd23L4EQ1m67B+2Z3PJy09XZuX8trcqk/gZ6A/WL2/eVhd/u5Oce0UQHPizEcMHgRN2YCipwEdGgLiWhgTF
xKyZxhgxpY8pilGEQO6Bvj3aNhPVoLzwjqboFIfekJQqDkjU15IWJymyngsnQX7m/dYeoq7jehvJl4usRx9Yv/SzTL/
qxO1cHRxImuwqaZAMqI6K3GJZVfEzdVPVXFyCIgTuEPxkLAlbM+q1ITydpFbw0Zf5WZghV7K8mN8SZuSQPWv4/zJ6ge5f
VCvlCmSZ9iutLYwR4OaZ7HKOIcJVTIO8At7nCvlJVL5Uq5nqYqUSzhS9LufkAYoaYTQ=</latexit>v1
v2
Y=">ACz3icjVHLSsNAFD2Nr1q1sdOhGARXJW0i6q7ghuXLdgHtKUk6bQNzYtkopRScesPuNXf8QvEvYJ+hd6ZpqAW0Ql
Jzpx7z5m59xq+bYVc054TysLi0vJKcjW1tr6R3sxsbdCLwpMVjU92wsah4y23JZlVvcZg0/YLpj2KxuDM9EvH7JgtDy3A
s+8lnb0fu1bNMnRPVajk6Hxi9cTpFDqZrJbT5FLnQT4G2VL64/Vxf/el7GWe0EIXHkxEcMDghO2oSOkp4k8NPjEtTEmL
iBkyTjDBCnSRpTFKEMndkjfPu2aMevSXniGUm3SKTa9ASlVHJLGo7yAsDhNlfFIOgv2N+x9BR3G9HfiL0cYjkGxP6lm2X+
Vydq4ejhRNZgU2+ZER1ZuwSya6Im6tfquLk4BMncJfiAWFTKmd9VqUmlLWL3uoy/iYzBSv2Zpwb4V3ckgac/znOeVAr5P
LFXLFCkz7FdCWxhwMc0TyPUcI5yqiSt4873ONBqShXyrVyM01VErFmB9+WcvsJYoOYTQ=</latexit>u2
u3
v3
u2
u3
g=">ACz3icjVHLSsNAFD2Nr1q1sdOhKAIrkriouqu4MZlC/YBbSlJOm1D8yKZVEqpuPUH3Orv+AXiXkG/Qu9MU/CB6IQ
kZ86958zce83AsSOuaU8pZW5+YXEpvZxZWV3Lruc2NquRH4cWq1i+4d104iY3uswm3usHoQMsM1HVYzB2ciXhuyMLJ974
KPAtZyjZ5nd23L4EQ1m67B+2Z3PJy09XZuX8trcqk/gZ6A/WL2/eVhd/u5Oce0UQHPizEcMHgRN2YCipwEdGgLiWhgTF
xKyZxhgxpY8pilGEQO6Bvj3aNhPVoLzwjqboFIfekJQqDkjU15IWJymyngsnQX7m/dYeoq7jehvJl4usRx9Yv/SzTL/
qxO1cHRxImuwqaZAMqI6K3GJZVfEzdVPVXFyCIgTuEPxkLAlbM+q1ITydpFbw0Zf5WZghV7K8mN8SZuSQPWv4/zJ6ge5f
VCvlCmSZ9iutLYwR4OaZ7HKOIcJVTIO8At7nCvlJVL5Uq5nqYqUSzhS9LufkAYoaYTQ=</latexit>v1
v2
v3
U=">ACz3icjVHLSsNAFD2Nr1pf9bETIVgEVyVxUXVXcOyBfuAtpQknbaheZFMlFIqbv0Bt/o7foG4V9Cv0DvTFNQiOiH
JmXPvOTP3XjNw7Ihr2nNKmZtfWFxKL2dWVtfWN7KbW9XIj0OLVSzf8cO6aUTMsT1W4TZ3WD0ImeGaDquZgzMRr12yMLJ974
IPA9ZyjZ5nd23L4EQ1m67B+2Z3FI/bejub0/KaXOos0BOQK65/vD7u7byU/OwTmujAh4UYLhg8cMIODET0NKBDQ0BcCyPiQ
kK2jDOMkSFtTFmMgxiB/Tt0a6RsB7thWck1Rad4tAbklLFAWl8ygsJi9NUGY+ls2B/8x5JT3G3If3NxMslqNP7F+6aeZ/
daIWji5OZA021RIRlRnJS6x7Iq4ufqlKk4OAXECdygeErakctpnVWoiWbvorSHjbzJTsGJvJbkx3sUtacD6z3HOgupRXi
/kC2Wa9CkmK41d7OQ5nmMIs5RQoW8A9zhHg9KWblSrpWbSaqSjTb+LaU209gI5hM</latexit>u1
cross-view
negative pair
within-view
negative pair
(a) (c1, c2) = (1, 0)
(b) (c1, c2) = (0, 1)
(c) (c1, c2) = (1, 1)
Figure 6. Graphs illustrating different loss configurations for n = 3.
The key distinction between cross-view and within-view negative pairs in our analysis lies in their structural incorporation
within the contrastive loss, rather than in the manner of their generation. To demonstrate that cross-view and within-view
negatives are not equivalent, we present a graph-based representation in Figure 6, which reframes Figure 1. In these graphs,
each node corresponds to an embedding, and each edge indicates a negative pair considered in the loss.
In the unimodal CL, the distinction between the two views, ui and vi for i ∈[3], is not semantically meaningful. Thus,
ui and vi may be interchanged without affecting the results. This implies that the four graphs depicted in Figure 6a are
equivalent under permutation of views, and the same reasoning applies to Figure 6b. Nevertheless, the overall graph
structures in Figure 6a and Figure 6b remain fundamentally different. One can confirm that cross-view graphs are fully
connected bipartite, whereas within-view graphs consist of disconnected subgraphs. This topological difference highlights
their non-equivalence.
15

On the Similarities of Embeddings in Contrastive Learning
C. Proofs
C.1. Approximation of Uniformity Metric
Under the normality assumption on u⊤v, Proposition C.1 gives
log E

exp
2u⊤v

= 2
E

u⊤v

+ Var

u⊤v

.
Accordingly, the uniformity metric can be approximated as
log Eu∼f♯ˆpx v∼f♯ˆpy
h
exp

−∥u −v∥2
2
i
≈log E(u,v)∼f♯ˆpneg
h
exp

−∥u −v∥2
2
i
≈2 (E [s(f; ˆpneg)] + Var [s(f; ˆpneg)] −1) ,
by Proposition C.2, as n goes to infinity.
Proposition C.1. Assume that the random variable u⊤v follows the normal distribution. Then,
log E

exp
2u⊤v

= 2
E

u⊤v

+ Var

u⊤v

Proof. Let X = u⊤v. Since X follows the normal distribution, we define µ := E[X] and σ2 := Var[X].
Note that the moment generating function of normal distribution is given by
E [exp(tX)] = exp

µt + σ2t2
2

.
Substituting t = 2, we have
E [exp(2X)] = exp
2µ + 2σ2
= exp (2E[X] + 2Var[X]) ,
which is equal to
log E [exp(2X)] = 2 (E[X] + Var[X]) .
Since X = u⊤v, we conclude
log E

exp
2u⊤v

= 2
E

u⊤v

+ Var

u⊤v

.
C.2. Proofs for Relation Between Positive and Negative Pairs
Proposition C.2. The distribution of negative pairs satisfies pneg(x, y) = px(x)py(y) for all x and y. However, for a
training dataset of size n, the empirical distribution of negative pairs is given by
ˆpneg(x, y) =
n
n −1 · ˆpx(x)ˆpy(y) −
1
n −1 · ˆppos(x, y),
for all x and y.
Proof. The empirical distribution of positive pairs, ˆppos, is defined under the assumption that all instances are equally
weighted with the probability Pr{I = i} = 1
n for all i ∈[n], where I is a random variable representing the index. Under
this assumption, the probability that a randomly selected pair is positive is
Pr{pos} = Pr{i = i′} =
X
i∈[n]
Pr{i = i} Pr{i = i} = n · 1
n2 = 1
n.
Then, the empirical distribution of negative pairs, ˆpneg, is subsequently derived as
ˆpx(x)ˆpy(y) = ˆppos(x, y) Pr{pos} + ˆpneg(x, y)(1 −Pr{pos})
= ˆppos(x, y) · 1
n + ˆpneg(x, y) · n −1
n
,
(14)
16

On the Similarities of Embeddings in Contrastive Learning
which leads to
ˆpneg(x, y) =
n
n −1 · ˆpx(x)ˆpy(y) −
1
n −1 · ˆppos(x, y).
Moreover, as n →∞, the above result implies that pneg(x, y) = px(x)py(y).
Lemma C.3. Assume that the encoder f(·) satisfies ∥f(x)∥2
2 = 1 for all x. For any distribution p, the following holds.
1 −E(u,v)∼f♯ppos

u⊤v

+ Eu∼f♯px
v∼f♯py

u⊤v

= 1
2 tr
Var(u,v)∼f♯ppos[u −v]

+ 1
2
E(u,v)∼f♯ppos [u + v]
2
2 .
Proof. Note that
E(u,v)∼f♯ppos [u −v]
2
2 −
E(u,v)∼f♯ppos [u + v]
2
2 = −4E(u,v)∼f♯ppos [u]⊤E(u,v)∼f♯ppos [v]
= −4Eu∼f♯px [u]⊤Ev∼f♯py [v] ,
(15)
where the equality in (15) follows from the assumption of matching marginals.
From the definition of variance, we have
tr
Var(u,v)∼f♯ppos[u−v]

= E(u,v)∼f♯ppos
h
tr
(u−v) −E(u,v)∼f♯ppos [u−v]
 (u−v) −E(u,v)∼f♯ppos [u −v]
⊤i
= E(u,v)∼f♯ppos
h(u −v) −E(u,v)∼f♯ppos [u −v]
2
2
i
= E(u,v)∼f♯ppos
h
∥u −v∥2
2
i
−
E(u,v)∼f♯ppos [u −v]
2
2
= E(u,v)∼f♯ppos

2 −2 · u⊤v

−
E(u,v)∼f♯ppos [u + v]
2
2 + 4Eu∼f♯px[u]⊤Ev∼f♯py[v]
= 2 −2E(u,v)∼f♯ppos

u⊤v

−
E(u,v)∼f♯ppos [u + v]
2
2 + 4Eu∼f♯px[u]⊤Ev∼f♯py[v].
(16)
By rearranging (16) and dividing by 2, we have
1
2 tr
Var(u,v)∼f♯ppos[u −v]

+
E(u,v)∼f♯ppos [u + v]
2
2 = 1 −E(u,v)∼f♯ppos

u⊤v

+ Eu∼f♯px[u]⊤Ev∼f♯py[v]
= 1 −E(u,v)∼f♯ppos

u⊤v

+ Eu∼f♯px
v∼f♯py

u⊤v

Lemma C.4. Assume that the encoder f(·) satisfies ∥f(x)∥2
2 = 1 for all x. For any empirical distribution ˆp with a sample
size of n, the following holds.
1−n −1
n
E(u,v)∼f♯ˆppos

u⊤v

+n −1
n
E(u,v)∼f♯ˆpneg

u⊤v

= 1
2 tr
Var(u,v)∼f♯ˆppos[u −v]

+1
2
E(u,v)∼f♯ˆppos [u + v]
2
2 .
Proof. Using Proposition C.2, the expectation over the empirical distribution can be decomposed into the expectations of
positive and negative pairs as follows.
Eu∼f♯ˆpx
v∼f♯ˆpy

u⊤v

= 1
nE(u,v)∼f♯ˆppos

u⊤v

+ n −1
n
E(u,v)∼f♯ˆpneg

u⊤v

.
Applying Lemma C.3 to the empirical distribution ˆp, we have
1
2 tr
Var(u,v)∼f♯ˆppos[u−v]

+
E(u,v)∼f♯ˆppos [u+v]
2
2 = 1 −E(u,v)∼f♯ˆppos

u⊤v

+ Eu∼f♯ˆpx
v∼f♯py

u⊤v

= 1−n−1
n
E(u,v)∼f♯ˆppos

u⊤v

+ n−1
n
E(u,v)∼f♯ˆpneg

u⊤v

.
17

On the Similarities of Embeddings in Contrastive Learning
Theorem C.5. Assume that the encoder f(·) satisfies ∥f(x)∥2
2 = 1 for all x. For any empirical distribution ˆp with a sample
size of n, the following inequality holds.
E(u,v)∼f♯ˆppos

u⊤v

≤1 +

E(u,v)∼f♯ˆpneg

u⊤v

+
1
n −1

,
where equality holds if and only if tr
Var(u,v)∼f♯ˆppos[u −v]

= 0 and Eu∼f♯ˆpx[u] + Ev∼f♯ˆpy[v] = 0.
Proof. From Lemma C.4, and variance and norm are non-negative, we have
E(u,v)∼f♯ˆppos

u⊤v

=
n
n −1 + E(u,v)∼f♯ˆpneg

u⊤v

−
n
2(n −1) tr
Var(u,v)∼f♯ˆppos[u −v]

−
n
2(n −1)
E(u,v)∼f♯ˆppos [u + v]
2
2
≤
n
n −1 + E(u,v)∼f♯ˆpneg

u⊤v

,
(17)
where equality in (17) holds if and only if tr
Var(u,v)∼f♯ˆppos[u −v]

= 0 and
E(u,v)∼f♯ˆppos[u + v]
2
2 = 0. Moreover,
the condition of
E(u,v)∼f♯ˆppos[u + v]
2
2 = 0 is equal to Eu∼f♯ˆpx[u] + Ev∼f♯ˆpy[v] = 0. As a result, the following holds:
E(u,v)∼f♯ˆppos

u⊤v

≤1 +

E(u,v)∼f♯ˆpneg

u⊤v

+
1
n −1

.
C.3. Proofs for Full-Batch CL
Lemma C.6 (Restatement of Lemma 1 in Lee et al. (2024)). Let u1, v1, u2, v2, · · · un, vn be 2n vectors, satisfying
u⊤
i ui = v⊤
i vi = 1 for all i ∈[n]. Then, the following inequality holds.
1
n(n −1)
X
i∈[n]
X
j∈[n]\{i}
u⊤
i vj ≥
n −2
2n(n −1)
X
i∈[n]
u⊤
i vi −
n
2(n −1),
(18)
where the equality conditions are
(
ui −vi = c for all i ∈[n], for some constant vector c,
P
i∈[n] ui + P
i∈[n] vi = 0.
Proof. By using Jensen’s inequality, we have
1
n
X
i∈[n]
∥ui −vi∥2
2 ≥

1
n
X
i∈[n]
(ui −vi)

2
2
=

1
n
X
i∈[n]
(ui + vi)

2
2
−4

1
n
X
i∈[n]
ui


⊤
1
n
X
i∈[n]
vi


≥−4

1
n
X
i∈[n]
ui


⊤
1
n
X
i∈[n]
vi

,
where the equality conditions are
(
ui −vi = c for all i ∈[n], for some constant vector c,
P
i∈[n] ui + P
i∈[n] vi = 0.
(19)
18

On the Similarities of Embeddings in Contrastive Learning
From the above, it follows that

1
n
X
i∈[n]
ui


⊤
1
n
X
i∈[n]
vi

≥−1
4n
X
i∈[n]
∥ui −vi∥2
2
(20)
= −1
2 + 1
2n
X
i∈[n]
u⊤
i vi,
(21)
where the last equality uses ∥ui −vi∥2
2 = 2 −2u⊤
i vi for all i ∈[n].
Note that the inner product of centroids is

1
n
X
i∈[n]
ui


⊤
1
n
X
i∈[n]
vi

= 1
n2
X
i∈[n]
u⊤
i vi + 1
n2
X
i∈[n]
X
j∈[n]\{i}
u⊤
i vj.
Combining this with (21), we have
1
n2
X
i∈[n]
X
j∈[n]\{i}
u⊤
i vj =

1
n
X
i∈[n]
ui


⊤
1
n
X
i∈[n]
vi

−1
n2
X
i∈[n]
u⊤
i vi
≥−1
2 + 1
2n
X
i∈[n]
u⊤
i vi −1
n2
X
i∈[n]
u⊤
i vi
= n −2
2n2
X
i∈[n]
u⊤
i vi −1
2.
The inequality follows from (20), with equality achieved under the conditions specified in (19).
Lemma C.7. Let u1, v1, u2, v2, · · · un, vn be 2n vectors, satisfying u⊤
i ui = v⊤
i vi = 1 for all i ∈[n]. Then, the following
inequality holds.
1
n(n −1)
X
i∈[n]
X
j∈[n]\{i}
(u⊤
i uj + v⊤
i vj + 2u⊤
i vi) ≥−
2
n(n −1)
X
i∈[n]
u⊤
i vi −
2
n −1,
(22)
where equality holds if and only if P
i∈[n](ui + vi) = 0.
Proof. Note that

X
i∈[n]
(ui + vi)

2
2
=

X
i∈[n]
ui


⊤
X
i∈[n]
ui

+

X
i∈[n]
vi


⊤
X
i∈[n]
vi

+ 2

X
i∈[n]
ui


⊤
X
i∈[n]
vi


= n +
X
i∈[n]
X
j∈[n]\{i}
u⊤
i uj + n +
X
i∈[n]
X
j∈[n]\{i}
v⊤
i vj + 2
X
i∈[n]
u⊤
i vi + 2
X
i∈[n]
X
j∈[n]\{i}
u⊤
i vj
= 2n +
X
i∈[n]
X
j∈[n]\{i}
u⊤
i uj + v⊤
i vj + 2u⊤
i vj

+ 2
X
i∈[n]
u⊤
i vi.
Rearranging terms, we have
1
n(n −1)
X
i∈[n]
X
j∈[n]\{i}
(u⊤
i uj + v⊤
i vj + 2u⊤
i vi) =
1
n(n −1)

X
i∈[n]
(ui + vi)

2
2
−
2
n(n −1)
X
i∈[n]
u⊤
i vi −
2
n −1
≥−
2
n(n −1)
X
i∈[n]
u⊤
i vi −
2
n −1,
where the equality condition is P
i∈[n](ui + vi) = 0.
19

On the Similarities of Embeddings in Contrastive Learning
Lemma C.8. Let u1, v1, u2, v2, · · · un, vn be 2n vectors, satisfying u⊤
i ui = v⊤
i vi = 1 for all i ∈[n]. Then, the following
inequality holds.
1
n(n −1)
X
i∈[n]
X
j∈[n]\{i}
(u⊤
i uj + v⊤
i vj) ≥−
2
n −1,
(23)
where equality holds if and only if P
i∈[n] ui = P
i∈[n] vi = 0.
Proof. Since u⊤
i ui = v⊤
i vi = 1 for all i ∈[n], we have
1
n(n −1)
X
i∈[n]
X
j∈[n]\{i}
u⊤
i uj + v⊤
i vj

=
1
n(n −1)

X
i∈[n]
X
j∈[n]
u⊤
i uj −
X
i∈[n]
u⊤
i ui +
X
i∈[n]
X
j∈[n]
v⊤
i vj −
X
i∈[n]
v⊤
i vi


=
1
n(n −1)




X
i∈[n]
ui

2
2
+

X
j∈[n]
vj

2
2


−
2
n −1
≥−
2
n −1,
where the equality condition is P
i∈[n] ui = P
i∈[n] vi = 0.
Theorem C.9. Suppose that d ≥n −1. Let the contrastive loss L (U, V ) be one of the following forms.
i. Linfo-sym (U, V ) in Def. 3.1.
ii. Lind-add (U, V ) in Def. 3.2, where (c1, c2) ∈{(0, 1), (1, 1)}.
iii. Lind-add (U, V ) in Def. 3.2, where (c1, c2) = (1, 0) and ϕ′ (1) >
n−2
2(n−1) · ψ′
−
1
n−1

.
Then, the embedding similarities for the full-batch optimal encoder f ⋆in (1) satisfy
s(f ⋆; ˆppos) = 1,
s(f ⋆; ˆpneg) = −
1
n −1.
Theorem C.10. Suppose that d ≥n. Let the contrastive loss L (U, V ) be the form of Lind-add (U, V ) in Def. 3.2, where
(c1, c2) = (1, 0) and ϕ′ (1) <
n−2
2(n−1) · ψ′
−
1
n−1

. Then, embedding similarities for the full-batch optimal encoder f ⋆in
(1) satisfy
s(f ⋆; ˆppos) < 1,
s(f ⋆; ˆpneg) < −
1
n −1.
Proof of Theorem. C.9 and Theorem. C.10. We prove for each category of loss, Linfo-sym (U, V ) in Def. 3.1 and
Lind-add (U, V ) in Def. 3.2, separately.
First, consider the case of Linfo-sym (U, V ) in Def. 3.1. By using Jensen’s inequality, we have
Linfo (U, V ) = 1
n
X
i∈[n]
ψ

c1
X
j∈[n]\{i}
ϕ
(vj −vi)⊤ui

+ c2
X
j∈[n]\{i}
ϕ
(uj −vi)⊤ui



≥1
n
X
i∈[n]
ψ

(c1 + c2)(n −1) · ϕ


1
(c1 + c2)(n −1)
X
j∈[n]\{i}
c1(vj −vi)⊤ui + c2(uj −vi)⊤ui





(24)
= 1
n
X
i∈[n]
ψ

(c1 + c2)(n −1) · ϕ


1
(c1 + c2)(n −1)
X
j∈[n]\{i}
c1v⊤
j ui + c2u⊤
j ui −(c1 + c2)v⊤
i ui




,
20

On the Similarities of Embeddings in Contrastive Learning
where equality in (24) holds if the argument of ϕ is constant for all j ∈[n] \ {i}.
Let define h(c1,c2)(x) := ψ((c1 + c2)(n −1)ϕ(x)), which is a convex and increasing function. Then, we have
Linfo-sym (U, V ) = 1
2Linfo (U, V ) + 1
2Linfo (V , U)
≥1
2n
X
i∈[n]
ψ

(c1 + c2)(n −1) · ϕ


1
(c1 + c2)(n −1)
X
j∈[n]\{i}
c1v⊤
j ui + c2u⊤
j ui −(c1 + c2)v⊤
i ui





+ 1
2n
X
i∈[n]
ψ

(c1 + c2)(n −1) · ϕ


1
(c1 + c2)(n −1)
X
j∈[n]\{i}
c1u⊤
j vi + c2v⊤
j vi −(c1 + c2)u⊤
i vi





≥ψ

(c1 + c2)(n −1) · ϕ

1
2n
X
i∈[n]
·
1
(c1 + c2)(n −1)
X
j∈[n]\{i}
c1v⊤
j ui + c2u⊤
j ui −(c1 + c2)v⊤
i ui

+ 1
2n
X
i∈[n]
·
1
(c1 + c2)(n −1)
X
j∈[n]\{i}
c1u⊤
j vi + c2v⊤
j vi −(c1 + c2)u⊤
i vi

!!
(25)
= h(c1,c2)

1
2(c1 + c2)n(n −1)
X
i∈[n]
X
j∈[n]\{i}
c12u⊤
j vi + c2(u⊤
j ui + v⊤
j vi) −2(c1 + c2)u⊤
i vi

!
where the inequality in (25) holds for Jensen’s inequality. Equality in (25) holds if the arguments of h(c1,c2) are constant for
all i ∈[n]. Moreover, from Jensen’s inequality, we have
E(U,V )∼f♯ˆp[n]
pos [Linfo-sym (U, V )]
≥E(U,V )∼f♯ˆp[n]
pos

h(c1,c2)

1
2(c1 + c2)n(n −1)
X
i∈[n]
X
j∈[n]\{i}
c12u⊤
j vi + c2(u⊤
j ui + v⊤
j vi) −2(c1 + c2)u⊤
i vi

!

≥h(c1,c2)

1
2(c1 + c2)E(U,V )∼f♯ˆp[n]
pos


1
n(n −1)
X
i∈[n]
X
j∈[n]\{i}
c12u⊤
j vi + c2(u⊤
j ui + v⊤
j vi) −2(c1 + c2)u⊤
i vi



!
.
Therefore, we only have to minimize
E(U,V )∼f♯ˆp[n]
pos


1
n(n −1)
X
i∈[n]
X
j∈[n]\{i}
c12u⊤
j vi + c2(u⊤
j ui + v⊤
j vi) −2(c1 + c2)u⊤
i vi


.
Now, consider each case of (c1, c2) ∈{(0, 1), (1, 0), (1, 1)}.
For the case of (c1, c2) = (1, 1), by using Lemma C.7, we have
E(U,V )∼f♯ˆp[n]
pos


1
n(n −1)
X
i∈[n]
X
j∈[n]\{i}
2u⊤
j vi + u⊤
j ui + v⊤
j vi −4u⊤
i vi



≥E(U,V )∼f♯ˆp[n]
pos

−
2
n(n −1)
X
i∈[n]
u⊤
i vi −
2
n −1 −4
n
X
i∈[n]
u⊤
i vi

.
For the case of (c1, c2) = (0, 1), by using Lemma C.8, we have
E(U,V )∼f♯ˆp[n]
pos


1
n(n −1)
X
i∈[n]
X
j∈[n]\{i}
u⊤
j ui + v⊤
j vi −2u⊤
i vi


≥E(U,V )∼f♯ˆp[n]
pos

−
2
n −1 −2
n
X
i∈[n]
u⊤
i vi

.
21

On the Similarities of Embeddings in Contrastive Learning
For the case of (c1, c2) = (1, 0), by using Lemma C.6, we have
E(U,V )∼f♯ˆp[n]
pos


1
n(n −1)
X
i∈[n]
X
j∈[n]\{i}
2u⊤
j vi −2u⊤
i vi



≥E(U,V )∼f♯ˆp[n]
pos


n −2
2n(n −1)
X
i∈[n]
u⊤
i vi −
n
2(n −1) −
2
n(n −1)
X
i∈[n]
X
j∈[n]\{i}
u⊤
i vi


= −
2
n(n −1) + −n3 + n2 + n −2
2n(n −1)
· E(U,V )∼f♯ˆp[n]
pos

X
i∈[n]
u⊤
i vi

.
Therefore, for every cases of (c1, c2), u⊤
i vi = 1 holds for all positive pairs (ui, vi) ∼f ⋆
♯ˆpi
pos and i ∈[n]. To achieve the
all equality conditions, u⊤v = −
1
n−1 must hold for all negative pairs (u, v) ∼f ⋆
♯ˆpneg. Therefore, embedding similarities
for the full-batch optimal encoder f ⋆in (1) satisfy
s(f ⋆; ˆppos) = 1,
s(f ⋆; ˆpneg) = −
1
n −1.
Second, consider the case of Lind-add (U, V ) in Def. 3.2. From Jensen’s inequality, we have
Lind-add(U, V ) = −1
n
X
i∈[n]
ϕ(u⊤
i vi) +
c1
n(n −1)
X
i̸=j∈[n]
ψ(u⊤
i vj) +
c2
2n(n −1)
X
i̸=j∈[n]
ψ(u⊤
i uj) + ψ(v⊤
i vj)

≥−ϕ

1
n
X
i∈[n]
u⊤
i vi

+
c1
n(n −1)
X
i̸=j∈[n]
ψ(u⊤
i vj) +
c2
2n(n −1)
X
i̸=j∈[n]
ψ(u⊤
i uj) + ψ(v⊤
i vj)

≥−ϕ

1
n
X
i∈[n]
u⊤
i vi

+ ψ


1
(2c1 + c2)n(n −1)
X
i̸=j∈[n]
(2c1u⊤
i vj + c2u⊤
i uj + c2v⊤
i vj)

.
Equality conditions for both inequality is ϕ and ψ are applied to a constant argument.
Now, consider each case of (c1, c2) ∈{(0, 1), (1, 0), (1, 1)}.
For the case of (c1, c2) = (1, 1), by using Lemma C.7, we have
Lind-add(U, V ) ≥−ϕ

1
n
X
i∈[n]
u⊤
i vi

+ ψ


1
3n(n −1)
X
i̸=j∈[n]
(2u⊤
i vj + u⊤
i uj + v⊤
i vj)


≥−ϕ

1
n
X
i∈[n]
u⊤
i vi

+ ψ

−
2
3n(n −1)
X
i∈[n]
u⊤
i vi −
2
3(n −1)

.
Note that ϕ and ψ are increasing functions. Therefore, by using the similar manner in the proof of Linfo-sym (U, V ) case
above, embedding similarities in Def. 4.1 of the full-batch optimal encoder f ⋆in (1) satisfy
s(f ⋆; ˆppos) = 1,
s(f ⋆; ˆpneg) = −
1
n −1.
For the case of (c1, c2) = (0, 1), by using Lemma C.8, we have
Lind-add(U, V ) ≥−ϕ

1
n
X
i∈[n]
u⊤
i vi

+ ψ


1
n(n −1)
X
i̸=j∈[n]
(u⊤
i uj + v⊤
i vj)


≥−ϕ

1
n
X
i∈[n]
u⊤
i vi

+ ψ

−
2
n −1

22

On the Similarities of Embeddings in Contrastive Learning
Note that ϕ and ψ are increasing functions. Therefore, by using the similar manner in the case of Linfo-sym (U, V ) in
Def. 3.1, embedding similarities in Def. 4.1 of the full-batch optimal encoder f ⋆in (1) satisfy
s(f ⋆; ˆppos) = 1,
s(f ⋆; ˆpneg) = −
1
n −1.
For the case of (c1, c2) = (1, 0), by using Lemma C.6, we have
Lind-add(U, V ) ≥−ϕ

1
n
X
i∈[n]
u⊤
i vi

+ ψ


1
n(n −1)
X
i̸=j∈[n]
u⊤
i vj


≥−ϕ

1
n
X
i∈[n]
u⊤
i vi

+ ψ

n −2
2n(n −1)
n
X
i=1
u⊤
i vi −
n
2(n −1)
!
= h

1
n
X
i∈[n]
u⊤
i vi


where the function h(·) is defined as
h(x) := −ϕ (x) + ψ
 n −2
2(n −1) · x −
n
2(n −1)

.
Note that both −ϕ(·) and ψ(·) are differentiable and convex functions, therefore h(·) is also a differentiable and convex
function. Therefore, to attain the minimum at x = 1, h′(1) < 0 holds. Then,
0 > h′(1) = −ϕ′ (1) +
n −2
2(n −1) · ψ′
 n −2
2(n −1) −
n
2(n −1)

= −ϕ′ (1) +
n −2
2(n −1) · ψ′

−
1
n −1

,
which is equal to
ϕ′ (1) >
n −2
2(n −1) · ψ′

−
1
n −1

.
Therefore, by using the similar manner in the case of Linfo-sym (U, V ) in Def. 3.1, embedding similarities in Def. 4.1 of the
full-batch optimal encoder f ⋆in (1) satisfy
s(f ⋆; ˆppos) = 1,
s(f ⋆; ˆpneg) = −
1
n −1.
if ϕ′ (1) >
n−2
2(n−1) · ψ′
−
1
n−1

. On the other hand, if ϕ′ (1) <
n−2
2(n−1) · ψ′
−
1
n−1

, embedding similarities in Def. 4.1 of
the full-batch optimal encoder f ⋆in (1) satisfy
s(f ⋆; ˆppos) < 1,
s(f ⋆; ˆpneg) < −
1
n −1.
Moreover, the existence of the embedding for d ≥n can be shown in Proposition 1 in Lee et al. (2024)
Example C.11. Consider the sigmoid contrastive loss Lsig(U, V ) (Zhai et al., 2023), defined as
Lsig(U, V ):= 1
n
X
i∈[n]
log
1 + exp
−tu⊤
i vi

· exp(b)

+ 1
n
X
i̸=j∈[n]
log
1+exp
tu⊤
i vj

·exp(−b)

,
where t > 0 and b ∈R are hyperparameters. This loss follows the form of Lind-add (U, V ) in Def. 3.2, where (c1, c2) =
(1, 0), ϕ(x) = −log(1 + exp(−tx + b)), and ψ(x) = (n −1) · log(1 + exp(tx −b)).
23

On the Similarities of Embeddings in Contrastive Learning
If hyperparameters t and b are chosen such that
1 + exp

t
n−1 + b

1 + exp(t −b)
< n −2
2
,
embedding similarities of the full-batch optimal encoder f ⋆in (1) satisfy
s(f ⋆; ˆppos) < 1,
s(f ⋆; ˆpneg) < −
1
n −1.
Proof. The sigmoid contrastive loss Lsig(U, V ) follows the loss form in Def. 3.2, see Appendix A.2. Consequently, by
Theorem C.10, it suffices to verify the condition of
ϕ′ (1) <
n −2
2(n −1) · ψ′

−
1
n −1

,
(26)
where ϕ(x) = −log(1 + exp(−tx + b)) and ψ(x) = (n −1) log(1 + exp(tx −b)). Taking the derivative of ϕ(x), we
obtain
ϕ′(x) =
t exp(−tx + b)
1 + exp(−tx + b) =
t
1 + exp(tx −b),
and differentiating ψ(x) yields
ψ′(x) = (n −1) ·
t exp(tx −b)
1 + exp(tx −b).
By plugging the derivative values into (26), we get
t
1 + exp(t −b) <
n −2
2(n −1) ·
(n −1)t exp

−
t
n−1 −b

1 + exp

−
t
n−1 −b

,
which simplifies to
1
1 + exp(t −b) <
n −2
2(n −1) ·
(n −1) exp

−
t
n−1 −b

1 + exp

−
t
n−1 −b

= n −2
2
·
1
exp

t
n−1 + b

+ 1
.
Therefore, if hyperparameters t and b satisfy
1 + exp

t
n−1 + b

1 + exp(t −b)
< n −2
2
,
(27)
following from Theorem C.10, the similarities of the full-batch optimal encoder f ⋆in (1) satisfy
s(f ⋆; ˆppos) < 1,
s(f ⋆; ˆpneg) < −
1
n −1.
C.4. Proofs for Mini-Batch CL
Definition C.12 (Simplex ETF). A set of n vectors U on the d-dimensional unit sphere is called (n −1)-simplex ETF, if
∥u∥2
2 = 1 and u⊤v = −
1
n −1,
∀u̸ = v ∈U.
Note that (n −1)-simplex ETF exists when d ≥n −1.
24

On the Similarities of Embeddings in Contrastive Learning
Lemma C.13. Let a set of n vectors U be a (n −1)-simplex ETF on the d-dimensional unit sphere with d ≥n −1. Then,
the following holds:
X
u∈U
u = 0
Proof. By the definition of a (n −1)-simplex ETF, each vector u ∈U satisfies ∥u∥2 = 1 and the pairwise inner product
for any u, v ∈U with u̸ = v is u⊤v = −
1
n−1. Then,

X
u∈U
u

2
2
=
 X
u∈U
u
!⊤ X
u∈U
u
!
=
X
u∈U
u⊤u +
X
u̸=v∈U
u⊤v = n · 1 + n(n −1) ·

−
1
n −1

= 0.
Since the squared norm is zero, we conclude P
u∈U u = 0.
Lemma C.14. Let a set of n vectors U be a (n −1)-simplex ETF, and a set of m vectors V be a (m −1)-simplex ETF,
where all vectors are on the d-dimensional unit sphere with d ≥max(n, m) −1. Then, the following holds:
1
|U ∪V |(|U ∪V | −1)
X
u̸=v∈U∪V
u⊤v = −
1
n + m −1.
Here, U ∪V denotes the concatenation of the two sets, representing the full collection of all n + m vectors from U and V .
Proof. From Def C.12, we have
1
n(n −1)
X
u̸=v∈U
u⊤v = −
1
n −1,
1
m(m −1)
X
u̸=v∈V
u⊤v = −
1
m −1.
Moreover, Lemma C.13 implies that
X
u∈U
X
v∈V
u⊤v =
 X
u∈U
u
!⊤ X
v∈V
v
!
= 0⊤0 = 0.
The total sum of pairwise inner products for the combined set U ∪V can be written as
X
u̸=v∈U∪V
u⊤v =
X
u∈U∪V
X
v∈U∪V \{u}
u⊤v
=
X
u∈U
X
v∈U∪V \{u}
u⊤v +
X
u∈V
X
v∈U∪V \{u}
u⊤v
=
X
u∈U
X
v∈U\{u}
u⊤v +
X
u∈U
X
v∈V
u⊤v +
X
u∈V
X
v∈U
u⊤v +
X
u∈V
X
v∈V \{u}
u⊤v
=
X
u̸=v∈U
u⊤v +
X
u∈U,v∈V
u⊤v +
X
v∈V ,u∈U
u⊤v +
X
u̸=v∈V
u⊤v
=
X
u̸=v∈U
u⊤v +
X
u̸=v∈V
u⊤v
(28)
= n(n −1) ·

−
1
n −1

+ m(m −1) ·

−
1
m −1

= −n −m,
where the equality in (28) holds because the total pairwise inner product sums within U and within V are zero.
Therefore, we obtain
1
|U ∪V |(|U ∪V | −1)
X
u̸=v∈U∪V
u⊤v =
1
(n + m)(n + m −1)(−n −m) = −
1
n + m −1.
25

On the Similarities of Embeddings in Contrastive Learning
Lemma C.15. Suppose d ≥n −1. Let V and W be d × n matrices whose columns form (n −1)-simplex ETF on the
d-dimensional unit sphere. Then, there exist an orthogonal matrix P ∈Rd×d such that V = P W .
Proof. From the definition of simplex ETF in Def. C.12, the Gram matrices satisfy
V ⊤V = W ⊤W ,
where each diagonal entry is 1 and each off-diagonal entry is −
1
n−1. Then, from Theorem 7.3.11 in Horn & Johnson (2012)
there exist an orthogonal matrix P ∈Rd×d such that V = P W .
Theorem C.16. Suppose d ≥m −1. Let the contrastive loss L (U, V ) be one of the forms in Theorem 5.1. Define f ⋆
batch
as the optimal encoder that minimizes the fixed mini-batch loss, given by
f ⋆
batch := arg min
f
E(U,V )∼f♯ˆp[n]
pos

X
k∈[b]
L (UIk, VIk)

,
where Ik := [m(k −1) + 1 : mk] for k ∈[b].
Then, embedding similarities for the mini-batch optimal encoder f ⋆
batch satisfy
s(f ⋆
batch; ˆppos) = 1,
E [s(f ⋆
batch; ˆpneg)] = −
1
n −1,
Var [s(f ⋆
batch; ˆpneg)] ∈

n −m
(m −1)(n −1)2 ,
n (n −m)
(m −1)(n −1)2

.
(29)
A necessary condition for attaining the minimum variance of negative-pair similarities in (11) is d ≥b(m −1).
Proof. Note that
E(U,V )∼f♯ˆp[n]
pos

X
k∈[b]
L (UIk, VIk)

=
X
k∈[b]
E(U,V )∼f♯ˆp
Ik
pos [L (UIk, VIk)] ,
by applying Theorem 5.1 to each batch, m random vectors in each batch are degenerated to construct the (m −1)-simplex
ETF in Def. C.12. Therefore, for k ∈[b], we have:
u⊤v = 1
∀(u, v) ∼f♯ˆpIk
pos,
u⊤v = −
1
m −1
∀(u, v) ∼f♯ˆpIk
neg.
(30)
In what follows, for all positive pairs, we have
u⊤v = 1
∀(u, v) ∼f ⋆
♯ˆppos,
which is equal to
s(f ⋆
batch; ˆppos) = 1.
For k ∈[b], let U (k) and V (k) denote d × m random matrices, where the columns represent the vectors in the k-th batch.
Additionally, define U and V as d × mb random matrices formed by concatenation of all corresponding batch matrices, i.e.,
U :=

U (1), U (2), · · · , U (b)
and V :=

V (1), V (2), · · · , V (b)
.
Let W be a d × m matrix whose columns form (m −1)-simplex ETF in Def. C.12. From Lemma C.15, for k ∈[b], there
exist orthogonal matrices P (k) ∈Rd×d such that V (k) = P (k)W . Moreover, based on the singular value decomposition,
let W = W1ΣW ⊤
2 , where W1 is a d × d orthogonal matrix, W2 is an m × m orthogonal matrix, and Σ is a d × m
rectangular diagonal matrix with non-negative values of σ1, σ2, · · · , σm on the diagonal.
26

On the Similarities of Embeddings in Contrastive Learning
For all k ∈[b], we have


U (k)⊤
V (k)

2
F
=


V (k)⊤
V (k)

2
F
=
W ⊤W
2
F = m · 1 + m(m −1) ·

−
1
m −1
2
=
m2
m −1.
For all k1̸ = k2 ∈[b], we have


U (k1)⊤
V (k2)

2
F
=


V (k1)⊤
V (k2)

2
F
=
W ⊤
P (k1)⊤
P (k2)W

2
F
≥0,
where the minimum value of zero is achieved if
P (k1)⊤P (k2) is the d × d consisting entirely of zero elements.
On the other hand,


U (k1)⊤
V (k2)

2
F
=


V (k1)⊤
V (k2)

2
F
=
W ⊤
P (k1)⊤
P (k2)W

2
F
=
W2ΣW ⊤
1

P (k1)⊤
P (k2)W1ΣW ⊤
2

2
F
=
ΣW ⊤
1

P (k1)⊤
P (k2)W1Σ

2
F
=
ΣP ⊤
1 P2Σ
2
F ,
where P1 := P (k1)W1 and P2 := P (k2)W1 are m × m orthogonal matrices, and each P1i and P2i is a column vector of
P1 and P2, respectively. Since P1 and P2 are orthogonal matrices, their columns are orthonormal vectors, respectively.
Then,


U (k1)⊤
V (k2)

2
F
=
ΣP ⊤
1 P2Σ
2
F =
X
i∈[m]
σ2
i P ⊤
1iP2i ≥
X
i∈[m]
σ2
i = ∥ΣΣ∥2
F =
W ⊤W
2
F =
m2
m −1,
where the maximum value of m is attained if P1i = P2i for all i ∈[m], i.e., P1 = P2.
From Lemma C.14, the expectation of the negative-pair similarity is
E [s(f ⋆
batch; ˆpneg)] = E(u,v)∼f ⋆
batch ♯ˆpneg

u⊤v

= −
1
n −1.
Note that
E

s(f ⋆
batch; ˆpneg)2
= E(u,v)∼f ⋆
batch ♯ˆpneg
hu⊤v
2i
=
1
n2 −n
U ⊤V
2
F −n

=
1
n2 −n
X
k1,k2∈[b]


U (k1)⊤
V (k2)

2
F
−
1
n −1
=
1
n2 −n
X
k1̸=k2∈[b]


U (k1)⊤
V (k2)

2
F
+
1
n2 −n
X
k∈[b]


U (k)⊤
V (k)

2
F
−
1
n −1
27

On the Similarities of Embeddings in Contrastive Learning
=
1
n2 −n
X
k1̸=k2∈[b]


U (k1)⊤
V (k2)

2
F
+
1
n2 −n · b ·
m2
m −1 −
1
n −1
=
1
n2 −n
X
k1̸=k2∈[b]


U (k1)⊤
V (k2)

2
F
+
1
(m −1)(n −1)
∈

0 +
1
(m −1)(n −1),
1
n2 −n · b(b −1) ·
m2
m −1 +
1
(m −1)(n −1)

,
where the range is equal to
h
1
(m−1)(n−1),
m(b−1)+1
(m−1)(n−1)
i
.
Therefore, the variance of the negative-pair similarity is
Var [s(f ⋆
batch; ˆpneg)] = E

s(f ⋆
batch; ˆpneg)2
−E [s(f ⋆
batch; ˆpneg)]2
= E

s(f ⋆
batch; ˆpneg)2
−
1
(n −1)2
∈

n −m
(m −1)(n −1)2 ,
n (n −m)
(m −1)(n −1)2

.
Lemma C.17. Let m1 and m2 be natural numbers with m1 ≤m2. For any positive values {ci > 0}i∈[m2], the following
inequality holds:
m1
P
i∈[m1] ci
m2
P
i∈[m2] ci
≤1,
where the equality condition is m1 = m2.
Proof. Since m2 > 0 and m2 −m1 ≥0, we have
m2
X
i∈[m2]
ci −m1
X
i∈[m1]
ci = m2
X
i∈[m2]\[m1]
ci + (m2 −m1)
X
i∈[m1]
ci ≥0,
where the equality condition is m1 = m2. Note that m1
P
i∈[m1] ci > 0. Rearranging the above yields
m1
P
i∈[m1] ci
m2
P
i∈[m2] ci
≤1.
Theorem C.18. Consider the InfoNCE loss LInfoNCE (U, V ) (Oord et al., 2018), which corresponds to the loss
Linfo-sym (U, V ) in Def. 3.1 where ϕ(x) = exp(x/t) for some t > 0, ψ(x) = log(1 + x), and (c1, c2) = (1, 0).
For any two integers m1, m2 ∈[n] such that m1 ≤m2, the gradient of the InfoNCE loss with respect to a negative-pair
similarity satisfies the following inequalities for any distinct indices i̸ = j ∈[m].
E(U,V )∼f♯ˆp1:m1
"
−
∂
∂
u⊤
i vj
LInfoNCE(U, V )
#
≤E(U,V )∼f♯ˆp1:m2
"
−
∂
∂
u⊤
i vj
LInfoNCE(U, V )
#
≤0.
Moreover, the equality condition of the first inequality is m1 = m2.
Proof. Without loss of generality, suppose there are m positive pairs in (U, V ). Then, the InfoNCE loss is given as follows.
L(U, V ) = 1
m
X
i∈[m]
log

1 +
X
j∈[m]\{i}
exp(u⊤
i (vj −vi)/t)

+ 1
m
X
i∈[m]
log

1 +
X
j∈[m]\{i}
exp((uj −ui)⊤vi/t)

.
28

On the Similarities of Embeddings in Contrastive Learning
Following the gradients analysis in Wang & Liu (2021), the partial derivatives of the loss with respect to negative pair are
derived as follows. In particular, for all i̸ = j ∈[m], we have
∂
∂
u⊤
i vj
L(U, V ) = 1
m ·
∂
∂
u⊤
i vj
 log

1 +
X
j′∈[m]\{i}
exp(u⊤
i (vj′ −vi)/t)


+ 1
m ·
∂
∂
u⊤
i vj
 log

1 +
X
i′∈[m]\{i}
exp((ui′ −uj)⊤vj/t)


= 1
m ·
exp(u⊤
i (vj −vi)/t)/t
1 + P
j′∈[m]\{i} exp(u⊤
i (vj′ −vi)/t) + 1
m ·
exp((ui −uj)⊤vj/t)/t
1 + P
i′∈[m]\{i} exp((ui′ −uj)⊤vj/t)
= 1
mt ·
exp(u⊤
i vj/t)
P
j′∈[m] exp(u⊤
i vj′/t) + 1
mt ·
exp(u⊤
i vj/t)
P
i′∈[m] exp(u⊤
i′ vi/t)
= 1
mt

exp(u⊤
i vj/t)
P
j∈[m] exp(u⊤
i vj/t) +
exp(u⊤
i vj/t)
P
i′∈[m] exp(u⊤
i′ vi/t)
!
≥0.
Then, for any m1 ≤m2 ≤n and i̸ = j ∈[m1], the following inequality holds:
E(U,V )∼f♯ˆpm2
pos
"
∂
∂
u⊤
i vj
L(U, V )
#
= E(U,V )∼f♯ˆpm2
pos
"
1
m2t

exp(u⊤
i vj/t)
P
j∈[m2] exp(u⊤
i vj/t) +
exp(u⊤
i vj/t)
P
i′∈[m2] exp(u⊤
i′ vi/t)
!#
=
1
m1tE(U,V )∼f♯ˆpm2
pos
"
exp(u⊤
i vj/t)
P
j∈[m1] exp(u⊤
i vj/t) ·
m1
P
j∈[m1] exp(u⊤
i vj/t)
m2
P
j∈[m2] exp(u⊤
i vj/t)
#
+
1
m1tE(U,V )∼f♯ˆpm2
pos
"
exp(u⊤
i vj/t)
P
i′∈[m2] exp(u⊤
i′ vi/t) ·
m1
P
i′∈[m1] exp(u⊤
i′ vi/t)
m2
P
i′∈[m2] exp(u⊤
i′ vi/t)
#
≤
1
m1tE(U,V )∼f♯ˆpm2
pos
"
exp(u⊤
i vj/t)
P
j∈[m1] exp(u⊤
i vj/t) · 1
#
+
1
m1tE(U,V )∼f♯ˆpm2
pos
"
exp(u⊤
i vj/t)
P
i′∈[m2] exp(u⊤
i′ vi/t) · 1
#
(31)
=
1
m1tE(U,V )∼f♯ˆpm1
pos
"
exp(u⊤
i vj/t)
P
j∈[m1] exp(u⊤
i vj/t) +
exp(u⊤
i vj/t)
P
i′∈[m1] exp(u⊤
i′ vi/t)
#
(32)
= E(U,V )∼f♯ˆpm1
pos
"
∂
∂
u⊤
i vj
L(U, V )
#
,
where the inequality in (31) follows from Lemma C.17, since the exponential function is strictly positive. The equality
condition in (31) is m1 = m2.
Moreover, equality in (32), where f♯ˆpm2
pos is replaced with f♯ˆpm1
pos, holds because the expectation involves only embeddings
(U, V ) with indices in [m1]. This concludes the proof.
29

On the Similarities of Embeddings in Contrastive Learning
D. Experiment Details
In this section, we provide the details of the experiment setup mentioned in Sec. 6. Our implementation is based on
the open-source library solo-learn (da Costa et al., 2022) for self-supervised learning. The source code is available at
https://github.com/leechungpa/embedding-similarity-cl/.
D.1. Architecture and Training Details
For all experiments, we use modified ResNet-18 (He et al., 2016; Chen et al., 2020) as the backbone for CIFAR datasets
and ResNet-50 for ImageNet-100. For CIFAR datasets, we modify ResNet-18 by replacing the first convolutional layer
with a 3×3 kernel at a stride of 1 and removing the initial max pooling step. In contrast, we use the standard ResNet-50
architecture for ImageNet-100 without any modifications. Regardless of the backbone used, we attach a 2-layer MLP as the
projection head, which projects representations to a 128-dimensional latent space. Batch normalization is applied to the
fully connected layers, with the hidden layer dimension set to 2048 for ImageNet-100 and 512 for the CIFAR datasets.
We follow the data augmentation strategy used in SimCLR (Chen et al., 2020). Specifically, we apply random resized
cropping, horizontal flipping, color jittering, and Gaussian blurring. For the CIFAR datasets, the crop size is set to 32, while
for ImageNet-100, we use a crop size of 224. These augmentations are applied consistently across all experiments.
For the optimizer, we use stochastic gradient descent (SGD) for 200 epochs. The learning rate is scaled linearly with the
batch size as lr × BatchSize/256, where the base learning rate is set to 0.3 for the CIFAR datasets and 0.1 for ImageNet-100.
A cosine decay schedule is applied, with a weight decay of 0.0001 and SGD momentum set to 0.9. Additionally, we use
linear warmup for the first 10 epochs.
We tune the temperature parameter for baseline methods, SimCLR, DCL, and DHEL, by performing a grid search over
the range of 0.1 to 0.5 in increments of 0.1 and selecting the temperature value that yielded the best performance for
each method. For tuning the proposed loss LVRNS(U, V) in Def. 5.7, we conducted a grid search for λ from the set
{0.1, 0.3, 1, 3, 10, 30, 100}.
All experiments were conducted using a single NVIDIA RTX 4090 GPU.
D.2. Evaluation Details
For the linear evaluation protocol, we remove the projector head and using the pretrained encoder for downstream
classification tasks. Specifically, we extract the encoder outputs from the trained model without applying any augmentations.
These feature vectors are then normalized and used to train a linear classifier. Following prior works (Kornblith et al., 2019;
Lee et al., 2021; Koromilas et al., 2024), we report top 1 accuracy on the downstream dataset. We use SGD, setting the
learning rate to 0.1 without weight decay. The classifier is trained for 200 epochs with a batch size of 256.
E. Additional Experiments on the ImageNet Dataset
Table 4. Effect of our proposed loss (when combined with SimCLR) on the top-1 and top-5 classification accuracies (%). Bold entries
indicate the highest accuracy.
Dataset
Temperature
SimCLR
SimCLR + Ours
Top 1
Top 5
Top 1
Top 5
ImageNet-100
t = 0.1
70.14
91.14
69.50
90.80
t = 0.2
73.80
93.14
73.94
93.08
t = 0.3
72.30
92.94
74.04
93.24
t = 0.4
69.92
92.10
73.12
92.98
t = 0.5
68.60
90.90
72.88
92.84
We further validate the effectiveness of the proposed loss through experiments on the ImageNet dataset. Table 4 reports the
top-1 and top-5 classification accuracies on ImageNet-100 for various temperature values. For each temperature, we compare
SimCLR with and without the proposed loss. The results demonstrate that incorporating our loss generally improves
30

On the Similarities of Embeddings in Contrastive Learning
Table 5. Top-1 accuracy (%) on the full ImageNet dataset.
Method
Top-1 accuracy (%)
SimCLR
51.79
SimCLR + Ours
52.48
performance across a range of temperatures, with the largest gain observed at t = 0.3.
We also report results from 100-epoch training on the full ImageNet dataset. Using the same experimental setup as for
ImageNet-100, we compare SimCLR with our method (SimCLR + the proposed loss) using t = 0.2 and λ = 40. As shown
in Table 5, our method outperforms the baseline.
F. Discussion on the Proposed Loss for Variance Reduction
The auxiliary loss LVRNS(U, V) proposed in Def. 5.7 shows effectiveness in the following scenarios:
• Small Batch Training: As established in Theorem 5.5, the variance of negative-pair similarities increases as batch size
decreases. The proposed loss in Def. 5.7 directly penalizes this variance, making it particularly advantageous when
training with small batch sizes. This effect is empirically validated in Figure 4.
• Temperature Robustness: The performance of CL methods is often sensitive to the choice of the temperature
parameter, which affects the distribution of similarities among embedding pairs (Wang & Liu, 2021). By explicitly
encouraging negative-pair similarities towards the optimal value of −1/(n −1), the proposed loss reduces this
sensitivity and stabilizes performance across a wide range of temperature settings, as shown in Figure 3.
Despite its advantages, the proposed loss also presents several limitations:
• Suppression of Semantically Meaningful Variance: In some cases, variance in negative-pair similarities may
capture meaningful semantic differences between instances. Enforcing uniform similarity can potentially suppress this
informative structure, adversely affecting representation quality.
• Reduced Impact with Large Batch Sizes: The variance-reducing effect of proposed loss diminishes as batch size
increases, since the variance of negative-pair similarities naturally decreases in larger batches.
• Hyperparameter Sensitivity: The proposed loss introduces an additional hyperparameter, λ, which necessitates
careful tuning to achieve optimal performance.
31
