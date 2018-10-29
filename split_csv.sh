#!/bin/bash -l
#$ -S /bin/bash
#$ -N $1
mkdir $1_splited
tail -n +2 $1 | split -l 5000 - $1_splited/split_
for file in $1_splited/split_*
do
    head -n 1 $1 > tmp_file
    cat $file >> tmp_file
    mv -f tmp_file $file
done
