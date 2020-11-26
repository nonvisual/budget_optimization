import pandas as pd
from preparation.rules_preparer import prepare_rules
from preparation.types_classifier import assign_type, assign_entity
from functools import partial


def prepare_data(data: pd.DataFrame):
    prepare_date_columns(data)
    rules = prepare_rules()
    f = partial(
        assign_type,
        types_mapping=rules,
        info_columns=["Beneficiary / Originator", "Payment Details"],
    )
    data["type"] = data.apply(f, axis=1)

    f = partial(
        assign_entity,
        types_mapping=rules,
        info_columns=["Beneficiary / Originator", "Payment Details"],
    )
    data["entity"] = data.apply(f, axis=1)


def prepare_date_columns(data: pd.DataFrame):
    data["Booking date"] = pd.to_datetime(data["Booking date"])
    data["day"] = data["Booking date"].dt.day
    data["month"] = data["Booking date"].dt.month
    data["year"] = data["Booking date"].dt.year
    data["weekday"] = data["Booking date"].dt.weekday
    data["week"] = data["Booking date"].dt.isocalendar().week
