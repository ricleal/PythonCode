/**
 * 3D
   for ( int i = 0; i < width; ++i )
	for ( int j = 0; j < height; ++j )
		for ( int k = 0; k < depth; ++k )
			sum += data[i][j][k];

			index = (i * height * depth) + (j * depth) + k
 * 2D
 * for ( int i = 0; i < width; ++i )
	for ( int j = 0; j < height; ++j )
		index = i * width + j

 */


__kernel void stupid_mul(__global float* A, __global float* B, __global float* C) {


	const int dim1 = get_global_size(0);
	const int dim2 = get_global_size(1);

	for(int i=0; i<dim1; i++) // row
	{
		for(int j=0; j<dim2; j++) // column
		{
			int idx = dim1 * i + j;
			C[idx] = 0;
			for(int k=0; k<dim2; k++)
			{
				//C[idx] = C[idx] + ( A[i][k] * B[k][j] );
				C[idx] = C[idx] + ( A[dim1 * i + k] * B[dim2*j+k] );
			}
		}
	}
}
