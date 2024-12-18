# North Carolina Election and Census Data Visualization

## Overview
This project focuses on gathering, processing, and visualizing North Carolina election data alongside census demographic data. The end result is an interactive choropleth map that allows users to explore various statistics for each county in North Carolina.

---

## Data Sources
1. **Election Results Data**
   - The historical election results data was pulled from the [North Carolina State Board of Elections](https://www.ncsbe.gov/results-data/election-results/historical-election-results-data#by-precinct).
   - The data includes county-level results for elections in North Carolina, broken down by party votes and other relevant metrics.

2. **Census Demographic Data**
   - Demographic data was obtained via the U.S. Census Bureau's API, specifically through datasets found on the [Census Bureau Developer Data Sets](https://www.census.gov/data/developers/data-sets.html).
   - This data includes:
     - Population statistics
     - Median age
     - Median income
     - Racial demographics (White, Black, Native, Asian, Hispanic)
     - Education levels (bachelor's degree, master's degree, STEM fields)
     - Median home value

3. **FIPS Codes**
   - FIPS (Federal Information Processing Standard) codes were used to ensure proper county-level mapping.
   - The `geojson` file for counties was retrieved from the [Plotly GeoJSON Dataset](https://plotly.com/python/county-choropleth/).

---

## Tools and Technologies
- **Pandas**: For cleaning, merging, and analyzing the election and census data.
- **Plotly Express**: To create the interactive choropleth map for North Carolina counties.
- **Python**: General scripting and data manipulation.

---

## Process
### 1. Data Collection
- **Election Results**: CSV files were downloaded from the North Carolina State Board of Elections.
- **Census Data**: API calls were made to the Census Bureau to retrieve demographic information, including population, age, income, and racial breakdown.

### 2. Data Cleaning and Merging
- The county names were standardized (e.g., removing "COUNTY" suffixes) to ensure consistency between the datasets.
- FIPS codes were merged with the election and census data to enable geographic mapping.

### 3. Visualization
- A **choropleth map** was created using Plotly Express.
- The map allows users to select and view various metrics such as:
  - Population
  - Median Age
  - Median Income
  - Median Home Value
  - Racial Composition (White, Black, Native, Asian, Hispanic)
  - Education Levels (Bachelor's Degree, Master's Degree, STEM fields)
- The map is interactive, enabling hovering over counties to display specific data values.

---

## How to Run
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Install required libraries:
   ```bash
   pip install pandas plotly requests
   ```
3. Run the script:
   ```bash
   python main.py
   ```

4. Open the generated map in your browser.

---

## References
- [North Carolina State Board of Elections](https://www.ncsbe.gov/results-data/election-results/historical-election-results-data#by-precinct)
- [U.S. Census Bureau API](https://www.census.gov/data/developers/data-sets.html)
- [Plotly County Choropleth Documentation](https://plotly.com/python/county-choropleth/)
