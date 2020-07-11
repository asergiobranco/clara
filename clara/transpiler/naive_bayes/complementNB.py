class ComplementNBTranspiler(object):

    def __init__(self, model):
        self.model = model
        self.n_classes = len(self.model.class_log_prior_)
        self.n_features = len(self.model.feature_log_prob_[0])
        self.build_cls_log()
        self.build_features_log()

    def build_cls_log(self):
        self.cls_log_prior = ','.join(self.model.class_log_prior_.astype(str))

    def build_features_log(self):
        matrix =[]
        for log in self.model.feature_log_prob_.T:
            matrix.append("{%s}" % ','.join(log.astype(str)))

        self.f_log_prob = ',\n'.join(matrix)

    def generate_code(self):
        return """/*
        The following code was generated using Clara.Transpiler. For more information please visit: https://github.com/asergiobranco/clara
        */
        #define N_CLASSES %d
        #define N_FEATURES %d

        double f_log_prob[N_FEATURES][N_CLASSES] = {%s};

        #if N_CLASSES == 1
        double cls_log_prior[N_CLASSES] = {%s};
        #endif

        int predict(double * sample){
            unsigned int i = 0, j = 0, class;
            double classes_prob[N_CLASSES] = {0};
            for(i=0; i<N_CLASSES; i++){
                for(j=0; j<N_FEATURES; j++){
                    classes_prob[i] +=  sample[j] * f_log_prob[j][i];
                }

                #if N_CLASSES == 1
                classes_prob[i] += cls_log_prior[i];
                #endif
            }

            class = 0;
            for(i=0; i<N_CLASSES; i++){
                if(classes_prob[i] > classes_prob[class]){
                    class = i;
                }
            }
            return class;
        }
        """ % (self.n_classes, self.n_features, self.f_log_prob,self.cls_log_prior)
