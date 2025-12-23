"""
Módulo para gestionar localidades y buscar coincidencias por partido.

Este módulo permite buscar localidades en una lista principal y, si no se encuentra,
buscar en una lista de fallback la mejor opción del mismo partido.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class Localidad:
    """Representa una localidad con su partido y provincia."""
    nombre: str
    partido: str
    provincia: str
    
    def __repr__(self):
        return f"Localidad(nombre='{self.nombre}', partido='{self.partido}', provincia='{self.provincia}')"


class LocalidadMatcher:
    """
    Clase para buscar localidades con lógica de fallback.
    
    Permite buscar localidades en una lista principal y, si no se encuentra,
    buscar en una lista de fallback para encontrar la mejor opción del mismo partido.
    """
    
    def __init__(self, lista_principal: List[Localidad], lista_fallback: List[Localidad] = None):
        """
        Inicializa el matcher con las listas de localidades.
        
        Args:
            lista_principal: Lista de localidades principales donde se realiza la búsqueda inicial
            lista_fallback: Lista de localidades de fallback para buscar si no se encuentra en la principal
        """
        self.lista_principal = lista_principal
        self.lista_fallback = lista_fallback or []
        
        # Crear índices para búsqueda rápida
        self._crear_indices()
    
    def _crear_indices(self):
        """Crea índices para búsqueda rápida por nombre y partido."""
        # Índice por nombre de localidad (normalizado)
        self.indice_principal = {
            self._normalizar(loc.nombre): loc 
            for loc in self.lista_principal
        }
        
        self.indice_fallback = {
            self._normalizar(loc.nombre): loc 
            for loc in self.lista_fallback
        }
        
        # Índice por partido en lista principal
        self.indice_por_partido = {}
        for loc in self.lista_principal:
            partido_norm = self._normalizar(loc.partido)
            if partido_norm not in self.indice_por_partido:
                self.indice_por_partido[partido_norm] = []
            self.indice_por_partido[partido_norm].append(loc)
    
    def _normalizar(self, texto: str) -> str:
        """
        Normaliza un texto para comparación (minúsculas, sin espacios extras).
        
        Args:
            texto: Texto a normalizar
            
        Returns:
            Texto normalizado
        """
        return texto.lower().strip()
    
    def buscar_localidad(self, nombre_localidad: str) -> Optional[Localidad]:
        """
        Busca una localidad por nombre.
        
        Primero busca en la lista principal. Si no encuentra, busca en la lista
        de fallback y retorna la mejor opción del mismo partido en la lista principal.
        
        Args:
            nombre_localidad: Nombre de la localidad a buscar
            
        Returns:
            Localidad encontrada o la mejor opción de fallback, None si no se encuentra
        """
        nombre_norm = self._normalizar(nombre_localidad)
        
        # Primero buscar en la lista principal
        if nombre_norm in self.indice_principal:
            return self.indice_principal[nombre_norm]
        
        # Si no está en la principal, buscar en fallback
        if nombre_norm in self.indice_fallback:
            localidad_fallback = self.indice_fallback[nombre_norm]
            # Buscar la mejor opción del mismo partido en la lista principal
            return self._encontrar_mejor_del_partido(localidad_fallback.partido)
        
        return None
    
    def _encontrar_mejor_del_partido(self, partido: str) -> Optional[Localidad]:
        """
        Encuentra la mejor localidad del partido especificado en la lista principal.
        
        Por ahora retorna la primera localidad del partido. Esta lógica puede
        extenderse para implementar criterios de selección más sofisticados.
        
        Args:
            partido: Nombre del partido
            
        Returns:
            Primera localidad del partido en la lista principal, None si no hay ninguna
        """
        partido_norm = self._normalizar(partido)
        localidades_partido = self.indice_por_partido.get(partido_norm, [])
        
        if localidades_partido:
            # Retornar la primera localidad del partido
            # Aquí se podría implementar lógica más sofisticada para elegir la "mejor"
            return localidades_partido[0]
        
        return None
    
    def buscar_todas_del_partido(self, partido: str) -> List[Localidad]:
        """
        Retorna todas las localidades de un partido en la lista principal.
        
        Args:
            partido: Nombre del partido
            
        Returns:
            Lista de localidades del partido
        """
        partido_norm = self._normalizar(partido)
        return self.indice_por_partido.get(partido_norm, [])


def crear_localidad(nombre: str, partido: str, provincia: str) -> Localidad:
    """
    Función helper para crear una localidad.
    
    Args:
        nombre: Nombre de la localidad
        partido: Partido al que pertenece
        provincia: Provincia a la que pertenece
        
    Returns:
        Nueva instancia de Localidad
    """
    return Localidad(nombre=nombre, partido=partido, provincia=provincia)
