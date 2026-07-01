import math

#Modeled using the ISA Standard Atmosphere 1976
def get_atmospheric_temperature(h):
    if h<=11019: T = 15 - 6.5*(h/1000)
    elif 11019<h<=20063: T = -56.5
    elif 20063<h<=32162: T = -56.5 + 1*(h/1000)
    elif 32162<h<=47350: T = -44.5 + 2.5*(h/1000)
    elif 47350<h<=51412: T = -2.5
    elif 51412<h<=71802: T = -2.5 - 2.8*(h/1000)
    elif 71802<h<=86000: T = -58.5 - 2*(h/1000)
    else: T = -92.5
    return T

#Modeled using the Earth Atmosphere Model from the Glenn Research Centre
def get_atmospheric_pressure(h):
    T = get_atmospheric_temperature(h)
    if h>25000:
        pressure = 2.488 * ((T+273.1)/216.6)**-11.388
        return pressure
    elif 11000<=h<25000:
        pressure = 22.65*math.e**(1.73-0.000157*h)
        return pressure
    elif h<11000:
        pressure = 101.29*((T+273.1)/288.08)**5.256
        return pressure
    else:
        print("Temperature calculation error")

#Also from the Glenn Research Centre
def get_air_density(h):
    p = get_atmospheric_pressure(h)
    T = get_atmospheric_temperature(h)
    density = p / (0.2869 * (T+273.1))
    return density

