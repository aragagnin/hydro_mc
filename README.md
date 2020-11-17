# hydro_mc

hydro_mc is a python library and executable to perform masses conversions and Concentration fits of haloes in [Magenticum](http://www.magneticum.org) hydrodynamic simulations. This package is written by **Antonio Ragagnin** and its conversions are based on fits presented in the paper [Ragagnin et al. (2020)](https://ui.adsabs.harvard.edu/abs/2020MNRAS.tmp.3313R/abstract).

To start using this tool, just download the content of this repository. 

Mass calibration python notebook: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/aragagnin/hydro_mc/master?filepath=mass-calibration.ipynb)


You can use it as an executable via `python hydro_mc.py --help` or as a library inside your python project by including `import hydro_mc`.

Table of Content:

- [Install, User Manual, References and License](#install-user-manual-references-and-license)
- [Examples](#examples)
    - [Obtain halo concentration $c_delta$ from a halo mass via a mass-concentration relation](#obtain-halo-concentration-c_delta-from-a-halo-mass-via-a-mass-concentration-relation)
    - [Obtain halo concentration $c_delta2$ from a halo concentration $c_delta1$](#obtain-halo-concentration-c_delta2-from-a--halo-concentration-c_delta1)
    - [Obtain halo mass $M_delta2$ from a halo mass $M_delta1$ via a mass-concentration relation](#obtain-halo-mass-m_delta2-from-a-halo-mass-m_delta1-via-a-mass-concentration-relation)
    - [Obtain halo mass $M_delta2$ from a halo mass $M_delta1$ via a mass-mass relation](#obtain-halo-mass-m_delta2-from-a-halo-mass-m_delta1-via-a-mass-mass-relation)
    - [Obtain halo mass $M_delta2$ from a halo mass $M_delta1$ and its concentration $c_delta1$](#obtain-halo-mass-m_delta2-from-a-halo-mass-m_delta1-and-its-concentration-c_delta1)
    - [Display and change fit parameters](#display-and-change-fit-parameters)
- [License](#license)


## Install, User Manual, References and License

You can install *hydro_mc* just by downloading the file `hydro_mc.py` of this repository.

You can use `hydro_mc.py` in two ways: 
 - as a stand alone tool, see `python hydro_mc.py --help` for a brief guide on the possible parameters, 
 - or you can include the package `hydro_mc` into your python project.

The package provides the following functions:


Function name |  Parameters | Comments
--- | --- | ---
`concentration_from_mc_relation` | delta,<br> M, [Msun]<br> a, <br> omega_b, <br> omega_m, <br>sigma8, <br>h0, <br>table=None,<br> use_lite_mc_fit=False,<br> use_lite_mc_dm_fit=False <br> | Obtain halo concentration on overdensity `delta`  from the Ragagnin et al. 2020 MC relation (see Table 4 in this paper) fit a halo with properties mass M, scale factor a, omega_b, omega_m, sigma8 and h0. If `table` is provided (see Sec. [Display and edit fit parameters](#display-and-change-fit-parameters)) then fit parameters are taken from it. Use ` use_lite_mc_fit=True` to utilise the fit parameters in  Ragagnin et al. 2020 (table A1) and `use_lite_mc_fit=True, use_lite_mc_dm_fit=True`  to utilise fit parameters in Ragagnin et al. 2020 (table A2)
`mass_from_mm_relation` | delta1, <br> delta2,<br>  M, [Msun] <br> a, <br> omega_b, <br> omega_m, <br> sigma8, <br> h0, <br> table=None,  | Obtain halo mass on overdensity `delta2`  from the Ragagnin et al. 2020 MM relation (see Table 5 and Table 6 in this paper) for a halo with properties mass `M`, on overdensity `delta1`, scale factor `a`, omega_b, omega_m, sigma8 and h0. If `table` is provided (see Sec. [Display and edit fit parameters](#display-and-change-fit-parameters)) then fit parameters are taken from it. 
`mass_from_mc_relation` | delta1, <br>  delta2, <br> M,<br>  a, <br> omega_b, <br>  omega_m, <br> sigma8, <br> h0, <br>  table=None | Obtain halo mass on overdensity `delta2`  from the Ragagnin et al. 2020 MM relation (see Table 4 and Equations 9-11) for a halo with properties mass `M`, on overdensity `delta1`, scale factor `a`, omega_b, omega_m, sigma8 and h0. If `table` is provided (see Sec. [Display and edit fit parameters](#display-and-change-fit-parameters)) then fit parameters are taken from it. 
`convert_concentration` | delta1, <br> delta2, <br> c, <br>omega_m=None, f_profile=None,<br>  c_hu_kratsov_2002=False |  Converts concentrations by using the relation $ (c_delta2/c_delta1)^3 = delta1/delta * f(c_delta2)/f(c_delta1),$ where $f(c)=ln(1+c)+c/(1+c).$ Set  `f_profile` to a different function to change `f`. Set `c_hu_kratsov_2002=False` to use the fitting formula provided in [Hu & Kravtsov (2002)](https://adsabs.harvard.edu/abs/2003ApJ...584..702H/). 
`mass_from_m_and_c` |  delta1, delta2, M, c, omega_m=None  |  Same as above but returns the mass in that overdensity with the formula $M_delta2/M_delta1 = (c_delta2/c_delta1)^3 * delta2/delta1$
    
The values of `delta` parameters can be something as `delta` = `200c`, `2500c`, `500c`, `200m`, `vir`.

You can also pass both arrays and scalars of M,a,omega_m,omega_b sigma8, and h0. In the first  case the function will return an array of concentrations.

If you use this package, please cite Ragagnin et al. (2020, in prep).

This package is released under New BSD License, see Section [License](#license).

## Examples

Here below a list of examples to use this package.

### Obtain halo concentration $c_delta$ from a halo mass via a mass-concentration relation

To obtain the concentration in 200c overdensity, of a halo of 1e14 Msun, at a scale factor of 0.1 and omega_m=0.2, omega_b = 0.04, sigma8 =0.7 and hubble_0 = 0.7, then execute the following command:
```console
python hydro_mc.py  --delta 200c --concentration-from-mc-relation --M 1e14 --a 0.1 --omega-m 0.2 --omega-b 0.04 --sigma8 0.7 --h0 0.7
```
Or, within a python script:
```python
import hydro_mc
c_200 = hydro_mc.concentration_from_mc_relation('200c', M=1e14, a=0.1, omega_m = 0.2, omega_b = 0.04, sigma8=0.7, h0=0.7)
```

### Obtain halo concentration $c_delta2$ from a  halo concentration $c_delta1$

To obtain the concentration in 200c overdensity, given the concentration first in 500c and then in critical overdensity, execute the following command

 ```console
python hydro_mc.py  --delta1 500c --delta2 200c --concentration-from-c --c 3.
python hydro_mc.py  --delta1 vir --delta2 200c --concentration-from-c --c 3. --omega-m 0.24
```
Or, inside a python script:
```python
import hydro_mc
c_200_from_vir = hydro_mc.mass_from_m_and_c('vir', '200c', 3., omega_m=0.24)
```

Note that we had to provide `omega_m` because one of the overdensity is `vir`. You can ignore this parameter if you convert between tho other critical overdensities.

Also, you do not need to stick with overdensities `200c, 500c, 2500c`. For instance, here below the conversion between overdensity 200c and 173c:
```bash
python hydro_mc.py  --delta1 200c --delta2 173c --concentration-from-c --c 3
```
The above conversions assume an NFW profile. In particular, the function uses the fractional density within a given concentration, namely `integral_NFW(c) = ln(1+c) - c/(1+c)`. When you can plug a different funtion, from the library in the following way
```python
import hydro_mc
def f_non_nfw(c):
    return ln(1+c)
def f_nfw(c):
    return ln(1+c) + c/(1+c)
c_200_from_500_non_nfw = hydro_mc.mass_from_m_and_c('500c', '200c', 3., f_profile = f_non_nfw)
c_200_from_500_nfw = hydro_mc.mass_from_m_and_c('500c', '200c', 3., f_profile = f_nfw)
```

### Obtain halo mass $M_delta2$ from a halo mass $M_delta1$ via a mass-concentration relation

To convert masses from two overdensities, by passing thgough a MC relation, use, from command line - the flag `--mass-from-mc-relation`, and from a script use the function `mass_from_mm_relation`, From command line:
 ```console
 python hydro_mc.py --delta1 500c --mass-from-mc-relation --delta2 vir  --M 1e14  --a 1. --omega-m 0.2 --omega-b 0.04 --sigma8 0.7 --h0 0.7
```
while from a python script:
```python
import hydro_mc
M_500c = hydro_mc.mass_from_mc_relation('500c','vir', 1e14,1.,0.2,0.04,0.7,0.7)
#You can also specify the parameters with the keywors `M,a,omega_m,omega_b,sigma8` and `h0` (this is true for all function calls of this package), for instance:
M_vir = hydro_mc.mass_from_mc_relation('vir','200c', M=1e14, a=1.,omega_m=0.2, omega-b=0.04, sigma8=0.7, h0=0.7)
```
### Obtain halo mass $M_delta2$ from a halo mass $M_delta1$ via a mass-mass relation

To convert masses from two overdensities, according to Table 7 in Ragagnin et al. (2020, in prep), use - from command line - the flag `--mass-from-mc-relation`, and from a script, use the function, from command line:
```console
    python hydro_mc.py --delta1 500c --mass-from-mm-relation --delta2 vir  --M 1e14  --a 1. --omega-m 0.2 --omega-b 0.04 --sigma8 0.7 --h0 0.7
```
From script:
```python
import hydro_mc
M_500 = hydro_mc.mass_from_mm_relation('500c','vir', 1e14,1.,0.2,0.04,0.7,0.7)
#which is equal to:
M_vir = hydro_mc.mass_from_mm_relation('vir','200c', M=1e14, a=1.,omega_m=0.2, omega-b=0.04, sigma8=0.7, h0=0.7)
```
### Obtain halo mass $M_delta2$ from a halo mass $M_delta1$ and its concentration $c_delta1$

If you know the mass and concentration of a halo, you do not need any fit relation.
From command line
```console
  python hydro_mc.py --delta1 500c --mass-from-mass-and-c --delta2 c200c  --M 1e14  --c 2.
```
And, from library
```python
import hydro_mc
M_vir = hydro_mc.mass_from_m_and_c('vir','200c', 2.)
#in case we'd need to convert from or to `delta=vir`,  we'd need to specify, respectively `--omega-m value` or `omega_m=value`. 
```  

### Display and change fit parameters

To be completely sure which fit parameters you are using, from command line add the flag `--show-fit-parameters`, while from script, add the flag `show_fit_parameters` to the functions `mass_from_mm_relation`, `mass_from_mc_relation` and `concentration_from_mc_relation`. For instance:
```console
python hydro_mc.py --delta1 500c --mass-from-mc-relation --delta2 vir  --M 1e14  --a 1. --omega-m 0.2 --omega-b 0.04 --sigma8 0.7 --h0 0.7 --debug  --show-fit-parameters  --use-lite-mc-fit
```
or, from library
```python
import hydro_mc
M_500c = hydro_mc.mass_from_mc_relation('500c','vir', 1e14, 1., 0.2, 0.04, 0.7, 0.7, show_fit_parameters=True,use_lite_mc_fit=True)
```

You can use the dark matter profile the mass-concentration fit (where there is also there no dpeendency of cosmology in the mass logarithmic slope) with the flag `--use-lite-mc-fit --use-lite-mc-dm-fit` or, adding the parameters `use_lite_mc_fit=True, use_lite_mc_dm_fit=True` in function calls. 

Additionally, wathever fit you are using (it also holds for mass-mass fits) you can change fit parameters.
The fit parameter names are:
`'A0','B0','C0','alpha_m','alpha_b','alpha_sigma','alpha_h','beta_m','beta_b','beta_sigma','beta_h','gamma_m','gamma_b','gamma_sigma','gamma_h','sigma'` and their pivots are `'M','a','omega_m','omega_b','sigma8','h0'`.
From command line use teh option `--set-fit-parameters` and `--set-pivots`. Parameters that are unset will be zeroed.


The following example convert the mass of `1e14Msun/h` at `z=0` (`a=1`) fit parameters from CLASH data [(see Merten et al. 2015)](https://adsabs.harvard.edu/abs/2015ApJ...806....4M/abstract) (`exp(A0) = 3.66, B0 = -0.32, C0 = -0.14` and masses in units of `Msun/h`):
```console
python hydro_mc.py --delta1 200c --mass-from-mc-relation --delta2 500c  --M 1e14  --a 1.0 --set-fit-parameters A0=1.297 B0=-0.32 C0=-0.14 --set-pivots  M=8e14 a=0.73  
```
From a script, try the following
```python
import hydro_mc
table = {}
hydro_mc.set_fit_parameters(table,  A0=1.297, B0=-0.32 ,C0=-0.14)
hydro_mc.set_pivots(table, M=8e14, a=0.73)
M_500c = hydro_mc.mass_from_mc_relation('200c','500c', 1e14, 1., omega_b=None, omega_m=None, sigma8=None, h0=None, table=table show_fit_parameters=True)
```


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
