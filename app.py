import json
import time
from datetime import datetime
import requests
import pandas as pd
from data import Data
import streamlit as st
import plotly.express as px
from io import StringIO
import plotly.graph_objs as go

class App:

    def __init__(self):
        self.base_currency = "usd"
        self.base_url = "https://api.coingecko.com/api/v3/coins"
        self.data_instance = Data()
        self.appSetup()

    def appSetup(self):
        # Create a Streamlit app
        st.title("December Trade ideas")

        # Create a sidebar with tabs
        st.sidebar.header("Tabs")
        selected_tab = st.sidebar.selectbox(
            "Select a Tab", ("Logic / Overview", "Cryptocurrency Prices", "Lending Protocol Data", "Ethereum Mainnet", "<PLACEHOLDER>")
        )
        
        if selected_tab == "Logic / Overview":
            self.tabHome()

        if selected_tab == "Cryptocurrency Prices":
            self.tabCryptoPrices()
        if selected_tab == "Lending Protocol Data":
            self.tabLendingData()
        if selected_tab == "Ethereum Mainnet":
            self.tabSpecificNetwork()
        if selected_tab == "<PLACEHOLDER>":
            self.clientTestTab()
    
    def tabHome(self):
        st.header("Home")
        markdown_text = """
        Idea: Bridge Tokens
            
        Stand Out Tokens:
            
        - [**Across Protocol - ACX**](https://defillama.com/protocol/across): [*$157.2m FDV*](https://www.coingecko.com/en/coins/across-protocol)
        - [**Axelar - AXL**](https://defillama.com/protocol/axelar): [*$718.3m FDV*](https://www.coingecko.com/en/coins/axelar)
        - [**ChainPort - PORTX**](https://defillama.com/protocol/chainport): [*$17.9m FDV*](https://www.coingecko.com/en/coins/chainport)
        - [**Hop Protocol - HOP**](https://defillama.com/protocol/hop-protocol): [*$60.5m FDV*](https://www.coingecko.com/en/coins/hop-protocol)
        - [**Injective - INJ**](https://defillama.com/protocol/injective-bridge): [*$1.59b FDV*](https://www.coingecko.com/en/coins/injective)
        - [**Maya Protocol - CACAO**](https://defillama.com/protocol/maya-protocol): [*$92.68m*](https://www.coingecko.com/en/coins/maya-protocol)
        - [**Symbiosis - SIS**](https://defillama.com/protocol/symbiosis): [*$42.15m*](https://www.coingecko.com/en/coins/symbiosis)
        - [**Synapse - SYN**](https://defillama.com/protocol/synapse): [*$87.1m*](https://www.coingecko.com/en/coins/synapse)
        - [**Thorchain - RUNE**](https://defillama.com/protocol/thorchain): [*$3.19b FDV](https://www.coingecko.com/en/coins/thorchain)
            
        Others to Consider:
            
        - **AllBridge - ABR** () - Super volatile recently. Shilled by big CT accounts.

        Some features of the app we may find beneficial include:

        - **Technical Knowledge Free**: Ability to create unlimited CSV files with Dune Data (only costs API request credits).
        - **Dashboard Creation**: Ability to create dashboards that can be used internally without having to share our Dune or related credentials with anyone or making our work on said platforms public.
        - **Data Visualization**: Ability to visualize data from any number of sources side by side (cuts down on the constraints of fragmented data problem for non-technical folks).
        """
        st.markdown(markdown_text)

# Price Tab --------------------------------------------------------------------------------        
    def tabCryptoPrices(self):
        # List of cryptocurrencies for the dropdown
        asset = ["Across Protocol - ACX", "AllBridge - ABR", "Axelar - AXL", "ChainPort - PORTX", "Hop Protocol - HOP", "Injective - INJ", "Maya Protocol - CACAO", "Symbiosis - SIS", "Synapse - SYN", "Thorchain - RUNE"]

        # Dropdown to select a cryptocurrency
        selected_cryptocurrency = st.sidebar.selectbox("Select a Cryptocurrency", asset)

        # Extract the cryptocurrency code from the selection
        selected_cryptocurrency_code = selected_cryptocurrency.split(" - ")[1].lower()

        # Date input for start and end dates
        start_date = st.sidebar.date_input("Start Date", datetime(2023, 10, 1))
        end_date = st.sidebar.date_input("End Date", datetime(2023, 10, 31))

        # Granularity selection
        granularity = st.sidebar.selectbox("Select Granularity", ["minute", "hour", "day"])

        # Button to fetch data
        if st.sidebar.button("Fetch Data"):
            with st.spinner("Fetching Data..."):
                # Fetch data using the amberPrices method
                price_data = self.data_instance.amberPrices(
                    start_date.strftime("%Y-%m-%d"),
                    end_date.strftime("%Y-%m-%d"),
                    selected_cryptocurrency_code,
                    granularity
                )

                if not price_data:
                    st.error(f"An error occurred while retrieving data for {selected_cryptocurrency}.")
                else:
                    # Create DataFrame from fetched data
                    df = pd.DataFrame(price_data)

                    # Remove milliseconds and convert timestamp to datetime
                    df['timestamp'] = pd.to_datetime(df['timestamp'].str.split(' ').str[0], format='%Y-%m-%d', errors='coerce')

                    # Check if 'price' and 'volume' are strings and convert them to numeric values
                    if df['price'].dtype == 'object':
                        df['price'] = df['price'].str.replace(',', '').astype(float)
                    if df['volume'].dtype == 'object':
                        df['volume'] = df['volume'].str.replace(',', '').astype(float)

                    # Remove duplicates and sort by timestamp
                    df = df.drop_duplicates(subset='timestamp')
                    df.sort_values('timestamp', inplace=True)
                    df.set_index('timestamp', inplace=True)

                    # Debug print
                    #st.write("Processed Data:", df.head())
                    # ... [previous code] ...

                    fig = go.Figure()

                    # Add bar trace for volume on the left y-axis
                    fig.add_trace(go.Bar(x=df.index, y=df['volume'], name='Volume', yaxis='y2'))

                    # Add line trace for price
                    fig.add_trace(go.Scatter(x=df.index, y=df['price'], name='Price ($)', mode='lines', yaxis='y1'))

                    # Layout updates for dual y-axes
                    fig.update_layout(
                        title=f"{selected_cryptocurrency.split(' - ')[0]} Prices and Volume",
                        xaxis=dict(title='Date'),
                        yaxis=dict(title='Price ($)', side='left', showgrid=False),
                        yaxis2=dict(title='Volume', side='right', overlaying='y', showgrid=False),
                        legend=dict(x=0.01, y=0.99, bordercolor="Black", borderwidth=1)
                    )

                    # Display the chart
                    st.plotly_chart(fig, use_container_width=True)

                    # ... [CSV export code] ...

                    # ... [rest of the method] ...

                    # CSV export
                    csv_df = df.reset_index()
                    csv_df.rename(columns={'timestamp': 'Date', 'price': 'Price USD', 'volume': 'Volume'}, inplace=True)
                    csv_data = csv_df.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv_data,
                        file_name=f"{selected_cryptocurrency_code}_prices_and_volume.csv",
                        mime='text/csv',
                        key="download-csv"
                    )
        else:
            st.warning("Select a date range and click 'Fetch Data' to view the cryptocurrency prices.")
        
        st.sidebar.markdown(
            'Data: [AmberData](https://www.amberdata.io/)',
            unsafe_allow_html=True
        )


# Network Tab --------------------------------------------------------------------------------
    def tabSpecificNetwork(self):
        st.header("Ethereum Mainnet On-Chain Data")
        chart_type = st.sidebar.radio("Select Chart Type:", ("Line Chart", "Bar Chart"))

        # Hardcoded chart titles and button names
        chart_titles = [
            "Ethereum: Daily Transaction Count",
            "Ethereum: Average TX Fee ($)",
            "Ethereum: Daily Revenue ($)",
            "Ethereum: Daily Fees Paid Per DAU",
            "Ethereum: Daily Active Users (DAU)",
            "Ethereum: Daily Gas Consumed"
        ]
        button_names = [
            "Download TX Count",
            "Download TX Fee",
            "Download Revenue",
            "Download Fee / DAU",
            "Download DAU",
            "Download Gas"
        ]

        if st.sidebar.button("Run Queries"):
            with st.spinner('Fetching data...'):
                # Fetching data for all charts
                data_frames = [
                    self.data_instance.fetchSpecificNetwork1(),
                    self.data_instance.fetchSpecificNetwork2(),
                    self.data_instance.fetchSpecificNetwork3(),
                    self.data_instance.fetchSpecificNetwork4(),
                    self.data_instance.fetchSpecificNetwork5(),
                    self.data_instance.fetchSpecificNetwork6()
                ]

            # Check if the data is fetched successfully
            if all(df is not None and not df.empty for df in data_frames):
                st.success("Data successfully fetched.")
                st.subheader("Use and Economics --------------------->")

                # Create columns for side-by-side charts
                cols = st.columns(2)

                # Function to create chart and place download button below it
                def create_chart(df, column, chart_title, button_name, chart_type, value_column='Value', additional_trace=None):
                    # Initialize a figure
                    fig = go.Figure()

                    if chart_type == "Bar Chart":
                        # Add a bar chart for the 'Value' column
                        fig.add_trace(go.Bar(x=df['Date'], y=df[value_column], name='Value'))
                    else:
                        # Add a line chart for the 'Value' column
                        fig.add_trace(go.Scatter(x=df['Date'], y=df[value_column], mode='lines', name='Value'))

                    # Add the additional trace if specified and it's not a bar chart (since Z values stay as lines)
                    if additional_trace and additional_trace in df.columns:
                        fig.add_trace(go.Scatter(x=df['Date'], y=df[additional_trace], mode='lines', name=additional_trace))

                    # Update layout options
                    fig.update_layout(
                        title=chart_title,
                        xaxis_title='Date',
                        yaxis_title='Value',
                        legend_title_text='Traces'
                    )

                    # Plot the figure in the specified column
                    column.plotly_chart(fig, use_container_width=True)

                    # Add a "Download CSV" button below the chart
                    csv_data = df.to_csv(index=False)
                    csv_io = StringIO()
                    csv_io.write(csv_data)
                    column.download_button(
                        label=button_name,
                        data=csv_io.getvalue(),
                        file_name=chart_title.replace(" ", "_").lower() + ".csv",
                        mime='text/csv',
                        key="download-csv-" + chart_title.replace(" ", "_").lower()
                    )
                    
                    # Add the markdown text under the chart
                    column.markdown('Data: [Galaxy Research Dune](https://dune.com/home)', unsafe_allow_html=True)

                # Loop through each dataframe and create its chart
                for i, df in enumerate(data_frames):
                    # Define the additional trace name based on the chart index
                    additional_trace = None
                    if i == 0 or i == 1 or i == 2 or i == 3 or i == 4 or i == 5:
                        additional_trace = 'Z_Value'  # Replace with the actual column name as required
                        
                    # Create the chart and the download button in the main layout
                    create_chart(df, cols[i % 2], chart_titles[i], button_names[i], chart_type, additional_trace=additional_trace)

               # Validator Landscape --------------------->
                st.subheader("Validator Landscape ---------->")
                
                # Fetching data for all validator charts
                validator_data_frames = [
                    self.data_instance.fetchValidator1(),
                    self.data_instance.fetchValidator2(),
                    self.data_instance.fetchValidator1(),
                    self.data_instance.fetchValidator2(),
                    self.data_instance.fetchValidator1(),
                    self.data_instance.fetchValidator2()
                ]

                # Check if the validator data is fetched successfully and display charts (extended check)
                if all(df is not None and not df.empty for df in validator_data_frames):
                    # Assuming you want a 3x2 grid for the 6 validator charts
                    validator_rows = [st.columns(3) for _ in range(2)]  # Creates two rows of three columns each

                    validator_chart_titles = [
                        "Validator Data 1", "Validator Data 2", "Validator Data 3",
                        "Validator Data 4", "Validator Data 5", "Validator Data 6"
                    ]

                    for i, data_frame in enumerate(validator_data_frames):
                        row = i // 3
                        col = i % 3
                        self.create_validator_chart(data_frame, validator_rows[row][col], validator_chart_titles[i], chart_type)
                else:
                    st.warning("Data fetching was incomplete for validator data. Please try running the queries again.")
            else:
                st.warning("Data fetching was incomplete. Please try running the queries again.")
        else:
            st.warning("Please press 'Run Queries' to fetch the data.")

    def create_validator_chart(self, df, column, chart_title, chart_type):
        fig = go.Figure()

        if chart_type == "Bar Chart":
            fig.add_trace(go.Bar(x=df['Date'], y=df['Value'], name='Value'))
        else:
            fig.add_trace(go.Scatter(x=df['Date'], y=df['Value'], mode='lines', name='Value'))

        fig.update_layout(
            title=chart_title,
            xaxis_title='Date',
            yaxis_title='Value',
            legend_title_text='Traces'
        )

        column.plotly_chart(fig, use_container_width=True)

        # Add a "Download CSV" button below the chart
        csv_data = df.to_csv(index=False)
        csv_io = StringIO()
        csv_io.write(csv_data)
        column.download_button(
            label="Download " + chart_title,
            data=csv_io.getvalue(),
            file_name=chart_title.replace(" ", "_").lower() + ".csv",
            mime='text/csv',
            key="download-csv-" + chart_title.replace(" ", "_").lower()
        )
        
        # Add the markdown text under the chart
        column.markdown('Data: [Coin Metrics](https://coinmetrics.io/)', unsafe_allow_html=True)


# Category Tab --------------------------------------------------------------------------------
    def tabLendingData(self):
        lending_protocol = st.sidebar.text_input(
            "Enter lending protocol (Aave, Compound, Venus, etc.):"
        )
        lending_protocol = lending_protocol.lower()

        st.sidebar.header("Historical Borrowed and Current Borrowed Data")
        if st.sidebar.button("Fetch Lending Protocol Data"):
            with st.spinner('Fetching data...'):
                try:
                    # Existing functionality to fetch and display the first two charts
                    protocol_data, historical_df = self.data_instance.fetchLendingData(lending_protocol)
                    if protocol_data:
                        st.success("Data successfully fetched for the first two charts.")
                        
                        # Display the line chart for historical borrowed data
                        st.write("Historical Borrowed Assets:")
                        st.plotly_chart(
                            px.line(
                                historical_df,
                                x="Date",
                                y="Tvl",
                                title="Historical Borrowed Assets",
                            ),
                            use_container_width=True,
                        )

                        # Create a DataFrame from the protocol data for the bar chart
                        protocol_df = pd.DataFrame(protocol_data)

                        # Display the bar chart for current borrowed data
                        st.write("Current Borrowed Assets by Chain:")
                        st.plotly_chart(
                            px.bar(
                                protocol_df,
                                x="Chain",
                                y="Borrowed Assets",
                                title="Current Borrowed Assets by Chain",
                            ),
                            use_container_width=True,
                        )
                    
                   # Fetch data for the third chart using fetchMultiLine1
                    multi_line_df = self.data_instance.fetchMultiLine1(lending_protocol)
                    st.write("Total Value Locked (TVL) Across Chains:")
                    
                    # Let the user choose the type of chart
                    chart_type = st.radio(
                        "Choose chart type:",
                        ('Line Chart', 'Stacked Bar Chart')
                    )

                    if chart_type == 'Line Chart':
                        fig = px.line(
                            multi_line_df,
                            title="Total Value Locked (TVL) Across Chains"
                        )
                    else:  # Stacked Bar Chart
                        fig = px.bar(
                            multi_line_df,
                            title="Total Value Locked (TVL) Across Chains",
                            barmode='stack'
                        )

                    st.plotly_chart(fig, use_container_width=True)

                except Exception as e:
                    st.error(f"Failed to fetch data: {e}")
            
        st.sidebar.markdown(
            'Data: [DeFiLlama](https://defillama.com/)',
            unsafe_allow_html=True
        )
# Trigger App
App()