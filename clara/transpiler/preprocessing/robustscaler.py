class RobustScalerTranspiler(object):

    def __init__(self, model):
        self.model = model
        self.n_features = len(self.model.mean_)
        self.center = ','.join(self.model.center_.astype(str))
        self.scale = ','.join(self.model.scale_.astype(str))
        self.with_what()

    def with_what(self):
        self.what = ""

        if self.model.with_scaling:
            self.what+= "#define SCALE\n"

        if self.model.with_centering:
            self.what+= "#define CENTERING\n"


    def generate_code(self):
        return """
        /*
        The following code was generated using Clara.Transpiler. For more information please visit: https://github.com/asergiobranco/clara
        */
        #define N_FEATURES %d

        %s

        #ifdef CENTERING
        double center[N_FEATURES] = {%s};
        #endif

        #ifdef SCALE
        double scale[N_FEATURES] = {%s};
        #endif

        double * transform(double * sample){
            unsigned int i = 0;

            #ifdef CENTERING
            for(i = 0; i < N_FEATURES; i++){
                sample[i] -= center[i];
            }
            #endif

            #ifdef SCALER
            for(i = 0; i < N_FEATURES; i++){
                sample[i] /= scale[i];
            }
            #endif

            return sample;
        }
        """ % (self.n_features, self.what, self.mean, self.std)
