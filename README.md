# Clara

CLARA is a tool designed to help Machine Learning developers to build their models using High-Level languages (Python), but easily implement them in C. The goal is not to convert the code, but to convert the trained model itself (the object). Therefore, this is not a code converter, but a **code transpiler**.

The following algorithms are available

+ __Classification__
  - MLP
  - Decision Tree
  - Support-Vector Machines (SVC & Nu)
  - LinearSVM
  - Gaussian Naive Bayes
  - Complement Naive Bayes
  - Multinomial Naive Bayes
  - Categorical Naive Bayes
  - Bernoulli Naive Bayes
+ __Regression__
  - MLP
  - Support-Vector Machines
+ __Decomposition__
  - PCA
+ __Preprocessing__
  - StandardScaler
  - KernelCenterer
  - MaxAbsScaler
  - MinMaxScaler
  - RobustScaler


## Transpiling Tools

| Python Class | Clara Class |
|:------------:|:-----------------:|
| *Decomposition* |
| [sklearn.decomposition.PCA](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html) | clara.transpiler.pca.PCATranspiler |
| *Neural Networks* ||
| [sklearn.neural_network.MLPClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html) | clara.transpiler.mlp.MLPCTranspiler|
| [sklearn.neural_network.MLPRegressor](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPRegressor.html) | clara.transpiler.mlp.MLPRTranspiler|
| *Decision Tree* ||
| [sklearn.tree.DecisionTreeClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html) | clara.transpiler.tree.DecisionTreeClassifierTranspiler|
| *Support-Vector Machines* ||
| [sklearn.svm.SVC](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html) | clara.transpiler.svm.SVCTranspiler|
| [sklearn.svm.NuSVC](https://scikit-learn.org/stable/modules/generated/sklearn.svm.NuSVC.html) | clara.transpiler.svm.SVCTranspiler|
| [sklearn.svm.LinearSVM](https://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVM.html) | clara.transpiler.svm.LinearSVMTranspiler |
| [sklearn.svm.SVR](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVR.html) | clara.transpiler.svm.SVRTranspiler |
| *Naive Bayes* ||
| [sklearn.naive_bayes.GaussianNB ](https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.GaussianNB.html) | clara.transpiler.naive_bayes.GaussianNBTranspiler |
| [sklearn.naive_bayes.ComplementNB ](https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.ComplementNB.html) | clara.transpiler.naive_bayes.ComplementNBTranspiler |
| [sklearn.naive_bayes.MultinomialNB](https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.MultinomialNB.html) | clara.transpiler.naive_bayes.MultinomialNBTranspiler |
| [sklearn.naive_bayes.CategoricalNB](https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.CategoricalNB.html) | clara.transpiler.naive_bayes.CategoricalNBTranspiler |
| [sklearn.naive_bayes.BernoulliNB](https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.BernoulliNB.html) | clara.transpiler.naive_bayes.BernoulliNBTranspiler |
| *Preprocessing* |
| [sklearn.preprocessing.StandardScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html) | clara.transpiler.preprocessing.StandardScalerTranspiler |


## Syntax

Besides the multiple available algorithms, the syntax to use in any of them is the same and shown in the snippet bellow.


```python

#The ML Algorithm you want to use
model = ScikitLearnClass()

# TRAIN YOUR MODEL FIRST!!!
model.fit()

# The correspondent CLARA TRanspiler Class
transpiler = ClaraClassTranspiler(model) #The correspondent Clara Class


# The C code to be exported to a .c file and compiled
# The code is of the model trained, therefore no retraining is needed.
c_code = transpiler.generate_code()


```

# PCA Transpiler

### Python Exporting

```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_wine

data = load_wine()
dataset = np.column_stack((data.data, data.target))
scale = StandardScaler()

pca = PCA(n_components=0.8)

X = scale.fit_transform(dataset[::,:-1])
pca.fit(X)

from clara.transpiler.pca import PCATranspiler

transpiler = PCATranspiler(pca)

code = transpiler.generate_code()

with open("pca.c", "w+") as fp:
  fp.write(code)

```

# Test code in C

The results may vary, but if they should be the same!!

```c
int main(int argc, const char * argv[]) {
    // insert code here...
    double sample[N_FEATURES] = { 1.51861254, -0.5622498 ,  0.23205254, -1.16959318,  1.91390522,
        0.80899739,  1.03481896, -0.65956311,  1.22488398,  0.25171685,
                                  0.36217728,  1.84791957,  1.01300893};
    double scores[N_COMPONENTS] = {0};

    double inverse_sample[N_FEATURES] = {0};

    calculate_scores(sample, scores);

    printf("\nScores\n");


    for(int i = 0; i < N_COMPONENTS; i++){
        printf("%f\t", scores[i]);
    }

    printf("\n\nInverse Transform\n");

    inverse(scores, inverse_sample);

    for(int i = 0; i < N_FEATURES; i++){
        printf("%f\t", inverse_sample[i]);
    }

    printf("\n\n");

    pca_dimensions_t val;

    val = calculate_dimensions(sample);

    printf("T2 = %f, Q-Residuals: %f\n\n", val.hoteling2, val.q_residuals);



}
```

# MLP Transpiler

Multi-Layer Perceptron are the basis of Neural Networks and Deep Learning. Our tools provides a way to transpile MLPs for regression and classification problems.
* **Note:** At the current time, binary classifications are not working... Sorry*

## MLPClassifier

```python
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import load_wine
import numpy as np

from clara.transpiler.mlp import MLPCTranspiler

data = load_wine()
dataset = np.column_stack((data.data, data.target))

mlp = MLPClassifier(hidden_layer_sizes=(30, 10))

mlp.fit(ddataset.data, dataset.target)


transpiler = MLPCTranspiler(mlp)

code = transpiler.generate_code()

with open("mlp.c", "w+") as fp:
  fp.write(code)

```

## MLPRegressor

```python
from sklearn.neural_network import MLPRegressor
from sklearn.datasets import load_boston
import numpy as np

from clara.transpiler.mlp import MLPRTranspiler

data = load_boston()
dataset = np.column_stack((data.data, data.target))

mlp = MLPClassifier(hidden_layer_sizes=(30, 10))

mlp.fit(dataset.data, dataset.target)



transpiler = MLPRTranspiler(mlp)

code = transpiler.generate_code()

with open("mlp.c", "w+") as fp:
  fp.write(code)

```

# Test code in C


```c
int main(){
    double s[N_FEATURES] = {14.23, 1.71, 2.43, 15.6, 127.0, 2.8, 3.06, 0.28, 2.29, 5.64, 1.04, 3.92, 1065.0};
    int class;
    for(int i = 0; i<N_FEATURES; i++){
      sample[i] = s[i];
    }
    class = predict(sample);
    return 0;
}

```

# Cite Us

Please, if you use our tool in any of your projects, cite us. This will help us improve and look at what people may need! Thanks!

DOI: [10.5281/zenodo.3930335](https://doi.org/10.5281/zenodo.3930335)

`Sérgio Branco. (2020, July 4). CLARA - Embedded ML Tools (Version v0.0.1). Zenodo. http://doi.org/10.5281/zenodo.3930336`

```
@software{sergio_branco_2020_3930336,
  author       = {Sérgio Branco},
  title        = {CLARA - Embedded ML Tools},
  month        = jul,
  year         = 2020,
  publisher    = {Zenodo},
  version      = {v0.0.1},
  doi          = {10.5281/zenodo.3930336},
  url          = {https://doi.org/10.5281/zenodo.3930336}
}
```
