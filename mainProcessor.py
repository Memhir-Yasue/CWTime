import pandas as pd
from dfply import *


class Automater:

    def __init__(self):
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
                 'Airport','Terminal','Date','Hour','US_Citizen_Avrg_Wait',
                 'U.S_Citizen_Max_Wait', 'Non_U.S_Citizen_Avrg_Wait', 'Non_US_Citizen_Max_Wait',
                 'All_Avrg_Wait', 'All_Max_Wait',
                 '0-15', '16-30','31-45','46-60','61-90','91-120','120_plus',
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

    def add_columns(self,df):
        df['Year'] = pd.Series()
        df['Month'] = pd.Series()
        for row in range(len(df)):
            df.Year[row] = int(float(str(df.Date[row]).split('/')[2]))
            df.Month[row] = int(float(str(df.Date[row]).split('/')[0]))
        # df['Year1'] = str(df.Year).split('\\')
        return df

    def output_csv(self, df):
        df.to_csv('output.csv')
        print(os.getcwd())
        print("Successfully wrote output.csv file")

class by_Year_Month:
    def __init__(self):
        self.df_row_len = 0

    def convert_to_by_yr_m(self, df):
        return (df >>
        select(X.Airport, X.Year, X.Month, X.All_Avrg_Wait) >>
        group_by(X.Year, X.Airport, X.Month) >>
        summarize(Average_wait_time = X.All_Avrg_Wait.mean()) )

        # return pd.DataFrame(data=df)

    def make_airport_column(self, df):
        airport_column = []
        for airport in df.Airport:
            if airport not in airport_column:
                airport_column.append(airport)
            if len(airport_column) == len(set(df.Airport)):
                break
        num_months = int(df.shape[0] / len(airport_column))
        return airport_column, num_months

    def make_wait_time_list(self,df,num_months):
        wait_time_list = []
        begin = 0
        for i in range(len(df)):
        # i + 1 so that the last set of data is included. Example if 47 is the last row, then i+1 = 48
            if ((i + 1) % num_months == 0) & (i != 0):
                to_append = list(df['Average_wait_time'][begin:i + 1])
                wait_time_list.append(to_append)
                begin = i + 1
    #         print(i+1,"MOD ME")
        return wait_time_list

    def make_airport_wait_time(self,airport_column, wait_time_list):
        airport_dict = {}
        i = 0
        for airport in airport_column:
            airport_dict[airport] = wait_time_list[i]
            i+=1
        return airport_dict

    def make_airport_col_df(self,airport_column,airport_dict):
        airport_df = pd.DataFrame(columns=[airport for airport in airport_column])
        for airport in airport_column:
            airport_df[airport] = airport_dict[airport]
        return airport_df

    def make_year_col_df(self,df,year):
        row_num = df.shape[0]
        some_df = pd.DataFrame({'Year':[year for i in range(row_num)]})
        return some_df

    def make_month_col_df(self,num_months):
        month_df = pd.DataFrame({'Month':[int(i+1) for i in range(num_months)]})
        return month_df

    def process_by_year(self,df):
        yearly_df_list = []
        for year in set(df.Year):
            df_year = df[df.Year == year]
            airport_col, num_months = self.make_airport_column(df_year)
            wait_time_list = self.make_wait_time_list(df_year,num_months)
            airport_dict = self.make_airport_wait_time(airport_col,wait_time_list)

            airport_df = self.make_airport_col_df(airport_col,airport_dict)
            year_df = self.make_year_col_df(df_year,year)
            month_df = self.make_month_col_df(num_months)
            time_df = self.concat_df_cols(year_df,month_df)
            new_df = self.concat_df_cols(time_df,airport_df)
            yearly_df_list.append(new_df)
        return yearly_df_list

    def concat_df_cols(self,df1,df2):
        concatinated_df = pd.concat([df1,df2],axis = 1)
        return concatinated_df

    def concat_df_rows(self,df1,df2):
        concatinated_df = pd.concat([df1,df2],axis = 0)
        return concatinated_df

    def remove_na(self,df_list):
        clean_df_list = []
        for df in df_list:
            df_clean = df.dropna()
            clean_df_list.append(df_clean)
        return clean_df_list

    def final_concat(self,clean_df_list):
        all_years_data = pd.concat(clean_df_list)
        look_up = { 1.0: 'Jan', 2.0: 'Feb', 3.0: 'Mar', 4.0: 'Apr', 5.0:
                   'May', 6.0: 'Jun', 7.0: 'Jul', 8.0: 'Aug', 9.0: 'Sep', 10.0: 'Oct',
                   11.0: 'Nov', 12.0: 'Dec'}

        all_years_data['Month'] = all_years_data['Month'].apply(lambda x: look_up[x])
        return all_years_data
