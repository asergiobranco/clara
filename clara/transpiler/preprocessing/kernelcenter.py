class KernelCentererTranspiler(object):

    def __init__(self, model):
        self.model = model
        self.n_features = len(self.model.K_fit_rows_)
        self.K_fit_rows_ = ','.join(self.model.K_fit_rows_.astype(str))
        self.K_fit_all_ = self.model.K_fit_all_.astype(str)


    def generate_code(self):
        return """
        /*
        The following code was generated using Clara.Transpiler. For more information please visit: https://github.com/asergiobranco/clara
        */
        #define N_FEATURES %d


        double K_fit_rows_[N_FEATURES] = {%s};
        double K_fit_all_ = %s;


        double * transform(double * sample){
            unsigned int i = 0;
            double sum = 0.0;

            for(i = 0; i < N_FEATURES; i++){
                sum += sample[i];
            }

            sum /= N_FEATURES;

            for(i = 0; i < N_FEATURES; i++){
                sample[i] -= K_fit_rows_[i];
                sample[i] -= sum;
                sample[i] += K_fit_all_;
            }


            return sample;
        }
        """ % (self.n_features, self.K_fit_rows_, self.K_fit_all_)
