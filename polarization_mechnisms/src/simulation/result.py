from copy import deepcopy
from typing import List, Dict

import numpy as np
import pandas as pd
from numpy import ndarray


class IterationResult:

    def __init__(self, opinions_list: List[float]) -> None:
        # TODO: change from dict to pd/np obj for performance
        self.opinions_list = sorted(deepcopy(opinions_list))

    def get_opinions(self) -> ndarray:
        return np.array(self.opinions_list)

    def get_opinion(self, i: int) -> float:
        return self.opinions_list[i]


class SimulationResult:

    def __init__(self) -> None:
        # TODO: change from dict to pd/np obj for performance
        self.iteration_map: Dict[str, IterationResult] = {}

    def get_results_df(self) -> pd.DataFrame:
        return pd.DataFrame({k: v.get_opinions() for k, v in self.iteration_map.items()}).transpose()

    def add_iteration_result(self, iteration: int, to_results: IterationResult) -> None:
        self.iteration_map[f"{iteration}"] = to_results

    def get_iteration(self, iteration: int) -> IterationResult:
        return self.iteration_map.get(str(iteration))
