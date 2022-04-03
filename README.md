# Cocotb + Icarus Setup

[Cocotb](https://github.com/cocotb/cocotb) is an open-source python-based alternative to SystemVerilog testbenches. Since python is a productive high-level language with a rich ecosystem of well-maintained libraries such as numpy, tensorflow and pytorch, using python for verification allows the direct usage of those libraries. Cocotb does not simulate the testbench itself. Instead, it interfaces with any of the following simulators:

* Icarus-Verilog
* Verilator
* Synopsys VCS
* Cadence Incisive
* [and more](https://docs.cocotb.org/en/stable/simulator_support.html)

While Verilator is a fast & widely used open-source simulator, I could not find an easy way to install it in windows. Therefore, I will use icarus-verilog.

Cocotb-test is a pytest-based library that wraps around cocotb and simplifies the make system. Advantages are:

* Specifying makefile is also done in python
* Can run the same test with different parameters automatically

## Setup anaconda, install cocotb

Install anaconda from [here](https://docs.anaconda.com/anaconda/install/index.html). Then create an environment and install needed packages.

```
conda create --name verify
conda install numpy
pip install cocotb cocotb-test
```

## Install Icarus & GTKwave

* [Icarus download](https://bleyer.org/icarus/)
* [GTK download](http://gtkwave.sourceforge.net/) - just extract the zip

## Run example

```
conda activate verify
pytest tb/
```

View Waveform:
```
path/to/gtkwave.exe sim_build/WIDTH_IN=16/dff.vcd
```