#! /bin/bash
convert() {
   case $1 in
     I) value=1 ;;
     V) value=5 ;;
     X) value=10 ;;
     L) value=50 ;;
     C) value=100 ;;
     D) value=500 ;;
     M) value=1000 ;;
  esac
  echo $value
   
}

decimalRoman(){
	inp=$1
  arr1=("" M MM MMM)
  arr2=("" C CC CCC CD D DC DCC DCCC CM)
  arr3=("" X XX XXX XL L LX LXX LXXX XC)
  arr4=("" I II III IV V VI VII VIII IX)
  
    out=${arr1[$((inp/1000))]}
    inp=$inp%1000
    out+=${arr2[$((inp/100))]}
    inp=$inp%100
    out+=${arr3[$((inp/10))]}
    inp=$inp%10
    out+=${arr4[$inp]}
	  echo $out
}



if (( $# == 1 ))	
then
	decimal=$(decimalRoman $1)
	echo $decimal
elif [[ $1 =~ ^[0-9]+$ ]]	
then
   #echo "hi"
	add=$(($1+$2))
	output=$(decimalRoman $add)
	echo $output
else
  #echo "hello"

	symbol="I"
	value1=0
	num=$1
  	len=$((${#1}-1))
	for((i=$len;i>=0;i--));		
	do
		a2=$(convert ${symbol})
		char="${num:$i:1}"
		a1=$(convert $char)

		if !((a1 >= a2))
		then
			value1=$(($value1-$a1))
		else
			value1=$(($value1+$a1))
			symbol=$char
		fi
	done

	symbol="I"
	value2=0
	num=$2
  	len=$((${#2}-1))
	for((i=$len;i>=0;i--));		
	do
		a2=$(convert ${symbol})
		char="${num:$i:1}"
		a1=$(convert $char)

		if !((a1 >= a2))
		then
			value2=$(($value2-$a1))
		else
			value2=$(($value2+$a1))
			symbol=$char
		fi
	done

	echo $(( $value1+$value2 ))
fi