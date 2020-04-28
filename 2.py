import pandas as pd
import numpy as np
import requests
from spyre import server

newIDs = [24, 25, 5, 6, 27, 23, 26, 7, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 8, 9, 10, 1, 3, 2, 4]

provinces = [
    'Cherkasy',
    'Chernihiv',
    'Chernivtsi',
    'Crimea',
    'Dnipro',
    'Donets\'k',
    'Ivano-Frankivs\'k',
    'Kharkiv',
    'Kherson',
    'Khmel\'nyts\'kyy',
    'Kiev',
    'Kiev City',
    'Kirovograd',
    'Luhans\'k',
    'L\'viv',
    'Mykolayiv',
    'Odessa',
    'Poltava',
    'Rivne',
    'Sevastopol\'',
    'Sumy',
    'Ternopil\'',
    'Transcarpathia',
    'Vinnytsya',
    'Volyn',
    'Zaporizhzhya',
    'Zhytomyr'
]


def cleanup(data: str):
    start = data.find("<pre>") + 5
    end = data.find("</pre>")
    data = data[start:end]
    data = data.replace(" ", "")
    data = data.replace("\\n", "\n")
    return data


def downloadData(ID):
    for id in ID:
        url = f"https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={newIDs[id - 1]}&year1=1981&year2=2020&type=Mean"
        filename = f"{id}"
        with requests.get(url, headers={"Accept": "text/plain"}) as plain:
            data = str(plain.content)
            data = cleanup(data)
        with open(f"Data/{filename}.csv", "w+") as output:
            output.write(f"Year,Week,SMN,SMT,VCI,TCI,VHI\n")
            output.write(data)


def createFrame(ID):
    tempframes = []
    for id in ID:
        try:
            with open(f'Data/{id}.csv') as f:
                pass
        except IOError:
            downloadData([id])
        temp = pd.read_csv(f"Data/{id}.csv", header=0, index_col=False)
        temp["Province"] = id
        tempframes.append(temp)

    df = pd.concat(tempframes)
    return df


class app(server.App):
    title = "VHI Visualising"
    inputs = [
        {
            'type': 'dropdown',
            'label': 'Province',
            'options': [
                {'label': 'Cherkasy', 'value': 1},
                {'label': 'Chernihiv', 'value': 2},
                {'label': 'Chernivtsi', 'value': 3},
                {'label': 'Crimea', 'value': 4},
                {'label': 'Dnipro', 'value': 5},
                {'label': "Donets'k", 'value': 6},
                {'label': "Ivano-Frankivs'k", 'value': 7},
                {'label': 'Kharkiv', 'value': 8},
                {'label': 'Kherson', 'value': 9},
                {'label': "Khmel'nyts'kyy", 'value': 10},
                {'label': 'Kiev', 'value': 11},
                {'label': 'Kiev City', 'value': 12},
                {'label': 'Kirovograd', 'value': 13},
                {'label': "Luhans'k", 'value': 14},
                {'label': "L'viv", 'value': 15},
                {'label': 'Mykolayiv', 'value': 16},
                {'label': 'Odessa', 'value': 17},
                {'label': 'Poltava', 'value': 18},
                {'label': 'Rivne', 'value': 19},
                {'label': "Sevastopol'", 'value': 20},
                {'label': 'Sumy', 'value': 21},
                {'label': "Ternopil'", 'value': 22},
                {'label': 'Transcarpathia', 'value': 23},
                {'label': 'Vinnytsya', 'value': 24},
                {'label': 'Volyn', 'value': 25},
                {'label': 'Zaporizhzhya', 'value': 26},
                {'label': 'Zhytomyr', 'value': 27}
            ],
            'action_id': 'update_data',
            'key': 'prc',
            'value': 1,
        },
        {
            'type': 'dropdown',
            'label': 'Data type',
            'options': [
                {'label': 'VCI', 'value': 'VCI'},
                {'label': 'TCI', 'value': 'TCI'},
                {'label': 'VHI', 'value': 'VHI'}
            ],
            'action_id': 'update_data',
            'key': 'dt',
            'value': 1,
        },
        {
            'type': 'text',
            'label': 'Year',
            'action_id': 'update_data',
            'key': 'year',
            'value': 1982,
        },
        {
            'type': 'text',
            'label': 'From week',
            'action_id': 'update_data',
            'key': 'from',
            'value': 1,
        },
        {
            'type': 'text',
            'label': 'To week',
            'action_id': 'update_data',
            'key': 'to',
            'value': 52,
        }
    ]
    controls = [
        {
            'type': 'hidden',
            'id': 'update_data'
        }
    ]
    tabs = ['Plot', 'Table', 'country_df']
    outputs = [
        {
            'type': 'plot',
            'id': 'plot',
            'control_id': 'update_data',
            'tab': 'Plot',
            'on_page_load': True,
        },
        {
            'type': 'table',
            'id': 'plot_data',
            'control_id': 'update_data',
            'tab': 'Table'
        },
        {
            'type': 'table',
            'id': 'country_df',
            'tab': 'country_df'
        }
    ]

    def getData(self, params):
        if params['output_id'] == 'plot_data':
            return self.plot_data(params)
        elif params['output_id'] == 'country_df':
            return self.country_df(params)

    def getPlot(self, params):
        df = self.plot_data(params)
        df.set_index('Week', inplace=True)
        fig = (df.plot()
               .get_figure())
        return fig

    def country_df(self, params):
        df = (global_df.groupby("Year")
              .agg({"VHI": ["min", "max", "mean"]})
              .reset_index()
              .astype({"Year": np.int8}))
        return df

    def plot_data(self, params):
        ID = [int(params['prc'])]
        df = createFrame(ID)

        df = (df.loc[
                  (df['Week'] >= int(params['from'])) &
                  (df['Week'] <= int(params['to'])) &
                  (df['Year'] == int(params['year']))
                  ]
              .where(df[params['dt']] != -1)
              .dropna()
              )
        df = df[['Week', params['dt']]]
        return df


global_df = createFrame(range(1, len(provinces) + 1))
global_df = (global_df.where(global_df["VHI"] != -1)
             .dropna())

app = app()
app.launch(port=9093)
