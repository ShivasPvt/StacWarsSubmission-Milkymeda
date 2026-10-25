# Draws the brightness graph (light curve) of the three stars.

import matplotlib.pyplot as plt

# STAC-1: measured every day from day 0 to day 20
days1 = list(range(0, 21))
flux1 = []
for d in days1:
    if d in [3, 8, 12, 16, 20]:
        flux1.append(0.9970)
    else:
        flux1.append(1.0000)

# STAC-2: measured every 20 days
days2 = list(range(0, 201, 20))
flux2 = []
for d in days2:
    if d in [20, 100, 180]:
        flux2.append(0.9990)
    else:
        flux2.append(1.0000)

# STAC-3: measured every 10 days
days3 = list(range(0, 201, 10))
stac3_dips = {20: 0.9990, 60: 0.9992, 100: 0.9991, 140: 0.9993, 170: 0.9990}
flux3 = []
for d in days3:
    if d in stac3_dips:
        flux3.append(stac3_dips[d])
    else:
        flux3.append(1.0000)

# draw 3 graphs, one under the other
plt.figure(figsize=(8, 8))

plt.subplot(3, 1, 1)
plt.plot(days1, flux1, "o-")
plt.title("STAC-1 (period 4.2 days)")
plt.ylabel("Brightness")

plt.subplot(3, 1, 2)
plt.plot(days2, flux2, "o-", color="orange")
plt.title("STAC-2 (period 80 days)")
plt.ylabel("Brightness")

plt.subplot(3, 1, 3)
plt.plot(days3, flux3, "o-", color="green")
plt.title("STAC-3 (period 40 days, odd dip at day 170)")
plt.ylabel("Brightness")
plt.xlabel("Time (days)")

plt.tight_layout()
plt.savefig("light_curves.png")
plt.show()
