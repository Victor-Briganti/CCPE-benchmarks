#include <omp.h>
#include <stdio.h>
#include <stdlib.h>

int main() {
  long long count = 0;
  long long n;
  double pi;

  scanf("%lld", &n);

#pragma omp approx fastmath
  {
#pragma omp parallel num_threads(NUM_THREADS) shared(count)
    {
      double x, y, z;
      unsigned int thread_seed = 0;

#pragma omp for reduction(+ : count)
      for (int i = 0; i < n; ++i) {
        x = (double)rand_r(&thread_seed) / RAND_MAX;
        y = (double)rand_r(&thread_seed) / RAND_MAX;

        z = x * x + y * y;

        if (z <= 1) {
          count++;
        }
      }
    }

    pi = (double)count / n * 4;
  }

  printf("%g\n", pi);

  return 0;
}
