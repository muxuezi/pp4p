#include "iostream.h"
#include "number.h"

main()
{
    Number *num;
    int res, val;

    num = new Number(1);            // make a C++ class instance
    num->add(4);                    // call its methods
    num->display();
    num->sub(2);
    num->display();

    res = num->square();                     // method return value
    cout << "square: " << res << endl;
    
    num->data = 99;                          // set C++ data member
    val = num->data;                         // fetch C++ data member
    cout << "data:   " << val << endl;
    cout << "data+1: " << val + 1 << endl; 

    num->display();
    cout << num << endl;            // print raw instance ptr
    delete num;                     // run destructor
}
