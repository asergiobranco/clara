import numpy as np

class DecisionTreeClassifierTranspiler(object):

    def __init__(self, model):
        self.model = model

        self.build_classes()
        self.build_feature_idx()
        self.build_right_nodes()
        self.build_thresholds()

    def build_feature_idx(self):
        self.features_idx = ','.join(self.model.tree_.feature.astype(str))

    def build_classes(self):
        class_aux = list(map(lambda x : x[0], self.model.tree_.value))
        self.classes = np.argmax(class_aux, axis = 1)
        self.classes = ','.join(self.classes.astype(str))

    def build_right_nodes(self):
        self.right_nodes = ','.join(self.model.tree_.children_right.astype(str)).replace('-1', '0')

    def build_thresholds(self):
        self.thresholds = ','.join(self.model.tree_.threshold.astype(str))

    def generate_code(self):
        return """
        /*
        The following code was generated using Clara.Transpiler. For more information please visit: https://github.com/asergiobranco/clara
        */
        #define NO_NODES %s

        unsigned char classes[NO_NODES] = {%s};

        int FEATURE_IDX_NODE[NO_NODES] = {%s};

        int RIGHT_CHILDS[NO_NODES] = {%s};

        float THRESHOLDS[NO_NODES] = {%s};


        int predict(double * sample){
            unsigned int current_node = 0;
            int feature_idx  = FEATURE_IDX_NODE[0];
            while(feature_idx >= 0){
                if(sample[feature_idx] <= THRESHOLDS[current_node]){
                    current_node++;
                }
                else{
                    current_node = RIGHT_CHILDS[current_node];
                }
                feature_idx = FEATURE_IDX_NODE[current_node];
            }
            return classes[current_node];
        }
        """ % (self.model.tree_.node_count, self.classes, self.features_idx, self.right_nodes, self.thresholds)
