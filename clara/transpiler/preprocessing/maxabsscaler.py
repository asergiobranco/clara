class MaxAbsScalerTranspiler(object):

        def __init__(self, model):
            self.model = model
            self.n_features = len(self.model.scale_)
            self.std = ','.join(self.model.scale_.astype(str))


        def generate_code(self):
            return """
            /*
            The following code was generated using Clara.Transpiler. For more information please visit: https://github.com/asergiobranco/clara
            */
            #define N_FEATURES %d

            double max[N_FEATURES] = {%s};


            double * transform(double * sample){
                unsigned int i = 0;

                for(i = 0; i < N_FEATURES; i++){
                    sample[i] /= max[i];
                }

                return sample;
            }
            """ % (self.n_features,  self.std)
