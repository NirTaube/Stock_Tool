from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
from statsmodels.tsa.arima.model import ARIMA
from sklearn.linear_model import Ridge
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
import numpy as np

app = FastAPI()

origins = [
    "http://10.0.0.95:8080", # Your front-end's origin
    # You can add additional origins here if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Stock Price Prediction Service, let's make some bread!"}

def fetch_stock_data(ticker_symbol: str):
    stock = yf.Ticker(ticker_symbol)
    data = stock.history(period="1d", interval="5m")
    return data

def predict_arima(data):
    y = data['Close'].values
    model = ARIMA(y, order=(5,1,0))
    model_fit = model.fit() # Removed disp=0
    prediction = model_fit.forecast()[0]
    return prediction

def predict_ridge(data):
    X = np.arange(len(data)).reshape(-1, 1)
    y = data['Close'].values
    model = Ridge()
    model.fit(X, y)
    future_time = np.array([[len(data)]]) # Predicting the next interval
    prediction = model.predict(future_time)
    return prediction[0]

def predict_gpr(data):
    X = np.arange(len(data)).reshape(-1, 1)
    y = data['Close'].values
    kernel = 1.0 * RBF() + C(1.0, (1e-3, 1e3))
    model = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10)
    model.fit(X, y)
    future_time = np.array([[len(data)]]) # Predicting the next interval
    prediction = model.predict(future_time)
    return prediction[0]

@app.get("/stock/{ticker}")
def get_stock_data(ticker: str):
    data = fetch_stock_data(ticker)
    red_prediction = predict_arima(data) # ARIMA
    blue_prediction = predict_ridge(data) # Ridge
    green_prediction = predict_gpr(data)  # GPR
    return {"data": data.to_dict(orient="records"), "red_prediction": red_prediction, "blue_prediction": blue_prediction, "green_prediction": green_prediction}
