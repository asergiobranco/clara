# clara


# PCA Transpiler

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
