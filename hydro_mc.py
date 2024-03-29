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

#start of fit parameters
__mc_fit_parameters = {"vir": {"params": [1.503454114104443, -0.04283092691408333, 0.5157209989941997, 0.45445667750331026, -0.24856881467360964, 0.5544350140093234, -0.0048813484527866656, -0.12199409397642753, 0.11663423303800534, 0.05110946208460489, -0.07892747676338406, 0.24005903699741252, -0.1263499637381384, 0.6640188439939326, -0.0299567877892118, 0.3877956797872577], "pivots": {"M": 198759238503196.03, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}, "200c": {"params": [1.2436364990990914, -0.04817261898156871, 0.20419215885982817, 0.6316820273466903, -0.24605297432854378, 0.560570072125268, -0.02627068018190943, -0.11775877953823762, 0.11193584169417208, 0.05634549061614718, -0.043822582719200295, 0.3524426183203193, -0.03879420539288709, 0.7673900896521332, -0.27569460666976725, 0.3843115348866266], "pivots": {"M": 173960723876953.16, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}, "500c": {"params": [0.8637563855047179, -0.05344871238505832, 0.1878750841109432, 0.6618004570191556, -0.23490408373403376, 0.5190661049361811, -0.03143074979091932, -0.11241937064515797, 0.1257731196624856, 0.08805802745200282, -0.1563176516883163, 0.3463795016853568, -0.044602075614319794, 0.8564224417001306, -0.34652816060672165, 0.3765132317155449], "pivots": {"M": 137038782293146.31, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}, "2500c": {"params": [0.12656051215719555, -0.03050866662392269, 0.10725429255827736, 0.7593881752986629, -0.27160211703510345, 0.42181074155295156, -0.020575075642635738, -0.1163991007298093, 0.28880298414213335, 0.10263452464907902, -0.34222932053193433, 0.3844570767051972, -0.1334171989405518, 0.8457199265161256, 0.0028417430312315424, 0.3827347978288253], "pivots": {"M": 68722326105291.2, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}, "200m": {"params": [1.692410096240174, -0.040346034043160055, 0.9092242875122345, 0.2268328343963277, -0.2664240976376676, 0.5283845428748246, 0.015645163737334208, -0.11627375082296813, 0.11528658344781062, 0.05003254567973524, -0.09358485276497253, -0.04322554482713586, -0.06348838757477149, 0.6351347984085912, -0.40487997854959523, 0.3882554231750548], "pivots": {"M": 224397583007812.53, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}}
__mc_lite_fit_parameters = {"vir": {"params": [1.4985649929244846, -0.04754653951295999, 0.5199383344534508, 0.42335872983250744, -0.14123672388625216, 0.6530026638126829, -0.27667601800841235, 0.18958103942142024, 0.02371146453902725, 0.7637789994055261, -0.44859556264866146, 0.38803081506367154], "pivots": {"M": 198759238503196.03, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}, "200c": {"params": [1.2382820777898689, -0.053413793724654476, 0.20072654857310923, 0.603607539963483, -0.1521899342583827, 0.6467505386837067, -0.24540931053697695, 0.3595828585445649, -0.14575941582538823, 0.7247582262393436, -0.07329103607606331, 0.3845164814226978], "pivots": {"M": 173960723876953.16, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}, "500c": {"params": [0.8591961760288123, -0.05970360132842668, 0.18730552659285832, 0.6319223562569485, -0.13145810034048822, 0.6120793998567394, -0.2739015100800711, 0.33628042357787796, -0.04344994933928333, 0.8893178406086549, -0.4363827722023437, 0.3766897270799671], "pivots": {"M": 137038782293146.31, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}, "2500c": {"params": [0.12248240026576206, -0.03731339714808029, 0.11023256345276963, 0.72734695998088, -0.17862618662088695, 0.5163267659318049, -0.23053189558090148, 0.3593064374504373, 0.001045506046395887, 0.9380532152882959, -0.45993132673543496, 0.38286807046506977], "pivots": {"M": 68722326105291.2, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}, "200m": {"params": [1.6876665626182177, -0.04439299009821192, 0.9102898686541654, 0.20117611449430742, -0.18592086055940954, 0.6032760056708096, -0.17458924277519577, -0.09573339329894155, 0.0033439095394409493, 0.608072469993025, -0.3914462271263976, 0.3884769419509934], "pivots": {"M": 224397583007812.53, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}}
__mc_dm_lite_fit_parameters = {"vir": {"params": [1.6147833157974498, -0.03653643924892916, 0.5387731878631365, 0.2235973904479776, -0.03482719529568293, 0.5647576889755415, -0.06791394004084528, 0.04825806113259144, -0.03699590802199347, 0.5181350657778563, 0.058112733061820535, 0.49732992864301045], "pivots": {"M": 198759238503196.03, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}, "200c": {"params": [1.3646710162370588, -0.03994872573988859, 0.22971042288590945, 0.4018553382603236, -0.04873586208519482, 0.5407381274632099, -0.15735912238338862, 0.2484181316840925, -0.22372711779769497, 0.47113281527183, -0.1262945839495521, 0.4981430221720337], "pivots": {"M": 173960723876953.16, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}, "500c": {"params": [0.9785288098930186, -0.03885461349058336, 0.17813810471397806, 0.4562092312012737, -0.0844283000357409, 0.47202095163570484, -0.33185662366382357, 0.3427667412703562, -0.3709489464232765, 0.4978856094616349, -1.0860705258088728, 0.5063466555940676], "pivots": {"M": 137038782293146.31, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}, "2500c": {"params": [0.21319259819504097, -0.01544383363128253, 0.05466159499929143, 0.5881312963731252, -0.20367090026868506, 0.36261905823870594, -0.4709358214950252, 0.5090317463610325, -0.7263228265986462, 0.29973682920914935, -1.856442289282263, 0.48429006429598354], "pivots": {"M": 68722326105291.2, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}, "200m": {"params": [1.7976155441540107, -0.034095172349226, 0.9175740293353059, 0.008184806629000403, -0.07196912106941096, 0.5330560972093654, 0.02721684778176066, -0.233089714297092, -0.08679242774966536, 0.45285870483992335, 0.024278999082778235, 0.49888743097957355], "pivots": {"M": 224397583007812.53, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}}
__mm_fit_parameters = {"vir": {"200c": {"params": [32.716547549657776, 1.003624235982134, -0.24285174426894685, 0.16541934519101023, 0.0033936660265926786, 0.048050628901760484, -0.04459000278005045, -0.016200536421750403, 0.030030242515596328, -0.024342652536468334, -0.006676361566485594, 0.15869015700748806, -0.050311846483695695, 0.12304114439302616, 0.03552291505923428, 0.06454744597293166], "pivots": {"M": 198759238503196.03, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}, "500c": {"params": [32.31446170750654, 0.9957545596825734, -0.23650532119192375, 0.2948522939712546, -0.020389686318549444, 0.1768387756432282, -0.10495909929153542, -0.042692472722319866, 0.09641454792547807, -0.042888930408444256, -0.03783227262005023, 0.21319305053988458, -0.11521355529169561, 0.3540794241397968, 0.025691358051782416, 0.15784411582392668], "pivots": {"M": 198759238503196.03, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}, "2500c": {"params": [31.33961332257922, 0.9254279357105467, -0.0053270941693614494, 0.6190932916396321, -0.16217319698168417, 0.5740259662954277, -0.05432452884580115, -0.07581377233461492, 0.20315509596579287, -0.010241003783698724, -0.20257727811313234, 0.37895353769136536, -0.23205433590391472, 0.5549732387160674, 0.03894561657006593, -0.31215630263491023], "pivots": {"M": 198759238503196.03, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}, "200m": {"params": [33.043740627011175, 0.9943124075863463, 0.2313347126069795, -0.13806731562975613, -0.010240592809525413, -0.022999828518708895, 0.04060039791084734, 0.016727926541201598, -0.0222023048410995, 0.017025963386900593, 0.003578603780419614, -0.16977721619147226, 0.025905856208134456, -0.09040496944966961, 0.017859428165411285, -0.04185469196689413], "pivots": {"M": 198759238503196.03, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}}
, "200c": {"vir": {"params": [32.98886748964721, 0.9946954684713093, 0.23317589419011725, -0.15583130016402208, -0.0027649751672118965, -0.03537720517127878, 0.03694056315127605, 0.015235188635094389, -0.02604116709934822, 0.01659025441331936, 0.014502710755606715, -0.15279212057259547, 0.056976353804893874, -0.10718333934243857, -0.034684277786017556, 0.05574800104986218], "pivots": {"M": 173960723876953.16, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}, "500c": {"params": [32.393131973068954, 0.9937644168359898, 0.003275074957470214, 0.12510715614390733, -0.019920809376511372, 0.11980406971722012, -0.06043552298867497, -0.02465206855526117, 0.06223912280770675, -0.019749653610058062, -0.02461493467928295, 0.051887276561479075, -0.05205208121240217, 0.24350335440584456, -0.038285984050181535, 0.11297954816728545], "pivots": {"M": 173960723876953.16, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}, "2500c": {"params": [31.41292708395347, 0.9218754436147497, 0.22473262945872488, 0.46125388997842653, -0.14973283035644322, 0.5387745708530132, -0.04186337961525381, -0.05847813577142404, 0.17085378515815575, 0.005649589124360711, -0.1797170357421586, 0.21068318994679433, -0.07964314269044909, 0.48564804595024696, -0.17508445487715912, -0.2961086703422706], "pivots": {"M": 173960723876953.16, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}, "200m": {"params": [33.10619274508529, 0.988300056080471, 0.4578470359717449, -0.2879822751326564, -0.016796161356124422, -0.05303150212542579, 0.07762487233039962, 0.03063434190996475, -0.039732772400170854, 0.029499435116064416, 0.0174896515173054, -0.3134504603341965, 0.06237923922665093, -0.2010890652382813, 0.026078974733249775, 0.08368950274345158], "pivots": {"M": 173960723876953.16, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}}
, "500c": {"vir": {"params": [33.12321369014936, 0.9932788709016931, 0.2519043379398163, -0.2644290710899303, 0.0029966003732370358, -0.11078404266730466, 0.08420789410872768, 0.03424047108886404, -0.08263869850070836, 0.033127975943963626, 0.06422801120206824, -0.18986883526731976, 0.10090479702324148, -0.3733901777471524, -0.0174837312155619, 0.12918131911404912], "pivots": {"M": 137038782293146.31, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}, "200c": {"params": [32.92980304167373, 1.000432504899137, 0.015803790410215145, -0.11393514470414566, 0.006082046014311101, -0.08799950639275685, 0.058161722610182424, 0.019121493107348314, -0.052841009086270416, 0.01914838769890406, 0.036133433382039615, -0.033289631502490806, 0.0049598818431250535, -0.2807737776254389, 0.12986714906111868, 0.09604999325693657], "pivots": {"M": 137038782293146.31, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}, "2500c": {"params": [31.57535471760162, 0.9318722094794489, 0.21855959154186297, 0.33527661776578477, -0.1251191577173232, 0.40889832733341, 0.014617742399567287, -0.0325774515229764, 0.11450195454978987, 0.030586927383806823, -0.19658231425260478, 0.1621935539428323, -0.08091389620080668, 0.22342000901107478, -0.08328828716608871, -0.23543953158927047], "pivots": {"M": 137038782293146.31, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}, "200m": {"params": [33.23903345563792, 0.9865128591080334, 0.47790508411897487, -0.39461069560703277, -0.014848254125418958, -0.1263752449670363, 0.13012800037745717, 0.04947867680060586, -0.09691553298092222, 0.043457051853553925, 0.06942653018321447, -0.3517453874533708, 0.09306484852316713, -0.4697391694946282, 0.050691417663899, 0.1448990284901391], "pivots": {"M": 137038782293146.31, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}}
, "2500c": {"vir": {"params": [33.33250029698809, 1.0201182055583708, 0.15638196345692268, -0.5626207801067565, 0.09275325012892445, -0.342012899698197, 0.10337736735979336, 0.06292933100705556, -0.29955921366779437, -0.019140856382829426, 0.4118272633198809, -0.3055551331105463, 0.15201763720184808, -0.6379445332329354, 0.036814113820383625, 0.24202529082598515], "pivots": {"M": 68722326105291.2, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}, "200c": {"params": [33.13953071477643, 1.026891952032215, -0.07808336091126943, -0.4143648359670483, 0.09975057598004186, -0.31583036253406244, 0.06645483332317353, 0.04906929511499684, -0.2638546841822804, -0.03480980339878514, 0.3818221240976384, -0.15888388250674507, 0.07503360811985466, -0.5319793017394844, 0.14681359532192825, 0.22791963123847883], "pivots": {"M": 68722326105291.2, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}, "500c": {"params": [32.773474003459484, 1.0314903544118486, -0.09991206710669961, -0.30655844541924504, 0.0899261627701992, -0.25529881455381004, 0.019319160046123388, 0.02888210069554159, -0.18867246798751744, -0.0450691158276003, 0.31965039226923164, -0.1339260335822625, 0.046829695425163395, -0.26786469607363345, 0.042821693277460486, 0.18179748839481427], "pivots": {"M": 68722326105291.2, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}, "200m": {"params": [33.449928994127625, 1.0137672613631057, 0.3884270448825958, -0.6945245790633495, 0.07586049305592515, -0.35742671170676377, 0.13516778655853254, 0.07850133213044976, -0.32416434385441756, -0.014257525322939018, 0.44860092910474053, -0.4733572404757807, 0.17635892757694627, -0.7263246721102229, 0.001987326362323298, 0.24683192744384327], "pivots": {"M": 68722326105291.2, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}}
, "200m": {"vir": {"params": [32.91923993459246, 1.004998283710883, -0.24327974796307458, 0.146916873080803, 0.014085866496374992, 0.03403136832842445, -0.05495582811339603, -0.017709014761172495, 0.024922878675272438, -0.022277807902568742, -0.002687549490900499, 0.18766656690092864, -0.015980084879887904, 0.12354164631530422, -0.051383216549240274, -0.04852060193023841], "pivots": {"M": 224397583007812.53, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}, "200c": {"params": [32.7092432548728, 1.0078543539776024, -0.4923401628810212, 0.317991173206413, 0.013757313724573065, 0.08830533446268542, -0.10310730596591498, -0.035138014465154285, 0.06273672319138414, -0.05014998021686202, -0.010943256393764618, 0.35758349293839736, -0.10227564269822434, 0.24551406258367856, 0.03345997504983831, -0.10235368375951033], "pivots": {"M": 224397583007812.53, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}, "500c": {"params": [32.30590606420742, 1.0000540537767286, -0.4830289557913123, 0.4458649778490151, -0.013155061128686208, 0.21813115725504514, -0.15948649173162333, -0.06122690436674333, 0.12660113555523209, -0.07277092932568646, -0.04164041554251069, 0.4082628758536285, -0.17486998423199526, 0.47758038193650526, 0.013784564207430024, -0.1814127296908954], "pivots": {"M": 224397583007812.53, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}, "2500c": {"params": [31.33382470213857, 0.9313085568714797, -0.23360541371644739, 0.7538862738599599, -0.1582096612458364, 0.6036429135207855, -0.11084469907190307, -0.09380588110396984, 0.23204562989471772, -0.04050734632304558, -0.19328155795275154, 0.5642713366169192, -0.29968357150510994, 0.6506712481038401, 0.026156355100851708, -0.3181591586420962], "pivots": {"M": 224397583007812.53, "a": 0.8771929824561403, "omega_m": 0.272, "omega_b": 0.0456, "sigma8": 0.809, "h0": 0.704}}}
}
#end of fit parameters

__fit_parameter_names = ['A0','B0','C0','alpha_m','alpha_b','alpha_sigma','alpha_h','beta_m','beta_b','beta_sigma','beta_h','gamma_m','gamma_b','gamma_sigma','gamma_h','sigma']
__fit_parameter_lite_names = ['A0','B0','C0','alpha_m','alpha_b','alpha_sigma','alpha_h','gamma_m','gamma_b','gamma_sigma','gamma_h','sigma']
__fit_pivot_names = ['M','a','omega_m','omega_b','sigma8','h0']
__deltas = ['200c','500c','2500c','vir','200m']


def panic(x):
    sys.stderr.write(x+'\n')
    sys.exit(1)

def printf(x):
    sys.stdout.write(x+'\n')

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
        if parameter_name in kw and kw[parameter_name] is not None:
            value = kw[parameter_name] 
        else:
            value = 0.

        fit_parameter_values.append(value)

    table['params']=fit_parameter_values
    for parameter_name in __fit_pivot_names:
        if 'pivot_'+parameter_name in kw and kw['pivot_'+parameter_name] is not None:
            table['pivots'][parameter_name]=kw['pivot_'+parameter_name]



            


def fit_from_ragagnin2019_fit(table, pivots, use_lite_mc_fit=False, **kw):
    if not  use_lite_mc_fit:
        norm, slopem, slopea,   pim , pib, pis, pih,    sim, sib, sis, sih,       aim, aib, ais, aih, sigma = table
    else:
        norm, slopem, slopea,   pim , pib, pis, pih,     aim, aib, ais, aih, sigma = table

    logM, loga, logomega_m, logomega_b, logsigma8, logh0 = [np.log(np.array(kw[pivot]) / pivots[pivot]) if pivot in pivots else 0. for pivot in __fit_pivot_names]




    norm_2 = norm + pim* logomega_m +pib* logomega_b  +  pis * logsigma8  + pih * logh0
    if not  use_lite_mc_fit:
        slopem_2 = slopem  +sim* logomega_m +sib* logomega_b  + sis* logsigma8  + sih * logh0
    else:
        slopem_2 = slopem

    
    slopea_2 = slopea + aim*   logomega_m +aib* logomega_b  + ais* logsigma8  + aih* logh0

    return np.exp(norm_2 + logM*slopem_2 +  loga*slopea_2)

def concentration_from_mc_relation(delta, M, a, omega_m, omega_b, sigma8, h0, use_lite_mc_fit=False, use_lite_mc_dm_fit=False, show_fit_parameters=False, table=None, **kw):

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
        use_lite_mc_fit and use_lite_mc_dm_fit and     printf('\n Dark matter concentration with lite parametrisation: ') and    print_abc_equation(is_lite=True)
        use_lite_mc_fit and not use_lite_mc_dm_fit and     printf('\n Total matter oncentration with lite parameters: ') and    print_abc_equation(is_lite=True)
        use_lite_mc_fit and not use_lite_mc_dm_fit and     printf('\n Total matter oncentration: ') and    print_abc_equation()
        print('    Delta = %s'% delta)
        print_fit_params_and_pivots(table,is_lite= use_lite_mc_fit)

    return fit_from_ragagnin2019_fit( table['params'], table['pivots'],use_lite_mc_fit=use_lite_mc_fit,
                                         M=M,a=a,omega_m=omega_m, omega_b=omega_b, sigma8=sigma8, h0=h0,
                                         **kw)



def mass_from_mm_relation(delta_from, delta_to, M, a, omega_m, omega_b, sigma8, h0,  show_fit_parameters=False,  table=None, **kw):
    if show_fit_parameters:
                    print_fit_params_and_pivots(__mm_fit_parameters[delta_from][delta_to])
    if table is None:
        table = __mm_fit_parameters[delta_from][delta_to]
    return fit_from_ragagnin2019_fit( table['params'], table['pivots'],
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

def critical_overdensity(delta,  **args):
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
    

def convert_concentration(delta_from, delta_to, concentration, f_profile=None,  c_hu_kratsov_2002=False, **kw):
    overdensity_from = critical_overdensity(delta_from, **kw)
    overdensity_to = critical_overdensity(delta_to, **kw)
    if not  c_hu_kratsov_2002:
        if f_profile is None:
            f_profile = f_NFW
        return c2_bc(overdensity_to, overdensity_from, concentration, f_NFW=f_profile)
    else:
        return HK_1(overdensity_to, overdensity_from, concentration)

def mass_from_m_and_c(delta_from, delta_to, concentration,  **kw):
    c = concentration
    overdensity_from = critical_overdensity(delta_from, a=a, omega_m = omega_m, **kw)
    overdensity_to = critical_overdensity(delta_to,  a=a, omega_m = omega_m, **kw)
    new_c =  c2_bc(overdensity_to, overdensity_from, c)
    return    kw['M'] * (overdensity_to/overdensity_from)*(new_c/c)**3.


def mass_from_mc_relation(delta_from, delta_to, M, a, omega_m, omega_b, sigma8, h0,   **kw):
    overdensity_from = critical_overdensity(delta_from,  a=a, omega_m = omega_m,**kw)
    overdensity_to = critical_overdensity(delta_to,  a=a, omega_m = omega_m, **kw)
    c =  concentration_from_mc_relation(delta_from, M, a, omega_m, omega_b, sigma8, h0, **kw)
    new_c =  c2_bc(overdensity_to, overdensity_from, c)
    M = M* (overdensity_to/overdensity_from)*(new_c/c)**3.
    return   M

def split_kv(a,d, names,prekey=''):
    for arg in a:
        if '=' not in arg:
            raise Exception('Values must be key/values separated by "=", found %s'%arg)
        k,v = arg.split('=')
        if k not in names:
            raise Exception('Parameter is not a valid key=value pair. Found "%s" but should be one of %s'%(k, ', '.join(names)))
        try:
            d[prekey+k]=float(v)
        except Exception as e:
            raise Exception('Value  must be floats, in "%s" found "%s"'%(arg, v))
def main():
    parser = argparse.ArgumentParser(description='Magneticum Cosmological Masses and Concentration Converter')
    parser.add_argument('--delta1','--delta', type=str, help='Overdensity Delta for the MC relation', default=None)
    parser.add_argument('--delta2', type=str,help='Destination overdensity in case of mass-mass or concentration-concentration conversion', default=None)

    parser.add_argument('--M', type=float,help='Halo mass to be converted', default=None)
    parser.add_argument('--a', type=float,help='scale factor of halo to be converted',default=None)
    parser.add_argument('--omega-m', type=float,help='Omega_m parameter of the conversion',default=None)
    parser.add_argument('--omega-b', type=float,help='Omega_b parameter of the conversion',default=None)
    parser.add_argument('--sigma8', type=float,help='sigma8 parameter of the conversion',default=None)
    parser.add_argument('--h0', type=float,help='h0 parameter of the conversion',default=None)

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
    try:
        if args.set_pivots:
            split_kv(args.set_pivots,args.__dict__,__fit_pivot_names, prekey='pivot_')
            args.personalise_fit_parameters=True
            if args.set_fit_parameters:
                split_kv(args.set_fit_parameters,args.__dict__,__fit_parameter_names)


        not args.personalise_fit_parameters  and not args.show_fit_parameters  and not args.concentration_from_mc_relation  and not args.concentration_from_c  and not args.mass_from_mm_relation and not args.mass_from_mc_relation and not args.mass_from_mass_and_c and parser.print_help()
        args.personalise_fit_parameters and not (args.concentration_from_mc_relation or args.mass_from_mc_relation or args.mass_from_mm_relation) and panic("Use --personalise-fit-parameters only in combination with --concentration-from-mc-relation or --mass-from-mc-relation or --mass-from-mm-relation")
        not args.personalise_fit_parameters and (args.concentration_from_mc_relation  or  args.mass_from_mc_relation  or args.mass_from_mm_relation  ) and (args.M is None or args.a is None or args.omega_m is None or args.omega_b is None or args.sigma8 is None or args.h0 is None) and  panic("If you use  --concentration-from-mc-relation or --mass-from-mc-relation or --mass-from-mm-relation then you must set --M --a --omega-m --omega-b --sigma8 and --h0")
        args.mass_from_mass_and_c and args.c is None and panic('With --mass_from_mass_and_c you must set also the concentration in delta1 via --c')


        
        table = {"pivots":{}, "params":[]}
        args.personalise_fit_parameters  and set_fit_parameters(table, **args.__dict__)  and set_pivots(table, **args.__dict__)
        if table=={"pivots":{}, "params":[]}:
            table=None
        args.table = table
        args.concentration_from_mc_relation and  printf('c_%s = %.3f'%(args.delta1, concentration_from_mc_relation(args.delta1, **args.__dict__)))
        args.concentration_from_c and  printf('c_%s = %.3f'%(args.delta2, convert_concentration(args.delta1, args.delta2, args.c, **args.__dict__)))
        args.mass_from_mm_relation and  printf('M_%s = %.3e'%(args.delta2, mass_from_mm_relation(args.delta1, args.delta2,  **args.__dict__)))
        args.mass_from_mc_relation and  printf('M_%s = %.3e'%(args.delta2, mass_from_mc_relation(args.delta1, args.delta2,  **args.__dict__)))
        args.mass_from_mass_and_c and  printf('M_%s = %.3e'%(args.delta2, mass_from_m_and_c(args.delta1, args.delta2,  **args.__dict__)))
    except  Exception as e:
        if args.debug:
            raise 
        panic('Error "%s": %s'%(type(e).__name__,str(e)))
if __name__ == "__main__":
    main()
