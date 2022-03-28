# Cocotb + Icarus Setup

[Cocotb](https://github.com/cocotb/cocotb) is an open-source python-based alternative to SystemVerilog testbenches. Since python is a productive high-level language with a rich ecosystem of well-maintained libraries such as numpy, tensorflow and pytorch, using python for verification allows the direct usage of those libraries. Cocotb does not simulate the testbench itself. Instead, it interfaces with any of the following simulators:

* Icarus-Verilog
* Verilator
* Synopsys VCS
* Cadence Incisive
* [and more](https://docs.cocotb.org/en/stable/simulator_support.html)

While Verilator is a fast & widely used open-source simulator, I could not find an easy way to install it in windows. Therefore, I will use icarus-verilog.

## Setup anaconda, install cocotb

Install anaconda from [here](https://docs.anaconda.com/anaconda/install/index.html). Then create an environment and install needed packages.

```
conda create --name verify
conda install numpy
pip install cocotb
```

## Install Icarus & GTKwave

* [Icarus download](https://bleyer.org/icarus/)
* [GTK download](http://gtkwave.sourceforge.net/) - just extract the zip

## Run example

```
conda activate verify
make
```

View Waveform:
```
path/to/gtkwave.exe dff.vcd
```