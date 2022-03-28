# optimizer
Suppose a code takes an input, x, and spits out an output y.  It may be desireable to treat the code as a black box function, y=f(x), and optimize the input variable for some specific objective function.  This repo contains python code that can be used to wrap around third party codes and optimize an input variable.  The base optimizerClass.py provides a generic entry point interface that can be wrapped around pretty much any code.  The interfaces/ directory contains IO interfaces to explicit codes.  If a user desires to optimize an input variable in a new code, the user should add a new IO python class to the interfaces directory.  So far, single variable inputs are all that is included, but there will soon be multi-variable optimization.

This code was originally developed to wrap around the Heat flux Engineering Analysis Toolkit (HEAT), which can be found here:  
https://github.com/plasmapotential/HEAT

HEAT is a complex code for simulating tokamak power exhaust, and it takes as input MHD Equilibria, CAD files, and some 0D inputs (ie injected power).  Because these variables are so interdependent, it is difficult to manually scan through the various permutations of MHD EQ, CAD, and 0D inputs, to find an optimum.  The optimizer enables the user to scan through these inputs to find the optimum output.  For example, a user could optimize a CAD geometric feature to generate an optimum heat flux profile.

This repo is young and will grow over the coming months.  

This code was engineered by Dr. Tom Looby.  Questions can be directed to tlooby@cfs.energy
