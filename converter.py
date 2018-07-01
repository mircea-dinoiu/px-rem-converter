import re
import os


class Converter:
    def __init__(self, base=16):
        self.__base = base
        self.__path = ''

    def set_path(self, path):
        self.__path = path

        return self

    def set_base(self, base):
        self.__base = base

        return self

    def run(self, option):
        if option == 1:
            self.px_to_rem()
        elif option == 2:
            self.rem_to_px()
        elif option == 3:
            self.px_to_rem()
            self.rem_to_px()
        elif option == 4:
            self.rem_to_px()
            self.px_to_rem()

        return self

    def __px_to_rem_replacement_function(self, match):
        try:
            value = round(float(match.group(2)))
        except:
            raise Exception(match.group(0))

        if value == 0:
            return "{before}0".format(
                before=match.group(1)
            )
        else:
            if value == 1:
                return "{before}{value}px".format(
                    before=match.group(1),
                    value=value
                )
            else:
                value /= self.__base

                return "{before}{value}rem".format(
                    before=': ' if match.group(1) == ':' else match.group(1),
                    value=(value if value != int(value) else int(value))
                )

    def __rem_to_px_replacement_function(self, match):
        try:
            value = float(match.group(2))
        except:
            raise Exception(match.group(0))

        if value == 0:
            return "{before}0".format(
                before=match.group(1)
            )
        else:
            value *= self.__base

            return "{before}{value}px".format(
                before=': ' if match.group(1) == ':' else match.group(1),
                value=round(value)
            )

    @staticmethod
    def __replace_in_file(path, regex, replacement_function):
        if path.endswith((".scss", ".css")):
            file_in = open(path, 'r')
            file_in_lines = file_in.readlines()
            file_in.close()

            file_out_lines = []
            line_index = 0

            for line in file_in_lines:
                line_index += 1
                try:
                    line = re.sub(regex, replacement_function, line)
                except Exception as e:
                    print('Invalid value \'' + str(e) + '\' at ' + path + ':' + str(line_index))
                file_out_lines.append(line)

            file_out = open(path, 'w', newline='\n')
            file_out.writelines(file_out_lines)
            file_out.close()

    def __file_conversion(self, regex, replacement_function):
        if os.path.isdir(self.__path):
            for root, dir_names, file_names in os.walk(self.__path):
                for filename in file_names:
                    self.__replace_in_file(os.path.join(root, filename), regex, replacement_function)
        else:
            self.__replace_in_file(self.__path, regex, replacement_function)

    def px_to_rem(self):
        regex = '(\s|\(|:|-)([0-9]*\.?[0-9]*)px'
        self.__file_conversion(regex, self.__px_to_rem_replacement_function)

    def rem_to_px(self):
        regex = '(\s|\(|:|-)([0-9]*\.?[0-9]*)rem'
        self.__file_conversion(regex, self.__rem_to_px_replacement_function)