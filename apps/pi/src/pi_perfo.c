#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
  int i;
  long long count = 0;
  long long ncount = 0;
  long long n;
  double x, y, z, pi;

  scanf("%lld", &n);

#pragma omp parallel num_threads(NUM_THREADS) private(x, y, z) shared(count)
  {
    // Each thread needs its own seed
// unsigned int thread_seed = omp_get_thread_num();
	 unsigned int thread_seed = time(NULL);

#if PERFO == 0
#pragma omp approx for perfo(init, (int)(10 * DROP)) reduction(+ : count)
#elif PERFO == 1
#pragma omp approx for perfo(fini, (int)(10 * DROP)) reduction(+ : count)
#elif PERFO == 2
#pragma omp approx for perfo(large, (int)(10 * DROP))
#elif PERFO == 3
#pragma omp approx for perfo(small, (int)(10 * DROP)) reduction(+ : count)
#elif PERFO == 4
#pragma approx omp for perfo(default, (int)(1))  reduction(+ : count) reduction(+ : ncount)
#endif
    for (int i = 0; i < n; ++i) {
      // Generate random numbers using rand_r with the thread-specific seed
      x = ((double)rand_r(&thread_seed)) / RAND_MAX;
      y = ((double)rand_r(&thread_seed)) / RAND_MAX;

      z = x * x + y * y;

      if (z <= 1) {
        count++;
      }
      ncount++;
    }
  }

  pi = (double)count / ncount * 4;

  printf("%g\n", pi);

  return 0;
}
