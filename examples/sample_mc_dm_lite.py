#
# Example for Ragagnin et al. (2020)
#
# To make this script work you need to import hydro_mc,
# to do so, copy the hydro_mc.py file in the same folder of this file (or in your repository)
#
# The following python script get's the 200c concetration of a   halo with M_200c=1e14Msun halo at a=0.1,
# with a cosmology (omega_m = 0.2, omega_b = 0.04, sigma8=0.7, h0=0.7).
#
# The conversion uses the dark matter NFW concentration in the mass-concentration relation presented in Table A2 of Ragagnin et al. (2020).
#

import hydro_mc
c_200 = hydro_mc.concentration_from_mc_relation('200c', M=1e14, a=0.9,
              omega_m = 0.2, omega_b = 0.04, sigma8=0.7, h0=0.7,
              use_lite_mc_fit=True,
              use_lite_mc_dm_fit=True
              )
print('c_200c(M_200c=1e14Msun, a=0.9) = %.3f # from MC relation where mass log-slope does not depend on cosmology'%c_200)
