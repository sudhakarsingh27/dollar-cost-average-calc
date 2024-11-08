import yfinance as yf
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Set up Jinja2Templates with the directory where your templates are stored
templates = Jinja2Templates(directory="templates")

# Add this after creating the FastAPI app
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/calculator", response_class=HTMLResponse)
async def calculator(request: Request):
    return templates.TemplateResponse("dca.html", {"request": request})

@app.post("/api/submit-dates")
async def submit_dates(request: Request):
    data = await request.json()
    start_date = data['start_date']
    end_date = data['end_date']
    symbol = data['ticker']
    amount = data['amount']
    frequency = data['frequency']
    
    try:
        # Create ticker object
        ticker = yf.Ticker(symbol)
        
        # Convert string dates to datetime
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d") if end_date else datetime.now()
        
        # Get historical data
        hist = ticker.history(
            start=start,
            end=end,
            interval="1d"
        )
        
        # Convert the data to dict format
        hist_dict = hist.reset_index().to_dict('records')
        def process_investment_data(hist_data, investment_amount, frequency):
            results = {
                'daily': {
                    'profit_loss': 0,
                    'total_invested': 0
                },
                'weekly': {
                    'profit_loss': 0,
                    'total_invested': 0
                },
                'monthly': {
                    'profit_loss': 0,
                    'total_invested': 0
                }
            }
            
            if not hist_data:
                return results
                
            # Sort data by date to ensure chronological order
            hist_data = sorted(hist_data, key=lambda x: x['Date'])
            
            # Adjust investment amount based on frequency to keep total invested amount comparable
            trading_days_per_month = 21  # approximate number of trading days in a month
            daily_amount = (investment_amount / trading_days_per_month if frequency == 'monthly' 
                           else investment_amount / 5 if frequency == 'weekly' 
                           else investment_amount)
            weekly_amount = (investment_amount * (trading_days_per_month/5) if frequency == 'monthly'
                            else investment_amount * 5 if frequency == 'daily'
                            else investment_amount)
            monthly_amount = (investment_amount * trading_days_per_month if frequency == 'daily'
                             else investment_amount * (trading_days_per_month/5) if frequency == 'weekly'
                             else investment_amount)
            
            # Calculate daily investment results
            daily_shares = 0
            for day in hist_data:
                shares_bought = daily_amount / day['Open']
                daily_shares += shares_bought
            
            final_value = daily_shares * hist_data[-1]['Close']
            total_invested_daily = daily_amount * len(hist_data)
            results['daily']['profit_loss'] = final_value - total_invested_daily
            results['daily']['total_invested'] = total_invested_daily
            
            # Calculate weekly investment results
            weekly_shares = 0
            num_weeks = 0
            for i, day in enumerate(hist_data):
                if i % 5 == 0:  # First trading day of each week
                    shares_bought = weekly_amount / day['Open']
                    weekly_shares += shares_bought
                    num_weeks += 1
            
            final_value = weekly_shares * hist_data[-1]['Close']
            total_invested_weekly = weekly_amount * num_weeks
            results['weekly']['profit_loss'] = final_value - total_invested_weekly
            results['weekly']['total_invested'] = total_invested_weekly
            
            # Calculate monthly investment results
            monthly_shares = 0
            num_months = 0
            current_month = None
            
            for day in hist_data:
                day_date = day['Date']
                if isinstance(day_date, str):
                    day_date = datetime.strptime(day_date, '%Y-%m-%d')
                    
                # Invest on first trading day of each month
                if current_month != day_date.month:
                    shares_bought = monthly_amount / day['Open']
                    monthly_shares += shares_bought
                    num_months += 1
                    current_month = day_date.month
            
            final_value = monthly_shares * hist_data[-1]['Close']
            total_invested_monthly = monthly_amount * num_months
            results['monthly']['profit_loss'] = final_value - total_invested_monthly
            results['monthly']['total_invested'] = total_invested_monthly
            
            return results
            
        # Call the processing function
        investment_results = process_investment_data(hist_dict, float(amount), frequency)
        return {
            "symbol": symbol,
            "amount": amount,   
            "frequency": frequency,
            "start_date": start_date,
            "end_date": end_date,
            "results": investment_results
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
