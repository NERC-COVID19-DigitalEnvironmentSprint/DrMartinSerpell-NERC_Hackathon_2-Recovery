from pathlib import Path
import pandas as pd
import numpy as np

PATH = Path(__file__).parents[1]
DATA_PATH = (PATH / "data").resolve()
assert DATA_PATH.exists()


def load_data(filename, datetime_format=None):
    file_path = DATA_PATH / filename
    assert file_path.exists()

    if file_path.suffix == '.csv':
        data = pd.read_csv(DATA_PATH / filename)
    elif file_path.suffix == '.json':
        data = pd.read_json(str(file_path))
    else:
        raise TypeError(f'{file_path.suffix} is not supported.')

    data.rename(lambda x: str(x).lower(), axis='columns', inplace=True)
    if 'date' in list(data.keys()):
        data['date'] = pd.to_datetime(data['date'], format=datetime_format)
    return data


def get_mins_maxs():
    df = load_data('ALL_rm_daily_2.csv')
    the_keys = [k for k in list(df.keys()) if k not in ('location', 'date')]
    min_maxs = {pollutant: {'min': df[pollutant].min(),
                            'max': df[pollutant].max()}
                for pollutant in the_keys}
    return min_maxs


def get_locations():
    meta_df = load_data('all_meta_2019.csv')
    locs_df = meta_df[['code', 'site']]
    u, idx = np.unique(locs_df['code'].values, return_index=True)

    return locs_df.iloc[idx, :]


meta_df = load_data('all_meta_2019.csv')
diff_df = load_data('ALL_rm_daily_2.csv')
min_max_dict = get_mins_maxs()
dates = [str(diff_df['date'][i]) for i in range(len(np.unique(diff_df['date'])))]
dmarks = dates[5::7]


def get_avail_data(pollutant, date=None):
    # load data
    if date is None:
        df = diff_df[['location', pollutant]]
    else:
        df = diff_df[['location', pollutant, 'date']]
    df = df.dropna()
    return df


def get_available_locs(pollutant):
    df = get_avail_data(pollutant)
    u_loc = pd.unique(df['location'].values)
    return u_loc


def get_date(d):
    return dates[d]


def get_datemarks(d):
    return dmarks[d]


if __name__ == '__main__':
    print(PATH)
    print(DATA_PATH)
