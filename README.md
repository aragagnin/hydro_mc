# hydro-mc

hydro-mc is a python library and executable to perform masses conversions and Concentration fits of haloes in [Magenticum](http://www.magneticum.org) hydrodynamic simulations.

These conversions are based on fits presented in the paper Ragagnin et al. (2020, in prep).

To use this software, just download the content of this repository. 
You can use it as an executable via `python hydro_mc.py --help` or as a library inside your python project by including `import hydro_mc`.

## Obtain halo concentration $c_delta$ from a halo mass via a mass-concentration relation

To compute the concentration via a mass-concentration relation, execute the script with the `--concentration-from-mc-relation` flag or call the function `do_get_concentration_from_mc_relation(delta,  M, a, omega_m, omega_b, sigma8, h0)`.

For instance, to obtain the concentration in 200c overdensity, of a halo of 1e14 Msun, at a scale factor of 0.1 and omega_m=0.2, omega_b = 0.04, sigma8 =0.7 and hubble_0 = 0.7, then execute the following command

    python hydro_mc.py  --delta 200c --concentration-from-mc-relation --M 1e14 --a 0.1 --omega-m 0.2 --omega-b 0.04 --sigma8 0.7 --h0 0.7

Or, within a python script

    import hydro_mc
    c_200 = hydro_mc.do_get_concentration_from_mc_relation('200c', M=1e14, a=0.1, omega_m = 0.2, omega_b = 0.04, sigma8=0.7, h0=0.7)

You can also pass arrays of M,a,omega_m,omega_b sigma8, and h0. In that case the function will return an array of concentrations.

This conversion, by default is obtained using the fit results in Table 5 of Ragagnin et al (2020, in prep).

## Obtain halo concentration $c_delta2$ from a  halo concentration $c_delta1$

In case you want to convert the concentration from two overdensities use `--concentration-from-c`, set the starting overdensity with `--delta1` and the destination overdensity with `--delta2`, and the concentration in $delta1$ with `--c`  or call the function `do_get_mass_from_m_and_c(delta1, delta2, c)`.

In case you need to convert from or to the virial over density (by setting delta1 or delta2 to `vir`), you need to provide the omega_m parameter (add '--omega-m 0.7' to the command line and 'omega_m=0.7' in hte function call). 

For instance, to obtain the concentration in 200c overdensity, given the concentration first in 500c and then in critical overdensity, execute the following command

    python hydro_mc.py  --delta1 500c --delta2 200c --concentration-from-c --c 3.
    python hydro_mc.py  --delta1 vir --delta2 200c --concentration-from-c --c 3. --omega-m 0.24

Or, inside a python script

    import hydro_mc
    c_200_from_500 = hydro_mc.do_get_mass_from_m_and_c('500c', '200c', 3.)
    c_200_from_vir = hydro_mc.do_get_mass_from_m_and_c('vir', '200c', 3., omega_m=0.24)




## Obtain halo mass $M_delta2$ from a halo mass $M_delta1$ via a mass-concentration relation


## Obtain halo mass $M_delta2$ from a halo mass $M_delta1$ via a mass-mass relation


## Obtain halo mass $M_delta2$ from a halo mass $M_delta1$ and its concentration $c_delta1$

## Display and change fit parameters

## Final remarks





