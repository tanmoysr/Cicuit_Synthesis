# Circuit Synthesis
This repository is related to implementaionl of using combinational and sequential synthesis tools like 'ABC', 'Yosys'. This project shows circuit synthesis for combinational circuit (ISCAS85) and sequential circuit (IWLS_2005/ISCAS).

## Tool setup
I will discuss about installation of two tools ([ABC](https://people.eecs.berkeley.edu/~alanmi/abc/), [NEOS](https://bitbucket.org/kavehshm/neos/src/master/) and [Yosys](http://www.clifford.at/yosys/)) here in linux environment (Ubuntu 20.04). 

### ABC setup
- Open terminal
- Run the following line

```console
tc@pc:~$ sudo apt install berkeley-abc
```
### NEOS setup
There are other ways to use ABC. One of those is using [NEOS](https://bitbucket.org/kavehshm/neos/src/master/). You can check the details from this [link](https://bitbucket.org/kavehshm/neos/src/master/). Only tricky part is linking libreadline.so.6. You can use the following commands in you linux terminal. It will solve the problem. I have used Ubuntu 20.04.

```console
tc@pc:~$ sudo apt-get install libreadline-dev
tc@pc:~$ cd /usr/lib/x86_64-linux-gnu/
tc@pc:~$ sudo ln -s libreadline.so.8.0 libreadline.so.6
```

### Yosys setup
- Open terminal
- Run the following line

```console
tc@pc:~$ sudo add-apt-repository ppa:saltmakrell/ppa
tc@pc:~$ sudo apt-get update
tc@pc:~$ sudo apt-get install -y yosys
```

## Converting bench to verilog file
```console
tc@pc:~$ berkeley-abc
abc> read_bench c17.bench
abc> write_verilog c17.v
```

## Making schematic diagram

```console
tc@pc:~$ yosys
yosys> read_verilog c17.v
yosys> synth -top c17
yosys> show c17
```

If you want to use customized library
```console
tc@pc:~$ yosys
yosys> read_liberty GSCLib_3.0.lib
yosys> read_verilog c17.v
yosys> show c17
```

## Circuit Synthesis

Very basic comands for circuit synthesis by using 'ABC'
```console
tc@pc:~$ berkeley-abc
abc> read_lib GSCLib_3.0.lib
abc> read c17.blif
abc> strash
abc> balance
abc> refactor
abc> map
abc> stime
abc> write_verilog c17.v
```

Here I posted the code for two types of circuits (sequential and combinational) syntheses. You need to define the installation path of 'ABC' and 'Yosys'. You can find the location by using following command:
```console
tc@pc:~$ whereis yosys
tc@pc:~$ whereis berkeley-abc
tc@pc:~$ dpkg -L berkeley-abc
```
For sequential circuit synthesis use blif format as input and run [cktSynthesis.py](/cktSynthesis.py).
For combinational circuit if you have verilog file, then use [v2blif_Converter.py](/v2blif_Converter.py) to convert the verilog format file to blif format. Make sure you have installed ABC and Yosys in your system. Then use [cktSynthesis.py](/cktSynthesis.py) for circuit synthesis.
If you want to use verilog file without converting to blif format then you can try NEOS also.

```console
tc@pc:~$ ./neos --use_verilog -e xorprob ./c17.v ./c17_enc.v 10
```

## Using Yosys for making CNF from Verilog
```console
tc@pc:~$ yosys
yosys> read_liberty GSCLib_3.0.lib
yosys> design -save lib
yosys> read_verilog c17.v
yosys> hierarchy -check
yosys> prep -flatten -top c17
yosys> proc
yosys> opt
yosys> fsm
yosys> opt
yosys> memory
yosys> opt
yosys> techmap
yosys> opt
yosys> sat -dump_cnf c17_cnf c17
```
## Benchmark
- [IWLS 2005 Benchmark](https://iwls.org/iwls2005/benchmarks.html)
- [ISCAS85 verilog format download link](http://www.pld.ttu.ee/~maksim/benchmarks/iscas85/verilog/)
