class StandardScalerTranspiler(object):

    def __init__(self, model):
        self.model = model
        self.n_features = len(self.model.mean_)
        self.mean = ','.join(self.model.mean_.astype(str))
        self.std = ','.join(self.model.scale_.astype(str))
        self.with_what()

    def with_what(self):
        self.what = ""

        if self.model.with_mean:
            self.what+= "#define MEAN\n"

        if self.model.with_std:
            self.what+= "#define STD\n"


    def generate_code(self):
        return """
        /*
        The following code was generated using Clara.Transpiler. For more information please visit: https://github.com/asergiobranco/clara
        */
        #define N_FEATURES %d

        %s

        #ifdef MEAN
        double mean[N_FEATURES] = {%s};
        #endif

        #ifdef STD
        double scale[N_FEATURES] = {%s};
        #endif

        double * transform(double * sample){
            unsigned int i = 0;
            #ifdef MEAN
            for(i = 0; i < N_FEATURES; i++){
                sample[i] -= mean[i];
            }
            #endif

            #ifdef STD
            for(i = 0; i < N_FEATURES; i++){
                sample[i] /= scale[i];
            }
            #endif

            return sample;
        }
        """ % (self.n_features, self.what, self.mean, self.std)
