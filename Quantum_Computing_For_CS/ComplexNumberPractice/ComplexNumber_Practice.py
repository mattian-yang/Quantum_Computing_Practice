# Import math library for calculation
import math
from fractions import Fraction

# Define ComplexNumber class
class ComplexNumber:
    """
    This is a class for mathematical operations on complex numbers.
 
    Attributes:
        real (float): The real (a) part of the complex number, using for general form.
        imag (float): The imaginary (b) part of the complex number, using for general form.
        magnitude (float): The magitude (rho) of the complex number, using for polar form.
        phase (float): The phase (theta) of the complex number, using for polar form.
        degree (float): The phase value converted from radian to degree. 
        form (str): Specify the form of the input complex number, default to general form 
                    but can also take polar form.
    """

    def __init__(self, real=None, imag=None, magnitude=None, phase=None, form="general"):
        """
        The constructor for ComplexNumber class.
 
        Parameters:
            real (float): The real (a) part of the complex number, using for general form.
            imag (float): The imaginary (b) part of the complex number, using for general form.
            magnitude (float): The magitude (rho) of the complex number, using for polar form.
            phase (float): The phase (theta) of the complex number, using for polar form.
            form (str): Specify the form of the input complex number, default to "general" form 
                    but can also take "polar" form.
        """

        # ensure the numeric inputs have been given for the corresponding form
        if (form == "general" and (real==None or imag==None)) \
            or (form == "polar" and (magnitude==None or phase==None)):
            raise ValueError("Missing numeric inputs for your selected complex number form.")
        
        # ensure the inputs are numeric
        if form == "general":
            if (type(real) not in [int, float]) or (type(imag) not in [int, float]):
                raise TypeError("Your complex number inputs must be numeric.")
        if form == "polar":
            if (type(magnitude) not in [int, float]) or (type(phase) not in [int, float]):
                raise TypeError("Your complex number inputs must be numeric.")
        
        # ensure the form of the complex number takes only "general" or "polar"
        if form not in ["general", "polar"]:
            raise ValueError("The form of the complex number must be either \"general\" or \"polar\"")

        self.form = form
        
        # automatically calculate values for the other form
        if self.form == "general":
            self.real = real
            self.imag = imag
            self.magnitude = (self.real**2 + self.imag**2)**(1/2)
            self.phase = math.atan(self.imag/self.real)
            self.degree = self.phase * 180 / math.pi
        elif self.form == "polar":
            self.magnitude = magnitude
            self.phase = phase
            self.real = self.magnitude * math.cos(self.phase)
            self.imag = self.magnitude * math.sin(self.phase)
            self.degree = self.phase * 180 / math.pi
    

    def print_general_form(self):
        """
        print out the math expression of the general form
        """

        print(f"{self.real}+{self.imag}i")
    

    def print_polar_form(self):
        """
        print out the math expression of the polar form
        """

        print(f"{self.magnitude}(cos({self.phase})+isin({self.phase}))")
    

    def __eq__(self, other):
        """
        Compare whether two complex numbers are the same (with accuracy up to 8 decimal places).
        If either or both objects are not complex number, return False.
        """

        if not (isinstance(self, ComplexNumber) and isinstance(other, ComplexNumber)):
            return False
        else:
            return (round(self.real, 8) == round(other.real, 8)) and (round(self.imag, 8) == round(other.imag, 8))
    

    def __add__(self, other):
        """
        Addition of two complex number.
        """

        if not (isinstance(self, ComplexNumber) and isinstance(other, ComplexNumber)):
            raise TypeError("This operation must be applied to complex numbers.")
        else:
            return ComplexNumber(real=self.real+other.real, imag=self.imag+other.imag)


    def __sub__(self, other):
        """
        Subtraction of two complex number.
        """

        if not (isinstance(self, ComplexNumber) and isinstance(other, ComplexNumber)):
            raise TypeError("This operation must be applied to complex numbers.")
        else:
            return ComplexNumber(real=self.real-other.real, imag=self.imag-other.imag)
    

    def conjugate(self):
        """
        Return the conjugate of the given complex number.
        """

        if not isinstance(self, ComplexNumber):
            raise TypeError("This operation must be applied to complex numbers.")
        else:
            return ComplexNumber(real=self.real, imag=-self.imag)
    

    def __mul__(self, other):
        """
        Multiplication of two complex numbers.
        This is performed using polar form.
        """

        if not (isinstance(self, ComplexNumber) and isinstance(other, ComplexNumber)):
            raise TypeError("This operation must be applied to complex numbers.")
        else:
            return ComplexNumber(magnitude=self.magnitude*other.magnitude, phase=self.phase+other.phase, form="polar")
    
    
    def __truediv__(self, other):
        """
        Division of two complex numbers.
        This is performed using polar form.
        """

        if not (isinstance(self, ComplexNumber) and isinstance(other, ComplexNumber)):
            raise TypeError("This operation must be applied to complex numbers.")
        else:
            return ComplexNumber(magnitude=self.magnitude/other.magnitude, phase=self.phase-other.phase, form="polar")


    def __pow__(self, other):
        """
        Take exponential of the complex number, where the power is a real number.
        This is performed using polar form.
        Output is a tuple as fractional power will yield more than one complex number.
        """

        if not isinstance(self, ComplexNumber):
            raise TypeError("This operation must be applied to complex numbers.")
        elif not isinstance(other, (int, float)):
            raise TypeError("Power value can only be numeric.")
        else:
            result = tuple()
            complex_one = ComplexNumber(1, 0)
            power = abs(other)
            if isinstance(other, int):
                if other >= 0:
                    result = tuple([ComplexNumber(magnitude=self.magnitude**power, phase=self.phase*power, form="polar")])
                else:
                    result = tuple([complex_one.__truediv__(\
                                  ComplexNumber(magnitude=self.magnitude**power, phase=self.phase*power, form="polar"))])
            else:
                power_num = Fraction(power).limit_denominator()._numerator
                power_den = Fraction(power).limit_denominator()._denominator
                if other >= 0:
                    result = tuple([ComplexNumber(magnitude=self.magnitude**other, \
                                                phase=(self.phase+2*k*math.pi)/power_den*power_num, form="polar") \
                                      for k in range(power_den)])
                else:
                    result = tuple([complex_one.__truediv__(\
                                  ComplexNumber(magnitude=self.magnitude**other, \
                                                phase=(self.phase+2*k*math.pi)/power_den*power_num, form="polar")) \
                                      for k in range(power_den)])
            # print some results out
            i = 0
            while i < min(len(result), 10):
                result[i].print_general_form()
                i += 1
            if len(result) > 10:
                print("......")

            return result



# Run through some unit tests
import unittest

class TestComplexNumber(unittest.TestCase):

    def test_general_form_initiation(self):
        c1 = ComplexNumber(3,4)

        self.assertIsInstance(c1, ComplexNumber)
    

    def test_polar_form_initiation(self):
        c1 = ComplexNumber(magnitude=5, phase=0.9272952180016122, form="polar")
        
        self.assertIsInstance(c1, ComplexNumber)
    
    def test_wrong_initiation(self):
        with self.assertRaises(ValueError):
            ComplexNumber(magnitude=5, phase=0.9272952180016122)
        with self.assertRaises(TypeError):
            ComplexNumber(magnitude="five", phase=0.9272952180016122, form="polar")
        with self.assertRaises(ValueError):
            ComplexNumber(magnitude=5, phase=0.9272952180016122, form="Eular")
    
    
    def test_comparison(self):
        c1, c2 = ComplexNumber(3, 4), ComplexNumber(magnitude=5, phase=0.9272952180016122, form="polar")
        
        self.assertEqual(c1, c2)
        

    def test_add_substract(self):
        c1, c2 = ComplexNumber(3, 4), ComplexNumber(5, 12)
        c_add = c1 + c2
        c_sub = c1 - c2

        self.assertEqual(c_add.real, 8)
        self.assertEqual(c_add.imag, 16)
        self.assertEqual(c_sub.real, -2)
        self.assertEqual(c_sub.imag, -8)
    

    def test_multiply(self):
        c1, c2 = ComplexNumber(3, 4), ComplexNumber(5, 12)
        c_mul1 = c1 * c2
        c_mul_real = 3 * 5 - 4 * 12
        c_mul_imag = 3 * 12 + 4 * 5
        c_mul2 = ComplexNumber(c_mul_real, c_mul_imag)

        self.assertEqual(c_mul1, c_mul2)

    
    def test_exponential1(self):
        c1 = ComplexNumber(3, 4)
        c_pow2_1 = c1 ** 2
        c_pow2_2 = c1 * c1

        self.assertEqual(c_pow2_1[0], c_pow2_2)
    
    
    def test_exponential2(self):
        c2 = ComplexNumber(1, 0)
        c_pow1o5 = c2 ** 0.2
 
        self.assertEqual(c_pow1o5[1].degree, 72)
    
    
    def test_exponential3(self):
        c3 = ComplexNumber(1, 0)
        c_pow1o5 = c3 ** 0.2
        c_pown1o5 = c3 ** -0.2
        
        self.assertEqual(c_pow1o5[1].conjugate(), c_pown1o5[1])
        
        
# Run unittest as the main module
if __name__ == '__main__':
    # if run in jupyter:
    # unittest.main(argv=['first-arg-is-ignored'], exit=False)
    unittest.main()