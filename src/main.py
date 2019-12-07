from flow_network_generator import create_flow
from max_flow_generator import max_flow

flow_networks = [0] * 10

for i in range(0, 10):
    create_flow(i)

for i in range(0, 10):
    max_flow(i)



