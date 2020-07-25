"""Contains classes for consolidacion app listings"""

class ConsolidacionList():
    """Consolidacion listing classs"""
    def __init__(self, id, cedula, placa, fecha, motivo, sede, motivo_id, sede_id):
        self.id = id
        self.cedula = cedula
        self.placa = placa
        self.fecha = fecha
        self.motivo = motivo
        self.sede = sede
        self.motivo_id = motivo_id
        self.sede_id = sede_id
