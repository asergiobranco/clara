class GaussianNBTranspiler(object):

    def __init__(self, model):
        self.model = model
        self.n_classes = len(self.model.class_prior_)
        self.n_features = len(self.model.theta_[0])
        self.build_cls_log()
        self.build_theta()
        self.build_sigma()

    def build_cls_log(self):
        self.cls_log_prior = ','.join(self.model.class_prior_.astype(str))

    def build_theta(self):
        matrix =[]
        for log in self.model.theta_:
            matrix.append("{%s}" % ','.join(log.astype(str)))

        self.theta = ',\n'.join(matrix)

    def build_sigma(self):
        matrix =[]
        for log in self.model.sigma_:
            matrix.append("{%s}" % ','.join(log.astype(str)))

        self.sigma = ',\n'.join(matrix)

    def generate_code(self):
        return """/*
        The following code was generated using Clara.Transpiler. For more information please visit: https://github.com/asergiobranco/clara
        */
#include <math.h>
#define N_CLASSES %d
#define N_FEATURES %d


double theta[N_CLASSES][N_FEATURES] = {%s};
double sigma[N_CLASSES][N_FEATURES] = {%s};

double cls_log_prior[N_CLASSES] = {%s};



int predict(double * sample){
    unsigned int i = 0, j = 0, class;
    double classes_prob[N_CLASSES] = {0};

    for(i=0; i<N_CLASSES; i++){
        for(j=0; j<N_FEATURES; j++){
            classes_prob[i] -=  0.5*log(2*M_PI*sigma[i][j]);
            classes_prob[i] -=  0.5*pow(sample[j] - theta[i][j], 2)/sigma[i][j];
        }

        classes_prob[i] += log(cls_log_prior[i]);
    }

    class = 0;
    for(i=0; i<N_CLASSES; i++){
        if(classes_prob[i] > classes_prob[class]){
            class = i;
        }
    }
    return class;
}""" % (self.n_classes, self.n_features, self.theta, self.sigma, self.cls_log_prior)
