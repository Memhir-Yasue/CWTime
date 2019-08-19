from flask import Flask, make_response, request,render_template
import pandas as pd
from mainProcessor import Automater, by_Year_Month





app = Flask(__name__)

@app.route('/')
def form():
    return render_template('index.html')

@app.route('/process', methods = ['POST'])
def process_view():
    if not request.files:
        return "No file"
    files = request.files.getlist("data_files")
    # Data processing stage goes under here!

    # Entire concatinated data for all airport(s)
    robo = Automater()
    df_files_list = robo.htm_to_df(files)
    clean_df_list = robo.pre_process_df(df_files_list)
    concatinated_df = robo.concatinate_df(clean_df_list)
    neo_conc_df = robo.add_columns(concatinated_df)


    # By month summary
    B_M = by_Year_Month()
    summary_df = B_M.convert_to_by_yr_m(neo_conc_df)
    dirty_yearly_list = B_M.process_by_year(summary_df)
    clean_yearly_list = B_M.remove_na(dirty_yearly_list)
    final_df = B_M.final_concat(clean_yearly_list)
    return final_df.to_html()

    # return final_df.

    # data_xls = pd.read_csv(files[0])
    # return data_xls.to_html()


if __name__ == '__main__':
    app.run(debug=True)
