#!/usr/bin/env sh

set -e

x=0

programs=("mandelbrot")
names=("default" "memo" "task" "fast" "perfo_init" "perfo_fini" "perfo_large" "perfo_small" "perfo_default")
sequence=(1 2 4 8)

for program in "${programs[@]}"; do
  for i in "${sequence[@]}"; do
    for name in "${names[@]}"; do
      if [[ "$name" != "default" ]] && [[ "$name" != "memo" ]] && [[ "$name" != "fast" ]]; then

        for j in $(seq 0 4); do
          make -B NUM_THREADS=$i DROP=0.$((j + 1)) $name -C $program/
          bash $program/run $name $i 0.$((j + 1))
        done

      elif [[ "$name" == "memo" ]]; then
        
        for j in $(seq 0 4); do
          make -B NUM_THREADS=$i THRESHOLD=$(((j + 1) * 10)) $name -C $program/
          bash $program/run $name $i $(((j + 1) * 10))
        done

      else
        make -B NUM_THREADS=$i $name -C $program/
        bash $program/run $name $i
      fi

      make clean -C $program/
    done
  done
done
