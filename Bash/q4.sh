#! /bin/bash

integerToRoman(){
	# Interger to Roman
	# Input will be an integer and we will modify it to roman number

	num=${1}

	# Reference leetcode 
    I=("" I II III IV V VI VII VIII IX)
    X=("" X XX XXX XL L LX LXX LXXX XC)
    C=("" C CC CCC CD D DC DCC DCCC CM)
	M=("" M MM MMM)

    local roman=${M[$((num/1000))]}${C[$(($((num%1000))/100))]}${X[$(($((num%100))/10))]}${I[$((num%10))]}
	echo "$roman"
}

unorderedMap(){
	# Roman character corresponding integer value
	num=0
	if [[ ${1} == "I" ]]
	then 
		num=1
	elif [[ ${1} == "V" ]]
	then
		num=5
	elif [[ ${1} == "X" ]]
	then
		num=10
	elif [[ ${1} == "L" ]]
	then
		num=50
	elif [[ ${1} == "C" ]]
	then
		num=100
	elif [[ ${1} == "D" ]]
	then
		num=500
	else
		num=1000
	fi

	local value=${num}
	echo ${value}
}

romanToInteger(){
	# Convert Roman no. to integer
	# Assumption valid Roman no.
	number=${1}
	answer=0
	character="I"

	for((i=$((${#1}-1));i>=0;--i));		
	do
		char="${number:$i:1}"
		
		first=$(unorderedMap ${char})
		second=$(unorderedMap ${character})

		if ((first < second))
		then
			answer=$((${answer}-${first}))
		else
			answer=$((${answer}+${first}))
			character=${char}
		fi
	done

	local value=${answer}
	echo "$answer"
}


if [[ $# == 1 ]]				#4a	number to roman
then
	value=$(integerToRoman ${1})
	echo $value
elif [[ ${1} =~ ^[0-9]+$ ]]		#4b Addition of two integer and converting to roman
then
	sum=$((${1}+${2}))
	value=$(integerToRoman ${sum})
	echo $value
else							#4c Addition of two roman no and return output in integer
	value1=$(romanToInteger ${1})
	#echo $value1

	value2=$(romanToInteger ${2})
	#echo $value2

	echo $((${value1}+${value2}))
fi