def sort_and_display_countries():
    list_of_tuples = [
        ('Russia', '25'),
        ('France', '132'),
        ('Germany', '132'),
        ('Spain', '178'),
        ('Italy', '162'),
        ('Portugal', '17'),
        ('Finland', '3'),
        ('Hungary', '2'),
        ('The Netherlands', '28'),
        ('The USA', '610'),
        ('The United Kingdom', '95'),
        ('China', '83'),
        ('Iran', '76'),
        ('Turkey', '65'),
        ('Belgium', '34'),
        ('Canada', '28'),
        ('Switzerland', '26'),
        ('Brazil', '25'),
        ('Austria', '14'),
        ('Israel', '12')
    ]
    
    country_dict = {}
    for country, number in list_of_tuples:
        country_dict[country] = int(number)
    
    # Sort the dictionary items first by value in descending order, then by key in ascending order
    sorted_items = sorted(country_dict.items(), key=lambda item: (-item[1], item[0]))
    
    for country, number in sorted_items:
        print(country)

if __name__ == "__main__":
    sort_and_display_countries()