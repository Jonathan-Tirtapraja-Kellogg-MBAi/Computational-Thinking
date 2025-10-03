# Netid: ZAP9441 & BVG4349
from match import match
from data import features

##########Action Functions###############################
    
def country_by_rank(matches):
    """Takes a list of matches as input - specifically one that holds a rank
        and a feature, like 'population.' Finds the country with that rank
        using the feature and returns it in a list.

        Args: matches - a list of strings resulting from a call to match. It
        holds a rank and a feature.

        Returns: a list of one string - the rank of the country for the
        specified feature. If the country or feature is not found, returns an
        empty list.
    """
    if not matches or len(matches) < 2:
        return []
    rank, feature = matches[0], matches[1].lower()
    if feature in features:
        for country, (r, v) in features[feature].items():
            if r == rank:
                return [country]
    return []

def rank_by_country(matches):
    """Takes a list of matches as input - specifically one that holds a country
        and a feature, like 'population.' Finds the rank for that country
        using tha feature and returns it in a list.

        Args: matches - a list of strings resulting from a call to match. It
        holds a country and a feature.

        Returns: a list of one string - the rank of the country for the
        specified feature. If the country or feature is not found, returns an
        empty list.
    """
    if not matches or len(matches) < 2:
        return []
    country, feature = matches[0].lower(), matches[1].lower()
    if feature not in features:
        return []

    data = features[feature]
    if country not in data:
        return []
    return [data[country][0]]

def list_countries(unused):
    """Takes an input that is unused (empty list resulting from a call to match).
        Constructs a list of countries by looking at the keys from one of the
        dictionaries. You can use any of the dictionaries for this. I know
        this is not an accurate response as some countries are listed under
        some features but not under others.

        Args: unused - an empty list resulting from a call to match.

        Returns: a list of countries.
    """
    any_feature = next(iter(features))
    return sorted(list(features[any_feature].keys()))

def list_patterns(unused):
    """Takes an input that is unused (empty list resulting from a call to match).
        Constructs a list of the patterns from the pa_list and returns it.

        Args: unused - an empty list resulting from a call to match.

        Returns: a list of the known patterns.
    """
    out = []
    for pat, action in pa_list:
        out.append(" ".join(pat))
    return out


def bye_action(unused):
    """This action function gets called when the user writes 'bye'.
        It raises KeyboardInterrupt in order to break out of the query loop.

        Args: unused - an empty list resulting from a call to match.
    """
    raise KeyboardInterrupt


def list_data_set(unused):
    """Returns the names of all datasets stored in the features dictionary.
        This answers the question: "What datasets does the bot know about?"
        Each dataset corresponds to a key in the global features dictionary.
        Returns:
            list[str]: A list of dataset names (keys of features).
    """
    return list(features.keys())

def max_country(matches):
    """
        Finds the top-ranked country for a given dataset (feature).

        This function expects `matches` to contain at least one element
        representing the name of a dataset (e.g., "population", "gdp").
        It looks up the dataset in the global `features` dictionary, then
        searches for the country whose rank is "1". If found, it returns
        the country and its associated value.

        Args:
            matches - a list of strings resulting from a call to match. It
            holds a country's name

        Returns:
            list[str]: [country, value] for the top-ranked entry in that dataset.
                       Returns an empty list if the dataset does not exist
                       or no rank "1" entry is found.
    """
    if not matches or len(matches) < 1:
        return []
    feature = matches[0].lower()
    data = features.get(feature)
    if not data:
        return []

    for country, pair in data.items():  # pair = [rank, value]
        if pair and pair[0] == "1":
            return [country, pair[1]]
    return []

def all_data_country(matches):
    """
    Given a country name, returns that country's rank and value
    across all available datasets in the global `features` dictionary.

    This function searches each dataset in `features`.
    For every dataset where the country exists, its rank and value are collected.

    Args:
        matches - a list of strings resulting from a call to match. It
        holds a country's name

    Returns:
        list[str]: A list of strings in the form:
                   "<feature_name>: rank <rank>, value <value>"
                   for each dataset the country is found in.
        Returns an empty list if no matches or if the
            country is not found in any dataset.
    """
    if not matches or len(matches) < 1:
        return []

    country = " ".join(matches[0].lower().split())
    answers = []

    for feature_name, data in features.items():
        rec = data.get(country)
        if not rec:
            continue
        if rec and len(rec) >= 2:
            rank, value = rec[0], rec[1]
            answers.append(f"{feature_name}: rank {rank}, value {value}")

    return answers

##########Pattern, Action list###############################

pa_list = [(str.split("which country is ranked number _ for %"), country_by_rank),
           (str.split("what is % ranked for %"), rank_by_country),
           (str.split("which countries do you know about"), list_countries),
           (str.split("what kinds of questions do you understand"), list_patterns),
           (str.split("what datasets do you know about"), list_data_set),
           (str.split("which country has the highest %"), max_country),
           (str.split("show me all the data for %"), all_data_country),
           (["bye"], bye_action)]

def search_pa_list(src):
    """Takes source, finds matching pattern and calls corresponding action. If it finds
    a match but has no answers it returns ["No answers"]. If it finds no match it
    returns ["I don't understand"].

    Args:
        source - a phrase represented as a list of words (strings)

    Returns:
        a list of answers. Will be ["I don't understand"] if it finds no matches and
        ["No answers"] if it finds a match but no answers
    """
    for pattern, action in pa_list:
        match_result = match(pattern, src)
        if match_result is None:
            continue
        answer = action(match_result)
        if not answer:
            return ["No answers"]
        return answer
    return ["I don't understand"]

def query_loop():
    """Query_lop asks the user for input, then "cleans" that input
        by converting all characters to lowercase, removing any training
        punctuation (e.g. ?). After then converting the input to a list
        of strings, we pass the list off to search_pa_list to get answers,
        then display the answers to the user.
        Use a try/except structure to catch Ctrl-C or Ctrl-D characters
        and exit gracefully. You'll need to except KeyboardInterrupt and
        EOFError.
    """
    try:
        while True:
            raw = input("> ")
            source = raw.strip().lower().rstrip("?.!").split()
            answers = search_pa_list(source)
            print(answers)
    except (KeyboardInterrupt, EOFError):
        print("Goodbye!")

    pass

if __name__ == "__main__":
    assert country_by_rank(["2", "population"]) == ["india"], "country_by_rank test"
    assert rank_by_country(["united states", "area"]) == ["4"], "rank_by_country test"
    assert search_pa_list(["hi", "there"]) == ["I don't understand"], "search_pa_list test 1"
    assert search_pa_list(["which", "country", "is", "ranked", "number", "2", "for",
                           "median", "age"]) == ["japan"], "search_pa_list test 2"
    assert search_pa_list(["what", "is", "XYZ", "ranked", "for", "population"]) == [
        "No answers"], "search_pa_list test 3"
    assert search_pa_list(["which", "country", "has", "the", "highest", "area"]) == ["russia",
                                                                                     "17,098,242"], "search_pa_list test 4"
    assert search_pa_list(["which", "country", "has", "the", "highest", "population"]) == ["china",
                                                                                           "1,397,897,720"], "search_pa_list test 5"
    # uncomment the line below to interact with your chatbot
    query_loop()
