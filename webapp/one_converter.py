import hydro_mc
from browser import document, window
#from browser import alert
#from browser.widgets.dialog import InfoDialog
#import traceback
#storage = window.localStorage
alert = window.alert
from browser.local_storage import storage

def compute_f_from_kw(fields, sanity, function):
    """
    convert `form` fields to float (or leave it as strings if they are overdensitiess)
    and call function(**dictionary).  and convert form f
    """
    kw = {}
    
    print('fields',fields)
    sanity(fields)
    for k in  fields:
        name = k
        value = fields[k]
        print(name, value)
        value = value.strip()
        if len(value)==0:
            raise Exception('Value of "%s" cannot be empty'%name)

        if not(('c' in value) or ('i' in value) or ('m' in value)):
            try:
                value = float(value)
            except:
                raise Exception('Unable to convert "%s" value "%s" to float'%(name, value))
            if value==0.:
                raise Exception('The value of "%s" cannot be zero'%(name))
        kw[name] = value
    print('function', function)
    print('kw', kw)
    res = function(**kw)
    return res

def compute_f(form_id, sanity, function, format, additional_fields = None, set_res_e = True):
    """
    parse form inputs in `form_id`, perform sanity check with `sanity(form.elements)`, store elemnts in a dictionary and call function(**dictionary). 
    Format output with format string (e.g. format = '%.5f' for concentration)
    """
    res_e = None
    kw = {}
    
    fields = dict({})
    if additional_fields is not None:
        fields = dict(additional_fields)
    for e in  document[form_id].elements:
        name = e.name
        if ('result' in name):
            res_e = e

            continue
        if ('ignore' in name):
            continue
        if(e.type=='button'):
            continue
        fields[e.name] = e.value
    res = compute_f_from_kw(fields, sanity, function) #call not tested after refactorying
    print(res)
    if set_res_e:
        res_e.value = format%res
    return format%res

def mm_sanity(kw):
    #perform sanity checks on mass-mass conversion
    if kw['delta_from'] == kw['delta_to']:
        raise Exception("Delta1 must be different than Delta2")
    if  (kw['delta_from']=='200m' and kw['delta_to']!='200c') or (kw['delta_to']=='200m' and kw['delta_from']!='200c'):
        raise Exception("When one overdensity is 200m, then you can only convert between 200c<-->200m and viceversa")

def mc_sanity(kw):
    #no sanity checks for mass-concentration
    pass


def compute_mc_exc(form_id, sanity, function, format, additional_fields = None, set_res_e = True):
    #generic wrapper that alert exceptions and store data if everything is succesful
    s = None
    res_e = None
    try:
        res_e = compute_f(form_id, sanity, function, format, additional_fields = additional_fields, set_res_e = set_res_e)
    except Exception as e:
        s = str(e) #traceback.format_exc())
        print(s)
        
    if s is not None:
        #alert( ' '.join(s.split('\n')[-2:]))
	alert(s)
    else:
        store()
    return res_e

def store():
    #save form values in internal browser memory
    for i,e in enumerate(document.select('input, select')):
        k = '%s_%d'%(e.name,i)
        storage[k] = e.value

def restore(default_values):
    #restore form values from internal browser memory
    for i,e in enumerate(document.select('input, select')):
        k = '%s_%d'%(e.name,i)
        if 'result' in e.class_name:
            continue
        if k in storage:
            e.value = storage[k]
        elif k in default_values:
            e.value = default_values[k]

def mc_dm_lite(**kw):
    kw['use_lite_mc_fit'] = True
    kw['use_lite_mc_dm_fit'] = True
    return hydro_mc.concentration_from_mc_relation(**kw)


def form_get(form, k):
    for e in document[form].elements:
        if e.name == k:
            return e.value
    raise Exception("Field not found: '%s'"%k)

def put_exponent(s):
    if 'e' not in s:
        return s
    if 'e' in s:
        base,exponent = s.split('e')
        if exponent[0]=='+':
            exponent = exponent[1:]
        if exponent[0]=='0' :
            exponent = exponent[1:]
        return base+ ' &middot; 10<sup>'+exponent+'</sup>'
def mix_click(ev):

    destination = form_get('mix_form', 'output_ignore')
    #
    # ideally we 'd like to have two forms: one for MM and one for Mc,
    # in this simplified app we fake an Mc or MM form based on user input
    #
    try:
        z = float(form_get('mix_form', 'z_ignore'))
    except:
        return alert('Unable to convert redshift to float')
    a = str(1./(1.+z))
    if destination[0]=='c':
        f = hydro_mc.concentration_from_mc_relation
        units = ''
        result_name =  'c'+'<sub>'+( form_get('mix_form','delta_ignore'))+'</sub>'+':'

        sanity = mc_sanity
        format = '%.4f'
        additional_fields = {'delta': form_get('mix_form','delta_ignore'), 'a':a}
    elif destination[0]=='M':
        f = hydro_mc.mass_from_mm_relation
        sanity = mm_sanity
        additional_fields = {'delta_from': form_get('mix_form','delta_ignore'), 'delta_to': destination[1:], 'a':a}
        units = '[M<sub>&#x2299;</sub>]'
        result_name =  'M'+'<sub>'+destination[1:]+'</sub>'+':'
        format = '%.4e'
    
    res = compute_mc_exc('mix_form', sanity, f, format, additional_fields = additional_fields, set_res_e = False)
    document['mix_result'].html =  put_exponent(res)
    document['output_label'].html = result_name
    document['output_units'].html = units
        
#hook
#document["mc_full_btn"].bind("click", lambda ev:compute_mc_exc('mc_full_form', mc_sanity, hydro_mc.concentration_from_mc_relation, '%.5f'))
#document["mc_dm_btn"].bind("click", lambda ev:compute_mc_exc('mc_dm_form',  mc_sanity, mc_dm_lite, '%.5f'))
#document["mm_mc_btn"].bind("click", lambda ev:compute_mc_exc('mm_mc_form', mm_sanity, hydro_mc.mass_from_m_and_c, '%.5e'))
document["mix_btn"].bind("click", mix_click)

#restore form values from last usage

#_default_values = {"h0_11":"0.7","delta_from_14":"500c","M_5":"2e14","cdelta_16":"2.90247e+14","delta_to_15":"200c","omega_b_1":"0.04","sigma8_10":"0.8","a_4":"1.0","omega_b_9":"0.04","cdelta_7":"5.18523","omega_m_0":"0.3","omega_m_8":"0.3","M_13":"2e14","delta_6":"vir","h0_3":"0.7","a_12":"1.0","sigma8_2":"0.8"}

_default_values = {"M_5":"2e14","delta_ignore_6":"200c","cdelta_result_8":"3.8661","omega_b_1":"0.04","z_ignore_4":"0.0","h0_3":"0.7","output_ignore_7":"c","sigma8_2":"0.8","omega_m_0":"0.3"}

restore(_default_values)

document['loading'].style.display='none'

