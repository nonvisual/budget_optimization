from typing import Dict, List
import pandas as pd


def assign_type(row, types_mapping: Dict[str, List[str]], info_columns: List[str]):
    matching = []

    for c in info_columns:
        if not pd.isna(row[c]):
            matching.extend(
                [
                    s
                    for s in types_mapping
                    if any(xs in row[c].lower() for xs in types_mapping[s])
                ]
            )
    matching.append("unknown")
    return matching[0]
