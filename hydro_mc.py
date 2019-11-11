"""
hydro_mc is a python library and executable to perform masses conversions and Concentration fits of haloes in [Magenticum](http://www.magneticum.org) hydrodynamic simulations.

These conversions are based on fits presented in the paper Ragagnin et al. (2020, in prep).

To use this software, just download the content of this repository.
You can use it as an executable via `python hydro_mc.py --help` or as a library inside your python project by including `import hydro_mc`.

"""
__author__="Antonio Ragagnin (c) 2019"
__version__="0.1"

import numpy as np
import argparse
import sys
import re


__mc_fit_parameters = {"vir": {"params": [1.503454114104443, -0.04283092691408333, 0.5157209989941997, 0.45445667750331026, -0.24856881467360964, 0.5544350140093234, -0.0048813484527866656, -0.12199409397642753, 0.11663423303800534, 0.05110946208460489, -0.07892747676338406, 0.24005903699741252, -0.1263499637381384, 0.6640188439939326, -0.0299567877892118, 0.3877956797872577], "pivots": {"M": 198759238503196.03, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.272, "sigma8": 0.272, "h0": 0.704}}, "200c": {"params": [1.2436364990990914, -0.04817261898156871, 0.20419215885982817, 0.6316820273466903, -0.24605297432854378, 0.560570072125268, -0.02627068018190943, -0.11775877953823762, 0.11193584169417208, 0.05634549061614718, -0.043822582719200295, 0.3524426183203193, -0.03879420539288709, 0.7673900896521332, -0.27569460666976725, 0.3843115348866266], "pivots": {"M": 173960723876953.16, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.272, "sigma8": 0.272, "h0": 0.704}}, "500c": {"params": [0.8637563855047179, -0.05344871238505832, 0.1878750841109432, 0.6618004570191556, -0.23490408373403376, 0.5190661049361811, -0.03143074979091932, -0.11241937064515797, 0.1257731196624856, 0.08805802745200282, -0.1563176516883163, 0.3463795016853568, -0.044602075614319794, 0.8564224417001306, -0.34652816060672165, 0.3765132317155449], "pivots": {"M": 137038782293146.31, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.272, "sigma8": 0.272, "h0": 0.704}}, "2500c": {"params": [0.12656051215719555, -0.03050866662392269, 0.10725429255827736, 0.7593881752986629, -0.27160211703510345, 0.42181074155295156, -0.020575075642635738, -0.1163991007298093, 0.28880298414213335, 0.10263452464907902, -0.34222932053193433, 0.3844570767051972, -0.1334171989405518, 0.8457199265161256, 0.0028417430312315424, 0.3827347978288253], "pivots": {"M": 68722326105291.2, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.272, "sigma8": 0.272, "h0": 0.704}}, "200m": {"params": [1.692410096240174, -0.040346034043160055, 0.9092242875122345, 0.2268328343963277, -0.2664240976376676, 0.5283845428748246, 0.015645163737334208, -0.11627375082296813, 0.11528658344781062, 0.05003254567973524, -0.09358485276497253, -0.04322554482713586, -0.06348838757477149, 0.6351347984085912, -0.40487997854959523, 0.3882554231750548], "pivots": {"M": 224397583007812.53, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.272, "sigma8": 0.272, "h0": 0.704}}}

__mc_lite_fit_parameters = {"vir": {"params": [1.4985649929244846, -0.04754653951295999, 0.5199383344534508, 0.42335872983250744, -0.14123672388625216, 0.6530026638126829, -0.27667601800841235, 0.18958103942142024, 0.02371146453902725, 0.7637789994055261, -0.44859556264866146, 0.38803081506367154], "pivots": {"M": 198759238503196.03, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}, "200c": {"params": [1.2382820777898689, -0.053413793724654476, 0.20072654857310923, 0.603607539963483, -0.1521899342583827, 0.6467505386837067, -0.24540931053697695, 0.3595828585445649, -0.14575941582538823, 0.7247582262393436, -0.07329103607606331, 0.3845164814226978], "pivots": {"M": 173960723876953.16, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}, "500c": {"params": [0.8591961760288123, -0.05970360132842668, 0.18730552659285832, 0.6319223562569485, -0.13145810034048822, 0.6120793998567394, -0.2739015100800711, 0.33628042357787796, -0.04344994933928333, 0.8893178406086549, -0.4363827722023437, 0.3766897270799671], "pivots": {"M": 137038782293146.31, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}, "2500c": {"params": [0.12248240026576206, -0.03731339714808029, 0.11023256345276963, 0.72734695998088, -0.17862618662088695, 0.5163267659318049, -0.23053189558090148, 0.3593064374504373, 0.001045506046395887, 0.9380532152882959, -0.45993132673543496, 0.38286807046506977], "pivots": {"M": 68722326105291.2, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}, "200m": {"params": [1.6876665626182177, -0.04439299009821192, 0.9102898686541654, 0.20117611449430742, -0.18592086055940954, 0.6032760056708096, -0.17458924277519577, -0.09573339329894155, 0.0033439095394409493, 0.608072469993025, -0.3914462271263976, 0.3884769419509934], "pivots": {"M": 224397583007812.53, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}}

__mc_dm_lite_fit_parameters = {"vir": {"params": [1.4985649929244846, -0.04754653951295999, 0.5199383344534508, 0.42335872983250744, -0.14123672388625216, 0.6530026638126829, -0.27667601800841235, 0.18958103942142024, 0.02371146453902725, 0.7637789994055261, -0.44859556264866146, 0.38803081506367154], "pivots": {"M": 198759238503196.03, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}, "200c": {"params": [1.2382820777898689, -0.053413793724654476, 0.20072654857310923, 0.603607539963483, -0.1521899342583827, 0.6467505386837067, -0.24540931053697695, 0.3595828585445649, -0.14575941582538823, 0.7247582262393436, -0.07329103607606331, 0.3845164814226978], "pivots": {"M": 173960723876953.16, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}, "500c": {"params": [0.9785288098930186, -0.03885461349058336, 0.17813810471397806, 0.4562092312012737, -0.0844283000357409, 0.47202095163570484, -0.33185662366382357, 0.3427667412703562, -0.3709489464232765, 0.4978856094616349, -1.0860705258088728, 0.5063466555940676], "pivots": {"M": 137038782293146.31, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}, "2500c": {"params": [0.21319259819504097, -0.01544383363128253, 0.05466159499929143, 0.5881312963731252, -0.20367090026868506, 0.36261905823870594, -0.4709358214950252, 0.5090317463610325, -0.7263228265986462, 0.29973682920914935, -1.856442289282263, 0.48429006429598354], "pivots": {"M": 68722326105291.2, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}, "200m": {"params": [1.7976155441540107, -0.034095172349226, 0.9175740293353059, 0.008184806629000403, -0.07196912106941096, 0.5330560972093654, 0.02721684778176066, -0.233089714297092, -0.08679242774966536, 0.45285870483992335, 0.024278999082778235, 0.49888743097957355], "pivots": {"M": 224397583007812.53, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}}

__mm_fit_parameters = {"vir": {"200c": {"params": [32.71655403933012, 1.0036501314062962, -0.24301905743769378, 0.16556171834167083, 0.0030986890096535396, 0.047977215233604695, -0.04483567187975675, -0.016615342331499812, 0.03276557151074428, -0.023840618405776757, -0.009723050108930395, 0.15982037016456369, -0.0548201337731943, 0.11914774567523363, 0.05294084491312891, 0.06454828082161385], "pivots": {"M": 198759238503196.03, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.272, "sigma8": 0.272, "h0": 0.704}}, "500c": {"params": [32.31445336000839, 0.995763318333006, -0.23673393737777193, 0.294611800646245, -0.019319169951921223, 0.17646012483853593, -0.10346985361761771, -0.042373056557927787, 0.09508678139955502, -0.04322178493143714, -0.03821264476174489, 0.2128349844377909, -0.11310778096536986, 0.3482878969952066, 0.04783715388383589, 0.1578454124519618], "pivots": {"M": 198759238503196.03, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.272, "sigma8": 0.272, "h0": 0.704}}, "2500c": {"params": [31.33961332257922, 0.9254279357105467, -0.0053270941693614494, 0.6190932916396321, -0.16217319698168417, 0.5740259662954277, -0.05432452884580115, -0.07581377233461492, 0.20315509596579287, -0.010241003783698724, -0.20257727811313234, 0.37895353769136536, -0.23205433590391472, 0.5549732387160674, 0.03894561657006593, -0.31215630263491023], "pivots": {"M": 198759238503196.03, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.272, "sigma8": 0.272, "h0": 0.704}}, "200m": {"params": [33.043740627011175, 0.9943124075863463, 0.2313347126069795, -0.13806731562975613, -0.010240592809525413, -0.022999828518708895, 0.04060039791084734, 0.016727926541201598, -0.0222023048410995, 0.017025963386900593, 0.003578603780419614, -0.16977721619147226, 0.025905856208134456, -0.09040496944966961, 0.017859428165411285, -0.04185469196689413], "pivots": {"M": 198759238503196.03, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}}
, "200c": {"vir": {"params": [32.988858833122194, 0.9947011777578895, 0.2331346721997433, -0.15579445425909785, -0.0027833536594894077, -0.03560913908152464, 0.03733886642410514, 0.015211194766097011, -0.026132071146800672, 0.01705452121842437, 0.0135858079335707, -0.15260350657435226, 0.05672693534757724, -0.10986336717327269, -0.03078169700473028, 0.05574789746231171], "pivots": {"M": 173960723876953.16, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.272, "sigma8": 0.272, "h0": 0.704}}, "500c": {"params": [32.393133728143745, 0.9938822717918784, 0.0031353708366267793, 0.12525883175594232, -0.019659335854126016, 0.12028412362582543, -0.06269694112509237, -0.02557330802924724, 0.06797560282186788, -0.016151361354021093, -0.03855757087539305, 0.0531700152512363, -0.061180506267994594, 0.24268725436554792, -0.02371422287884702, 0.11297880447777645], "pivots": {"M": 173960723876953.16, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.272, "sigma8": 0.272, "h0": 0.704}}, "2500c": {"params": [31.41292708395347, 0.9218754436147497, 0.22473262945872488, 0.46125388997842653, -0.14973283035644322, 0.5387745708530132, -0.04186337961525381, -0.05847813577142404, 0.17085378515815575, 0.005649589124360711, -0.1797170357421586, 0.21068318994679433, -0.07964314269044909, 0.48564804595024696, -0.17508445487715912, -0.2961086703422706], "pivots": {"M": 173960723876953.16, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.272, "sigma8": 0.272, "h0": 0.704}}, "200m": {"params": [33.10619274508529, 0.988300056080471, 0.4578470359717449, -0.2879822751326564, -0.016796161356124422, -0.05303150212542579, 0.07762487233039962, 0.03063434190996475, -0.039732772400170854, 0.029499435116064416, 0.0174896515173054, -0.3134504603341965, 0.06237923922665093, -0.2010890652382813, 0.026078974733249775, 0.08368950274345158], "pivots": {"M": 173960723876953.16, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}}
, "500c": {"vir": {"params": [33.12321802976011, 0.9933637767596534, 0.25201304695394433, -0.26456114498311467, 0.004269035275038148, -0.11095196257971061, 0.08383827710696919, 0.033890849291052294, -0.0801513761836326, 0.0348494828871805, 0.05599513726801808, -0.19079055953097704, 0.11041607918676997, -0.3753581764280458, -0.026980425826214335, 0.1291827918154416], "pivots": {"M": 137038782293146.31, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.272, "sigma8": 0.272, "h0": 0.704}}, "200c": {"params": [32.92981553629957, 1.0004160501687807, 0.01653189328025767, -0.11377621628226807, 0.006121480577403694, -0.08775732385955169, 0.05590236987264638, 0.018728419657978522, -0.05218023631576236, 0.019590483062834695, 0.038635118462186445, -0.035790528004585674, 0.027940217621289534, -0.2667181113523159, 0.05134581292621492, 0.0960500243971675], "pivots": {"M": 137038782293146.31, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.272, "sigma8": 0.272, "h0": 0.704}}, "2500c": {"params": [31.57535884271605, 0.9318980664650164, 0.2188012774464708, 0.3352814482914344, -0.12469106361967909, 0.4086786598617626, 0.014279281429356925, -0.032678092755522824, 0.11452497130233726, 0.03133328360267627, -0.19870512634358725, 0.1602579259457747, -0.06791745678994192, 0.22821827195971517, -0.10934841424300924, 0.2354404576932033], "pivots": {"M": 137038782293146.31, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.272, "sigma8": 0.272, "h0": 0.704}}, "200m": {"params": [33.23903345563792, 0.9865128591080334, 0.47790508411897487, -0.39461069560703277, -0.014848254125418958, -0.1263752449670363, 0.13012800037745717, 0.04947867680060586, -0.09691553298092222, 0.043457051853553925, 0.06942653018321447, -0.3517453874533708, 0.09306484852316713, -0.4697391694946282, 0.050691417663899, 0.1448990284901391], "pivots": {"M": 137038782293146.31, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}}
, "2500c": {"vir": {"params": [33.33250239270301, 1.0201077553837221, 0.15636838746249407, -0.5626391237424389, 0.09276332824044844, -0.3419327662536003, 0.1032050708368785, 0.06300097411731626, -0.2998413193159778, -0.019402208527135766, 0.41265136094448035, -0.30553780743423037, 0.15172866627956008, -0.6382946989163267, 0.038670684413241216, 0.24202455955294258], "pivots": {"M": 68722326105291.2, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.272, "sigma8": 0.272, "h0": 0.704}}, "200c": {"params": [33.13952419096927, 1.026870699455518, -0.07815670892392547, -0.41427354086763674, 0.0991651583378647, -0.31605224602332754, 0.06744052944810479, 0.04905123190352774, -0.2640306473765457, -0.03489992949957441, 0.3833420678922011, -0.1577312152457987, 0.06883435915982403, -0.5349295702901506, 0.15491952333096054, 0.2279218874616231], "pivots": {"M": 68722326105291.2, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.272, "sigma8": 0.272, "h0": 0.704}}, "500c": {"params": [32.773474003459484, 1.0314903544118486, -0.09991206710669961, -0.30655844541924504, 0.0899261627701992, -0.25529881455381004, 0.019319160046123388, 0.02888210069554159, -0.18867246798751744, -0.0450691158276003, 0.31965039226923164, -0.1339260335822625, 0.046829695425163395, -0.26786469607363345, 0.042821693277460486, 0.18179748839481427], "pivots": {"M": 68722326105291.2, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.272, "sigma8": 0.272, "h0": 0.704}}, "200m": {"params": [33.449928994127625, 1.0137672613631057, 0.3884270448825958, -0.6945245790633495, 0.07586049305592515, -0.35742671170676377, 0.13516778655853254, 0.07850133213044976, -0.32416434385441756, -0.014257525322939018, 0.44860092910474053, -0.4733572404757807, 0.17635892757694627, -0.7263246721102229, 0.001987326362323298, 0.24683192744384327], "pivots": {"M": 68722326105291.2, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}}
, "200m": {"vir": {"params": [32.91923993459246, 1.004998283710883, -0.24327974796307458, 0.146916873080803, 0.014085866496374992, 0.03403136832842445, -0.05495582811339603, -0.017709014761172495, 0.024922878675272438, -0.022277807902568742, -0.002687549490900499, 0.18766656690092864, -0.015980084879887904, 0.12354164631530422, -0.051383216549240274, -0.04852060193023841], "pivots": {"M": 224397583007812.53, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}, "200c": {"params": [32.7092432548728, 1.0078543539776024, -0.4923401628810212, 0.317991173206413, 0.013757313724573065, 0.08830533446268542, -0.10310730596591498, -0.035138014465154285, 0.06273672319138414, -0.05014998021686202, -0.010943256393764618, 0.35758349293839736, -0.10227564269822434, 0.24551406258367856, 0.03345997504983831, -0.10235368375951033], "pivots": {"M": 224397583007812.53, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}, "500c": {"params": [32.30590606420742, 1.0000540537767286, -0.4830289557913123, 0.4458649778490151, -0.013155061128686208, 0.21813115725504514, -0.15948649173162333, -0.06122690436674333, 0.12660113555523209, -0.07277092932568646, -0.04164041554251069, 0.4082628758536285, -0.17486998423199526, 0.47758038193650526, 0.013784564207430024, -0.1814127296908954], "pivots": {"M": 224397583007812.53, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}, "2500c": {"params": [31.33382470213857, 0.9313085568714797, -0.23360541371644739, 0.7538862738599599, -0.1582096612458364, 0.6036429135207855, -0.11084469907190307, -0.09380588110396984, 0.23204562989471772, -0.04050734632304558, -0.19328155795275154, 0.5642713366169192, -0.29968357150510994, 0.6506712481038401, 0.026156355100851708, -0.3181591586420962], "pivots": {"M": 224397583007812.53, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}}
}

__fit_parameter_names = ['A0','B0','C0','alpha_m','alpha_b','alpha_sigma','alpha_h','beta_m','beta_b','beta_sigma','beta_h','gamma_m','gamma_b','gamma_sigma','gamma_h','sigma']
__fit_parameter_lite_names = ['A0','B0','C0','alpha_m','alpha_b','alpha_sigma','alpha_h','gamma_m','gamma_b','gamma_sigma','gamma_h','sigma']
__fit_pivot_names = ['M','a','omega_m','omega_b','sigma8','h0']
__deltas = ['200c','500c','2500c','vir','200m']


def panic(x):
    sys.stderr.write(x+'\n')
    sys.exit(1)


def print_fit_params_and_pivots(table,is_lite=False):
    iparam=-1
    fit_parameter_names = __fit_parameter_names if not is_lite else __fit_parameter_lite_names
    for parameter in fit_parameter_names:
        iparam+=1
        print('            %s = %.3f'%(parameter, table['params'][iparam]))
    print('')
    for pivot in __fit_pivot_names:
        if pivot in table['pivots']:
            print('            %s_pivot = %.3f '%(pivot, table['pivots'][pivot]))

def print_abc_equation(is_lite=False):
    print('     A = A0 + alpha_m * ln (Omega_m/Omega_m_pivot) + alpha_b * ln(Omega_b/Omega_b_pivot) + alpha_s * ln(sigma_8/sigma_8_pivot) + alpha_h * ln(h0/h0_pivot) ')
    if not is_lite:
        print('     B = B0 + beta_m * ln (Omega_m/Omega_m_pivot) + beta_b * ln(Omega_b/Omega_b_pivot) + beta_s * ln(sigma_8/sigma_8_pivot) + beta_h * ln(h0/h0_pivot) ')
    else:
        print ('     B = B0')
    print('     C = C0 + gamma_m * ln (Omega_m/Omega_m_pivot) + gamma_b * ln(Omega_b/Omega_b_pivot) + gamma_s * ln(sigma_8/sigma_8_pivot) + gamma_h * ln(h0/h0_pivot) ')



def set_fit_parameters(table, **kw):
    fit_parameter_values  = []
    for parameter_name in __fit_parameter_names:

        value = kw[parameter_name]  if parameter_name in kw and kw[parameter_name] is not None else 0.

        fit_parameter_values.append(value)

    table['params']=fit_parameter_values
    for parameter_name in __fit_pivot_names:
        if 'pivot_'+parameter_name in kw and kw['pivot_'+parameter_name] is not None:
            table['pivots'][parameter_name]=kw['pivot_'+parameter_name]



            


def do_get_from_ragagnin2019_fit(table, pivots, use_lite_mc_fit=False, **kw):
    if not  use_lite_mc_fit:
        norm, slopem, slopea,   pim , pib, pis, pih,    sim, sib, sis, sih,       aim, aib, ais, aih, sigma = table
    else:
        norm, slopem, slopea,   pim , pib, pis, pih,     aim, aib, ais, aih, sigma = table
    M, a, omega_m, omega_b, sigma8, h0 = [kw[pivot] / pivots[pivot] for pivot in __fit_pivot_names]




    norm_2 = norm + pim*np.log(omega_m) +pib*np.log(omega_b)  +  pis*np.log(sigma8)  + pih*np.log(h0)
    if not  use_lite_mc_fit:
        slopem_2 = slopem  +sim*np.log(omega_m) +sib*np.log(omega_b)  + sis*np.log(sigma8)  + sih*np.log(h0)
    else:
        slopem_2 = slopem
    slopea_2 = slopea + aim*np.log(omega_m) +aib*np.log(omega_b)  + ais*np.log(sigma8)  + aih*np.log(h0)

    return np.exp(norm_2 + np.log(M)*slopem_2 +  np.log(a)*slopea_2)

def do_get_concentration_from_mc_relation(delta, M, a, omega_m, omega_b, sigma8, h0, use_lite_mc_fit=False, use_lite_mc_dm_fit=False, show_fit_parameters=False, table=None, **kw):

    if use_lite_mc_dm_fit and not  use_lite_mc_fit:
        raise Exception('If you activate use_lite_mc_dm_fit= you must also activate use_lite_mc_fit=True')
    if table is None:
        if use_lite_mc_fit and use_lite_mc_dm_fit:
            table = __mc_dm_lite_fit_parameters[delta]
        elif use_lite_mc_fit:
            table =  __mc_lite_fit_parameters[delta]
        else:
            table =  __mc_fit_parameters[delta]
    if show_fit_parameters:
        print(' MC relation fit: ')
        print('     ln(c_delta) = A + B ln(M_delta/Mp) + C ln(a/ap) ')
        use_lite_mc_fit and use_lite_mc_dm_fit and     print('\n Dark matter concentration with lite parametrisation: ') and    print_abc_equation(is_lite=True)
        use_lite_mc_fit and not use_lite_mc_dm_fit and     print('\n Total matter oncentration with lite parameters: ') and    print_abc_equation(is_lite=True)
        use_lite_mc_fit and not use_lite_mc_dm_fit and     print('\n Total matter oncentration: ') and    print_abc_equation()
        print('    Delta = %s'% delta)
        print_fit_params_and_pivots(table,is_lite= use_lite_mc_fit)

    return do_get_from_ragagnin2019_fit( table['params'], table['pivots'],use_lite_mc_fit=use_lite_mc_fit,
                                         M=M,a=a,omega_m=omega_m, omega_b=omega_b, sigma8=sigma8, h0=h0,
                                         **kw)



def do_get_mass_from_mm_relation(delta_from, delta_to, M, a, omega_m, omega_b, sigma8, h0,  show_fit_parameters=False,  table=None, **kw):
    if show_fit_parameters:
                    print_fit_params_and_pivots(__mm_fit_parameters[delta_from][delta_to])
    if table is None:
        table = __mm_fit_parameters[delta_from][delta_to]
    return do_get_from_ragagnin2019_fit( table['params'], table['pivots'],
                                         M=M,a=a,omega_m=omega_m, omega_b=omega_b, sigma8=sigma8, h0=h0,
                                         **kw)


def Omega(a, Omega_M, Omegar, Omegak, Omegal):
    return Omega_M * a**-3. /    (Omega_M * a**-3. + Omegar * a**-4. + Omegak * a**-2. + Omegal)

def delta_c(a, Omega_M, Omegar, Omegak, Omegal):
    Omegaz =     Omega(a, Omega_M, Omegar, Omegak, Omegal)
    x =   Omegaz -1.

    return (18. * np.pi **2. + 82. * x - 39. * x**2.) #/ Omegaz;

def f_NFW(c):
    return (np.log(1.+c)-c/(1.+c))

def banach_caccioppoli(f,x0,accuracy=0.001):
    """ this function solves equation of the kind x=f(x) by iterations, given an initial value x=x0"""
    condition=True
    x1=x0
    steps=0
    while condition:

        steps+=1
        x2 = f(x1)
        error = np.abs(x2-x1)/x2
        condition = np.all(error>accuracy)
        x1=x2
    return x2

def do_get_critical_overdensity(delta,  **args):
    arguments_vectorise(args)
    if delta=='vir':
        if('a' not in args or args['a'] is None or 'omega_m' not in args or args['omega_m'] is None):
            raise Exception("You need to provide parameters a and omega_m if you use a delta==vir")
        return delta_c(args['a'], args['omega_m'], 0., 0., 1.- args['omega_m'])
    elif  'c' in delta:
        return float(delta[:-1])
    else:
        raise Exception("Critical overdensity cannot be obtained from %s",delta)


def cdelta1(delta2,delta1,cdelta1, f_NFW=f_NFW):
     return lambda cdelta2: cdelta1 * (  (delta1/delta2)*(f_NFW(cdelta2)/f_NFW(cdelta1))  )**(1./3.)


def c2_bc(delta2, delta1, c1, f_NFW=f_NFW):
    c2 = banach_caccioppoli( cdelta1(delta2, delta1, c1, f_NFW = f_NFW), c1)
    return c2


def  HK_func(x):
    log = np.log
    return(x*x*x*(log(1+1.0/x)-1.0/(1+x)));

def HK_1(delta, delta_vir, cvir):
    log = np.log
    sqrt=np.sqrt
    a1 = 0.5116
    a2 = -0.4283
    a3 = -3.13E-3
    a4 = -3.52E-5
    f=delta/delta_vir*HK_func(1.0/cvir);
    p=a2+a3*log(f)+a4*log(f)*log(f);
    x1=1.0/sqrt(a1*(f**(2.*p))+0.5625)+2*f;
    return 1./x1
    

def do_convert_concentration(delta_from, delta_to, concentration, f_profile=None,  c_hu_kratsov_2002=False, **kw):
    arguments_vectorise(kw)
    overdensity_from = do_get_critical_overdensity(delta_from, **kw)
    overdensity_to = do_get_critical_overdensity(delta_to, **kw)
    if not  c_hu_kratsov_2002:
        if f_profile is None:
            f_profile = f_NFW
        return c2_bc(overdensity_to, overdensity_from, concentration, f_NFW=f_profile)
    else:
        return HK_1(overdensity_to, overdensity_from, concentration)

def do_get_mass_from_m_and_c(delta_from, delta_to, concentration,  **kw):
    c = concentration
    overdensity_from = do_get_critical_overdensity(delta_from, **kw)
    overdensity_to = do_get_critical_overdensity(delta_to, **kw)
    new_c =  c2_bc(overdensity_to, overdensity_from, c)
    return    kw['M'] * (overdensity_to/overdensity_from)*(new_c/c)**3.


def do_get_mass_from_mc_relation(delta_from, delta_to, omega_m, omega_b, sigma8, h0,   **kw):
    overdensity_from = do_get_critical_overdensity(delta_from, **kw)
    overdensity_to = do_get_critical_overdensity(delta_to, **kw)
    c =  do_get_concentration_from_mc_relation(delta_from, **kw)
    new_c =  c2_bc(overdensity_to, overdensity_from, c)
    M = kw['M'] * (overdensity_to/overdensity_from)*(new_c/c)**3.
    return   M



def main():
    parser = argparse.ArgumentParser(description='Magneticum Cosmological Masses and Concentration Converter')
    parser.add_argument('--delta1','--delta', type=str, help='Overdensity Delta for the MC relation', default=None)
    parser.add_argument('--delta2', type=str,help='Destination overdensity in case of mass-mass or concentration-concentration conversion', default=None)

    parser.add_argument('--M', type=float,help='Halo mass to be converted')
    parser.add_argument('--a', type=float,help='scale factor of halo to be converted')
    parser.add_argument('--omega-m', type=float,help='Omega_m parameter of the conversion')
    parser.add_argument('--omega-b', type=float,help='Omega_b parameter of the conversion')
    parser.add_argument('--sigma8', type=float,help='sigma8 parameter of the conversion')
    parser.add_argument('--h0', type=float,help='h0 parameter of the conversion')

    parser.add_argument('--c', type=float,help='Concentration of the halo. Use in combination with --concentration-from-c and --mass-from-mass-and-c')



    parser.add_argument('--set-pivots', type=str,nargs='+',help='Set pivot values of fit. Set parameters with key and values separated by "=" sign. For instance: --set-pivots M=1.e14 a=0.7 omega_m=0.2 omega_b=0.04 sigma8=0.6 h0=0.7' )
    parser.add_argument('--set-fit-parameters', nargs='+', type=str,help='Set fit values of fit. Set parameters with key and values separated by "=" sign. For instance: --set-fit-parameters A0=3.2 B0=0. C0=0. alpha_m=-0.01. The keys to use for set parameters are %s'%(', '.join(__fit_parameter_names)))

    parser.add_argument('--show-fit-parameters', action='store_true', default=False, help='help show the fit parameters for the MC and MM fits. If --delta,--delta1 or --delta2 are set, then it will display only the fit parameters for the given overdensities')


    parser.add_argument('--concentration-from-mc-relation', action='store_true', default=False,help='Return the concentration in overdensity --delta (or --delta1) from Ragagnin et al. 2020 MC relation. The concentration depends on mass, scalefactor, and cosmological parameters. Set the parameters --M, -a, --omega-m, --omega-b, --sigma8 and --h0')
    parser.add_argument('--concentration-from-c', action='store_true', default=False,help= ' Return the concentration in overdensity --delta2,  given the concentration on overdensity --delta1. In case one of the two overdensities is "vir", then Provide also --omega-m, --omega-b, --sigma8 and --h0' )

    parser.add_argument('--use-lite-mc-fit', action='store_true', default=False,help= 'Uses parametrisation with B=B0 in Eq. 8 of Ragagnin et al. 2020')
    parser.add_argument('--use-lite-mc-dm-fit', action='store_true', default=False,help= 'Uses parametrisation with B=B0 in Eq. 8 and r_s computed on dark matter profile of Ragagnin et al. 2020')

    parser.add_argument('--mass-from-mc-relation', action='store_true', default=False,help='Computes mass in --delta2 given a MC relation and mass in --delta1.' )
    parser.add_argument('--mass-from-mm-relation', action='store_true', default=False,help='Computes mass in --delta2 given a mass in --delta1 using Ragagnin et al. 2020 MM relation.' )
    parser.add_argument('--mass-from-mass-and-c', action='store_true', default=False,help=' Computes mass in --delta2 given a mass and a concentration (use --c) in --delta1')

    parser.add_argument('--concentration-hu-kratsov-2002', action='store_true', default=False,help=' Computes concetatrion using Hu & Kratsov (2002) fit in Appendix B.')
        
    parser.add_argument('--debug', action='store_true', default=False,help='Show full stacktrace in case of error')

    args = parser.parse_args()
    args.personalise_fit_parameters=False;
    if args.set_pivots:
        for arg in args.set_pivot:
            if '=' not in arg:
                panic('Use --set-pivot values must be key/values separated by "=", found %s'%arg)
            k,v = arg.split('=')
            if k not in __fit_pivot_names:
                panic('Parameter in --set-pivot is not a valid pivot. Found "%s" but should be one of %s'%(k, ', '.join(__fit_pivot_names)))
            if re.match("^\d+?\.\d+?$", v) is None:
                panic('Values in --set-pivot must be floats, found "%s"'%(v))
            args.__dict__['pivot_'+k]=float(v)
        args.personalise_fit_parameters=True

    if args.set_fit_parameters:
        for arg in args.set_fit_parameters:
            if '=' not in arg:
                panic('Use --set-fit-parameters values must be key/values separated by "=", found %s'%arg)
            k,v = arg.split('=')
            if k not in __fit_parameter_names:
                panic('Parameter in --set-fit-parameters is not a valid pivot. Found "%s" but should be one of %s'%(k, ', '.join(__fit_parameter_names)))
            if re.match("^\d+?\.\d+?$", v) is None:
                panic('Values in --set-fit-parameters must be floats, found "%s"'%(v))
            args.__dict__[k]=float(v)

        args.personalise_fit_parameters=True


    not args.personalise_fit_parameters  and not args.show_fit_parameters  and not args.concentration_from_mc_relation  and not args.concentration_from_c  and not args.mass_from_mm_relation and not args.mass_from_mc_relation and not args.mass_from_mass_and_c and parser.print_help()
    args.personalise_fit_parameters and not (args.concentration_from_mc_relation or args.mass_from_mc_relation or args.mass_from_mm_relation) and panic("Use --personalise-fit-parameters only in combination with --concentration-from-mc-relation or --mass-from-mc-relation or --mass-from-mm-relation")
    (args.concentration_from_mc_relation  or  args.mass_from_mc_relation  or args.mass_from_mm_relation  ) and (args.M is None or args.a is None or args.omega_m is None or args.omega_b is None or args.sigma8 is None or args.h0 is None) and  panic("If you use  --concentration-from-mc-relation or --mass-from-mc-relation or --mass-from-mm-relation then you must set --M --a --omega-m --omega-b --sigma8 and --h0")
    args.mass_from_mass_and_c and args.c is None and panic('With --mass_from_mass_and_c you must set also the concentration in delta1 via --c')

    try:
        
        table = {}
        args.personalise_fit_parameters and (args.concentration_from_mc_relation or args.mass_from_mc_relation) and set_fit_parameters(table, **kw)
        args.personalise_fit_parameters and args.mass_from_mm_relation and   set_fit_parameters(table, **kw)
        if table=={}:
            table=None
        args.table = table
        args.concentration_from_mc_relation and  print('c_%s = %.3f'%(args.delta1, do_get_concentration_from_mc_relation(args.delta1, **args.__dict__)))
        args.concentration_from_c and  print('c_%s = %.3f'%(args.delta2, do_convert_concentration(args.delta1, args.delta2, args.c, **args.__dict__)))
        args.mass_from_mm_relation and  print('M_%s = %.3e'%(args.delta2, do_get_mass_from_mm_relation(args.delta1, args.delta2,  **args.__dict__)))
        args.mass_from_mc_relation and  print('M_%s = %.3e'%(args.delta2, do_get_mass_from_mc_relation(args.delta1, args.delta2,  **args.__dict__)))
        args.mass_from_mass_and_c and  print('M_%s = %.3e'%(args.delta2, do_get_mass_from_m_and_c(args.delta1, args.delta2,  **args.__dict__)))
    except  Exception as e:
        if args.debug:
            raise e
        panic('Error "%s": %s'%(type(e).__name__,str(e)))
if __name__ == "__main__":
    main()
