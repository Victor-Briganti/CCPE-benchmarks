#include <stdio.h>
#include <stdlib.h>

#ifndef DATATYPE
#define DATATYPE int
#endif

int main(int argc, char *argv[]) {
  int size;
  DATATYPE *A, *B, *C;
  int i, j, k;

  scanf("%d", &size);

  // Allocate memory for input matrices
  A = (DATATYPE *)calloc(size * size, sizeof(DATATYPE));
  B = (DATATYPE *)calloc(size * size, sizeof(DATATYPE));

  // Allocate memory for resulting matrix
  C = (DATATYPE *)calloc(size * size, sizeof(DATATYPE));

  // Read input A
  for (i = 0; i < size; i++) {
    for (j = 0; j < size; j++) {
      scanf("%d", &(A[i * size + j]));
    }
  }

  // Read input B
  for (i = 0; i < size; i++) {
    for (j = 0; j < size; j++) {
      scanf("%d", &(B[i * size + j]));
    }
  }

// Multiply
#pragma omp parallel for num_threads(NUM_THREADS) schedule(dynamic) collapse(2)
  for (int i = 0; i < size; i++) {
    for (int j = 0; j < size; j++) {
      DATATYPE temp = 0;
#pragma omp approx memo threshold(THRESHOLD) shared(temp)
      for (int k = 0; k < size; k++) {
        temp += A[i * size + k] * B[k * size + j];
      }
      C[i * size + j] = temp;
    }
  }

  // Print output C
  for (i = 0; i < size; i++) {
    for (j = 0; j < size; j++) {
      printf("%d\n", C[i * size + j]);
    }
  }

  return 0;
}
