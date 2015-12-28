echo "Compilation..."
gcc -shared -fPIC -std=c99 -fopenmp -O2 -Wall task.c -o libtask.so -lm
echo "Execute Python"
python task.py
