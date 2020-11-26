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


def assign_entity(row, types_mapping: Dict[str, List[str]], info_columns: List[str]):
    matched_entity = []
    for c in info_columns:
        if not pd.isna(row[c]):

            matched_entity.extend(
                [
                    [xs for xs in types_mapping[s] if xs in row[c].lower()][0]
                    for s in types_mapping
                    if any(xs in row[c].lower() for xs in types_mapping[s])
                ]
            )
    matched_entity.append("unknown_entity")

    return matched_entity[0]
