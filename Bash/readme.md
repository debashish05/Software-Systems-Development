## Assignment - 1: Bash Scripting
#### Software Systems Development

###### Answer 1
1. a ) `ls -d */` is used for printing all the visible directories in the current folder.
It will through an error if there is no directory. To catch this error will point this stderr to a /dev/null file. When directory names are printed it will also print extra '/' since it is a directory. To avoid this I have used cut. I have commented on this line because in the expected output it is not considered.  

1. b ) `du -sh */` is used to get disk size followed by directory name. It will through an error if there is no directory. To catch this error will point this stderr to a /dev/null file. When directory names are printed it will also print extra '/' since it is a directory. To avoid this I have used cut. Now we want to sort it in decreasing order. To-Do this I have used the command `sort -rh`. In the expected output, we have to print the directory names followed by sizes. To-Do this I have piped the output to awk. `awk  '{printf("%s\t%s\n",$2,$1);}'` So for every record we will have two fields so we just print the second field followed by 1st field. And also we have to put a tab between them.

###### Answer 2
Two command-line arguments filename will be provided.
In the expected output, it is mentioned that we should print "Inside Output.txt file" followed by a blank line but as per the discussion we just need to print the words in lowercase. So I have commented that line. `awk '{for(i=1;i<=NF;i++) { print $i }}' $1 > temp.txt` for every word I am printing it to a temporary file temp.txt. `grep -i 'ing\>' temp.txt` It finds the words ending with ing, and not being case sensitive. Then converting all upper case to lower case `tr A-Z a-z`  and then writing the desired words in the given output file. And in end, I have removed the file by `rm temp.txt`.

###### Answer 3
`compgen -bck` is used to get all the commands. I have piped this command to and sorted it. Then used `uniq` to remove duplicate. Sorting is a prerequisite for uniq. `input=( $(echo ${1}| grep -o . | sort |tr -d "\n") )` will sort the input word's characters. Grep will break the word into characters and then we remove the new line decimator to make it a word. Then for every command will we check for the permutation only if sizes are equal. Then we also sort the commands with equal sizes. If words after sorting are equal then there exists a permutation for the given input word and we need to print YES followed by tab space and words. Since We have sorted the compgen output we will already get matching words in sorted order. So no need to extra sort.

###### Answer 4
There is an assumption that valid input will be provided. For 4a only an integer in the range [1,3999] will be provided. For 4b) two integers whose sum will range in [1,3999] will be provided.
For 4c) two valid Roman numbers will be provided. The Roman numbers will be made from capital letters. The character included can be I,V,X,L,C,D,M.

###### Answer 5
It assumes that if there is a directory temp_activity it will be deleted first. Files are not deleted after the script is over. `zip` is a prerequisite for this.  