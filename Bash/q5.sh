#! /bin/bash

rm -rf temp_activity	#remove directory if already such directory is created

#5a
mkdir temp_activity

#5b
cd temp_activity
touch temp{1..50}.txt

#5c
for((i=1;i<=25;++i));
do
	mv "temp"$i".txt" "temp"$i".md"
done

#5d
#5d.a
for f in *;
do
	name=$f
	extension="${name##*.}"
	name="${name%.*}"
	
	mv "${name}.${extension}" "${name}"_modified.${extension}""
done

#for((i=1;i<=50;++i));
#do 
#	if [[ i -lt 26 ]]
#	then 
#		mv "temp"$i".md" "temp"$i"_modified.md"
#	else
#		mv "temp"$i".txt" "temp"$i"_modified.txt"	
#	fi
#done

#5d.b
for f in *;
do
	if [[ $f == *.txt ]]
	then
		zip -q txt_compressed.zip $f
	fi
done