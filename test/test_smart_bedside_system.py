import unittest
from unittest.mock import patch, MagicMock, call

from mock import max30102, GPIO
from src.smart_bedside_error import SmartBedsideError
from src.smart_bedside_system import SmartBedsideSystem


##########################################################################################
########################### Acceptance Tests for User Story #1 ###########################
##########################################################################################

class TestUserStory1(unittest.TestCase):

    @patch.object(max30102.DFRobot_BloodOxygen_S, "__init__", return_value=None)
    @patch.object(max30102.DFRobot_BloodOxygen_S, "begin")
    @patch.object(max30102.DFRobot_BloodOxygen_S, "sensor_start_collect")
    def read_vital_signs(self) -> int:
        spo2 = self.spo2_hr_sensor.get_spo2()

        if spo2 == -1:
            raise SmartBedsideError("Invalid SpO2 reading")

        return int(spo2)

    def manage_alarm(self) -> None:


    def test_spo2_sensor_initialization(self, mock_sensor_start_collect: MagicMock,
            mock_begin: MagicMock, mock_DFRobot_BloodOxygen_S: MagicMock):
        system = SmartBedsideSystem()
        # Assert that the sensor was instantiated without any arguments.
        mock_DFRobot_BloodOxygen_S.assert_called_once_with()
        # Assert that the sensor's begin() method was called exactly once.
        mock_begin.assert_called_once_with()
        # Assert that the sensor's data acquisition was started exactly once.
        mock_sensor_start_collect.assert_called_once_with()
        # Assert that the sensor was stored in the spo2_hr_sensor instance variable.
        self.assertIsInstance(system.spo2_hr_sensor, max30102.DFRobot_BloodOxygen_S)

    def update_spo2_alarm(self) -> None:
        spo2 = self.read_vital_signs()  # Propagates SmartBedsideError
        if spo2 < self.SPO2_ALARM_THRESHOLD:
            self.activate_alarm()
        else:
            self.deactivate_alarm()

    @patch.object(max30102.DFRobot_BloodOxygen_S, "get_spo2")
    def test_read_valid_spo2(self, mock_get_spo2: MagicMock):
        mock_get_spo2.return_value = 98  # Simulate a valid SpO2 reading of 98%.
        system = SmartBedsideSystem()
        spo2 = system.read_vital_signs()
        # Assert that the returned SpO2 value matches the sensor reading
        self.assertEqual(spo2, 98

                         @ patch.object(max30102.DFRobot_BloodOxygen_S, "get_spo2")

        def test_read_valid_spo2(self, mock_get_spo2: MagicMock):
            mock_get_spo2.return_value = 98

            system = SmartBedsideSystem()

            spo2 = system.read_vital_signs()

            self.assertEqual(spo2, 98)

    @patch.object(max30102.DFRobot_BloodOxygen_S, "get_spo2")
    def test_read_invalid_spo2(self, mock_get_spo2: MagicMock):
        mock_get_spo2.return_value = -1  # Simulate an invalid SpO2 reading.
        system = SmartBedsideSystem()
        # Assert that SmartBedsideError is raised when the sensor returns -1.
        self.assertRaises(SmartBedsideError, system.read_vital_signs)

        @patch.object(max30102.DFRobot_BloodOxygen_S, "get_spo2")
        def test_read_invalid_spo2(self, mock_get_spo2: MagicMock):
            mock_get_spo2.return_value = -1

            system = SmartBedsideSystem()

            self.assertRaises(
                SmartBedsideError,
                system.read_vital_signs
            )


##########################################################################################
########################### Acceptance Tests for User Story #2 ###########################
##########################################################################################

class TestUserStory2(unittest.TestCase):

    @patch.object(GPIO, "setup")
    def test_buzzer_initialization(self, mock_gpio_setup: MagicMock):
        system = SmartBedsideSystem()
        accepted_calls = [
            call(system.BUZZER_PIN, GPIO.OUT),
            call(system.BUZZER_PIN, GPIO.OUT, initial=GPIO.LOW),
        ]
        # Assert that the buzzer pin was configured as an output pin (optionally starting LOW, i.e. OFF).
        found = False
        for accepted_call in accepted_calls:
            if accepted_call in mock_gpio_setup.call_args_list:
                found = True
        self.assertTrue(found)
        # Assert that the alarm status is initialized to OFF.
        self.assertFalse(system.alarm_on)

        def __init__(self):
            GPIO.setmode(GPIO.BOARD)
            GPIO.setwarnings(False)

            # Initialise MAX30102 sensor
            self.spo2_hr_sensor = DFRobot_BloodOxygen_S()

            # Initialise buzzer
            GPIO.setup(self.BUZZER_PIN, GPIO.OUT, initial=GPIO.LOW)
            self.alarm_on = False

            # Initialise pushbutton
            GPIO.setup(self.BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

            # Initialise servo
            GPIO.setup(self.O2_SERVO_PIN, GPIO.OUT)
            self.o2_servo = GPIO.PWM(self.O2_SERVO_PIN, 50)
            self.o2_servo.start(0)
            self.o2_valve_angle = 0.0



    @patch.object(GPIO, "output")
    @patch.object(SmartBedsideSystem, "read_vital_signs")
    def test_manage_alarm_critical_spo2(self,
            mock_read_vital_signs: MagicMock, mock_gpio_output: MagicMock):
        mock_read_vital_signs.return_value = 87 # Simulate a valid SpO2 reading of 87%.
        system = SmartBedsideSystem()
        mock_gpio_output.reset_mock()  # Ignore GPIO.output calls made by the constructor.
        system.alarm_on = False
        system.manage_alarm()
        # Assert that the buzzer was turned ON.
        mock_gpio_output.assert_called_once_with(system.BUZZER_PIN, True)
        # Assert that the alarm status was updated to ON.
        self.assertTrue(system.alarm_on)

    @patch.object(GPIO, "output")
    @patch.object(SmartBedsideSystem, "read_vital_signs")
    def test_manage_alarm_no_critical_spo2(self,
            mock_read_vital_signs: MagicMock, mock_gpio_output: MagicMock):
        mock_read_vital_signs.return_value = 88  # Simulate a valid SpO2 reading of 88%.
        system = SmartBedsideSystem()
        mock_gpio_output.reset_mock()  # Ignore GPIO.output calls made by the constructor.
        system.alarm_on = True
        system.manage_alarm()
        # Assert that the buzzer was turned OFF.
        mock_gpio_output.assert_called_once_with(system.BUZZER_PIN, False)
        # Assert that the alarm status was updated to OFF.
        self.assertFalse(system.alarm_on)

    @patch.object(GPIO, "output")
    @patch.object(SmartBedsideSystem, "read_vital_signs")
    def test_manage_alarm_invalid_spo2(self,
            mock_read_vital_signs: MagicMock, mock_gpio_output: MagicMock):
        mock_read_vital_signs.side_effect = SmartBedsideError  # Simulate an invalid SpO2 reading.
        system = SmartBedsideSystem()
        mock_gpio_output.reset_mock()  # Ignore GPIO.output calls made by the constructor.
        system.alarm_on = True
        # Assert that the SmartBedsideError is propagated to the caller.
        self.assertRaises(SmartBedsideError, system.manage_alarm)
        # Assert that the buzzer output was not changed.
        mock_gpio_output.assert_not_called()
        # Assert that the alarm status was not changed.
        self.assertTrue(system.alarm_on)


##########################################################################################
########################### Acceptance Tests for User Story #3 ###########################
##########################################################################################

class TestUserStory3(unittest.TestCase):

    @patch.object(GPIO, "setup")
    def test_button_initialization(self, mock_gpio_setup: MagicMock):
        system = SmartBedsideSystem()
        accepted_calls = [
            call(system.BUTTON_PIN, GPIO.IN),
            call(system.BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN),
        ]
        # Assert that the button pin was configured as an input pin (optionally with a pull-down).
        found = False
        for accepted_call in accepted_calls:
            if accepted_call in mock_gpio_setup.call_args_list:
                found = True
        self.assertTrue(found)

    @patch.object(GPIO, "output")
    @patch.object(GPIO, "input")
    def test_stop_alarm_button_pressed(self,
            mock_gpio_input: MagicMock, mock_gpio_output: MagicMock):
        mock_gpio_input.return_value = True
        system = SmartBedsideSystem()
        mock_gpio_output.reset_mock()  # Ignore GPIO.output calls made by the constructor.
        system.alarm_on = True
        system.stop_alarm()
        # Assert that the buzzer was turned OFF.
        mock_gpio_output.assert_called_once_with(system.BUZZER_PIN, False)
        # Assert that the alarm status was updated to OFF.
        self.assertFalse(system.alarm_on)

    @patch.object(GPIO, "output")
    @patch.object(GPIO, "input")
    def test_stop_alarm_button_not_pressed(self,
            mock_gpio_input: MagicMock, mock_gpio_output: MagicMock):
        mock_gpio_input.return_value = False
        system = SmartBedsideSystem()
        mock_gpio_output.reset_mock()  # Ignore GPIO.output calls made by the constructor.
        system.alarm_on = True
        system.stop_alarm()
        # Assert that the buzzer output was not changed.
        mock_gpio_output.assert_not_called()
        # Assert that the alarm status remains ON.
        self.assertTrue(system.alarm_on)


##########################################################################################
########################### Acceptance Tests for User Story #4 ###########################
##########################################################################################

class TestUserStory4(unittest.TestCase):

    @patch.object(GPIO, "PWM")
    @patch.object(GPIO, "setup")
    def test_o2_servo_initialization(self, mock_gpio_setup: MagicMock, mock_gpio_pwm: MagicMock):
        system = SmartBedsideSystem()
        # Assert that the servo motor pin was configured as an output pin.
        mock_gpio_setup.assert_any_call(system.O2_SERVO_PIN, GPIO.OUT)
        # Assert that the PWM instance was created with the correct pin and frequency.
        mock_gpio_pwm.assert_called_once_with(system.O2_SERVO_PIN, 50)
        # Assert that the PWM signal was started with a 5.0% duty cycle.
        mock_gpio_pwm.return_value.start.assert_called_once_with(5.0)
        # Assert that the servo angle was initialized to 0 degrees.
        self.assertEqual(system.o2_valve_angle, 0.0)

    @patch.object(GPIO, "PWM")
    def test_set_o2_valve_angle_in_between(self, mock_gpio_pwm: MagicMock):
        system = SmartBedsideSystem()
        mock_gpio_pwm.return_value.reset_mock()  # Ignore servo calls made by the constructor.
        system.set_o2_valve_angle(90)
        # Assert that the PWM duty cycle was updated to 7.5%.
        mock_gpio_pwm.return_value.ChangeDutyCycle.assert_called_once_with(7.5)
        # Assert that the stored valve angle was updated.
        self.assertEqual(system.o2_valve_angle, 90)

    @patch.object(GPIO, "PWM")
    def test_set_o2_valve_angle_minimum(self, mock_gpio_pwm: MagicMock):
        system = SmartBedsideSystem()
        mock_gpio_pwm.return_value.reset_mock()  # Ignore servo calls made by the constructor.
        system.set_o2_dvalve_angle(0)
        # Assert that the PWM duty cycle was updated to 5.0%.
        mock_gpio_pwm.return_value.ChangeDutyCycle.assert_called_once_with(5.0)
        # Assert that the stored valve angle was updated to 0 degrees.
        self.assertEqual(system.o2_valve_angle, 0)

    @patch.object(GPIO, "PWM")
    def set_o2_dvalve_angle(self, angle: float) -> None:
        """
        Set the oxygen delivery valve to the specified angle
        by controlling the servo motor.

        Args:
            angle (float): Target angle between 0 and 180 degrees.

        Raises:
            SmartBedsideError: If the target angle is outside
            the valid range of 0 to 180 degrees.
        """

        if not 0 <= angle <= 180:
            raise SmartBedsideError(
                "Angle must be between 0 and 180 degrees."
            )

        duty_cycle = 5.0 + (angle / 180.0) * 5.0

        self.o2_servo.ChangeDutyCycle(duty_cycle)

        self.o2_valve_angle = angle

    def test_set_o2_valve_angle_maximum(self, mock_gpio_pwm: MagicMock):
        system = SmartBedsideSystem()
        mock_gpio_pwm.return_value.reset_mock()  # Ignore servo calls made by the constructor.
        system.set_o2_valve_angle(180)
        # Assert that the PWM duty cycle was updated to 10.0%.
        mock_gpio_pwm.return_value.ChangeDutyCycle.assert_called_once_with(10.0)
        # Assert that the stored valve angle was updated to 180 degrees.
        self.assertEqual(system.o2_valve_angle, 180)

    @patch.object(GPIO, "PWM")
    def test_set_o2_valve_angle_invalid_above_limit(self, mock_gpio_pwm: MagicMock):
        system = SmartBedsideSystem()
        mock_gpio_pwm.return_value.reset_mock()  # Ignore servo calls made by the constructor.
        # Assert that SmartBedsideError is raised for an invalid angle.
        self.assertRaises(SmartBedsideError, system.set_o2_valve_angle, 181)
        # Assert that the servo position was not changed.
        mock_gpio_pwm.return_value.ChangeDutyCycle.assert_not_called()

    @patch.object(GPIO, "PWM")
    def test_set_o2_valve_angle_invalid_below_limit(self, mock_gpio_pwm: MagicMock):
        system = SmartBedsideSystem()
        mock_gpio_pwm.return_value.reset_mock()  # Ignore servo calls made by the constructor.
        # Assert that SmartBedsideError is raised for an invalid angle.
        self.assertRaises(SmartBedsideError, system.set_o2_valve_angle, -1)
        # Assert that the servo position was not changed.
        mock_gpio_pwm.return_value.ChangeDutyCycle.assert_not_called()


##########################################################################################
########################### Acceptance Tests for User Story #5 ###########################
##########################################################################################

class TestUserStory5(unittest.TestCase):

    @patch.object(GPIO, "PWM")
    @patch.object(SmartBedsideSystem, "read_vital_signs")
    def test_manage_oxygen_valve_close(self,
            mock_read_vital_signs: MagicMock, mock_gpio_pwm: MagicMock):
        mock_read_vital_signs.return_value = 95 # Simulate a valid SpO2 reading of 95%.
        system = SmartBedsideSystem()
        mock_gpio_pwm.return_value.reset_mock()  # Ignore servo calls made by the constructor.
        system.manage_oxygen_valve()
        # Assert that the servo duty cycle was set to 5.0% (valve fully closed).
        mock_gpio_pwm.return_value.ChangeDutyCycle.assert_called_once_with(5.0)
        # Assert that the stored valve angle was updated to 0 degrees.
        self.assertEqual(system.o2_valve_angle, 0)

    @patch.object(GPIO, "PWM")
    @patch.object(SmartBedsideSystem, "read_vital_signs")
    def manage_oxygen_valve(self) -> None:
        """
        Automatically regulate the oxygen delivery valve based
        on the patient's blood oxygen saturation (SpO2).

        If SpO2 is below 95%, fully open the valve.
        Otherwise, fully close the valve.

        Raises:
            SmartBedsideError: If the SpO2 reading is invalid.
        """

        spo2 = self.read_vital_signs()

        if spo2 < 95:
            self.o2_servo.ChangeDutyCycle(10.0)
            self.o2_valve_angle = 180

        else:
            self.o2_servo.ChangeDutyCycle(5.0)
            self.o2_valve_angle = 0

    def test_manage_oxygen_valve_open(self,
            mock_read_vital_signs: MagicMock, mock_gpio_pwm: MagicMock):
        mock_read_vital_signs.return_value = 94 # Simulate a valid SpO2 reading of 94%.
        system = SmartBedsideSystem()
        mock_gpio_pwm.return_value.reset_mock()  # Ignore servo calls made by the constructor.
        system.manage_oxygen_valve()
        # Assert that the servo duty cycle was set to 10.0% (valve fully open).
        mock_gpio_pwm.return_value.ChangeDutyCycle.assert_called_once_with(10.0)
        # Assert that the stored valve angle was updated to 180 degrees.
        self.assertEqual(system.o2_valve_angle, 180)

    @patch.object(GPIO, "PWM")
    @patch.object(SmartBedsideSystem, "read_vital_signs")
    def test_manage_oxygen_valve_invalid_spo2(self,
            mock_read_vital_signs: MagicMock, mock_gpio_pwm: MagicMock):
        mock_read_vital_signs.side_effect = SmartBedsideError  # Simulate an invalid SpO2 reading.
        system = SmartBedsideSystem()
        mock_gpio_pwm.return_value.reset_mock()  # Ignore servo calls made by the constructor.
        system.o2_valve_angle = 90.0
        # Assert that the SmartBedsideError is propagated to the caller.
        self.assertRaises(SmartBedsideError, system.manage_oxygen_valve)
        # Assert that the servo position was not changed.
        mock_gpio_pwm.return_value.ChangeDutyCycle.assert_not_called()
        # Assert that the stored valve angle was not changed.
        self.assertEqual(system.o2_valve_angle, 90.0)


##########################################################################################
######################## Run the acceptance tests of ALL user stories ####################
##########################################################################################

if __name__ == "__main__":
    unittest.main()