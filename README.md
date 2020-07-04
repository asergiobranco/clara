# clara


# PCA Transpiler

### Python Exporting

```
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

# Cite Us

`Sérgio Branco. (2020, July 4). asergiobranco/clara: PCA Transpiling (Version v0.0.1). Zenodo. http://doi.org/10.5281/zenodo.3930336`

```
@software{sergio_branco_2020_3930336,
  author       = {Sérgio Branco},
  title        = {asergiobranco/clara: PCA Transpiling},
  month        = jul,
  year         = 2020,
  publisher    = {Zenodo},
  version      = {v0.0.1},
  doi          = {10.5281/zenodo.3930336},
  url          = {https://doi.org/10.5281/zenodo.3930336}
}
```
