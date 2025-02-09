import pandas as pd
import json
import hashlib

# Charger le fichier Excel
file_path = "/Users/mac/Desktop/CODE_frisedocs/organic/datafrise250208_2.xlsx"
df = pd.read_excel(file_path)

# Convertir toutes les colonnes datetime en chaînes immédiatement
for col in df.select_dtypes(include=["datetime64"]).columns:
    df[col] = df[col].astype(str)

def generate_color(extension):
    """ Génère une couleur unique basée sur l'extension du fichier. """
    if not isinstance(extension, str) or pd.isna(extension):  
        extension = "inconnu"  # Valeur par défaut pour les fichiers sans extension
    
    hash_object = hashlib.md5(extension.encode("utf-8"))
    hex_color = "#" + hash_object.hexdigest()[:2]  # Prendre les 6 premiers caractères pour une couleur hex
    return hex_color

# Initialisation des structures
nodes = []
nodes_set = set()
folder_attributes = {}

# Extraction des nœuds
for _, row in df.iterrows():
    file_id = row["Nom du fichier"]
    folder_id = row["Dossier"]
    file_type = row.get("Catégorie", "Autres")
    size_category = row.get("Catégorie de Poids_x", 1)
    extension = row.get("Extension", "")

    row_dict = row.to_dict()  # Convertir la ligne en dictionnaire (les datetime sont déjà des strings)
    
    color = generate_color(extension)  # Couleur basée sur l'extension

    if file_id not in nodes_set:
        nodes.append({"id": file_id, "type": "Fichier", "size": size_category, "color": color, "attributes": row_dict})
        nodes_set.add(file_id)

    if folder_id not in nodes_set:
        folder_attributes[folder_id] = row_dict  # Stocke les attributs du dossier
        nodes_set.add(folder_id)

# Ajouter les dossiers avec des attributs extraits du premier fichier qu'ils contiennent
for folder_id, attributes in folder_attributes.items():
    folder_type = attributes.get("Dossier", "Autres")
    size_category = attributes.get("Catégorie de Poids_x", 1)
    color = generate_color(folder_type)

    nodes.append({"id": folder_id, "type": "Dossier", "size": size_category, "color": color, "attributes": attributes})

# Générer les liens
links = [{"source": row["Dossier"], "target": row["Nom du fichier"]} for _, row in df.iterrows()]

# Création du JSON final
graph_data = {"nodes": nodes, "links": links}

# Sauvegarder en JSON en forçant la conversion des types non sérialisables
output_path = "/Users/mac/Desktop/CODE_frisedocs/organic/graph_data.json"
with open(output_path, "w") as f:
    json.dump(graph_data, f, indent=4, default=str)  # 🔥 Solution miracle ici

print(f"Fichier JSON enregistré : {output_path}")
