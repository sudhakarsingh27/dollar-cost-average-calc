# Dollar Cost Averaging (DCA) Calculator

A web application that helps users understand and compare different Dollar Cost Averaging investment strategies using historical stock data.

## Features

- Calculate DCA returns for stocks and ETFs
- Compare daily, weekly, and monthly investment strategies 
- Auto-complete stock ticker suggestions
- Historical data visualization with interactive charts
- Customizable investment amount and time period
- Support for major US stocks and ETFs
- Clean and intuitive user interface

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Web browser (Chrome, Firefox, Safari, or Edge)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd dca-calculator
```

2. Create and activate a virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install required packages:
```bash
pip install fastapi uvicorn yfinance jinja2 python-multipart
```

## Project Structure
```
dca-calculator/
├── main.py                 # FastAPI application and backend logic
├── templates/             
│   ├── index.html         # Landing page with DCA information
│   └── dca.html           # Calculator interface
└── README.md              # Project documentation
```

## Running the Application

1. Start the FastAPI server:
```bash
uvicorn main:app --reload
```

2. Open your web browser and navigate to:
```
http://localhost:8000
```

## How to Use

1. Visit the homepage to learn about Dollar Cost Averaging
2. Click "Try DCA Calculator" to access the calculator
3. Enter your investment details:
   - Stock ticker symbol (e.g., AAPL, MSFT)
   - Investment amount per period
   - Investment frequency (daily, weekly, or monthly)
   - Start and end dates
4. Click "Calculate Returns" to see the results
5. Review the comparison of different investment frequencies

## API Endpoints

- `GET /`: Homepage with DCA information
- `GET /calculator`: DCA calculator page
- `POST /api/submit-dates`: Calculate investment returns

## Implementation Details

The calculator:
- Uses real market data from Yahoo Finance
- Calculates returns based on actual trading days
- Adjusts for market holidays and weekends
- Provides comparable results across different investment frequencies
- Shows total investment amount and profit/loss for each strategy

## Development

This project was developed entirely using [Cursor](https://cursor.sh/), an AI-first IDE that enhances coding productivity through intelligent code completion and integrated AI assistance.

## Important Notes

- This tool is for educational purposes only
- Historical data is provided by Yahoo Finance API
- Calculations assume:
  - No transaction fees
  - Perfect execution of trades
  - Approximately 21 trading days per month
- Always conduct your own research before making investment decisions

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Cursor IDE](https://cursor.sh/) for development environment
- Yahoo Finance for market data
- FastAPI framework and community
- All contributors to this project

---

<p align="center">
Developed with Cursor IDE
</p>

