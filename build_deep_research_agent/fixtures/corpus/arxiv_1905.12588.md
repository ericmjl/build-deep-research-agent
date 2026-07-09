---
title: "Meta-Learning Representations for Continual Learning"
authors: "Khurram Javed, Martha White"
year: 2019
source: arxiv
source_id: "1905.12588"
url: "http://arxiv.org/abs/1905.12588v2"
domain: ai
---
Meta-Learning Representations for
Continual Learning
Khurram Javed, Martha White
Department of Computing Science
University of Alberta
T6G 1P8
kjaved@ualberta.ca, whitem@ualberta.ca
Abstract
A continual learning agent should be able to build on top of existing knowledge to
learn on new data quickly while minimizing forgetting. Current intelligent systems
based on neural network function approximators arguably do the opposite—they
are highly prone to forgetting and rarely trained to facilitate future learning. One
reason for this poor behavior is that they learn from a representation that is not
explicitly trained for these two goals. In this paper, we propose OML, an objective
that directly minimizes catastrophic interference by learning representations that
accelerate future learning and are robust to forgetting under online updates in con-
tinual learning. We show that it is possible to learn naturally sparse representations
that are more effective for online updating. Moreover, our algorithm is comple-
mentary to existing continual learning strategies, such as MER and GEM. Finally,
we demonstrate that a basic online updating strategy on representations learned by
OML is competitive with rehearsal based methods for continual learning. 1
1
Introduction
Continual learning—also called cumulative learning and lifelong learning—is the problem setting
where an agent faces a continual stream of data, and must continually make and learn new predictions.
The two main goals of continual learning are (1) to exploit existing knowledge of the world to quickly
learn predictions on new samples (accelerate future learning) and (2) reduce interference in updates,
particularly avoiding overwriting older knowledge. Humans, as intelligence agents, are capable
of doing both. For instance, an experienced programmer can learn a new programming language
signiﬁcantly faster than someone who has never programmed before and does not need to forget
the old language to learn the new one. Current state-of-the-art learning systems, on the other hand,
struggle with both (French, 1999; Kirkpatrick et al., 2017).
Several methods have been proposed to address catastrophic interference. These can generally be
categorized into methods that (1) modify the online update to retain knowledge, (2) replay or generate
samples for more updates and (3) use semi-distributed representations. Knowledge retention methods
prevent important weights from changing too much, by introducing a regularization term for each
parameter weighted by its importance (Kirkpatrick et al., 2017; Aljundi et al., 2018; Zenke et al.,
2017; Lee et al., 2017; Liu et al., 2018). Rehearsal methods interleave online updates with updates
on samples from a model. Samples from a model can be obtained by replaying samples from older
data (Lin, 1992; Mnih et al., 2015; Chaudhry et al., 2019; Riemer et al., 2019; Rebufﬁet al., 2017;
Lopez-Paz and Ranzato, 2017; Aljundi et al., 2019), by using a generative model learned on previous
data (Sutton, 1990; Shin et al., 2017), or using knowledge distillation which generates targets using
1We release an implementation of our method at https://github.com/khurramjaved96/mrcl
33rd Conference on Neural Information Processing Systems (NeurIPS 2019), Vancouver, Canada.
arXiv:1905.12588v2  [cs.LG]  30 Oct 2019

Representation Learning Network (RLN)
x1
x2
xn
. . .
Input
Prediction Learning Network (PLN)
Learned
representation
y
Output
Meta-parameters
(Only updated in the outer loop
during meta-training)
Adaptation Parameters
(Updated in the inner loop
and at meta-testing)
. . .
r1
r2
r3
r4
Network
Connections
Could be any diﬀerentiable
layer e.g a conv layer + relu
or fc layer + relu
rd
Network
Connections
Network
Connections
Network
Connections
Network
Connections
Network
Connections
Network
Connections
Figure 1: An example of our proposed architecture for learning representations for continual learning.
During the inner gradient steps for computing the meta-objective, we only update the parameters
in the prediction learning network (PLN). We then update both the representation learning network
(RLN) and the prediction learning network (PLN) by taking a gradient step with respect to our
meta-objective. The online updates for continual learning also only modify the PLN. Both RLN and
PLN can be arbitrary models.
predictions from an older predictor (Li and Hoiem, 2018). These ideas are all complementary to that
of learning representations that are suitable for online updating.
Early work on catastrophic interference focused on learning semi-distributed (also called sparse)
representations (French, 1991, 1999). Recent work has revisited the utility of sparse representations
for mitigating interference (Liu et al., 2019) and for using model capacity more conservatively to
leave room for future learning (Aljundi et al., 2019). These methods, however, use sparsity as a proxy,
which alone does not guarantee robustness to interference. A recently proposed online update for
neural networks implicitly learns representations to obtain non-interfering updates (Riemer et al.,
2019). Their objective maximizes the dot product between gradients computed for different samples.
The idea is to encourage the network to reach an area in the parameter space where updates to the
entire network have minimal interference and positive generalization. This idea is powerful: to specify
an objective to explicitly mitigate interference—rather than implicitly with sparse representations.
In this work, we propose to explicitly learn a representation for continual learning that avoids
interference and promotes future learning. We propose to train the representation with OML – a
meta-objective that uses catastrophic interference as a training signal by directly optimizing through
an online update. The goal is to learn a representation such that the stochastic online updates the
agent will use at meta-test time improve the accuracy of its predictions in general. We show that
using our objective, it is possible to learn representations that are more effective for online updating
in sequential regression and classiﬁcation problems. Moreover, these representations are naturally
highly sparse. Finally, we show that existing continual learning strategies, like Meta Experience
Replay (Riemer et al., 2019), can learn more effectively from these representations.
2
Problem Formulation
A Continual Learning Prediction (CLP) problem consists of an unending stream of samples
T = (X1, Y1), (X2, Y2), . . . , (Xt, Yt), . . .
for inputs Xt and prediction targets Yt, from sets X and Y respectively.2 The random vector Yt is sam-
pled according to an unknown distribution p(Y |Xt). We assume the process X1, X2, . . . , Xt, . . . has
a marginal distribution µ : X →[0, ∞), that reﬂects how often each input is observed. This assump-
tion allows for a variety of correlated sequences. For example, Xt could be sampled from a distribution
2This deﬁnition encompasses the continual learning problem where the tuples also include task descriptors
Tt (Lopez-Paz and Ranzato, 2017). Tt in the tuple (Xt, Tt, Yt) can simply be considered as part of the inputs.
2

Solution Manifold
for Task 1
Solution manifolds in a
representation space not
optimized for continual learning
Joint Training
Soluion
Parameter Space
Solution manifolds in a
representation space ideal
for continual learning
W
W
p1
p2
p3
p1
p2
p3
Figure 2: Effect of the representation on continual learning, for a problem where targets are generated
from three different distributions p1(Y |x), p2(Y |x) and p3(Y |x). The representation results in
different solution manifolds for the three distributions; we depict two different possibilities here. We
show the learning trajectory when training incrementally from data generates ﬁrst by p1, then p2
and p3. On the left, the online updates interfere, jumping between distant points on the manifolds.
On the right, the online updates either generalize appropriately—for parallel manifolds—or avoid
interference because manifolds are orthogonal.
potentially dependent on past variables Xt−1 and Xt−2. The targets Yt, however, are dependent only
on Xt, and not on past Xi. We deﬁne Sk = (Xj+1Yj+1), (Xj+2Yj+2) . . . , (Xj+k, Yj+k), a random
trajectory of length k sampled from the CLP problem T . Finally, p(Sk|T ) gives a distribution over
all trajectories of length k that can be sampled from problem T .
For a given CLP problem, our goal is to learn a function fW,θ that can predict Yt given Xt. More
concretely, let ℓ: Y × Y →R be the function that deﬁnes loss between a prediction ˆy ∈Y and target
y as ℓ(ˆy, y). If we assume that inputs X are seen proportionally to some density µ : X →[0, ∞),
then we want to minimize the following objective for a CLP problem:
LCLP (W, θ)
def
= E[ℓ(fW,θ(X), Y )] =
Z Z
ℓ(fW,θ(x), y)p(y|x)dy

µ(x)dx.
(1)
where W and θ represent the set of parameters that are updated to minimize the objective. To
minimize LCLP , we limit ourselves to learning by online updates on a single k length trajectory
sampled from p(Sk|T ). This changes the learning problem from the standard iid setting – the agent
sees a single trajectory of correlated samples of length k, rather than getting to directly sample from
p(x, y) = p(y|x)µ(x). This modiﬁcation can cause signiﬁcant issues when simply applying standard
algorithms for the iid setting. Instead, we need to design algorithms that take this correlation into
account.
A variety of continual problems can be represented by this formulation. One example is an online
regression problem, such as predicting the next spatial location for a robot given the current location;
another is the existing incremental classiﬁcation benchmarks. The CLP formulation also allows for
targets Yt that are dependent on a history of the most recent m observations. This can be obtained by
deﬁning each Xt to be the last m observations. The overlap between Xt and Xt−1 does not violate
the assumptions on the correlated sequence of inputs. Finally, the prediction problem in reinforcement
learning—predicting the value of a policy from a state—can be represented by considering the inputs
Xt to be states and the targets to be sampled returns or bootstrapped targets.
3
Meta-learning Representations for Continual Learning
Neural networks, trained end-to-end, are not effective at minimizing the CLP loss using a single
trajectory sampled from p(Sk|T ) for two reasons. First, they are extremely sample-inefﬁcient,
requiring multiple epochs of training to converge to reasonable solutions. Second, they suffer from
catastrophic interference when learning online from a correlated stream of data (French, 1991). Meta-
learning is effective at making neural networks more sample efﬁcient (Finn et al., 2017). Recently,
Nagabandi et al. (2019); Al-Shedivat et al. (2018) showed that it can also be used for quick adaptation
from a stream of data. However, they do not look at the catastrophic interference problem. Moreover,
3

their work meta-learns a model initialization, an inductive bias we found insufﬁcient for solving the
catastrophic interference problem (See Appendix C.1).
To apply neural network to the CLP problem, we propose meta-learning a function φθ(X) – a deep
Representation Learning Network (RLN) parametrized by θ – from X →Rd. We then learn another
function gW from Rd →Y, called a Prediction Learning Network (PLN). By composing the two
functions we get fW,θ(X) = gW (φθ(X)), which constitute our model for the CLP tasks as shown in
Figure 1. We treat θ as meta-parameters that are learned by minimizing a meta-objective and then
later ﬁxed at meta-test time. After learning θ, we learn gW from Rd →Y for a CLP problem from a
single trajectory S using fully online SGD updates in a single pass. A similar idea has been proposed
by Bengio et al. (2019) for learning causal structures.
For meta-training, we assume a distribution over CLP problems given by p(T ). We consider two
meta-objectives for updating the meta-parameters θ. (1) MAML-Rep, a MAML (Finn et al., 2017)
like few-shot-learning objective that learns an RLN instead of model initialization, and OML (Online
aware Meta-learning) – an objective that also minimizes interference in addition to maximizing fast
adaptation for learning the RLN. Our OML objective is deﬁned as:
min
W,θ
X
Ti∼p(T )
OML(W, θ)
def
=
X
Ti∼p(T )
X
Sj
k∼p(Sk|Ti)
h
LCLPi

U(W, θ, Sj
k)
i
(2)
where Sj
k = (Xi
j+1Y i
j+1), (Xi
j+2Y i
j+2), . . . , (Xi
j+kY i
j+k). U(Wt, θ, Sj
k) = (Wt+k, θ) represents an
update function where Wt+k is the weight vector after k steps of stochastic gradient descent. The jth
update step in U is taken using parameters (Wt+j−1, θ) on sample (Xi
t+j, Y i
t+j) to give (Wt+j, θ).
MAML-Rep and OML objectives can be implemented as Algorithm 1 and 2 respectively, with the
primary difference between the two highlighted in blue. Note that MAML-Rep uses the complete
batch of data Sk to do l inner updates (where l is a hyper-parameter) whereas OML uses one data
point from Sk for one update. This allows OML to take the effects of online continual learning –
such as catastrophic forgetting – into account.
Algorithm 1: Meta-Training : MAML-Rep
Require: p(T ): distribution over CLP problems
Require: α, β: step size hyperparameters
Require: l: No of inner gradient steps
1: randomly initialize θ
2: while not done do
3:
randomly initialize W
4:
Sample CLP problem Ti ∼p(T )
5:
Sample Strain from p(Sk|Ti)
6:
W0 = W
7:
for j in 1, 2, . . . , l do
8:
Wj = Wj−1 −α∇Wj−1ℓi(fθ,Wl(Strain[:, 0]), Strain[:, 1])
9:
end for
10:
Sample Stest from p(Sk|Ti)
11:
Update θ ←θ −β∇θℓi(fθ,Wl(Stest[:, 0]), Stest[:, 1])
12: end while
The goal of the OML ob-
jective is to learn represen-
tations suitable for online
continual learnings. For an
illustration of what would
constitute an effective rep-
resentation for continual
learning, suppose that we
have three clusters of inputs,
which have signiﬁcantly dif-
ferent p(Y |x), correspond-
ing to p1, p2 and p3. For
a ﬁxed 2-dimensional repre-
sentation φθ : X →R2, we
can consider the manifold
of solutions W ∈R2 given
by a linear model that pro-
vide equivalently accurate solutions for each pi. These three manifolds are depicted as three different
colored lines in the W ∈R2 parameter space in Figure 2. The goal is to ﬁnd one parameter vector
W that is effective for all three distributions by learning online on samples from three distributions
sequentially. For two different representations, these manifolds, and their intersections can look very
different. The intuition is that online updates from a W are more effective when the manifolds are
either parallel—allowing for positive generalization—or orthogonal—avoiding interference. It is
unlikely that a representation producing such manifolds would emerge naturally. Instead, we will
have to explicitly ﬁnd it. By taking into account the effects of online continual learning, the OML
objective optimizes for such a representation.
We can optimize this objective similarly to other gradient-based meta-learning objectives. Early work
on learning-to-learn considered optimizing parameters through learning updates themselves, though
typically considering approaches using genetic algorithms (Schmidhuber, 1987). Improvements
4

in automatic differentiation have made it more feasible to compute gradient-based meta-learning
updates (Finn, 2018). Some meta-learning algorithms have similarly considered optimizations
through multiple steps of updating for the few-shot learning setting (Finn et al., 2017; Li et al., 2017;
Al-Shedivat et al., 2018; Nagabandi et al., 2019) for learning model initializations. The successes
in these previous works in optimizing similar objectives motivate OML as a feasible objective for
Meta-learning Representations for Continual Learning.
4
Evaluation
Algorithm 2: Meta-Training : OML
Require: p(T ): distribution over CLP problems
Require: α, β: step size hyperparameters
1: randomly initialize θ
2: while not done do
3:
randomly initialize W
4:
Sample CLP problem Ti ∼p(T )
5:
Sample Strain from p(Sk|Ti)
6:
W0 = W
7:
for j = 1, 2, . . . , k do
8:
(Xj, Yj) = Strain[j]
9:
Wj = Wj−1 −α∇Wj−1ℓi(fθ,Wj−1(Xj), Yj)
10:
end for
11:
Sample Stest from p(Sk|Ti)
12:
Update θ ←θ −β∇θℓi(fθ,Wk(Stest[:, 0]), Stest[:, 1])
13: end while
In this section, we investigate the
question: can we learn a representa-
tion for continual learning that pro-
motes future learning and reduces
interference? We investigate this
question by meta-learning the repre-
sentations ofﬂine on a meta-training
dataset. At meta-test time, we ini-
tialize the continual learner with this
representation and measure predic-
tion error as the agent learns the
PLN online on a new set of CLP
problems (See Figure 1).
4.1
CLP Benchmarks
We evaluate on a simulated regres-
sion problem and a sequential clas-
siﬁcation problem using real data.
Incremental Sine Waves: An Incremental Sine Wave CLP problem is deﬁned by ten (randomly
generated) sine functions, with x = (z, n) for z ∈[−5, 5] as input to the sine function and n a
one-hot vector for {1, . . . , 10} indicating which function to use. The targets are deterministic, where
(x, y) corresponds to y = sinn(z). Each sine function is generated once by randomly selecting an
amplitude in the range [0.1, 5] and phase in [0, π]. A trajectory S400 from the CLP problem consists
of 40 mini-batches from the ﬁrst sine function in the sequence (Each mini-batch has eight elements),
and then 40 from the second and so on. Such a trajectory has sufﬁcient information to minimize loss
for the complete CLP problem. We use a single regression head to predict all ten functions, where
the input id n makes it possible to differentiate outputs for the different functions. Though learnable,
this input results in signiﬁcant interference across different functions.
Split-Omniglot: Omniglot is a dataset of over 1623 characters from 50 different alphabets (Lake et al.,
2015). Each character has 20 hand-written images. The dataset is divided into two parts. The ﬁrst 963
classes constitute the meta-training dataset whereas the remaining 660 the meta-testing dataset. To
deﬁne a CLP problem on this dataset, we sample an ordered set of 200 classes (C1, C2, C3, . . . , C200).
X and Y, then, constitute of all images of these classes. A trajectory S1000 from such a problem is a
trajectory of images – ﬁve images per class – where we see all ﬁve images of C1 followed by ﬁve
images of C2 and so on. This makes k = 5 × 200 = 1000. Note that the sampling operation deﬁnes
a distribution p(T ) over problems that we use for meta-training.
4.2
Meta-Training Details
Incremental Sine Waves: We sample 400 functions to create our meta-training set and 500 for
benchmarking the learned representation. We meta-train by sampling multiple CLP problems. During
each meta-training step, we sample ten functions from our meta-training set and assign them task
ids from one to ten. We concatenate 40 mini-batches generated from function one, then function
two and so on, to create our training trajectory S400. For evaluation, we similarly randomly sample
ten functions from the test set and create a single trajectory. We use SGD on the MSE loss with a
mini-batch size of 8 for online updates, and Adam (Kingma and Ba, 2014) for optimizing the OML
objective. Note that the OML objective involves computing gradients through a network unrolled for
5

Pretraining
SR-NN
OML
Oracle

Mean
Squared
Error
No of functions learned
0.0
0.5
1.0
1.5
1
3
7
9
5
10
8
6
4
2
Continual Regression Experiment
Error Distribution
1
3
7
9
10
8
6
4
2
5
1
2
3
0
1
2
3
0
1
2
3
0
Task ID

Mean
Squared
Error
Figure 3: Mean squared error across all 10 regression tasks. The x-axis in (a) corresponds to seeing
all data points of samples for class 1, then class 2 and so on. These learning curves are averaged over
50 runs, with error bars representing 95% conﬁdence interval drawn by 1,000 bootstraps. We can see
that the representation trained on iid data—Pre-training—is not effective for online updating. Notice
that in the ﬁnal prediction accuracy in (b), Pre-training and SR-NN representations have accurate
predictions for task 10, but high error for earlier tasks. OML, on the other hand, has a slight skew
in error towards later tasks in learning but is largely robust. Oracle uses iid sampling and multiple
epochs and serves as a best case bound.
400 steps. At evaluation time, we use the same learning rate as used during the inner updates in the
meta-training phase for OML. For our baselines, we do a grid search over learning rates and report
the results for the best performing parameter.
We found that having a deeper representation learning network (RLN) improved performance. We use
six layers for the RLN and two layers for the PLN. Each hidden layer has a width of 300. The RLN
is only updated with the meta-update and acts as a ﬁxed feature extractor during the inner updates in
the meta-learning objective and at evaluation time.
Split-Omniglot: We learn an encoder – a deep CNN with 6 convolution and two FC layers – using
the MAML-Rep and the OML objective. We treat the convolution parameters as θ and FC layer
parameters as W. Because optimizing the OML objective is computationally expensive for H = 1000
(It involves unrolling the computation graph for 1,000 steps), we approximate the two objectives.
For MAML-Rep we learn the φθ by maximizing fast adaptation for a 5 shot 5-way classiﬁer. For
OML, instead of doing |Strain| no of inner-gradient steps as described in Algorithm 2, we go over
Strain ﬁve steps at a time. For kth ﬁve steps in the inner loop, we accumulate our meta-loss on
Stest[0 : 5 × k], and update our meta-parameters using these accumulated gradients at the end as
explained in Algorithm 3 in the Appendix. This allows us to never unroll our computation graphs for
more than ﬁve steps (Similar to truncated back-propagation through time) and still take into account
the effects of interference at meta-training.
Finally, both MAML-Rep and OML use 5 inner gradient steps and similar network architectures for a
fair comparison. Moreover, for both methods, we try multiple values for the inner learning rate α and
report the results for the best parameter. For more details about hyper-parameters see the Appendix.
For more details on implementation, see Appendix B.
4.3
Baselines
We compare MAML-Rep and OML – the two Meta-learneing based Representations Leanring
methods to three baselines.
Scratch simply learns online from a random network initialization, with no meta-training.
Pre-training uses standard gradient descent to minimize prediction error on the meta-training set.
We then ﬁx the ﬁrst few layers in online training. Rather than restricting to the same 6-2 architecture
for the RLN and PLN, we pick the best split using a validation set.
SR-NN use the Set-KL method to learn a sparse representation (Liu et al., 2019) on the meta-training
set. We use multiple values of the hyper-parameter β for SR-NN and report results for one that
performs the best. We include this baseline to compare to a method that learns a sparse representation.
6

Accuracy
0.0
0.2
0.4
0.6
0.8
1.0
0.0
0.2
0.4
0.6
0.8
1.0
No of classes learned incrementally
0.0
0.2
0.4
0.6
0.8
1.0
IID, Multiple Epochs, Train Error
IID, Multiple Epochs, Test Error
MAML-Rep
SRNN
0
200
100
50
150
0
200
100
50
150
(c)
(d)
OML
Scratch
All of them
Online, Single Pass, Train Error
Online, Single Pass, Test Error
OML
MAML-Rep
SRNN
0
200
100
50
150
0
200
100
50
150
0.0
0.2
0.4
0.6
0.8
1.0
(a)
(b)
Pretraining
Scratch
OML
MAML-Rep
SRNN
Pretraining
Scratch
Figure 4: Comparison of representations learned by the MAML-Rep, OML objective and the baselines
on Split-Omniglot. All curves are averaged over 50 CLP runs with 95% conﬁdence intervals drawn
using 1,000 bootstraps. At every point on the x-axis, we only report accuracy on the classes seen
so far. Even though both MAML-Rep and OML learn representations that result in comparable
performance of classiﬁers trained under the IID setting (c and d), OML out-performs MAML-Rep
when learning online on a highly correlated stream of data showing it learns representations more
robust to interference. SR-NN, which does not do meta-learning, performs worse even under the IID
setting showing it learns worse representations.
4.4
Meta-Testing
We report results of LCLP (Wonline, θmeta) for fully online updates on a single Sk for each CLP
problem. For each of the methods, we separately tune the learning rate on a ﬁve validation trajectories
and report results for the best performing parameter.
Incremental Sine Waves: We plot the average mean squared error over 50 runs on the full testing
set, when learning online on unseen sequences of functions, in Figure 3 (left). OML can learn new
functions with a negligible increase in average MSE. The Pre-training baseline, on the other hand,
clearly suffers from interference, with increasing error as it tries to learn more and more functions.
SR-NN, with its sparse representation, also suffers from noticeably more interference than OML.
From the distribution of errors for each method on the ten functions, shown in Figure 3 (right), we
can see that both Pre-training and SR-NN have high errors for functions learned in the beginning
whereas OML performs only slightly worse on those.
16
18
16
18
6
20
10
8
12
14
0.6
0.4
0.2
0.3
0.2
0.5
0.4
0.1
Pretraining
OML
OML
Pretraining
6
20
10
8
12
14
1.0
0.8
Meta-testing: Train Accuracy
Accuracy
No of classes learned incrementally
SR-NN
SR-NN
Meta-testing: Test Accuracy
Figure 5: OML scales to more complex datasets
such a Mini-imagenet. We use the existing meta-
training/meta-testing split of mini-imagenet. At
meta-testing, we learn a 20 way classiﬁer using 30
samples per class.
Split-Omniglot:
We report classiﬁcation accuracy on the train-
ing trajectory (Strain) as well as the test set in
Figure 4. Note that training accuracy is a mean-
ingful metric in continual learning as it measures
forgetting. The test set accuracy reﬂects both
forgetting and generalization error. Our method
can learn the training trajectory almost perfectly
with minimal forgetting. The baselines, on the
other hand, suffer from forgetting as they learn
more classes sequentially. The higher training
accuracy of our method also translates into bet-
ter generalization on the test set. The difference
in the train and test performance is mainly due
to how few samples are given per class: only 15
for training and 5 for testing.
As a sanity check, we also trained classiﬁers by sampling data IID for 5 epochs and report the results
in Fig. 4 (c) and (d). The fact that OML and MAML-Rep do equally well with IID sampling indicates
that the quality of representations (φθ = Rd) learned by both objectives are comparable and the
higher performance of OML is indeed because the representations are more suitable for incremental
learning.
Moreover, to test if OML can learn representations on more complex datasets, we run the same
experiments on mini-imagenet and report the results in Figure 5.
7

OML
SR-NN
(Sparse)
Pre-training
Random Instance 1
Random Instance 2
Average Activation
0.0
1.0
Random Instance 3
SR-NN
Figure 6: We reshape the 2304 length representation vectors into 32x72, normalize them to have a
maximum value of one and visualize them; here random instance means representation for a randomly
chosen input from the training set, whereas average activation is the mean representation for the
complete dataset. For SR-NN, we re-train the network with a different value of parameter β to have
the same instance sparsity as OML. Note that SR-NN achieves this sparsity by never using a big part
of representation space. OML, on the other hand, uses the full representation space. In-fact, OML
has no dead neurons whereas even pre-training results in some part of the representation never being
used.
4.5
What kind of representations does OML learn?
As discussed earlier, French (1991) proposed that sparse representations could mitigate forgetting.
Ideally, such a representation is instance sparse–using a small percentage of activations to represent
an input– while also utilizing the representation to its fullest. This means that while most neurons
would be inactive for a given input, every neuron would participate in representing some input. Dead
neurons, which are inactive for all inputs, are undesirable and may as well be discarded. An instance
sparse representation with no dead neurons reduces forgetting because each update changes only a
small number of weights which in turn should only affect a small number of inputs. We hypothesize
that the representation learned by OML will be sparse, even though the objective does not explicitly
encourage this property.
We compute the average instance sparsity on the Omniglot training set, for OML, SR-NN, and
Pre-training. OML produces the most sparse network, without any dead neurons. The network
learned by Pre-training, in comparison, uses over 10 times more neurons on average to represent an
input. The best performing SR-NN used in Figure 4 uses 4 times more neurons. We also re-trained
SR-NN with a parameter to achieve a similar level of sparsity as OML, to compare representations of
similar sparsity rather than representations chosen based on accuracy. We use β = 0.05 which results
in an instance sparsity similar to OML.
Table 1: Instance sparisty and dead neuron percentage
for different methods. OML learns highly sparse repre-
sentations without any dead neurons. Even Pre-training,
which does not optimize for sparsity, ends up with some
dead neurons, on the other hand.
Method
Instance Sparsity
Dead Neurons
OML
3.8%
0%
SR-NN (Best)
15%
0.7%
SR-NN (Sparse)
4.9%
14%
Pre-Training
38%
3%
We visualize all the solutions in Figure
6. The plots highlight that OML learns
a highly sparse and well-distributed rep-
resentation, taking the most advantage of
the large capacity of the representation.
Surprisingly, OML has no dead neurons,
which is a well-known problem when learn-
ing sparse representations (Liu et al., 2019).
Even Pre-training, which does not have
an explicit penalty to enforce sparsity, has
some dead neurons. Instance sparsity and
dead neurons percentage for each method
are reported in Table 1.
5
Improvements by Combining with Knowledge Retention Approaches
We have shown that OML learns effective representations for continual learning. In this section, we
answer a different question: how does OML behave when it is combined with existing continual
8

Table 2: OML combined with existing continual learning methods. All memory-based methods
use a buffer of 200. Error margins represent one std over 10 runs. Performance of all methods is
considerably improved when they learn from representations learned by OML moreover, even online
updates are competitive with rehearsal based methods with OML. Finally, online updates on OML
outperform all methods when they learn from other representations. Note that MER does better than
approx IID in some cases because it does multiple rehearsal-based updates for every sample.
Split-Omniglot
One class per task, 50 tasks
Five classes per task, 20 tasks
Method
Standard
OML
Pre-training
Standard
OML
Pre-training
Online
04.64 ± 2.61
64.72 ± 2.57
21.16 ± 2.71
01.40 ± 0.43
55.32 ± 2.25
11.80 ± 1.92
Approx IID
53.95 ± 5.50
75.12 ± 3.24
54.29 ± 3.48
48.02 ± 5.67
67.03 ± 2.10
46.02 ± 2.83
ER-Reservoir
52.56 ± 2.12
68.16 ± 3.12
36.72 ± 3.06
24.32 ± 5.37
60.92 ± 2.41
37.44 ± 1.67
MER
54.88 ± 4.12
76.00 ± 2.07
62.76 ± 2.16
29.02 ± 4.01
62.05 ± 2.19
42.05 ± 3.71
EWC
05.08 ± 2.47
64.44 ± 3.13
18.72 ± 3.97
02.04 ± 0.35
56.03 ± 3.20
10.03 ± 1.53
learning methods? We test the performance of EWC (Lee et al., 2017), MER (Riemer et al., 2019) and
ER-Reservoir (Chaudhry et al., 2019), in their standard form—learning the whole network online—as
well as with pre-trained ﬁxed representations. We use pre-trained representations from OML and
Pre-training, obtained in the same way as described in earlier sections. For the Standard online form
of these algorithms, to avoid the unfair advantage of meta-training, we initialize the networks by
learning iid on the meta-training set.
As baselines, we also report results for (a) fully online SGD updates that update one point at a time in
order on the trajectory and (b) approximate IID training where SGD updates are used on a random
shufﬂing of the trajectory, removing the correlation.
We report the test set results for learning 50 tasks with one class per task and learning 20 tasks with 5
tasks per class in Split-Omniglot in Table 2. For each of the methods, we do a 15/5 train/test split
for each Omniglot class and test multiple values for all the hyperparameters and report results for
the best setting. The conclusions are surprisingly clear. (1) OML improves all the algorithms; (2)
simply providing a ﬁxed representation, as in Pre-training, does not provide nearly the same gains as
OML and (3) OML with a basic Online updating strategy is already competitive, outperforming all
the continual learning methods without OML. There are a few additional outcomes of note. OML
outperforms even approximate IID sampling, suggesting it is not only mitigating interference but also
making learning faster on new data. Finally, the difference in online and experience replay based
algorithms for OML is not as pronounced as it is for other representations.
6
Conclusion and Discussion
In this paper, we proposed a meta-learning objective to learn representations that are robust to inter-
ference under online updates and promote future learning. We showed that using our representations,
it is possible to learn from highly correlated data streams with signiﬁcantly improved robustness to
forgetting. We found sparsity emerges as a property of our learned representations, without explicitly
training for sparsity. We ﬁnally showed that our method is complementary to the existing state of the
art continual learning methods, and can be combined with them to achieve signiﬁcant improvements
over each approach alone.
An important next step for this work is to demonstrate how to learn these representations online
without a separate meta-training phase. Initial experiments suggest it is effective to periodically
optimize the representation on a recent buffer of data, and then continue online update with this
updated ﬁxed representation. This matches common paradigms in continual learning—based on the
ideas of a sleep phase and background planning—and is a plausible strategy for continually adapting
the representation network for a continual stream of data. Another interesting extension to the work
would be to use the OML objective to meta-learn some other aspect of the learning process – such as
a local learning rule (Metz et al., 2019) or an attention mechanism – by minimizing interference.
9

References
Al-Shedivat, Maruan, Trapit Bansal, Yuri Burda, Ilya Sutskever, Igor Mordatch, and Pieter Abbeel
(2018). Continuous adaptation via meta-learning in nonstationary and competitive environments.
International Conference on Learning Representations.
Aljundi, Rahaf, Francesca Babiloni, Mohamed Elhoseiny, Marcus Rohrbach, and Tinne Tuytelaars
(2018). Memory aware synapses: Learning what (not) to forget. In European Conference on
Computer Vision.
Aljundi, Rahaf, Min Lin, Baptiste Goujaud, and Yoshua Bengio (2019). Gradient based sample
selection for online continual learning. Advances in Neural Information Processing Systems.
Aljundi, Rahaf, Marcus Rohrbach, and Tinne Tuytelaars (2019). Selﬂess sequential learning. Interna-
tional Conference on Learning Representations.
Bengio, Yoshua, Tristan Deleu, Nasim Rahaman, Rosemary Ke, Sébastien Lachapelle, Olexa Bilaniuk,
Anirudh Goyal, and Christopher Pal (2019). A meta-transfer objective for learning to disentangle
causal mechanisms. arXiv preprint arXiv:1901.10912.
Chaudhry, Arslan, Marc’Aurelio Ranzato, Marcus Rohrbach, and Mohamed Elhoseiny (2019).
Efﬁcient lifelong learning with a-gem. International Conference on Learning Representations.
Chaudhry, Arslan, Marcus Rohrbach, Mohamed Elhoseiny, Thalaiyasingam Ajanthan, Puneet K
Dokania, Philip HS Torr, and Marc’Aurelio Ranzato (2019). Continual learning with tiny episodic
memories. arXiv:1902.10486.
Finn, Chelsea (2018, Aug). Learning to Learn with Gradients. Ph. D. thesis, EECS Department,
University of California, Berkeley.
Finn, Chelsea, Pieter Abbeel, and Sergey Levine (2017). Model-agnostic meta-learning for fast
adaptation of deep networks. In International Conference on Machine Learning.
French, Robert M (1991). Using semi-distributed representations to overcome catastrophic forgetting
in connectionist networks. In Annual cognitive science society conference. Erlbaum.
French, Robert M (1999). Catastrophic forgetting in connectionist networks. Trends in cognitive
sciences.
Kingma, Diederik P and Jimmy Ba (2014).
Adam: A method for stochastic optimization.
arXiv:1412.6980.
Kirkpatrick, James, Razvan Pascanu, Neil Rabinowitz, Joel Veness, Guillaume Desjardins, Andrei A
Rusu, Kieran Milan, John Quan, Tiago Ramalho, Agnieszka Grabska-Barwinska, et al. (2017).
Overcoming catastrophic forgetting in neural networks. National academy of sciences.
Lake, Brenden M, Ruslan Salakhutdinov, and Joshua B Tenenbaum (2015). Human-level concept
learning through probabilistic program induction. Science.
Lee, Sang-Woo, Jin-Hwa Kim, Jaehyun Jun, Jung-Woo Ha, and Byoung-Tak Zhang (2017). Overcom-
ing catastrophic forgetting by incremental moment matching. In Advances in Neural Information
Processing Systems.
Li, Zhizhong and Derek Hoiem (2018). Learning without forgetting. IEEE Transactions on Pattern
Analysis and Machine Intelligence.
Li, Zhenguo, Fengwei Zhou, Fei Chen, and Hang Li (2017). Meta-sgd: Learning to learn quickly for
few-shot learning. arXiv:1707.09835.
Lin, Long-Ji (1992). Self-improving reactive agents based on reinforcement learning, planning and
teaching. Machine learning.
Liu, Vincent, Raksha Kumaraswamy, Lei Le, and Martha White (2019). The utility of sparse
representations for control in reinforcement learning. AAAI Conference on Artiﬁcial Intelligence.
10

Liu, Xialei, Marc Masana, Luis Herranz, Joost Van de Weijer, Antonio M Lopez, and Andrew D
Bagdanov (2018). Rotate your networks: Better weight consolidation and less catastrophic
forgetting. In International Conference on Pattern Recognition.
Lopez-Paz, David and Marc’Aurelio Ranzato (2017). Gradient episodic memory for continual
learning. In Advances in Neural Information Processing Systems.
Metz, Luke, Niru Maheswaranathan, Brian Cheung, and Jascha Sohl-dickstein (2019). Meta-learning
update rules for unsupervised representation learning. International Conference on Learning
Representations.
Mnih, Volodymyr, Koray Kavukcuoglu, David Silver, Andrei A Rusu, Joel Veness, Marc G Bellemare,
Alex Graves, Martin Riedmiller, Andreas K Fidjeland, Georg Ostrovski, et al. (2015). Human-level
control through deep reinforcement learning. Nature.
Nagabandi, Anusha, Chelsea Finn, and Sergey Levine (2019). Deep online learning via meta-learning:
Continual adaptation for model-based rl. International Conference on Learning Representations.
Rebufﬁ, Sylvestre-Alvise, Alexander Kolesnikov, Georg Sperl, and Christoph H Lampert (2017).
icarl: Incremental classiﬁer and tation learning. In Conference on Computer Vision and Pattern
Recognition.
Riemer, Matthew, Ignacio Cases, Robert Ajemian, Miao Liu, Irina Rish, Yuhai Tu, and Gerald
Tesauro (2019). Learning to learn without forgetting by maximizing transfer and minimizing
interference. International Conference on Learning Representations.
Schmidhuber, Jurgen (1987). Evolutionary principles in self-referential learning, or on learning how
to learn. Ph. D. thesis, Institut fur Informatik,Technische Universitat Munchen.
Shin, Hanul, Jung Kwon Lee, Jaehong Kim, and Jiwon Kim (2017). Continual learning with deep
generative replay. In Advances in Neural Information Processing Systems.
Sutton, Richard (1990). Integrated architectures for learning planning and reacting based on approxi-
mating dynamic programming. In International Conference on Machine Learning.
Zenke, Friedemann, Ben Poole, and Surya Ganguli (2017). Continual learning through synaptic
intelligence. In International Conference on Machine Learning.
11

. . .
Sample a trajectory
 from the stream
RLN
PLN
W0
Use L(Yi+1, Y 0
i+1)
to update W0 to W1
Use L(Yi+k, Y 0
i+k)
to update Wk−1 to Wk
W1
RLN
PLN
RLN
PLN
Stest = (Xrand, Y rand)
Sample a random
 batch of data
2
RLN
PLN
‘
Data stream
T = (X0, Y0), (X1, Y1), . . . , (Xk, Yk), . . . , (Xn, Yn), . . . ,
RLN
PLN
W 0
0
4
1
3
Update RLN and PLN using
gradients from random batch
✓0
✓
✓
✓
✓
Sk = (Xi+1, Yi+1), (Xi+2, Yi+2), . . . , (Xi+k, Yi+k)
Wk
Wk
Xi+1
Y 0
i+1
Xi+2
Y 0
i+2
L(Yi+1, Y 0
i+1)
Xrand
+
Xtraj
Y 0
rand
+
Y 0
traj
L(Y rand + Y traj, Y 0
rand + Y 0
traj)
Backpropogation
Minimize loss on a random
batch with respect to
initial parameters
Figure 7: Flowchart elucidating a single gradient update for representation learning. (1) We sample
trajectory Sk from our stream of data for inner updates in the meta-training, and another trajectory
Stest for evaluation. (2) We use Sk to do k gradient updates on the PLN (Prediction learning network).
(3) We then use this updated network to compute loss on the Sk + Stest and compute gradients for
this loss with respect to the initial parameters θ1, W1. (4) Finally, we update our initial parameters
θ, W0 to θ′, W ′
0.
Table 3: Parameters for Sinusoidal Regression Experiment
Parameter
Description
Value
Meta LR
Learning rate used for the meta-update
1e-4
Meta Update Optimizer
Optimizer used for the meta-update
Adam
Inner LR
LR used for the inner updates for meta-learning
0.003
Inner LR Search
Inner LRs tried before picking the best
[0.1, 1e-6]
Steps-per-function
Number of gradient updates for each of the ten tasks
40
Inner steps
Number of inner gradient steps
400
Total layers
Total layers in the fully connected NN
9
Layer Width
Number of neurons in each layer
300
Non-linearly
Non-linearly used
relu
RLN Layers
Number of layers used for learning representation
6
Pre-training set
Number of functions in the meta-training set
400
Appendix
A
Discussion on the Connection to Few-Shot Meta-Learning
Our approach is different from gradient-based meta-learning in two ways; ﬁrst, we only update PLN
during the inner updates whereas maml (and other gradient-based meta-learning techniques) update
all the parameters in the inner update. By not updating the initial layers in the inner update, we change
the optimization problem from "ﬁnding a model initialization with xyz properties" to "ﬁnding a model
initialization and learning a ﬁxed representation such that starting from the learned representation
it has xyz properties." This gives our model freedom to transform the input into a more desirable
representation for the task—such as a sparse representation.
Secondly, we sample trajectories and do correlated updates in the inner updates, and compute the
meta-loss with respect to a batch of data representing the CLP problem at large. This changes the
12

Table 4: Parameters for Omniglot Representation Learning
Parameter
Description
Value
Meta LR
Learning rate used for the meta-update
1e-4
Meta update optimizer
Optimizer used for the meta-update
Adam
Inner LR
LR used for the inner updates for meta-learning
0.03
Inner LR Search
Inner LRs tried before picking the best
[0.1, 1e-6]
Inner steps
Number of inner gradient steps
20
Conv-layers
Total convolutional layers
6
FC Layers
Total fully connected layers
2
RLN
Layers in RLN
6
Kernel
Size of the convolutional kernel
3x3
Non-linearly
Non-linearly used
relu
Stride
Stride for convolution operation in each layer
[2,1,2,1,2,2]
# kernels
Number of convolution kernels in each layer
256 each
Input
Dimension of the input image
84 x 84
optimization from "ﬁnding an initialization that allows for quick adaptation" (such as in maml Finn
(2018)) to "ﬁnding an initialization that minimizes interference and maximizes transfer." Note that
we learn the RLN and the initialization for PLN using a single objective in an end-to-end manner.
We empirically found that having an RLN is extremely important for effective continual learning, and
vanilla maml trained with correlated trajectories performed poorly for online learning.
B
Reproducing Results
We release our code, and pretrained OML models for Split-Omniglot and Incremental Sine Waves
available at https://github.com/Khurramjaved96/mrcl. In addition, we also provide details
of hyper-parameters used from learning the representations of Incremental Sine Waves experiment
and Split-Omniglot in Table 3 and 4 respectively.
For online learning experiments in Figure 3 and 4, we did a sweep over the only hyper-parameter,
learning rate, in the list [0.3, 0.1, 0.03, 0.01, 0.003, 0.001, 0.0003, 0.0001, 0.00003, 0.00001] for each
method on a ﬁve validation trajectories and reported result for the best learning rate on 50 random
trajectories.
B.1
Computing Infrastructure
We learn all representations on a single V100 GPU; even with a deep neural network and meta-updates
involving roll-outs of length up to 400, OML can learn representations in less than ﬁve hours for both
the regression problem and omniglot experiments. For smaller roll-outs in Omniglot, it is possible
to learn good representations with-in an hour. Note that this is despite the fact that we did not use
batch-normalization layers or skip connections which are known to stabilize and accelerate training.
C
Representations
We present more samples of the learned representations in Figure 8. We also include the averaged
representation for the best performing SR-NN model (15% instance sparsity) in Figure 10 which was
excluded from Figure 6 due to lack of space.
13

OML
SR-NN (4.9%)
SR-NN (15%)
Pretraining
Figure 8: More samples of representations for random input images for different methods. Here
SR-NN (4.9%) is trained to have similar sparsity as OML whereas SR-NN (15%) is trained to have
the best performance on Split-Omniglot benchmark.
OML: Learning RLN
OML: Learning an Initialization
Number of classes learned
Accuracy
25
50
75
100
125
150
175
0.0
0.2
0.4
0.6
0.8
1.0
10
Omniglot Training Trajectory Performance
Figure 9: Instead of learning an encoder φθ , we learn an initialization by updating both θ and W
in the inner loop of meta-training. In "OML without RLN," we also update both at meta-test time
whereas in "OML without RLN at test time," we ﬁx theta at meta-test time just like we do for OML .
For each of the methods, we report the training error during meta-testing. It’s clear from the results
that a model initialization is not an effective bias for incremental learning. Interestingly, "OML with
RLN at test time" doesn’t do very poorly. However, if we know we’ll be ﬁxing θ at meta-test time, it
doesn’t make sense to update it in the inner loop of meta-training (Since we’d want the inner loop
setting to be as similar to meta-test setting as possible.
Figure 10: Average activation map for the best performing SR-NN with 15% sparsity. Scale goes
from 0 to max (Light to dark green.)
14

Algorithm 3: Meta-Training : Approximate Implementation of the OML Objective
Require: p(T ): distribution over tasks
Require: α, β: step size hyperparameters
Require: m: No of inner gradient steps per update before truncation
1: randomly initialize θ, W
2: while not done do
3:
Sample task Ti ∼p(T )
4:
Sample Si
train from p(Sk|Ti)
5:
W0 = W
6:
∇accum = 0
7:
while j ≤|Strain| do
8:
for k in 1, 2, . . . , m do
9:
Wj = Wj−1 −α∇Wj−1ℓi(fθ,Wj−1(Xi
j), Y i
j )
10:
j = j + 1
11:
end for
12:
Sample Si
test from p(Sk|Ti)
13:
θ = θ + ∇θℓi(fθ,Wj[Stest[0 : j, 0]], Si
test[0 : j, 1])
14:
Stop Gradients(fθ,Wj))
15:
end while
16: end while
C.1
Why Learn an Encoder Instead of an Initialization
We empirically found that learning an encoder results in signiﬁcantly better performance than learning
just an initialization as shown in Fig 9. Moreover, the meta-learning optimization problem is more
well-behaved when learning an encoder (Less sensitive to hyper-parameters and converges faster).
One explanation for this difference is that a global and greedy update algorithm – such as gradient
descent – will greedily change the weights of the initial layers of the neural network with respect
to current samples when learning on a highly correlated stream of data. Such changes in the initial
layers will interfere with the past knowledge of the model. As a consequence, an initialization is not
an effective inductive bias for incremental learning. When learning an encoder φθ, on the other hand,
it is possible for the neural network to learn highly sparse representations which make the update less
global (Since weights connecting to features that are zero remain unchanged).
15
