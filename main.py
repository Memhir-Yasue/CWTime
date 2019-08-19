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
    robo = Automater()
    df_files_list = robo.htm_to_df(files)
    clean_df_list = robo.pre_process_df(df_files_list)
    concatinated_df = robo.concatinate_df(clean_df_list)
    neo_conc_df = robo.add_columns(concatinated_df)
    summary_df = by_Year_Month.convert_to_by_yr_m(neo_conc_df)
    return summary_df.to_html()

    # data_xls = pd.read_csv(files[0])
    # return data_xls.to_html()


if __name__ == '__main__':
    app.run(debug=True)
