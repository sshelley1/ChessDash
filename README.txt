For this to work correctly follow these instructions:M

1. Make sure Kibana and ElasticSearch are installed and running
2. Open Kibana and copy paste the code from json_mapping_kibana .txt file into the Developer's Console
3. Execute the line with "PUT /chess_geocoord"
4. Run the chess_data-collect-script to collect data for kibana
5. Specify the location of index patterns "chess_geocoord" and "chess_non_geocoord" under management, 
	**make sure "Index contains time-based events" is unchecked
6. Import all json files for searches, dashboard, and visuals into Kibana under Management