import csv
import json
from datetime import datetime

# Leer el CSV y extraer los datos
data = []
with open('onepiece_IMDb_episodes_list_1077.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            episode_num = int(row['Episode Number'])
            rating = float(row['Average Rating'])
            
            # Parsear fecha
            date_str = row['Release Date'].strip()
            # Convertir fecha como "Wed, Oct 20, 1999"
            date_obj = datetime.strptime(date_str, "%a, %b %d, %Y")
            year = date_obj.year
            
            data.append({
                'episode': episode_num,
                'title': row['Title'].strip(),
                'plot': row['Plot'].strip(),
                'releaseDate': date_str,
                'releaseYear': year,
                'rating': rating
            })
        except:
            continue

# Ordenar por rating y obtener los top 20
top_episodes = sorted(data, key=lambda x: x['rating'], reverse=True)[:20]

# Episodios peores calificados
worst_episodes = sorted(data, key=lambda x: x['rating'])[:10]

# Episodios por año
episodes_by_year = {}
for ep in data:
    year = ep['releaseYear']
    if year not in episodes_by_year:
        episodes_by_year[year] = {
            'count': 0,
            'total_rating': 0,
            'episodes': []
        }
    episodes_by_year[year]['count'] += 1
    episodes_by_year[year]['total_rating'] += ep['rating']
    episodes_by_year[year]['episodes'].append(ep)

# Calcular promedio por año
year_stats = []
for year in sorted(episodes_by_year.keys()):
    avg_rating = episodes_by_year[year]['total_rating'] / episodes_by_year[year]['count']
    year_stats.append({
        'year': year,
        'count': episodes_by_year[year]['count'],
        'avgRating': round(avg_rating, 2),
        'episodes': episodes_by_year[year]['episodes']
    })

# Todos los datos completos
all_data = sorted(data, key=lambda x: x['episode'])

# Estadísticas generales
stats = {
    'totalEpisodes': len(data),
    'averageRating': round(sum(ep['rating'] for ep in data) / len(data), 2),
    'highestRated': max(data, key=lambda x: x['rating']),
    'lowestRated': min(data, key=lambda x: x['rating']),
    'yearsSpan': f"{min(ep['releaseYear'] for ep in data)} - {max(ep['releaseYear'] for ep in data)}"
}

# Guardar todos los JSONs
with open('static/top_episodes.json', 'w', encoding='utf-8') as f:
    json.dump(top_episodes, f, ensure_ascii=False, indent=2)

with open('static/worst_episodes.json', 'w', encoding='utf-8') as f:
    json.dump(worst_episodes, f, ensure_ascii=False, indent=2)

with open('static/year_stats.json', 'w', encoding='utf-8') as f:
    json.dump(year_stats, f, ensure_ascii=False, indent=2)

with open('static/all_episodes.json', 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)

with open('static/stats.json', 'w', encoding='utf-8') as f:
    json.dump(stats, f, ensure_ascii=False, indent=2)

print(f"✓ Total de episodios: {len(data)}")
print(f"✓ Top 20 episodios guardados")
print(f"✓ Peores 10 episodios guardados")
print(f"✓ Estadísticas por año guardadas")
print(f"✓ Todos los episodios guardados")
print(f"✓ Estadísticas generales guardadas")
print(f"\n📊 Rango temporal: {stats['yearsSpan']}")
print(f"⭐ Calificación promedio: {stats['averageRating']}/10")
print(f"🏆 Mejor: {stats['highestRated']['title']} ({stats['highestRated']['rating']}/10)")
