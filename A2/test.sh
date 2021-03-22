./Lorenzo360-Administration.py Administration-test2.in  > temp.txt
diff temp.txt Administration-test2.out
./Lorenzo360-Administration.py Administration-test1.in  > temp.txt
diff temp.txt Administration-test1.out

rm temp.txt
echo DONE 

