#include <omp.h>
#include <math.h>
#include <stdio.h>

// Recursive fibonacci
size_t fibonacci(size_t n){
  if (n == 0 || n == 1)
    return n;
  else
    return (fibonacci(n-1) + fibonacci(n-2));
}

// Main function
void do_some_omp_task(size_t *input_array, size_t *output_array, size_t size) {
	size_t i;
#pragma omp parallel for default(shared) private(i)
	for (i = 0; i < size; i++)
	{	
		output_array[i] = fibonacci(input_array[i]);
	}
}
