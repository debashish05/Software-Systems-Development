#! /bin/bash

#2
#echo "Inside "$2" file" > $2	# Need to check line no. 4 and 5 has to be included or not
#echo >> $2

awk '{for(i=1;i<=NF;i++) { print $i }}' $1 > temp.txt
grep -i 'ing\>' temp.txt |  tr A-Z a-z > $2
rm temp.txt

#2 me output lowercase me karna hai, if new test case is passed output will be newly created
