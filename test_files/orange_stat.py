# Description: Demostrates the use of classification scores, orange data mining
# Author: Rick Giuly


import orange, orngTest, orngTree, orngEnsemble

minimumExamples = 10

tree = orngTree.TreeLearner(storeNodeClassifier = 0,
                            storeContingencies=0,
                            storeDistributions=1,
                            minExamples=minimumExamples, ).instance()
gini = orange.MeasureAttribute_gini()
tree.split.discreteSplitConstructor.measure = \
 tree.split.continuousSplitConstructor.measure = gini
tree.split = orngEnsemble.SplitConstructor_AttributeSubset(tree.split, 3)

#forest = orngEnsemble.RandomForestLearner(data, trees=50,
#                                          name="forest", learner=tree)

learners = [orngEnsemble.RandomForestLearner(name="random_forest", trees=10, learner=tree),
            orngEnsemble.RandomForestLearner(name="random_forest", trees=10, learner=tree)]

voting = orange.ExampleTable("voting3")
res = orngTest.crossValidation(learners, voting)


import orngStat

for cutoffInteger in range(0, 10, 1):

    cutoff = float(cutoffInteger) * 0.1

    cm = orngStat.confusionMatrices(res, cutoff=cutoff)[0]
    #print type(orngStat.confusionMatrices(res, cutoff=cutoff))
    #print cm
    #print type(cm)
    #print type(cm[0])
    print "cutoff %f:" % cutoff
    print "TP: %i, FP: %i" % (cm.TP, cm.FP)


