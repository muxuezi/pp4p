/***************************************************************
 * Swig module description file, to generate all Python wrapper
 * code for C lib getenv/putenv calls: "swig -python environ.i".
 ***************************************************************/

%module environ

extern char * getenv(const char *varname);
extern int    putenv(char *assignment);
