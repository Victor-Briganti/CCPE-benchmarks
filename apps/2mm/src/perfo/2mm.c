/**
 * 2mm.c: This file is part of the PolyBench 3.0 test suite.
 *
 *
 * Contact: Louis-Noel Pouchet <pouchet@cse.ohio-state.edu>
 * Web address: http://polybench.sourceforge.net
 */
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

/* Include polybench common header. */
#include "polybench.h"

/* Include benchmark-specific header. */
/* Default data type is double, default size is 4000. */
#include "2mm.h"

#define MIN(x, y) ((x) < (y) ? (x) : (y))

/* Array initialization. */
static void init_array(int ni, int nj, int nk, int nl, DATA_TYPE *alpha,
                       DATA_TYPE *beta,
                       DATA_TYPE POLYBENCH_2D(A, ni, nk, ni, nl),
                       DATA_TYPE POLYBENCH_2D(B, nk, nj, nk, nj),
                       DATA_TYPE POLYBENCH_2D(C, nl, nj, nl, nj),
                       DATA_TYPE POLYBENCH_2D(D, ni, nl, ni, nl)) {
  *alpha = 32412;
  *beta = 2123;

  for (int i = 0; i < ni; i++)
    for (int j = 0; j < nk; j++)
      A[i][j] = ((DATA_TYPE)i * j) / ni;

  for (int i = 0; i < nk; i++)
    for (int j = 0; j < nj; j++)
      B[i][j] = ((DATA_TYPE)i * (j + 1)) / nj;

  for (int i = 0; i < nl; i++)
    for (int j = 0; j < nj; j++)
      C[i][j] = ((DATA_TYPE)i * (j + 3)) / nl;

  for (int i = 0; i < ni; i++)
    for (int j = 0; j < nl; j++)
      D[i][j] = ((DATA_TYPE)i * (j + 2)) / nk;
}

/* DCE code. Must scan the entire live-out data.
   Can be used also to check the correctness of the output. */
static void print_array(int ni, int nl,
                        DATA_TYPE POLYBENCH_2D(D, ni, nl, ni, nl)) {
  int i, j;

  for (i = 0; i < ni; i++)
    for (j = 0; j < nl; j++) {
      fprintf(stdout, DATA_PRINTF_MODIFIER, D[i][j]);
      if ((i * ni + j) % 20 == 0)
        fprintf(stdout, "\n");
    }
  fprintf(stdout, "\n");
}

/* Main computational kernel. The whole function will be timed,
   including the call and return. */
static void kernel_2mm(int ni, int nj, int nk, int nl, DATA_TYPE alpha,
                       DATA_TYPE beta,
                       DATA_TYPE POLYBENCH_2D(tmp, ni, nj, ni, nj),
                       DATA_TYPE POLYBENCH_2D(A, ni, nk, ni, nk),
                       DATA_TYPE POLYBENCH_2D(B, nk, nj, nk, nj),
                       DATA_TYPE POLYBENCH_2D(C, nl, nj, nl, nj),
                       DATA_TYPE POLYBENCH_2D(D, ni, nl, ni, nl)) {
/* D := alpha*A*B*C + beta*D */
#pragma omp parallel num_threads(NUM_THREADS)
  {
#if PERFO == 0
#pragma omp approx for perfo(init, (int)(10 * DROP))
#elif PERFO == 1
#pragma omp approx for perfo(fini, (int)(10 * DROP))
#elif PERFO == 2
#pragma omp approx for perfo(large, (int)(10 * DROP))
#elif PERFO == 3
#pragma omp approx for perfo(small, (int)(10 * DROP))
#elif PERFO == 4
#pragma omp approx for perfo(default, (int)(10 * DROP))
#endif
    for (int i = 0; i < ni; i++)
      for (int j = 0; j < nj; j++) {
        tmp[i][j] = 0;
        for (int k = 0; k < nk; ++k)
          tmp[i][j] += alpha * A[i][k] * B[k][j];
      }

#if PERFO == 0
#pragma omp approx for perfo(init, (int)(10 * DROP))
#elif PERFO == 1
#pragma omp approx for perfo(fini, (int)(10 * DROP))
#elif PERFO == 2
#pragma omp approx for perfo(large, (int)(10 * DROP))
#elif PERFO == 3
#pragma omp approx for perfo(small, (int)(10 * DROP))
#elif PERFO == 4
#pragma omp approx for perfo(default, (int)(10 * DROP))
#endif
    for (int i = 0; i < ni; i++)
      for (int j = 0; j < nl; j++) {
        D[i][j] *= beta;
        for (int k = 0; k < nj; ++k)
          D[i][j] += tmp[i][k] * C[k][j];
      }
  }
}

int main(int argc, char **argv) {
  /* Retrieve problem size. */
  int ni;
  scanf("%d", &ni);
  int nj;
  scanf("%d", &nj);
  int nk;
  scanf("%d", &nk);
  int nl;
  scanf("%d", &nl);

  /* Variable declaration/allocation. */
  DATA_TYPE alpha;
  DATA_TYPE beta;
  POLYBENCH_2D_ARRAY_DECL(tmp, DATA_TYPE, ni, nj, ni, nj);
  POLYBENCH_2D_ARRAY_DECL(A, DATA_TYPE, ni, nk, ni, nk);
  POLYBENCH_2D_ARRAY_DECL(B, DATA_TYPE, nk, nj, nk, nj);
  POLYBENCH_2D_ARRAY_DECL(C, DATA_TYPE, nl, nj, nl, nj);
  POLYBENCH_2D_ARRAY_DECL(D, DATA_TYPE, ni, nl, ni, nl);

  /* Initialize array(s). */
  init_array(ni, nj, nk, nl, &alpha, &beta, POLYBENCH_ARRAY(A),
             POLYBENCH_ARRAY(B), POLYBENCH_ARRAY(C), POLYBENCH_ARRAY(D));

  /* Start timer. */
  polybench_start_instruments;

  /* Run kernel. */
  kernel_2mm(ni, nj, nk, nl, alpha, beta, POLYBENCH_ARRAY(tmp),
             POLYBENCH_ARRAY(A), POLYBENCH_ARRAY(B), POLYBENCH_ARRAY(C),
             POLYBENCH_ARRAY(D));

  /* Stop and print timer. */
  polybench_stop_instruments;
  polybench_print_instruments;

  /* Prevent dead-code elimination. All live-out data must be printed
     by the function call in argument. */
  print_array(ni, nl, POLYBENCH_ARRAY(D));

  /* Be clean. */
  POLYBENCH_FREE_ARRAY(tmp);
  POLYBENCH_FREE_ARRAY(A);
  POLYBENCH_FREE_ARRAY(B);
  POLYBENCH_FREE_ARRAY(C);
  POLYBENCH_FREE_ARRAY(D);

  return 0;
}
