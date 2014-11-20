# -*- coding: utf-8 -*-

import numpy as np

from itertools import chain, permutations, product


def calculate_neighbours(board):

    """

    Funkcja zwraca tablicę która w polu N[R, C] zwraca ilość sąsiadów którą 
    ma komórka Board[R, C]. Za sąsiada uznajemy obszazoną komórkę po bokach lub
    na ukos od danej komórki, komórka nie jest swoim sąsiatem, zatem maksymalna
    ilość sąsiadów danej komórki wynosi 8.

    Funkcja ta powinna być zwektoryzowana, tj ilość operacji w bytekodzie
    Pythona nie powinna zależeć od rozmiaru macierzy.

    :param np.ndarray board: Dwuwymiarowa tablica zmiennych logicznych która
    obrazuje aktualny stan game of life. Jeśli w danym polu jest True (lub 1)
    oznacza to że dana komórka jest obsadzona


    Podpowiedź: Czy jest możliwe obliczenie ilości np. lewych sąsiadów
    których ma każda z komórek w macierzy, następnie liczymy ilość sąsiadów
    prawych itp.

    Podpowiedź II: Proszę uważać na komówki na bokach i rogach planszy.
    """

    def pad_zeros(vector, pad_width, iaxis, kwargs):
        vector[:pad_width[0]] = 0
        vector[-pad_width[1]:] = 0
        return vector

    padded = np.pad(board, 1, pad_zeros)

    n = np.roll(padded, 1, 0) + 0 + np.roll(padded, -1, 0) + np.roll(padded, 1, 1) + np.roll(padded, -1, 1) + np.roll(np.roll(padded, 1, 0), 1, 1) + np.roll(np.roll(padded, 1, 0), -1, 1) + np.roll(np.roll(padded, -1, 0), 1, 1) + np.roll(np.roll(padded, -1, 0), -1, 1)

    return n[1:board.shape[0]+1, 1:board.shape[1]+1]


def iterate(board):

    """

    Funkcja pobiera planszę game of life i zwraca jej następną iterację.

    Zasady Game of life są takie:

    1. Komórka może być albo żywa albo martwa.
    2. Jeśli komórka jest martwa i ma trzech sąsiadóœ to ożywa.
    3. Jeśli komórka jest żywa i ma mniej niż dwóch sąsiadów to umiera,
       jeśli ma więcej niż trzech sąsiadóœ również umiera. W przeciwnym wypadku
       (dwóch lub trzech sąsiadów) to żyje dalej.

    :param np.ndarray board: Dwuwymiarowa tablica zmiennych logicznych która
    obrazuje aktualny stan game of life. Jeśli w danym polu jest True (lub 1)
    oznacza to że dana komórka jest obsadzona

    """

    neighbours = calculate_neighbours(board)

    return np.logical_or(np.logical_and(board, np.logical_and(neighbours >= 2, neighbours <= 3)), np.logical_and(np.logical_not(board), neighbours == 3))


