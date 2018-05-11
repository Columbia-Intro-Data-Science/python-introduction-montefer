# To run: FLASK_APP=fernando.py flask run
# Check out localhost:5000

from flask import Flask, render_template, request
import csv

app = Flask(__name__)


def get_stats(borough, min_satisfaction, min_reviews, beds, price, price_range):


    arr_mean = []
    arr_std = []
    #file_name_mean = 'mean_'+borough+str(min_satisfaction)+str(min_reviews)+str(beds)+str(price-price_range)+'-'+str(price+price_range)+'.csv'
    #file_name_std = 'std_'+borough+str(min_satisfaction)+str(min_reviews)+str(beds)+str(price-price_range)+'-'+str(price+price_range)+'.csv'

    file_name_mean='ezpez1.csv'
    file_name_std='ezpez2.csv'

    with open(file_name_mean, 'rt') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            arr_mean.append(row[1])

    with open(file_name_std, 'rt') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            arr_std.append(row[1])


    #reviews
    #overall_satisfaction
    #accommodates
    #bedrooms
    #price
    review_stat = (int(min_reviews)-float(arr_mean[0]))/float(arr_std[0])
    satisfaction_stat = (int(min_satisfaction)-float(arr_mean[1]))/float(arr_std[1])
    bedrooms_stat = (int(beds)-float(arr_mean[3]))/float(arr_std[3])
    price_stat = (int(price)-float(arr_mean[4]))/float(arr_std[4])

    if review_stat<=0:
        review_output = "The reviews for your listing are "+str(review_stat)+" standard deviations below the mean given its stats"
    if review_stat>0:
        review_output = "The reviews for your listing are "+str(review_stat)+" standard deviations above the mean given its stats"

    if satisfaction_stat<=0:
        satisfaction_output = "The overall satisfaction for your listing is "+str(satisfaction_stat)+" standard deviations below the mean given its stats"
    if satisfaction_stat>0:
        satisfaction_output = "The overall_satisfaction for your listing is "+str(satisfaction_stat)+" standard deviations above the mean given its stats"

    if bedrooms_stat<=0:
        bedrooms_output = "The number of bedrooms your listing has is below average given its other stats!"
    if bedrooms_stat>0:
        bedrooms_output = "The number of bedrooms your listing has is above average given its other stats"

    if price_stat<=0:
        price_output = "The price for your listing is "+str(price_stat)+" standard deviations below the mean. Have you considered increasing the price?"
    if price_stat>0:
        price_output = "The price for your listing is "+str(price_stat)+" standard deviations above the mean. Your place might be too expensive for some people."








    return review_output, satisfaction_output, bedrooms_output, price_output



@app.route("/")
def hello():
    return render_template("index.html")

@app.route('/output2')
def create():
    bedrooms = request.args.get('bedrooms')
    satisfaction = request.args.get('satisfaction')
    price = request.args.get('price')
    location = request.args.get('location')
    reviews = request.args.get('reviews')

    price_low = int(price.split('-')[0])
    price_high = int(price.split('-')[1])
    price = (price_high+price_low)/2
    price_range = price_high-price_low

    #review_output, satisfaction_output, bedrooms_output, price_output = get_stats('Manhattan',3,1,3,300,50)#get_stats(location,int(satisfaction),int(reviews),int(bedrooms),int(price),int(price_range))

    file_name = location+str(satisfaction)+str(reviews)+str(bedrooms)+str(price-price_range)+'-'+str(price+price_range)


    context = {
        'bedrooms': bedrooms,
        'satisfaction': satisfaction,
        'price': price,
        'location': location,
        'price_range':price_range,
        'reviews': reviews,
        'file': file_name
        #'review_output': review_output,
        #'satisfaction_output': satisfaction_output,
        #'bedrooms_output': bedrooms_output,
        #'price_output': price_output
    }
    return render_template("output2.html", **context)