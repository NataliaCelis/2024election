import pandas as pd

# Load the election results file
data = pd.read_csv("srcs/election_results.txt", delimiter="\t")

# Rename columns for easier handling
data.columns = [col.strip().lower().replace(" ", "_") for col in data.columns]

# Keep only relevant columns
columns_to_keep = ['county', 'precinct', 'choice_party', 'total_votes']
data = data[columns_to_keep]

# Remove rows with zero or missing votes
data = data.dropna(subset=['total_votes'])
data = data[data['total_votes'] > 0]

# Create party-specific DataFrames
dem_votes = data[data['choice_party'] == 'DEM'].groupby(['county', 'precinct'], as_index=False)['total_votes'].sum()
rep_votes = data[data['choice_party'] == 'REP'].groupby(['county', 'precinct'], as_index=False)['total_votes'].sum()
third_votes = data[~data['choice_party'].isin(['DEM', 'REP'])].groupby(['county', 'precinct'], as_index=False)['total_votes'].sum()

# Rename columns for clarity
dem_votes = dem_votes.rename(columns={'total_votes': 'dem'})
rep_votes = rep_votes.rename(columns={'total_votes': 'rep'})
third_votes = third_votes.rename(columns={'total_votes': 'third'})

# Merge all party-specific votes into a single DataFrame
precinct_summary = pd.merge(dem_votes, rep_votes, on=['county', 'precinct'], how='outer')
precinct_summary = pd.merge(precinct_summary, third_votes, on=['county', 'precinct'], how='outer')

# Fill missing values with 0 (no votes for that party)
precinct_summary[['dem', 'rep', 'third']] = precinct_summary[['dem', 'rep', 'third']].fillna(0)

# Calculate total votes
precinct_summary['total'] = precinct_summary['dem'] + precinct_summary['rep'] + precinct_summary['third']

# Calculate percentages and round to 2 decimal places
precinct_summary['pct_dem'] = ((precinct_summary['dem'] / precinct_summary['total']) * 100).round(2)
precinct_summary['pct_rep'] = ((precinct_summary['rep'] / precinct_summary['total']) * 100).round(2)
precinct_summary['pct_third'] = ((precinct_summary['third'] / precinct_summary['total']) * 100).round(2)

# Calculate margin and round to 2 decimal places
precinct_summary['pct_margin'] = (precinct_summary['pct_dem'] - precinct_summary['pct_rep']).round(2)

# Rename 'precinct' to 'precinct_id'
precinct_summary.rename(columns={'precinct': 'precinct_id'}, inplace=True)

# Reorganize columns (exclude 'precinct_name')
final_columns = ['county', 'precinct_id', 'dem', 'rep', 'third',
                 'total', 'pct_dem', 'pct_rep', 'pct_third', 'pct_margin']
precinct_summary = precinct_summary[final_columns]

# Save the cleaned data to a CSV file
output_file = "cleaned_election_results_summary.csv"
precinct_summary.to_csv(output_file, index=False)

print(f"Data cleaned and saved as {output_file}")
