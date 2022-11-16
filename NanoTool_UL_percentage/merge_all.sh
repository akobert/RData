#!/bin/bash

#This Script merges multiple files of the same bin (i.e. file 1,2,3,4... of DataC)

./merge_5.sh $1
./merge_10.sh $1
./merge_15.sh $1
./merge_25.sh $1
./merge_30.sh $1
./merge_50.sh $1
