import pandas as pd
import glob
import os
from os import listdir

class Automater:

    def __init__(self):
        self.concatinated_df = None
        self.df_row_len = 0

    def htm_to_df(self, files):
        """
        converts from an htm file type to a pandas dataframe.
        Note the xls file from the awt.cbo.gov is recognized as html by pandas
        """
        df_list = []
        for file in files:
            print(file,"^"*10)
            df_Xtype = pd.read_html(file)
            df_Xtype = df_Xtype[0]
            self.df_row_len += len(df_Xtype.index)
            df_list.append(df_Xtype)
        return df_list

    def pre_process_df(self,df_list):
        """
        renames the columns of the dataframes
        """
        clean_df_list = []
        cols = [
                 'Airport','Terminal','Date','Hour','U.S Citizen Avrg Wait',
                 'U.S Citizen Max Wait', 'Non U.S Citizen Avrg Wait', 'Non U.S Citizen Max Wait',
                 'All Avrg Wait', 'All Max Wait',
                 '0-15', '16-30','31-45','46-60','61-90','91-120','120 plus',
                 'Excluded','Total','Flights','Booths'
               ]
        for df in df_list:
            # Change column name
            df.columns = cols
            clean_df_list.append(df)
        return clean_df_list

    def concatinate_df(self,clean_df_list):
        df_list = clean_df_list
        concatinated_df = pd.concat(df_list)
        row_num_orig = len(concatinated_df.index)
        if row_num_orig != self.df_row_len:
            raise ValueError("Some data might have been lost from the input files. ORIGINAL {} Concatinated {}".format(row_num_orig, self.df_row_len))
        return concatinated_df

    def output_csv(self):
        df = self.concatinated_df
        df.to_csv('output.csv')
        print(os.getcwd())
        print("Successfully wrote output.csv file")
