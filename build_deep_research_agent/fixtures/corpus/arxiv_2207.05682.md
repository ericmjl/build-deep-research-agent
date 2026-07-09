---
title: "Long Short-Term Memory to predict 3D Amino acids Positions in GPCR Molecular Dynamics"
authors: "Juan Manuel López-Correa, Caroline König, Alfredo Vellido"
year: 2022
source: arxiv
source_id: "2207.05682"
url: "http://arxiv.org/abs/2207.05682v1"
domain: computational-biology
---
June 2021
Long Short-Term Memory to predict 3D
Amino acids Positions in GPCR
Molecular Dynamics
Juan Manuel L ´OPEZ-CORREA a,1, Caroline K ¨ONIG a,b and Alfredo VELLIDO a,b
aComputer Science Dept., Univ. Polit`ecnica de Catalunya - UPC BarcelonaTech,
08034, Barcelona, Spain
bIntelligent Data Science and Artiﬁcial Intelligence (IDEAI-UPC) Research Center
Abstract. G-Protein Coupled Receptors (GPCRs) are a big family of eukaryotic
cell transmembrane proteins, responsible for numerous biological processes. From
a practical viewpoint around 34% of the drugs approved by the US Food and
Drug Administration target these receptors. They can be analyzed from their sim-
ulated molecular dynamics, including the prediction of their behavior in the pres-
ence of drugs. In this paper, the capability of Long Short-Term Memory Networks
(LSTMs) are evaluated to learn and predict the molecular dynamic trajectories of
a receptor. Several models were trained with the 3D position of the amino acids
of the receptor considering different transformations on the position of the amino
acid, such as their centers of mass, the geometric centers and the position of the
α–carbon for each amino acid. The error of the prediction of the position was eval-
uated by the mean average error (MAE) and root-mean-square deviation (RMSD).
The LSTM models show a robust performance, with results comparable to the state-
of-the-art in non-dynamic 3D predictions. The best MAE and RMSD values were
found for the mass center of the amino acids with 0.078 ˚A and 0.156 ˚A respec-
tively. This work shows the potential of LSTM to predict the molecular dynamics
of GPRCs.
Keywords. G-Protein Coupled Receptors, LSTM, Molecular Dynamics
1. Introduction
G-Protein Coupled Receptors (GPCRs) are a big family of eukaryotic cell transmem-
brane proteins. They are abundant cell surface receptors accounting for 4% (800) of all
human genes [1] and responsible for numerous biological processes. This is the result
of their ability to transmit extracellular signals, which makes them relevant for pharma-
cology and the research about drugs targeting these receptors. Around the 34 % of the
drugs approved by the US Food and Drug Administration [1]. This has led, over the last
decade, to active research in the ﬁeld of proteomics.
1Corresponding Author: Juan Manuel L ´OPEZ-CORREA, Univ. Polit`ecnica de Catalunya. Barcelona Tech,
08034, Barcelona, Spain juan.manuel.lopez.correa@upc.edu.
arXiv:2207.05682v1  [q-bio.BM]  2 Jun 2022

June 2021
The functionality of a protein depends widely on its 3-D structure, which determines
its ability for certain ligand binding. However, the 3-D structure of human GPCRs is not
fully determined yet [2]. As an alternative, when the information about the 3-D struc-
ture is not available, the investigation of the functionality of a protein can be achieved
through the analysis of its amino acid sequence, which is known and available in several
public curated databases[3]. Computing biotechnology, X-ray crystallography and cryo-
electron microscopy over the last year has evolved exponentially, yielding 3-D models of
many proteins. Such structures are publicly available at repositories, such as at the Pro-
tein Data Bank (PDB) [4], but provide only a static view of the receptor’s state. Molecu-
lar dynamics (MD) simulations are an interesting technology to explore dynamically the
conformational landscape of receptors under the presence of different drugs. MD sim-
ulations take the 3D models as starting point for the computer assisted simulation and
explore the molecular dynamics at the simulated environment [5]. Speciﬁc repositories
of simulated MDs are available, such as the GPCRMD for MD simulations of GPCRs
[6].
For the study of the temporal evolution of molecular dynamics with machine learn-
ing (ML) techniques, Recurrent Neural Networks (RNN) are used due to their capabil-
ity for modeling temporal sequences. RNNs have shown success at applications such
as human language modeling [7]. In recent years, a particular RNN, Long Short-Term
Memory (LSTM)[8], has been successfully applied to machine translation[9][10], speech
recognition [11], sequence learning [12] and weather forecasting [13]. LSTMs solve a
limitations of the RNN architecture, the inability to learn information originated from
far past in time. LSTMs overcome that limitation by their ability to accumulate infor-
mation for a long period of time and allowing the network to dynamically learn to for-
get old aspects of information. Recently, LSTMs have been used to mimic trajectories
produced by simulations[14], achieving accurate predictions about a short time into the
future. LSTM and their variants have shown great potential in sequence processing [15],
and there are several studies where they were applied for the analysis of trajectories from
simulation systems [16,17,18]. Some authors, incorporate LSTM into the numerical inte-
grator that solves Newton’s equations in molecular dynamics simulations [19]. Another
applies LSTM directly onto the low dimensional molecular trajectories and predicts the
rare events in the sequential data [18,20]. However, none of them have reported robust
results to predict the amino acid’s position in the molecular dynamics of GPRCs.
In this work, the capability of LSTMs are evaluated to learn and predict the 3D po-
sitions of the amino acids of a GPCR receptor in molecular dynamic simulations. In a
ﬁrst experiment, the prediction of two types of LSTMs are compared, the unidirectional
and bidirectional variant of LSTMs. In the second experiment, different representations
of the amino acid position and several variables of the LSTM are analyzed to ﬁnd the
combination of the parameters, which best predict the molecular trajectory. The experi-
ments are carried out on a public available dataset of the molecular dynamic simulations
of the β2AR-rh1 GPCR receptor [21].
The remaining part of the articles is structured as follows. In section Materials the
dataset under study is explained. Methods section describe the ML model, data prepro-
cessing and the experimental setup. The Result section evaluates the quality of predic-
tion of the models per experiment. Finally in the Discussion and Conclusion section the
results and impact of the study are discussed.

June 2021
2. Materials
2.1. MD simulations
In this work a dataset of the MD simulations of the β2AR-rh1 GPCR receptor is ana-
lyzed. The β2-adrenergic receptor (β2AR) is implicated in type-2 diabetes, obesity, and
asthma, and is a member of the class A, rhodopsin-like GPCRs (rh1) [22]. This simu-
lations have been created by [21] at the Google’s Exacycle cloud computing platform.
The simulations under study in this work comprise 10.000 trajectories of the β2AR-rh1
GPCR receptor with a full agonist. Each trajectory describes the 3D position of the re-
ceptor during 28 consecutive timesteps, which are referred to as frames in this study. The
time elapsed between each frame are 500 picoseconds. The receptor has 282 amino acids
for which the position is predicted during the different frames of the simulation in this
work.
3. Methods
3.1. Long Short-Term Memory (LSTM)
A speciﬁc and extremely popular instance of RNNs are LSTM [8] neural networks,
which show more ﬂexibility and can be used for challenging tasks such as language mod-
eling, machine translation, and weather forecasting [23,24,10]. In this paper, unidirec-
tional LSTM (ULSTM) and bidirectional LSTM (BLSTM) are used to predict the trajec-
tories of the MD simulations. ULSTMs work by processing data in the forward direction,
while BLSTMs processes sequence data in both forward and backward directions with
two separate hidden layers [25]. The bidirectional networks are often reported to yield
better prediction results than unidirectional ones, such as at phoneme classiﬁcation [26]
or speech recognition [27], to number a few. Bidirectional LSTMs have not been used
yet in molecular dynamic predictions of the GPCRs problem, based on a review of the
literature [28,25,29,30,31] .
3.2. Data Preprocessing
Data normalisation: The models are trained with normalized data. This process
is done by applying a linear max–min normalization [32,33]. The normalized data pre-
dicted by the model can by transformed back to the original range of values to asses the
quality of prediction in Angstrom ( ˚A) units.
Center of the amino acids: Each simulation is made up of 28 frames (step positions)
and 282 amino acids. However, the original information of the MD simulation provides
the position of the atoms, not of the amino acids. For this reason, three representations
for the 3D amino acid position are calculated: a) Geometric Center (CG), b) Center of
Mass (CM) and c) α–carbon (αC) conforming three derived datasets with the 3D posi-
tions (xyz) for each amino acid in each step (frame) of the simulated molecular trajectory.

June 2021
3.3. Experimental Setup
In the following the variables and parameters used for the conﬁguration of the experi-
ments are explained:
nClones: As explained in the Materials section, the original dataset comprises
10.000 simulated trajectories of the β2AR-rh1 receptor. Each of these trajectories is
named a nClones in this work. Each trajectory is simulated under the presence of a full
agonist.
nSteps-in : The training of the LSTM models is carried out with the information of
short sequences of the 3D positions of the amino acids. The lengths of these sequences
is named nSteps-in in this work. In one step each amino acid has three position values
(x,y,z). In the experiments the models are trained with different values for the parameter
nSteps-in.
nSteps-out: After the training of the LSTM models with different nSteps-in, the
model can predict a sequence of next steps for the trajectory. The number of predicted
steps is referred to as the parameter nSteps-out.
Model optimisation: Of the 10.000 nClones available at the original dataset, 1.000
were taken for model creation. This dataset was split in 5 folds with 200 nClones per
fold. Four folds were used for training, conforming the train set and the remaining fold
was used only for the evaluation of the quality of prediction of the model, conforming
the test set. The model creation was carried out following a cross validation approach
[9]. This means, the training was repeated 4 time per experiment. For each training rep-
etition 3 folds of 4 train set folds were selected to train the model and the remaining
fold (validation set) was use to test the predictions through Mean Average Error (MAE)
[34]. This process was repeated for each fold of the train set. In this way, all the folds
of the train set were tested without mixing the training and validation data. The training
process generates 4 trained models and 4 testing results. The best model was chosen by
the lowest MAE value. The best model was used to evaluate the predictive ability against
new data never seen by the model,in this work the test set.
Outline of experiments: The ﬁrst and second experiment were performed by two
types of LSTMs - ULSTM and BLSTM. The ﬁrst experiment was carried out comparing
the predictions of the LSTM on the CG, CM, αC transformed dataset. The experiments
aims to ﬁnd out which representation of the amino acid center is best to predict the
molecular dynamic sequences of the GPCR.
When a position sequence is shown to the LSTM, it needs to know the previous
amino acid positions to predict the next positions. For this reason, the next experiment
investigates if the parameter nSteps-in has an impact on the quality of prediction. Values
in the range of three, ﬁve and seven for the parameter nSteps-in per center of the amino
acid were evaluated.
Finally, the third experiment was developed to know the capability of the ULSTM
to predict different length of the sequence. For this experiments the predictions of 12
nSteps-out were evaluated.
The results in the following section are reported using two metrics calculated on the
original range of values in Angstrom ( ˚A) unit:
1. Mean absolute error (MAE) [34] for each predicted value of the x,y and z position.
2. Root-mean-square deviation of amino acid positions (RMDS)[35] for each pre-
dicted value of x,y and z position.

June 2021
4. Results
In this section the results of the experiments with LSTMs for the prediction of the se-
quences of the trajectories of the receptor are described. The ULSTM and BLSTM were
trained to predict multivariate time series data on sample trajectories. Table 1 and Table
2 show the MAE (mean of the position ”x”, ”y” and ”z” for the amino acids) , MAEx
(mean of the position ”x”), MAEy (mean of the position ”y”), MAEz (mean of the po-
sition ”z”) and RMSD by ULSTM and BLSTM respectively. In addition, in both tables
the standard deviation [36] (std) for MAE and RMSD is indicated. In this experiment,
to simplify the analysis the nStep-out was set to a value of 1. About the nStep-in, the
results show the mean value from experiments carried out with the values 3,5,7 for the
parameter nSteps-in.
Table 1. MAE predictions of the amino acid position by Geometric center, Mass center, α-carbon by ULSTM
Amino acid center
MAE
MAEx
MAEy
MAEz
RMSD
Geometric
0.0850 ± 0.024
0.0793
0.0864
0.0894
0.1703 ± 0.040
Mass
0.0781 ± 0.016
0.0728
0.0793
0.0822
0.1561 ± 0.027
α–carbon
0.0792 ± 0.0219
0.0739
0.0809
0.0838
0.15934 ± 0.034
Table 2. MAE predictions of the amino acid position by Geometric center, Mass center, α-carbon by BLSTM
Amino acid center
MAE
MAEx
MAEy
MAEz
RMSD
Geometric
0.0835 ± 0.024
0.0775
0.0845
0.0883
0.1673 ± 0.040
Mass
0.0806 ± 0.021
0.0753
0.0821
0.0844
0.1615 ± 0.025
α-carbon
0.0829 ± 0.023
0.0773
0.0842
0.0871
0.1661 ± 0.039
Figure 1 represents the results for the second experiment considering the center of
the mass variable as amino acid representation. The MAE of the sequence prediction are
shown considering the nSteps-out = 1 for ULSTM (rhombuses bar) and BLSTM (full
gray bar) with three sequences lengths as nSteps-in = 3, 5, 7 values.

June 2021
Figure 1. Mean Average Error(MAE) of the sequence prediction by ULSTM (full gray bar) and BLSTM
(rhombuses bar) for three sequences lengths asnSteps-in = 3, 5, 7 values. MAE in ˚A units
The objective of the third experiment is the evaluation of the forecasting capabil-
ity of a ULSTM to predict long sequences. The MAE and RMSD behavior for the 12
nSteps-out predictions is represented in the Table 3. In this experiment the parameters,
which have yielded the best results in the previous experiments were used, i.e. center
of mass representation, nStepsIn of 5 and a ULSTM. In this case, the MAE predictions
is discriminated in 3D coordinates (MAEx, MAEy, MAEz). As well also, the standard
deviation (st)) for mean 3D position MAE and RMSD is shown.
Table 3. Error prediction by MAE and RMSD for 12 length sequences ( nSteps-out ) with ULSTM.
step
MAE
MAEx
MAEy
MAEz
RMSD
1
0.0769 ± 0.0220
0.0713
0.0780
0.0814
0.1535 ± 0.0379
2
0.0814 ± 0.0224
0.0761
0.0823
0.0858
0.1626 ± 0.0381
3
0.0837 ± 0.0229
0.0784
0.0847
0.0880
0.1674 ± 0.0383
4
0.0842 ± 0.0231
0.0788
0.0855
0.0883
0.1684 ± 0.0388
5
0.0852 ± 0.0234
0.0797
0.0867
0.0892
0.1706 ± 0.0392
6
0.0854 ± 0.0234
0.0798
0.0869
0.0895
0.1712 ± 0.0390
7
0.0857 ± 0.0233
0.0797
0.0870
0.0903
0.1714 ± 0.0391
8
0.0862 ± 0.0236
0.0804
0.0870
0.0912
0.1725 ± 0.0396
9
0.0865 ± 0.0241
0.0810
0.0868
0.0919
0.1735 ± 0.0404
10
0.0864 ± 0.0241
0.0802
0.0869
0.0920
0.1730 ± 0.0412
11
0.08601 ± 0.02433
0.0793
0.0870
0.0916
0.1719 ± 0.0425
12
0.0861 ± 0.0246
0.0794
0.0872
0.0916
0.1722 ± 0.0433

June 2021
5. Discussion
The ﬁrst experiment focusing on the different transformations of the amino acid posi-
tions has shown that center of mass is the transformation that best predicts the molec-
ular dynamics sequences of the GPRC yielding minimum MAE and std values for UL-
STM and BLSTM (bold numbers in Table 1 and Table 2). However, the geometric center
and α-carbon center, also, get quite good prediction results comparable with anothers
works that work only with Static Molecular Structures [37,38]. The second experiment
seeks to discover the best sequence length as nSteps-in. For both the ULSTM and the
BLSTM the minimum MAE was obtained for the value of 5 for the input steps. This
means 5 steps as the best length for the input information of the sequence for the model
to best predict future trajectories. Regarding the capabilities of ULSTMs and BLSTMs,
the ULSTM demonstrate a better performance in all experiments.Finally, the results of
the third experiment reveal the increment of the error with the length of predicted se-
quence. With larger nSteps-out values, both the MAE and RMSD metric increase. In ad-
dition, the MAE in the plane ”x” shows greater ability to predict more steps compared to
the ”y” and ”z” plane. As well also, the plane z show the biggest error analysing the 3D
coordinates.
6. Conclusions
GPCRs are family of receptors with great interest in pharmacology and molecular dy-
namics are a powerful tool to discover the conformational space and the behavior of the
receptors. Due the large amount and complexity of data in MD simulations, machine
learning approaches are a promising approach to discover relevant knowledge. This study
has used a speciﬁc machine learning approach, namely LSTMs to study the ability to pre-
dict the movements of a receptor. This prediction is not trivial as the receptor comprises
282 amino acid, which yield a dataset of 846 data points. Furthermore, these datasets are
in the context of a temporal sequence and methods taking into account the temporal evo-
lution are needed. This study has demonstrated the potential of LSTMs to predict accu-
rately molecular dynamics sequences of a GPRC receptor, speciﬁcally for β2AR-rh1. In
addition, the study has provided insights about which are the best parameters regarding
the representation of amino acid positions, the lengths of the input sequence and length
of the predicted sequence. In particular, the center of the mass is the best representation
of the 3D amino acid position for a complex receptor yielding the best results at the
forecasting. Furthermore, the study has shown that the best length of input information
are 5 steps. The prediction performance of ULSTM show slightly better results com-
paring with BLSTM, although both models achieved accurate results. Finally, the study
also conﬁrmed that the capability to predict long sequences decreases with the lengths
of the forecasted sequence. These results are important for the conﬁguration of other ex-
periments on the analysis of MD data. As a future line of research the use of generative
models is planned in order to artiﬁcially generate MD trajectories.

June 2021
Acknowledgments
This work is funded by Spanish PID2019-104551RB-I00 research project and by the
PhD. training program (PRE2020-092428) through the Ministry Science and Innovation
of Spain.
References
[1]
Ismael Rodr´ıguez-Espigares, Mariona Torrens-Fontanals, Johanna KS Tiemann, David Aranda-Garc´ıa,
Juan Manuel Ram´ırez-Anguita, Tomasz Maciej Stepniewski, Nathalie Worp, Alejandro Varela-Rial,
Adri´an Morales-Pastor, Brian Medel-Lacruz, et al. Gpcrmd uncovers the dynamics of the 3d-gpcrome.
Nature Methods, 17(8):777–787, 2020.
[2]
Vsevolod Katritch, Vadim Cherezov, and Raymond C Stevens. Structure-function of the g protein–
coupled receptor superfamily. Annual review of pharmacology and toxicology, 53:531–556, 2013.
[3]
Caroline K¨onig, Ra´ul Cruz-Barbosa, Ren´e Alqu´ezar, and Alfredo Vellido. Svm-based classiﬁcation of
class c gpcrs from alignment-free physicochemical transformations of their sequences. In International
Conference on Image Analysis and Processing, pages 336–343. Springer, 2013.
[4]
Helen M Berman. The protein data bank: a historical perspective. Acta Crystallographica Section A,
64(1):88–95, 2008.
[5]
Naomi R Latorraca, AJ Venkatakrishnan, and Ron O Dror. Gpcr dynamics: structures in motion. Chem-
ical reviews, 117(1):139–155, 2017.
[6]
Ismael Rodr´ıguez-Espigares, Mariona Torrens-Fontanals, Johanna KS Tiemann, David Aranda-Garc´ıa,
Juan Manuel Ram´ırez-Anguita, Tomasz Maciej Stepniewski, Nathalie Worp, Alejandro Varela-Rial,
Adri´an Morales-Pastor, Brian Medel-Lacruz, et al. Gpcrmd uncovers the dynamics of the 3d-gpcrome.
Nature Methods, 17(8):777–787, 2020.
[7]
R Rico-Martines, IG Kevrekidis, MC Kube, and JL Hudson. Discrete-vs. continuous-time nonlinear
signal processing: Attractors, transitions and parallel implementation issues. In 1993 American Control
Conference, pages 1475–1479. IEEE, 1993.
[8]
Sepp Hochreiter and J¨urgen Schmidhuber. Long short-term memory. Neural computation, 9(8):1735–
1780, 1997.
[9]
Payam Refaeilzadeh, Lei Tang, and Huan Liu. Cross-validation. Encyclopedia of database systems,
5:532–538, 2009.
[10]
Kyunghyun Cho, Bart Van Merri¨enboer, Caglar Gulcehre, Dzmitry Bahdanau, Fethi Bougares, Holger
Schwenk, and Yoshua Bengio. Learning phrase representations using rnn encoder-decoder for statistical
machine translation. arXiv preprint arXiv:1406.1078, 2014.
[11]
Alex Graves, Abdel-rahman Mohamed, and Geoffrey Hinton. Speech recognition with deep recurrent
neural networks. In 2013 IEEE international conference on acoustics, speech and signal processing,
pages 6645–6649. Ieee, 2013.
[12]
Ilya Sutskever, Oriol Vinyals, and Quoc V Le. Sequence to sequence learning with neural networks.
Advances in neural information processing systems, 27, 2014.
[13]
Xingjian Shi, Zhourong Chen, Hao Wang, Dit-Yan Yeung, Wai-Kin Wong, and Wang-chun Woo. Con-
volutional lstm network: A machine learning approach for precipitation nowcasting. Advances in neural
information processing systems, 28, 2015.
[14]
Mohammad Javad Eslamibidgoli, Mehrdad Mokhtari, and Michael H Eikerling.
Recurrent neu-
ral network-based model for accelerated trajectory analysis in aimd simulations.
arXiv preprint
arXiv:1909.10124, 2019.
[15]
Mantas Lukoˇseviˇcius and Herbert Jaeger. Reservoir computing approaches to recurrent neural network
training. Computer Science Review, 3(3):127–149, 2009.
[16]
Mohammad Javad Eslamibidgoli, Mehrdad Mokhtari, and Michael H Eikerling.
Recurrent neu-
ral network-based model for accelerated trajectory analysis in aimd simulations.
arXiv preprint
arXiv:1909.10124, 2019.
[17]
Jaideep Pathak, Brian Hunt, Michelle Girvan, Zhixin Lu, and Edward Ott. Model-free prediction of
large spatiotemporally chaotic systems from data: A reservoir computing approach. Physical review
letters, 120(2):024102, 2018.

June 2021
[18]
Sun-Ting Tsai, En-Jui Kuo, and Pratyush Tiwary. Learning molecular dynamics with simple language
model built upon long short-term memory neural network. Nature communications, 11(1):1–11, 2020.
[19]
JCS Kadupitiya, Geoffrey C Fox, and Vikram Jadhao.
Deep learning based integrators for solving
newton’s equations with large timesteps. arXiv preprint arXiv:2004.06493, 2020.
[20]
Wenqi Zeng, Siqin Cao, Xuhui Huang, and Yuan Yao. A note on learning rare events in molecular
dynamics using lstm and transformer. arXiv preprint arXiv:2107.06573, 2021.
[21]
Joseph L Hellerstein, Kai J Kohlhoff, and David E Konerding. Science in the cloud: accelerating dis-
covery in the 21st century. IEEE Internet Computing, 16(4):64–68, 2012.
[22]
Kai J Kohlhoff, Diwakar Shukla, Morgan Lawrenz, Gregory R Bowman, David E Konerding, Dan Belov,
Russ B Altman, and Vijay S Pande. Cloud-based simulations on google exacycle reveal ligand modula-
tion of gpcr activation pathways. Nature chemistry, 6(1):15–21, 2014.
[23]
Xingjian Shi, Zhourong Chen, Hao Wang, Dit-Yan Yeung, Wai-Kin Wong, and Wang-chun Woo. Con-
volutional lstm network: A machine learning approach for precipitation nowcasting. Advances in neural
information processing systems, 28, 2015.
[24]
Martin Sundermeyer, Ralf Schl¨uter, and Hermann Ney. Lstm neural networks for language modeling.
In Thirteenth annual conference of the international speech communication association, 2012.
[25]
Zhiyong Cui, Ruimin Ke, Ziyuan Pu, and Yinhai Wang. Deep bidirectional and unidirectional lstm
recurrent neural network for network-wide trafﬁc speed prediction. arXiv preprint arXiv:1801.02143,
2018.
[26]
Alex Graves and J¨urgen Schmidhuber. Framewise phoneme classiﬁcation with bidirectional lstm and
other neural network architectures. Neural networks, 18(5-6):602–610, 2005.
[27]
Alex Graves, Navdeep Jaitly, and Abdel-rahman Mohamed. Hybrid speech recognition with deep bidi-
rectional lstm. In 2013 IEEE workshop on automatic speech recognition and understanding, pages
273–278. IEEE, 2013.
[28]
Cheng Wang, Haojin Yang, Christian Bartz, and Christoph Meinel. Image captioning with deep bidirec-
tional lstms. In Proceedings of the 24th ACM international conference on Multimedia, pages 988–997,
2016.
[29]
Reza Paki, Esmaeil Nourani, and Davoud Farajzadeh. Classiﬁcation of g protein-coupled receptors using
attention mechanism. Gene Reports, 21:100882, 2020.
[30]
Xueliang Liu. Deep recurrent neural network for protein function prediction from sequence. arXiv
preprint arXiv:1701.08318, 2017.
[31]
Xueliang Liu. Deep recurrent neural network for protein function prediction from sequence. arXiv
preprint arXiv:1701.08318, 2017.
[32]
Ali Jahan and Kevin L Edwards. A state-of-the-art survey on the inﬂuence of normalization techniques
in ranking: Improving the materials selection process in engineering design. Materials & Design (1980-
2015), 65:335–342, 2015.
[33]
MJ Asgharpour. Multiple criteria decision making. Tehran: Tehran University, 1998.
[34]
Tianfeng Chai and Roland R Draxler. Root mean square error (rmse) or mean absolute error (mae).
Geoscientiﬁc Model Development Discussions, 7(1):1525–1534, 2014.
[35]
Karen Sargsyan, C´edric Grauffel, and Carmay Lim. How molecular size impacts rmsd applications in
molecular dynamics simulations. Journal of chemical theory and computation, 13(4):1518–1524, 2017.
[36]
Dong Kyu Lee, Junyong In, and Sangseok Lee. Standard deviation and standard error of the mean.
Korean journal of anesthesiology, 68(3):220, 2015.
[37]
Vitali Nesterov, Mario Wieser, and Volker Roth. 3dmolnet: a generative network for molecular struc-
tures. arXiv preprint arXiv:2010.06477, 2020.
[38]
Michael A Hanson and Raymond C Stevens. Discovery of new gpcr biology: one receptor structure at a
time. Structure, 17(1):8–14, 2009.
