#
# The following python script get's  M_200c of a halo with M_500c = 1e14Msun halo at a=0.1,
# with a cosmology (omega_m = 0.2, omega_b = 0.04, sigma8=0.7, h0=0.7).
#
# The conversion uses the relation in Table 5 and Table 6 of Ragagnin et al. (2020).
#

import hydro_mc
M_200c = hydro_mc.mass_from_mm_relation('500c','200c', M=1e14, a=1.,omega_m = 0.2, omega_b = 0.04, sigma8=0.7, h0=0.7)
