# %%% Getting Prices




df = pd.read_excel('C:\\Users\\hasanallahyarov\\Desktop\\result.xlsx')



# Convert the 'Filed_At' column to datetime format
df['Filed_At'] = pd.to_datetime(df['Filed_At'], format='%Y%m%d')

# Convert the datetime format back to the desired format "YYYY-MM-DD"
df['Filed_At'] = df['Filed_At'].dt.strftime('%Y-%m-%d')
df['Price'] = None  
df['Price+1'] = None


for i in df.index:
    print(i)
    ticker=df['ticker'].iloc[i]
    
    if pd.notna(ticker):
        GetInformation = yahooFinance.Ticker(ticker)
    else:
        continue

    pd.set_option('display.max_rows', None)

    prices = GetInformation.history(period="max")
    
 
    
    prices.reset_index(inplace=True)
    
    prices['Date'] = pd.to_datetime(prices['Date'])
    
    prices['Date'] = prices['Date'].dt.strftime('%Y-%m-%d')
    
    desired_date = df['Filed_At'].iloc[i]
    
    
    result_df = prices[prices['Date'] == desired_date]
    
    if not result_df.empty:
        index_of_date = result_df.index[0]
    else:
        continue
    
    price_of_day = prices['Close'].iloc[index_of_date]
    
    price_of_next_day = prices['Close'].iloc[index_of_date+1]
    
    df.at[i, 'Price'] = price_of_day
    
    df.at[i, 'Price+1'] = price_of_next_day
    
df.to_excel('C:\\Users\\hasanallahyarov\\Desktop\\result_with_prices.xlsx', index=False)
    
    
    
# %%%
df = pd.read_excel('C:\\Users\\hasanallahyarov\\Desktop\\10q_ with_prices.xlsx')

df['Percentage_Diff'] = ((df['Price+1'] - df['Price']) / df['Price']) * 100

# Round the percentage difference to 2 decimal places
df['Percentage_Diff'] = df['Percentage_Diff'].round(2)

df.drop(['cik_str', 'FLS_pct', 'Score', 'Value', 'Date', 'title', 'Price', 'Price+1' ], axis=1, inplace=True)

df=df.dropna()
## Dataframe will containt only: Filed_Date, Document_type, Ticker, Num_Words, Percentage_Diff,

df = df[(df['num_words'] >= 1000) & (df['num_words'] <= 20000)]


import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score


# Convert the Filed_At column to the year
df['Filed_At'] = pd.to_datetime(df['Filed_At'])

# Create separate columns for each day using one-hot encoding
df = pd.get_dummies(df, columns=['Filed_At'], prefix='day', drop_first=False)

# Create dummy variables for ticker and document_type
df = pd.get_dummies(df, columns=['ticker', 'document_type'], drop_first=True)

# Split the data into training and testing sets
X = df.drop('Percentage_Diff', axis=1)
y = df['Percentage_Diff']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the linear regression model with fixed effects
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r_squared = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r_squared}")

# Inspect coefficients and intercept
coefficients = pd.Series(model.coef_, index=X.columns)
intercept = model.intercept_

print("Coefficients:")
print(coefficients)
print("Intercept:")
print(intercept)
