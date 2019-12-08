"""Assignment 3: Club Recommendations - Starter code."""
from typing import List, Tuple, Dict, TextIO


# Sample Data (Used by Doctring examples)

P2F = {'Jesse Katsopolis': ['Danny R Tanner', 'Joey Gladstone',
                            'Rebecca Donaldson-Katsopolis'],
       'Rebecca Donaldson-Katsopolis': ['Kimmy Gibbler'],
       'Stephanie J Tanner': ['Michelle Tanner', 'Kimmy Gibbler'],
       'Danny R Tanner': ['Jesse Katsopolis', 'DJ Tanner-Fuller',
                          'Joey Gladstone']}

P2C = {'Michelle Tanner': ['Comet Club'],
       'Danny R Tanner': ['Parent Council'],
       'Kimmy Gibbler': ['Rock N Rollers', 'Smash Club'],
       'Jesse Katsopolis': ['Parent Council', 'Rock N Rollers'],
       'Joey Gladstone': ['Comics R Us', 'Parent Council']}


# Helper functions

def update_dict(key: str, value: str,
                key_to_values: Dict[str, List[str]]) -> None:
    """Update key_to_values with key/value. If key is in key_to_values,
    and value is not already in the list associated with key,
    append value to the list. Otherwise, add the pair key/[value] to
    key_to_values.

    >>> d = {'1': ['a', 'b']}
    >>> update_dict('2', 'c', d)
    >>> d == {'1': ['a', 'b'], '2': ['c']}
    True
    >>> update_dict('1', 'c', d)
    >>> d == {'1': ['a', 'b', 'c'], '2': ['c']}
    True
    >>> update_dict('1', 'c', d)
    >>> d == {'1': ['a', 'b', 'c'], '2': ['c']}
    True
    """

    if key not in key_to_values:
        key_to_values[key] = []

    if value not in key_to_values[key]:
        key_to_values[key].append(value)

def sort_clubs(clubs: List[Tuple[str, int]])->None:
    """Updates clubs such that the recommendations
    are sorted from highest to lowest score. If multiple clubs have
    the same score, they are sorted alphabetically by clubs' names.

    >>> clubs_to_sort = [('CS',5),('Math',2),('English',3),('Calc',3)]
    >>> sort_clubs(clubs_to_sort)
    >>> clubs_to_sort == [('CS',5),('Calc',3),('English',3),('Math',2)]
    True
    
    """

    l = len(clubs)
    for i in range(0, l):
        for j in range(0, l - i - 1):
            if (clubs[j][1] < clubs[j + 1][1]):
                clubs[j], clubs[j + 1] = clubs[j + 1], clubs[j]

    for club in range(l - 1):
        if clubs[club][1] == clubs[club + 1][1]:
            pairs_clubs = [clubs[club], clubs[club + 1]]
            pairs_clubs.sort()
            clubs[club], clubs[club + 1] = pairs_clubs[0], pairs_clubs[1]


def add_pts_method1(potential_clubs: Dict[str, int],
                    person_to_friends: Dict[str, List[str]],
                    person_to_clubs: Dict[str, List[str]],
                    person: str)->None:
    """Updates potential_clubs such that the potential club's score
    for each of the person person's friends who are members
    of the potential club, increases by 1.

    >>> P2F={"David":['Rob','Cass']}
    >>> P2C={"Rob":['Math'], "Ken":['CS']}
    >>> person="David"
    >>> potential_clubs={"Math":0, "CS":0}
    >>> add_pts_method1(potential_clubs,P2F,P2C, person)
    >>> potential_clubs == {"Math":1, "CS":0}
    True

    """
    
    clubs_to_person = invert_and_sort(person_to_clubs)
    friends_to_person = invert_and_sort(person_to_friends)
    for club in potential_clubs:
        if person in person_to_friends:
            for friend in person_to_friends[person]:
                if (person not in clubs_to_person[club]\
                and person in friends_to_person[friend]) and\
                (friend in clubs_to_person[club]):
                    potential_clubs[club] += 1

def add_pts_method2(potential_clubs: Dict[str, int],
                    person_to_clubs: Dict[str, List[str]],
                    person: str)->None:
    """Updates potential_clubs such that potential club's score
    increases by 1 for every member of the potential club, who is
    in at least one different club with person.
    
    >>> P2F={"David":['Rob','Cass']}
    >>> P2C={"Rob":['Math', 'English'], "Ken":['CS'], 'David':['English']}
    >>> person="David"
    >>> potential_clubs={"Math":0, "CS":0, "English":0}
    >>> add_pts_method1(potential_clubs,P2F,P2C, person)
    >>> potential_clubs == {"Math":1, "CS":0, "English":0}
    True
    
    """
    
    clubs_to_person = invert_and_sort(person_to_clubs)
    for club in potential_clubs:
        for other in clubs_to_person[club]:
            for club2 in clubs_to_person:
                if club != club2 and person in clubs_to_person[club2] and\
                    other in clubs_to_person[club2] and \
                    other != person and \
                    len(person_to_clubs[other]) > 1 and\
                    club in person_to_clubs[other]:

                    potential_clubs[club] += 1
    
# Required functions


def load_profiles(profiles_file: TextIO) -> Tuple[Dict[str, List[str]],
                                                  Dict[str, List[str]]]:
    """Return a two-item tuple containing a "person to friends" dictionary
    and a "person_to_clubs" dictionary with the data from
    profiles_file.

    NOTE: Functions (including helper functions) that have a parameter
          of type TextIO do not need docstring examples.

    """

    person_to_friends, person_to_clubs, first_line_profile = {}, {}, True
    for line in profiles_file.readlines():
        if line != '\n':
            line = line[:-1]
            if first_line_profile:
                name = line[line.find(',')+2:] + ' ' + line[:line.find(',')]
                person_to_friends[name], person_to_clubs[name] = [], []
            else:
                if ',' in line:
                    friend = line[line.find(',')+2:]+' '+line[:line.find(',')]
                    person_to_friends[name].append(friend)

                else: person_to_clubs[name].append(line)
                person_to_friends[name].sort()
                person_to_clubs[name].sort()
            first_line_profile = False
        else:
            first_line_profile = True

    r_person_to_friends, r_person_to_clubs = {}, {}

    for person in person_to_friends:
        if len(person_to_friends[person]) > 0:
            r_person_to_friends[person] = person_to_friends[person]
        if len(person_to_clubs[person]) > 0:
            r_person_to_clubs[person] = person_to_clubs[person]

    return (r_person_to_friends, r_person_to_clubs)


def get_average_club_count(person_to_clubs: Dict[str, List[str]]) -> float:
    """Return the average number of clubs that a person in person_to_clubs
    belongs to.

    >>> get_average_club_count(P2C)
    1.6

    """
    clubs = 0
    if len(person_to_clubs) == 0:
        return 0
    for person in person_to_clubs:
        clubs += len(person_to_clubs[person])
    return clubs / len(person_to_clubs)


def get_last_to_first(
        person_to_friends: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """Return a "last name to first name(s)" dictionary with the people
    from the "person to friends" dictionary person_to_friends.

    >>> get_last_to_first(P2F) == {
    ...    'Katsopolis': ['Jesse'],
    ...    'Tanner': ['Danny R', 'Michelle', 'Stephanie J'],
    ...    'Gladstone': ['Joey'],
    ...    'Donaldson-Katsopolis': ['Rebecca'],
    ...    'Gibbler': ['Kimmy'],
    ...    'Tanner-Fuller': ['DJ']}
    True

    """
    names = []
    last_to_first = {}
    for person in person_to_friends:
        names.append(person)
        for friend in person_to_friends[person]:
            if friend not in names and len(friend) != 0:
                names.append(friend)

    for name in names:
        last = name[name.rfind(' ') + 1:]
        first = name[:name.rfind(' ')]
        update_dict(last, first, last_to_first)
        last_to_first[last].sort()

    return last_to_first


def invert_and_sort(key_to_value: Dict[object, object]) -> Dict[object, list]:
    """Return key_to_value inverted so that each key is a value (for
    non-list values) or an item from an iterable value, and each value
    is a list of the corresponding keys from key_to_value.  The value
    lists in the returned dict are sorted.

    >>> invert_and_sort(P2C) == {
    ...  'Comet Club': ['Michelle Tanner'],
    ...  'Parent Council': ['Danny R Tanner', 'Jesse Katsopolis',
    ...                     'Joey Gladstone'],
    ...  'Rock N Rollers': ['Jesse Katsopolis', 'Kimmy Gibbler'],
    ...  'Comics R Us': ['Joey Gladstone'],
    ...  'Smash Club': ['Kimmy Gibbler']}
    True

    """
    inverted = {}
    for key in key_to_value:
        for val in key_to_value[key]:
            if val not in inverted:
                inverted[val] = []
            inverted[val].append(key)
            inverted[val].sort()

    return inverted


def get_clubs_of_friends(person_to_friends: Dict[str, List[str]],
                         person_to_clubs: Dict[str, List[str]],
                         person: str) -> List[str]:
    """Return a list, sorted in alphabetical order, of the clubs in
    person_to_clubs that person's friends from person_to_friends
    belong to, excluding the clubs that person belongs to.  Each club
    appears in the returned list once per each of the person's friends
    who belong to it.

    >>> get_clubs_of_friends(P2F, P2C, 'Danny R Tanner')
    ['Comics R Us', 'Rock N Rollers']

    """
    clubs = []
    for friend in person_to_friends[person]:
        if friend in person_to_clubs and person in person_to_clubs:
            for club in person_to_clubs[friend]:
                if club not in person_to_clubs[person]:
                    clubs.append(club)

    clubs.sort()
    return clubs

def recommend_clubs(
        person_to_friends: Dict[str, List[str]],
        person_to_clubs: Dict[str, List[str]],
        person: str,) -> List[Tuple[str, int]]:
    """Return a list of club recommendations for person based on the
    "person to friends" dictionary person_to_friends and the "person
    to clubs" dictionary person_to_clubs using the specified
    recommendation system.

    >>> recommend_clubs(P2F, P2C, 'Stephanie J Tanner')
    [('Comet Club', 1), ('Rock N Rollers', 1), ('Smash Club', 1)]

    """

    potential_clubs = {}
    clubs_to_person = invert_and_sort(person_to_clubs)
    for club in clubs_to_person:
        if person not in clubs_to_person:
            potential_clubs[club] = 0

    add_pts_method1(potential_clubs, person_to_friends, person_to_clubs, person)
    add_pts_method2(potential_clubs, person_to_clubs, person)

    r_potential_clubs = []
    for club in potential_clubs:
        if potential_clubs[club] > 0:
            r_potential_clubs.append((club, potential_clubs[club]))

    sort_clubs(r_potential_clubs)

    return r_potential_clubs

if __name__ == '__main__':
    pass
    #recommend_clubs(P2F, P2C, 'Rebecca Donaldson-Katsopolis')
    #load_profiles(profiles_file)

    # If you add any function calls for testing, put them here.
    # Make sure they are indented, so they are within the if statement body.
    # That includes all calls on print, open, and doctest.

    #import doctest
    #doctest.testmod()
