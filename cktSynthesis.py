# input files for sequential circuits should be in BLIF format
# input files for combinatorial circuits could be in Verilog/BLIF/Bench format. 
#But it sometimes gives error. So it is better to convert the verilog file to blif file at first.
import os
import subprocess
import random
import sys
import time

def generate_circuits(input_file, output_file):
    script = 'read_lib GSCLib_3.0.lib\n'
    script += 'read {}\n'.format(input_file)
    script += 'strash\n'

    # select random optimization sequence
    sel_commands = []
    for i in range(random.randint(1, len(commands))):
        c = random.randint(0, len(commands)-1)
        sel_commands.append(commands[c])
    script += ';'.join(sel_commands)
    script += '\n'
    script += 'map\n'
    script += 'stime\n'
    script += 'write_verilog {}\n'.format(output_file)

    print(sel_commands)

    script_file = out_dir + '/script.tcl'
    with open(script_file, 'w') as file:
        file.write(script)
    file.close()

    	
    #print(ckt_properties)
    ckt_properties = subprocess.check_output([abc_bin, "-f {}".format(script_file)])
    #print(ckt_properties.decode("utf-8"))
    with open(output_file, 'a') as file:
        #file.write(script)
        file.write(ckt_properties.decode("utf-8"))
    file.close()
    


if __name__ == "__main__":
    #abc_bin = "/usr/bin/berkeley-abc"
    commands = ['resub', 'resub -z',
            'rewrite', 'rewrite -z',
            'refactor', 'refactor -z',
            'balance']
    gen_samples = 5040

    benchmark_list = ['c17', 'c432', 'c499', 'c880', 'c880a', 'c1355', 'c1908', 'c1908a', 'c2670', 'c2670a', 'c3540', 'c3540a', 'c5315', 'c5315a', 'c6288', 'c7552']
    for benchmark_name in benchmark_list:
        path = os.path.join("/home/usr/abc_files/abc_output/",benchmark_name)
        os.mkdir(path)
        target_file = "/home/usr/abc_files/benchmarks/iscas85/"+benchmark_name+".blif"
        out_dir = "/home/usr/abc_files/abc_output/"+benchmark_name+"/"
        tic = time.perf_counter()
        for i in range(gen_samples):
            output_file = '{}/{}.v'.format(out_dir, benchmark_name+'_'+str(i))
            print('circuit {}: {}'.format(i, output_file))
            generate_circuits(target_file, output_file)
        toc = time.perf_counter()
        print("Total Running time {}".format(toc-tic))