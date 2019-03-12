#!/binbash

echo "Create zero-filled test file. SIZE will be 1024 x [YOUR INPUT] byte.
Enter the size of the file:"
read ans

dd if=/dev/zero of=test bs=1024 count=$ans
#rm -f test
