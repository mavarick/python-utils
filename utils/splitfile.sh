#!/bin/bash
size=$2
lineno=`wc -l $1 | awk '{print $1}'`
echo $lineno

file=1
n1=1
while [ $n1 -lt $lineno ]
do
    n2=`expr $n1 + $size`
    sed -n "${n1}, ${n2}p" $1 > $1_$file.split
    n1=`expr $n2 + 1`
    file=`expr $file + 1`
done


