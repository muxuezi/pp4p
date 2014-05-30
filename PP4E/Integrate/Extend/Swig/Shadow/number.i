/********************************************************
 * Swig module description file for wrapping a C++ class.
 * Generate by running "swig -c++ -python number.i".
 * The C++ module is generated in file number_wrap.cxx; 
 * module 'number' refers to the number.py shadow class.
 ********************************************************/

%module number

%{
#include "number.h"
%}

%include number.h
