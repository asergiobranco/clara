class LinearSVMTranspiler(object):

    def __init__(self, model):
        self.model = model
        self.n_classes = len(self.model.classes_)
        self.n_coefs = len(self.model.coef_[0])
        self.build_coefs()
        self.build_intercepts()

    def build_coefs(self):
        matrix =[]
        for sv in self.model.coef_:
            matrix.append("{%s}" % ','.join(sv.astype(str)))

        self.coefs_ = ',\n'.join(matrix)

    def build_intercepts(self):
        self.intercept_ = ','.join(self.model.intercept_.astype(str))

    def generate_code(self):
        return """
        /*
        The following code was generated using Clara.Transpiler. For more information please visit: https://github.com/asergiobranco/clara
        */
        #define N_CLASSES %d
        #define N_COEFS %d
        double coefficients[N_CLASSES][N_COEFS] = {%s};
        double intercepts[N_CLASSES] = {%s};
        int predict (double * sample) {
            double class_val = 0;
            unsigned int class = 0, i, il, j, jl;

            for (i = 0, il = N_CLASSES; i < il; i++) {
                double prob = 0.0;
                for (j = 0, jl = N_COEFS; j < jl; j++) {
                    prob += coefficients[i][j] * sample[j];
                }
                if(i==0){class_val = prob + intercepts[i];}
                if (prob + intercepts[i] > class_val) {
                    class_val = prob + intercepts[i];
                    class= i;
                }
            }
            return class;
        }
        """ % (self.n_classes, self.n_coefs, self.coefs_, self.intercept_)
