import pandas as pd
import random
import csv


def get_indics(company, year, risk):
    try:
        csv_file = f"data/{company}.csv"
        df = pd.read_csv(csv_file, delimiter=',',
                         quotechar='"', on_bad_lines='skip')

        if year in df.columns:
            first_column = df.columns[0]
            filtered_df = df[[first_column, year]]
            json_data = filtered_df.to_json(orient='records')
            return json_data
        else:
            return f"Year {year} not found in data."
    except Exception as e:
        return f"Error : {e}"


def get_quant_indics(company, year, risk):
    try:
        csv_file = f"data/{company}.csv"
        df = pd.read_csv(csv_file, delimiter=',',
                         quotechar='"', on_bad_lines='skip')

        if year in df.columns:
            first_column = df.columns[0]
            filtered_df = df[[first_column, year]].set_index(first_column)

            ratios = {}
            sumproduct = 0

            # 'Ratio d\'autonomie financière'
            num = filtered_df.loc['Capitaux propre', year]
            denom = filtered_df.loc['Total Bilan', year]
            ratios['Ratio d\'autonomie financière'] = num / denom

            # 'Ratio de capacité de remboursement'
            num = filtered_df.loc['Dette Long/Moyen Terme', year]
            denom = filtered_df.loc['Excédent Brut d\'exploitation (EBE)',
                                    year]
            ratios['Ratio de capacité de remboursement'] = num / denom

            # 'Ratio d\'endettement net (Gearing)'
            num = filtered_df.loc['Dette', year]
            denom = filtered_df.loc['Capitaux propre', year]
            ratios['Ratio d\'endettement net (Gearing)'] = num / denom

            # 'Ratio de liquidité générale'
            num = filtered_df.loc['Actifs Circulants (ou Actifs Courants)', year]
            denom = filtered_df.loc['Dette CT (Dette Court Terme)', year]
            ratios['Ratio de liquidité générale'] = num / denom

            # 'Ratio de couverture des intérêts'
            num = filtered_df.loc['Bénéfice Avant Intérêts et Impôts (EBIT)',
                                  year]
            denom = filtered_df.loc['Charges Financières', year]
            ratios['Ratio de couverture des intérêts'] = num / denom

            # 'Marge opérationelle'
            num = filtered_df.loc['Bénéfice Avant Intérêts et Impôts (EBIT)',
                                  year]
            denom = filtered_df.loc['Chiffre d\'Affaires (CA)', year]
            ratios['Marge opérationelle'] = num / denom

            # 'Ratio de rentabilité des actifs'
            num = filtered_df.loc['Résultat Net', year]
            denom = filtered_df.loc['Total Bilan', year]
            ratios['Ratio de rentabilité des actifs'] = num / denom

            # 'Ratio de rentabilité des capitaux propres'
            num = filtered_df.loc['Résultat Net', year]
            denom = filtered_df.loc['Capitaux propre', year]
            ratios['Ratio de rentabilité des capitaux propres'] = num / denom

            # 'Free cash flow indicator'
            num = filtered_df.loc['Free Cash Flow (FCF)', year]
            denom = filtered_df.loc['Dette', year]
            ratios['Free cash flow indicator'] = num / denom

            # 'Charges de l\'entreprise'
            num = filtered_df.loc['Charges Financières', year]
            denom = filtered_df.loc['Chiffre d\'Affaires (CA)', year]
            ratios['Charges de l\'entreprise'] = num / denom

            for ratio in ratios:
                points, weights = get_points_weights(ratio, ratios[ratio])
                ratios[ratio] = {
                    'value': ratios[ratio],
                    'points': points,
                    'weight': weights
                }
                # Calculate the sumproduct (SOMMEPROD)
                if points is not None and weights is not None:
                    sumproduct += points * weights

            return ratios, sumproduct

        else:
            return f"Year {year} not found in data."
    except Exception as e:
        return f"Error : {e}"


def get_points_weights(ratio, ratio_value):
    try:
        # Read the weights CSV file
        weights_df = pd.read_csv("data/weights.csv", index_col=0, header=None)

        # Initialize default points and weights
        points = None
        weights = None

        # Get the weights for the given ratio
        if ratio in weights_df.index:
            weights = weights_df.loc[ratio].values[0]

        # Specific handling for 'Ratio d'autonomie financière'
        if ratio == "Ratio d'autonomie financière":
            points = get_ratio_auto_fin(ratio_value)
        elif ratio == "Ratio de capacité de remboursement":
            points = get_ratio_points_capacite_remboursement(ratio_value)
        elif ratio == "Ratio d'endettement net (Gearing)":
            points = get_ratio_points_endettement_net(ratio_value)
        elif ratio == "Ratio de liquidité générale":
            points = get_ratio_points_liquidite_generale(ratio_value)
        elif ratio == "Ratio de couverture des intérêts":
            points = get_ratio_points_couverture_interets(ratio_value)
        elif ratio == "Marge opérationelle":
            points = get_ratio_points_marge_operationelle(ratio_value)
        elif ratio == "Ratio de rentabilité des actifs":
            points = get_ratio_points_rentabilite_actifs(ratio_value)
        elif ratio == "Ratio de rentabilité des capitaux propres":
            points = get_ratio_points_rentabilite_capitaux_propres(ratio_value)
        elif ratio == "Free cash flow indicator":
            points = get_ratio_points_free_cash_flow_indicator(ratio_value)
        elif ratio == "Charges de l'entreprise":
            points = get_ratio_points_charges_entreprise(ratio_value)

        return points, weights

    except Exception as e:
        return f"Error: {e}"


def get_ratio_auto_fin(value):
    if value < -1:
        return 350
    elif value < 0.05:
        return 300
    elif value < 0.1:
        return 250
    elif value < 0.2:
        return 200
    elif value < 0.3:
        return 150
    elif value < 0.4:
        return 100
    return 50


def get_ratio_points_capacite_remboursement(value):
    if value < 0.5:
        return 50
    elif value < 1:
        return 100
    elif value < 2:
        return 150
    elif value < 3:
        return 200
    elif value < 4:
        return 250
    elif value < 40:
        return 300
    return 350


def get_ratio_points_endettement_net(value):
    if value < 1:
        return 50
    elif value < 3:
        return 100
    elif value < 5:
        return 150
    elif value < 7:
        return 200
    elif value < 9:
        return 250
    elif value < 20:
        return 300
    return 350


def get_ratio_points_liquidite_generale(value):
    if value > 2:
        return 50
    elif value > 1.5:
        return 100
    elif value > 1:
        return 150
    elif value > 0.5:
        return 200
    elif value > 0.2:
        return 250
    elif value > -1:
        return 300
    return 350


def get_ratio_points_couverture_interets(value):
    if value > 15:
        return 50
    elif value > 10:
        return 100
    elif value > 6:
        return 150
    elif value > 3:
        return 200
    elif value > 2:
        return 250
    elif value > -50:
        return 300
    return 350


def get_ratio_points_marge_operationelle(value):
    if value > 0.1:
        return 50
    elif value > 0.08:
        return 100
    elif value > 0.05:
        return 150
    elif value > 0.03:
        return 200
    elif value > 0.01:
        return 250
    elif value > -1:
        return 300
    return 350


def get_ratio_points_rentabilite_actifs(value):
    if value > 0.1:
        return 50
    elif value > 0.05:
        return 100
    elif value > 0.03:
        return 150
    elif value > 0.01:
        return 200
    elif value > 0.008:
        return 250
    elif value > -1:
        return 300
    return 350


def get_ratio_points_rentabilite_capitaux_propres(value):
    if value > 0.35:
        return 50
    elif value > 0.25:
        return 100
    elif value > 0.15:
        return 150
    elif value > 0.05:
        return 200
    elif value > 0.03:
        return 250
    elif value > -1:
        return 300
    return 350


def get_ratio_points_free_cash_flow_indicator(value):
    if value > 0.3:
        return 50
    elif value > 0.2:
        return 100
    elif value > 0.1:
        return 150
    elif value > 0.05:
        return 200
    elif value > 0.03:
        return 250
    elif value > -1:
        return 300
    return 350


def get_ratio_points_charges_entreprise(value):
    if value < 0.01:
        return 50
    elif value < 0.02:
        return 100
    elif value < 0.03:
        return 150
    elif value < 0.04:
        return 200
    elif value < 0.1:
        return 250
    elif value < -1:
        return 300
    return 350


def get_qual_indics(company, year, risk):
    try:
        sector_risk = 10
        risk_weights = {
            'A1': 25,
            'A2': 50,
            'A3': 75,
            'A4': 100,
            'B': 125,
            'C': 150,
            'D': 175,
            'E': 200,
        }

        risk_data = {
            'Year': [2022, 2021, 2020, 2019],
            'France': ['A3', 'A2', 'A3', 'A2'],
            'USA': ['A2', 'A1', 'A2', 'A1'],
            'Japan': ['A2', 'A1', 'A1', 'A1'],
        }
        df = pd.DataFrame(risk_data)
        for country in df.columns[1:]:
            df[country] = df[country].map(risk_weights)
        df = df.set_index('Year').T
        df.columns = df.columns.map(str)

        """
        Year    2022  2021  2020  2019
        France    75    50    75    50
        USA       50    25    50    25
        Japan     50    25    25    25
        """
        companies_df = pd.read_csv("data/companies.csv")
        country = companies_df[companies_df['Entreprise'].str.lower(
        ) == company.lower()]['Siège social'].values[0]
        country_risk = df.loc[country, str(year)]

        sectorial_risk_data = {
            'Risque sectoriel': ['lvmh', "oreal", 'airbus', 'boeing', 'total', 'exxon', 'ford', 'toyota'],
            '2022': [100, 100, 100, 75, 75, 50, 75, 75],
            '2021': [100, 100, 75, 75, 75, 75, 75, 75],
            '2020': [100, 100, 75, 75, 75, 75, 75, 75],
            '2019': [100, 75, 75, 75, 75, 50, 75, 75]
        }
        sector_df = pd.DataFrame(sectorial_risk_data)
        sector_df.set_index('Risque sectoriel', inplace=True)
        sector_risk = sector_df.loc[company.lower(), str(year)]

        return (country_risk, sector_risk), country_risk+sector_risk
    except Exception as e:
        return f"Error: {e}", 10


def get_mba_rating(points):
    if points < 70:
        return "A+"
    elif points < 110:
        return "A"
    elif points < 170:
        return "A-"
    elif points < 220:
        return "B+"
    elif points < 240:
        return "B"
    elif points < 270:
        return "B-"
    return "C"


def get_sp_moodys(company, year):
    # S&P data
    year = int(year)
    data_sp = {
        'Company': ['airbus', 'airbus', 'airbus', 'airbus', 'boeing', 'boeing', 'boeing', 'boeing',
                    'ford', 'ford', 'ford', 'ford', 'toyota', 'toyota', 'toyota', 'toyota',
                    'exxon', 'exxon', 'exxon', 'exxon', 
                    'total', 'total', 'total', 'total',
                    "oreal", "oreal", "oreal", "oreal"],
        'Year': [2022, 2021, 2020, 2019, 2022, 2021, 2020, 2019,
                2022, 2021, 2020, 2019, 2022, 2021, 2020, 2019,
                2022, 2021, 2020, 2019, 2022, 2021, 2020, 2019,
                2022, 2021, 2020, 2019],
        'Rating': ['A', 'A', 'A', 'N/A', 'BBB-', 'BBB', 'BBB', 'A-',
                'BB+', 'BB+', 'BB+', 'BBB-', 'A+', 'A+', 'A+', 'A+',
                'AA-', 'AA', 'AA+', 'AA+', 'A+', 'A', 'A+', 'A+',
                'AA', 'N/A', 'N/A', 'N/A']
    }

    # Moody's data
    data_moodys = {
        'Company': ['airbus', 'airbus', 'airbus', 'airbus', 'boeing', 'boeing', 'boeing', 'boeing',
                    'ford', 'ford', 'ford', 'ford', 'toyota', 'toyota', 'toyota', 'toyota',
                    'exxon', 'exxon', 'exxon', 'exxon', 'total', 'total', 'total', 'total',
                    "oreal", "oreal", "oreal", "oreal"],
        'Year': [2022, 2021, 2020, 2019, 2022, 2021, 2020, 2019,
                2022, 2021, 2020, 2019, 2022, 2021, 2020, 2019,
                2022, 2021, 2020, 2019, 2022, 2021, 2020, 2019,
                2022, 2021, 2020, 2019],
        'Rating': ['A2', 'A2', 'A2', 'N/A', 'baa2', 'baa2', 'baa2', 'A3',
                'ba1', 'ba2', 'ba2', 'ba1', 'A1', 'A1', 'A1', 'N/A',
                'Aa2', 'Aa1', 'Aa1', 'Aaa', 'A1', 'A1', 'Aa3', 'Aa3',
                'Aa1', 'N/A', 'N/A', 'N/A']
    }

    # Create dataframes and pivot them
    df_sp = pd.DataFrame(data_sp)
    df_sp_pivot = df_sp.pivot(index='Company', columns='Year', values='Rating')

    df_moodys = pd.DataFrame(data_moodys)
    df_moodys_pivot = df_moodys.pivot(index='Company', columns='Year', values='Rating')

    # Retrieve the rating for the given company and year
    sp_rate = df_sp_pivot.loc[company, year] if company in df_sp_pivot.index and year in df_sp_pivot.columns else 'N/A'
    moodys_rate = df_moodys_pivot.loc[company, year] if company in df_moodys_pivot.index and year in df_moodys_pivot.columns else 'N/A'

    return sp_rate, moodys_rate


def get_currency_and_industry(company):
    # Load industry data
    with open('data/industries.csv', 'r', newline='', encoding='utf-8') as industries_file:
        industries_reader = csv.DictReader(industries_file)
        for row in industries_reader:
            if row['Company'] == company:
                industry = row['Industry']
                break
        else:
            industry = None  # Set to None if not found

    # Load currency data
    with open('data/currencies.csv', 'r', newline='', encoding='utf-8') as currencies_file:
        currencies_reader = csv.DictReader(currencies_file)
        for row in currencies_reader:
            if row['Company'] == company:
                currency = row['Currency']
                break
        else:
            currency = None  # Set to None if not found

    return industry, currency