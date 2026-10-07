from machine import Pin, PWM
from time import sleep


# =========================
# MOTOR SETUP
# =========================

# Motor A
e1 = PWM(Pin(28))
m1 = Pin(27, Pin.OUT)

# Motor B
e2 = PWM(Pin(26))
m2 = Pin(22, Pin.OUT)

# PWM frequency
e1.freq(1000)
e2.freq(1000)


# =========================
# SETTINGS
# =========================

SPEED = 32767          # 50% speed

# Calibration values
TIME_PER_METER = 2.0
TIME_90_DEGREES = 0.8

ROUTE_FILE = "route.txt"


# =========================
# MOTOR FUNCTIONS
# =========================

def stop():
    e1.duty_u16(0)
    e2.duty_u16(0)
    sleep(0.5)


def forward(meters):
    print("Forward:", meters, "m")

    m1.value(1)
    m2.value(1)

    e1.duty_u16(SPEED)
    e2.duty_u16(SPEED)

    sleep(meters * TIME_PER_METER)

    stop()


def reverse(meters):
    print("Reverse:", meters, "m")

    m1.value(0)
    m2.value(0)

    e1.duty_u16(SPEED)
    e2.duty_u16(SPEED)

    sleep(meters * TIME_PER_METER)

    stop()


def left(degrees):
    print("Left:", degrees, "degrees")

    m1.value(0)
    m2.value(1)

    e1.duty_u16(SPEED)
    e2.duty_u16(SPEED)

    sleep((degrees / 90) * TIME_90_DEGREES)

    stop()


def right(degrees):
    print("Right:", degrees, "degrees")

    m1.value(1)
    m2.value(0)

    e1.duty_u16(SPEED)
    e2.duty_u16(SPEED)

    sleep((degrees / 90) * TIME_90_DEGREES)

    stop()


def turn_around():
    print("Turn around")

    right(180)


# =========================
# READ ROUTE FILE
# =========================

def read_route():

    route = []

    try:
        file = open(ROUTE_FILE, "r")
    except OSError:
        print("ERROR: route.txt was not found!")
        print("Upload route.txt to the Pico.")
        return route

    for line in file:

        line = line.strip()

        # Ignore empty lines
        if line == "":
            continue

        # Ignore comments
        if line.startswith("#"):
            continue

        parts = line.split()

        command = parts[0].lower()

        # turn_around does not need a number
        if command == "turn_around":
            route.append(("turn_around", 0))

        # Other commands need a number
        elif len(parts) == 2:

            try:
                value = float(parts[1])
                route.append((command, value))

            except ValueError:
                print("Invalid number:", line)

        else:
            print("Invalid instruction:", line)

    file.close()

    return route


# =========================
# EXECUTE ROUTE
# =========================

def run_route(route):

    for command, value in route:

        if command == "forward":
            forward(value)

        elif command == "reverse":
            reverse(value)

        elif command == "left":
            left(value)

        elif command == "right":
            right(value)

        elif command == "turn_around":
            turn_around()

        else:
            print("Unknown command:", command)

        sleep(0.2)


# =========================
# PROGRAM START
# =========================

print("FoCar Assignment 6.2")

route = read_route()

print("Instructions loaded:", len(route))

if len(route) == 0:

    print("No route instructions found.")
    stop()

else:

    print("Starting in 5 seconds...")

    sleep(5)

    print("Starting route!")

    run_route(route)

    stop()

    print("Route completed!")