class SVRTranspiler(object):

    def __init__(self, model):
        self.model = model

        self.n_sv = len(self.model.support_vectors_)
        self.n_features = len(self.model.support_vectors_[0])

        self.gamma = str(self.model._gamma)
        self.coef = str(self.model.coef0)
        self.degree = str(self.model.degree)
        self.kernel_type = self.model.kernel.upper()

        self.build_support_vectors()
        self.build_intercepts()
        self.build_coefs()

    def build_intercepts(self):
        self.intercepts = self.model.intercept_[0]

    def build_support_vectors(self):
        matrix =[]
        for sv in self.model.support_vectors_:
            matrix.append("{%s}" % ','.join(sv.astype(str)))

        self.sv = ',\n'.join(matrix)

    def build_coefs(self):
        self.coefs = ','.join(self.model.dual_coef_[0].astype(str))

    def generate_code(self):
        return """
        /*
        The following code was generated using Clara.Transpiler. For more information please visit: https://github.com/asergiobranco/clara
        */
        #include <stdio.h>
        #include <math.h>

        #define N_SUPPORT_VECTORS %d
        #define N_FEATURES %d
        #define %s

        #ifndef LINEAR
        #define GAMMA %s
        #define COEF %s
        #endif

        double support_vectors[N_SUPPORT_VECTORS][N_FEATURES] = {%s};
        double coefs[N_SUPPORT_VECTORS] = {%s};
        double intercepts = %s;


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
        #define KERNEL(...) linear_kernel(__VA_ARGS__)
        #endif

        double predict(double * sample){
            double decision_rule = 0.0;
            unsigned int i=0;
            double kernels[N_SUPPORT_VECTORS] = {};

            KERNEL(sample, kernels);


            for(i=0; i<N_SUPPORT_VECTORS; i++){
                decision_rule += kernels[i] * coefs[i];
            }

            return (decision_rule + intercepts);
        }

        """ % (self.n_sv, self.n_features, self.kernel_type, self.gamma, self.coef,
        self.sv, self.coefs, self.intercepts, self.degree)
