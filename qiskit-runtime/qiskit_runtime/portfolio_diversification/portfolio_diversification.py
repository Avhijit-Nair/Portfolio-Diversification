import sys
import json
import numpy as np
from qiskit.finance.data_providers import *
from qiskit.circuit.library import TwoLocal

from qiskit.finance.applications.ising import portfolio_diversification

from qiskit.providers.ibmq.runtime import UserMessenger, ProgramBackend

import sys
sys.path.insert(0, '..') # Add qiskit_runtime directory to the path

from qiskit.providers.ibmq.runtime.utils import RuntimeEncoder, RuntimeDecoder
from qiskit.providers.ibmq.runtime import UserMessenger

def get_portfoliodiversification_solution(n, result):
        v = result.eigenstate
        if isinstance(v, StateFn):
            v = v.to_matrix()

        N = n ** 2 + n

        index_value = [x for x in range(len(v)) if v[x] == max(v)][0]
        string_value = "{0:b}".format(index_value)

        while len(string_value) < N:
            string_value = '0' + string_value

        x_state = list()
        for elements in string_value:
            if elements == '0':
                x_state.append(0)
            else:
                x_state.append(1)

        x_state = np.flip(x_state, axis=0)

        return x_state

def diversify_portfolio(backend: ProgramBackend, user_messenger: UserMessenger, **kwargs):
    """Function that does classical-quantum calculation."""
    
    rho = kwargs.pop('rho')
    n = kwargs.pop('num_assets')
    q = kwargs.pop('num_clusters')
    
    qubitOp = portfolio_diversification.get_operator(rho, n, q)
    optimizer = kwargs.pop('optimizer')
    initial_point = kwargs.pop('initial_point')
    ansatz = kwargs.pop('ansatz')
    
    vqe_inputs = {
        'ansatz': ansatz,
    'operator': qubitOp,
    'optimizer': optimizer,
    'initial_point': initial_point,
    'measurement_error_mitigation': True,
    'shots': 1024
    }
    
    backend_options = {
    'backend_name': backend.name()
    }
    
    job = provider.runtime.run(
    program_id='vqe',
    inputs=vqe_inputs,
    options=backend_options,
    callback=raw_callback
    )
    
    raw_result = job.result()
    quantum_solution = get_portfoliodiversification_solution(n,raw_result)
    ground_level = portfolio_diversification.get_portfoliodiversification_value(rho, n, q, quantum_solution)
    
    return quantum_solution, ground_level

def raw_callback(*args):
    intermediate_info = {
    'nfev': [],
    'parameters': [],
    'energy': [],
    'stddev': []
    }
    
    job_id, (nfev, parameters, energy, stddev) = args
    intermediate_info['nfev'].append(nfev)
    intermediate_info['parameters'].append(parameters)
    intermediate_info['energy'].append(energy)
    intermediate_info['stddev'].append(stddev)

def main(backend: ProgramBackend, user_messenger: UserMessenger, **kwargs):
    """This is the main entry point of a runtime program.

    The name of this method must not change. It also must have ``backend``
    and ``user_messenger`` as the first two positional arguments.

    Args:
        backend: Backend for the circuits to run on.
        user_messenger: Used to communicate with the program user.
        kwargs: User inputs.
    """
    result = diversify_portfolio(backend, user_messenger, **kwargs)
    user_messenger.publish(result, final=True)  

inputs = {'rho':rho,
         'num_assets':n,
         'num_clusters':q,
         'optimizer':{'name':'COBYLA','max_iter':50},
          'ansatz':ansatz,
          'initial_point':initial_point
         }
backend = Aer.get_backend('qasm_simulator')
user_messenger = UserMessenger()
serialized_inputs = json.dumps(inputs, cls=RuntimeEncoder)
unserialized_inputs = json.loads(serialized_inputs, cls=RuntimeDecoder)
portfolio_diversification.main(backend,user_messenger,**unserialized_inputs)
