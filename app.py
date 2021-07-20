import pandas as pd
import folium
from flask import Flask,render_template, request
import tweepy
def find(n=10):
    cov_data=pd.read_csv("coviddata.csv")
    temp = cov_data.groupby('Country').sum()[['Confirmed', 'Deaths', 'Recovered', 'Active']]
    data = temp.nlargest(n,'Confirmed')[['Confirmed']]
    return data

data=find()
pairs=[(country,confirmed) for country,confirmed in zip(data.index,data['Confirmed'])]
cov_data = pd.read_csv("coviddata.csv")
cov_data=cov_data[['Lat','Long','Confirmed']]
cov_data=cov_data.dropna()
m=folium.Map(location=[20,78],tiles='Stamen Terrain',zoom_start=3)

def circle_maker(x):
    folium.Circle(location=[x[0],x[1]],radius=float(x[2]),color="red",popup='confirmed cases:{}'.format(x[2])).add_to(m)

cov_data.apply(lambda x:circle_maker(x),axis=1)
html_map=m._repr_html_()

app=Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html",table=data, cmap=html_map,pairs=pairs)

@app.route('/tweet',methods=['GET'])
def tweet():
    auth = tweepy.OAuthHandler("qzZhq8Zml22gD91APqeekciNK", "MacfJtwBkHbwd99hAJ65lDN6FB6GaDCLk6b91x1F0GSZDG83PR")
    auth.set_access_token("1267426961694945288-8MRBc5pYifWZilRkX3vHzkM3ZX7WSL", "HBxtEcmijdFRnBEy47QmIHTRbkFbjl13c9SNMFWE6M3iq")
    api = tweepy.API(auth)
    search = request.args.get('handle')
    u_tweets = api.user_timeline(search)
    return render_template('tweet.html', tweets=u_tweets)


if __name__=="__main__":
    app.run(debug=True)