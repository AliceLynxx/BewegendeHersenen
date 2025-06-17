"""
BewegendeHersenen - fMRI-achtige animaties van numpy arrays

Een eenvoudige Python library voor het maken van matplotlib animaties 
die lijken op functional MRI hersenscans.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.image import imread
from typing import Optional, Union
import warnings
import os


class BewegendHersenAnimatie:
    """
    Hoofdklasse voor het maken van fMRI-achtige animaties van numpy arrays.
    
    Deze klasse biedt eenvoudige functionaliteit om 3D numpy arrays 
    (width, height, time_frames) om te zetten naar animaties die lijken 
    op functional MRI hersenscans, met optionele hersenachtergrond overlay.
    """
    
    def __init__(self, colormap: str = 'hot', interval: int = 100, 
                 background_image: Optional[str] = None, overlay_alpha: float = 0.7):
        """
        Initialiseer BewegendHersenAnimatie.
        
        Args:
            colormap (str): Matplotlib colormap voor brain-like visualisatie
                          Aanbevolen: 'hot', 'plasma', 'inferno', 'viridis'
            interval (int): Tijd tussen frames in milliseconden
            background_image (str, optional): Pad naar hersenachtergrond afbeelding
            overlay_alpha (float): Transparantie van fMRI data overlay (0.0-1.0)
        """
        self.colormap = colormap
        self.interval = interval
        self.background_image_path = background_image
        self.overlay_alpha = overlay_alpha
        self.data = None
        self.background_data = None
        self.fig = None
        self.ax = None
        self.im = None
        self.background_im = None
        self.animation = None
        
        # Valideer overlay_alpha
        if not 0.0 <= overlay_alpha <= 1.0:
            raise ValueError(f"overlay_alpha moet tussen 0.0 en 1.0 zijn, kreeg {overlay_alpha}")
        
        # Laad achtergrond als pad is opgegeven
        if background_image:
            self.load_background(background_image)
        
    def load_data(self, numpy_array: np.ndarray) -> None:
        """
        Laad numpy array data voor animatie.
        
        Args:
            numpy_array (np.ndarray): 3D array met shape (width, height, time_frames)
                                    of (height, width, time_frames)
        
        Raises:
            ValueError: Als input niet een 3D numpy array is
            ValueError: Als array leeg is of ongeldige dimensies heeft
        """
        if not isinstance(numpy_array, np.ndarray):
            raise ValueError("Input moet een numpy array zijn")
            
        if numpy_array.ndim != 3:
            raise ValueError(f"Input moet een 3D array zijn, kreeg {numpy_array.ndim}D array")
            
        if numpy_array.size == 0:
            raise ValueError("Input array is leeg")
            
        if numpy_array.shape[2] < 2:
            raise ValueError("Minimaal 2 tijdframes nodig voor animatie")
            
        self.data = numpy_array
        print(f"Data geladen: {numpy_array.shape[0]}x{numpy_array.shape[1]} pixels, "
              f"{numpy_array.shape[2]} tijdframes")
    
    def load_background(self, image_path: str) -> None:
        """
        Laad hersenachtergrond afbeelding.
        
        Args:
            image_path (str): Pad naar achtergrond afbeelding (PNG, JPG, JPEG)
            
        Raises:
            FileNotFoundError: Als bestand niet bestaat
            ValueError: Als bestandsformaat niet ondersteund wordt
            RuntimeError: Als afbeelding niet geladen kan worden
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Achtergrond afbeelding niet gevonden: {image_path}")
        
        # Controleer bestandsextensie
        valid_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif'}
        file_ext = os.path.splitext(image_path)[1].lower()
        
        if file_ext not in valid_extensions:
            raise ValueError(f"Niet ondersteund bestandsformaat: {file_ext}. "
                           f"Ondersteunde formaten: {', '.join(valid_extensions)}")
        
        try:
            # Laad afbeelding
            background_img = imread(image_path)
            
            # Converteer naar grijswaarden als het een kleurafbeelding is
            if background_img.ndim == 3:
                if background_img.shape[2] == 4:  # RGBA
                    # Gebruik alpha channel voor transparantie, converteer naar grijswaarden
                    background_img = np.dot(background_img[...,:3], [0.2989, 0.5870, 0.1140])
                elif background_img.shape[2] == 3:  # RGB
                    # Converteer naar grijswaarden
                    background_img = np.dot(background_img, [0.2989, 0.5870, 0.1140])
            
            # Normaliseer naar 0-1 range
            if background_img.max() > 1.0:
                background_img = background_img / 255.0
            
            self.background_data = background_img
            self.background_image_path = image_path
            
            print(f"Achtergrond geladen: {background_img.shape[0]}x{background_img.shape[1]} pixels")
            print(f"Intensiteit range: {background_img.min():.3f} - {background_img.max():.3f}")
            
        except Exception as e:
            raise RuntimeError(f"Kon achtergrond afbeelding niet laden: {e}")
    
    def _scale_background_to_data(self) -> np.ndarray:
        """
        Schaal achtergrond afbeelding naar data dimensies.
        
        Returns:
            np.ndarray: Geschaalde achtergrond data
            
        Raises:
            RuntimeError: Als geen data of achtergrond geladen is
        """
        if self.data is None:
            raise RuntimeError("Geen fMRI data geladen. Gebruik eerst load_data()")
        
        if self.background_data is None:
            raise RuntimeError("Geen achtergrond geladen. Gebruik eerst load_background()")
        
        target_height, target_width = self.data.shape[:2]
        
        # Als dimensies al overeenkomen, return origineel
        if self.background_data.shape == (target_height, target_width):
            return self.background_data
        
        # Gebruik matplotlib's resize functionaliteit via imshow interpolatie
        from scipy import ndimage
        
        # Bereken schaalfactoren
        scale_y = target_height / self.background_data.shape[0]
        scale_x = target_width / self.background_data.shape[1]
        
        # Schaal de achtergrond
        scaled_background = ndimage.zoom(self.background_data, (scale_y, scale_x), order=1)
        
        print(f"Achtergrond geschaald van {self.background_data.shape} naar {scaled_background.shape}")
        
        return scaled_background
    
    def _validate_input(self, data: np.ndarray) -> bool:
        """
        Private methode voor input validatie.
        
        Args:
            data (np.ndarray): Te valideren data
            
        Returns:
            bool: True als data geldig is
        """
        return (isinstance(data, np.ndarray) and 
                data.ndim == 3 and 
                data.size > 0 and 
                data.shape[2] >= 2)
    
    def create_animation(self, output_path: Optional[str] = None, 
                        figsize: tuple = (8, 6),
                        dpi: int = 100,
                        show_colorbar: bool = True,
                        title: str = "fMRI-achtige Hersenactiviteit") -> animation.FuncAnimation:
        """
        Genereer fMRI-achtige animatie van de geladen data met optionele achtergrond.
        
        Args:
            output_path (str, optional): Pad om animatie op te slaan als GIF/MP4
            figsize (tuple): Figuur grootte (width, height) in inches
            dpi (int): Resolutie voor opgeslagen animatie
            show_colorbar (bool): Toon colorbar naast animatie
            title (str): Titel voor de animatie
            
        Returns:
            matplotlib.animation.FuncAnimation: Animatie object
            
        Raises:
            RuntimeError: Als geen data is geladen
        """
        if self.data is None:
            raise RuntimeError("Geen data geladen. Gebruik eerst load_data()")
            
        # Setup figuur en axes
        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.ax.set_title(title, fontsize=14, fontweight='bold')
        self.ax.set_xlabel('X-positie')
        self.ax.set_ylabel('Y-positie')
        
        # Bepaal kleurschaal range voor consistente visualisatie
        vmin, vmax = self.data.min(), self.data.max()
        
        # Als er een achtergrond is, toon deze eerst
        if self.background_data is not None:
            try:
                scaled_background = self._scale_background_to_data()
                
                # Toon achtergrond in grijswaarden
                self.background_im = self.ax.imshow(scaled_background, 
                                                  cmap='gray',
                                                  aspect='equal',
                                                  interpolation='bilinear',
                                                  alpha=1.0)  # Achtergrond volledig ondoorzichtig
                
                print(f"Achtergrond toegevoegd met overlay transparantie: {self.overlay_alpha}")
                
            except Exception as e:
                warnings.warn(f"Kon achtergrond niet toevoegen: {e}. Gebruik normale visualisatie.")
                self.background_data = None
        
        # Initiële fMRI data frame (als overlay of standalone)
        self.im = self.ax.imshow(self.data[:, :, 0], 
                                cmap=self.colormap,
                                vmin=vmin, vmax=vmax,
                                aspect='equal',
                                interpolation='bilinear',
                                alpha=self.overlay_alpha if self.background_data is not None else 1.0)
        
        # Colorbar toevoegen (alleen voor fMRI data)
        if show_colorbar:
            cbar = plt.colorbar(self.im, ax=self.ax)
            cbar.set_label('Activiteit Intensiteit', rotation=270, labelpad=20)
        
        # Animatie functie
        def animate(frame):
            """Update functie voor animatie frames."""
            self.im.set_array(self.data[:, :, frame])
            
            # Update titel met frame informatie
            frame_title = f"{title} - Frame {frame + 1}/{self.data.shape[2]}"
            if self.background_data is not None:
                frame_title += f" (Overlay α={self.overlay_alpha})"
            
            self.ax.set_title(frame_title)
            
            return [self.im] + ([self.background_im] if self.background_im else [])
        
        # Maak animatie
        self.animation = animation.FuncAnimation(
            self.fig, animate, 
            frames=self.data.shape[2],
            interval=self.interval,
            blit=True,
            repeat=True
        )
        
        # Opslaan als GIF/MP4 indien gewenst
        if output_path:
            print(f"Animatie wordt opgeslagen naar: {output_path}")
            try:
                if output_path.lower().endswith('.gif'):
                    self.animation.save(output_path, writer='pillow', fps=1000/self.interval, dpi=dpi)
                elif output_path.lower().endswith('.mp4'):
                    self.animation.save(output_path, writer='ffmpeg', fps=1000/self.interval, dpi=dpi)
                else:
                    # Default naar GIF
                    output_path += '.gif'
                    self.animation.save(output_path, writer='pillow', fps=1000/self.interval, dpi=dpi)
                print(f"Animatie succesvol opgeslagen!")
            except Exception as e:
                warnings.warn(f"Kon animatie niet opslaan: {e}")
        
        return self.animation
    
    def show(self) -> None:
        """
        Toon de animatie in een matplotlib venster.
        
        Raises:
            RuntimeError: Als geen animatie is gemaakt
        """
        if self.animation is None:
            raise RuntimeError("Geen animatie gemaakt. Gebruik eerst create_animation()")
            
        plt.show()
    
    def get_frame(self, frame_index: int) -> np.ndarray:
        """
        Krijg een specifieke frame uit de data.
        
        Args:
            frame_index (int): Index van gewenste frame
            
        Returns:
            np.ndarray: 2D array van specifieke frame
            
        Raises:
            RuntimeError: Als geen data is geladen
            IndexError: Als frame_index buiten bereik is
        """
        if self.data is None:
            raise RuntimeError("Geen data geladen. Gebruik eerst load_data()")
            
        if frame_index < 0 or frame_index >= self.data.shape[2]:
            raise IndexError(f"Frame index {frame_index} buiten bereik (0-{self.data.shape[2]-1})")
            
        return self.data[:, :, frame_index]


# Convenience functies voor snelle animaties
def maak_snelle_animatie(numpy_array: np.ndarray, 
                        output_path: Optional[str] = None,
                        colormap: str = 'hot',
                        interval: int = 100) -> animation.FuncAnimation:
    """
    Convenience functie voor het snel maken van een fMRI-achtige animatie.
    
    Args:
        numpy_array (np.ndarray): 3D array met hersendata
        output_path (str, optional): Pad om animatie op te slaan
        colormap (str): Matplotlib colormap
        interval (int): Tijd tussen frames in ms
        
    Returns:
        matplotlib.animation.FuncAnimation: Animatie object
    """
    animatie = BewegendHersenAnimatie(colormap=colormap, interval=interval)
    animatie.load_data(numpy_array)
    return animatie.create_animation(output_path=output_path)


def maak_animatie_met_achtergrond(numpy_array: np.ndarray, 
                                 background_path: str,
                                 output_path: Optional[str] = None,
                                 overlay_alpha: float = 0.7,
                                 colormap: str = 'hot',
                                 interval: int = 100) -> animation.FuncAnimation:
    """
    Convenience functie voor het maken van een fMRI animatie met hersenachtergrond.
    
    Args:
        numpy_array (np.ndarray): 3D array met fMRI hersendata
        background_path (str): Pad naar hersenachtergrond afbeelding
        output_path (str, optional): Pad om animatie op te slaan
        overlay_alpha (float): Transparantie van fMRI overlay (0.0-1.0)
        colormap (str): Matplotlib colormap voor fMRI data
        interval (int): Tijd tussen frames in ms
        
    Returns:
        matplotlib.animation.FuncAnimation: Animatie object
        
    Raises:
        FileNotFoundError: Als achtergrond afbeelding niet bestaat
        ValueError: Als overlay_alpha niet tussen 0.0 en 1.0 ligt
    """
    animatie = BewegendHersenAnimatie(
        colormap=colormap, 
        interval=interval,
        background_image=background_path,
        overlay_alpha=overlay_alpha
    )
    animatie.load_data(numpy_array)
    return animatie.create_animation(output_path=output_path)