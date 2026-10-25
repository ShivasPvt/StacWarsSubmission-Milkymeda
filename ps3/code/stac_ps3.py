import math
# STEP 1: Putting values

R_SUN = 696000      # solar radius
R_EARTH = 6371      # earth raduis
AU = 1.496e8        # 1 AU 
YEAR = 365.25       # days in 1 year

star_names = ["STAC-1", "STAC-2", "STAC-3"]
mass       = [1.0, 0.8, 0.5]      
radius     = [1.0, 0.8, 0.5]      
luminosity = [1.0, 0.4, 0.08]     

# days when the star got dimmer 
dip_days = [
    [3, 8, 12, 16, 20],           # STAC-1
    [20, 100, 180],               # STAC-2
    [20, 60, 100, 140],           # STAC-3 (not adding 170)
]
dip_flux = [
    [0.9970, 0.9970, 0.9970, 0.9970, 0.9970],
    [0.9990, 0.9990, 0.9990],
    [0.9990, 0.9992, 0.9991, 0.9993],
]

# STEP 2: Find the period

def find_period(days):
    n = len(days)
    numbers = list(range(n))  
    avg_num = sum(numbers) / n
    avg_day = sum(days) / n

    top = 0
    bottom = 0
    for i in range(n):
        top = top + (numbers[i] - avg_num) * (days[i] - avg_day)
        bottom = bottom + (numbers[i] - avg_num) ** 2

    period = top / bottom
    first = avg_day - period * avg_num
    return period, first


# STEP 3: Find the transit depth



def find_depth(fluxes):
    avg_flux = sum(fluxes) / len(fluxes)
    depth = (1.0 - avg_flux) / 1.0
    return depth

# STEP 4: Find the planet size

def planet_size(star_radius, depth):
    star_km = star_radius * R_SUN
    planet_km = star_km * math.sqrt(depth)
    planet_earths = planet_km / R_EARTH
    return planet_km, planet_earths


def planet_type(earths):
    if earths < 1.25:
        return "Earth-size"
    elif earths < 2:
        return "Super-Earth"
    elif earths < 6:
        return "Neptune-size"
    else:
        return "Jupiter-size"

# STEP 5: Find the orbit (Keplers third law)

def orbit_distance(period_days, star_mass):
    period_years = period_days / YEAR
    a = (period_years ** 2 * star_mass) ** (1 / 3)
    return a

# STEP 6: Habitable zone and starlight

def habitable_zone(lum):
    return math.sqrt(lum)


def starlight(lum, a):
    return lum / (a ** 2)


# STEP 7: Run everything ad print the answers

def main():
    best_star = ""
    best_score = 0

    for i in range(3):
        name = star_names[i]
        print("========", name, "========")

        period, first = find_period(dip_days[i])
        print("Dip days:", dip_days[i])
        print("Period =", round(period, 2), "days")

        depth = find_depth(dip_flux[i])
        print("Depth =", round(depth, 5))

        km, earths = planet_size(radius[i], depth)
        print("Planet radius =", round(km), "km =", round(earths, 2), "Earth radii")
        print("Planet type =", planet_type(earths))

        a = orbit_distance(period, mass[i])
        print("Orbit =", round(a, 3), "AU =", "{:.2e}".format(a * AU), "km")

        hz = habitable_zone(luminosity[i])
        light = starlight(luminosity[i], a)
        print("Habitable zone =", round(hz, 3), "AU")
        print("Planet is at", round(a / hz * 100), "% of the habitable zone distance")
        print("Starlight =", round(light, 1), "times what Earth gets")

        if a / hz > best_score and earths < 2:
            best_score = a / hz
            best_star = name
        print()

    print("Most promising planet:", best_star, "b")
    print("Reason: smallest (rocky), least starlight, closest to its habitable zone.")


# run main() onlly when this file is started directl
# so check_answers.py can borrow the functions without printing all this
if __name__ == "__main__":
    main()
