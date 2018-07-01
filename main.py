import traceback
import os
import sys
from converter import Converter
from history import History

CONVERSION_OPTIONS = {
    1: "px -> rem",
    2: "rem -> px",
    3: "px -> rem -> px",
    4: "rem -> px -> rem"
}


def hr():
    print('________________________________________________________________\n')


def get_conversion_option():
    hr()
    for key, optionDescription in CONVERSION_OPTIONS.items():
        print(str(key) + ": " + optionDescription)

    print("0: Back to base selection")

    selected_option = input('\nEnter your option: ')

    try:
        selected_option = int(selected_option)
    except ValueError:
        selected_option = None

    return selected_option


def get_base():
    base = input('Enter base (1-16  or 0 to go back to paths selection): ')
    invalid_base = True

    while invalid_base:
        try:
            base = int(base)
            assert (base in range(0, 17))
            invalid_base = False
        except:
            base = input('Invalid base, please try again (1-16  or 0 to go back to paths selection): ')

    return base


def run(history, converter):
    hr()
    paths = []
    if history.length() > 0:
        history.print()
        read = input('\nEnter dir/file paths separated by pipeline or history indexes separated by space: ').strip()

        indexes = read.split()
        good_indexes_count = 0

        for index in indexes:
            try:
                index = int(index)
                if index in range(1, history.length() + 1):
                    paths.extend(history.get(index - 1).split('|'))
                    good_indexes_count += 1
            except:
                pass

        if good_indexes_count == 0:
            paths = read.split('|')
    else:
        paths = input('\nEnter dir/file paths separated by pipeline: ').split('|')

    for path in paths:
        if not os.path.exists(path):
            paths.remove(path)
        else:
            history.add(path)

    if paths:
        base = get_base()
        while base != 0:
            converter.set_base(base)
            option = get_conversion_option()
            while option != 0:
                if option in CONVERSION_OPTIONS:
                    for path in paths:
                        converter.set_path(path)
                        converter.run(option)
                else:
                    print('The entered option is invalid, please try again')
                option = get_conversion_option()
            base = get_base()
    else:
        print('The specified paths do not exist, please try again')


try:
    historyInstance = History('.history')
    converterInstance = Converter()
    if len(sys.argv) > 1:
        converterInstance.set_path(sys.argv[1]).set_base(int(sys.argv[2])).run(int(sys.argv[3]))
    else:
        while True:
            run(historyInstance, converterInstance)
except KeyboardInterrupt:
    pass
except:
    traceback.print_exc()
