import numpy as np
from spyre import server
from functions import createFrame

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
    tabs = ['Plot', 'Table', 'Plot_month', 'Table_month']
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
            'id': 'table',
            'control_id': 'update_data',
            'tab': 'Table'
        },
        {
            'type': 'plot',
            'id': 'plot_month',
            'control_id': 'update_data',
            'tab': 'Plot_month',
            'on_page_load': True,
        },
        {
            'type': 'table',
            'id': 'table_month',
            'control_id': 'update_data',
            'tab': 'Table_month'
        }
    ]

    def plot(self, params):
        df = self.table(params)
        df.set_index('Week', inplace=True)
        fig = (df.plot()
               .get_figure())
        return fig

    def table(self, params):
        df = self.select(params)
        df = df[['Week', params['dt']]]
        return df

    def plot_month(self, params):
        df = self.table_month(params)
        fig = (df.plot()
               .get_figure())
        return fig

    def table_month(self, params):
        vhimonth_df = self.select(params)
        vhimonth_df["Month"] = 7 * vhimonth_df["Week"] // 31 + 1
        vhimonth_df = (vhimonth_df.groupby("Month")
                       .agg({"VHI": ["min", "max", "mean"]}))
        return vhimonth_df

    def select(self, params):
        ID = [int(params['prc'])]
        df = createFrame(ID)

        df = df.loc[
                  (df['Week'] >= int(params['from'])) &
                  (df['Week'] <= int(params['to'])) &
                  (df['Year'] == int(params['year']))
                  ]
        return df

global_df = createFrame(range(1, len(provinces) + 1))

app = app()
app.launch(port=9093)
