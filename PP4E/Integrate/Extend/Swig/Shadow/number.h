class Number
{
public:
    Number(int start);             // constructor
    ~Number();                     // destructor
    void add(int value);           // update data member
    void sub(int value);
    int  square();                 // return a value
    void display();                // print data member
    int data;
};
