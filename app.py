from datetime import timedelta
import datetime
from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

def get_data_from_db(day=None, open_fib_status=None, 
                     fib0618_status=None, open_equals=None, 
                     gap_range=None,n_fii=None,
                     b_fii=None,s_fii=None,fii_ilm=None,
                     fii_ism=None,
                     fii_index_longs_vs_shorts_percent=None,
                     fii_sl=None,fii_ss=None,
                     fii_stock_longs_vs_shorts_percent=None,
                     client_ilm=None,client_ism=None,
                     client_index_longs_vs_shorts_percent=None,
                     client_sl=None,client_ss=None,
                     client_stock_longs_vs_shorts_percent=None,
                     pro_ilm=None,pro_ism=None,
                     pro_index_longs_vs_shorts_percent=None,
                     pro_sl=None,pro_ss=None,
                     pro_stock_longs_vs_shorts_percent=None,dates_pk=None):

    try:
        conn = psycopg2.connect(
            dbname="NIFTY50",
            user="postgres",
            password="126128",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        query = """SELECT v.date, MAX(v.Open), MAX(v.High),
                   MAX(v.Low), MAX(v.Close), MAX(v.High_Low),
                   MAX(v.Gap_Up_or_Down), MAX(v.High_Open), 
                   MAX(v.Low_Open), MAX(v.Day), MAX(v.Fib0382), 
                   MAX(v.Fib0618),MAX(v.last7d),MAX(v.last15d),
                   MAX(v.last30d),MAX(v.open_fib0382_status),
                   MAX(v.open_fib0618_status),MAX(f.fib0382tohigh),
                   MAX(f.fib0382tolow),MAX(f.fib0618tohigh),
                   MAX(f.fib0618tolow),MAX(x.moon),MAX(x.high),
                   MAX(v.b_fii),MAX(v.s_fii),MAX(v.n_fii),
                   MAX(v.fii_ilm),MAX(v.fii_ism),
                   MAX(v.fii_index_longs_vs_shorts_percent),MAX(v.fii_sl),
                   MAX(v.fii_ss),MAX(v.fii_stock_longs_vs_shorts_percent),
                   MAX(v.client_ilm),MAX(v.client_ism),
                   MAX(v.client_index_longs_vs_shorts_percent),
                   MAX(v.client_sl),MAX(v.client_ss),
                   MAX(v.client_stock_longs_vs_shorts_percent),
                   MAX(v.pro_ilm),MAX(v.pro_ism),
                   MAX(v.pro_index_longs_vs_shorts_percent),
                   MAX(v.pro_sl),MAX(v.pro_ss),
                   MAX(v.pro_stock_longs_vs_shorts_percent),
                   MAX(v.price_above_c15),MAX(v.price_below_c15_low),MAX(v.next_trading_date)
                   FROM values AS v
                   LEFT JOIN vix AS x ON v.date = x.date
                   LEFT JOIN fibdata AS f ON v.date = f.date WHERE 1=1 """
        params = []

        if day:
            query += "AND EXTRACT(DOW FROM v.date) = %s "
            params.append(day)

        if open_fib_status:
            query += "AND v.open_fib0382_status = %s "
            params.append(open_fib_status)

        if fib0618_status:
            query += "AND v.open_fib0618_status = %s "
            params.append(fib0618_status)

        if open_equals == 'HIGH':
            query += "AND v.Open = v.High "

        if open_equals == 'LOW':
            query += "AND v.Open = v.Low "

        if gap_range:
            query += "AND v.Gap_Up_or_Down >= %s AND v.Gap_Up_or_Down <= %s "
            params.extend(gap_range)

        if n_fii:
            query += "AND v.n_fii >= %s AND v.n_fii <= %s "
            params.extend(n_fii)
        
        if b_fii:
            query += "AND v.b_fii >= %s AND v.b_fii <= %s "
            params.extend(b_fii)
        
        if s_fii:
            query += "AND v.s_fii >= %s AND v.s_fii <= %s "
            params.extend(s_fii)
        if fii_ilm:
            query += "AND v.fii_ilm >= %s AND v.fii_ilm <= %s "
            params.extend(fii_ilm)
        if fii_ism:
            query += "AND v.fii_ism >= %s AND v.fii_ism <= %s "
            params.extend(fii_ism)

        if fii_index_longs_vs_shorts_percent:
            query += "AND v.fii_index_longs_vs_shorts_percent >= %s AND v.fii_index_longs_vs_shorts_percent <= %s "
            params.extend(fii_index_longs_vs_shorts_percent)
        if fii_sl:
            query += "AND v.fii_sl >= %s AND v.fii_sl <= %s "
            params.extend(fii_sl)
        if fii_ss:
            query += "AND v.fii_ss >= %s AND v.fii_ss <= %s "
            params.extend(fii_ss)
        if fii_stock_longs_vs_shorts_percent:
            query += "AND v.fii_stock_longs_vs_shorts_percent >= %s AND v.fii_stock_longs_vs_shorts_percent <= %s "
            params.extend(fii_stock_longs_vs_shorts_percent)
        if client_ilm:
            query += "AND v.client_ilm >= %s AND v.client_ilm <= %s "
            params.extend(client_ilm)
        if client_ism:
            query += "AND v.client_ism >= %s AND v.client_ism <= %s "
            params.extend(client_ism)
        if client_index_longs_vs_shorts_percent:
            query += "AND v.client_index_longs_vs_shorts_percent >= %s AND v.client_index_longs_vs_shorts_percent <= %s "
            params.extend(client_index_longs_vs_shorts_percent)
        if client_sl:
            query += "AND v.client_sl >= %s AND v.client_sl <= %s "
            params.extend(client_sl)

        if client_ss:
            query += "AND v.client_ss >= %s AND v.client_ss <= %s "
            params.extend(client_ss)
        if client_stock_longs_vs_shorts_percent:
            query += "AND v.client_stock_longs_vs_shorts_percent >= %s AND v.client_stock_longs_vs_shorts_percent <= %s "
            params.extend(client_stock_longs_vs_shorts_percent)

        if pro_ilm:
            query += "AND v.pro_ilm >= %s AND v.pro_ilm <= %s "
            params.extend(pro_ilm)
        if pro_ism:
            query += "AND v.pro_ism >= %s AND v.pro_ism <= %s "
            params.extend(pro_ism)

        if pro_index_longs_vs_shorts_percent:
            query += "AND v.pro_index_longs_vs_shorts_percent >= %s AND v.pro_index_longs_vs_shorts_percent <= %s "
            params.extend(pro_index_longs_vs_shorts_percent)

        if pro_sl:
            query += "AND v.pro_sl >= %s AND v.pro_sl <= %s "
            params.extend(pro_sl)

        if pro_ss:
            query += "AND v.pro_ss >= %s AND v.pro_ss <= %s "
            params.extend(pro_ss)

        if pro_stock_longs_vs_shorts_percent:
            query += "AND v.pro_stock_longs_vs_shorts_percent >= %s AND v.pro_stock_longs_vs_shorts_percent <= %s "
            params.extend(pro_stock_longs_vs_shorts_percent)
        if dates_pk:
            date_placeholders = ', '.join(['%s' for _ in dates_pk])
            query += f"AND v.date IN ({date_placeholders}) "
            params.extend(dates_pk)

        query += "GROUP BY v.date ORDER BY v.date DESC;"

        cursor.execute(query, params)

        data = cursor.fetchall()
        return data
    except Exception as e:
        print("Error occurred in get_data_from_db: ", e)
        return None
    finally:
        if conn:
            conn.close()

def get_record_count_by_date():
    try:
        conn = psycopg2.connect(
            dbname="NIFTY50",
            user="postgres",
            password="126128",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        query = "SELECT date, COUNT(*) FROM values GROUP BY date ORDER BY date DESC;"
        cursor.execute(query)
        
        data = cursor.fetchall()
        return data
    except Exception as e:
        print("Error occurred in get_record_count_by_date: ", e)
        return None
    finally:
        if conn:
            conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    
    form_data = {
        'day': None,
        'open_fib_status': None,
        'fib0618_status': None,
        'open_equals': None,
        'gap_start': "-300",
        'gap_end': "300",
        'nse_start': "-300",
        'nse_end': "300",
        'avg_fii_buy_start': "0",
        'avg_fii_buy_end': "300",
        'avg_fii_sell_start': "0",
        'avg_fii_sell_end': "300",
        'fii_ilm_start': "0",
        'fii_ilm_end': "300",
        'fii_ism_start': "0",
        'fii_ism_end': "300",
        'fii_index_longs_vs_shorts_percent_start': "0",
        'fii_index_longs_vs_shorts_percent_end': "300",
        'fii_sl_start': "0",
        'fii_sl_end': "300",
        'fii_ss_start':"0",
        'fii_ss_end': "300", 
        'fii_stock_longs_vs_shorts_percent_start':"0",
        'fii_stock_longs_vs_shorts_percent_end': "300" ,
        'client_ilm_start': "0",
        'client_ilm_end': "300",
        'client_ism_start': "0",
        'client_ism_end': "300",
        'client_index_longs_vs_shorts_percent_start': "0",
        'client_index_longs_vs_shorts_percent_end': "300",
        'client_sl_start': "0",
        'client_sl_end': "300",
        'client_ss_start': "0",
        'client_ss_end': "300",
        'client_stock_longs_vs_shorts_percent_start': "0",
        'client_stock_longs_vs_shorts_percent_end': "300",
        'pro_ilm_start': "0",
        'pro_ilm_end': "300",
        'pro_ism_start': "0",
        'pro_ism_end': "300",
        'pro_index_longs_vs_shorts_percent_start': "0",
        'pro_index_longs_vs_shorts_percent_end': "300",
        'pro_sl_start': "0",
        'pro_sl_end': "300",
        'pro_ss_start': "0",
        'pro_ss_end': "300",
        'pro_stock_longs_vs_shorts_percent_start': "0",
        'pro_stock_longs_vs_shorts_percent_end': "300",
        'dates_pk': None,
    }
    

    if request.method == 'POST':
        if 'reset' in request.form:
                form_data = {
        'day': None,
        'open_fib_status': None,
        'fib0618_status': None,
        'open_equals': None,
        'gap_start': "-300",
        'gap_end': "300",
        'nse_start': "-300",
        'nse_end': "300",
        'avg_fii_buy_start': "0",
        'avg_fii_buy_end': "300",
        'avg_fii_sell_start': "0",
        'avg_fii_sell_end': "300",
        'fii_ilm_start': "0",
        'fii_ilm_end': "300",
        'fii_ism_start': "0",
        'fii_ism_end': "300",
        'fii_index_longs_vs_shorts_percent_start': "0",
        'fii_index_longs_vs_shorts_percent_end': "300",
        'fii_sl_start': "0",
        'fii_sl_end': "300",
        'fii_ss_start':"0",
        'fii_ss_end': "300", 
        'fii_stock_longs_vs_shorts_percent_start':"0",
        'fii_stock_longs_vs_shorts_percent_end': "300" ,
        'client_ilm_start': "0",
        'client_ilm_end': "300",
        'client_ism_start': "0",
        'client_ism_end': "300",
        'client_index_longs_vs_shorts_percent_start': "0",
        'client_index_longs_vs_shorts_percent_end': "300",
        'client_sl_start': "0",
        'client_sl_end': "300",
        'client_ss_start': "0",
        'client_ss_end': "300",
        'client_stock_longs_vs_shorts_percent_start': "0",
        'client_stock_longs_vs_shorts_percent_end': "300",
        'pro_ilm_start': "0",
        'pro_ilm_end': "300",
        'pro_ism_start': "0",
        'pro_ism_end': "300",
        'pro_index_longs_vs_shorts_percent_start': "0",
        'pro_index_longs_vs_shorts_percent_end': "300",
        'pro_sl_start': "0",
        'pro_sl_end': "300",
        'pro_ss_start': "0",
        'pro_ss_end': "300",
        'pro_stock_longs_vs_shorts_percent_start': "0",
        'pro_stock_longs_vs_shorts_percent_end': "300",
        'dates_pk': None,
    }
        else:
            # Normal form submission
            for key in form_data.keys():
                form_data[key] = request.form.get(key, "")
    if form_data['dates_pk'] and form_data['dates_pk'].strip() != '':
        try:
            form_data['dates_pk'] = [datetime.datetime.strptime(date.strip(), '%Y-%m-%d') for date in form_data['dates_pk'].split(',')]
            # Convert datetime objects to strings
            form_data['dates_pk'] = [date.strftime('%Y-%m-%d') for date in form_data['dates_pk']]
        except ValueError as e:
            print(f"Invalid date format: {e}")
            form_data['dates_pk'] = None  # Set to None if invalid
    else:
        form_data['dates_pk'] = ""  # Set to None if empty or not provided

    gap_range = (form_data['gap_start'], form_data['gap_end'])
    fii_ilm = (form_data['fii_ilm_start'], form_data['fii_ilm_end'])
    client_ilm = (form_data['client_ilm_start'], form_data['client_ilm_end'])
    client_ism = (form_data['client_ism_start'], form_data['client_ism_end'])
    client_index_longs_vs_shorts_percent = (form_data['client_index_longs_vs_shorts_percent_start'], form_data['client_index_longs_vs_shorts_percent_end'])
    fii_sl = (form_data['fii_sl_start'], form_data['fii_sl_end'])
    client_sl = (form_data['client_sl_start'], form_data['client_sl_end'])
    client_ss = (form_data['client_ss_start'], form_data['client_ss_end'])
    client_stock_longs_vs_shorts_percent = (form_data['client_stock_longs_vs_shorts_percent_start'], form_data['client_stock_longs_vs_shorts_percent_end'])
    fii_ss = (form_data['fii_ss_start'], form_data['fii_ss_end'])
    fii_ism = (form_data['fii_ism_start'], form_data['fii_ism_end'])
    fii_index_longs_vs_shorts_percent = (form_data['fii_index_longs_vs_shorts_percent_start'], form_data['fii_index_longs_vs_shorts_percent_end'])
    n_fii = (form_data['nse_start'], form_data['nse_end'])
    b_fii = (form_data['avg_fii_buy_start'], form_data['avg_fii_buy_end'])
    s_fii = (form_data['avg_fii_sell_start'], form_data['avg_fii_sell_end'])
    fii_stock_longs_vs_shorts_percent = (form_data['fii_stock_longs_vs_shorts_percent_start'], form_data['fii_stock_longs_vs_shorts_percent_end'])
    pro_ilm = (form_data['pro_ilm_start'], form_data['pro_ilm_end'])
    pro_ism = (form_data['pro_ism_start'], form_data['pro_ism_end'])
    pro_index_longs_vs_shorts_percent = (form_data['pro_index_longs_vs_shorts_percent_start'], form_data['pro_index_longs_vs_shorts_percent_end'])
    pro_sl = (form_data['pro_sl_start'], form_data['pro_sl_end'])
    pro_ss = (form_data['pro_ss_start'], form_data['pro_ss_end'])
    pro_stock_longs_vs_shorts_percent = (form_data['pro_stock_longs_vs_shorts_percent_start'], form_data['pro_stock_longs_vs_shorts_percent_end'])
    
    data = get_data_from_db(form_data['day'], form_data['open_fib_status'], 
                            form_data['fib0618_status'], form_data['open_equals'], 
                            gap_range,n_fii,b_fii,s_fii,fii_ilm,fii_ism,
                            fii_index_longs_vs_shorts_percent,
                            fii_sl,fii_ss,fii_stock_longs_vs_shorts_percent,
                            client_ilm,client_ism,client_index_longs_vs_shorts_percent,
                            client_sl,client_ss,
                            client_stock_longs_vs_shorts_percent,pro_ilm,pro_ism,
                            pro_index_longs_vs_shorts_percent,pro_sl,pro_ss,
                            pro_stock_longs_vs_shorts_percent,form_data['dates_pk'])
    
    record_count_by_date = get_record_count_by_date()
    # Assuming that 'gap_up_or_down' is the 6th element in each tuple (index 6)


    dates = [record[46]  for record in data if record[46] is not None]

    gap_up_or_down_values = [record[6] for record in data if record[6] is not None]
    if gap_up_or_down_values:
        average_gap_up_or_down = sum(gap_up_or_down_values) / len(gap_up_or_down_values)
        average_gap_up_or_down = round(average_gap_up_or_down)
    else:
        average_gap_up_or_down = None

   # Assuming that 'high_low' is the 5th element in each tuple (index 5)
    high_low_values = [record[5] for record in data if record[5] is not None]
    if high_low_values:
        average_high_low = sum(high_low_values) / len(high_low_values)
        average_high_low = round(average_high_low)
    else:
        average_high_low = None
      # Assuming that 'high_open' is the 5th element in each tuple (index 5)
    high_open_values = [record[7] for record in data if record[7] is not None]
    if high_open_values:
        average_high_open = sum(high_open_values) / len(high_open_values)
        average_high_open = round(average_high_open)
    else:
        average_high_open = None
           # Assuming that 'low_open' is the 8th element in each tuple (index 5)
    low_open_values = [record[8] for record in data if record[8] is not None]
    if low_open_values:
        average_low_open = sum(low_open_values) / len(low_open_values)
        average_low_open = round(average_low_open)
    else:
        average_low_open = None


    strength_values = [record[9] for record in data if record[9] is not None]
    if strength_values:
        strength_values  = average_high_open / average_low_open *100
        strength_values  = round(strength_values)
    else:
        strength_values  = None
   
    return render_template('index.html', data=data, form_data=form_data, record_count_by_date=record_count_by_date, average_gap_up_or_down=average_gap_up_or_down, average_high_low=average_high_low,average_high_open=average_high_open,average_low_open=average_low_open,dates=dates,strength_values=strength_values,dates_pk=form_data['dates_pk'])

if __name__ == '__main__':
    app.run(debug=True)
    #cd C:\Users\prave\OneDrive\Pictures\Screenshots\
    #python -m http.server 5000