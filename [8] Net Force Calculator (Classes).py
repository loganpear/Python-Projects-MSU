import copy
import math

"Magnitude: {}"
"\nAngle: {}"
"\nBoth objects must be of the Force class"
"\nForce object {} already exists!"
"\nForce object {} does not exist!"
"\nForce #{}: {}"
"\n{}"


class Force(object):
    """
        A class for force vectors with the magnitude and angle
    """

    def __init__(self, magnitude=0, angle=0):
        """
        Initializes the Force object with its magnitude and angle
        """
        self.magnitude = magnitude
        self.angle = angle

    def get_magnitude(self):
        """
        returns the magnitude of the force
        """
        return self.magnitude

    def get_angle(self):
        """
        returns the angle of the force
        """
        return self.angle

    def get_components(self):
        """
        Returns the x and y components of the force
        """
        x_component = self.magnitude * math.cos(math.radians(self.angle))
        y_component = self.magnitude * math.sin(math.radians(self.angle))
        return x_component, y_component

    def __str__(self):
        """
        Returns a formatted string of the Force object
        """
        return f"Magnitude: {self.magnitude:.2f}\nAngle: {self.angle:.2f}"

    def __eq__(self, other):
        """
        Checks if two Force objects are equal
        """

        if not isinstance(other, Force):
            raise RuntimeError("Both objects must be of the Force class")
        return self.magnitude == other.magnitude and self.angle == other.angle

    def __add__(self, other):
        """
        Adds the two Force objects to return the resultant force
        """

        if not isinstance(other, Force):
            raise RuntimeError(
                "Both objects must be of the Force class")

        x_one, y_one = self.get_components()
        x_two, y_two = other.get_components()
        x_sum = x_one + x_two
        y_sum = y_one + y_two

        magnitude = math.sqrt(x_sum ** 2 + y_sum ** 2)  # magnitude equation
        angle = math.degrees(math.atan2(y_sum, x_sum))

        if angle < 0:  # makes sure angle is positive
            angle += 360  # converts angle to ist positive version
        return Force(magnitude, angle)


class ForceCalculator(object):
    """
    class for a calculator for computing multiple forces
    """

    def __init__(self, forces=None):
        """
        Initializes a ForceCalculator object with optional initial forces
        """
        if forces is None:
            self.forces = {}
        else:
            self.forces = forces

    def get_forces(self):
        """
        Returns the dictionary of all forces
        """
        return self.forces

    def add_force(self, name, magnitude, angle):
        """
        Adds a force to the calculator
        """
        if name in self.forces:
            raise RuntimeError(f"\nForce object {name} already exists!")
        self.forces[name] = Force(magnitude, angle)

    def remove_force(self, name):
        """
        Removes a force from the calculator
        """

        if name not in self.forces:
            raise RuntimeError(f"\nForce object {name} does not exist!")
        self.forces.pop(name)

    def __getitem__(self, name):
        """
        Accesses individual forces with their keys of they exist
        """
        if name not in self.forces:
            raise RuntimeError(f"\nForce object {name} does not exist!")
        else:
            return self.forces[name]

    def compute_net_force(self):
        """
        Computes the net force of all forces in the calculator
        """
        if not self.forces:
            return Force()
        net_force = Force()
        for force in self.forces.values():
            net_force += force
        return net_force

    def __str__(self):
        """
        Returns a string representation of the ForceCalculator object
        """
        output = ""
        for i, (name, force) in enumerate(self.forces.items(), start=1):
            output += f"\nForce #{i:02}: {name}"
            output += f"\n{force}"
        return output
