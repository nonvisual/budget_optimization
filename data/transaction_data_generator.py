import pandas as pd
import numpy as np
import datetime


def generate_transaction_data(
    data_size: int = 400,
    start_date=datetime.date(2019, 1, 1),
    end_date=datetime.date(2020, 1, 1),
    seed=1245,
) -> pd.DataFrame:
    np.random.seed(seed=seed)
    info_recs = [
        "Lidl",
        "Rewe",
        "Edeka",
        "Aldi",
        "Zalando",
        "Amazon",
        "Decathlon",
        "Mediamarkt",
        "Easyjet",
        "Lufthansa",
        "Booking.com",
    ]
    multipliers_recs = [1, 1, 1, 1, 2, 2, 3, 4, 10, 15, 25]
    rec_probabilities = np.array([7, 5, 10, 5, 3, 3, 1, 0.5, 0.1, 0.1, 0.1])
    rec_probabilities = rec_probabilities / sum(rec_probabilities)

    choices = np.random.choice(len(info_recs), data_size, p=rec_probabilities)
    data = pd.DataFrame(
        {
            "Beneficiary / Originator": np.take(info_recs, choices),
            "Payment Details": np.take(info_recs, choices),
            "Debit": np.take(multipliers_recs, choices),
        }
    )

    data["Debit"] = round(data["Debit"] * np.random.rand(data_size) * 60, 2)
    data["Booking date"] = generate_random_date(start_date, end_date, data_size)
    data["Credit"] = np.nan

    data = add_rent_transactions(data, start_date, end_date, amount=1300.0)
    data = add_salary_transactions(data, start_date, end_date, amount=3000.0)
    data["Currency"] = "EUR"
    return data.sample(frac=1).reset_index(drop=True)


def add_rent_transactions(data, start_date, end_date, amount=1200.0):
    dates = pd.date_range(start_date, end_date, freq="MS").strftime("%m/%d/%Y").tolist()
    data_rent = pd.DataFrame(
        {
            "Beneficiary / Originator": ["Landlord"] * len(dates),
            "Payment Details": ["Rent"] * len(dates),
            "Debit": [amount] * len(dates),
            "Credit": np.nan,
            "Booking date": dates,
        }
    )

    data = pd.concat([data_rent, data])
    return data


def add_salary_transactions(data, start_date, end_date, amount=1200.0):
    dates = pd.date_range(start_date, end_date, freq="MS").strftime("%m/%d/%Y").tolist()

    data_rent = pd.DataFrame(
        {
            "Beneficiary / Originator": np.nan,
            "Payment Details": ["Salary"] * len(dates),
            "Debit": np.nan,
            "Credit": [amount] * len(dates),
            "Booking date": dates,
        }
    )

    data = pd.concat([data_rent, data])
    return data


def generate_random_date(start_date, end_date, size):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = np.random.randint(days_between_dates, size=size)

    days_to_date_string = lambda x: (
        start_date + datetime.timedelta(days=int(x))
    ).strftime("%m/%d/%Y")
    days_to_date_string = np.vectorize(days_to_date_string)

    return days_to_date_string(random_number_of_days)
