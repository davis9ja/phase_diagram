import numpy as np
import sys, os
import pickle

sys.path.append('/mnt/home/daviso53/Research/reference_state_ensemble/')
import reference_ensemble as re

sys.path.append('/mnt/home/daviso53/Research/mixed_state_test/')
import pyci_pairing_plus_ph as pyci

sys.path.append('/mnt/home/daviso53/Research/im-srg_tensorflow/')
from main import main

if not os.path.exists('solved_mesh/'):
    os.mkdir('solved_mesh/')

paramPath = sys.argv[1]

g, pb = pickle.load(open(paramPath, 'rb'))

states = pyci.init_states()
hme = pyci.matrix(states, 0.0, 1.0, g, pb)
true = np.linalg.eigvalsh(hme)

ensemble = re.ReferenceEnsemble(6, g, pb, 'white', '', 'vac_coeffs')
opt_x = ensemble.optimize_reference(1)
ref1 = ensemble.refs.T.dot(opt_x)


data = main(4,4, g=g, pb=pb, ref=ref1, generator='white', output_root='vac_coeffs')

H0B, H1B, H2B, eta1B_vac, eta2B_vac = pickle.load(open('vac_coeffs/vac_coeffs_evolved.p', 'rb'))

hme = pyci.matrix(states, H0B, H1B, H2B, H2B)
eig = np.linalg.eigvalsh(hme)

solved_dict = {'g':g, 'pb':pb, 
               'gs_eig':eig[0], 
               'abs_error_gs':abs(eig[0] - true[0]), 
               'error_gs':(eig[0] - true[0]), 
               'eta1B_norm':np.linalg.norm(np.ravel(eta1B_vac)), 
               'eta2B_norm':np.linalg.norm(np.ravel(eta2B_vac))}

pickle.dump(solved_dict, open('solved_mesh/{}'.format(paramPath.split('/')[1]), 'wb'))
