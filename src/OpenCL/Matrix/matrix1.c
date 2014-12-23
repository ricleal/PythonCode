__kernel void naive_mul(__global float* A, __global float* B, __global float* C) {

	const int xid = get_global_id(0);
	const int yid = get_global_id(1);
	const int dim = get_global_size(0);

	__private float c = 0.f;

	for (int k = 0; k < dim; ++k) {
		c += A[k + yid * dim] * B[k*dim + xid];
	}
	C[xid + yid * dim] = c;
}
