# hydro_mc

hydro_mc is a python library and executable to perform masses conversions and Concentration fits of haloes in [Magenticum](http://www.magneticum.org) hydrodynamic simulations.

These conversions are based on fits presented in the paper Ragagnin et al. (2020, in prep).

To use this software, just download the content of this repository. 
You can use it as an executable via `python hydro_mc.py --help` or as a library inside your python project by including `import hydro_mc`.

Table of Content:

- [Install, Usage, references and License](#install-usage-references-and-license)
- [Examples](#examples)
    - [Obtain halo concentration $c_delta$ from a halo mass via a mass-concentration relation](#obtain-halo-concentration-c_delta-from-a-halo-mass-via-a-mass-concentration-relation)
    - [Obtain halo concentration $c_delta2$ from a halo concentration $c_delta1$](#obtain-halo-concentration-c_delta2-from-a--halo-concentration-c_delta1)
    - [Obtain halo mass $M_delta2$ from a halo mass $M_delta1$ via a mass-concentration relation](#obtain-halo-mass-m_delta2-from-a-halo-mass-m_delta1-via-a-mass-concentration-relation)
    - [Obtain halo mass $M_delta2$ from a halo mass $M_delta1$ via a mass-mass relation](#obtain-halo-mass-m_delta2-from-a-halo-mass-m_delta1-via-a-mass-mass-relation)
    - [Obtain halo mass $M_delta2$ from a halo mass $M_delta1$ and its concentration $c_delta1$](#obtain-halo-mass-m_delta2-from-a-halo-mass-m_delta1-and-its-concentration-c_delta1)
- [Display and change fit parameters](#display-and-change-fit-parameters)
- [License](#license)


## Install, API Manual, Scientific References and License

You can install *hydro_mc* just by downloading the file `hydro_mc.py`.

You can use `hydro_mc.py` in two ways: (i) as a stand alone tool, see `python hydro_mc.py --help` for a brief guide on the possible parameters, or (ii) you can include the package `hydro_mc` into your python project.

The package provides the following functions:


    def do_get_concentration_from_mc_relation(delta, M, a, omega_b, omega_m, sigma8, h0)   #obtain halo concentration from the Ragagnin et al. 2020 MC relation
    def do_get_mass_from_mm_relation(delta1, delta2, M, a, omega_b, omega_m, sigma8, h0)   #obtain hallo mass from the Ragagnin et al. 2020 MC relation
    def do_get_mass_from_mc_relation(delta1, delta2, M, a, omega_b, omega_m, sigma8, h0)   #obtain hallo mass from the Ragagnin et al. 2020 MM relation


The following functions convert massses and concentrations without any fit parameter.

    def do_convert_concentration(delta1, delta2, c, omega_m) #when converting c_delta2 to c_delta1, you need omega_m if one delta is 'vir'
    def do_get_mass_from_m_and_c(delta1, delta2, M, c) 
    
delta parameters can be something as `delta` = `200c`, `2500c`, `500c`, `200m`, `vir`.

If you use this package, please cite Ragagnin et al. (2020).

This package is released under New BSD License, see Section [License](#license).

## Examples

Here below a list of examples to use this package.

### Obtain halo concentration $c_delta$ from a halo mass via a mass-concentration relation

To compute the concentration via a mass-concentration relation, execute the script with the `--concentration-from-mc-relation` flag or call the function `do_get_concentration_from_mc_relation(delta,  M, a, omega_m, omega_b, sigma8, h0)`.
This conversion, by default is obtained using the fit results in Table 5 of Ragagnin et al (2020, in prep).


For instance, to obtain the concentration in 200c overdensity, of a halo of 1e14 Msun, at a scale factor of 0.1 and omega_m=0.2, omega_b = 0.04, sigma8 =0.7 and hubble_0 = 0.7, then execute the following command

    python hydro_mc.py  --delta 200c --concentration-from-mc-relation --M 1e14 --a 0.1 --omega-m 0.2 --omega-b 0.04 --sigma8 0.7 --h0 0.7

Or, within a python script

    import hydro_mc
    c_200 = hydro_mc.do_get_concentration_from_mc_relation('200c', M=1e14, a=0.1, omega_m = 0.2, omega_b = 0.04, sigma8=0.7, h0=0.7)

You can also pass arrays of M,a,omega_m,omega_b sigma8, and h0. In that case the function will return an array of concentrations.


### Obtain halo concentration $c_delta2$ from a  halo concentration $c_delta1$

In case you want to convert the concentration from two overdensities use `--concentration-from-c`, set the starting overdensity with `--delta1` and the destination overdensity with `--delta2`, and the concentration in $delta1$ with `--c`  or call the function `do_get_mass_from_m_and_c(delta1, delta2, c)`.

In case you need to convert from or to the virial over density (by setting delta1 or delta2 to `vir`), you need to provide the omega_m parameter (add '--omega-m 0.7' to the command line and 'omega_m=0.7' in hte function call). 

For instance, to obtain the concentration in 200c overdensity, given the concentration first in 500c and then in critical overdensity, execute the following command

    python hydro_mc.py  --delta1 500c --delta2 200c --concentration-from-c --c 3.
    python hydro_mc.py  --delta1 vir --delta2 200c --concentration-from-c --c 3. --omega-m 0.24

Or, inside a python script

    import hydro_mc
    c_200_from_500 = hydro_mc.do_get_mass_from_m_and_c('500c', '200c', 3.)
    c_200_from_vir = hydro_mc.do_get_mass_from_m_and_c('vir', '200c', 3., omega_m=0.24)

This conversion assumes an NFW profile. In particular, the function uses the fractional density within a given concentration, namely 

`integral_NFW(c) = ln(1+c) - c/(1+c)`,

When you can plug a different funtion, from the library in the following way

    import hydro_mc
    def f_non_nfw(c):
        return ln(1+c)
    def f_nfw(c):
        return ln(1+c) - c/(1+c)
    c_200_from_500_non_nfw = hydro_mc.do_get_mass_from_m_and_c('500c', '200c', 3., integral_profile = f_non_nfw)
    c_200_from_500_nfw = hydro_mc.do_get_mass_from_m_and_c('500c', '200c', 3., integral_profile = f_nfw)

## Obtain Halo Masses

### Obtain halo mass $M_delta2$ from a halo mass $M_delta1$ via a mass-concentration relation

To convert masses from two overdensities, by passing thgough a MC relation, use, from command line - the flag `--mass-from-mc-relation`, and from a script use the function `do_get_mass_from_mm_relation`

From command line:

    python hydro_mc.py --delta1 500c --mass-from-mc-relation --delta2 vir  --M 1e14  --a 1. --omega-m 0.2 --omega-b 0.04 --sigma8 0.7 --h0 0.7

From script:

    import hydro_mc
    M_500c = hydro_mc.do_get_mass_from_mc_relation('500c','vir', 1e14,1.,0.2,0.04,0.7,0.7)

You can also specify the parameters with the keywors `M,a,omega_m,omega_b,sigma8` and `h0`, for instance

    
    import hydro_mc
    M_vir = hydro_mc.do_get_mass_from_mc_relation('vir','200c', M=1e14, a=1.,omega_m=0.2, omega-b=0.04, sigma8=0.7, h0=0.7)

### Obtain halo mass $M_delta2$ from a halo mass $M_delta1$ via a mass-mass relation

To convert masses from two overdensities, according to Table 7 in Ragagnin et al. (2020, in prep), use - from command line - the flag `--mass-from-mc-relation`, and from a script, use the function

From command line:

    python hydro_mc.py --delta1 500c --mass-from-mm-relation --delta2 vir  --M 1e14  --a 1. --omega-m 0.2 --omega-b 0.04 --sigma8 0.7 --h0 0.7

From script:

    import hydro_mc
    M_500 = hydro_mc.do_get_mass_from_mm_relation('500c','vir', 1e14,1.,0.2,0.04,0.7,0.7)

You can also specify the parameters with the keywors `M,a,omega_m,omega_b,sigma8` and `h0`, for instance

    
    import hydro_mc
    M_vir = hydro_mc.do_get_mass_from_mm_relation('vir','200c', M=1e14, a=1.,omega_m=0.2, omega-b=0.04, sigma8=0.7, h0=0.7)
    
### Obtain halo mass $M_delta2$ from a halo mass $M_delta1$ and its concentration $c_delta1$

If you know the mass and concentration of a halo, you do not need any fit relation.
From command line

  python hydro_mc.py --delta1 500c --mass-from-mass-and-c --delta2 c200c  --M 1e14  --c 2.

And, from library

    import hydro_mc
    M_vir = hydro_mc.do_get_mass_from_m_and_c('vir','200c', 2.)
   

In case you need to convert from or to `delta=vir`, you need to specify, respectively `--omega-m value` or `omega_m=value`. 
  
## Display and change fit parameters


You can switch to the 'lite' version of the mass-concentration fit (where there is no dpeendency of cosmology in the mass logarithmic slope) with the flag `--use-lite-mc-fit` or, adding the parameter `use_lite_mc_fit=True` to function calls.

You can use the dark matter profile the mass-concentration fit (where there is also there no dpeendency of cosmology in the mass logarithmic slope) with the flag `--use-lite-mc-fit --use-lite-mc-dm-fit` or, adding the parameters `use_lite_mc_fit=True, use_lite_mc_dm_fit=True` in function calls.

Additionally, wathever fit you are using (it also holds for mass-mass fits) you can change fit parameters.

The fit parameter names are:
`'A0','B0','C0','alpha_m','alpha_b','alpha_sigma','alpha_h','beta_m','beta_b','beta_sigma','beta_h','gamma_m','gamma_b','gamma_sigma','gamma_h','sigma'` and their pivots are `'M','a','omega_m','omega_b','sigma8','h0'`.

From command line use teh option `--set-fit-parameters` and `--set-pivots` as follows

 ~/anaconda3/bin/python hydrosim_mass_concentration.py --delta1 500c --mass-from-mm-relation --delta2 vir  --M 1e14  --a 1. --omega-m 0.2 --omega-b 0.04 --sigma8 0.7 --h0 0.7 --set-fit-parameters A0=1.0 B0=0.0 --set-pivots  M=1e4.

From a script, try the following

    import hydro_mc
    hydro_mc.
    M_500c = hydro_mc.do_get_mass_from_mc_relation('500c','vir', 1e14, 1., 0.2, 0.04, 0.7, 0.7, show_fit_parameters=True,use_lite_mc_fit=True)


To be completely sure which fit parameters you are using, from command line add the flag `--show-fit-parameters`, while from script, add the flag `show_fit_parameters` to the functions `do_get_mass_from_mm_relation`, `do_get_mass_from_mc_relation` and `do_get_concentration_from_mc_relation`. For instance:

   python hydro_mc.py --delta1 500c --mass-from-mc-relation --delta2 vir  --M 1e14  --a 1. --omega-m 0.2 --omega-b 0.04 --sigma8 0.7 --h0 0.7 --debug  --show-fit-parameters  --use-lite-mc-fit

or, from library

    import hydro_mc
    M_500c = hydro_mc.do_get_mass_from_mc_relation('500c','vir', 1e14, 1., 0.2, 0.04, 0.7, 0.7, show_fit_parameters=True,use_lite_mc_fit=True)



## Debug

Add the `--debug` flag to the command line in order to obtain the full stack trace of errors.


# License

Copyright (c) 2019 Antonio Ragagnin <antonio.ragagnin@inaf.it>  

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation and/or
other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may
be used to endorse or promote products derived from this software without specific
prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL
THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

