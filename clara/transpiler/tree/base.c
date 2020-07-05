#include <stdio.h>

#define NO_NODES 23

unsigned char classes[NO_NODES] = {1,1,2,2,2,1,1,1,2,1,2,1,1,1,1,0,0,2,2,1,0,0,1};

int FEATURE_IDX_NODE[NO_NODES] = {12,11,10,6,-2,-2,2,-2,-2,6,-2,0,-2,1,-2,-2,6,10,-2,-2,4,-2,-2};

int RIGHT_CHILDS[NO_NODES] = {16,9,6,5,0,0,8,0,0,11,0,13,0,15,0,0,20,19,0,0,22,0,0};

float THRESHOLDS[NO_NODES] = {755.0,2.1149998903274536,0.9350000023841858,1.5800000429153442,-2.0,-2.0,2.4499999284744263,-2.0,-2.0,0.7950000166893005,-2.0,13.174999713897705,-2.0,2.1249999403953552,-2.0,-2.0,2.165000081062317,0.8030000030994415,-2.0,-2.0,135.5,-2.0,-2.0};


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

int main(){
    double sample[] = {12.33,1.1,2.28,16.0,101.0,2.05,1.09,0.63,0.41,3.27,1.25,1.67,680.0};
    int class = 0;
    class = predict(sample);
    // 1
    printf("%d\n", class);
    return 0;

}
