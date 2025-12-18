import csv
import json

# Leer el CSV y extraer los datos
data = []
with open('onepiece_IMDb_episodes_list_1077.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append({
            'episode': int(row['Episode Number']),
            'title': row['Title'],
            'plot': row['Plot'],
            'releaseDate': row['Release Date'],
            'rating': float(row['Average Rating'])
        })

# Ordenar por rating y obtener los top 20
top_episodes = sorted(data, key=lambda x: x['rating'], reverse=True)[:20]

# Guardar en JSON
with open('static/data.json', 'w', encoding='utf-8') as f:
    json.dump(top_episodes, f, ensure_ascii=False, indent=2)

print(f"✓ Se procesaron {len(top_episodes)} episodios top")
print(f"✓ Datos guardados en static/data.json")
