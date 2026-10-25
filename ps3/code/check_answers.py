# Checks that stac_ps3.py gives correct answers.
# Idea: first give the code questions where we ALREADY KNOW the answer
# (our own Solar System). If it gets those right, we can trust it on STAC.

from stac_ps3 import *

passed = 0
failed = 0

def check(what, got, expected, allowed_error):
    global passed, failed
    if abs(got - expected) <= allowed_error:
        print("PASS  ", what, "-> got", "{:.5g}".format(got), "expected", "{:.5g}".format(expected))
        passed = passed + 1
    else:
        print("FAIL  ", what, "-> got", "{:.5g}".format(got), "expected", "{:.5g}".format(expected))
        failed = failed + 1


print("TEST 1: Kepler's law on real planets of our Sun")
print("(we know these distances already)")
check("Earth   (365.25 d)", orbit_distance(365.25, 1.0), 1.000, 0.005)
check("Mercury (87.97 d) ", orbit_distance(87.97, 1.0), 0.387, 0.005)
check("Mars    (686.98 d)", orbit_distance(686.98, 1.0), 1.524, 0.005)
check("Jupiter (4332.6 d)", orbit_distance(4332.6, 1.0), 5.203, 0.01)
print()

print("TEST 2: Planet size using Earth and Jupiter crossing the Sun")
# if Earth crossed the Sun, depth = (6371 / 696000)^2
earth_depth = (6371 / 696000) ** 2
km, earths = planet_size(1.0, earth_depth)
check("Earth size   ", earths, 1.00, 0.01)
# Jupiter radius is 69911 km = 10.97 Earths
jup_depth = (69911 / 696000) ** 2
km, earths = planet_size(1.0, jup_depth)
check("Jupiter size ", earths, 10.97, 0.05)
print()

print("TEST 3: Period finder on made-up data with a known answer")
p, first = find_period([2, 7, 12, 17, 22])
check("dips every 5 days ", p, 5.0, 0.001)
p, first = find_period([10, 40, 70])
check("dips every 30 days", p, 30.0, 0.001)
print()

print("TEST 4: Backtest - use our period to PREDICT the dips, compare with real data")
for i in range(3):
    p, first = find_period(dip_days[i])
    predicted = []
    for n in range(len(dip_days[i])):
        predicted.append(round(first + n * p))
    if predicted == dip_days[i]:
        print("PASS  ", star_names[i], "predicted", predicted, "= real", dip_days[i])
        passed = passed + 1
    else:
        print("FAIL  ", star_names[i], "predicted", predicted, "but real", dip_days[i])
        failed = failed + 1
# STAC-3: the next dip should be at day 180, but the star was normal there
p, first = find_period(dip_days[2])
print("       STAC-3 next dip predicted at day", round(first + 4 * p),
      "-> real data shows no dip there, dip at 170 instead (the odd one)")
print()

print("TEST 5: Reverse check - go backwards from the answer to the data")
for i in range(3):
    depth = find_depth(dip_flux[i])
    km, earths = planet_size(radius[i], depth)
    depth_back = (km / (radius[i] * R_SUN)) ** 2       # depth = (Rp / Rs)^2
    check(star_names[i] + " depth from radius", depth_back, depth, 0.000001)

    p, first = find_period(dip_days[i])
    a = orbit_distance(p, mass[i])
    p_back = math.sqrt(a ** 3 / mass[i]) * YEAR           # P = sqrt(a^3 / M)
    check(star_names[i] + " period from orbit ", p_back, p, 0.001)
print()

print("TEST 6: Check STAC-3 orbit a second way (Newton's formula in metres)")
G = 6.674e-11
M_SUN_KG = 1.989e30
P_seconds = 40 * 86400
a_metres = (G * 0.5 * M_SUN_KG * P_seconds ** 2 / (4 * math.pi ** 2)) ** (1 / 3)
a_km_newton = a_metres / 1000
a_km_ours = orbit_distance(40, 0.5) * AU
check("STAC-3 orbit (million km)", a_km_ours / 1e6, round(a_km_newton / 1e6, 2), 0.05)
print()

print("RESULT:", passed, "passed,", failed, "failed")
