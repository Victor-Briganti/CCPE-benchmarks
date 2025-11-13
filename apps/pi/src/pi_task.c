#include <omp.h>
#include <stdio.h>
#include <stdlib.h>

int main() {
  long long count = 0;
  long long ncount = 0;
  long long n;

  scanf("%lld", &n);

#pragma omp parallel num_threads(NUM_THREADS) shared(ncount, count)
  {
    double x, y, z;
    unsigned int thread_seed = omp_get_thread_num();

#pragma omp single
    {
#pragma omp approx taskloop drop((int)(10 * DROP)) reduction(+ : count)        \
    reduction(+ : ncount)
      {
        for (int i = 0; i < n; ++i) {
          x = (double)rand_r(&thread_seed) / RAND_MAX;
          y = (double)rand_r(&thread_seed) / RAND_MAX;

          z = x * x + y * y;

          if (z <= 1) {
            count++;
          }

          ncount++;
        }
      }
    }
  }

  double pi = (double)count / ncount * 4;
  printf("%g\n", pi);

  return 0;
}
