# -*- coding: utf-8 -*-

import mmap
import struct
import numpy as np
from os.path import getsize


class InvalidFormatError(IOError):
    pass


def load_data(filename):

    """

    Funkcja ładuje dane z pliku binarnego. Plik ma następującą strukturę:

    * Nagłówek
    * Następnie struktury z danymi

    Nagłówek ma następującą strukturę:

    0. 16 "magicznych" bajtów te bajty to b'6o\xfdo\xe2\xa4C\x90\x98\xb2t!\xbeurn'
    1. 2 bajty wersji "głównej"
    2. 2 bajty wersji "pomniejszej"
    3. 2 bajty określające rozmiar pojedyńczej struktury danych
    4. 4 bajty określających ilość struktur
    5. 4 bajty określających offset między początkiem pliku a danymi
    6. Następnie mamy tyle struktur ile jest określone w nagłówku

    Struktura danych ma taką postać:

    * event_id: uint16 numer zdarzenia
    * particle_position: 3*float32 we współrzędnych kartezjańskich [m]
    * particle mass: float32 współrzędne kartezjańskie [kg]
    * particle_velocity: 3*float32 współrzędne kartezjańskie [m/s]

    Struktura i nagłówek nie mają paddingu i są zapisani little-endian!

    Ten format pliku jest kompatybilny wstecznie i do przodu w ramach wersji
    "pomniejszej". W następujący sposób:

    * Jeśli potrzebuję dodać jakieś nowe pola do nagłówka to je dodaję,
      i odpowiednio modyfikuję offset między początkiem pliku a danymi.
      Program czytający te pliki który nie jest przystosowany do pracy ze
      starszą wersją może te pola zignorować.
    * Jeśli chce dodać jakieś pola do struktury z danymi to zwiększam pole rozmiar
      jednej struktury danych i dodaje pola. Dane są dodawane do końca struktury,
      więc program czytający dane będzie wiedział że następna struktura zaczyna
      się np. 82 bajty od początku poprzedniej.

    Funkcja ta musi zgłosić wyjątek InvalidLoadError w następujących przypadkach:

    * W pliku nie zgadzają się magiczne bajty
    * Główna wersja pliku nie równa się 3
    * Rozmiar pliku jest nieodpowiedni. Tj rozmiar pliku nie wynosi:
      "offset między początkiem pliku a danymi" + "ilość struktur" * "rozmiar pojedyńczej struktury danych"


    Rada:

    * Proszę załadować nagłówek za pomocą modułu ``struct``  odczytać go,
      a następnie załadować resztę pliku (offset! za pomocą ``np.memmap``).

    Funkcja zwraca zawartość pliku w dowolnym formacie. Testy tego zadania będą
    sprawdzać czy funkcja zgłasza błędy dla niepoprawnych plików.

    W zadaniu 3 będziecie na tym pliku robić obliczenia.
    """

    with open(filename, 'r') as f:
        filesize = getsize(filename)

        if filesize == 0:
            raise InvalidFormatError('File {} is empty'.format(filename))

        mm = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)

        if mm[:16] != b'6o\xfdo\xe2\xa4C\x90\x98\xb2t!\xbeurn':
            raise InvalidFormatError('Wrong magic number')

        major, minor, struct_size, n, offset = struct.unpack_from('<HHHLL', mm, 16)

        if major != 3:
            raise InvalidFormatError('Wrong major version ({}) instead of 3'.format(major))

        if filesize != (offset + n*struct_size):
            raise InvalidFormatError('Wrong total file size: got {}, offset:{}, struct_size: {}, n: {}'.format(filesize, offset, struct_size, n))

        mm.close()

        padding = struct_size - (2+3*4+4+3*4)

        if padding < 0:
            raise InvalidFormatError('Wrong structure size (too small), got: {}, minimum: {}'.format(struct_size, (2+3*4+4+3*4)))

        if (filesize - offset) % struct_size != 0:
            raise InvalidFormatError('Size of available data ({}) is not a multiple of the data-type size {}'.format(filesize-offset, struct_size))

        dtype = np.dtype([('event_id', np.uint16),
                          ('particle_position', np.dtype('3float32')),
                          ('particle_mass', np.float32),
                          ('particle_velocity', np.dtype('3float32')),
                          ('padding', np.dtype('{}int8'.format(padding)))])

        return np.memmap(filename, dtype=dtype, mode='r', offset=offset)
