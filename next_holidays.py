import argparse
from datetime import date, timedelta
from collections import defaultdict
import holidays as hd

TODAY = date.today()
YEAR = TODAY.year

COUNTRY_NAMES = {
    'US': 'United States', 'CA': 'Canada', 'GB': 'United Kingdom',
    'AU': 'Australia', 'IN': 'India', 'CN': 'China', 'JP': 'Japan',
    'DE': 'Germany', 'FR': 'France', 'IT': 'Italy', 'ES': 'Spain',
    'BR': 'Brazil', 'MX': 'Mexico', 'KR': 'South Korea', 'RU': 'Russia',
    'ZA': 'South Africa', 'NL': 'Netherlands', 'BE': 'Belgium',
    'CH': 'Switzerland', 'SE': 'Sweden', 'NO': 'Norway', 'DK': 'Denmark',
    'FI': 'Finland', 'PL': 'Poland', 'PT': 'Portugal', 'IE': 'Ireland',
    'NZ': 'New Zealand', 'SG': 'Singapore', 'MY': 'Malaysia',
    'HK': 'Hong Kong', 'TW': 'Taiwan', 'AR': 'Argentina', 'AT': 'Austria',
    'CL': 'Chile', 'CO': 'Colombia', 'CZ': 'Czech Republic', 'EG': 'Egypt',
    'GR': 'Greece', 'HU': 'Hungary', 'ID': 'Indonesia', 'IL': 'Israel',
    'KE': 'Kenya', 'NG': 'Nigeria', 'PH': 'Philippines', 'RO': 'Romania',
    'SA': 'Saudi Arabia', 'TH': 'Thailand', 'TR': 'Turkey', 'UA': 'Ukraine',
    'AE': 'United Arab Emirates', 'VN': 'Vietnam', 'PK': 'Pakistan',
    'BD': 'Bangladesh',
}

SUB_NAMES = {
    'US': {
        'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas', 'AZ': 'Arizona',
        'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut',
        'DC': 'District of Columbia', 'DE': 'Delaware', 'FL': 'Florida',
        'GA': 'Georgia', 'HI': 'Hawaii', 'IA': 'Iowa', 'ID': 'Idaho',
        'IL': 'Illinois', 'IN': 'Indiana', 'KS': 'Kansas', 'KY': 'Kentucky',
        'LA': 'Louisiana', 'MA': 'Massachusetts', 'MD': 'Maryland',
        'ME': 'Maine', 'MI': 'Michigan', 'MN': 'Minnesota', 'MO': 'Missouri',
        'MS': 'Mississippi', 'MT': 'Montana', 'NC': 'North Carolina',
        'ND': 'North Dakota', 'NE': 'Nebraska', 'NH': 'New Hampshire',
        'NJ': 'New Jersey', 'NM': 'New Mexico', 'NV': 'Nevada',
        'NY': 'New York', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon',
        'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
        'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas',
        'UT': 'Utah', 'VA': 'Virginia', 'VT': 'Vermont', 'WA': 'Washington',
        'WI': 'Wisconsin', 'WV': 'West Virginia', 'WY': 'Wyoming',
    },
    'CA': {
        'AB': 'Alberta', 'BC': 'British Columbia', 'MB': 'Manitoba',
        'NB': 'New Brunswick', 'NL': 'Newfoundland and Labrador',
        'NS': 'Nova Scotia', 'NT': 'Northwest Territories',
        'NU': 'Nunavut', 'ON': 'Ontario', 'PE': 'Prince Edward Island',
        'QC': 'Quebec', 'SK': 'Saskatchewan', 'YT': 'Yukon',
    },
    'AU': {
        'ACT': 'Australian Capital Territory', 'NSW': 'New South Wales',
        'NT': 'Northern Territory', 'QLD': 'Queensland', 'SA': 'South Australia',
        'TAS': 'Tasmania', 'VIC': 'Victoria', 'WA': 'Western Australia',
    },
    'DE': {
        'BB': 'Brandenburg', 'BE': 'Berlin', 'BW': 'Baden-Württemberg',
        'BY': 'Bavaria', 'HB': 'Bremen', 'HE': 'Hesse',
        'HH': 'Hamburg', 'MV': 'Mecklenburg-Vorpommern',
        'NI': 'Lower Saxony', 'NW': 'North Rhine-Westphalia',
        'RP': 'Rhineland-Palatinate', 'SH': 'Schleswig-Holstein',
        'SL': 'Saarland', 'SN': 'Saxony', 'ST': 'Saxony-Anhalt',
        'TH': 'Thuringia',
    },
    'MY': {
        '01': 'Johor', '02': 'Kedah', '03': 'Kelantan',
        '04': 'Malacca', '05': 'Negeri Sembilan', '06': 'Pahang',
        '07': 'Penang', '08': 'Perak', '09': 'Perlis',
        '10': 'Selangor', '11': 'Terengganu', '12': 'Sabah',
        '13': 'Sarawak', '14': 'Kuala Lumpur', '15': 'Labuan',
        '16': 'Putrajaya',
    },
    'AR': {
        'A': 'Salta', 'B': 'Buenos Aires', 'C': 'Capital Federal',
        'D': 'San Luis', 'E': 'Entre Ríos', 'F': 'La Rioja',
        'G': 'Santiago del Estero', 'H': 'Chaco', 'J': 'San Juan',
        'K': 'Catamarca', 'L': 'La Pampa', 'M': 'Mendoza',
        'N': 'Misiones', 'P': 'Formosa', 'Q': 'Neuquén',
        'R': 'Río Negro', 'S': 'Santa Fe', 'T': 'Tucumán',
        'U': 'Chubut', 'V': 'Tierra del Fuego', 'W': 'Corrientes',
        'X': 'Córdoba', 'Y': 'Jujuy', 'Z': 'Santa Cruz',
    },
    'AT': {
        '1': 'Burgenland', '2': 'Carinthia', '3': 'Lower Austria',
        '4': 'Upper Austria', '5': 'Salzburg', '6': 'Styria',
        '7': 'Tyrol', '8': 'Vorarlberg', '9': 'Vienna',
    },
    'CH': {
        'AG': 'Aargau', 'AI': 'Appenzell Innerrhoden',
        'AR': 'Appenzell Ausserrhoden', 'BE': 'Bern', 'BL': 'Basel-Landschaft',
        'BS': 'Basel-Stadt', 'FR': 'Fribourg', 'GE': 'Geneva',
        'GL': 'Glarus', 'GR': 'Graubünden', 'JU': 'Jura',
        'LU': 'Lucerne', 'NE': 'Neuchâtel', 'NW': 'Nidwalden',
        'OW': 'Obwalden', 'SG': 'St. Gallen', 'SH': 'Schaffhausen',
        'SO': 'Solothurn', 'SZ': 'Schwyz', 'TG': 'Thurgau',
        'TI': 'Ticino', 'UR': 'Uri', 'VD': 'Vaud',
        'VS': 'Valais', 'ZG': 'Zug', 'ZH': 'Zürich',
    },
    'BR': {
        'AC': 'Acre', 'AL': 'Alagoas', 'AP': 'Amapá', 'AM': 'Amazonas',
        'BA': 'Bahia', 'CE': 'Ceará', 'DF': 'Distrito Federal',
        'ES': 'Espírito Santo', 'GO': 'Goiás', 'MA': 'Maranhão',
        'MT': 'Mato Grosso', 'MS': 'Mato Grosso do Sul', 'MG': 'Minas Gerais',
        'PA': 'Pará', 'PB': 'Paraíba', 'PR': 'Paraná', 'PE': 'Pernambuco',
        'PI': 'Piauí', 'RJ': 'Rio de Janeiro', 'RN': 'Rio Grande do Norte',
        'RS': 'Rio Grande do Sul', 'RO': 'Rondônia', 'RR': 'Roraima',
        'SC': 'Santa Catarina', 'SP': 'São Paulo', 'SE': 'Sergipe',
        'TO': 'Tocantins',
    },
    'MX': {
        'AGU': 'Aguascalientes', 'BCN': 'Baja California',
        'BCS': 'Baja California Sur', 'CAM': 'Campeche',
        'CHH': 'Chihuahua', 'CHP': 'Chiapas', 'CMX': 'Mexico City',
        'COA': 'Coahuila', 'COL': 'Colima', 'DUR': 'Durango',
        'GRO': 'Guerrero', 'GUA': 'Guanajuato', 'HID': 'Hidalgo',
        'JAL': 'Jalisco', 'MEX': 'State of Mexico', 'MIC': 'Michoacán',
        'MOR': 'Morelos', 'NAY': 'Nayarit', 'NLE': 'Nuevo León',
        'OAX': 'Oaxaca', 'PUE': 'Puebla', 'QUE': 'Querétaro',
        'ROO': 'Quintana Roo', 'SIN': 'Sinaloa', 'SLP': 'San Luis Potosí',
        'SON': 'Sonora', 'TAB': 'Tabasco', 'TAM': 'Tamaulipas',
        'TLA': 'Tlaxcala', 'VER': 'Veracruz', 'YUC': 'Yucatán',
        'ZAC': 'Zacatecas',
    },
}

SUB_COUNTRIES = list(SUB_NAMES.keys())

SKIP_KEYWORDS = ['day off', 'substituted from']

CAT_ORDER = [
    'public', 'government', 'bank', 'de_facto', 'armed_forces',
    'workday', 'school', 'half_day', 'optional', 'unofficial',
    'catholic', 'christian', 'orthodox', 'protestant',
    'hebrew', 'islamic', 'hindu', 'sabian', 'yazidi',
    'albanian', 'armenian', 'bosnian', 'roma', 'serbian', 'turkish', 'vlach',
]
CAT_WEIGHT = {c: i for i, c in enumerate(CAT_ORDER)}


def cat_label(cat):
    return cat


def region_label(code, subdiv=None):
    name = COUNTRY_NAMES.get(code, code)
    if subdiv:
        sub_name = SUB_NAMES.get(code, {}).get(subdiv, subdiv)
        return f"{name} ({sub_name})"
    return name


def is_valid_holiday(name):
    lower = name.lower()
    return not any(kw in lower for kw in SKIP_KEYWORDS)


def gather():
    raw = []

    for code in COUNTRY_NAMES:
        supported = hd.list_supported_countries().get(code, [])
        if code in SUB_COUNTRIES and supported:
            for sub in supported:
                try:
                    cal = hd.country_holidays(code, subdiv=sub, years=[YEAR])
                    cats = getattr(cal, 'supported_categories', ('public',))
                    for cat in cats:
                        cal = hd.country_holidays(code, subdiv=sub, years=[YEAR, YEAR + 1], categories=[cat])
                        for d, n in cal.items():
                            if d >= TODAY - timedelta(days=1) and is_valid_holiday(n):
                                raw.append((d, n, code, sub, cat))
                except Exception:
                    pass
        else:
            try:
                cal = hd.country_holidays(code, years=[YEAR])
                cats = getattr(cal, 'supported_categories', ('public',))
                for cat in cats:
                    cal = hd.country_holidays(code, years=[YEAR, YEAR + 1], categories=[cat])
                    for d, n in cal.items():
                        if d >= TODAY - timedelta(days=1) and is_valid_holiday(n):
                            raw.append((d, n, code, None, cat))
            except Exception:
                pass

    return raw


def group_consecutive(entries):
    by_key = defaultdict(list)
    for d, n, code, sub, cat in entries:
        by_key[(n, code, sub, cat)].append(d)

    result = []
    for (n, code, sub, cat), dates in by_key.items():
        dates.sort()
        ranges = []
        start = end = dates[0]
        for d in dates[1:]:
            if d == end + timedelta(days=1):
                end = d
            else:
                ranges.append((start, end))
                start = end = d
        ranges.append((start, end))
        for s, e in ranges:
            result.append((s, e, n, code, sub, cat))

    result.sort(key=lambda x: x[0])
    return result


def fmt_holiday(start, end, name, code, sub, cat):
    region = region_label(code, sub)
    tag = f"[{cat_label(cat)}]"
    if start == end:
        return f"{name} {tag} - {region} - {start}"
    return f"{name} {tag} - {region} - {start}<->{end}"


def main():
    parser = argparse.ArgumentParser(description='Show upcoming holidays worldwide')
    parser.add_argument('-n', type=int, default=20, help='Number of upcoming holidays to show (default: 20)')
    parser.add_argument('-T', action='store_true', help='Output as CSV')
    args = parser.parse_args()

    raw = gather()

    # Dedup by (date, name, code, sub) keeping most significant category
    best = {}
    for d, n, code, sub, cat in raw:
        key = (d, n, code, sub)
        if key not in best or CAT_WEIGHT.get(cat, 99) < CAT_WEIGHT.get(best[key][4], 99):
            best[key] = (d, n, code, sub, cat)
    raw = list(best.values())

    grouped = group_consecutive(raw)

    seen = set()
    deduped = []
    for s, e, n, code, sub, cat in grouped:
        key = (s, n, code, sub)
        if key not in seen:
            seen.add(key)
            deduped.append((s, e, n, code, sub, cat))

    deduped.sort(key=lambda x: x[0])

    count = args.n

    if args.T:
        import csv
        import sys
        writer = csv.writer(sys.stdout)
        writer.writerow(['holiday', 'category', 'start', 'end', 'country', 'subdivision'])
        printed = 0
        for s, e, n, code, sub, cat in deduped:
            if s >= TODAY:
                writer.writerow([n, cat, str(s), str(e), code, sub or ''])
                printed += 1
                if printed >= count:
                    break
        return

    print(f"Today: {TODAY}\n")
    print(f"Next {count} holidays:\n")
    printed = 0
    for s, e, n, code, sub, cat in deduped:
        if s >= TODAY:
            print(fmt_holiday(s, e, n, code, sub, cat))
            printed += 1
            if printed >= count:
                break


if __name__ == '__main__':
    main()
