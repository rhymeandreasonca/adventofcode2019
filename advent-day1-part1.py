import math
import traceback

class CalculationException(Exception):
	""" Raised when the FuelCalculator encounters a fatal error. """
	pass

class FuelCalculator:
	"""A simple tool for calculating the total amount of fuel required to launch a group of modules based on their individual masses.
	
	Args:

	module_masses (list): A list of integers representing the masses of modules that need to be launched and for which fuel requirements need to be calculated.

	"""

	def __init__(self, module_masses):
		try:
			self._module_masses = list()
			self._module_masses += module_masses
		except TypeError:
			print("Module masses were not provided in the correct format. Please provide masses in a list.\r\n")
			raise CalculationException

	def get_fuel_for_module(self, module_mass):
		""" Calculates the amount of fuel required to launch a single module based on its mass. """
		fuel = 0 

		try:
			fuel = math.floor(module_mass/3) - 2

		except TypeError:
			print("Module masses were not provided in a numeric format. Please provide masses as numbers.\r\n")
			raise CalculationException
		
		return int(fuel)

	def get_total_fuel(self):
		""" Calculates the total sum of fuel required to launch all modules provided to the calculator instance. """
		total_fuel = 0

		try:
			for module in self._module_masses:
				total_fuel += self.get_fuel_for_module(module)
		except CalculationException:
			total_fuel = "Unknown. Calculation Failed.\r\n"

		return total_fuel

module_masses = [141657,108912,57953,130157,81114,120358,53075,82893,61045,133276,118918,83442,69634,91360,114473,129148,89966,82662,91680,136321,69756,104495,94736,115985,103428,119147,83952,129708,90115,135629,96715,125560,144363,132711,108987,82157,62962,66436,87388,57312,146342,145167,67944,133897,149537,72973,76650,129914,91527,149755,128253,132606,86480,118149,132469,81445,112436,83057,75936,55345,96544,121752,78590,72417,148164,99428,85137,132276,96763,106806,106563,81540,108366,119792,79118,62130,137706,124220,135189,72519,81616,56448,53525,86792,98569,139069,67337,101651,148685,73432,94946,122955,144581,121306,126622,130625,125811,128017,55621,132501]

try:
	calculator = FuelCalculator(module_masses)
	print("The total fuel required is: " + str(calculator.get_total_fuel()))
except Exception:
	print("The calculator experienced a fatal error. See the traceback for more information.\r\n")
	traceback.print_exc()