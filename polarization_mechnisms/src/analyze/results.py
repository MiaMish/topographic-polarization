from uuid import UUID

from numpy import ndarray


class MeasurementResult:

    def __init__(self, y: ndarray, sample_stds: ndarray, x: ndarray, experiment_id: UUID, measurement_type: str,
                 display_name: str or None = None) -> None:
        self.y = y
        self.sample_stds = sample_stds
        self.x = x
        self.experiment_id = experiment_id
        self.measurement_type = measurement_type
        self.display_name = f"{experiment_id}_{measurement_type}" if display_name is None else display_name
