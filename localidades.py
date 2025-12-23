"""
Módulo para gestionar localidades y encontrar coincidencias basadas en partido y provincia.
"""
from typing import List, Optional, Dict
from dataclasses import dataclass
from difflib import SequenceMatcher


# Umbral mínimo de similitud para considerar una coincidencia válida
SIMILITUD_MINIMA = 0.3


@dataclass
class Localidad:
    """Representa una localidad con su partido y provincia."""
    nombre: str
    partido: str
    provincia: str
    
    def __repr__(self):
        return f"Localidad(nombre='{self.nombre}', partido='{self.partido}', provincia='{self.provincia}')"


def similitud_texto(texto1: str, texto2: str) -> float:
    """
    Calcula la similitud entre dos textos usando SequenceMatcher.
    
    Args:
        texto1: Primer texto a comparar
        texto2: Segundo texto a comparar
        
    Returns:
        float: Valor entre 0 y 1 representando la similitud (1 = idéntico)
    """
    return SequenceMatcher(None, texto1.lower(), texto2.lower()).ratio()


def encontrar_localidad(
    localidad_buscada: str,
    lista_principal: List[Localidad],
    lista_referencia: Optional[List[Localidad]] = None,
    umbral_similitud: float = SIMILITUD_MINIMA
) -> Optional[Localidad]:
    """
    Busca una localidad en la lista principal. Si no se encuentra, busca en la lista de referencia
    y retorna la mejor coincidencia de la lista principal basándose en partido y provincia.
    
    Estrategia de búsqueda:
    1. Buscar coincidencia exacta en lista_principal
    2. Si no se encuentra, buscar en lista_referencia
    3. Si se encuentra en lista_referencia, buscar en lista_principal:
       a. Primero por mismo partido (mejor similitud de nombre)
       b. Luego por misma provincia (mejor similitud de nombre)
    
    Args:
        localidad_buscada: Nombre de la localidad a buscar
        lista_principal: Lista de localidades disponibles (lista A)
        lista_referencia: Lista de localidades de referencia (lista B). Si es None, usa lista_principal
        umbral_similitud: Umbral mínimo de similitud (0.0 a 1.0) para considerar una coincidencia válida
        
    Returns:
        Localidad encontrada o None si no hay coincidencias
    """
    if lista_referencia is None:
        lista_referencia = lista_principal
    
    # 1. Buscar coincidencia exacta en lista principal
    for localidad in lista_principal:
        if localidad.nombre.lower() == localidad_buscada.lower():
            return localidad
    
    # 2. Buscar en lista de referencia para obtener partido y provincia
    localidad_ref = None
    mejor_similitud_ref = 0.0
    
    for localidad in lista_referencia:
        similitud = similitud_texto(localidad.nombre, localidad_buscada)
        if similitud > mejor_similitud_ref:
            mejor_similitud_ref = similitud
            localidad_ref = localidad
    
    # Si no se encontró ninguna referencia razonable, retornar None
    if localidad_ref is None or mejor_similitud_ref < umbral_similitud:
        return None
    
    # 3. Buscar en lista principal con mismo partido (prioridad)
    candidatos_partido = [
        loc for loc in lista_principal 
        if loc.partido.lower() == localidad_ref.partido.lower()
    ]
    
    if candidatos_partido:
        # Retornar el candidato del mismo partido con nombre más similar
        mejor_candidato = max(
            candidatos_partido,
            key=lambda loc: similitud_texto(loc.nombre, localidad_buscada)
        )
        return mejor_candidato
    
    # 4. Fallback: buscar en lista principal con misma provincia
    candidatos_provincia = [
        loc for loc in lista_principal 
        if loc.provincia.lower() == localidad_ref.provincia.lower()
    ]
    
    if candidatos_provincia:
        # Retornar el candidato de la misma provincia con nombre más similar
        mejor_candidato = max(
            candidatos_provincia,
            key=lambda loc: similitud_texto(loc.nombre, localidad_buscada)
        )
        return mejor_candidato
    
    # No se encontró ninguna coincidencia útil
    return None


def encontrar_localidad_detallado(
    localidad_buscada: str,
    lista_principal: List[Localidad],
    lista_referencia: Optional[List[Localidad]] = None,
    umbral_similitud: float = SIMILITUD_MINIMA
) -> Dict:
    """
    Versión detallada que retorna información sobre el proceso de búsqueda.
    
    Args:
        localidad_buscada: Nombre de la localidad a buscar
        lista_principal: Lista de localidades disponibles (lista A)
        lista_referencia: Lista de localidades de referencia (lista B). Si es None, usa lista_principal
        umbral_similitud: Umbral mínimo de similitud (0.0 a 1.0) para considerar una coincidencia válida
    
    Returns:
        Dict con:
            - 'encontrada': Localidad encontrada o None
            - 'metodo': Método usado ('exacta', 'partido', 'provincia', 'no_encontrada')
            - 'similitud': Valor de similitud con la búsqueda
            - 'referencia': Localidad usada como referencia en lista_referencia
    """
    if lista_referencia is None:
        lista_referencia = lista_principal
    
    resultado = {
        'encontrada': None,
        'metodo': 'no_encontrada',
        'similitud': 0.0,
        'referencia': None
    }
    
    # 1. Buscar coincidencia exacta
    for localidad in lista_principal:
        if localidad.nombre.lower() == localidad_buscada.lower():
            resultado['encontrada'] = localidad
            resultado['metodo'] = 'exacta'
            resultado['similitud'] = 1.0
            return resultado
    
    # 2. Buscar en lista de referencia
    localidad_ref = None
    mejor_similitud_ref = 0.0
    
    for localidad in lista_referencia:
        similitud = similitud_texto(localidad.nombre, localidad_buscada)
        if similitud > mejor_similitud_ref:
            mejor_similitud_ref = similitud
            localidad_ref = localidad
    
    if localidad_ref is None or mejor_similitud_ref < umbral_similitud:
        return resultado
    
    resultado['referencia'] = localidad_ref
    
    # 3. Buscar por partido
    candidatos_partido = [
        loc for loc in lista_principal 
        if loc.partido.lower() == localidad_ref.partido.lower()
    ]
    
    if candidatos_partido:
        similitudes = [(loc, similitud_texto(loc.nombre, localidad_buscada)) for loc in candidatos_partido]
        mejor_candidato, mejor_sim = max(similitudes, key=lambda x: x[1])
        resultado['encontrada'] = mejor_candidato
        resultado['metodo'] = 'partido'
        resultado['similitud'] = mejor_sim
        return resultado
    
    # 4. Buscar por provincia
    candidatos_provincia = [
        loc for loc in lista_principal 
        if loc.provincia.lower() == localidad_ref.provincia.lower()
    ]
    
    if candidatos_provincia:
        similitudes = [(loc, similitud_texto(loc.nombre, localidad_buscada)) for loc in candidatos_provincia]
        mejor_candidato, mejor_sim = max(similitudes, key=lambda x: x[1])
        resultado['encontrada'] = mejor_candidato
        resultado['metodo'] = 'provincia'
        resultado['similitud'] = mejor_sim
        return resultado
    
    return resultado
