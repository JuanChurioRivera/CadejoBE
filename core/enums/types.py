from enum import Enum


class QualityOfSleep(str, Enum):
    """Maps to Sleep.quality_of_sleep"""

    POOR = "POOR"
    MID = "MID"
    GOOD = "GOOD"
    EXCELLENT = "EXCELLENT"


class SleepStage(str, Enum):
    """Maps to SleepSegment.sleep_stage"""

    AWAKE = "AWAKE"
    LIGHT_SLEEP = "LIGHT_SLEEP"
    DEEP_SLEEP = "DEEP_SLEEP"
    REM = "REM"


class UserRole(str, Enum):
    """Maps to UserPreferences.role """
    ADMIN = "ADMIN"
    USER = "USER"