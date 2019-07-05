#  ____   ___  _     ___ ____
# / ___| / _ \| |   |_ _|  _ \
# \___ \| | | | |    | || | | |
#  ___) | |_| | |___ | || |_| |
# |____/ \___/|_____|___|____/


# Staticaly typed languages - C++, JAVA - Abstract classes and interfaces
# Dynamicaly typed languages - Ruby, Python - Duck Typing and protocols -
#                              PEP and conventions Zen of Python
# - https://www.python.org/dev/peps/pep-0234/#abstract
# - import this

# Why interfaces exist? To get around the diamond problem.

# SOLID is about mid-level software structures called classes or something else
# show what you mean by level in a context
# IF is the thing you wanna get away from

# #############################################

# SRP: A module should be responsible to one, and only one actor.
# keywords: actor, client

# 1- accidental duplication
# 2- merge conflicts

# PROBLEM #1: too many people asking too many changes in one place

class Employee(object):
    def calculate_pay(self): # ordered by COO
        return self.calculate()

    def report_hours(self, hours): # ordered by CFO
        return self.calculate() * hours

    def save(self): # ordered by CTO
        pass

    def calculate(self): # impacts `calculate_pay` and `report_hours`
        pass

# SOLUTION #1: separate the logic into different classes based on the "scope" of the problem

class PaymentCalculator(object):
    def calculate_pay(self, employee): # ordered by COO
        return self.calculate(employee)

class Reporter(object):
    def report_hours(self, employee): # ordered by COO
        return self.calculate(employee)

class EmployeeRepository(object):
    def save(self, employee): # ordered by COO
        pass

# OCP: open for extension, close for modification
# keywords: extension-not-changes

# PROBLEM #1: I need to know the type inside the method to get what I want

class Operation(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Addition(Operation):
    pass

class Subtraction(Operation):
    pass

class BasicCalculator(Calculator):
    def calculate(self, operation):
        if isinstance(operation, Addition):
            return operation.x + operation.y
        elif isinstance(operation, Subtraction):
            return operation.x - operation.y

# SOLUTION #1: delegate to object, not touching on BasicCalculator to add new operations

class Operation(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Addition(Operation):
    def peform_operation(self):
        return self.x + self.y

class Subtraction(Operation):
    def peform_operation(self):
        return self.x - self.y

class BasicCalculator(Calculator):
    def calculate(self, operation):
        return operation.perform_operation()

# PROBLEM #2: flag parameter to dictate behaviour of another class, bad, bad, very bad

class Printer(object):
    def print(self, filename):
        pass

class ColorPrinter(Printer):
    def print(self, filename):
        HPLASER.print_file(filename)

class BWPrinter(Printer):
    def print(self, filename):
        HPINKJET.print_file(filename)

class ReportGenerator(object):
    def print(self, filename, ink_type):
        if ink_type == 'BLACK':
            BWPrinter.print_file(filename)
        else ink_type == 'COLOR':
            ColorPrinter.print_file(filename)
        else:
            raise BaseException("There is no printer for that type")

# SOLUTION #2: delegate instead of ifs

class Printer(object):
    def print(self, filename):
        pass

class ColorPrinter(Printer):
    def print(self, filename):
        HPLASER.print_file(filename)

class BWPrinter(Printer):
    def print(self, filename):
        HPINKJET.print_file(filename)

class ReportGenerator(object):
    def __init__(self, printer):
        self.printer = printer

    def print(self, filename, ink_type):
        self.printer.print_file(filename)

# LSP: A o1 of type S can be replaced o2 of type T with no behaviour changes if S is subtype of T
# keyword: Behaviour

# Preconditions cannot be strengthened in a subtype.
#   precondition is a condition or predicate that must always be true just as prior the changes
# Postconditions cannot be weakened in a subtype.
#   postcondition is a condition or predicate that must always be true just as after the changes
# Invariants of the supertype must be preserved in a subtype.
#   assertions that used to be true on runtime prior the changes
# History constraint (the "history rule").
#   ...

# PROBLEM #1: behaviour of rectangle is not the same as a square

class Rectangle(object):
    pass

class Square(Rectangle):
    pass

class ShapeCalculator(object):
    def calculate_perimeter(self, shapes):
        return len(shapes) * shapes.x * 2


# SOLUTION #1: not all shapes behave the same way

class Shape(object):
    def get_perimeter(self):
        return self.x * 2 + self.y * 2

class Rectangle(Shape):
    pass

class Square(object):
    pass

class ShapeCalculator(object):
    def calculate_perimeter(self, shapes):
        return sum(shape.get_perimeter() for shape in shapes)

# PROBLEM #2: not all tasks behave the same way. The behaviour changes not the number of methods

class Task(object):
    status = None

    def close(self):
        self.status = 'CLOSED'

class BasicTask(Task):
    pass

class ProjectTask(Task):
    def close(self):
        if (self.status == 'STARTED')
              raise Exception("Cannot close a started Project Task");

# ISP: client should be forced to depend on methods it does not use
# keyword: too-many-methods

# PROBLEM #1: a lot of methods not being used

class Charger(object):
    def charge_usb1(self):
        IOUSB1.connect(phone)
    def charge_usb2(self):
        IOUSB2.connect(phone)
    def charge_apple(self):
        IOAPPLE.connect(phone)

class AndroidCharger(Charger):
    pass

class AppleCharger(Charger):
    pass

# SOLUTION #1: abstract the methods and delegate. Leave details to implementation

class Charger(object):
    def connect(self):
        pass
    def disconnect(self):
        pass
    def charge(self):
        pass

class AndroidCharger(object):
    def connect(self):
        IOUSB2.connect(phone)

class AppleCharger(object):
    def connect(self):
        IOAPPLE.connect(phone)


# PROBLEM #2: one method is not being used in one of the implementations

class CoffeeMachine(object):
    def brew_filter_coffee(self):
        pass
    def add_ground_coffee(self):
        pass
    def brew_espresso(self):
        pass

class BasicCoffeeMachine(CoffeeMachine):
    pass

class EspressoMachine(CoffeeMachine):
    pass

# SOLUTION #2: add another level of inheritance

class CoffeeMachine(object):
    def add_ground_coffee(self):
        pass

class FilterCoffeeMachine(CoffeeMachine):
    def brew_filter_coffee(self):
        pass

class EspressoCoffeeMachine(CoffeeMachine):
    def brew_espresso(self):
        pass

class BasicCoffeeMachine(FilterCoffeeMachine):
    pass

class EspressoMachine(EspressoCoffeeMachine):
    pass

# DIP: high level modules and low level modules should depend on abstractions
# keyword: conform-to-interface-contract, program-to-abstraction-rather-than-implementation

# PROBLEM #1: no contract == ifs

class CopyProgram(object):
    devices = {'printer': Printer, 'disk': Disk}

    def __init__(self, device):
        self.device = device

    def copy(self):
        with ReadKeyboard() as c:
            if self.device == self.devices.get('printer'):
                WritePrinter(c)
            else:
                WriteDisk(c)

# SOLUTION #1: establish a contract (interface) between the classes inverting the dependency

class Reader(object): # interface
    pass

class Writer(object): # interface
    pass

class KeyboardReader(object):
    pass

class PrinterWriter(object):
    pass

class CopyProgram(object):
    def copy(self, reader, writer):
        with reader() as c:
            writer(c)

# PROBLEM #2: program to implementation is bad

class Lamp(object):
    def turn_on(self):
        pass
    def turn_off(self):
        pass

class Button(object):
    def __init__(self, lamp):
        self.lamp = lamp # What is the target object?

    def get_physical_state(self):
        pass

    def detect(self):
        button_on = self.get_physical_state() # What mechanism is used to detect the user gesture?
        if button_on:
            self.lamp.turn_on()
        else:
            self.lamp.turn_off()

# SOLUTION #2: dependency inverted for contracts(abstraction) rather than implementation

class ButtonClient(object):
    def turn_on(self):
        pass
    def turn_off(self):
        pass

class Button(object):
    def __init__(self, button_client):
        self.button_client = button_client # What is the target object? Irrelevant!

    def detect(self):
        button_on = self.get_state() # What mechanism is used to detect the user gesture? Irrelevant!
        if button_on:
            self.button_client.turn_on()
        else:
            self.button_client.turn_off()

    def get_state(self):
        pass

class Lamp(ButtonClient):
    pass

class ButtonImp(object):
    pass



# reference:
# http://butunclebob.com/ArticleS.UncleBob.PrinciplesOfOod
# https://stackify.com/interface-segregation-principle/
# https://martinfowler.com/bliki/FlagArgument.html
# ;:,,::,,;,:;:;:::,,,::.,,:,:::,,:,,,:::::,::,,:,:,,,,,,...,,.,,,,::::::,.```,,....,,..`..,,....,,......,.,......,,,.,:,:,,;,,,,,:''':,,:+:;;;++;@@#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# :;,::::;;:;:;;:,;::::,,,:::::,,::,::,:,:::,:,:::,,,,,,.,,.,.,,.,.,.....```...`....`......,..,,,...,,..............,.,,:,,:::,:::#;+;;;;,;:+'';;''@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# :;;:::::;;;;:;:::::;:.:::::,,,:::,:;:,,:,,:;,,::,,,,,.:.,,,,:......`.`...``...``...,`......,.....,......,.........,.,,:,,::::;,;:;#;@;:;:'':+';##@@#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ;:;:,,,::,:::::::::,,,,:::,::;::,::::::::::,,,,::::,,,,,:,,,,...```....`..```.`.............,...................,..,,,:,,;:::::'';'';::+::;';'+@@'@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ,:,,,.,::.;:,:,,:,,,:,;,:::,:;:,,,;;:,:::,::,,:::,,,::::.,.,..``.......`...`.`................,..................,...,,:,:::;::'##'+'++:;'+''+;'@#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# :,,.`.,;;:,::::,,:::::::;:,::,:,::,,,:::::::;:;:,::,,;,,:,,....`..``....`............,..,,,,,.,.,...............,....,,:,:::;;,'@@';'+;:#'#;#;+@+#;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ::..`.::;;:;';;,:;:;:;,::::::,,,;;::;,:,,:::;;::::;:::,:,,...........`....`...,`..,.,.,`.............,.............,..,,,,,:;:,;+@'+#+@;;':+'@@@#+##@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ,,.`..,,::;;;;',:,:::::.::,;,,:;::::,,:::::::::::;;:,,,,:,.....................,............,,,.,......,...........,.,,,,,,:;:,#'@''##++';##+#+@@@##@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ,,.......,,,::,,,:::;:::::::::;,:::::::::;;;:::,':,,,,:....................,.....,......,...,........,.................,,,,:::,+@''##+#+';@'##@#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ...,,...`....::,:,:;,,:::,:,:;,,,:,,,:::;;::;,::+',,,;.,...............``....,,.........,.,,..,,........,..........,..,.,,,;::,++++#@@#@@@@#@@#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# .,,,,,....,,,:,,.,,,:.::,,:,:,,,:,,,,,,;:,;:,,::,,;:,:,........``..............,,....,,.,,.,.......,....,.............,,,,::,::;'#+#@@##@@@@@#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ,:,,,,,,,;++++..,,,,::.,:,,,,,,:,,:.,,;,,;,::::,..,,':.,`..``..............`...``....................................,,.,,::,:,:@@+@@@@#@@@@#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ,,,,,,:'+'':::,,,,.,::,,:,:,:,,.,..,,,.,:::::,....,,.,+:......,...,.............`........................,,...........,,,.,,,,:,#+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ,,,,,,':....,,....,.,..,,:::::...,,,...:,:,,.....,,,...,#..`........,....`......`.........................,............,,,..,,::@+'@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ::,,,+......,,.,,,,,.,.,.:::,...,.,,,:,;:,::.....,:.,...`;#.``....`...,,................................................,....,,:@@@@@#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ,:,:'`.....,,....,,...,,;,:,....,:,,:..,:,,,.....,......`.,;+`,.................`..`.....,`............................,.....,,:@@@@#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ,:;,.`.....,,,,...,.,:,:,,...,:::,,,,.:...,,...`,..,..,.....;''........................::;,;:,;:...,..........,........,,....,,,@@@@#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ::.........,,:......,:,..,..:,.,,,:,,::,,.,.....,......`.....,,+:``.....,,`...`..`...::,,,:..+';::,..,................,,,...,,,,@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ,,..```.`..,:;......,,,.,:;::,;:,:,,:,:,,,.,........,...,...,.,;.#,``..`...`.......,..`.,.,:;,::;;,,.,..............,,,,,....,,,@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ,,.```.....,,:.........,,:::.::,;:::;:,,,,,,...,....`,..........;:.#,,...,.,.,,.,,,.......,.,,:,;,,:,,,,......,.....,.,.,...,,,,@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ,,,.``...,.,,:..`.......,.:,.,,:,,,:,,,,,...,...,....,.......,...,;.,#.,,,,,,,,,.......,,...,,,:,;:;;.,,,,:,,......,,.:,,.,...,'@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ,,..............``......`.:,,:;::::::,.,.,....,..,......`,........,;,.;+.,,.,,,,.,,,,..`...,:,,.;,;;';';::,.,.,....,.,,,..,..,,#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ,,,.............```..,...`,.,.,,,:..,,,.,,,,.,,......,.....,....,.,,:,,.''....,..,....,.......,,.:;;;'';::,:'::,,,,..,.,...,,,,@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# .,,......``.,,..........,..,.,,.,,...,,,,,,.,.,,,..,.....`..........,::,,.+;..,..,.,.....,,,.,.,,,:;;;:;;',,;',:.,,..,.,...,,,:#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ,......,```..,,.....,.......,....,,,.,,,.,,,,,,,..,..,,,..,.....`...,.:;,,..#,,,,,,,,,,,,,,:,,,,,,:;:;;;;;;,+:::,,,,:.,,..,,,,:'#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ,.......,`...:,......,``.......,.,,.,,.,,,.,.,.,,,.,,.,......,,,....,,,:;::,,,#::,::;'+####@;#;:::;:::;;';::;::::,.,,,,,.,,:,::;;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ,,,.,....,.,.::....,.............,.,,.,,,,,.,,.,,...,,,...........`.,.,,:::.:;+'+;++';:+,#''@#+##+;;;'';'';;;;;::,,:,,:,.,,,,:;:;+++@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ..,,......,,.,:,..........,,,.,,,.,,,,,.,,,,...,.,,,,...,.,``........,,,,:::,,,:,;+,, ,;++#@''+##+#''''+''';;;;;,,:..,:,,,:,,:;';;#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ..,,........,;;...,..,....,,,...,,,,..,,..,..,..,,,,..,,,,,,......`...,.,.,,:,,,...''@:;;;'';;:+#+#+';'''+';';;:,:..,;,,,:,::;;;'''#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ..,...............,,,,,..,.,..,.,..,,,..,,...,,,,,..,.,,....,.,.,...........,,,.,.```@@,;;;::',:+;';;;;;';;:;;:::.,,,:,::::::,;;'+'#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ,,..........``....,,..,,,,,,,,,,.,,,,.,...,..,..,,.,,.,....,.................,,:,..`.#;'`';;;,.;''+###+ +';:;;:,.,,,:::;:;;:;;;;';@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# .,.............,..,,..,.,,,.,,..,..,...,....,,.,..,.,,.,.,......`........,.....,,,....,,.;#,.`##',,:,.....:+#,..,,,,;:;;;:::;''''+##@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ,,................,,,.,,.,.,......,.,..,..,..,,,,,,...,..,,,....................,,:.....,,`:`.;,:,,,......,..:#`,,:;;'';;''+'+'''@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ,,...............,,..,,,,,,,.,,,,..,.....,,.,.,...,,,.,..................,......,,,:::.,.,,,++,,:,,........,,,,#`,:++####+''#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ::,...............,..,..,,,,.,,,,.,....,.,.....,..,...........`......,...........,,;':,,..`##.:::,,,.,..........#.;@ ######'#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# #,,,..............,..,,:.,,.,.,.,,,.......,.,..,,,,,,,..,.......................,,,:'::,,,'#,:::::,,,,,,.........'@@##+##@@@@#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ++,,..............,,,,,,,,,,,.,.,,.............,,..,,...............,...,.,.....,,,:::::::#;;:;:;;;:::::::,,,:,,.#;+++##@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# '++:,,........`..,,,,,,,,,..,,..,,,..,.,.,.....,....,,.,...........,......,,,...,,,,,:::::+'';;;;'';;;';;;;;;::,,;,';'@@#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# :++#:,,,....,,...,,.,,,,,,,,,,....,...,......,.......,...,.........,.....,..,.,,,,,,,::;:@+++';';+'';+++''''';;;+;,;'#@@@#@@##+##@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ,:'+++,,,,,,,,,,.,,.,,,,,,,,.,,,,,,...........,,,,,,..,,,,......,.,.....,...,.,,.,,.,,::''++#+'';+'''++''';;,,,':#..:+##@@'++'#+@@@++#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ..:;++#+;,,:+:,,..,,,,,,,,,,.,,.,,.,.,..,....,...,,.,.,,:,:....,.........,....,,..,,,,,::++++'''+'';''';:,.....;:#;,.'#@;+'#@@@@+@@###@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ,.,,,;++'+++::,,,.,,,:.,,,,.,.,,,,.....,...,,.,.,.,.,.,,,,:..,...,................,,,,,;'+++';''';:,,,,...,.``+,+.,;:++@;@@@@@@@@+###@#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ,..,..,,,:,,::,,,.,,,,,,,,.,.,.,,,...........,.,..,,,,,,,,,,.......,.....,........,..,,;'+'''';:,.,....`, `..',:+..:''#'`@##@@@@@#++@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ,,.,..,,.,,,:,,.,.,,,,,,,,,,,,...,..........,,`,,...,,,,,,,...,.,.......,............,;;;+''';:......```` ,,`,,+..,.+@''#@@@@@@@#####@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# .,.,..,,,,,,,,:,.,,,,.,,,,.,,..,.......,....,.,.,,,,,,,,.,,,,,,.....,..,..............:;;''';,..``.`.````,`,:,;,...,##,##@@@@@@####@##+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# .,,,,.,,,.,,,,,,,,.,,,.,,,,.,.,...,.,.......,...`..,,,.,,,.,.....,.,,,`..,............;::;':,....``````.`;;:,:'....,++##@@@@@@@###@@@##@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ,,,,,,.,,,,,:,,:,..,,,.,.,.,,,.,.....,.............,,,,,,...,.,.,,...,..............`,;.,,,....`````````.::,:,.....,,'@@@@@@@@###@@@@@#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##
# ,...,.,,,.,,:,::,,,::,,,,.,,,.,.,..,.........,.,,,.,,,,,,,,....,...,,,..,............:;.,......````.````.,,:.......,,@#@@@@@@@##@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##++''
# ,..,,,,,,.:,,:,:,,..,,:,.,,,,,,,,.,,.,.............,.,,,,,,...,..,...................;;:..`....```.````..,:.........,##@@@@@@##@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##++''';;
# ,,,.:,,,,,:,,:,:,,,.,,,,,,.,.,.,,,,,,...,..........,,,,:,.,.....,,.,...,.............,,.,.......``````.,,:.`......,,,##@@@@@@#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#++'';;;:::
# .,,.,,,,,,:,,:,:,,:,:,,,,.,,.,,,,,.,,.............,.,,,,:,,.....,.,,..,.,.......,....,,..;.....`````..,,;.``........,'+@@@@@#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##++';;;::::::
# ,,,,,:,,:,:,,,::,,,.:.,,,.,,.,..,.........,`..,..,,,,.,,,,,..,.....,...........,..,....:.`,,....` `.,,:,.`..........,;+#@@@@@@@@@@+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#++'';;:::::,,::
# ,,,,.:,,:,,,,.:,,,,,:,,,..,,,......,...,..,.,..,..,,,,,,,,,.,...,..................,,,,:',,..:.```..,',.....`...,..,.,+#@@@@@@@@#+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+'';;::::,,,,,,,:
# ,,,,,:,,,,,,,,,,:,.,,,,.,,.,,......,...,..........,,,,,,,,.,,.,.,....,...,,,.,....,,,,,,:;';::'+++++;...........,.,..,+#@@@@@@@+#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+';;:::,,,,,,,,,,,
# ,.,,,,,,.,,,,,,,,,,..,,,...,..,..,...,............,.,,,,,,,,,.........,.....,.,...,......,,::'++++',,...,,...........,+@@@@@##'@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+';;:::,,,,,,,,,,,,,
# ,,,.,,,:,,,,,.,::,,.,:,,:...,,,.,,,..,.,.........,.,,.,,,,.,,,,.,.,.,......,,,,,........,,,,''';:,,.,,.,............,,#@@@@#'@#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+';::,,,,,,,,,,,,,,,
# ,,,,,.::,:,:,.,:,,,,,,,,,...,.....,,,..............,..,,,,,,,....,.........,,.,,...,,,..,,,:,,.,...,,.,.,.......`.....;@@@++@#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+';:,,,,,,,,,,,,,,,,,
# ,.,,,,::,,.,,,,,,,,,.,,,,,,..,,,,,.,.,..,..,.....,...,..,...................,...,,...,,.,:::,.,..,,..,.,,.,..,........:@#'@@#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+';::,,,,,,,,,,,,,,,..
# ,,.,,,,:,,,.,,,.,,,,.,,,,,,..,.,,.,...,.,.....,,......,.,.....,.............,...,,,,,.,,;,:,,.,,.,,..,.,..........,.,.,+#@#+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+';;::,,,,,,,,,,,,,....
# ,,,,,,,;,,,::,,,:,...::,,,...,,,,..,......,....,,.,..,.....,,,......,.........,,.,.,,,,;,,,,,.,,.........,...........,.#@'+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+';;:::,,,,,,,,,,.......
# ,,,,,.,:,,,,:,,,,,,,,,,,.,,.,,.,,,,..,.,.,..,....,....,.,.,..,.......,........,,,,,,,:;,,,,,,.,....................,..,:@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+';;::::,,,,,,,,.........
# ,,,.,,,,,,,,,,,,.,.,,,,,,,.,..,,,,,,,.,.,...,....,......,,,.,,,..,.,..,...,,.,,,,,,,:;,,,,,:,,,.......`.`......`.`....,.+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+';;::,,,,,,,,,..........
# :,,,,,,.:,,,,,,,,:,.,.::,,.,,..,,,.,.,.,,,,,..,......,,...,,,,,,..,..,,,...,,,,,,,,,::,,.,,,::,,.........``.....```....,@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+';;:::,,,,,,,,...........
# .:,,,,,,:,,.,:,,,,,,,,,,,,,,.....,,,,.,,.,........,.,...,,..,,.,,.....,,,.,..,,,,,,::,....,,,;::,,,,,,,,........`....`,.@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+'';:::,,,,,,,,...........,
# ,:,,.,,.:,,.,:,.,.,,.,.,,,,,...,,,.,,,.,,....,...,.........,.,,,,,,.,,..,.,,,,,::,,,,,....,,,::;;++++++#+,....``...,..,,@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+';::::,,,,,,,...........,,
# ..:,.,,,,,,,,.,,,.:,,.,:,,,..,,.,,,,,.................,..,..,..,.,,.,..,,...,,,:.,,,,.,,,..,,,,.,..,,:,`;++,,,.......,,.@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+';;::,,,,,,,.............,,
# ..:,,,,,.:,,,,,,,,:,...,,,,,,..,.,,...,,,,..,,..,.....,.....,.,.,.,.....,,.,,:....,,,..,.,,,,,,,,,...,.,,:'#:,,,....,,,,@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+';;::,,,,,,,.............,,:
# ..,,,,.,,:,,.,,.,,,,,..,,,.,,,.,.,.,,.,,.,,,...,.,..........,...,.....,..,,:,,..,,,.......,,,,,,,,,,,,:,;;:'+',,,,,,,,,,@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+';:::,,,,,..............,,,:
# .,.:,,.,,,,,,,.,,,,,,,.,,,,,,,,,.,,.,.,,,,.,,,,............,,,.,.,,.,...,:,.,.....,.,,,.,,..,,,,,.,,:;:,,.:`:+:,,,,::,,+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+';;::,,,,...............,,,:;
# ,,.,,...,,:,..,,,,,,,,,.,,,,,,,,.,,,,.,,,..,,.,.,,.,.......,,.,,,..,...,,....,,.,,,..,..,.,.,,,,,,,,,,;;,,..,,::::;;:,;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+'';:::,,,,..............,,,:;'
# ,,,.;,,,..:,.,,,,,,,,,,.:,,,,,..,,,..,..,,,,,.,,,............,,.......,,....,,,....,,.,,...,,,,,,,,,,:;'';:,,,::;;;;;#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##+'';;:::,,,..............,,,:;''
# ,,,..,....:,...,,.,,,,..,,,,,,,,,.,,,.,.,,,,,,,,,...,.....,,,.,...........,,.,........,,.,,..,,,,,,,,::,:;'''@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#++''';;;:::,,,............,,,::;;''
# .,,..;,,,,,,,,.,..,,,,,,.:,,,,,.,,,.,,,,...,..,.,,.,.......,...........,,,,,.,.,.,,,....,,,....,.,,.,,,..:''+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+'';;;;;;;:::,,............,,,::;;;;;
# `.,,,.,.,..,,,,.,,,,,,,..,:,,..,,.,,,,.,,,,,,,,,,.....,,........,...,.,,,,,.,,,,..,...,...,.......,..,,..:''@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+';;;:;:;;;;:::,,,.........,,,,::;;;;::
# .`.:,.;,...,,,,,,..,,,,..,:,,,,.,,,,..,,...,,,.,.....,.,,,.............,,,,,:,,.,,,,,..,...,.,.,,....,,..:;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#'';::::::;;;::::,,,.........,,,::;;;;::,
# ```.,,.,,,,,,,,,,..,,,,,,,,,,,,,,,,,,,,,,,.,,:,.,,...,,,.,,,...,...,..,,:,,,,,,,,,,,,,,..,..........,,,..,'@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+';;:::,::::::::::,,,.......,,,,:;;;;::,,,
# ````.,,;,,,,,:,,.,,,,:,,,,,:,,,:,.,,,,,,,,,,,,,,,..,....,.,,......,...,::;;::,:,,,,,,,,,,,.....,....,,.,,,'@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+';:::,,:::::::::::,,,......,,,,:;;;;::,,,,
# `````.,,:,,.,,,,.,,.,,,,,,,:,,,,:,,,,,,,,,,,,.,,,.,.,...,,,,..,......,:,;+';:::.:,,:,,.,.,..........,,.,,,'@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#';::,,,::::::::::::,,,......,,,,:;;;::,,,,,
# ``.````,:,,.,,,.,,,..,,,,,,,:,,,,,,,,,,,.:,,::,.,:.,,,....,.,........,:;''''+;;:,,,,,,,,,,........,..,.,,,@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+';::,:::::::::::::,,,,.....,,,,,::;:,,,,,,.
# ```````.:;,,,,,,,,,,..,,,,.,:,:,,,,,,,,,,,,:,,,,.,.,,.,,,,..,,......,,:;:;:;';;:;''::,,,,...........,.,,,,@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+;::,,:::::::::;:::,,,......,,,,,::::,,,,,..
# ````````.:,,,,,,,,,,..,,,,,,,,,,,,,,,,:,,,,:,,,,,,,,.,,,,,...,.....,::,,.,;,:,,,:;';;+'';::,,,,..,..,.,,,:@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#';:::::::,,,::;;:::,,,......,,,,,,:,,,,,....
# `````````.',,,,,.,,,.,,,,,,.,:,,,,,,,,,,,,,,,,,.,,.,..,,,,..,......,:,..,,::..` .,:,:,:;++'';;;::,,,,,,,,;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#';:::::::,,,::;;:::,,,.......,,,,,,,,,,.....
# ````.`````.',,,,,,,,,,,,,,,,.:,,.,,:,,,,.,,,,,,,.,,,,,,,,...,,....,:,.....,,;```.,....,::,:+++'+';;:,,,,,@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#';::::::,,,,:;;;::,,,,......,,,,,,,,,,......
# ````.``````.',,,,,,,,,,,,,,,,,:,,.,,,,,,,,,,,,,,:,,,,,,,...,.....,,,,......,,:``.,..``.,..,::'#+#++';;;';@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+';:::::,,,,,:;;;:::,,,......,,,,,,,,,,......
# ````````````.;,,,,,,,,,,.,,,,,:,,,,.,:,:,,,,,,,,,.,,,,,,,.,,.....,,,........,,,;.``.`.....,,.;;;++#+#+++@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+';::::,,,,,::;;::::,,,.....,,,,,,,,,,.......
# `````````````.;,,,,,,,,,,:,,:,,:,,,,,,:,,,,,:,:....,..,,,.,.....,,,........,..,::;,``........,,:,+''@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+';:::,,,,,,::;;::::,,,....,,,,,,,,,,,.......
# ```````````````:,,,,,,,,,,,.,,,:,:,,,,,,,,,,,,,,..,,.,,,..,.,..,,,,...........,,,,,,:::.....,.,.+''+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+';:::,,,,,,::;;:::,,,,,..,,,,,,,,,,........,
# ````````````.```:,,,,,,,,,,,.,:,,,,,,:,:,,,,,,,,.,,.,....,.,...,,,,.............,,,,,:,:::,..,,,'';@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+';;:,,,,,,,:;;;:::,,,,,,,,,,,,,,,,,........,
# ````````````````.:,,,,,,,,,,,,,,:,,,,,,,,,,,,,,,,,..,,,,,:..,,.,,..,..............,,:,,,,::::,,;''+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+';;:,,,,,,:::;:::,,,,,,,,,,,,,,,,,.......,,,
# `````````````````.:,,,,,,,,,,,,,,:,,,,::,,,..:,,.,..,,,,,,,,,,.,..,.........,......,..,,,,,,:;:;';@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+';;:,,,,,,:::::::,,,,,,,,,,,,,,,.........,,,
# .``````````````````:,,,,.,,,,,,.,::,,,::,,,,,::,....,,:,,,.,,..,..................,.,.,.,,,,,,:::+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+';;:,,,,,,::::::,,,,,,,,,,,,,,,,.......,,,,,
# ```````````````````.,,,,,,,,,,,,,::,,,,::,,,..,.,,,..,,,.....,,.,.....................,,,,,,,,,::;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#'';;::,,,,::::::,,,,,,,,,,,:::,,,,.....,,,,,:
# ````````````````````,,,,,,,,,,,,,,:,,,,:,,,,,,,,.....,,,,..,...,.,.,.................,,...,,,,,,,:'@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+';;;:,,,,::::::,,,,,,,,,,,::::,,,.....,,,,::
# ````````````````````..:,,,,,,,,,,,::,,.,::,,.,,,,,..,,,,,.,..,.,,,...........,,.,..,..,,,,,,,,,,,,;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+'';;:::,::::::,,,,,,,,,,,,::::,,,,,,,,,,,,:;
# .````````````````````.,:,,,,,,,,,,,:,,,,,:,,,,:,,.,,,:,,,,..,.,,..,................,,,,,:,,,,,,,,::@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+';;;:::::::::,,,,,,...,,,::::::,,,,,,,,,,::'
# `````````````.```````...:,,,,,,,.,.,,,,,,::,,,,,,,.,,,,,,,,..,,...,..............,.,,,,,::;;;:,,,:+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+'';;;::::::,:,,,,,,...,,,:,,,:,,,,,,,,,,,:;'
# ```````..````````.`````.,,,,,,,,,,,::,,,,,::,,,:,,,,,,,,,,,,,....,,,.,............,,,,,,:,:;''';::@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+'';;;::::::,,,,,,,....,,::,,,,,,,,,,,,,,,:;'
# ````````````````````````.,,,,,,,,,,,,,,,,,::,,,,,,,,,,,,,,,.,......................,,,,,,,,,,::;;+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+'';;;::::::,,,,,,,....,,::,,,,,,,,,,,,,,::;;
# ````````````````.``.`````.;:,,,,,,,,,:,,,.,:,,,,,.,,,,,,,,,..,.,.............,......,,,,,,,,,,;;+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+'';;;;::::,,,,,,,,...,,,::,,,,,,,,,,,,,,::;:
# `````````````````````````..;:,,,,,,,,,,.,,,::,,,:,,,,,,,,,,,,,....................,.,,,,,,,,,:;#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+''';;;:::::,,,,,,....,,:::,,,,,,,,,,,,,,::::
# `````..``````````````.```.`.:,,,,,,,,,,,,,,,:,,,,,,,,,,,,,.,,,..,,.................,.,,,.,,,:;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@++''';;;;::::,,,,,,....,,:::::,,,,,,,,,,,,:::,
# ````````````````````````````.;:,,,,,,,:,,,,,:,,,,,,,,,,,,,,,,.,,:,....................,:,,::;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+''';;;:::::,,,,,,....,,:::::,,,,,,,,,,,,:,,,
# ``````````.`````````````````..:,,,,,,,,,,,,,:,,,,:,,::,,,,,,,,,,,,...,..,..........,..,,,,::+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#'';';;;;:::::,,,,,,..,,:::::::,,,,,,,,,,,,,,.
# `````````````````````````````..;,:,,,,:,,.,,,,,,,,,,,::,,,,,,,,,......,................,,,,:@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#'';';;;;:::::,,,,,,..,,:::::::,,,,,,,,,,,,,..
# ``````````````````````````````..::,,,,:,,,,:,:,,,,,:,,,,,,,,,.,.,.,,,..........,,.......,,.:@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#'';;';;;::::::,,,,,,,,,:::::::,,,,,,,,,,,,...
# ````````.``````````````````````..;:,,,,,,,,,,,,,,,,,,,,,,,,,,,,.,,,...................,.,,,:@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+'';;';;;::::::,,,,,,,,:::::::::,,,,,,,,,,,...
# ````````````````````````````````..:,,,,,,,,,,,,,,,:,:,,,,:,,,,,,,,,...,...,,.........,.,,,,:@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+'';';;;;::::::,,,,,,,,::::::::,,,,,,,,,,,....
# ````````````````````.````````````.,::,,:,,,,,,,,,,,,,:,,,,,,,,,,,,,,.,,...,,...........,,.,:@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+';;;;;;;::;::::,,,,,,,,:::::::,,,,,,,,,,,....
#  ```````````````.`...````````````..,:,,:,:,,,::,:,,:,:,,,,,,:,,,,,,,,...,.,,...........,.:,,@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+';;;;;;;;:;;;:::,,,,,,,:::::::,,,,,,,,,,,....
# `.````````````````.`````````````....:,:,:,,:,,:::::,:,,,,,,,,,,,,:,,,,.,...,..........,.,,,,@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+';;;;;;;:;;;;;::::,,,,,,::::,:,,,,,,,,,,,....
# ````````````````````...``````````....;,::::::,,:::::,,,,,:::,::,,,:,,:,..,.,,.........,,,,,,@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+';;;;;;;:;;;;;::::::,:,,,,::,,,,,,,..........
# `. .````````````````...`````````.`...`;:::::::::::::::::,:::,::::::,:,,,.,.,.,,,,.,,,,,,,,,:@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+;;;;;;;;;;;;;;;::::::::,,,,,,,,,,,...........
# `.`..```````````.``.`.....```````..`...;:;:;::::::::::::::,:::::::,::,,,...,.,.,,,.,,,,:,,,:@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+';;;;;;;;;;;;;;::::::::,,,,,,,,,,,...........
# `.```..`.````````````.....````````.....,#';;;;::;:;::::;:::::::::::::::.,,,...,,.,,,,::,,::'@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+;;;;;;;;;;;;;;;:::::::::,,,,,,,,,,...........
# `..``...```..`````````......```````.....;#'''';;;;;;;;;;;;:::::::;:;::::,,,,,.,,,,,:::,,,::@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#';;;;;;;;;;;;;::::::::::::,,,,,,,,,...........
# .`..`....`..`..````````.....````````.....:+'''';';;;;;;;;;;:::::::;;;;;::::,,:,,:,::;,,,::'@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+';;;;;;;;;:;;;;:::::::::::,,,,,,,,,...........
# ```.``.........````````......```````.``...:++'';;'';;;;::::::;;:;::;';;':;,:::,::::;:,,:::@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+';;;;;;;;;::;;:::::::::::,,,,,,,,,,...........
# ```..`...`.....`.`````......``````````.``..#++++';;;;;;;;:;;;;;;;:;;;';'++';;:;;:;:;::::;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+';;;;;;;;;;:;;::::::::::::,,,,,,,,,...........
# ``....`.......,....`````.....````````.``....@#+'''''';;;';;;;;;:;:::'''''++'''''''';::;#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+';;;;;;;;;;;;::::::::::::,,,,,,,,,,...........
# ````...`.`....,.....```.``...````````````...;@@@@#++'''''';'';;;';;;;;'''+++++'++':''+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+';;;;;;;;;;::;::::::::::::,,,,,,,,........,,..
# ```....`.......,.,....````....```````````...,@@@@@@@@@@@#+'''''''''''+++'#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+';;;;;;:::::;;::::::::::::,,,,,,,,,,.....,,,..
# ````....``.`..`..,....```.....``````````````:@@@@@@@@@@@@@@@@@@@@#+++#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+';;;;;;;::::;;;::::::::::,,,,,,,,,,,.....,,,,.
# `````....`.```....,.....`.......``````.`````#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+';;;;;;::::::;::::::::::,,,,,,,,,,,,....,,,,,,
# `````....`````....`.....``......``````````` @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+;;;;;;;;;:::;;;;;:::::::,,,,,,,,,,,,,,,,,,,,,,
# ```````....````.`..````````...`````````````'@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+';;;;;;;;;::::;;;;:::::::,,,,,,,,,,,,,,,,,,,,,,
# ``````````..`.```...````````````.``````````,@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+';;:;;;;;:::::;;;;;:::::::,,,,,,,,,,,,,,,,,,,,,
# `````````.``..```.....```````.```.`````` `'.#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##'';:;;;:;::::::;;;;::::::::,,,,,,,,,,,,,,,,,,,,,
# ```````````.``````..,,..````....`````````::,#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##+';;::::::::::::;;;;;::::::::,,,,,,,,,,,,,,,,,,,,
# ..````````````.````..,,........`.```````.;;.@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##++';;;:::::::::::;;;;:::::::::,,,,,,,,,,,,,,,,,,,,
# ...`````````..`````...,.........``.```.`':,+#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#++'';;;:::::;::::::;;::;:::::::,,,,,,,,,,,,.,,,,,,:
# `..````````````.......,,..........`...`;::;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+'';;;;;::::::::::;:;:;:;::::::,,,,,,,,,,,,,,,,,,,:
# ``...````````..`..`.``.,,.............;;;#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+';;;;;::::::;:::::;;;:;;::::::,,,,,,,,,,.,.,,,,,:;
# ```..````````.``........,,.,........,:;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#++';;;;;::::::;;;:::::::;;::::::,,,,,,,,,,,,.,,,,,:;