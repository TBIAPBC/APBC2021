

./Lorenzo360-KLetShuffle.py KLetShuffle-test100_k2.in -N 1 -k 2 > KLetShuffle-test100_k2_shuf.in
./Lorenzo360-KLetShuffle.py KLetShuffle-test100_k2.in -N 1 -k 2 --justStats > KLetShuffle-test100_k2.stats
./Lorenzo360-KLetShuffle.py KLetShuffle-test100_k2_shuf.in -N 1 -k 2 --justStats > KLetShuffle-test100_k2_shuf.stats
diff KLetShuffle-test100_k2.stats KLetShuffle-test100_k2_shuf.stats

./Lorenzo360-KLetShuffle.py KLetShuffle-test100_k3.in -N 1 -k 3 > KLetShuffle-test100_k3_shuf.in
./Lorenzo360-KLetShuffle.py KLetShuffle-test100_k3.in -N 1 -k 3 --justStats > KLetShuffle-test100_k3.stats
./Lorenzo360-KLetShuffle.py KLetShuffle-test100_k3_shuf.in -N 1 -k 3 --justStats > KLetShuffle-test100_k3_shuf.stats
diff KLetShuffle-test100_k3.stats KLetShuffle-test100_k3_shuf.stats


./Lorenzo360-MonoShuffle.py MonoShuffle-test100.in -N 1 >  MonoShuffle-test100_shuff.in
./Lorenzo360-RollingDice.py -N 0 --verbose MonoShuffle-test100_shuff.in >  MonoShuffle-test100_shuff.stats
./Lorenzo360-RollingDice.py -N 0 --verbose MonoShuffle-test100.in   >  MonoShuffle-test100.stats
diff MonoShuffle-test100_shuff.stats MonoShuffle-test100.stats


./Lorenzo360-MonoShuffle.py MonoShuffle-test30.in -N 1 >  MonoShuffle-test30_shuff.in
./Lorenzo360-RollingDice.py -N 0 --verbose MonoShuffle-test30_shuff.in >  MonoShuffle-test30_shuff.stats
./Lorenzo360-RollingDice.py -N 0 --verbose MonoShuffle-test30.in   >  MonoShuffle-test30.stats
diff MonoShuffle-test30_shuff.stats MonoShuffle-test30.stats


rm *stats *_shuf.in