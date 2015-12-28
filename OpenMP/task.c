#include <omp.h>
#include <math.h>
#include <stdio.h>

void do_some_omp_task(float* input_array, float* output_array, size_t size) {

	int i;
#pragma omp parallel for default(shared) private(i)
	for (i = 0; i < size; i++) {
		output_array[i] = sqrt( pow(input_array[i], input_array[i])
				* sin(input_array[i])
				* exp(input_array[i])
				* cos(input_array[i])
				* asin(input_array[i])
				* acos(input_array[i])
				* tan(input_array[i])
				* atan(input_array[i])
				* pow( tan(input_array[i]), atan(input_array[i]))
				);


	}
}
