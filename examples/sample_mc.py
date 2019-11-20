#
# Example for Ragagnin et al. (2020)
#
# To make this script work you need to import hydro_mc,
# to do so, copy the hydro_mc.py file in the same folder of this file (or in your repository)
#
# The following python script get's the 200c concetration of a halo with M_200c=1e14Msun halo at a=0.9,
# with a cosmology (omega_m = 0.2, omega_b = 0.04, sigma8=0.7, h0=0.7).
#
# The conversion uses the relation in Table 4 of Ragagnin et al. (2020).
#

import hydro_mc
c_200 = hydro_mc.concentration_from_mc_relation('200c', M=1e14, a=0.9, omega_m = 0.2, omega_b = 0.04, sigma8=0.7, h0=0.7)
print('c_200(M_200c=1e14Msun, a=0.9) = %.2f'%c_200)
