"""
BewegendeHersenen - fMRI-achtige animaties van numpy arrays

Een eenvoudige Python library voor het maken van matplotlib animaties 
die lijken op functional MRI hersenscans.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from typing import Optional, Union
import warnings


class BewegendHersenAnimatie:
    """
    Hoofdklasse voor het maken van fMRI-achtige animaties van numpy arrays.
    
    Deze klasse biedt eenvoudige functionaliteit om 3D numpy arrays 
    (width, height, time_frames) om te zetten naar animaties die lijken 
    op functional MRI hersenscans.
    """
    
    def __init__(self, colormap: str = 'hot', interval: int = 100):
        """
        Initialiseer BewegendHersenAnimatie.
        
        Args:
            colormap (str): Matplotlib colormap voor brain-like visualisatie
                          Aanbevolen: 'hot', 'plasma', 'inferno', 'viridis'
            interval (int): Tijd tussen frames in milliseconden
        """
        self.colormap = colormap
        self.interval = interval
        self.data = None
        self.fig = None
        self.ax = None
        self.im = None
        self.animation = None
        
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
        Genereer fMRI-achtige animatie van de geladen data.
        
        Args:
            output_path (str, optional): Pad om animatie op te slaan als GIF
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
        
        # Initiële frame
        self.im = self.ax.imshow(self.data[:, :, 0], 
                                cmap=self.colormap,
                                vmin=vmin, vmax=vmax,
                                aspect='equal',
                                interpolation='bilinear')
        
        # Colorbar toevoegen
        if show_colorbar:
            cbar = plt.colorbar(self.im, ax=self.ax)
            cbar.set_label('Activiteit Intensiteit', rotation=270, labelpad=20)
        
        # Animatie functie
        def animate(frame):
            """Update functie voor animatie frames."""
            self.im.set_array(self.data[:, :, frame])
            self.ax.set_title(f"{title} - Frame {frame + 1}/{self.data.shape[2]}")
            return [self.im]
        
        # Maak animatie
        self.animation = animation.FuncAnimation(
            self.fig, animate, 
            frames=self.data.shape[2],
            interval=self.interval,
            blit=True,
            repeat=True
        )
        
        # Opslaan als GIF indien gewenst
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


# Convenience functie voor snelle animaties
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