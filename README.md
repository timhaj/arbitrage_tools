# arbitrage_tools
A collection of tools used for arbitrage betting,...

- arbitrage_calc.xlsm -> template Excel file for arbitrage betting
- arbitrage_calculator.py -> Python app with GUI for arbitrage betting

## How to make arbitrage_calculator.py a .exe:
1. Run `requirements.txt` after activating your Python environment. Requires Python >= 3.8
2. In terminal, go to `cd path\to\your\script`
3. Create an executable using: `pyinstaller --onefile --windowed arbitrage_calculator.py`
4. After the build finishes, you can find your executable in the `dist` folder. 
5. You can delete the `build` folder and the `.spec` file for cleanup. 