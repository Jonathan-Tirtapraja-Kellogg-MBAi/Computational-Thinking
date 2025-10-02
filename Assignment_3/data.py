
import csv

def load_csv(file_name):
    """Opens and reads the provided file. Creates a dictionary that maps name to a
        list of ranking and value. For example, the "population" dictionary would look like...
        {'china': ['1', '1,397,897,720'],
        'india': ['2', '1,339,330,514'],
        'united states': ['3', '334,998,398'],
        'isndonesia': ['4', '275,122,131'],
        ...}
        Notice that all items in values/lists (e.g. ['1', '1,397,897,720']) are strings.

        Args:
            The path of a csv file that contains some world factbook country comparison data.
            The file must be one that includes the following fields: name, ranking, and value. 

        Returns:
            A dictionary mapping 'name' to a list containing rank and value - both as strings. 
        """
    
    
    d = dict()
    with open(file_name, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for a_row in reader:
            d[a_row[0].lower()] = [a_row[4], a_row[2]]

    return d

#https://www.cia.gov/the-world-factbook/references/guide-to-country-comparisons/
#Here we will create a dictionary where the keys are attribute names, like "area" or "life expectancy."
#   These keys will map to values that are themselves dictionaries. 
features = {}
features["area"] = load_csv("world_factbook/geography/area.csv")
features["population"] = load_csv("world_factbook/people_and_society/population.csv")
features["median age"] = load_csv("world_factbook/people_and_society/median_age.csv")
features["life expectancy"] = load_csv("world_factbook/people_and_society/life_expectancy_at_birth.csv")
features["gdp"] = load_csv("world_factbook/economy/real_gdp_purchasing_power_parity.csv")
