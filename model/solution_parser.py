import pandas as pd
from typing import Dict, Any, Tuple
import pulp
import logging
import numpy as np

logger = logging.getLogger(__name__)


def parse_solution(
    data: pd.DataFrame, decision_vars: Dict[int, Any], model
) -> Tuple[pd.Series, float]:
    if model.status != pulp.const.LpStatusOptimal:
        raise Exception(f"Cannot parse solution of not optimally solved model")

    logging.info(f"Status is optimal, parsing solution")
    df = pd.Series(
        [decision_vars[t].varValue for t in range(len(data))],
        index=data.index,
        name="solution",
        dtype=np.int64,
    )
    objective = pulp.value(model.objective)

    return df, objective
