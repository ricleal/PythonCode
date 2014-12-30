echo "GCC 1"
gcc -O3 -lm -fopenmp -fPIC -c task.c -o task.o
echo "GCC 2"
gcc -shared -lgomp -o libtask.so task.o
# gcc -shared -liomp5 -o libtask.so task.o
echo "Execute Python"
python task.py
