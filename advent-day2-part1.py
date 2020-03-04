import traceback
import abc

class CalculationException(Exception):
    """Raised when the IntCodeComputer encounters a fatal error."""
    pass

class IntCodeStrategy(metaclass=abc.ABCMeta):
    """An abstract class used for providing strategies for defining how the 
       IntCodeComputer performs specific mathematical operations."""
    NON_INT_ERROR_TEXT = "A non-integer was given to the {} operation."

    @abc.abstractmethod
    def calculate(self, first_value, second_value):
        pass

class IntCodeAddStrategy(IntCodeStrategy):
    STRATEGY_NAME = "addition"

    """A strategy used by the IntCodeComputer to perform addition operations."""
    def calculate(self, first_value, second_value):

        calculated = None

        try:
            calculated = first_value + second_value
        except (TypeError, ValueError):
            print(self.NON_INT_ERROR_TEXT.format(self.STRATEGY_NAME))

        return calculated

class IntCodeMultiplyStrategy(IntCodeStrategy):
    STRATEGY_NAME = "multiplication"

    """A strategy used by the IntCodeComputer to perform multiplication operations."""
    def calculate(self, first_value, second_value):

        calculated = None

        try:
            # Cast to int to protect against a string being passed as arguments. Strings
            # have a valid multiplication operation.
            return int(first_value) * int(second_value)
        except (TypeError, ValueError):
            print(self.NON_INT_ERROR_TEXT.format(self.STRATEGY_NAME))

        return calculated

class IntCodeComputer:
    """ A tool for processing int-code instructions. Where int-code 
        instructions use the following format:
            - A list of integers to be processed in sets of 4 integers, where 
              in each set:
                - Position 1 is a mathematical operation code or a halt code
                - Position 2 is the position in the int-code instructions of 
                  the first value to be operated upon
                - Position 3 is the position in the int-code instructions of 
                  the second value to be operated upon
                - Position 4 is the position in the int-code instructions where
                  the result of the operation will be written
            - The mathematical operation codes are:
                - 1 for an addition operation
                - 2 for a multiplication operation
            - The halting code is 99

        Args:
            int_code_list (list): A list of integers representing a set of 
            int-code instructions.
    """

    def __init__(self, int_code_list):
        try:
            self._int_code_list = list()
            self._int_code_list += int_code_list
            
            self._add_strategy = IntCodeAddStrategy()
            self._multiply_strategy = IntCodeMultiplyStrategy()
            self._is_state_nominal = False
            
            self._INSTR_SET_LEN = 4

            self._STRATEGY_POS = 0
            self._VALUE_1_POS  = 1
            self._VALUE_2_POS  = 2
            self._TARGET_POS   = 3

            self._ADD_STRATEGY_CODE      = 1
            self._MULTIPLY_STRATEGY_CODE = 2
            self._HALT_CODE              = 99

            self._restore_1202_state()

        except TypeError:
            print("IntCodes were not provided in the correct format. Please provide masses in a list.")
            raise CalculationException

    def _restore_1202_state(self):
        """Restore the 1202 Program Alarm to the nominal state."""
        try:
            self._int_code_list[1] = 12
            self._int_code_list[2] = 2
            self._is_state_nominal = True

        except IndexError:
            print("The 1202 Program Alarm state could not be restored due to an input error.")
            raise CalculationException

    def _set_target_value(self, target, value):
        """Set the target position in the int-code instructions to the provided value."""
        if value is not None:
            self._int_code_list[target] = value
        else:
            raise CalculationException

    def compute_int_code(self):
        """Process the int-code instructions provided to the IntCodeComputer 
           instance, returns the value of position 0 of the int-code 
           instructions at the end of the computation."""
        
        return_value = 0
        return_value_pos = 0

        try:
            if not self._is_state_nominal:
                self._restore_1202_state()

            cursor_pos = 0

            while cursor_pos < len(self._int_code_list):
                strategy   = self._int_code_list[cursor_pos + self._STRATEGY_POS]
                value1_pos = self._int_code_list[cursor_pos + self._VALUE_1_POS] 
                value1     = self._int_code_list[value1_pos]
                value2_pos = self._int_code_list[cursor_pos + self._VALUE_2_POS]
                value2     = self._int_code_list[value2_pos]
                target     = self._int_code_list[cursor_pos + self._TARGET_POS]
                
                if(strategy == self._ADD_STRATEGY_CODE):
                    self._set_target_value(target, self._add_strategy.calculate(value1, value2))

                elif(strategy == self._MULTIPLY_STRATEGY_CODE):
                    self._set_target_value(target,self._multiply_strategy.calculate(value1, value2))

                elif(strategy == self._HALT_CODE):
                    break

                else:
                    print("Unexpected instruction value received.")
                    raise CalculationException
                    break

                cursor_pos += self._INSTR_SET_LEN

            return_value = self._int_code_list[return_value_pos]

        except Exception:           
            print("Incorrect parameters. Aborting computation.")
            return_value = "Unknown. Prepare for impact."
            traceback.print_exc()

        return return_value


if __name__ == "__main__":

    int_code_input = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,9,19,1,19,5,23,1,13,23,27,1,27,6,31,2,31,6,35,2,6,35,39,1,39,5,43,1,13,43,47,1,6,47,51,2,13,51,55,1,10,55,59,1,59,5,63,1,10,63,67,1,67,5,71,1,71,10,75,1,9,75,79,2,13,79,83,1,9,83,87,2,87,13,91,1,10,91,95,1,95,9,99,1,13,99,103,2,103,13,107,1,107,10,111,2,10,111,115,1,115,9,119,2,119,6,123,1,5,123,127,1,5,127,131,1,10,131,135,1,135,6,139,1,10,139,143,1,143,6,147,2,147,13,151,1,5,151,155,1,155,5,159,1,159,2,163,1,163,9,0,99,2,14,0,0]

    try:
        int_code_computer = IntCodeComputer(int_code_input)
        print("The value of position 0 of the int-code instructions after computation is: " + 
            str(int_code_computer.compute_int_code()))
    except Exception:
        print("The ship computer could not be restored. Prepare for impact.")
        traceback.print_exc()