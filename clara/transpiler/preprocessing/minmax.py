class MinMaxScalerTranspiler(object):

    def __init__(self, model):
        self.model = model
        self.n_features = len(self.model.min_)
        self.min = ','.join(self.model.min_.astype(str))
        self.std = ','.join(self.model.scale_.astype(str))


    def generate_code(self):
        return """
        /*
        The following code was generated using Clara.Transpiler. For more information please visit: https://github.com/asergiobranco/clara
        */
        #define N_FEATURES %d


        double min[N_FEATURES] = {%s};
        double scale[N_FEATURES] = {%s};


        double * transform(double * sample){
            unsigned int i = 0;

            for(i = 0; i < N_FEATURES; i++){
                sample[i] *= scale[i];
            }

            for(i = 0; i < N_FEATURES; i++){
                sample[i] += min[i];
            }


            return sample;
        }
        """ % (self.n_features, self.min, self.std)
