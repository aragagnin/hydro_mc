#
# The following python script get's the 200c concetration of a halo with M_200c=1e14Msun halo at a=0.1,
# with a cosmology (omega_m = 0.2, omega_b = 0.04, sigma8=0.7, h0=0.7).
#
# The conversion uses the relation in Table 4 of Ragagnin et al. (2020).
#

import hydro_mc
c_200 = hydro_mc.concentration_from_mc_relation('200c', M=1e14, a=0.1, omega_m = 0.2, omega_b = 0.04, sigma8=0.7, h0=0.7)
print('c_200 = ',c_200)
