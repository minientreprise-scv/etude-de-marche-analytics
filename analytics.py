import csv
import datetime
import os.path

import matplotlib.pyplot as plot

age_index = 3
interested_index = 4
known_qr_index = 6
has_smartphone_index = 7
where_to_buy_index = 8
price_index = 9
plants_wanted_index = 10
email_index = 11
name_index = 12
date_index = 13


def get_average_age(rows):
    ages = []
    for row in rows:
        if row[age_index] == '':
            continue
        ages.append(int(row[age_index]))
    return sum(ages) / len(ages)


def get_average_age_interested(rows):
    ages = []
    for row in rows:
        if row[age_index] != '' and row[interested_index] == 'Oui':
            ages.append(int(row[age_index]))
    return sum(ages) / len(ages)


def get_median_age_interested(rows):
    ages = []
    for row in rows:
        if row[age_index] != '' and row[interested_index] == 'Oui':
            ages.append(int(row[age_index]))
    ages.sort()
    return ages[int(len(ages) / 2)]


def get_prices_by_percent(rows):
    prices = [row[price_index] for row in rows]
    total = len(prices)
    prices_by_number = {}
    prices_by_percent = {}
    for price in prices:
        if price == '':
            total -= 1
            continue
        if prices_by_number.get(price) is None:
            prices_by_number[price] = 1
            continue
        prices_by_number[price] += 1
    for price in prices_by_number.keys():
        prices_by_percent[price] = 100 * prices_by_number[price] / total
    return prices_by_percent


def get_places_by_percent(rows):
    places = [place for row in rows for place in row[where_to_buy_index].split(', ')]
    total = len(places)
    places_by_number = {}
    places_by_percent = {}
    for place in places:
        if place == '':
            total -= 1
            continue
        if places_by_number.get(place) is None:
            places_by_number[place] = 1
            continue
        places_by_number[place] += 1
    for place in places_by_number.keys():
        places_by_percent[place] = 100 * places_by_number[place] / total
    return places_by_percent


def get_wanted_plants_by_percent(rows):
    plants = [plant for row in rows for plant in row[plants_wanted_index].split(', ')]
    total = len(plants)
    plants_by_number = {}
    plants_by_percent = {}
    for plant in plants:
        if plant == '':
            total -= 1
            continue
        if plants_by_number.get(plant) is None:
            plants_by_number[plant] = 1
            continue
        plants_by_number[plant] += 1
    for plant in plants_by_number.keys():
        plants_by_percent[plant] = 100 * plants_by_number[plant] / total
    return plants_by_percent


def get_percentage_of_persons_who_know_qr(rows):
    number_of_person_who_know = 0
    for row in rows:
        if row[known_qr_index] == 'Oui':
            number_of_person_who_know += 1
    percentage = 100 * number_of_person_who_know / len(rows)
    stay = 100 - percentage
    return {'Oui': percentage, 'Non': stay}


def get_emails_names(rows):
    emails_names_list = []
    for row in rows:
        if row[email_index] != '' or row[name_index] != '':
            emails_names_list.append((row[email_index], row[name_index]))
    return emails_names_list


def get_age_interested(rows):
    age_interested = []
    for row in rows:
        if row[age_index] != '' and row[interested_index] != '':
            age_interested.append((row[age_index], row[interested_index]))
    age_interested.sort()
    return age_interested


def get_percentage_age_sliced_interested(rows):
    slices = [(0, 20), (20, 40), (40, 100)]
    percentage_of_slices = {f'{slice[0]} - {slice[1]} ans': [] for slice in slices}
    for part in slices:
        for row in rows:
            if row[age_index] != '' and row[interested_index] == 'Oui':
                if part[0] < int(row[age_index]) < part[1]:
                    percentage_of_slices[f'{part[0]} - {part[1]} ans'].append(int(row[age_index]))
    for slice in percentage_of_slices.keys():
        if len(percentage_of_slices[slice]) == 0:
            percentage_of_slices[slice] = 0
        else:
            percentage_of_slices[slice] = sum(percentage_of_slices[slice]) / len(percentage_of_slices[slice])
    return percentage_of_slices


def get_farthest_and_closest_dates(rows):
    dates = []
    for row in rows:
        if row[date_index] != '':
            date, hour = row[date_index].split(' ')
            year, month, day = date.split('-')
            hour, minutes = hour.split(':')
            dates.append(datetime.datetime(int(year), int(month), int(day), int(hour), int(minutes)).timestamp())
    dates.sort()
    return datetime.datetime.fromtimestamp(dates[0]).strftime('%m-%d-%y %H:%M'), datetime.datetime.fromtimestamp(dates[-1]).strftime('%m-%d-%y %H:%M')


def generate_pie_graph(datas, labels, name, title):
    explode = [0 for _ in datas]
    explode[datas.index(max(datas))] = 0.2
    plot.figure(figsize=(8, 5))
    plot.pie(datas, labels=labels,
             autopct=lambda x: str(round(x, 2)) + '%',
             pctdistance=0.7,
             labeldistance=1.4,
             explode=explode,
             shadow=True)
    plot.legend()
    plot.title(title)
    plot.savefig(f'graphs/{name}.png')


def generate_point_graph(datas, name, title, lines):
    plot.figure(figsize=(8, 5))
    fig, ax = plot.subplots(1, 1, figsize=(5, 7))
    plot.grid()
    fig.axes[0].set_yticks([i * 5 for i in range(1, 20)])
    for line in lines:
        ax.plot(['Oui', 'Non'], [line[0], line[0]], label=line[1], c=line[2])
        ax.legend()
    for data in datas:
        value = int(data[0])
        if data[1] == 'Oui':
            ax.plot(['Oui', 'Oui'], [value, value], 'o', c='g', label='Oui')
            continue
        ax.plot(['Non', 'Non'], [value, value], 'o', c='r', label='Non')

    ax.set(title=title)
    ax.set_ylabel('Âge en années')
    ax.set_xlabel('Est intéressé [Oui/Non]')
    fig.savefig(f'graphs/{name}.png')


def generate_summary(title, content, footer):
    try:
        open('graphs/Synthese.md', 'w').write(f'# {title}\n\n{content}\n\n_{footer}_')
    except:
        open('graphs/Synthese.md', 'x')
        generate_summary(title, content, footer)


if __name__ == '__main__':
    with open('tableau-resultats-etude-de-marche.csv') as file:
        rows = list(csv.reader(file))[1:-1]
        if not os.path.isdir('graphs'):
            os.mkdir('graphs')
        print('Planteqr - Étude de marché analytiques:')
        graphs = True if input('Générer des graphiques et une synthèse ?[y/n]') == 'y' else 'n'
        print(f"{len(rows)} entrées:")


        average_age = get_average_age(rows)
        average_age_interested = get_average_age_interested(rows)
        median_age_interested = get_median_age_interested(rows)

        data_period = ' au '.join(get_farthest_and_closest_dates(rows))

        prices_by_percent = get_prices_by_percent(rows)
        prices_by_percent_string = ''.join([f'\n\t- {price}: {value}%' for price, value in prices_by_percent.items()])

        places_by_percent = get_places_by_percent(rows)
        places_by_percent_string = ''.join([f'\n\t- {place}: {value}%' for place, value in places_by_percent.items()])

        wanted_plants_by_percent = get_wanted_plants_by_percent(rows)
        wanted_plants_by_percent_string = ''.join([f'\n\t- {plant}: {value}%' for plant, value in wanted_plants_by_percent.items()])

        percentage_of_persons_who_know_qr = get_percentage_of_persons_who_know_qr(rows)
        percentage_of_persons_who_know_qr_string = f"Oui: {percentage_of_persons_who_know_qr['Oui']}%, Non: {percentage_of_persons_who_know_qr['Non']}%"

        percentage_age_sliced_interested = get_percentage_age_sliced_interested(rows)
        percentage_age_sliced_interested_string = ''.join([f'\n\t- {slice}: {value}%' for slice, value in percentage_age_sliced_interested.items()])

        emails_names = get_emails_names(rows)
        emails_names_string = ''.join([f'\n\t - ' + email + ' : ' + nom for email, nom in emails_names])

        print(f"Moyenne d'âge: {average_age} ans")
        print(f"Moyenne d'âge intéressée: {average_age_interested} ans")
        print(f"Médiane d'âge intéressée: {median_age_interested} ans")
        print(f"Taux/prix voulu: {prices_by_percent_string}")
        print(f"Taux/lieu de vente voulu: {places_by_percent_string}")
        print(f"Taux/type de plante voulu: {wanted_plants_by_percent_string}")
        print(f"Connaissent le QR code: {percentage_of_persons_who_know_qr_string}")
        print(f"Tranches d'âge intéressées: {percentage_age_sliced_interested_string}")
        print(f"Email / noms récupérés: {emails_names_string}")

        if graphs:
            generate_pie_graph([prices_by_percent[key] for key in prices_by_percent.keys()], prices_by_percent.keys(), 'prix-de-vente', 'Taux de réponses à "tranche de prix"')
            generate_pie_graph([places_by_percent[key] for key in places_by_percent.keys()], places_by_percent.keys(), 'lieux-de-vente', 'Taux de réponses à "lieu d\'achat"')
            generate_pie_graph([wanted_plants_by_percent[key] for key in wanted_plants_by_percent.keys()], wanted_plants_by_percent.keys(), 'types-de-plante', 'Taux de réponses à "plante recherchée"')
            generate_pie_graph([percentage_of_persons_who_know_qr[key] for key in percentage_of_persons_who_know_qr.keys()], percentage_of_persons_who_know_qr.keys(), 'connaissent-qr', 'Taux de personnes qui savent utiliser un QR code')
            generate_pie_graph([percentage_age_sliced_interested[key] for key in percentage_age_sliced_interested.keys()], percentage_age_sliced_interested.keys(), 'tranches-interessees', 'Tranches d\'âge intéressées')
            generate_point_graph(get_age_interested(rows), 'analyses-ages', 'Analyses sur les âges.', [(average_age_interested, 'Moyenne intéressée', 'royalblue'), (median_age_interested, 'Médiane intéressée', 'orange'), (average_age, 'Moyenne d\'âge interrogée', 'lime')])


            date = datetime.datetime.now().date()
        summary = f"""
**Sur {len(rows)} réponses:**

La moyenne d'âge est de {average_age} ans.

La moyenne d'âge intéressée est de {average_age_interested} ans.

La médiane d'âge intéressée est de {median_age_interested} ans.

![Graphique du prix voulus](prix-de-vente.png)
![Graphique du lieu de vente voulus](lieux-de-vente.png)
![Graphique des types de plantes voulues](types-de-plante.png)
![Graphique du % de personnes qui connaissent les qr codes.](connaissent-qr.png)
![Graphique du % de personnes intéressées par tranches d'âge.](tranches-interessees.png)
![Graphique d'analyses sur les ages.](analyses-ages.png)
        """
        generate_summary(f'Résultats générés le {date}', summary, f'Données récoltées du {data_period}')
