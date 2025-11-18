#include <iomanip>
#include <iostream>
#include <math.h>
#include <omp.h> // Include OpenMP header
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <vector>

#define DIVIDE 120.0
#define fptype float
#define PAD 256
#define LINESIZE 64

typedef struct OptionData_ {
  fptype s;        // spot price
  fptype strike;   // strike price
  fptype r;        // risk-free interest rate
  fptype divq;     // dividend rate
  fptype v;        // volatility
  fptype t;        // time to maturity
  char OptionType; // "P"=PUT, "C"=CALL
  fptype divs;     // dividend values (not used)
  fptype DGrefval; // Reference value
} OptionData;

OptionData *data;
fptype *prices;
int numOptions;

int *otype;
fptype *sptprice;
fptype *strike;
fptype *rate;
fptype *volatility;
fptype *otime;

#define inv_sqrt_2xPI 0.39894228040143270286

fptype CNDF(fptype InputX) {
  int sign;
  fptype OutputX, xInput, xNPrimeofX;
  fptype expValues, xK2, xK2_2, xK2_3, xK2_4, xK2_5;
  fptype xLocal, xLocal_1, xLocal_2, xLocal_3;

#pragma omp approx fastmath
  {
    if (InputX < 0.0) {
      InputX = -InputX;
      sign = 1;
    } else {
      sign = 0;
    }

    xInput = InputX;
    expValues = exp(-0.5f * InputX * InputX);
    xNPrimeofX = expValues * inv_sqrt_2xPI;

    xK2 = 0.2316419 * xInput;
    xK2 = 1.0 + xK2;
    xK2 = 1.0 / xK2;

    xK2_2 = xK2 * xK2;
    xK2_3 = xK2_2 * xK2;
    xK2_4 = xK2_3 * xK2;
    xK2_5 = xK2_4 * xK2;

    xLocal_1 = xK2 * 0.319381530;
    xLocal_2 = xK2_2 * (-0.356563782);
    xLocal_3 = xK2_3 * 1.781477937;
    xLocal_2 = xLocal_2 + xLocal_3;
    xLocal_3 = xK2_4 * (-1.821255978);
    xLocal_2 = xLocal_2 + xLocal_3;
    xLocal_3 = xK2_5 * 1.330274429;
    xLocal_2 = xLocal_2 + xLocal_3;

    xLocal_1 = xLocal_2 + xLocal_1;
    xLocal = xLocal_1 * xNPrimeofX;
    xLocal = 1.0 - xLocal;

    OutputX = (sign) ? 1.0 - xLocal : xLocal;
  }

  return OutputX;
}

fptype BlkSchlsEqEuroNoDiv(fptype sptprice, fptype strike, fptype rate,
                           fptype volatility, fptype time, int otype,
                           float timet, fptype *N1, fptype *N2) {
  fptype OptionPrice;
#pragma omp approx fastmath
  {
    fptype xRiskFreeRate = rate;
    fptype xVolatility = volatility;
    fptype xTime = time;
    fptype xSqrtTime = sqrt(xTime);

    fptype logValues = log(sptprice / strike);
    fptype xLogTerm = logValues;

    fptype xPowerTerm = 0.5f * xVolatility * xVolatility;
    fptype xD1 = (xRiskFreeRate + xPowerTerm) * xTime + xLogTerm;
    fptype xDen = xVolatility * xSqrtTime;
    xD1 = xD1 / xDen;
    fptype xD2 = xD1 - xDen;

    fptype d1 = xD1, d2 = xD2;

    fptype NofXd1 = CNDF(d1);
    fptype NofXd2 = CNDF(d2);

    *N1 = NofXd1;
    *N2 = NofXd2;

    fptype FutureValueX = strike * exp(-rate * time);

    if (otype == 0) {
      OptionPrice = (sptprice * NofXd1) - (FutureValueX * NofXd2);
    } else {
      OptionPrice =
          (FutureValueX * (1.0 - NofXd2)) - (sptprice * (1.0 - NofXd1));
    }
  }

  return OptionPrice;
}

int main(int argc, char **argv) {
  FILE *file;
  int i;
  fptype *buffer;
  int *buffer2;
  int rv;

  file = stdin;
  rv = fscanf(file, "%i", &numOptions);
  if (rv != 1) {
    std::cerr << "ERROR: Unable to read number of options.\n";
    exit(1);
  }

  data = (OptionData *)malloc(numOptions * sizeof(OptionData));
  prices = (fptype *)malloc(numOptions * sizeof(fptype));

  for (int loopnum = 0; loopnum < numOptions; ++loopnum) {
    rv = fscanf(file, "%f %f %f %f %f %f %c %f %f", &data[loopnum].s,
                &data[loopnum].strike, &data[loopnum].r, &data[loopnum].divq,
                &data[loopnum].v, &data[loopnum].t, &data[loopnum].OptionType,
                &data[loopnum].divs, &data[loopnum].DGrefval);
    if (rv != 9) {
      std::cerr << "ERROR: Unable to read option data.\n";
      exit(1);
    }
  }

  buffer = (fptype *)malloc(5 * numOptions * sizeof(fptype) + PAD);
  sptprice = (fptype *)(((unsigned long long)buffer + PAD) & ~(LINESIZE - 1));
  strike = sptprice + numOptions;
  rate = strike + numOptions;
  volatility = rate + numOptions;
  otime = volatility + numOptions;

  buffer2 = (int *)malloc(numOptions * sizeof(fptype) + PAD);
  otype = (int *)(((unsigned long long)buffer2 + PAD) & ~(LINESIZE - 1));

  for (i = 0; i < numOptions; i++) {
    otype[i] = (data[i].OptionType == 'P') ? 1 : 0;
    sptprice[i] = data[i].s / DIVIDE;
    strike[i] = data[i].strike / DIVIDE;
    rate[i] = data[i].r;
    volatility[i] = data[i].v;
    otime[i] = data[i].t;
  }

#pragma omp parallel for num_threads(NUM_THREADS) schedule(static)
  for (i = 0; i < numOptions; i++) {
    fptype N1, N2;
    prices[i] =
        BlkSchlsEqEuroNoDiv(sptprice[i], strike[i], rate[i], volatility[i],
                            otime[i], otype[i], 0, &N1, &N2);
  }

  // Output results to stdout
  for (i = 0; i < numOptions; i++) {
    fprintf(stdout, "%.18f\n", prices[i]);
  }

  free(data);
  free(prices);
  free(buffer);
  free(buffer2);
  return 0;
}
