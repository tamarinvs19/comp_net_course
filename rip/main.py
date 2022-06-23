from network import Network


def main():
    network = Network()
    network.json_load('network_schema.json')
    network.simulate(file_name='output.txt')
    

if __name__ == '__main__':
    main()

