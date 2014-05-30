# this file has been updated for Python 3.X
from tictactoe_lists import *

# game object generator - external interface 

def TicTacToe(mode=Mode, **args):
    try:
        classname = 'TicTacToe' + mode            # e.g., -mode Minimax
        classobj  = eval(classname)               # get class by string name
    except:
        print('Bad -mode flag value:', mode)
        raise   # reraise
    return eval(classname)(**args)                # run class constructor (3.x: was apply())


# command-line logic

if __name__ == '__main__': 
    if len(sys.argv) == 1:
        TicTacToe().mainloop()   # default=3-across, expert2
    else:
        # ex: TicTacToe.py -degree 5 -mode Smart -bg blue -fg white -fontsz 30
        needEval = ['-degree']
        args = sys.argv[1:]
        opts = {} 
        for i in range(0, len(args), +2):
            if args[i] in needEval:
                opts[args[i][1:]] = eval(args[i+1])
            else:
                opts[args[i][1:]] = args[i+1]      # any constructor arg
        trace(opts)                                # on cmd line: '-name value'
        TicTacToe(**opts).mainloop()               # 3.x: was apply
