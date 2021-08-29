from qiskit.finance.data_providers import *
from qiskit.circuit.library import TwoLocal

stocks = ["TICKER1", "TICKER2"]
n = len(stocks)
rho = np.ones((n,n))
rho[0,1] = 0.8
rho[1,0] = 0.8

data = RandomDataProvider(tickers = stocks,
                 start = datetime.datetime(2016,1,1),
                 end = datetime.datetime(2016,1,30))
data.run()
rho = data.get_similarity_matrix()
rho = -1 * rho
q = 1
ansatz = TwoLocal(qubitOp.num_qubits, 'ry', 'cz', reps=5, entanglement='full')
np.random.seed(10)  # seed for reproducibility
initial_point = np.random.random(ansatz.num_parameters)

print('rho - ', rho,'\n','n -',n,'\n','q -',q,'\n','ansatz - ',ansatz,'\n','initial point - ',initial_point)
