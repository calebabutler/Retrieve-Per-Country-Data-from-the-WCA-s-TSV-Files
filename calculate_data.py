#!/usr/bin/env python3
import sys

def get_competitions_in_year(competitions_filepath, year_string):
    competitions = []
    with open(competitions_filepath) as f:
        next(f)
        for line in f:
            line_data = line.split("\t")
            if line_data[5] == year_string:
                competitions.append(line_data[0])
    return competitions

def create_persons_dict(results_filepath, competitions):
    persons = {}
    with open(results_filepath) as f:
        next(f)
        for line in f:
            line_data = line.split("\t")
            if line_data[0] in competitions:
                average = int(line_data[5])
                if line_data[7] in persons:
                    if average < persons[line_data[7]][1]:
                        persons[line_data[7]][1] = average
                else:
                    persons[line_data[7]] = [line_data[8], average]
    return persons

def get_bound(number, bounds):
    for i, bound in enumerate(bounds):
        if number >= bound[0] and number < bound[1]:
            return i
    if number >= bounds[-1][1]:
        return len(bounds)
    return -1

def create_countries_dict(persons, bounds):
    countries = {}
    for person, person_data in persons.items():
        if person_data[0] not in countries:
            countries[person_data[0]] = [0] * (len(bounds) + 1)
        bound = get_bound(person_data[1], bounds)
        if bound >= 0:
            countries[person_data[0]][bound] += 1
    return countries

def remove_countries_under_x(countries, x):
    countries_x_or_over = {}
    for country, country_data in countries.items():
        total_population = 0
        for data in country_data:
            total_population += data
        if total_population >= x:
            countries_x_or_over[country] = country_data
    return countries_x_or_over

# def add_countries_totals(countries, bounds):
#     countries["Total"] = [0] * (len(bounds) + 1)
#     for i in range(len(bounds) + 1):
#         for country, country_data in countries.items():
#             countries["Total"][i] += country_data[i]
#     for country, country_data in countries.items():
#         data_total = 0
#         for data in country_data:
#             data_total += data
#         country_data.append(data_total)

# def get_countries_expected_values(countries, bounds):
#     expected_values = {}
#     for country, country_data in countries.items():
#         expected_values[country] = [0] * len(country_data)
#         for i in range(len(bounds) + 1):
#             expected_values[country][i] = (country_data[-1] *
#                                            countries["Total"][i] /
#                                            countries["Total"][-1])
#         expected_values[country][-1] = country_data[-1]
#     return expected_values

def print_country_data(countries, bounds):
    for country, country_data in countries.items():
        print("--- " + country + " ---")
        print()
        for i, bound in enumerate(bounds):
            print("[" + str(bound[0]) + ", " + str(bound[1]) + ")\t: " +
                  str(country_data[i]))
        print("[" + str(bounds[-1][1]) + ", inf)\t: " +
              str(country_data[len(bounds)]))
        print()

def print_country_data_tsv(countries, bounds):
    for country, country_data in countries.items():
        print("\t" + country, end = "")
    print()
    for i, bound in enumerate(bounds):
        print("[" + str(bound[0]) + ", " + str(bound[1]) + ")", end = "")
        for country, country_data in countries.items():
            print("\t" + str(country_data[i]), end = "")
        print()
    print("[" + str(bounds[-1][1]) + ", inf)", end = "")
    for country, country_data in countries.items():
        print("\t" + str(country_data[len(bounds)]), end = "")
    print()

def get_per_country_data_from_wca_tsv_files(min_country_population):
    competitions = get_competitions_in_year("WCA_export_Competitions.tsv",
                                            "2017")
    persons = create_persons_dict("WCA_export_Results.tsv", competitions)
    del competitions
    bounds = [
        [1, 1500],
        [1500, 3000],
    ]
    countries = create_countries_dict(persons, bounds)
    del persons
    countries_x_or_over = remove_countries_under_x(countries,
                                                   min_country_population)
    print_country_data_tsv(countries_x_or_over, bounds)

def main():
    with open("results.tsv", "w") as output_file:
        sys.stdout = output_file
        if len(sys.argv) < 2 or not sys.argv[1].isdigit():
            print("The first argument must be an integer representing the " +
                  "minimum country population.", file = sys.stderr)
        else:
            get_per_country_data_from_wca_tsv_files(int(sys.argv[1]))

if __name__ == "__main__":
    main()
