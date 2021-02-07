# input files for sequential circuits should be in BLIF format
# input files for combinatorial circuits could be in Verilog/BLIF/Bench format
import os
import subprocess
import random
import sys
import time
subprocess.__file__

def v2blif_fn(input_file, output_file):
    script = 'read_verilog {}\n'.format(input_file)
    script += 'hierarchy\n'
    script += 'proc\n'
    script += 'opt\n'
    script += 'memory\n'
    script += 'opt\n'
    script += 'techmap\n'
    script += 'opt\n'
    script += 'write_blif {}\n'.format(output_file)

    script_file = out_dir + "script.tcl"
    with open(script_file, 'w') as file:
        file.write(script)
    file.close()
    
    process = subprocess.run([yosys_bin, "-s", script_file], shell=False)


if __name__ == "__main__":
    yosys_bin = "/usr/bin/yosys"

    benchmark_list = ['c17', 'c432', 'c499', 'c880', 'c880a', 'c880g', 'c1355', 'c1908', 'c1908a', 'c2670', 'c2670a',
                      'c3540', 'c3540a', 'c5315', 'c5315a', 'c6288', 'c7552.v']
    for benchmark_name in benchmark_list:
        print(benchmark_name)
        target_file = "/home/usr/abc_files/benchmarks/iscas85/" + benchmark_name + ".v"
        out_dir = "/home/usr/abc_files/benchmarks/iscas85/"
        tic = time.perf_counter()
        output_file = "/home/usr/abc_files/benchmarks/iscas85/" + benchmark_name + ".blif"
        v2blif_fn(target_file, output_file)
        toc = time.perf_counter()
        print("Total Running time {}".format(toc - tic))