import numpy as np
import csv
import io
import re
import matplotlib.pyplot as plt
import matplotlib


file = open("latest-results.csv", 'r')
csv_file = csv.DictReader(file)

res_binary = []
res_exact = []
rr = re.compile(r'_(\d+)')

for row in csv_file:
	d = dict(row)
	res = res_binary if d["rule"] == "binary" else res_exact

	profile = d["onions"]
	m = rr.search(profile)
	i = int(m.group(1))

	conf = d["alpaca_conf"]
	if conf.startswith("palpaca"):
		conf = rr.sub('', conf)

	if len(res) <= i:
		res.append({})
	res[i][conf] = float(row["leakage"])


data_binary = np.zeros((len(res_binary), 8))
data_exact = np.zeros((len(res_exact), 8))
data_comp_binary = np.zeros((len(res_binary), 2))
data_comp_exact = np.zeros((len(res_exact), 2))

for i in range(len(res_binary)):
	data_binary[i, 0] = res_binary[i]["noalpaca.conf"]
	data_binary[i, 1] = res_binary[i]["palpaca_optimal_binary.conf"]
	data_binary[i, 2] = res_binary[i]["dalpaca_1.conf"]
	data_binary[i, 3] = res_binary[i]["dalpaca_2.conf"]
	data_binary[i, 4] = res_binary[i]["dalpaca_3.conf"]
	data_binary[i, 5] = res_binary[i]["dalpaca_4.conf"]
	data_binary[i, 6] = res_binary[i]["palpaca_marginals.conf"]
	data_binary[i, 7] = res_binary[i]["palpaca_normal.conf"]

for i in range(len(res_exact)):
	data_exact[i, 0] = res_exact[i]["noalpaca.conf"]
	data_exact[i, 1] = res_exact[i]["palpaca_optimal_exact.conf"]
	data_exact[i, 2] = res_exact[i]["dalpaca_1.conf"]
	data_exact[i, 3] = res_exact[i]["dalpaca_2.conf"]
	data_exact[i, 4] = res_exact[i]["dalpaca_3.conf"]
	data_exact[i, 5] = res_exact[i]["dalpaca_4.conf"]
	data_exact[i, 6] = res_exact[i]["palpaca_marginals.conf"]
	data_exact[i, 7] = res_exact[i]["palpaca_normal.conf"]

for i in range(len(res_binary)):
	data_comp_binary[i, 0] = res_binary[i]["palpaca_optimal_exact.conf"]
	data_comp_binary[i, 1] = res_binary[i]["palpaca_optimal_binary.conf"]

for i in range(len(res_exact)):
	data_comp_exact[i, 0] = res_exact[i]["palpaca_optimal_exact.conf"]
	data_comp_exact[i, 1] = res_exact[i]["palpaca_optimal_binary.conf"]


def boxplot(data, title, labels, block=True):
	_fig1, ax = plt.subplots()
	ax.set_title(title)
	ax.boxplot(data)
	plt.xticks([x+1 for x in range(data.shape[1])], labels)
	plt.ylabel("Leakage")
	plt.show(block=block)


labels = ['No Noise', 'Optimal', 'DAlpaca1', 'DAlpaca2', 'DAlpaca3', 'DAlpaca4', 'Marginals', 'Normal']

boxplot(data_binary, 'Binary Adversary', labels, False)
boxplot(data_exact, 'Exact Adversary', labels, False)

labels = ['Exact-Opt', 'Binary-Opt']

boxplot(data_comp_binary, 'Binary Adversary', labels, False)
boxplot(data_comp_exact, 'Exact Adversary', labels, True)