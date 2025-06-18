# BewegendeHersenen 🧠

Python library voor het maken van matplotlib animaties op basis van numpy arrays, speciaal ontworpen voor het visualiseren van functional MRI-achtige hersenactiviteit.

## ✨ Nieuwe Features

### 🖼️ Statische Achtergrond Ondersteuning (v1.1)
- **Automatische detectie** van `afbeelding_achtergrond.png`
- **Nieuwe convenience functie** `maak_animatie_met_statische_achtergrond()`
- **Volledige backward compatibility** - alle bestaande code blijft werken
- **Professionele resultaten** met eigen hersenachtergrond afbeeldingen

## 🎯 Doel

BewegendeHersenen maakt het mogelijk om eenvoudig animaties te maken die lijken op functional MRI beelden. De library is ontwikkeld voor neurowetenschappers, onderzoekers en studenten die hersenactiviteit willen visualiseren zonder complexe setup.

## 🚀 Installatie

### Vereisten
- Python 3.7 of hoger
- NumPy >= 1.20.0
- Matplotlib >= 3.5.0
- SciPy (voor achtergrond scaling)

### Installatie stappen

1. Clone de repository:
```bash
git clone https://github.com/AliceLynxx/BewegendeHersenen.git
cd BewegendeHersenen
```

2. Installeer de dependencies:
```bash
pip install -r requirements.txt
```

## 📖 Gebruik

### 🏃‍♂️ Snelle Start

```python
import numpy as np
from bewegende_hersenen import maak_snelle_animatie

# Genereer test data (80x80 pixels, 50 frames)
data = np.random.rand(80, 80, 50)

# Maak animatie in één regel!
animatie = maak_snelle_animatie(data, output_path="mijn_hersenen.gif")
```

### 🧠 Met Hersenachtergrond

```python
from bewegende_hersenen import maak_animatie_met_achtergrond

# Met specifieke achtergrond
animatie = maak_animatie_met_achtergrond(
    data, 
    background_path="mijn_hersenachtergrond.png",
    output_path="hersenen_met_achtergrond.gif",
    overlay_alpha=0.7
)\n```

### 🖼️ Statische Achtergrond (NIEUW!)

#### Automatische Detectie
Plaats een bestand genaamd `afbeelding_achtergrond.png` in je werkdirectory:

```python
from bewegende_hersenen import maak_animatie_met_statische_achtergrond

# Automatische detectie van afbeelding_achtergrond.png
animatie = maak_animatie_met_statische_achtergrond(
    data,
    output_path="statische_achtergrond.gif"
)
```

#### Met Expliciet Pad
```python
# Met specifiek achtergrond pad
animatie = maak_animatie_met_statische_achtergrond(
    data,
    achtergrond_pad="mijn_speciale_achtergrond.png",
    output_path="custom_achtergrond.gif",
    overlay_alpha=0.8,
    colormap='plasma'
)
```

### 🎛️ Geavanceerd Gebruik

```python
from bewegende_hersenen import BewegendHersenAnimatie

# Volledige controle over alle parameters
animatie = BewegendHersenAnimatie(
    colormap='inferno',
    interval=120,  # 120ms tussen frames
    background_image="achtergrond.png",
    overlay_alpha=0.75,
    activity_threshold=0.3  # Alleen activiteit > 0.3 tonen
)

animatie.load_data(data)
animation_obj = animatie.create_animation(
    output_path="geavanceerd.gif",
    figsize=(12, 10),
    dpi=150,
    title="Mijn fMRI Analyse"
)

# Toon animatie
animatie.show()
```

## 🎨 Colormap Opties

- **`'hot'`** - Klassiek voor hersenscans (zwart→rood→geel→wit)
- **`'plasma'`** - Modern en kleurenblind-vriendelijk (paars→roze→geel)
- **`'inferno'`** - Donker en dramatisch (zwart→paars→oranje→geel)
- **`'viridis'`** - Wetenschappelijk standaard (paars→blauw→groen→geel)

## 📁 Ondersteunde Bestandsformaten

### Achtergrond Afbeeldingen
- PNG (aanbevolen)
- JPG/JPEG
- BMP
- TIFF/TIF

### Output Animaties
- **GIF** - Universeel ondersteund, kleinere bestanden
- **MP4** - Betere compressie, professioneler (vereist ffmpeg)

## 🛠️ API Referentie

### Convenience Functies

#### `maak_snelle_animatie(numpy_array, output_path=None, colormap='hot', interval=100)`
Eenvoudigste manier om een animatie te maken.

#### `maak_animatie_met_achtergrond(numpy_array, background_path, output_path=None, overlay_alpha=0.7, colormap='hot', interval=100)`
Animatie met specifieke hersenachtergrond.

#### `maak_animatie_met_statische_achtergrond(numpy_array, achtergrond_pad=None, output_path=None, overlay_alpha=0.7, colormap='hot', interval=100)` 🆕
Animatie met statische achtergrond. Zoekt automatisch naar `afbeelding_achtergrond.png` als geen pad opgegeven.

#### `zoek_standaard_achtergrond()` 🆕
Helper functie die zoekt naar `afbeelding_achtergrond.png` in de huidige directory.

### BewegendHersenAnimatie Klasse

#### Constructor Parameters
- `colormap` (str): Matplotlib colormap
- `interval` (int): Tijd tussen frames in milliseconden
- `background_image` (str, optional): Pad naar achtergrond afbeelding
- `overlay_alpha` (float): Transparantie van fMRI overlay (0.0-1.0)
- `activity_threshold` (float, optional): Drempel voor significante activiteit

#### Methoden
- `load_data(numpy_array)`: Laad 3D numpy array (height, width, frames)
- `load_background(image_path)`: Laad hersenachtergrond afbeelding
- `create_animation(output_path=None, figsize=(8,6), dpi=100, show_colorbar=True, title="fMRI-achtige Hersenactiviteit")`: Genereer animatie
- `show()`: Toon animatie in matplotlib venster
- `get_frame(frame_index)`: Krijg specifieke frame uit data

## 🎬 Demo Script

Voer het demo script uit om alle functionaliteit te zien:

```bash
python demo.py
```

Dit genereert verschillende voorbeeldanimaties en toont:
- Basis animatie functionaliteit
- Hersenachtergrond overlays
- Geavanceerde features
- **Statische achtergrond demonstratie (NIEUW!)**
- Verschillende colormaps en export formaten

## 💡 Tips & Best Practices

### 🎨 Visualisatie
- Gebruik `overlay_alpha=0.5-0.8` voor subtiele overlays
- Gebruik `overlay_alpha=0.8-1.0` voor prominente activiteit
- Experimenteer met verschillende colormaps voor optimale visualisatie

### 🖼️ Achtergrond Afbeeldingen
- **PNG formaat** wordt aanbevolen voor beste kwaliteit
- **Hogere resolutie** (200+ DPI) voor professionele resultaten
- **Grijswaarden** werken het beste als achtergrond
- Kleurafbeeldingen worden automatisch naar grijswaarden geconverteerd

### ⚡ Performance
- Kleinere arrays (32x32) voor snelle prototyping
- Grotere arrays (128x128+) voor publicatie-kwaliteit
- Minder frames voor snellere verwerking
- Hogere DPI (150+) voor scherpe prints

### 🔬 Voor Echte fMRI Data
- Normaliseer data naar 0-1 range voor beste resultaten
- Overweeg spatiale smoothing voor ruis reductie
- Gebruik anatomische achtergronden voor context
- Test verschillende `activity_threshold` waarden

## 🔧 Troubleshooting

### Veelvoorkomende Problemen

#### "Achtergrond afbeelding niet gevonden"
```python
# Controleer of het bestand bestaat
import os
print(os.path.exists("afbeelding_achtergrond.png"))

# Of gebruik expliciete pad
animatie = maak_animatie_met_statische_achtergrond(
    data, 
    achtergrond_pad="pad/naar/mijn/achtergrond.png"
)
```

#### "Kon animatie niet opslaan"
Voor MP4 ondersteuning:
```bash
# Installeer ffmpeg
conda install ffmpeg
# of
sudo apt-get install ffmpeg  # Ubuntu/Debian
brew install ffmpeg          # macOS
```

#### "Input moet een 3D array zijn"
```python
# Zorg ervoor dat je data 3D is (height, width, frames)
print(f"Data shape: {data.shape}")
if data.ndim != 3:
    data = data.reshape(height, width, frames)
```

#### Memory Issues met Grote Arrays
```python
# Reduceer resolutie of aantal frames
data_small = data[::2, ::2, ::2]  # Halveer alle dimensies
```

## 🎯 Doelgroep

Deze library is ontwikkeld voor:
- 🔬 **Neurowetenschappers** die hersenactiviteit willen visualiseren
- 🎓 **Onderzoekers** in de cognitieve wetenschappen
- 📚 **Studenten** die leren over functional MRI
- 📊 **Data scientists** die temporele patronen willen tonen
- 🎨 **Iedereen** die geïnteresseerd is in hersenvisualisatie

## 📝 Licentie

Dit project is open source. Zie de LICENSE file voor details.

## 🤝 Bijdragen

Bijdragen zijn welkom! Open een issue of stuur een pull request.

## 📞 Contact

Voor vragen of ondersteuning, open een issue op GitHub.

---

**BewegendeHersenen** - Maak je hersendata tot leven! 🧠✨