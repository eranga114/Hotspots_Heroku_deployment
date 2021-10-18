import uvicorn
from fastapi import FastAPI, Request
from pydantic import BaseModel
import pickle

with open( 'rfc_model_pickle', 'rb' ) as file:
    rf_pickle = pickle.load( file )

app = FastAPI()



class Item( BaseModel ):
    startPosition: int
    mut_count: int
    total_mut_count: int


@app.get( '/' )
def home():
    return {'message': 'Welcome to Hotspots analyzer'}


@app.post( '/hotspots' )
def hotspots_pred(data: Item):
    data = data.dict()
    startPosition = data['startPosition']
    mut_count = data['mut_count']
    total_mut_count = data['total_mut_count']

    prediction = rf_pickle.predict( [[startPosition, mut_count, total_mut_count]] )
    if prediction == 1:
        hotspot = "It's a cancer hotspot"
    else:
        hotspot = "It's not a cancer hotspot"

    return {
        "Prediction":int(prediction),
        "Cancer Hotspot Prediction": hotspot
    }


if __name__ == "__main__":
    uvicorn.run( app, host='localhost', port=8888 )
