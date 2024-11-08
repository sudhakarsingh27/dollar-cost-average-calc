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

## Opinion about the cursor IDE AI features
+ Great for prototyping and quick development
+ Especially when multiple code languages and stacks are involved. 
+ Can edit and/or refactor multiple files based on a single prompt

- Editing markdown files is a pain, the mark down code is fragmented and hard to simply "Apply" unlike other languages.
- The generation in the chat can take a long time for a big change, there should be an option to toggle it and make the changes directly in the editor.

### Specific to this project
1. Refactoring
    - Simple to refactor an html file into a js file for the scripting part and keep the rendering part in the html file.
    - Also the AI was able to update the `main.py` file to account for the new scripting file added.

2. Adding documentation
    - Although the documentation was added automatically, it also did some refactoring of the code and moved a function from within another function to outside and failed to populated the important sections of that function. This is a big issue. 
      - Seems like there should also be a continuous testing of the code to make sure the current changes are caught.

3. Adding tests
    - The generated unit tests are good but if something is wrong with the corresponding API usage, you need to manually fix it. I had to use python pdb to figure out that with an invalid ticker symbol, the error was not being thrown and that's because the `yfinance` library still returns a dictionary even with an invalid ticker symbol.
    - Writing tests to continuously check the API usage is very important. Found a calculation bug in the `main.py` file. But when asked to "double check" the calculation, the AI generated code corrected the bug.
