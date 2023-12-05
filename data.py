import csv
import time
import requests
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
#from dune_client.types import QueryParameter
#from dune_client.client import DuneClient
#from dune_client.query import QueryBase


class Data:

    def __init__(self):
        self.file_name = 'data.py'
        self.DUNE_API_KEY = "rbzUnMqFb3ZtFDTJ7MLVXHsYnTavj1dY" # Dune Analytics API Key
        self.AMBERDATA_API_KEY = "UAK0c028c3100dd891e636c471b40b71c09" # AmberData API Key

# Prices Tab --------------------------------------------------------------------------------
    def amberPrices(self, start, end, asset, granularity):
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")
        headers = {
            "accept": "application/json",
            "x-api-key": self.AMBERDATA_API_KEY
        }
        all_prices = []

        while start_date < end_date:
            # Format the startDate for the URL
            start_date_str = start_date.strftime("%Y-%m-%dT01:00:00")
            # The API can only pull one day at a time, so set end date to one day ahead
            end_date_str = (start_date + timedelta(days=1)).strftime("%Y-%m-%dT01:00:00")

            # Create the URL with the formatted dates
            url = (
                f"https://web3api.io/api/v2/market/spot/prices/assets/{asset}/historical/"
                f"?startDate={start_date_str}&endDate={end_date_str}"
                f"&timeInterval={granularity}&timeFormat=human_readable"
            )

            # Make the GET request
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                # Parse the JSON response
                json_data = response.json()
                # Extract the price data and filter out entries with '0' price
                for entry in json_data['payload']['data']:
                    price = entry.get('price', 0)
                    if isinstance(price, str):
                        price = float(price.replace(',', ''))
                    if price > 0:
                        all_prices.append(entry)
            else:
                print(f"Failed to retrieve data for {start_date_str}. Status code: {response.status_code}")

            # Increment the start_date by one day for the next iteration
            start_date += timedelta(days=1)

        return all_prices
    
# Network Tab --------------------------------------------------------------------------------
    # CHART 1 --------------------------------------------------------------------------------
    def fetchSpecificNetwork1(self):
        try:
            headers = {"X-Dune-API-Key": self.DUNE_API_KEY}
            base_url = "https://api.dune.com/api/v1/query/3177563/results"
            params = {}
            result_response = requests.get(base_url, headers=headers, params=params)

            if result_response.status_code == 200:
                data = result_response.json()
                rows = data['result']['rows']
                df = pd.DataFrame(rows)
                df.rename(columns={'x': 'Date', 'y': 'Value', 'z': 'Z_Value'}, inplace=True)
                df['Date'] = pd.to_datetime(df['Date'])
                df = df.sort_values('Date')

                return df
        except Exception as e:
            print(f"General Error: {e}")  # Use print instead of st.error since this is a method
            return None
        
    # CHART 2 --------------------------------------------------------------------------------
    def fetchSpecificNetwork2(self):
        try:
            headers = {"X-Dune-API-Key": self.DUNE_API_KEY}
            base_url = "https://api.dune.com/api/v1/query/3177615/results"
            params = {}
            result_response = requests.get(base_url, headers=headers, params=params)

            if result_response.status_code == 200:
                data = result_response.json()
                rows = data['result']['rows']
                df = pd.DataFrame(rows)
                df.rename(columns={'x': 'Date', 'y': 'Value', 'z': 'Z_Value'}, inplace=True)
                df['Date'] = pd.to_datetime(df['Date'])
                df = df.sort_values('Date')

                return df
        except Exception as e:
            print(f"General Error: {e}")  # Use print instead of st.error since this is a method
            return None
    
    # CHART 3 --------------------------------------------------------------------------------    
    def fetchSpecificNetwork3(self):
        try:
            headers = {"X-Dune-API-Key": self.DUNE_API_KEY}
            base_url = "https://api.dune.com/api/v1/query/3177607/results"
            params = {}
            result_response = requests.get(base_url, headers=headers, params=params)

            if result_response.status_code == 200:
                data = result_response.json()
                rows = data['result']['rows']
                df = pd.DataFrame(rows)
                df.rename(columns={'x': 'Date', 'y': 'Value', 'z': 'Z_Value'}, inplace=True)
                df['Date'] = pd.to_datetime(df['Date'])
                df = df.sort_values('Date')

                return df
        except Exception as e:
            print(f"General Error: {e}")  # Use print instead of st.error since this is a method
            return None
    
    # CHART 4 --------------------------------------------------------------------------------    
    def fetchSpecificNetwork4(self):
        try:
            headers = {"X-Dune-API-Key": self.DUNE_API_KEY}
            base_url = "https://api.dune.com/api/v1/query/3177679/results"
            params = {}
            result_response = requests.get(base_url, headers=headers, params=params)

            if result_response.status_code == 200:
                data = result_response.json()
                rows = data['result']['rows']
                df = pd.DataFrame(rows)
                df.rename(columns={'x': 'Date', 'y': 'Value', 'z': 'Z_Value'}, inplace=True)
                df['Date'] = pd.to_datetime(df['Date'])
                df = df.sort_values('Date')

                return df
        except Exception as e:
            print(f"General Error: {e}")  # Use print instead of st.error since this is a method
            return None

    # CHART 5 --------------------------------------------------------------------------------
    def fetchSpecificNetwork5(self):
        try:
            headers = {"X-Dune-API-Key": self.DUNE_API_KEY}
            base_url = "https://api.dune.com/api/v1/query/3177579/results"
            params = {}
            result_response = requests.get(base_url, headers=headers, params=params)

            if result_response.status_code == 200:
                data = result_response.json()
                rows = data['result']['rows']
                df = pd.DataFrame(rows)
                df.rename(columns={'x': 'Date', 'y': 'Value', 'z': 'Z_Value'}, inplace=True)
                df['Date'] = pd.to_datetime(df['Date'])
                df = df.sort_values('Date')

                return df
        except Exception as e:
            print(f"General Error: {e}")  # Use print instead of st.error since this is a method
            return None
    
    # CHART 6 --------------------------------------------------------------------------------
    def fetchSpecificNetwork6(self):
        try:
            headers = {"X-Dune-API-Key": self.DUNE_API_KEY}
            base_url = "https://api.dune.com/api/v1/query/3177667/results"
            params = {}
            result_response = requests.get(base_url, headers=headers, params=params)

            if result_response.status_code == 200:
                data = result_response.json()
                rows = data['result']['rows']
                df = pd.DataFrame(rows)
                df.rename(columns={'x': 'Date', 'y': 'Value', 'z': 'Z_Value'}, inplace=True)
                df['Date'] = pd.to_datetime(df['Date'])
                df = df.sort_values('Date')

                return df
        except Exception as e:
            print(f"General Error: {e}")  # Use print instead of st.error since this is a method
            return None

    # CHART 7 --------------------------------------------------------------------------------
    def fetchValidator1(self):
        try:
            headers = {"X-Dune-API-Key": self.DUNE_API_KEY}
            base_url = "https://api.dune.com/api/v1/query/3180493/results"
            params = {}
            result_response = requests.get(base_url, headers=headers, params=params)

            if result_response.status_code == 200:
                data = result_response.json()
                rows = data['result']['rows']
                df = pd.DataFrame(rows)
                df.rename(columns={'x': 'Date', 'y': 'Value'}, inplace=True)
                df['Date'] = pd.to_datetime(df['Date'])
                df = df.sort_values('Date')

                return df
        except Exception as e:
            print(f"General Error: {e}")  # Use print instead of st.error since this is a method
            return None

    # CHART 8 --------------------------------------------------------------------------------
    def fetchValidator2(self):
        try:
            headers = {"X-Dune-API-Key": self.DUNE_API_KEY}
            base_url = "https://api.dune.com/api/v1/query/3177667/results"
            params = {}
            result_response = requests.get(base_url, headers=headers, params=params)

            if result_response.status_code == 200:
                data = result_response.json()
                rows = data['result']['rows']
                df = pd.DataFrame(rows)
                df.rename(columns={'x': 'Date', 'y': 'Value'}, inplace=True)
                df['Date'] = pd.to_datetime(df['Date'])
                df = df.sort_values('Date')

                return df
        except Exception as e:
            print(f"General Error: {e}")  # Use print instead of st.error since this is a method
            return None

    # CHART 9 --------------------------------------------------------------------------------
    def fetchValidator3(self):
        try:
            headers = {"X-Dune-API-Key": self.DUNE_API_KEY}
            base_url = "https://api.dune.com/api/v1/query/3177667/results"
            params = {}
            result_response = requests.get(base_url, headers=headers, params=params)

            if result_response.status_code == 200:
                data = result_response.json()
                rows = data['result']['rows']
                df = pd.DataFrame(rows)
                df.rename(columns={'x': 'Date', 'y': 'Value'}, inplace=True)
                df['Date'] = pd.to_datetime(df['Date'])
                df = df.sort_values('Date')

                return df
        except Exception as e:
            print(f"General Error: {e}")  # Use print instead of st.error since this is a method
            return None

    # CHART 10 --------------------------------------------------------------------------------
    def fetchValidator4(self):
        try:
            headers = {"X-Dune-API-Key": self.DUNE_API_KEY}
            base_url = "https://api.dune.com/api/v1/query/3177667/results"
            params = {}
            result_response = requests.get(base_url, headers=headers, params=params)

            if result_response.status_code == 200:
                data = result_response.json()
                rows = data['result']['rows']
                df = pd.DataFrame(rows)
                df.rename(columns={'x': 'Date', 'y': 'Value'}, inplace=True)
                df['Date'] = pd.to_datetime(df['Date'])
                df = df.sort_values('Date')

                return df
        except Exception as e:
            print(f"General Error: {e}")  # Use print instead of st.error since this is a method
            return None

    # CHART 11 --------------------------------------------------------------------------------
    def fetchValidator5(self):
        try:
            headers = {"X-Dune-API-Key": self.DUNE_API_KEY}
            base_url = "https://api.dune.com/api/v1/query/3177667/results"
            params = {}
            result_response = requests.get(base_url, headers=headers, params=params)

            if result_response.status_code == 200:
                data = result_response.json()
                rows = data['result']['rows']
                df = pd.DataFrame(rows)
                df.rename(columns={'x': 'Date', 'y': 'Value'}, inplace=True)
                df['Date'] = pd.to_datetime(df['Date'])
                df = df.sort_values('Date')

                return df
        except Exception as e:
            print(f"General Error: {e}")  # Use print instead of st.error since this is a method
            return None

    # CHART 12 --------------------------------------------------------------------------------
    def fetchValidator6(self):
        try:
            headers = {"X-Dune-API-Key": self.DUNE_API_KEY}
            base_url = "https://api.dune.com/api/v1/query/3177667/results"
            params = {}
            result_response = requests.get(base_url, headers=headers, params=params)

            if result_response.status_code == 200:
                data = result_response.json()
                rows = data['result']['rows']
                df = pd.DataFrame(rows)
                df.rename(columns={'x': 'Date', 'y': 'Value'}, inplace=True)
                df['Date'] = pd.to_datetime(df['Date'])
                df = df.sort_values('Date')

                return df
        except Exception as e:
            print(f"General Error: {e}")  # Use print instead of st.error since this is a method
            return None

# Lending Tab --------------------------------------------------------------------------------

    def fetchMultiLine1(self, lending_protocol):
        url = f"https://api.llama.fi/protocol/{lending_protocol}"
        response = requests.get(url)
        data = response.json()

        chain_tvls = data.get('chainTvls', {})

        dfs = []
        for chain, tvl_data in chain_tvls.items():
            # Skip chains with '-borrowed' in the name or equal to 'pool2'
            if "-borrowed" in chain or chain == 'pool2':
                continue
            
            df = pd.DataFrame(tvl_data['tvl'])
            df['date'] = pd.to_datetime(df['date'], unit='s')
            df.set_index('date', inplace=True)
            df.rename(columns={'totalLiquidityUSD': chain}, inplace=True)
            dfs.append(df)

        combined_df = pd.concat(dfs, axis=1)
        combined_df = combined_df.fillna(method='ffill').fillna(method='bfill')  # Forward and backward fill to align dates

        return combined_df

    def historicalChainTvl(self, lending_protocol):
        url = f"https://bridges.llama.fi/bridgevolume/all?id={lending_protocol}"

        try:
            # Fetch data from the URL
            response = requests.get(url)
            response.raise_for_status()  # This will raise an exception for HTTP errors
            data = response.json()

            dates = []
            tvl_sums = []

            # Extract data
            for entry in data:
                date = entry.get("date", None)
                deposit_usd = entry.get("depositUSD", 0)
                withdraw_usd = entry.get("withdrawUSD", 0)

                if date is not None:
                    dates.append(date)
                    tvl_sums.append(deposit_usd + withdraw_usd)  # Sum of deposit and withdraw USD

            # Create a DataFrame
            df = pd.DataFrame({
                'Date': pd.to_datetime(dates, unit='s'),
                'Total TVL USD': tvl_sums
            })

            # Sort DataFrame by Date
            df = df.sort_values('Date')

            return df
            
        except Exception as e:
            st.error(f"Error fetching data: {e}")
            return None


    def currentChainTvls(self, lending_protocol, data, csv_file=False):
        
        try:
            chain_data = {}
            bar_chart_data = []

            # Iterate through the currentChainTvls data
            for key, value in data["currentChainTvls"].items():
                if "-borrowed" not in key:
                    continue
                # Split the key by '-' to get the chain name
                chain = key.split("-")[0]

                # Check if the chain is already in the dictionary
                if chain not in chain_data:
                    # If not, add the chain to the dictionary with the value
                    chain_data[chain] = value

            # Create a list for the bar chart data
            for key, value in chain_data.items():
                bar_chart_data.append({"Chain": key, "Borrowed Assets": value})

            if csv_file:
                # Write the data to a CSV file
                with open(f"{lending_protocol}_assets_borrowed_by_chain.csv", mode="w") as file:
                    writer = csv.writer(file)
                    writer.writerow(["Chain", "Borrowed Assets"])
                    for key, value in chain_data.items():
                        writer.writerow(
                            [key, "${:,.2f}".format(value)]
                        )  # Format the number as a currency

            return bar_chart_data
        
        except Exception as e:
            st.error(f"General Error: {e}")
            return None

    def fetchLendingData(self, lending_protocol):
        try:
            # Retrieve data from the lending protocol API
            response = requests.get(f"https://api.llama.fi/protocol/{lending_protocol}")
            response.raise_for_status()
            data = response.json()

            currentChainTvls = self.currentChainTvls(lending_protocol=lending_protocol, data=data, csv_file=False)
            historicalChainTvl = self.historicalChainTvl(data=data)

            return currentChainTvls, historicalChainTvl

        except requests.exceptions.HTTPError as errh:
            st.error(f"HTTP Error: {errh}")
            return None, None
        except requests.exceptions.ConnectionError as errc:
            st.error(f"Error Connecting: {errc}")
            return None, None
        except requests.exceptions.Timeout as errt:
            st.error(f"Timeout Error: {errt}")
            return None, None
        except requests.exceptions.RequestException as err:
            st.error(f"Something went wrong: {err}")
            return None, None
        except Exception as e:
            st.error(f"General Error: {e}")
            return None, None
        
# TEST TAB FOR DUNE CLIENT --------------------------------------------------

    #def clientTest(self, start, end, network):
     #   try:
      #      query = QueryBase(
       #         name="Sample Query",
        #        query_id=3174937,
         #       params=[
          #          QueryParameter.text_type(name="network", value=network),
           #         QueryParameter.date_type(name="start", value=start),
            #        QueryParameter.date_type(name="end", value=end),
             #   ],
           # )
           # print("Results available at", query.url())

           # dune = DuneClient.from_env()
           # results_df = dune.run_query_dataframe(query)
           # if results_df is None:
            #    print("No results returned from the query.")
             #   return pd.DataFrame()  # Return an empty DataFrame if no results

           # print(results_df)
           # return results_df

       # except Exception as e:
        #    print(f"An error occurred: {e}")
         #   return pd.DataFrame()  # Return an empty DataFrame in case of an error