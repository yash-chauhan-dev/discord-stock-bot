import os
from getData import GetData
from discord import File

# @bot.command(name = "graph")
async def graph(ctx, company_name):
    data = GetData(company_name)
    dataframe = data.query_data(period='1d', interval='1m')
    data.plot_and_save_graph(dataframe, name="close")
    data.plot_and_save_graph(dataframe, name="multiple", multiple=True)

    print(os.listdir("images/{}/".format(company_name)))
    for image in os.listdir("images/{}/".format(company_name)):
        if (image.endswith(".png")) and (image.startswith(("multiple", "close"))):
            await ctx.send(file=File("images/{}/{}".format(company_name, image)))
            os.remove("images/{}/{}".format(company_name, image))

async def get_eod_data(ctx, company_name):
    data = GetData(company_name)
    dataframe = data.query_data(period='1d', interval='1d')
    message_list = data.get_eod(dataframe)
    msg_txt = '\n'.join(message_list)

    await ctx.send(msg_txt)

async def last_hour(ctx, company_name):
    data = GetData(company_name)
    dataframe = data.query_data(period='1d', interval='1m')
    last_hour_df = dataframe.iloc[-60:]
    data.plot_and_save_graph(last_hour_df, title="(Last Hour)", name="lastHour")

    for image in os.listdir("images/{}/".format(company_name)):
        if (image.endswith(".png")) and (image.startswith("lastHour")):
            await ctx.send(file=File("images/{}/{}".format(company_name, image)))
            os.remove("images/{}/{}".format(company_name, image))

async def compare(ctx, company_list):
    df_dict = dict()

    for name in company_list:
        data = GetData(name)
        dataframe = data.query_data(period='max', interval='1d')
        df_dict[name] = dataframe

    data.plot_comparision_graph(df_dict)

    for image in os.listdir("images/"):
        if (image.endswith(".png")) and (image.startswith("compare")):
            await ctx.send(file=File("images/{}".format(image)))
            os.remove("images/{}".format(image))
