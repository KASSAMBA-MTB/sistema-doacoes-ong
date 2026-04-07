from datetime import date, timedelta
import holidays

def calcular_pascoa(ano):
    a = ano % 19
    b = ano // 100
    c = ano % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19*a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2*e + 2*i - h - k) % 7
    m = (a + 11*h + 22*l) // 451
    mes = (h + l - 7*m + 114) // 31
    dia = ((h + l - 7*m + 114) % 31) + 1
    return date(ano, mes, dia)

def gerar_eventos(ano):
    eventos = []

    br_holidays = holidays.Brazil(years=ano)

    for data, nome in br_holidays.items():
        eventos.append((nome, data, "feriado"))


    pascoa = calcular_pascoa(ano)

    eventos += [
        ("Páscoa", pascoa, "liturgico"),
        ("Cinzas", pascoa - timedelta(days=46), "liturgico"),
        ("Sexta Santa", pascoa - timedelta(days=2), "liturgico"),
        ("Pentecostes", pascoa + timedelta(days=49), "liturgico"),
        ("Corpus Christi", pascoa + timedelta(days=60), "liturgico"),
        ("Natal", date(ano, 12, 25), "liturgico"),
    ]

    return eventos