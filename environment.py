import copy

from colorama import Back, Fore

import logger


class Environment:
    def __init__(self, store, parent, name):
        logger.debug(
            Back.LIGHTMAGENTA_EX +
            Fore.BLACK,
            "NEW ENVIRONMENT CREATED",
            Back.RESET,
            Fore.RESET)
        self.name = name
        self.parent = parent

        # global counter
        # self.number = counter
        # counter += 1
        self.dict = {}
        self.store = store

    def define(self, name):
        id = self.store.make_variable(name)
        self.dict[name] = id
        logger.debug(Fore.GREEN, "DEFINED NEW VARIABLE: ", name, " with id ", id)
        logger.debug(self.store)
        logger.debug(self)
        logger.debug(Fore.RESET)

    def assign(self, name, value):
        if name in self.dict:
            id = self.dict[name]
            self.store.assign(id, value)
            logger.debug(
                Fore.MAGENTA,
                "Assigning value",
                value,
                " to variable ",
                name, " with id ", id,
                Fore.RESET)
            logger.debug(self.store)
        else:
            self.parent.assign(name, value)
            logger.log(
                Fore.RED,
                "#### ERROR: Trying to assign to undefined variable",
                name,
                "###",
                Fore.RESET)

    def copy(self):
        new = Environment(self.store, self.parent, self.name)
        new.dict = copy.deepcopy(self.dict)
        return new

    def get(self, name):
        if name in self.dict:
            id = self.dict[name]
            value = self.store.get(id)
            logger.debug(
                Fore.YELLOW,
                "Getting variable ",
                name,
                " with id ",
                id,
                " = ",
                value,
                Fore.RESET)
            return value
        else:
            return self.parent.get(name)
            logger.log(
                Fore.RED,
                "#### ERROR: Trying to get value of undefined variable",
                name,
                "###",
                Fore.RESET)

    def __str__(self):
        return "ENVIRONMENT " + ":" + str(self.dict)

    # def __del__(self):
    #     #### BREAKPOINT HERE WHY IS THERE AN EXTRA ENVIRONMENT???
    #     print(
    #         Fore.RED +
    #         "################# DESTROYING ENVIRONMENT " + str(self.number) + " NAME: " + self.name + ":::" +
    #         str(self) +
    #         Fore.RESET)
