CC=/home/aJoaoBriganti/bin/clang++ --gcc-install-dir=/usr/lib/gcc/x86_64-linux-gnu/12
LD=/home/aJoaoBriganti/bin/clang++ --gcc-install-dir=/usr/lib/gcc/x86_64-linux-gnu/12

NUM_THREADS ?= 1
DROP ?= 0.5
THRESHOLD ?= 10

CFLAGS  := -O3 -march=native -DNUM_THREADS=$(NUM_THREADS) -DDROP=$(DROP) -DTHRESHOLD=$(THRESHOLD) -fopenmp -std=c++11 -stdlib=libstdc++ -I/home/aJoaoBriganti/approx-llvm/build/projects/openmp/runtime/src/
LFLAGS  :=
HEADERS := src
INCLUDE :=
LIB     := -stdlib=libstdc++ -fopenmp -L/usr/lib/gcc/x86_64-linux-gnu/12 -I/home/aJoaoBriganti/approx-llvm/build/projects/openmp/runtime/src/ -lomp -L/home/aJoaoBriganti/approx-llvm/build/lib -Wl,-rpath,/home/aJoaoBriganti/approx-llvm/build/lib

TARGET_DEFAULT = blackscholes_default.a
EXE_DEFAULT    = bin/$(TARGET_DEFAULT)

SRC_DEFAULT_FILES := blackscholes.cpp
OBJ_DEFAULT_FILES := $(addprefix obj/,$(notdir $(SRC_DEFAULT_FILES:.cpp=.default.o)))

TARGET_TASK := blackscholes_task.a
EXE_TASK    := bin/$(TARGET_TASK)

SRC_TASK_FILES := blackscholes_task.cpp
OBJ_TASK_FILES := $(addprefix obj/,$(notdir $(SRC_TASK_FILES:.cpp=.task.o)))

TARGET_MEMO := blackscholes_memo.a
EXE_MEMO    := bin/$(TARGET_MEMO)

SRC_MEMO_FILES := blackscholes_memo.cpp
OBJ_MEMO_FILES := $(addprefix obj/,$(notdir $(SRC_MEMO_FILES:.cpp=.memo.o)))

TARGET_FAST := blackscholes_fast.a
EXE_FAST    := bin/$(TARGET_FAST)

SRC_FAST_FILES := blackscholes_fast.cpp
OBJ_FAST_FILES := $(addprefix obj/,$(notdir $(SRC_FAST_FILES:.cpp=.fast.o)))

TARGET_PERFO 	:= blackscholes_perfo
EXE_PERFO_INIT  := bin/$(TARGET_PERFO)_init.a
EXE_PERFO_FINI  := bin/$(TARGET_PERFO)_fini.a
EXE_PERFO_SMALL := bin/$(TARGET_PERFO)_small.a
EXE_PERFO_LARGE := bin/$(TARGET_PERFO)_large.a
EXE_PERFO_DEFAULT := bin/$(TARGET_PERFO)_default.a

SRC_PERFO_FILES := blackscholes_perfo.cpp
OBJ_PERFO_INIT_FILES := $(addprefix obj/,$(notdir $(SRC_PERFO_FILES:.cpp=.perfo_init.o)))
OBJ_PERFO_FINI_FILES := $(addprefix obj/,$(notdir $(SRC_PERFO_FILES:.cpp=.perfo_fini.o)))
OBJ_PERFO_SMALL_FILES := $(addprefix obj/,$(notdir $(SRC_PERFO_FILES:.cpp=.perfo_small.o)))
OBJ_PERFO_LARGE_FILES := $(addprefix obj/,$(notdir $(SRC_PERFO_FILES:.cpp=.perfo_large.o)))
OBJ_PERFO_DEFAULT_FILES := $(addprefix obj/,$(notdir $(SRC_PERFO_FILES:.cpp=.perfo_default.o)))

.PHONY: all default task memo fast perfo_fini perfo_init perfo_large perfo_small perfo_default clean

all: default task memo fast perfo_fini perfo_init perfo_large perfo_small perfo_default

default: DIR $(EXE_DEFAULT)

task: DIR $(EXE_TASK)

memo: DIR $(EXE_MEMO)

fast: DIR $(EXE_FAST)

perfo_fini: DIR $(EXE_PERFO_FINI)

perfo_init: DIR $(EXE_PERFO_INIT)

perfo_large: DIR $(EXE_PERFO_LARGE)

perfo_small: DIR $(EXE_PERFO_SMALL)

perfo_default: DIR $(EXE_PERFO_DEFAULT)

DIR:
	@mkdir bin -p
	@mkdir obj -p

$(EXE_DEFAULT): $(OBJ_DEFAULT_FILES)
	$(LD) $^ $(LIB) $(LFLAGS) -o $@

obj/%.default.o: src/%.cpp
	$(CC) $(CFLAGS) $(INCLUDE) -c $< -o $@

$(EXE_TASK): $(OBJ_TASK_FILES)
	$(LD) $^ $(LIB) $(LFLAGS) -o $@

obj/%.task.o: src/%.cpp
	$(CC) $(CFLAGS) $(INCLUDE) -c $< -o $@

$(EXE_MEMO): $(OBJ_MEMO_FILES)
	$(LD) $^ $(LIB) $(LFLAGS) -o $@

obj/%.memo.o: src/%.cpp
	$(CC) $(CFLAGS) $(INCLUDE) -c $< -o $@

$(EXE_FAST): $(OBJ_FAST_FILES)
	$(LD) $^ $(LIB) $(LFLAGS) -o $@

obj/%.fast.o: src/%.cpp
	$(CC) $(CFLAGS) $(INCLUDE) -c $< -o $@

$(EXE_PERFO_INIT): $(OBJ_PERFO_INIT_FILES)
	$(LD) $^ $(LIB) $(LFLAGS) -o $@

obj/%.perfo_init.o: src/%.cpp
	$(CC) $(CFLAGS) -DPERFO=0 $(INCLUDE) -c $< -o $@

$(EXE_PERFO_FINI): $(OBJ_PERFO_FINI_FILES)
	$(LD) $^ $(LIB) $(LFLAGS) -o $@

obj/%.perfo_fini.o: src/%.cpp
	$(CC) $(CFLAGS) -DPERFO=1 $(INCLUDE) -c $< -o $@

$(EXE_PERFO_SMALL): $(OBJ_PERFO_SMALL_FILES)
	$(LD) $^ $(LIB) $(LFLAGS) -o $@

obj/%.perfo_small.o: src/%.cpp
	$(CC) $(CFLAGS) -DPERFO=2 $(INCLUDE) -c $< -o $@

$(EXE_PERFO_LARGE): $(OBJ_PERFO_LARGE_FILES)
	$(LD) $^ $(LIB) $(LFLAGS) -o $@

obj/%.perfo_large.o: src/%.cpp
	$(CC) $(CFLAGS) -DPERFO=3 $(INCLUDE) -c $< -o $@

$(EXE_PERFO_DEFAULT): $(OBJ_PERFO_DEFAULT_FILES)
	$(LD) $^ $(LIB) $(LFLAGS) -o $@

obj/%.perfo_default.o: src/%.cpp
	$(CC) $(CFLAGS) -DPERFO=4 $(INCLUDE) -c $< -o $@

clean:
	@rm -rf *.o
	@rm -rf *.d
	@rm -rf *.out
	@rm -rf bin
	@rm -rf obj
