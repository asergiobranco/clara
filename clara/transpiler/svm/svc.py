import numpy as np
class SVCTranspiler(object):

    def __init__(self, model):
        self.model = model

        self.n_sv = len(self.model.support_vectors_)
        self.n_features = len(self.model.support_vectors_[0])
        self.n_classes = len(self.model.classes_)

        self.gamma = str(self.model._gamma)
        self.coef = str(self.model.coef0)
        self.degree = str(self.model.degree)
        self.kernel_type = self.model.kernel.upper()

        self.build_support_vectors()
        self.build_intercepts()
        self.build_coefs()
        self.build_dual_coefs()
        self.build_ranges()

    def build_intercepts(self):
        self.intercepts = ','.join(self.model.intercept_.astype(str))

    def build_support_vectors(self):
        matrix =[]
        for sv in self.model.support_vectors_:
            matrix.append("{%s}" % ','.join(sv.astype(str)))

        self.sv = ',\n'.join(matrix)

    def build_dual_coefs(self):
        matrix =[]
        for sv in self.model.dual_coef_:
            matrix.append("{%s}" % ','.join(sv.astype(str)))

        self.dual_coefs = ',\n'.join(matrix)

    def build_coefs(self):
        from itertools import combinations
        self.cls_combinations = np.asarray(list(combinations([np.asarray(x) for x in range(len(self.model.classes_))], 2)))

        matrix =[]
        for sv in self.cls_combinations:
            matrix.append("{%s}" % ','.join(sv.astype(str)))

        self.cls_combinations = ','.join(matrix)

        matrix=[]
        if self.model.kernel == "linear":
            for sv in self.model.coef_:
                matrix.append("{%s}" % ','.join(sv.astype(str)))

        self.coefs = ',\n'.join(matrix)

    def build_ranges(self):
        m = [0]
        for s in self.model.n_support_:
            m.append(m[-1] + s)

        self.ranges = ','.join(map(lambda x: str(x), m))

    def generate_code(self):
        return """
        /*
        The following code was generated using Clara.Transpiler. For more information please visit: https://github.com/asergiobranco/clara
        */
        #include <stdio.h>
        #include <math.h>

        #define N_SUPPORT_VECTORS %d
        #define N_FEATURES %d
        #define N_CLASSES %d
        #define N_INTERCEPTS (N_CLASSES*(N_CLASSES-1))/2
        #define %s

        #ifndef LINEAR
            #define GAMMA %s
            #define COEF %s
            double support_vectors[N_SUPPORT_VECTORS][N_FEATURES] = {%s};
            double coefs[N_CLASSES-1][N_SUPPORT_VECTORS] = {%s};
            unsigned int ranges[N_CLASSES+1] ={%s};
        #endif

        #ifdef LINEAR
            double support_vectors[N_INTERCEPTS][N_FEATURES] = {%s};
            unsigned int cls_combinations[N_INTERCEPTS][2] = {%s};
        #endif



        double intercepts[N_INTERCEPTS] = {%s};



        #ifndef RBF
        double * linear_kernel(double * sample, double * kernels){
            int i = 0, j=0;

            for(i=0; i<N_SUPPORT_VECTORS; i++){
                kernels[i] = 0;
                for(j=0; j<N_FEATURES; j++){
                    kernels[i] += support_vectors[i][j] * sample[j];
                }
            }

            return kernels;
        }
        #else
        double * rbf_kernel(double * sample, double * kernels){
            int i = 0, j=0;
            for(i=0; i<N_SUPPORT_VECTORS; i++){
                kernels[i] = 0;
                for(j=0; j<N_FEATURES; j++){
                    kernels[i] += (support_vectors[i][j]*support_vectors[i][j] - (2*support_vectors[i][j]*sample[j]) + sample[j]*sample[j]);
                    //kernels[i] += pow(support_vectors[i][j] - sample[j], 2);
                }
                kernels[i] = exp(-1* GAMMA * kernels[i]);
            }

            return kernels;
        }
        #define KERNEL(...) rbf_kernel(__VA_ARGS__)
        #endif

        #ifdef POLY
        #define DEGREE %s
        double * polynomial_kernel(double * sample, double * kernels){
            linear_kernel(sample, kernels);

            for(int i=0; i<N_SUPPORT_VECTORS; i++){
                kernels[i] = (GAMMA * kernels[i] + COEF);
                kernels[i] = pow(kernels[i], DEGREE);
            }

            return kernels;

        }
        #define KERNEL(...) polynomial_kernel(__VA_ARGS__)
        #endif

        #ifdef SIGMOID
        double * sigmoid_kernel(double * sample, double * kernels){
            linear_kernel(sample, kernels);

            for(int i=0; i<N_SUPPORT_VECTORS; i++){
                kernels[i] = (GAMMA * kernels[i] + COEF);
                kernels[i] = tanh(kernels[i]);
            }

            return kernels;

        }
        #define KERNEL(...) sigmoid_kernel(__VA_ARGS__)
        #endif

        #ifdef LINEAR


        int predict(double * sample){
            unsigned int amounts[N_CLASSES] = {0};
            unsigned int i, j, class = 0;
            double decision_rule;
            for(i = 0; i < N_INTERCEPTS; i++){

                decision_rule = 0;

                for(j = 0; j < N_FEATURES; j++){
                    decision_rule += support_vectors[i][j]*sample[j];
                }

                #if N_CLASSES==2
                    if(decision_rule + intercepts[i] < 0){
                        amounts[cls_combinations[i][0]]++;
                    }
                    else{
                        amounts[cls_combinations[i][1]]++;
                    }
                #else
                    if(decision_rule + intercepts[d_rule] > 0){
                        amounts[cls_combinations[i][0]]++;
                    }
                    else{
                        amounts[cls_combinations[i][1]]++;
                    }
                #endif
            }

            for(i=0; i<N_CLASSES; i++){
                class = (amounts[i] > amounts[class]) ? i : class;
            }


            return class;
        }
        #else
        int predict(double * sample){
            double decision_rule = 0.0;
            unsigned int amounts[N_CLASSES] = {0}, d_rule = 0, class = 0, i=0, j=0, k=0;
            double kernels[N_SUPPORT_VECTORS] = {};

            KERNEL(sample, kernels);

            for(i=0; i < N_CLASSES; i++){
                amounts[i] = 0; //Just to ensure everything is cleared
            }

            for(i=0; i<N_CLASSES; i++){
                for(j=i+1; j<N_CLASSES; j++){
                    decision_rule = 0;
                    for(k=ranges[j]; k<ranges[j+1]; k++){
                        decision_rule += kernels[k] * coefs[i][k];
                    }

                    for(k=ranges[i]; k<ranges[i+1]; k++){
                        decision_rule += kernels[k] * coefs[j-1][k];
                    }

                    #if N_CLASSES==2
                    if(decision_rule + intercepts[d_rule] < 0){
                        amounts[i]++;
                    }
                    else{
                        amounts[j]++;
                    }
                    #else
                    if(decision_rule + intercepts[d_rule] > 0){
                        amounts[i]++;
                    }
                    else{
                        amounts[j]++;
                    }
                    #endif

                    d_rule++;

                }
            }

            for(i=0; i<N_CLASSES; i++){
                class = (amounts[i] > amounts[class]) ? i : class;
            }


            return class;
        }

        #endif



        """ % (self.n_sv, self.n_features, self.n_classes, self.kernel_type, self.gamma, self.coef,
        self.sv, self.dual_coefs, self.ranges, self.coefs, self.cls_combinations, self.intercepts, self.degree)
