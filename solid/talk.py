#  ____   ___  _     ___ ____
# / ___| / _ \| |   |_ _|  _ \
# \___ \| | | | |    | || | | |
#  ___) | |_| | |___ | || |_| |
# |____/ \___/|_____|___|____/


# Staticaly typed languages - C++, JAVA - Abstract classes and interfaces
# type checking on compile time
# Dynamicaly typed languages - Ruby, Python - Duck Typing and protocols -
#                              PEP and conventions Zen of Python
# type checking on run time
# code smell

# - https://www.python.org/dev/peps/pep-0234/#abstract
# - import typing
# - import this

# SOLID - classes
# other principles:
# component chesion (4)/component coupling (4) - group of classes

# Why interfaces exist? To get around the diamond problem.

# SOLID is about mid-level software structures called classes or something else
# show what you mean by level in a context
# IF is the thing you wanna get away from

# ####################################################################
# SRP: A module should be responsible to one, and only one actor.    #
# keywords: actor, client                                            #
# ####################################################################

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

# PROBLEM #2: Same again, but multiple abstractions

class Modem(object):
    def dial(self, pno): # connection
        pass
    def hangup(self): # connection
        pass
    def send(self, c): # communication
        pass
    def recv(self): # communication
        pass

# SOLUTION #2: isolate responsibilities

from abc import ABC

class DataChannel(ABC):
    def send(self, c): # communication
        pass
    def recv(self): # communication
        pass

class Connection(ABC):
    def dial(self, pno): # connection
        pass
    def hangup(self): # connection
        pass

class Modem(DataChannel, Connection):
    pass


# ####################################################################
# OCP: open for extension, close for modification                    #
# keywords: extension-not-changes                                    #
# ####################################################################

# It should be clear that no significant program can be 100% closed. Depends on the requirements
# Main reason behind OOD

# convetions:
# - make member variables private as much as possible
# - no global veriables
# - avoid dynamic typecasting

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

    def print(self, filename):
        self.printer.print_file(filename)

# PROBLEM #3:

class Circle(object):
    pass

class Square(object):
    pass

def draw_all_shapes(shapes):
    for shape in shapes:
        if isinstance(shape, Square):
            draw_square(shape)
        if isinstance(shape, Circle):
            draw_circle(shape)

# SOLUTION #3:

class Shape(object):
    def draw(self):
        pass

class Circle(Shape):
    pass

class Square(Shape):
    pass

def draw_all_shapes(shapes):
    for shape in shapes:
        shape.draw()

# SOLUTION #3.2: Good, but what if we want to change the order? There is no way to be 100% closed

# ---

# ################################################################################
# LSP: A o1 of type S can be replaced o2 of type T                               #
# with no behaviour changes if S is subtype of T                                 #
# note: The LSP says that the subclass can be used in place of the parent class, #
# not that the parent class can be used in place of the subclass.                #
#       The validity of a model can only be expressed in terms of its clients    #
# keyword: Behaviour                                                             #
# ################################################################################

# Behavioural subtyping is undecidable in general:
# if q is the property "method for x always terminates",
# then it is impossible for a program (e.g. a compiler)
# to verify that it holds true for some subtype S of T,
# even if q does hold for T. Nonetheless, the principle is useful in reasoning
# about the design of class hierarchies.


# LSP Requirements:

# - Contravariance of method arguments in the subtype.
#   the very same as the definition for method arguments
# - Covariance of return types in the subtype.
#   the very same as the definition for method return types
# - No new exceptions should be thrown by methods of the subtype,
# except where those exceptions are themselves subtypes of exceptions thrown by the methods of the supertype.
#   the very same as the definition for exceptions types and if raised or not
# - Preconditions cannot be strengthened in a subtype.
#   precondition is a condition/assertion/predicate that must always be true just as prior the execution of the function
# - Postconditions cannot be weakened in a subtype.
#   postcondition is a condition/assertion/predicate or predicate that must always be true just as after the exection of the function
# - Invariants of the supertype must be preserved in a subtype.
#   assertions that are true on function runtime
#           {P} C {Q}
# - History constraint (the "history rule").
#  You can add method as long as the ones inherited behave the same


# In other words, when using an object through its base class interface, the user knows
# only the preconditions and postconditions of the base class. Thus, derived objects must not
# expect such users to obey preconditions that are stronger then those required by the base
# class. That is, they must accept anything that the base class could accept. Also, derived
# classes must conform to all the postconditions of the base. That is, their behaviors and outputs
# must not violate any of the constraints established for the base class. Users of the base
# class must not be confused by the output of the derived class.

# gist: the whole point of LSP is to be able to pass around a subclass as the parent class without any problems. It says nothing about not being able to downcast for additional functionality.

# PROBLEM #1: behaviour of rectangle is not the same as a square
#             postcondition is a condition or predicate that must always be true just as after the changes

class Rectangle(object):
    width = None
    height = None

    def set_width(self, w):
        self.width = w

    def set_height(self, h):
        self.height = h


class Square(Rectangle):
    def set_width(self, w):
        self.width = w
        set_height(w)

    def set_height(self, h):
        self.height = h
        set_width(h)

def g(rectangle): # works for a rectangle but not for a square
    rectangle.set_width(5)
    rectangle.set_height(3)

# SOLUTION #1: move to a better abstraction

class Quadrilateral(object):
    x1 = None
    x2 = None
    y1 = None
    y2 = None
    width = None
    height = None

    def set_x1(self, x1):
        self.x1 = x1

    # ...

    def get_width(self):
        return self.x2 - self.x1

    def get_height(self):
        return self.y2 - self.y1


class Rectangle(Quadrilateral):
    pass

class Square(Quadrilateral):
    pass

def g(rectangle): # works for a rectangle but not for a square
    rectangle.set_x1(10)
    rectangle.set_x2(5)
    rectangle.set_y1(6)
    rectangle.set_y2(3)

# PROBLEM #2: not all tasks behave the same way. The behaviour changes not the number of methods
#             precondition is a condition or predicate that must always be true just as prior the changes

class Task(object):
    status = None

    def close(self):
        self.status = 'CLOSED'

class BasicTask(Task):
    pass

class ProjectTask(Task):
    def close(self):
        if self.status == 'STARTED':
            raise Exception("Cannot close Task")
        super().close()

# SOLUTION #2: bring the behaviour up the inheritance chain

class Task(object):
    status = None

    def can_close(self):
        return True

    def close(self):
        if self.can_close():
            self.status = 'CLOSED'
        raise Exception("Cannot close Task") # exception expected on supertype

class BasicTask(Task):
    pass

class ProjectTask(Task):
    def can_close(self):
        return self.status == 'STARTED'

# PROBLEM #3: immutable point - allowed Under the definitions of Meyer and America
#             History constraint (the "history rule").
#             You can add method as long as they ones inherited behave the same

class ImmutablePoint(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class MutablePoint(ImmutablePoint):
    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

# SOLUTION #3: Move methods up the chain

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class ImmutablePoint(Point):
    pass

class MutablePoint(Point):
    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

# ####################################################################
# ISP: client should be forced to depend on methods it does not use  #
# keyword: too-many-methods                                          #
# ####################################################################

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

class AndroidCharger(Charger):
    def connect(self):
        IOUSB2.connect(phone)

class AppleCharger(Charger):
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

# #############################################################################
# DIP: high level modules and low level modules should depend on abstractions #
# keyword: conform-to-interface-contract,                                     #
#          program-to-abstraction-rather-than-implementation                  #
# show source dependecy vs flow of control diagram                            #
# #############################################################################

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

from abc import ABC

class Reader(ABC):
    pass

class Writer(ABC):
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

from abc import ABC

class ButtonClient(ABC):
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


# Reference:
# https://stackoverflow.com/questions/3023503/how-can-i-check-if-an-object-is-an-iterator-in-python
# https://www.python.org/dev/peps/pep-0544/#using-protocols-in-python-2-7-3-5
# https://en.wikipedia.org/wiki/Covariance_and_contravariance_(computer_science)
# https://softwareengineering.stackexchange.com/questions/170138/is-this-a-violation-of-the-liskov-substitution-principle/170141
# https://stackoverflow.com/questions/24408748/does-adding-public-method-to-subclass-violate-lsp-liskov-substitution-principle
# https://en.wikipedia.org/wiki/Hoare_logic
# http://butunclebob.com/ArticleS.UncleBob.PrinciplesOfOod
# https://stackify.com/interface-segregation-principle/
# https://martinfowler.com/bliki/FlagArgument.html
# https://en.wikipedia.org/wiki/Convention_over_configuration
# https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html
