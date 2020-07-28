set -x
for i in {0..99}; do sudo wf/bin/python alpaca-conf-eval.py -ac alpaca_config/conf/dalpaca_1.conf -cl exact -r alpaca_config/priors/pi_${i}.csv; done
for i in {0..99}; do sudo wf/bin/python alpaca-conf-eval.py -ac alpaca_config/conf/dalpaca_1.conf -cl binary -r alpaca_config/priors/pi_${i}.csv; done
mv results.csv dalpaca_1_results.csv

for i in {0..99}; do sudo wf/bin/python alpaca-conf-eval.py -ac alpaca_config/conf/dalpaca_2.conf -cl exact -r alpaca_config/priors/pi_${i}.csv; done
for i in {0..99}; do sudo wf/bin/python alpaca-conf-eval.py -ac alpaca_config/conf/dalpaca_2.conf -cl binary -r alpaca_config/priors/pi_${i}.csv; done
mv results.csv dalpaca_2_results.csv

for i in {0..99}; do sudo wf/bin/python alpaca-conf-eval.py -ac alpaca_config/conf/dalpaca_3.conf -cl exact -r alpaca_config/priors/pi_${i}.csv; done
for i in {0..99}; do sudo wf/bin/python alpaca-conf-eval.py -ac alpaca_config/conf/dalpaca_3.conf -cl binary -r alpaca_config/priors/pi_${i}.csv; done
mv results.csv dalpaca_3_results.csv

for i in {0..99}; do sudo wf/bin/python alpaca-conf-eval.py -ac alpaca_config/conf/dalpaca_4.conf -cl exact -r alpaca_config/priors/pi_${i}.csv; done
for i in {0..99}; do sudo wf/bin/python alpaca-conf-eval.py -ac alpaca_config/conf/dalpaca_4.conf -cl binary -r alpaca_config/priors/pi_${i}.csv; done
mv results.csv dalpaca_4_results.csv

for i in {0..99}; do sudo wf/bin/python alpaca-conf-eval.py -ac alpaca_config/conf/big/conf/palpaca_optimal_exact_${i}.conf -cl exact -r alpaca_config/priors/pi_${i}.csv; done
for i in {0..99}; do sudo wf/bin/python alpaca-conf-eval.py -ac alpaca_config/conf/big/conf/palpaca_optimal_exact_${i}.conf -cl binary -r alpaca_config/priors/pi_${i}.csv; done
mv results.csv palpaca_optimal_exact_results.csv

for i in {0..99}; do sudo wf/bin/python alpaca-conf-eval.py -ac alpaca_config/conf/big/conf/palpaca_optimal_binary_${i}.conf -cl exact -r alpaca_config/priors/pi_${i}.csv; done
for i in {0..99}; do sudo wf/bin/python alpaca-conf-eval.py -ac alpaca_config/conf/big/conf/palpaca_optimal_binary_${i}.conf -cl binary -r alpaca_config/priors/pi_${i}.csv; done
mv results.csv palpaca_optimal_binary_results.csv

for i in {0..99}; do sudo wf/bin/python alpaca-conf-eval.py -ac alpaca_config/conf/palpaca_marginals.conf -cl exact -r alpaca_config/priors/pi_${i}.csv; done
for i in {0..99}; do sudo wf/bin/python alpaca-conf-eval.py -ac alpaca_config/conf/palpaca_marginals.conf -cl binary -r alpaca_config/priors/pi_${i}.csv; done
mv results.csv palpaca_marginals_results.csv

for i in {0..99}; do sudo wf/bin/python alpaca-conf-eval.py -ac alpaca_config/conf/palpaca_normal.conf -cl exact -r alpaca_config/priors/pi_${i}.csv; done
for i in {0..99}; do sudo wf/bin/python alpaca-conf-eval.py -ac alpaca_config/conf/palpaca_normal.conf -cl binary -r alpaca_config/priors/pi_${i}.csv; done
mv results.csv palpaca_normal_results.csv

for i in {0..99}; do sudo wf/bin/python alpaca-conf-eval.py -ac alpaca_config/conf/noalpaca.conf -cl exact -r alpaca_config/priors/pi_${i}.csv; done
for i in {0..99}; do sudo wf/bin/python alpaca-conf-eval.py -ac alpaca_config/conf/noalpaca.conf -cl binary -r alpaca_config/priors/pi_${i}.csv; done
mv results.csv noalpaca_results.csv