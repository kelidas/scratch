 
#g++ -Wall -O2 rekurze.cpp -lgmp -lmpfr -o rekurze
g++ -o rekurze rekurze.cpp -DNDEBUG -g -ffast-math -lgmp -lmpfr -march=native -Wall -O3
#gcc -o rekurze rekurze.cpp -D NDEBUG -g -ffast-math -lgmp -lmpfr -march=native -Wall -O3