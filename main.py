import datetime
import matplotlib.pyplot as plt
import numpy as np

MACD_START = 26
SIGNAL_START = MACD_START+9

#filename = "tesla.csv"
#filename = "usdpln.csv"
filename = "cdr200.csv"
#filename = "apple.csv"
#filename = "apple200.csv"
#filename = "microsoft.csv"
#filename = "microsoft200.csv"

INWESTYCJA = 1_000
parametry = ""


class Gielda:

    kupione_akcje: float
    signal_wyzej: bool

    def __init__(self):
        self.kupione_akcje = 0.0
        self.signal_wyzej = False


def wczytaj(nazwa_pliku):
    dane = np.loadtxt(nazwa_pliku, delimiter=";", dtype=[('date', 'U10'), ('value', float)])

    wartosci_m = dane['value']
    daty_m = []

    for rekord in dane['date']:
        date_obj = datetime.datetime.strptime(rekord, "%d.%m.%Y").date()
        daty_m.append(date_obj)

    daty_m = np.asarray(daty_m)
    return daty_m, wartosci_m


def ema(n, wartosci_m):
    alfa: float = 2 / (n + 1)
    m_ema = np.zeros(len(wartosci_m))
    for p_i in reversed(range(n, len(wartosci_m))):

        licznik: float = 0
        mianownik: float = 0
        pot = 0

        for i in reversed(range(p_i - n, p_i+1)):
            licznik += wartosci_m[i] * ((1 - alfa) ** pot)
            mianownik +=(1-alfa)**pot
            pot += 1

        if mianownik == 0:
            m_ema[p_i] = 0
        else:
            m_ema[p_i] = licznik / mianownik

    return m_ema


def licz_zarobek(kwota_inwest, m_macd, m_signal, kurs, m_portfel: Gielda):

    def sprzedaj(n, ilosc_akcji):
        m_portfel.kupione_akcje = 0
        return ilosc_akcji * kurs[n]

    def kup(n, kwota):
        kupione = True
        ilosc_kupionych = 0
        tmp_kwota = kwota
        while(1):
            if tmp_kwota - kurs[n] >= 0:
                ilosc_kupionych += 1
                tmp_kwota -= kurs[n]

            else:
                break

        m_portfel.kupione_akcje = ilosc_kupionych
        return -1 * ilosc_kupionych * kurs[n]

    if m_macd[SIGNAL_START] > m_signal[SIGNAL_START]:
        # signal przecial MACD od gory
        m_portfel.signal_wyzej = False
        kwota_inwest += kup(SIGNAL_START, kwota_inwest)
    else:
        # signal przecial MACD od dolu
        m_portfel.signal_wyzej = True

    for j in range(SIGNAL_START+1, len(m_macd)):
        # trzeba rozpoznac kiedy wykresy się przecinają i w tym miejscu sprzedać akcje
        print(f" {daty[j]} :  ${wartosci[j]} bank: {kwota_inwest}  akcje: {portfel.kupione_akcje}")
        if m_portfel.signal_wyzej and (m_macd[j] > m_signal[j]):
            m_portfel.signal_wyzej = False
            kwota_inwest += kup(j, kwota_inwest)
        elif (not m_portfel.signal_wyzej) and (m_signal[j] > m_macd[j]):
            m_portfel.signal_wyzej = True
            kwota_inwest += sprzedaj(j, m_portfel.kupione_akcje)

    # end
    if m_portfel.kupione_akcje:
        kwota_inwest = sprzedaj(len(wartosci) - 1, m_portfel.kupione_akcje)

    return kwota_inwest


daty, wartosci = wczytaj(filename)
name = filename.rstrip(".csv").upper()

ema12 = np.zeros(len(wartosci))
ema26 = np.zeros(len(wartosci))

macd = np.zeros(len(wartosci))
signal = np.zeros(len(wartosci))

macd[MACD_START:] = (ema(12, wartosci) - ema(26, wartosci))[MACD_START:] # jest dobrze
signal[SIGNAL_START:] = ema(9, macd)[SIGNAL_START:]

portfel = Gielda()
print("Potencjalny zarobek dla " + name + " : ",
      (licz_zarobek(INWESTYCJA, macd, signal, wartosci, portfel) - INWESTYCJA).__round__(2))

# ---------- rysowanie wykresów -----------
y = macd
z = signal
x = daty

fig, (ax1, ax2) = plt.subplots(2, sharex=True)
fig.suptitle("akcje " + name)

ax1.plot(x, y, color='tab:orange', label='macd', linewidth=1, marker=".", markeredgewidth=0.1)
ax1.plot(x, z, color='tab:cyan', label='signal', linewidth=1, marker=".", markeredgewidth=0.1)

ax1.set_xlabel('daty')
ax1.set_ylabel('macd & signal')
ax1.legend(['macd', 'signal'])

ax2.plot(x, wartosci, color='tab:blue', label='cena', linewidth=1, marker=".", markeredgewidth=0.4)
ax2.set_xlabel('daty')
ax2.set_ylabel('cena')

plt.legend()
plt.show()
