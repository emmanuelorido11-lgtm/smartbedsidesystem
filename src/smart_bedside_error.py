class SmartBedsideError(Exception):
    """Custom exception raised for errors in SmartBedsideSystem."""
    pass

def read_vital_signs(self) -> int:
    """
    Read the patient's blood oxygen saturation (SpO₂).
    Returns: int: SpO₂ percentage (70–100).
    Raises: SmartBedsideError: If the sensor returns an invalid reading (-1).
    """

    spo2 = self.spo2_hr_sensor.get_spo2()

    if spo2 == -1 or spo2 is None:
        raise SmartBedsideError("Invalid SpO₂ reading from MAX30102 sensor.")

    if not 70 <= spo2 <= 100:
        raise SmartBedsideError("SpO₂ reading is outside the valid range (70–100).")

    return int(spo2)