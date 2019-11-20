#
# To make this script work you need to import hydro_mc,
# to do so, copy the hydro_mc.py file in the same folder of this file (or in your repository)
#

print('')
print('Example for Ragagnin et al. (2020)')
print('To make this script work you need to import hydro_mc,')
print('to do so, copy the hydro_mc.py file in the same folder of this file (or in your repository).')
print('')
print('The following python script get's  M_200c of a halo with M_500c = 1e14Msun halo at a=0.9')
print('with a cosmology (omega_m = 0.2, omega_b = 0.04, sigma8=0.7, h0=0.7).')
print(' The conversion uses the relation in Table 5 and Table 6 of Ragagnin et al. (2020).')

import hydro_mc
M_200c = hydro_mc.mass_from_mm_relation('500c','200c', M=1e14, a=0.9,omega_m = 0.2, omega_b = 0.04, sigma8=0.7, h0=0.7)
print('M_200c(M_500c=1e14Msun, a=0.9) = %e'%M_200c)

print('The following python script get's  M_200m given M_200c and the same properties as the previous example')

import hydro_mc
M_200m = hydro_mc.mass_from_mm_relation('200m','200c', M=1e14, a=0.9,omega_m = 0.2, omega_b = 0.04, sigma8=0.7, h0=0.7)
print('M_200m(M_200c=1e14Msun, a=0.9) = %e '%M_200m)
print('')
