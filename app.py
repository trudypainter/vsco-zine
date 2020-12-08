from flask import Flask, render_template, request, jsonify
import vsco as vsco_file
import datetime, time, calendar

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('form.html')

@app.route('/zine', methods = ["GET", "POST"])
def zine():

    # GET ZINE VARIABLES FROM FORM POST
    username = request.form['username']
    duration = request.form.get('daterange')
    start = duration[:10]
    end = duration[13:]
    end = request.form.get('end')
    captions = bool(request.form.get('captions', False))

    # CREATE VSCO OBJECT
    vsco = vsco_file.VSCO(username)

    # PARSE 
    # list of tuples to be passed to render template

    # START UNIXTIME
    if not start or len(start) < 5:
        start_datetime = 0
        start_unixtime = 0 
    else:
        start_datetime = datetime.datetime.strptime(start, '%m/%d/%Y')
        start_unixtime = int(time.mktime(start_datetime.timetuple()))*1000

    # END UNIXTIME
    if not end or len(end) < 5:
        end_datetime = datetime.datetime.today()
    else:
        end_datetime = datetime.datetime.strptime(end, '%m/%d/%Y')
    end_unixtime = int(time.mktime(end_datetime.timetuple()))*1000

    # [(img_link, caption)]
    img_list = []
    for img in vsco:
        uploaded_at = int(img['upload_date'])

        if uploaded_at > start_unixtime and uploaded_at < end_unixtime:
            if isinstance(start_datetime, int):
                start_datetime = datetime.datetime.utcfromtimestamp(start_datetime)

            #CHECK FOR CAPTIONS
            if captions:
                img_list.append((img['responsive_url'], img['description']))
            else:
                img_list.append((img['responsive_url'], ""))

        # BREAK OUT FOR INVALID DATES
        elif uploaded_at < start_unixtime:
            break
    
    img_list = img_list[::-1]
    return render_template('zine.html', img_list = img_list, \
                                start = start_datetime.strftime('%B %d, %Y'), end = end_datetime.strftime('%B %d, %Y'),
                                username = username)

if __name__ == '__main__':
    app.run(debug=True)