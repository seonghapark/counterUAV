
import urllib.request

# def get_nodelist():

url = 'http://beehive1.mcs.anl.gov/live-nodes.txt'
urllib.request.urlretrieve(url, './live-node.txt')
with open('./node-info.txt') as f:
    for line in f:
        cell = line.strip().split('|')
        if len(cell) > 2 and 'NULL' not in cell[-2] and 'NULL' not in cell[1] and cell[1].strip():
                print(line.strip().split('|'))
        # print('\n', "** description: ", line.strip(), ', node ID: ', nodeNAME[i])
        # nodeDescr.append(line.strip())ls
