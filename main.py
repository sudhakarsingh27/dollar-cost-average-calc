import yfinance as yf
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from decimal import Decimal
import logging
from fastapi import FastAPI, HTTPException, Request

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Set up Jinja2Templates with the directory where your templates are stored
templates = Jinja2Templates(directory="templates")

# Add this after creating the FastAPI app
app.mount("/static", StaticFiles(directory="static"), name="static")

async def validate_ticker(symbol: str) -> Optional[yf.Ticker]:
    """Validates ticker symbol and returns ticker object if valid."""
    try:
        if not symbol or not isinstance(symbol, str):
            raise ValueError("Ticker symbol must be a non-empty string")
            
        symbol = symbol.strip().upper()
        
        if not symbol.isalnum() or len(symbol) > 5:
            raise ValueError("Ticker must be 1-5 alphanumeric characters")

        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="5d")
        info = ticker.info
    
        # Check if 'regularMarketPrice' exists in the info dictionary
        # if 'regularMarketPrice' not in info or info['regularMarketPrice'] is None:
        if hist.empty:
            raise HTTPException(status_code=400, detail=f"Invalid ticker symbol: {symbol}")
            
        if info['symbol'].upper() != symbol:
            raise ValueError(f"Symbol mismatch: requested {symbol}, got {info['symbol']}")


        logger.info(f"Validated ticker: {symbol} ({info.get('shortName')})")
        return ticker

    except Exception as e:
        logger.error(f"Ticker validation failed: {str(e)}")
        return None

def validate_amount(amount: Any) -> float:
    """Validates investment amount."""
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > 1000000:  # Example maximum limit
            raise ValueError("Amount exceeds maximum limit of $1,000,000")
        return amount
    except (TypeError, ValueError) as e:
        raise ValueError(f"Invalid amount: {str(e)}")

def validate_frequency(frequency: str) -> str:
    """Validates investment frequency."""
    valid_frequencies = ['daily', 'weekly', 'monthly']
    frequency = frequency.lower().strip()
    if frequency not in valid_frequencies:
        raise ValueError(f"Invalid frequency. Must be one of: {', '.join(valid_frequencies)}")
    return frequency

def validate_dates(start_date: str, end_date: str) -> tuple[datetime, datetime]:
    """Validates date range."""
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        # Check date range validity
        if start > end:
            raise ValueError("Start date cannot be after end date")
            
        today = datetime.now()
        if end > today:
            raise ValueError("End date cannot be in the future")
            
        max_duration = timedelta(days=365 * 10)  # 10 years
        if end - start > max_duration:
            raise ValueError("Date range cannot exceed 10 years")
            
        min_duration = timedelta(days=7)  # 1 week
        if end - start < min_duration:
            raise ValueError("Date range must be at least 1 week")
            
        return start, end
        
    except ValueError as e:
        if "does not match format" in str(e):
            raise ValueError("Invalid date format. Use YYYY-MM-DD")
        raise

async def validate_request_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validates all request data."""
    try:
        # Check for required fields
        required_fields = ['ticker', 'amount', 'frequency', 'start_date', 'end_date']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        # Validate each field
        ticker = await validate_ticker(data['ticker'])
        if not ticker:
            raise ValueError(f"Invalid ticker symbol: {data['ticker']}")

        amount = validate_amount(data['amount'])
        frequency = validate_frequency(data['frequency'])
        start, end = validate_dates(data['start_date'], data['end_date'])

        # return {
        #     'ticker': ticker,
        #     'amount': amount,
        #     'frequency': frequency,
        #     'start_date': start,
        #     'end_date': end
        # }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/calculator", response_class=HTMLResponse)
async def calculator(request: Request):
    return templates.TemplateResponse("dca.html", {"request": request})

@app.post("/api/submit-dates")
async def submit_dates(request: Request):
    try:
        # Get and validate request data
        data = await request.json()
        logger.info(f"Received request: {data}")
        
        # Validate all inputs
        await validate_request_data(data)

        start_date = data['start_date']
        end_date = data['end_date']
        symbol = data['ticker']
        amount = data['amount']
        frequency = data['frequency']
        # Create ticker object
        # Validate ticker symbol
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
            
            # For daily investments:
            # - If monthly frequency specified, divide monthly amount by trading days
            # - If weekly frequency specified, divide weekly amount by 5 trading days
            # - Otherwise use amount as is for daily
            daily_amount = (investment_amount / trading_days_per_month if frequency == 'monthly'
                          else investment_amount / 5 if frequency == 'weekly'
                          else investment_amount)
            
            # For weekly investments:
            # - If monthly frequency specified, divide monthly amount by ~4 weeks
            # - If daily frequency specified, multiply daily by 5 days
            # - Otherwise use amount as is for weekly
            weekly_amount = (investment_amount / 4 if frequency == 'monthly'
                           else investment_amount * 5 if frequency == 'daily'
                           else investment_amount)
            
            # For monthly investments:
            # - If daily frequency specified, multiply daily by trading days
            # - If weekly frequency specified, multiply weekly by ~4 weeks
            # - Otherwise use amount as is for monthly
            monthly_amount = (investment_amount * trading_days_per_month if frequency == 'daily'
                            else investment_amount * 4 if frequency == 'weekly'
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
