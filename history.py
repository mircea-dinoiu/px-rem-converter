import pickle
import os


class History:
    def __init__(self, history_file_path):
        self.__history_file_path = history_file_path
        self.__history_file = None
        self.__history = []

        self.__load_history()

    def __load_history(self):
        try:
            file = open(self.__history_file_path, 'rb')
            history = pickle.load(file)
            file.close()
            assert(isinstance(history, list))

            self.__history = history
        except:
            pass

        self.__remove_nonexistent_files()

    def list(self):
        return self.__history

    def get(self, index):
        return self.__history[index]

    def length(self):
        return len(self.__history)

    def add(self, file):
        if file in self.__history:
            self.__history.remove(file)

        self.__history.insert(0, file)
        self.__remove_nonexistent_files()
        self.__save()

    def print(self):
        index = 0

        for file in self.__history:
            index += 1
            print(str(index) + ': ' + file)

    def __remove_nonexistent_files(self):
        history = list(self.__history)
        for file in history:
            if not os.path.exists(file) and file in self.__history:
                self.__history.remove(file)

    def __save(self):
        try:
            file = open(self.__history_file_path, 'wb')
            pickle.dump(self.__history, file)
            file.close()
        except:
            pass