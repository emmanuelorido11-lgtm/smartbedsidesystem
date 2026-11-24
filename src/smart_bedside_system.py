from src.smart_bedside_error import SmartBedsideError

try:
    import RPi.GPIO as GPIO
except ImportError:
    from mock import GPIO

try:
    from pinpong.libs.dfrobot_max30102 import DFRobot_BloodOxygen_S
except ImportError:
    from mock.max30102 import DFRobot_BloodOxygen_S


class SmartBedsideSystem:

    # BOARD (physical) numbers of the pins the components are connected to.
    BUZZER_PIN = 22  # KY-012 active buzzer used as the alarm (see User Story #2).
    BUTTON_PIN = 16  # B3F-1020 pushbutton used to stop the alarm (see User Story #3).
    O2_SERVO_PIN = 12  # MG90S servo motor controlling the oxygen delivery valve (see User Story #4).

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)  # Refer to the GPIO pins by their physical number on the board.
        GPIO.setwarnings(False)  # Disable warnings.

        self.spo2_hr_sensor = None  # Replace None by initializing the MAX30102 sensor (see User Story #1).

        self.alarm_on = None  # Replace None by initializing the alarm status (see User Story #2).

        self.o2_servo = None  # Replace None by initializing the servo motor's PWM instance (see User Story #4).
        self.o2_valve_angle = None  # Replace None by initializing the valve angle, in degrees (see User Story #4).

    def read_vital_signs(self) -> int:
        """
        Read the patient's blood oxygen saturation (SpO₂).
        Returns: int: SpO₂ percentage (70–100).
        Raises: SmartBedsideError: If the sensor returns an invalid reading (-1).
        """
        # See User Story #1.

    def read_vital_signs(self) -> int:
        spo2 = self.spo2_hr_sensor.get_spo2()

        if spo2 == -1:
            raise SmartBedsideError("Invalid SpO2 reading")

        return int(spo2)

    def manage_alarm(self) -> None:

        # See User Story #2.

        def update_spo2_alarm(self) -> None:
            spo2 = self.read_vital_signs()  # Propagates SmartBedsideError
            if spo2 < self.SPO2_ALARM_THRESHOLD:
                self.activate_alarm()
            else:
                self.deactivate_alarm()

    def stop_alarm(self) -> None:
        """
        Stop the alarm if the pushbutton is pressed. Otherwise, leave the alarm unchanged.
        """
        # See User Story #3.

        def stop_alarm(self) -> None:

            if GPIO.input(self.BUTTON_PIN) == GPIO.LOW:
                GPIO.output(self.BUZZER_PIN, GPIO.LOW)
                self.alarm_on = False

        def stop_alarm(self) -> None:

            if GPIO.input(self.BUTTON_PIN) == GPIO.LOW:
                GPIO.output(self.BUZZER_PIN, GPIO.LOW)
                self.alarm_on = False

                GPIO.setup(self.BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def set_o2_valve_angle(self, angle: float) -> None:
        """
        Set the oxygen delivery valve to the specified angle by controlling the servo motor.
        Args: angle (float): The target valve angle in degrees, between 0 and 180 degrees, inclusive.
        Raises: SmartBedsideError: If the target angle is outside the valid range of 0 to 180 degrees.
        """
        # See User Story #4.

    def set_oxygen_valve(self, angle: float) -> None:

        if not 0 <= angle <= 180:
            raise SmartBedsideError("Angle must be between 0 and 180 degrees.")

        duty_cycle = 2.5 + (angle / 180.0) * 10

        self.o2_servo.ChangeDutyCycle(duty_cycle)

        self.o2_valve_angle = angle


    def manage_oxygen_valve(self) -> None:
        """
        Automatically regulate the oxygen delivery valve based on the
        patient's blood oxygen saturation (SpO₂).
        If SpO₂ is below 95%, fully open the oxygen delivery valve.
        Otherwise, fully close the oxygen delivery valve.
        Raises: SmartBedsideError: If the SpO₂ reading is invalid (propagated from read_vital_signs()).
        """
        # See User Story #5.
def regulate_oxygen(self) -> None:
    spo2 = self.read_vital_signs()

    if spo2 < 95:
        self.set_oxygen_valve(180)
    else:
        self.set_oxygen_valve(0)
