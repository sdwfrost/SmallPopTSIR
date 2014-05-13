# Generate figures for paper

# Plots to generate :
#	Time-series / Predictions - alpha
#	Reporting rates
#	Periodicity
#	Predictions
#	Size

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
import matplotlib as mpl
import seaborn
#mpl.rcParams['text.latex.preamble'] = [r'\usepackage[utf8]{fontenc}'] 
mpl.rcParams['text.latex.unicode'] = True 
mpl.rcParams['text.usetex'] = True   

colours = seaborn.color_palette("deep", 8)
scalefactor = 20.
xdim = 1.1
ydim = 1.


name = []
t = []
ts = []
pred = []
rho = []
r = []
rup = []
rdn = []
sizex = []
sizey = []
sizeerrx = []
sizeerry = []
sizeerre = []
r2 = []
p = []
pearson = []
pearsonzero = []
sbar = []
sn = []
Z = []
grad = []
ciu = []
cid = []







for file in os.listdir("figures/") :
	if file.endswith(".json") :
		data = pd.read_json("figures/%s" % file)
		name.append(" %s" % file.split(".json")[0])
		t.append(data["t"].values[0])
		ts.append(data["ts"].values[0])
		pred.append(data["pred"].values[0])
		rho.append(data["rho"].values[0])
		r.append(np.array(data["r"].values[0]))
		rup.append(np.array(data["rup"].values[0]))
		rdn.append(np.array(data["rdn"].values[0]))
		sizex.append(data["sizex"].values[0])
		sizey.append(data["sizey"].values[0])
		sizeerrx.append(data["sizeerrx"].values[0])
		sizeerry.append(data["sizeerry"].values[0])
		sizeerre.append(data["sizeerre"].values[0])
		r2.append(data["r2"].values[0])
		p.append(data["p"].values[0])
		pearson.append(data["pearson"].values[0])
		pearsonzero.append(data["pearsonzero"].values[0])
		sbar.append(data["sbar"].values[0])
		grad.append(data["grad"].values[0])
		sn.append(data["sn"].values[0])
		ciu.append(data["predciu"].values[0])
		cid.append(data["predcid"].values[0])



"""
plt.figure(figsize=(xdim*210/scalefactor, ydim*297/scalefactor))
##plt.suptitle("Reported Incidence and Inferred Reporting Rate", fontsize=20, y=.999)
for i in range(len(name)) :

	ax1 = plt.subplot(len(name), 1, i+1)
	#ax1.plot(t[i], ts[i], lw=2)
	#ax1.plot(t[i], ts[i], lw=2, c=colours[2], alpha=0.6)
	ax1.plot(t[i], ts[i], lw=2, c=colours[0])
	ax1.set_title(u"%s" % name[i].decode("utf-8"), fontsize=16, loc="left")
	ax1.tick_params(labelsize=16)
	ax1.locator_params(nbins=5, axis="y")
	
	
	ax2 = ax1.twinx()
	ax2.plot(t[i], rho[i], lw=3, c=colours[2], alpha=0.6)
	ax2.grid(False)
	ax2.tick_params(labelsize=16)
	ax2.locator_params(nbins=5, axis="y")
	

	ax1.set_xlim([np.min(t[i]), np.max(t[i])])
	ax2.set_xlim([np.min(t[i]), np.max(t[i])])

	if i == 0 :
		ax1.legend(["Incidence", "Reporting Rate"], loc=2)

plt.figtext(.01, 0.5, r"Reported Incidence, $C$", ha="center", va="center", rotation="vertical", fontsize=16)
plt.figtext(.99, 0.5, r"Reporting Rate, $1/\rho$", ha="center", va="center", rotation="vertical", fontsize=16)
plt.figtext(.5, 0.01, "Time", ha="center", va="center", fontsize=16)
plt.tight_layout(rect=(0.01, 0.015, .98, 1))
plt.savefig("figures/0_incidence.pdf")
plt.close()








fig, axs = plt.subplots(3, 2, sharex=True, figsize=(xdim*210/scalefactor, ydim*297/scalefactor))
##plt.suptitle("Seasonality", fontsize=20, y=.999)
for i in range(len(name)) :
	axs[i % 3][np.floor(i/3)].plot(r[i] * sbar[i], lw=2)
	axs[i % 3][np.floor(i/3)].fill_between(range(24), rup[i] * sbar[i], rdn[i] * sbar[i], color=colours[0], alpha=0.3)
	axs[i % 3][np.floor(i/3)].set_title(name[i], fontsize=16, loc="left")
	axs[i % 3][np.floor(i/3)].set_xlim([0, 23])
	axs[i % 3][np.floor(i/3)].set_xticks(range(0, 23, 4))
	axs[i % 3][np.floor(i/3)].tick_params(labelsize=16)
	axs[i % 3][np.floor(i/3)].locator_params(nbins=5, axis="y")
plt.figtext(.5, 0.01, "Period", ha="center", va="center", fontsize=16)
plt.figtext(.01, 0.5, r"Seasonality, $r \bar{S}$", ha="center", va="center", rotation="vertical", fontsize=16)
plt.tight_layout(rect=(0.015, 0.015, .99, 1)) # (left, bottom, right, top) 
plt.savefig("figures/1_seasonality.pdf")
plt.close()







fig, axs = plt.subplots(len(name), 1, figsize=(xdim*210/scalefactor, ydim*297/scalefactor))
##plt.suptitle("Predicted Cases", fontsize=20, y=.999)
for i in range(len(name)) :
	axs[i].plot(t[i], ts[i], lw=2, c=colours[0])
	axs[i].plot(t[i], pred[i], lw=1, c=colours[2], alpha=1)
	axs[i].fill_between(t[i], cid[i], ciu[i], color=colours[2], alpha=0.3)
	axs[i].tick_params(labelsize=16)
	axs[i].locator_params(nbins=5, axis="y")
	axs[i].set_title(u"%s. $R^2$ = %.03f, zero-corrected $R^2$ = %.03f" % (name[i].decode("utf-8"), pearson[i], pearsonzero[i]), fontsize=16, loc="left")
	axs[i].set_xlim([np.min(t[i]), np.max(t[i])])
	if i == 0 :
		axs[i].legend([r"Observed Incidence", "Predicted Incidence"], loc=2)

plt.figtext(.01, 0.5, r"Incidence, $\rho\,C$", ha="center", va="center", rotation="vertical", fontsize=16)
plt.figtext(.5, 0.01, "Time", ha="center", va="center", fontsize=16)
plt.tight_layout(rect=(0.01, 0.015, .99, 1))
plt.savefig("figures/2_predictions.pdf")
plt.close()








fig, axs = plt.subplots(len(name), 1, figsize=(xdim*210/scalefactor, ydim*297/scalefactor))
#fig.suptitle("Predicted Epidemic Sizes", fontsize=20, y=.999)
for i in range(len(name)) :
	axs[i].errorbar(sizeerrx[i], sizeerry[i], yerr = sizeerre[i], fmt="o", ms=8, c=colours[0])
	axs[i].plot(sizex[i], sizey[i], lw=2, c=colours[2])
	axs[i].tick_params(labelsize=16)
	axs[i].locator_params(nbins=5, axis="y")
	axs[i].set_xlim([0, np.max(sizex[i])*1.02])
	axs[i].set_title(u"%s. $R^2$ = %.2f, slope = %.02f" % (name[i].decode("utf-8"), r2[i], grad[i]), fontsize=16, loc="left")

plt.figtext(.01, 0.5, "Simulated Epidemic Size", ha="center", va="center", rotation="vertical", fontsize=16)
plt.figtext(.5, 0.01, "Actual Epidemic Size", ha="center", va="center", fontsize=16)
plt.tight_layout(rect=(0.01, 0.015, .99, 1))
plt.savefig("figures/3_sizes.pdf")
plt.close()











plt.figure(figsize=(xdim*210/scalefactor, ydim*297/scalefactor))
for i in range(len(name)) :

	T = np.array(ts[i]) if len(ts[i]) % 2 == 0 else np.array(ts[i][:-1])
	T = T.reshape(len(T)/2, 2).sum(axis=1)

	num = np.zeros(12)
	count = np.zeros(12)

	for j, TS in enumerate(ts[i]) :
		if TS > 0.5 :
			num[j % 12] += 1
		count[j % 12] += 1

	plt.subplot(len(name), 1, i+1)
	plt.plot(num / count.astype(float), lw=2)
	plt.tick_params(labelsize=16)
	plt.locator_params(nbins=5, axis="y")

plt.figtext(.01, 0.5, "Fraction of Month with Cases", ha="center", va="center", rotation="vertical", fontsize=16)
plt.figtext(.5, 0.01, "Month", ha="center", va="center", fontsize=16)
plt.tight_layout(rect=(0.02, 0.015, .99, 1))
plt.savefig("figures/5_infectiontiming.pdf")
plt.close()

"""













fig, axs = plt.subplots(3, 2, sharex=True, figsize=(xdim*210/scalefactor, ydim*115/scalefactor))
##plt.suptitle("Seasonality", fontsize=20, y=.999)
for i in range(len(name)) :
	axs[i % 3][np.floor(i/3)].plot(t[i], ts[i], lw=2)
	axs[i % 3][np.floor(i/3)].set_title(u"%s" % name[i].decode("utf-8"), fontsize=16, loc="left")
	axs[i % 3][np.floor(i/3)].set_xlim([1900, 1965])
	#axs[i % 3][np.floor(i/3)].set_xticks(range(0, 23, 4))
	axs[i % 3][np.floor(i/3)].tick_params(labelsize=14)
	axs[i % 3][np.floor(i/3)].locator_params(nbins=5, axis="y")

	a = axs[i%3][np.floor(i/3)].twinx()
	a.plot(t[i], rho[i], lw=3, c=colours[2], alpha=0.6)
	a.grid(False)
	a.tick_params(labelsize=14)
	a.locator_params(nbins=5, axis="y")
	a.set_xlim([1900, 1965])

plt.figtext(.015, 0.5, r"Reported Incidence", ha="center", va="center", rotation="vertical", fontsize=16)
plt.figtext(.5, 0.05, "Time", ha="center", va="center", fontsize=16)
plt.tight_layout(rect=(0.02, 0.05, .99, 1)) # (left, bottom, right, top) 
plt.savefig("figures/6_fortalk.pdf")
plt.close()








fig, axs = plt.subplots(3, 2, sharex=True, figsize=(xdim*210/scalefactor, ydim*115/scalefactor))
##plt.suptitle("Seasonality", fontsize=20, y=.999)
for i in range(len(name)) :
	axs[i % 3][np.floor(i/3)].plot(r[i] * sbar[i], lw=2)
	axs[i % 3][np.floor(i/3)].fill_between(range(24), rup[i] * sbar[i], rdn[i] * sbar[i], color=colours[0], alpha=0.3)
	axs[i % 3][np.floor(i/3)].set_title(name[i], fontsize=16, loc="left")
	axs[i % 3][np.floor(i/3)].set_xlim([0, 23])
	axs[i % 3][np.floor(i/3)].set_xticks(range(0, 23, 4))
	axs[i % 3][np.floor(i/3)].tick_params(labelsize=16)
	axs[i % 3][np.floor(i/3)].locator_params(nbins=5, axis="y")
plt.figtext(.5, 0.05, "Period", ha="center", va="center", fontsize=16)
plt.figtext(.01, 0.5, r"Seasonality, $r \bar{S}$", ha="center", va="center", rotation="vertical", fontsize=16)
plt.tight_layout(rect=(0.02, 0.05, .99, 1)) # (left, bottom, right, top) 
plt.savefig("figures/7_fortalk.pdf")
plt.close()










fig, axs = plt.subplots(3, 2, sharex=True, figsize=(xdim*210/scalefactor, ydim*115/scalefactor))
##plt.suptitle("Predicted Cases", fontsize=20, y=.999)
for i in range(len(name)) :
	axs[i % 3][np.floor(i/3)].plot(t[i], ts[i], lw=2, c=colours[0])
	axs[i % 3][np.floor(i/3)].plot(t[i], pred[i], lw=1, c=colours[2], alpha=1)
	axs[i % 3][np.floor(i/3)].fill_between(t[i], cid[i], ciu[i], color=colours[2], alpha=0.3)
	axs[i % 3][np.floor(i/3)].tick_params(labelsize=16)
	axs[i % 3][np.floor(i/3)].locator_params(nbins=5, axis="y")
	axs[i % 3][np.floor(i/3)].set_title(u"%s. $R^2$ = %.03f" % (name[i].decode("utf-8"), pearson[i]), fontsize=16, loc="left")
	axs[i % 3][np.floor(i/3)].set_xlim([1900, 1965])
	axs[i % 3][np.floor(i/3)].set_ylim([0, max(np.max(ts[i]), np.max(pred[i]))])
	if i == 0 and np.floor(i/3) == 0 :
		axs[i % 3][np.floor(i/3)].legend([r"Observed Incidence", "Predicted Incidence"], loc=2)

plt.figtext(.015, 0.5, r"Incidence, $\rho_t\,C_t$", ha="center", va="center", rotation="vertical", fontsize=16)
plt.figtext(.5, 0.02, "Time", ha="center", va="center", fontsize=16)
plt.tight_layout(rect=(0.015, 0.05, .99, 1))
plt.savefig("figures/8_fortalk.pdf")
plt.close()











fig, axs = plt.subplots(3, 2, figsize=(xdim*210/scalefactor, ydim*115/scalefactor))
#fig.suptitle("Predicted Epidemic Sizes", fontsize=20, y=.999)
for i in range(len(name)) :
	axs[i % 3][np.floor(i/3)].errorbar(sizeerrx[i], sizeerry[i], yerr = sizeerre[i], fmt="o", ms=8, c=colours[0])
	axs[i % 3][np.floor(i/3)].plot(sizex[i], sizey[i], lw=2, c=colours[2])
	axs[i % 3][np.floor(i/3)].tick_params(labelsize=16)
	axs[i % 3][np.floor(i/3)].locator_params(nbins=5, axis="y")
	axs[i % 3][np.floor(i/3)].set_xlim([0, np.max(sizex[i])*1.02])
	axs[i % 3][np.floor(i/3)].set_ylim([0, max(np.max(sizey[i]), np.max(sizeerry[i]))*1.1])
	axs[i % 3][np.floor(i/3)].set_title(u"%s. $R^2$ = %.2f, slope = %.02f" % (name[i].decode("utf-8"), r2[i], grad[i]), fontsize=16, loc="left")

plt.figtext(.015, 0.5, "Simulated Epidemic Size", ha="center", va="center", rotation="vertical", fontsize=16)
plt.figtext(.5, 0.02, "Actual Epidemic Size", ha="center", va="center", fontsize=16)
plt.tight_layout(rect=(0.02, 0.035, .99, 1))
plt.savefig("figures/9_fortalk.pdf")
plt.close()


