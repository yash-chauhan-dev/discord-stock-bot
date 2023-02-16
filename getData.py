import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import datetime

class GetData():
    def __init__(self, company) -> None:
        self.company_name = company
        self.company = yf.Ticker(company)

    def query_data(self, period, interval):
        self.data_historical = self.company.history(period=period, interval=interval)
        return self.data_historical
        # self.data_historical.to_csv('file1.csv')
    
    def plot_and_save_graph(self, df, name, title="", multiple=False):
        # Plot the closing price against the Datetime

        fig = px.line(df, x = df.index, y = 'Close', title='{}'.format(title))
        if multiple:
            fig = px.line(df, x = df.index, y = df.columns[0:4], title='{}'.format(title))


        # Write images to directory
        if not os.path.exists("images/{}".format(self.company_name)):
            os.mkdir("images/{}".format(self.company_name))

        # save image
        img_file_name = "{}_{}_{}.png".format(name, self.company_name, datetime.date.today().isoformat())

        fig.write_image("images/{}/{}".format(self.company_name, img_file_name))

    def plot_comparision_graph(self, df_dict):
        # Plot the closing price against the Datetime

        fig = go.Figure()

        for dataframe in df_dict:
            fig = fig.add_trace(go.Scatter(x = df_dict[dataframe].index, y = df_dict[dataframe]["Close"], name = dataframe))

        # Write images to directory
        if not os.path.exists("images"):
            os.mkdir("images")

        # save image
        img_file_name = "{}_{}_{}.png".format("compare", self.company_name, datetime.date.today().isoformat())

        fig.write_image("images/{}".format(img_file_name))

    def get_eod(self, df):
        message_list = ["{} EOD data".format(self.company_name)]
        for item in df.iloc[0].items():
            message_list.append("- {} : {}".format(item[0], item[1]))
        return message_list