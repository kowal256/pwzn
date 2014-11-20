# -*- coding: utf-8 -*-

import csv
from heapq import merge as hmerge


def merge(path1, path2, out_file):
    """
    Funkcja pobiera nazwy dwóch plików z n-gramami (takie jak w poprzedmim
    zadaniu) i łączy zawartość tych plików i zapisuje do pliku w ścieżce ``out``.

    Pliki z n-gramami są posortowane względem zawartości n-grama.

    :param str path1: Ścieżka do pierwszego pliku
    :param str path2: Ścieżka do drugiego pliku
    :param str out_file:  Ścieżka wynikowa

    Testowanie tej funkcji na pełnych danych może być mało wygodne, możecie
    stworzyć inną funkcję która działa na dwóch listach/generatorach i testować
    ją.

    Naiwna implementacja polegałaby na stworzeniu dwóch słowników które
    zawierają mapowanie ngram -> ilość wystąpień i połączeniu ich.

    Lepsza implementacja ładuje jeden z plików do pamięci RAM (jako słownik
    bądź listę) a po drugim iteruje.

    Najlepsza implementacja nie wymaga ma złożoność pamięciową ``O(1)``.
    Podpowiedź: merge sort. Nie jest to trywialne zadanie, ale jest do zrobienia.
    """

    with open(path1, 'r', encoding='utf-8') as file1, open(path2, 'r', encoding='utf-8') as file2, open(out_file, 'w', encoding='utf-8') as output:
        reader1 = csv.reader(file1, dialect=csv.unix_dialect)
        reader2 = csv.reader(file2, dialect=csv.unix_dialect)
        reader_out = csv.writer(output, dialect=csv.unix_dialect)

        it = iter(hmerge(reader1, reader2))
        current = next(it)

        while True:
            try:
                nxt = next(it)
                if current[0] == nxt[0]:
                    current[1] = int(current[1]) + int(nxt[1])
                    nxt = current
                else:
                    reader_out.writerow(current)
                    current = nxt
            except StopIteration:
                reader_out.writerow(nxt)
                break


if __name__ == '__main__':

    merge(
        '/opt/pwzn/zaj3/enwiki-20140903-pages-articles_part_0.xmlascii.csv',
        '/opt/pwzn/zaj3/enwiki-20140903-pages-articles_part_1.xmlascii.csv',
        '/tmp/mergeout.csv')