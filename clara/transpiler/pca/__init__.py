class PCATranspiler(object):

    def __init__(self, model, transform = True):
        self.model = model
        self.library_ = ''
        self.n_components_ = len(self.model.components_)
        self.n_features_ = len(self.model.components_[0])
        self.mean_function_ = ''
        self.whithen_function_ = ''
        self.componentsT_ = "{ {%s} }" % ("},\n\t{".join(map(lambda x : ",".join(x.astype(str)), self.model.components_.T.astype(str))))
        self.explained_variance_ = "{%s}" %  (",".join(self.model.explained_variance_.astype(str)))
        self.code = """
        /*
        The following code was generated using Clara.Transpiler. For more information please visit: https://github.com/asergiobranco/clara
        */
        %s\n
        #define N_COMPONENTS %s
        #define N_FEATURES %s
        %s;
        double componentsT[N_FEATURES][N_COMPONENTS] = %s;
        double explained_variance[N_COMPONENTS] = %s;

        typedef struct pca_dimensions{
            double hoteling2;
            double q_residuals;
        } pca_dimensions_t;

        #ifdef MEAN
        double * X_mean(double * sample, double * sample_transformed){
            for(int i = 0; i < N_FEATURES; i++){
                sample_transformed[i] = sample[i] - mean[i];
            }
            return sample_transformed;
        }
        #endif

        %s

        double * calculate_scores(double * sample, double * scores){
            for(int i = 0; i < N_COMPONENTS; i++){
                scores[i] = 0;
                for(int j=0; j < N_FEATURES; j++){
                    scores[i] += sample[j] * componentsT[j][i];
                }
            }
            return scores;
        }

        void inverse(double * scores, double * inverse_sample){
            int i = 0, j = 0;


            #ifdef WHITHEN
            for(i = 0; i < N_COMPONENTS; i++){
                for(j = 0; j < N_FEATURES; j++){
                    inverse_sample[j] += scores[i] * componentsT[j][i] * sqrt(explained_variance[i]);
                }
            }
            #else
            for(i = 0; i < N_COMPONENTS; i++){
                for(j = 0; j < N_FEATURES; j++){
                    inverse_sample[j] += scores[i] * componentsT[j][i];
                }
            }
            #endif

            #ifdef MEAN
            for(j = 0; j < N_FEATURES; j++){
                inverse_sample[j] += mean[j];
            }
            #endif

        }

        pca_dimensions_t calculate_dimensions(double * sample){
            pca_dimensions_t val;
            double scores[N_COMPONENTS] = {0};
            double inverse_sample[N_FEATURES] = {0};
            double diff;
            int i = 0;

            val.hoteling2 = 0;
            val.q_residuals = 0;

            calculate_scores(sample, scores);

            for(i = 0; i < N_COMPONENTS; i++){
                val.hoteling2 += ((scores[i] * scores[i]) / explained_variance[i]);
            }

            inverse(scores, inverse_sample);

            for(i = 0; i < N_FEATURES; i++){
                diff = sample[i] - inverse_sample[i];
                val.q_residuals += (diff*diff);
            }


            return val;
        }

        double * predict(double sample[], double scores[]){
            #ifdef MEAN
            double sample_transformed[N_FEATURES];
            #endif

            double * x;

            x = sample;
            #ifdef MEAN
            x = X_mean(sample, sample_transformed);
            #endif



            calculate_scores(x, scores);
            %s
            return scores;
        }
        """

    def _default_header(self):
        """All the models need to have this code."""
        self.code += ""

    def _mean_function(self):
        if self.model.mean_ is not None:
            self.mean_ = "#define MEAN\n\ndouble mean[N_FEATURES]={%s}" % (','.join(self.model.mean_.astype(str)))
        else:
            self.mean_ = ""

    def _whiten_function(self):
        if self.model.whiten:
            self.library_ = "#include <math.h>"
            self.whithen_function_ = """
            double * whithen(double * scores){
                for(int i = 0; i < N_COMPONENTS; i++){
                    scores[i] /= sqrt(explained_variance[i]);
                }
                return scores;
            }
            """
            self.whithen_call_ = "scores = whithen(scores);"
        else:
            self.whithen_function_ = ""
            self.whithen_call_ = ""


    def generate_code(self):
        self._mean_function()
        self._whiten_function()

        self.final_code = self.code % (
            self.library_, self.n_components_, self.n_features_,
            self.mean_, self.componentsT_, self.explained_variance_,
            self.whithen_function_,
            self.whithen_call_
        )
        return self.final_code

    def export(self):
        pass
