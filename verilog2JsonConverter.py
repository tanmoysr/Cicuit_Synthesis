import re
import json

# Load Library
with open('GSE_LIB_3.json') as json_file:
    GSE_LIB = json.load(json_file)
def verilog2jsonFn(filename):    
    circuit_org={'module_name':'',
                 'module_properties':{},
                'inputs':{},
                'outputs':{},
                 'nodes':{},
                'edges':{}}


    with open(filename, 'r') as f: #open the file 
        lines_all = ' '.join(f.readlines()[1:]).replace('\n','').split('ABC command line')
        lines= lines_all[0].split(';')[:-1]
        lines2 = lines_all[1].split('\x1b')
        circuit_org['module_properties']['WireLoad']=lines2[0][re.search('WireLoad',lines2[0]).span()[0]:].split('=')[1].strip()
        circuit_org['module_properties']['Gates']=float(lines2[1][re.search('Gates',lines2[1]).span()[0]:].split('=')[1].strip())
        circuit_org['module_properties']['Cap']=float(lines2[3][re.search('Cap',lines2[3]).span()[0]:].split('=')[1].strip(' ').split(' ')[0])
        circuit_org['module_properties']['Area']=float(lines2[5][re.search('Area',lines2[5]).span()[0]:].split('=')[1].strip())
        circuit_org['module_properties']['Delay']=float(lines2[7][re.search('Delay',lines2[7]).span()[0]:].split('=')[1].strip(' ').split(' ')[0])
    
        for line in lines:
    #         print(re.search(r'module$',line))
    #         print(re.search(r'endmodule$',line))
    #         print('------')
            if re.match(r' module',line):
                circuit_org['module_name']= line.split(' ')[2]
            elif re.search(r' input',line):
                input_list = line.split('input')[1].replace(' ', '').split(',')
                for input_pin in input_list:
                    circuit_org['inputs'][input_pin]={}
            elif re.search(r'output',line):
                output_list = line.split('output')[1].replace(' ', '').split(',')
                for output_pin in output_list:
                    circuit_org['outputs'][output_pin]={}
            elif re.search(r'wire',line):
                wire_list = line.split('wire')[1].replace(' ', '').split(',')
                for wire in wire_list:
                    circuit_org['edges'][wire]={}
            else:
                gate_type =(line.split('g')[0].replace(' ',''))
                connection_line = line.split('g')[1].replace(' ','')
                gate_index = int(connection_line.split('(')[0])
                circuit_org['nodes'][gate_index]= []
                circuit_org['nodes'][gate_index].append(gate_type)
                circuit_org['nodes'][gate_index].append(GSE_LIB[gate_type]['area'])
                circuit_org['nodes'][gate_index].append(GSE_LIB[gate_type]['cell_leakage_power'])                
                for k,v in enumerate(circuit_org['inputs']):
                    if re.search(v+'\)',connection_line):
                        circuit_org['inputs'][v][gate_index]=[]
                        indexes = re.search(v,connection_line).span()
                        pin_name=re.search('.(.*)'+connection_line[indexes[0]:indexes[1]], connection_line).group(1).split('.')[-1].split('(')[0] 
                        circuit_org['inputs'][v][gate_index].append(GSE_LIB[gate_type]['pins'][pin_name]['direction'])
                        circuit_org['inputs'][v][gate_index].append(GSE_LIB[gate_type]['pins'][pin_name]['capacitance'])
                        circuit_org['inputs'][v][gate_index].append(GSE_LIB[gate_type]['pins'][pin_name]['rise_capacitance'])
                        circuit_org['inputs'][v][gate_index].append(GSE_LIB[gate_type]['pins'][pin_name]['fall_capacitance'])
                        circuit_org['inputs'][v][gate_index].append(GSE_LIB[gate_type]['pins'][pin_name]['max_capacitance'])
                for k,v in enumerate(circuit_org['outputs']):
                    if re.search(v+'\)',connection_line):
                        circuit_org['outputs'][v][gate_index]=[]
                        indexes = re.search(v,connection_line).span()
                        pin_name=re.search('.(.*)'+connection_line[indexes[0]:indexes[1]], connection_line).group(1).split('.')[-1].split('(')[0] 
                        circuit_org['outputs'][v][gate_index].append(GSE_LIB[gate_type]['pins'][pin_name]['direction'])
                        circuit_org['outputs'][v][gate_index].append(GSE_LIB[gate_type]['pins'][pin_name]['capacitance'])
                        circuit_org['outputs'][v][gate_index].append(GSE_LIB[gate_type]['pins'][pin_name]['rise_capacitance'])
                        circuit_org['outputs'][v][gate_index].append(GSE_LIB[gate_type]['pins'][pin_name]['fall_capacitance'])
                        circuit_org['outputs'][v][gate_index].append(GSE_LIB[gate_type]['pins'][pin_name]['max_capacitance'])
                for k,v in enumerate(circuit_org['edges']):
                    if re.search(v+'\)',connection_line):
                        circuit_org['edges'][v][gate_index]=[]
                        indexes = re.search(v,connection_line).span()
                        pin_name=re.search('.(.*)'+connection_line[indexes[0]:indexes[1]], connection_line).group(1).split('.')[-1].split('(')[0] 
                        circuit_org['edges'][v][gate_index].append(GSE_LIB[gate_type]['pins'][pin_name]['direction'])
                        circuit_org['edges'][v][gate_index].append(GSE_LIB[gate_type]['pins'][pin_name]['capacitance'])
                        circuit_org['edges'][v][gate_index].append(GSE_LIB[gate_type]['pins'][pin_name]['rise_capacitance'])
                        circuit_org['edges'][v][gate_index].append(GSE_LIB[gate_type]['pins'][pin_name]['fall_capacitance'])
                        circuit_org['edges'][v][gate_index].append(GSE_LIB[gate_type]['pins'][pin_name]['max_capacitance'])

    with open(filename[0:-2]+'.json', 'w') as outfile:
        json.dump(circuit_org, outfile)   
# filename= 'c17_0.v'
# verilog2jsonFn(filename)
gen_samples = 5040
benchmark_list = ['c17', 'c432', 'c499', 'c880', 'c880a','c880g', 'c1355', 'c1908', 'c1908a', 'c2670', 'c2670a', 'c3540', 'c3540a', 'c5315', 'c5315a', 'c6288', 'c7552']
for benchmark_name in benchmark_list:
    directory = "D:/abc_outputs/"+benchmark_name+"/"
    for i in range(gen_samples):
            input_file = '{}/{}.v'.format(directory, benchmark_name+'_'+str(i))
            verilog2jsonFn(input_file)