from uuid import UUID

from numpy import ndarray

from analyze.measurment import MeasurementType


class MeasurementResult:

    def __init__(self, y: ndarray, x: ndarray, experiment_id: UUID, measurement_type: MeasurementType,
                 display_name: str or None = None) -> None:
        self.y = y
        self.x = x
        self.experiment_id = experiment_id
        self.measurement_type = measurement_type
        self.display_name = f"{experiment_id}_{measurement_type}" if display_name is None else display_name
