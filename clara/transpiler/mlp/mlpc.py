class MLPCTranpiler(object):

    def __init__(self, model):
        self.model = model
        self.layer_sizes = ','.join(map(lambda x : str(x), self.model.hidden_layer_sizes))
        self.build_weights()
        self.build_layers()
        self.build_bias()

    def build_layers(self):
        self.networks = ""
        self.name_networks = "%s" % (','.join(["network%d" %(x+1) for x in range(len(self.model.hidden_layer_sizes))]))

        i = 1
        for hl in self.model.hidden_layer_sizes:
            self.networks += "double network%d[%d] = {0};" % (i, hl)
            i+=1
    def build_bias(self):
        i = 1
        self.bias_networks = "double * bias_networks[N_LAYERS-1] = {%s};" % (','.join(["bias%d" %(x+1) for x in range(len(self.model.intercepts_))]))

        self.bias =  ""
        for bias_networks in self.model.intercepts_:
            matrix = []
            self.bias += "double bias%d[%d] = {%s};\n" % (i, len(bias_networks ), ",".join(bias_networks.astype(str)))
            i+=1


    def build_weights(self):
        self.weights_networks = "double * weights_networks[N_LAYERS-1] = {%s};" % (','.join(["weights%d" %(x+1) for x in range(len(self.model.coefs_))]))
        self.weigths =  ""
        i = 1
        for weights_networks in self.model.coefs_:
            matrix = []
            for weights in weights_networks:
                matrix.append(','.join(weights.astype(str)))

            self.weigths += "double weights%d[%d] = {%s};\n" % (i, len(weights_networks) * len(weights), ",".join(matrix))
            i+=1
            
    def generate_code(self):
        return """
        /*
        The following code was generated using Clara.Transpiler. For more information please visit: https://github.com/asergiobranco/clara
        */
        #include <stdio.h>
        #include <math.h>

        #define N_LAYERS %d
        #define N_CLASSES %d
        #define N_FEATURES %d

        #define %s

        int networks_len[N_LAYERS] = {N_FEATURES, %s, N_CLASSES};

        double sample[N_FEATURES] = {0};
        %s
        double network_out[N_CLASSES] = {0};

        double * networks[N_LAYERS] = {sample, %s, network_out};

        %s

        %s

        %s
        %s

        #ifdef IDENTITY
        double identity(double neuron){
            return neuron;
        }
        #define ACTIVATION(...) identity(__VA_ARGS__)
        #endif


        #ifdef LOGISTIC
        double logistic(double neuron){
          return 1 / (1+exp(-neuron));
        }
        #define ACTIVATION(...) logistic(__VA_ARGS__)
        #endif

        #ifdef RELU
        double relu(double neuron){
          return (neuron > 0.0 ? neuron : 0.0);
        }
        #define ACTIVATION(...) relu(__VA_ARGS__)
        #endif

        #ifdef TANH
        #define ACTIVATION(...) tanh(__VA_ARGS__)
        #endif

        double * softmax(double * neurons, int len){
            double sum = 0;
            int i = 0;
            for(i =0; i<len; i++){
                neurons[i] = exp(neurons[i]);
                sum += neurons[i];
            }

            for(i =0; i<len; i++){
                neurons[i] /= sum;
            }

            return neurons;
        }

        double * propagation(double * network, double * next_network, double * weights, double * bias, int network_len, int next_network_len, int layer_no){
          int i = 0, j = 0, w=0;
          for(i=0; i < next_network_len; i++){
              next_network[i] = bias[i];
          }

          for(i=0; i < next_network_len; i++){
            for(j = 0; j < network_len; j++){
                w = (next_network_len * j) + i;
              next_network[i] += network[j] * weights[w];
            }
              if(layer_no < (N_LAYERS-2)){
                  next_network[i] = ACTIVATION(next_network[i]);
              }

          }



          return next_network;
        }

        int predict(double * sample){
          int i = 0;
          for(i =0 ; i<N_FEATURES; i++){networks[0][i] = sample[i];}
          for(i = 0; i < N_LAYERS - 1; i++){
            propagation(networks[i], networks[i+1], weights_networks[i], bias_networks[i], networks_len[i], networks_len[i+1], i);
          }

            softmax(networks[N_LAYERS-1], networks_len[N_LAYERS-1]);


          int class = 0;
          for(i = 0; i < N_CLASSES; i++){
            class = networks[N_LAYERS-1][i] > networks[N_LAYERS-1][class] ?  i : class;
          }
            return class;
        }


        """ % (
        len(self.model.coefs_) + 1, len(self.model.coefs_[0]), len(self.model.classes_), self.model.activation.upper(), self.layer_sizes,
        self.networks, self.name_networks,
        self.bias, self.bias_networks,
        self.weigths, self.weights_networks
        )
