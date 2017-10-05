import numpy as np
import pandas as pd

class create_prod_dict:
    ''' Create a dictionary based on a dataframe, key, and value column names '''
    
    def __init__(self, df, key_colName='ProductId', val_colName='ProductName', val_colName_2='CSPC', val_colName_3='UnitSizeML', val_colName_4='RetailPrice'):
        self.df = df
        self.key = key_colName
        self.val = val_colName
        self.val_2 = val_colName_2
        self.val_3 = val_colName_3
        self.val_4 = val_colName_4
        
    def create_dict(self):
        product_dict = {}
        for i in self.df[self.key].unique():
            product_dict[i] = [('Name', self.df.loc[self.df[self.key] == i, self.val].unique()[0]), \
                               ('CSPC', self.df.loc[self.df[self.key] == i, self.val_2].unique()[0]), \
                               ('Size ml', self.df.loc[self.df[self.key] == i, self.val_3].unique()[0]), \
                               ('Price', self.df.loc[self.df[self.key] == i, self.val_4].unique()[0]), \
                              ]

#         Dictionary comprehension for single key-value pair
#         product_dict = {i: self.df.loc[self.df[self.key] == i, self.val].unique()[0] for i in self.df[self.key].unique()}


        return product_dict

class map_to_dict:
    ''' Using a dictionary, map a series of productId to a series of productName '''
    
    def __init__(self, id_series, dict_):
        self.id_series = id_series
        self.dict_ = dict_
    
    def map_each_id(self, id_):
        try:
            name = self.dict_[id_]
        except KeyError as e:
            name = None
        return name
        
    
    def map_to_series(self):
        return self.id_series.map(self.map_each_id)

if __name__ == '__main__':
    
    # Load in CSV files
    rec_result = \
        pd.read_csv('Recommender_System_Pelee_Island _Web Service_ - 506153734175476c4f62416c57734963.faa6ba63383c4086ba587abf26b85814.v1-default-1643 - Results dataset (StoreId, ProductId).csv')
    prod_info = pd.read_csv('peele_island_product_data.csv')

    
    # Create the dictionary
    create_dict = create_prod_dict(prod_info, 'ProductId', 'ProductName')
    prod_dict = create_dict.create_dict()

    
    # Map each productId in rec_result dataframe to productName using the dictionary\
    for i in range(1, 11):
        id_to_dict = map_to_dict(rec_result['Item {}'.format(i)], prod_dict)
        rec_result['Item_{}_Name'.format(i)] = id_to_dict.map_to_series()
    
    
    # Save result as CSV
    rec_result.to_csv('./Recommender_Pelee_Island_Web_Result_Edited.csv', index=False)
    
    # Save result transposed as CSV
    rec_result.T.to_csv('./Recommender_Pelee_Island_Web_Result_Edited_Transposed.csv', index=False)
    
    print(rec_result.head())