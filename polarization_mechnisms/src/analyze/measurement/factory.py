from analyze.measurement import constants
from analyze.measurement.base import Measurement
from analyze.measurement.binsvar import VarianceInBinsMeasurement
from analyze.measurement.clusterscount import ClustersCountMeasurement
from analyze.measurement.coveredbins import CoveredBinsMeasurement
from analyze.measurement.disconnect import DisconnectIndexMeasurement
from analyze.measurement.dispersion import DispersionMeasurement
from analyze.measurement.peaks import PeaksMeasurement
from analyze.measurement.ripley import RipleyEstimatorMeasurement
from analyze.measurement.spread import SpreadMeasurement


class MeasurementFactory:

    def by_name(self, measurement_name: str) -> Measurement:
        if measurement_name == constants.NUM_OF_CLUSTERS:
            return ClustersCountMeasurement()
        if measurement_name == constants.COVERED_BINS:
            return CoveredBinsMeasurement()
        if measurement_name == constants.DISCONNECT_INDEX:
            return DisconnectIndexMeasurement()
        if measurement_name == constants.DISPERSION:
            return DispersionMeasurement()
        if measurement_name == constants.NUM_OF_LOCAL_MAX:
            return PeaksMeasurement()
        if measurement_name == constants.RIPLEY_ESTIMATOR:
            return RipleyEstimatorMeasurement()
        if measurement_name == constants.SPREAD:
            return SpreadMeasurement()
        if measurement_name == constants.BINS_VARIANCE:
            return VarianceInBinsMeasurement()
        raise NotImplementedError(f"Unknown measurement name {measurement_name}")
