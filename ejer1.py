import urllib.request 
import re, os.path

def read_url(url):
    f=urllib.request.urlopen(url)
    text = f.read()
    decod = text.decode('utf-8')
    titles = re.findall(r'<title>(.+)</title>', decod)
    links = re.findall(r'<link>(.+)</link>', decod)
    pubDates = re.findall(r'<pubDate>(.+)</pubDate>', decod)
    formatedDates = format_date(pubDates)
    return list(zip(titles,links,formatedDates))[1:]

def format_date(bad_Date):
    list_dates = []
    meses = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',
                    'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
    for date in bad_Date:
        good_date = re.match(r'.*(\d\d)\s*(.{3})\s*(\d{4}).*',date)
        mensaje = f"{good_date.group(1)}/{meses[good_date.group(2)]}/{good_date.group(3)}"
        list_dates.append(mensaje)
    return list_dates

def print_with_format(formated_list):
    for l in formated_list:
        print("Título: " + str(l[0]))
        print("Link: " + str(l[1]))
        print("Fecha: " + str(l[2]))

if __name__ == "__main__":
    url="https://sevilla.abc.es/rss/feeds/Sevilla_Sevilla.xml"
    text = read_url(url)
    print_with_format(text)

