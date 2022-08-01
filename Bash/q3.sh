#! /bin/bash

first=0

check(){
	# check if any permutation of first argument can form second argument
	# 1st argument ${1} will be input word that need to be checked, in sorted order
	# 2nd argument ${2} will be one of the commands

	cmd=( $(echo ${2}| grep -o . | sort |tr -d "\n") )
	
	if [[ "${1}" == "$cmd" ]]
	then
		if [[ ${first} == 0 ]]
		then 
			echo -ne "YES"
			first=1
		fi
		echo -ne "\t" ${2} 
	fi
}

list=( $(compgen -bck | sort | uniq) )		
#-c for commands directly available to be executed -b bash builtins -k bash keywords

len=${#list[*]}
input=( $(echo ${1}| grep -o . | sort |tr -d "\n") )

for ((i=0;i<${len};++i))
do
	if [[ ${#input} == ${#list[i]} ]] 
	then
		check ${input} ${list[i]} 
	fi
done

if [[ ${first} == 0 ]]
then 
	echo -ne "NO"
fi