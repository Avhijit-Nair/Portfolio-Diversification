# Portfolio-Diversification
An IEEE Quantum Hackathon project exploring Qiskit Runtime. The goal of this project is to include a Qiskit Runtime routine in an already existing Qiskit Finance's Portfolio Optimization program. More specifically, the VQE part of the program implements Qiskit Runtime.

# Prerequisites to run a test:
- Install a git client
- Install docker

# How to test it:
- Clone this repository and move inside it.
```
git clone https://github.com/Avhijit-codeboy/Portfolio-Diversification.git
cd Portfolio-Diversification/qiskit-runtime
```
- Create the docker image from the given docker file.
```
docker build -t qiskitruntime:latest .
```
- Create a container from the resulting image of the previous step.
```
docker run \
  --rm -d --name qr-test-server \
  --volume="$(pwd)"/qiskit_runtime:/qiskit-runtime/qiskit_runtime \
  --volume="$(pwd)"/logs:/qiskit-runtime/logs \
  -p 8000:8000 \
  -e "NUM_WORKERS=4" \
  qiskitruntime:latest \
  bash start-test-server.sh
```
- Install Redis.
```
docker pull redis
```
- Run Redis by exposing the default port.
```
docker run -d --name qr-test-server-redis -p 6379:6379 redis
```
- Install test server dependencies from the root of the repository.
```
pip install -r requirements.txt
pip install -r requirements-server.txt
```
- Run the server while ensuring that Redis is running.
```
python qiskit_runtime/test_server/worker.py
```
- From a different terminal and from the root of the repository, run this command.
```
uvicorn qiskit_runtime.test_server:runtime --reload --reload-dir qiskit_runtime
```
- From a different terminal , run the `data_generator.py` helper script by switching over to the `portfolio_diversification` folder and note down the output values.
```
cd qiskit-runtime/qiskit_runtime/portfolio_diversification
python data_generator.py
```
- Run the Portfolio Diversification program and plug in the values obtained from previous step in the `params` key.
```
curl -X 'POST' \
  'http://127.0.0.1:8000/jobs' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "programId": "portfolio-diversification",
  "hub": "string",
  "group": "string",
  "project": "string",
  "backend": "string",
  "params": [
    "{\"rho\":rho,
    \"num_assets\":n,
    \"num_clusters\":q,
    \"optimiser\":{'name':'COBYLA','max_iter':50},
    \"ansatz\":ansatz,
    \"initial_point\":initial_point}"
  ]
}'
```
- The server will now return a `job_id`. You can check the status of the job by running the following command -
```
curl -X 'GET' \
'http://127.0.0.1:8000/jobs/<job_id>' \
-H 'accept: application/json'
```
- See the result of the job by executing -
```
curl -X 'GET' \
'http://127.0.0.1:8000/jobs/<job_id>/results' \
-H 'accept: application/json'
```
