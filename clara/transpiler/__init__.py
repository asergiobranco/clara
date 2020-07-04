class PCATranspiler(object):

    def __init__(self, model, transform = True):
        self.model = model
        self.library_ = ''
        self.n_components_ = len(self.model.components_)
        self.n_features_ = len(self.model.components_[0])
        self.mean_function_ = ''
        self.whithen_function_ = ''
        self.componentsT_ = "{%s}" % ("},{".join(map(lambda x : ",".join(x.astype(str)), self.model.components_.T.astype(str))))
        self.explained_variance_ = "{%s}" %  (",".join(self.model.explained_variance_.astype(str)))
        self.code = """
        %s\n
        #define N_COMPONENTS {%s}\n
        #define N_FEATURES {%s}\n
        double componentsT[N_FEATURES][N_COMPONENTS] = %s;
        double explained_variance[N_COMPONENTS] = %s;

        %s

        {%s

        double * calculate_scores(double * sample){
            double scores[N_COMPONENTS] = {}
            for(int i = 0; i < N_COMPONENTS; i++){
                scores[i] = 0;
                for(int j=0; j < N_FEATURES; j++){
                    scores[i] += sample[j] * componentsT[j][i];
                }
            }
            return scores;
        }

        double * predict(double sample[]){
            double * scores;
            %s
            calculate_scores(sample);
            %s
            return scores;
        }
        """

    def _default_header(self):
        """All the models need to have this code."""
        self.code += ""

    def _mean_function(self):
        if self.model.mean_ is not None:
            self.mean_function_ = """
            double * X_mean(double * sample){
                double x_mean_tranformed[N_FEATURES] = {}
                for(int i = 0; i < N_FEATURES; i++){
                    x_mean_transformed = sample[i] - MEAN[i];
                }
                return x_mean_tranformed;
            }"""
            self.mean_call_ = "sample = X_mean(sample);"
        else:
            self.mean_function_ = ''
            self.mean_call_ = ""

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
            self.componentsT_, self.explained_variance_,
            self.mean_function_, self.whithen_function_,
            self.mean_call_, self.whithen_call_
        )
        return self.final_code

    def export(self):
        pass
