import pandas as pd


def update_descriptions_quntity(dataframe):
    # Create a mapping dictionary based on the first occurrence of each StockCode
    stockcode_first_description = dataframe.groupby('StockCode')['Description'].first().reset_index()
    stockcode_first_description = dict(zip(stockcode_first_description['StockCode'], stockcode_first_description['Description']))

    # Update the Description column based on the mapping
    dataframe['Description'] = dataframe['StockCode'].map(stockcode_first_description)

    df_grouped = dataframe.groupby(['InvoiceNo', 'Description'])['Quantity'].sum().reset_index()
    df_grouped.drop_duplicates(inplace=True)
    df_grouped.reset_index(drop=True, inplace=True)

    df_merged = dataframe.merge(df_grouped, on=['InvoiceNo', 'Description'], suffixes=('', '_updated'), how='left')
    df_merged.drop(columns=['Quantity'], inplace=True)

    df_merged.rename(columns={'Quantity_updated': 'Quantity'}, inplace=True)
    df_merged.drop_duplicates(inplace=True)
    df_merged.reset_index(drop=True, inplace=True)


    return df_merged
