import pandas as pd
import numpy as np

def generate_mock_data(data_size:int=400, seed=1245) ->pd.DataFrame:
    np.random.seed(seed=seed)
    info_recs = ['Lidl', 'Rewe', 'Edeka', 'Aldi', 'Zalando', 'Amazon', 'Decathlon', \
                 'Mediamarkt', 'Easyjet', 'Lufthansa', 'Booking.com']
    type_recs = [1, 1, 1, 1, 2, 4, 4, 4, 5, 5, 5]
    multipliers_recs = [1, 1, 1, 1, 2, 2, 3, 4, 10, 15, 25]
    rec_probabilities = np.array([7, 5, 10, 5, 3, 3, 1, 0.5, 0.1, 0.1, 0.1])
    rec_probabilities = rec_probabilities / sum(rec_probabilities)

    choices = np.random.choice(len(info_recs), data_size, p=rec_probabilities)
    data = pd.DataFrame({'info': np.take(info_recs, choices), 'type': np.take(type_recs, choices), \
                         'amount': np.take(multipliers_recs, choices)})
    data['amount'] = round(data['amount'] * np.random.rand(data_size) * 60, 2)
    total_weeks_number= 42
    data['week'] = np.random.choice(total_weeks_number, data_size)
    data_rent = pd.DataFrame({'info': ['Rent'] * 12, 'type': [3] * 12, \
                              'amount': [1200.0] * 12, 'week': np.round(np.arange(0,52,4.5)).astype(int)})

    data = pd.concat([data_rent, data])
    data['importance'] = np.random.choice(10, len(data))
    data.loc[data['info'] == 'Rent','importance'] = 9
    return data.sample(frac=1).reset_index(drop=True)
