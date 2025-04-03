# Wine Correlation Tool


A Python-based GUI application built with Tkinter to analyze correlations between 
numeric columns in a wine dataset stored in MySQL. This tool fetches data, computes 
correlations, and visualizes results with Matplotlib scatter plots.

## Features
- Connects to a MySQL database to retrieve wine data
- Allows users to select two columns via dropdown menus
- Computes Pearson correlation between selected columns
- Displays results with an interactive scatter plot
- Includes error handling for string data and database issues
- Customizable background image in the GUI

## Tech Stack
- **Python**: Core programming language
- **Tkinter**: GUI framework
- **MySQL Connector**: Database connectivity
- **Pandas**: Data manipulation
- **Matplotlib**: Data visualization
- **Pillow**: Image handling

## Installation
1. Clone the repository:
           git clone https://github.com/[YourUsername]/WineCorrelationTool.git
2. Install dependencies:
           pip install -r requirements.txt
3. Set up MySQL:
- Create a database named `python_wine`
- Create a table `wine_data` with numeric columns (e.g., `alcohol`, `pH`)
- Update the connection details in `main.py` (host, user, password)
4. Add a background image (e.g., `assets/background.jpg`)
5. Run the application:
           python main.py

## Usage
- Launch the app and select two columns from the dropdowns.
- Click "Compute Correlation" to see the result and scatter plot.
- Errors are displayed if non-numeric data is selected.

## Screenshot
- backgroung.jpg

## Skills Demonstrated
- GUI development with Tkinter
- Database integration with MySQL
- Data analysis with Pandas
- Visualization with Matplotlib
- Error handling and user experience design

## Future Improvements
- Add support for multiple database types (e.g., SQLite)
- Implement data filtering options
- Enhance UI with themes or custom widgets

## Author
[Sravani Peddi]  
[peddisravani087@gmail.com]  

