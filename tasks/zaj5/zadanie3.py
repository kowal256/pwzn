# -*- coding: utf-8 -*-

from tasks.zaj5.zadanie2 import  load_data # Musi tu być żeby testy przeszły

import numpy as np


def get_event_count(data):
    """

    Dane w pliku losowane są z takiego rozkładu:
    position, velocity: każda składowa losowana z rozkładu równomiernego 0-1
    mass: losowana z rozkładu równomiernego od 1 do 100.

    Zwraca ilość zdarzeń w pliku. Każda struktura ma przypisane do którego
    wydarzenia należy. Jeśli w pliku jest wydarzenie N > 0
    to jest i wydarzenie N-1.

    :param np.ndarray data: Wynik działania zadanie2.load_data
    """

    # posortowane?
    return data[-1]['event_id']

    # albo nie
    # return np.max(data['event_id'])


def get_center_of_mass(event_id, data):
    """
    Zwraca macierz numpy zawierajacą położenie x, y i z środka masy układu.
    :param np.ndarray data: Wynik działania zadanie2.load_data
    :return: Macierz 3 x 1
    """
    return np.average(data[data['event_id'] == event_id]['particle_position'], axis=0, weights=data[data['event_id'] == event_id]['particle_mass'])


def get_energy_spectrum(event_id, data, left, right, bins):
    """
    Zwraca wartości histogramu energii kinetycznej cząstek (tak: (m*v^2)/2).
    :param np.ndarray data: Wynik działania zadanie2.load_data
    :param int left: Lewa granica histogramowania
    :param int right: Prawa granica historamowania
    :param int bins: ilość binów w historamie
    :return: macierz o rozmiarze 1 x bins

    Podpowiedż: np.histogram
    """
    d = data[data['event_id'] == event_id]
    h, e = np.histogram(d['particle_mass'] * (np.linalg.norm(d['particle_velocity'], axis=1)**2) / 2, range=(left, right), bins=bins)

    return h

if __name__ == "__main__":
    data = load_data("...")
    # print(data['velocity'])
    print(get_event_count(data))
    print(get_center_of_mass(1, data))
    print(list(get_energy_spectrum(3, data, 0, 90, 100)))