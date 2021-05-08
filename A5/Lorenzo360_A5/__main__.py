'''Lorenzo360_A5 main programm'''
import argparse,os

def main():
    import Lorenzo360_A5
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', action='version', version='Lorenzo360_A5 '+Lorenzo360_A5.__version__)


    import Lorenzo360_A5.commands.Administration
    import Lorenzo360_A5.commands.HelloWorld
    import Lorenzo360_A5.commands.KLetShuffle
    import Lorenzo360_A5.commands.Manhattan
    import Lorenzo360_A5.commands.MonoShuffle
    import Lorenzo360_A5.commands.RollingDice
    import Lorenzo360_A5.commands.WordCount


    modules=[Lorenzo360_A5.commands.Administration,
    Lorenzo360_A5.commands.HelloWorld,
    Lorenzo360_A5.commands.KLetShuffle,
    Lorenzo360_A5.commands.Manhattan,
    Lorenzo360_A5.commands.MonoShuffle,
    Lorenzo360_A5.commands.RollingDice,
    Lorenzo360_A5.commands.WordCount,
    ]

    subparsers = parser.add_subparsers(title='Choose a command')
    subparsers.required = 'True'


 

    for module in modules:
        this_parser = subparsers.add_parser(get_str_name(module), description=module.__doc__)
        module.add_args(this_parser)
        this_parser.set_defaults(func=module.main)

    try:
        args = parser.parse_args()
        args.func(args)
    except Exception as e:
        print(parser.print_help())

def get_str_name(module):
        return os.path.splitext(os.path.basename(module.__file__))[0]


if __name__ == '__main__':
    main()
