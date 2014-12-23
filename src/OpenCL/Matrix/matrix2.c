#define LDIM 16

__kernel void local_mul(__global float* A, __global float* B, __global float* C) {

    const int LX = get_local_id(0);
    const int LY = get_local_id(1);
    const int WX = get_group_id(0);
    const int WY = get_group_id(1);
    const int DIM = get_global_size(0);
    const int TILES = get_num_groups(0);

    __local float Al[LDIM][LDIM], Bl[LDIM][LDIM];
    __private float cl;
    cl = 0.f;
    //make sure, it's zero!
    for (int k = 0; k < TILES; ++k) {
        Al[LY][LX] = A[LX + LY * DIM + k * LDIM + WY * LDIM * DIM];
        Bl[LX][LY] = B[LX + LY * DIM + k * LDIM * DIM + WX * LDIM];
        // transpose here
        barrier(CLK_LOCAL_MEM_FENCE);
        for (int kk = 0; kk < LDIM; ++kk) {
        	cl += Al[LY][kk] * Bl[LX][kk];
        }
        //transpose here
        barrier(CLK_LOCAL_MEM_FENCE);
    }
    C[get_global_id(0) + get_global_id(1) * DIM] = cl;
}
