from django.db import models

class TallConceptosOperaciones(models.Model):
    concepto = models.CharField(primary_key=True, max_length=2)
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    bloqueado = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'tall_conceptos_operaciones'

class TercerosActividadEconomica(models.Model):
    codigo = models.CharField(primary_key=True, max_length=4)
    descripcion = models.CharField(max_length=400)

    class Meta:
        managed = False
        db_table = 'Terceros_actividad_economica'
    
class CondicionesPago(models.Model):
    condicion = models.CharField(max_length=4)
    descripcion = models.CharField(max_length=40)
    dias_vcto = models.SmallIntegerField()
    hasta_dias_1 = models.SmallIntegerField()
    dcto_1 = models.FloatField()
    hasta_dias_2 = models.SmallIntegerField()
    dcto_2 = models.FloatField()
    hasta_dias_3 = models.SmallIntegerField()
    dcto_3 = models.FloatField()
    hasta_dias_4 = models.SmallIntegerField()
    dcto_4 = models.FloatField()
    exportado = models.CharField(max_length=1, blank=True, null=True)
    es_contado = models.CharField(max_length=1, blank=True, null=True)
    descuento_pie = models.FloatField(blank=True, null=True)
    id = models.AutoField(unique=True, primary_key=True)
    dias_gracia = models.SmallIntegerField(blank=True, null=True)
    estado = models.BooleanField(blank=True, null=True)
    inactiva = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'condiciones_pago'

class Referencias(models.Model):
    codigo = models.CharField(max_length=20, primary_key=True)
    descripcion = models.CharField(max_length=80, blank=True, null=True)
    codigo_oferta = models.CharField(max_length=1, blank=True, null=True)
    generico = models.ForeignKey('ReferenciasGen', models.DO_NOTHING, db_column='generico')
    clase = models.ForeignKey('ReferenciasCla', models.DO_NOTHING, db_column='clase')
    contable = models.ForeignKey('ReferenciasCon', models.DO_NOTHING, db_column='contable')
    grupo = models.ForeignKey('ReferenciasSub3', models.DO_NOTHING, db_column='grupo', related_name='ReferenciasSub3Q')
    subgrupo = models.ForeignKey('ReferenciasSub3', models.DO_NOTHING, db_column='subgrupo', related_name='ReferenciasSub3W')
    nit = models.ForeignKey('Terceros', models.DO_NOTHING, db_column='nit')
    valor_unitario = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    porcentaje_iva = models.FloatField(blank=True, null=True)
    costo_unitario = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    maneja_inventario = models.BooleanField()
    und_1 = models.CharField(max_length=4, blank=True, null=True)
    can_1 = models.FloatField(blank=True, null=True)
    und_2 = models.CharField(max_length=4, blank=True, null=True)
    can_2 = models.FloatField(blank=True, null=True)
    und_3 = models.CharField(max_length=4, blank=True, null=True)
    can_3 = models.FloatField(blank=True, null=True)
    und_vta = models.SmallIntegerField(blank=True, null=True)
    und_com = models.SmallIntegerField(blank=True, null=True)
    impoconsumo = models.FloatField(blank=True, null=True)
    valor_und1 = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    valor_und2 = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    valor_und3 = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    conversion = models.FloatField(blank=True, null=True)
    otro_impuesto = models.FloatField(blank=True, null=True)
    minimo_iva = models.FloatField(blank=True, null=True)
    minimo_iva_c = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    precio_marcado = models.CharField(max_length=1, blank=True, null=True)
    factor_compra = models.FloatField(blank=True, null=True)
    factor_venta_1 = models.FloatField(blank=True, null=True)
    factor_venta_2 = models.FloatField(blank=True, null=True)
    factor_venta_3 = models.FloatField(blank=True, null=True)
    factor_venta_4 = models.FloatField(blank=True, null=True)
    factor_venta_5 = models.FloatField(blank=True, null=True)
    factor_venta_6 = models.FloatField(blank=True, null=True)
    factor_venta_7 = models.FloatField(blank=True, null=True)
    factor_venta_8 = models.FloatField(blank=True, null=True)
    factor_venta_9 = models.FloatField(blank=True, null=True)
    factor_venta_10 = models.FloatField(blank=True, null=True)
    fec_cambio_precio = models.DateTimeField(blank=True, null=True)
    costo_anterior = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    fec_ultima_entrada = models.DateTimeField(blank=True, null=True)
    fec_ultima_salida = models.DateTimeField(blank=True, null=True)
    impoconsumo_compra = models.FloatField(blank=True, null=True)
    porcentaje_iva_compra = models.FloatField(blank=True, null=True)
    precio_si_costo_cero = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True)
    maximo_descuento = models.FloatField(blank=True, null=True)
    maneja_lotes = models.CharField(max_length=1, blank=True, null=True)
    maneja_otra_und = models.CharField(max_length=1, blank=True, null=True)
    otra_und = models.CharField(max_length=4, blank=True, null=True)
    tam_alto = models.FloatField(blank=True, null=True)
    tam_largo = models.FloatField(blank=True, null=True)
    tam_ancho = models.FloatField(blank=True, null=True)
    costo_estandar = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    reposicion = models.FloatField(blank=True, null=True)
    ref_anulada = models.CharField(max_length=1, blank=True, null=True)
    vcmto_refer = models.DateTimeField(blank=True, null=True)
    impodeporte = models.FloatField(blank=True, null=True)
    subgrupo2 = models.ForeignKey('ReferenciasSub3', models.DO_NOTHING, db_column='subgrupo2', blank=True, null=True, related_name='ReferenciasSub3E')
    subgrupo3 = models.ForeignKey('ReferenciasSub3', models.DO_NOTHING, db_column='subgrupo3', blank=True, null=True, related_name='ReferenciasSub3R')
    controlado = models.CharField(max_length=1, blank=True, null=True)
    promocion = models.CharField(max_length=1, blank=True, null=True)
    maneja_series = models.CharField(max_length=1, blank=True, null=True)
    codigo_enlace = models.CharField(max_length=20, blank=True, null=True)
    cantidad_enlace = models.FloatField(blank=True, null=True)
    usar_descto_cliente = models.CharField(max_length=1, blank=True, null=True)
    usar_dcto_vol = models.CharField(max_length=1, blank=True, null=True)
    costo_compra_emergencia = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    codigo_descuento = models.CharField(max_length=1, blank=True, null=True)
    pedir = models.CharField(max_length=1, blank=True, null=True)
    tipo_1 = models.IntegerField(blank=True, null=True)
    tipo_2 = models.IntegerField(blank=True, null=True)
    tipo_3 = models.IntegerField(blank=True, null=True)
    tipo_4 = models.IntegerField(blank=True, null=True)
    tipo_5 = models.IntegerField(blank=True, null=True)
    tipo_6 = models.IntegerField(blank=True, null=True)
    tipo_7 = models.IntegerField(blank=True, null=True)
    iva_es_costo = models.CharField(max_length=1, blank=True, null=True)
    fec_cambio_precio_vta = models.DateTimeField(blank=True, null=True)
    precio_pos = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    calificacion_abc = models.CharField(max_length=1, blank=True, null=True)
    id = models.IntegerField(unique=True)
    grupo_comision = models.CharField(max_length=10, blank=True, null=True)
    porcentaje_impoconsumo = models.FloatField(blank=True, null=True)
    no_aplica_retenciones = models.CharField(max_length=1, blank=True, null=True)
    accesorio = models.CharField(max_length=1, blank=True, null=True)
    notas = models.CharField(db_column='Notas', max_length=500, blank=True, null=True)  # Field name made lowercase.
    fecha_actualizacion = models.DateTimeField(blank=True, null=True)
    tipo_8 = models.IntegerField(blank=True, null=True)
    tipo_9 = models.IntegerField(blank=True, null=True)
    mindespacho = models.IntegerField(db_column='MinDespacho', blank=True, null=True)  # Field name made lowercase.
    restringir_pos = models.CharField(max_length=1, blank=True, null=True)
    eslubricante = models.BooleanField(db_column='esLubricante', blank=True, null=True)  # Field name made lowercase.
    espintura = models.BooleanField(db_column='EsPintura', blank=True, null=True)  # Field name made lowercase.
    esneumatico = models.BooleanField(db_column='esNeumatico', blank=True, null=True)  # Field name made lowercase.
    coddiv = models.CharField(db_column='codDIV', max_length=10, blank=True, null=True)  # Field name made lowercase.
    horas_uso = models.FloatField(blank=True, null=True)
    proveedor_unico = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'referencias'

class TallCitas(models.Model):
    id_cita = models.AutoField(primary_key=True)
    bodega = models.SmallIntegerField()
    fecha_hora_creacion = models.DateTimeField()
    estado_cita = models.CharField(max_length=1)
    fecha_hora_ini = models.DateTimeField()
    fecha_hora_fin = models.DateTimeField()
    hora = models.SmallIntegerField()
    minutos = models.SmallIntegerField()
    duracion_minutos = models.IntegerField(blank=True, null=True)
    codigo_veh = models.ForeignKey(Referencias, models.DO_NOTHING, db_column='codigo_veh', blank=True, null=True)
    placa = models.CharField(max_length=20)
    nit = models.ForeignKey('Terceros', models.DO_NOTHING, db_column='nit', blank=True, null=True)
    nombre_cliente = models.CharField(max_length=80, blank=True, null=True)
    nit_nuevo = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    nombre_encargado = models.CharField(max_length=80, blank=True, null=True)
    telefonos = models.CharField(max_length=80, blank=True, null=True)
    notas = models.CharField(max_length=400, blank=True, null=True)
    modelo_veh = models.CharField(max_length=20, blank=True, null=True)
    ano_veh = models.IntegerField(blank=True, null=True)
    fecha_hora_asistio = models.DateTimeField(blank=True, null=True)
    numero_orden_taller = models.IntegerField(blank=True, null=True)
    usuario = models.CharField(max_length=10, blank=True, null=True)
    pc = models.CharField(max_length=20, blank=True, null=True)
    modulo = models.CharField(max_length=4, blank=True, null=True)
    razon = models.CharField(max_length=4, blank=True, null=True)
    email_contacto = models.CharField(max_length=50, blank=True, null=True)
    alistamiento = models.CharField(max_length=1, blank=True, null=True)
    rotado = models.CharField(max_length=1, blank=True, null=True)
    certificado = models.CharField(max_length=2000, blank=True, null=True)
    idordentaller = models.IntegerField(db_column='idOrdenTaller', blank=True, null=True)  # Field name made lowercase.
    motivo_cita = models.CharField(max_length=5, blank=True, null=True)
    estado_confirmacion = models.CharField(max_length=5, blank=True, null=True)
    bahia = models.ForeignKey('WTallCitasBahias', models.DO_NOTHING, db_column='bahia', blank=True, null=True)
    id_tecnico_tecnico = models.IntegerField(db_column='id_tecnico_Tecnico', blank=True, null=True)  # Field name made lowercase.
    fecha_hora_ini_original = models.DateTimeField(db_column='fecha_hora_ini_Original', blank=True, null=True)  # Field name made lowercase.
    fecha_hora_fin_original = models.DateTimeField(db_column='fecha_hora_fin_Original', blank=True, null=True)  # Field name made lowercase.
    duracion_minutos_original = models.IntegerField(db_column='duracion_minutos_Original', blank=True, null=True)  # Field name made lowercase.
    hora_original = models.SmallIntegerField(db_column='hora_Original', blank=True, null=True)  # Field name made lowercase.
    minutos_original = models.SmallIntegerField(db_column='minutos_Original', blank=True, null=True)  # Field name made lowercase.
    fecha_hora_ini_original_agendado = models.DateTimeField(db_column='fecha_hora_ini_Original_Agendado', blank=True, null=True)  # Field name made lowercase.
    fecha_hora_fin_original_agendado = models.DateTimeField(db_column='fecha_hora_fin_Original_Agendado', blank=True, null=True)  # Field name made lowercase.
    duracion_minutos_original_agendado = models.IntegerField(db_column='duracion_minutos_Original_Agendado', blank=True, null=True)  # Field name made lowercase.
    hora_original_agendado = models.SmallIntegerField(db_column='hora_Original_Agendado', blank=True, null=True)  # Field name made lowercase.
    minutos_original_agendado = models.SmallIntegerField(db_column='minutos_Original_Agendado', blank=True, null=True)  # Field name made lowercase.
    puntopartido_agendado = models.CharField(db_column='puntoPartido_Agendado', max_length=5000, blank=True, null=True)  # Field name made lowercase.
    minpartido_agendado = models.CharField(db_column='MinPartido_Agendado', max_length=5000, blank=True, null=True)  # Field name made lowercase.
    fueratiempo = models.CharField(db_column='FueraTiempo', max_length=15, blank=True, null=True)  # Field name made lowercase.
    estadoreal = models.CharField(db_column='EstadoReal', max_length=15, blank=True, null=True)  # Field name made lowercase.
    listachequeo = models.CharField(db_column='ListaChequeo', max_length=400, blank=True, null=True)  # Field name made lowercase.
    numeroespacios = models.IntegerField(db_column='numeroEspacios')  # Field name made lowercase.
    facturado = models.CharField(db_column='Facturado', max_length=4)  # Field name made lowercase.
    numerocomfrimaciones = models.IntegerField(db_column='numeroComfrimaciones')  # Field name made lowercase.
    motivo_cancelacion = models.ForeignKey('WTallCitasCausasCancelacion', models.DO_NOTHING, db_column='motivo_Cancelacion', blank=True, null=True)  # Field name made lowercase.
    mail = models.CharField(max_length=45, blank=True, null=True)
    asesor = models.CharField(max_length=20, blank=True, null=True)
    w_act = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tall_citas'

class Sedesdebodegas(models.Model):
    codigo = models.CharField(max_length=10)
    descripcion = models.CharField(max_length=50)
    activo = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'SedesDeBodegas'

class Terceros(models.Model):
    nit = models.DecimalField(max_digits=18, decimal_places=0, primary_key=True)
    digito = models.SmallIntegerField(blank=True, null=True)
    nombres = models.CharField(unique=True, max_length=90, blank=True, null=True)
    direccion = models.CharField(max_length=60, blank=True, null=True)
    ciudad = models.CharField(max_length=20, blank=True, null=True)
    telefono_1 = models.CharField(max_length=15, blank=True, null=True)
    telefono_2 = models.CharField(max_length=15, blank=True, null=True)
    fax = models.CharField(max_length=15, blank=True, null=True)
    apartado_aereo = models.CharField(max_length=10, blank=True, null=True)
    tipo_identificacion = models.CharField(max_length=1, blank=True, null=True)
    pais = models.CharField(max_length=20, blank=True, null=True)
    gran_contribuyente = models.BooleanField()
    autoretenedor = models.BooleanField()
    bloqueo = models.SmallIntegerField(blank=True, null=True)
    notas = models.CharField(max_length=250, blank=True, null=True)
    lista = models.SmallIntegerField(blank=True, null=True)
    concepto_1 = models.ForeignKey('Terceros1', models.DO_NOTHING, db_column='concepto_1', blank=True, null=True)
    concepto_2 = models.ForeignKey('Terceros2', models.DO_NOTHING, db_column='concepto_2', blank=True, null=True)
    concepto_3 = models.ForeignKey('Terceros3', models.DO_NOTHING, db_column='concepto_3', blank=True, null=True)
    concepto_4 = models.ForeignKey('Terceros4', models.DO_NOTHING, db_column='concepto_4', blank=True, null=True)
    concepto_5 = models.ForeignKey('Terceros5', models.DO_NOTHING, db_column='concepto_5', blank=True, null=True)
    concepto_6 = models.ForeignKey('Terceros6', models.DO_NOTHING, db_column='concepto_6', blank=True, null=True)
    concepto_7 = models.ForeignKey('Terceros7', models.DO_NOTHING, db_column='concepto_7', blank=True, null=True)
    concepto_8 = models.ForeignKey('Terceros8', models.DO_NOTHING, db_column='concepto_8', blank=True, null=True)
    concepto_9 = models.ForeignKey('Terceros9', models.DO_NOTHING, db_column='concepto_9', blank=True, null=True)
    concepto_10 = models.ForeignKey('Terceros10', models.DO_NOTHING, db_column='concepto_10', blank=True, null=True)
    mail = models.CharField(max_length=45, blank=True, null=True)
    pos_num = models.SmallIntegerField()
    regimen = models.CharField(max_length=1, blank=True, null=True)
    cupo_credito = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    nit_real = models.DecimalField(max_digits=18, decimal_places=0)
    condicion = models.ForeignKey(CondicionesPago, models.DO_NOTHING, db_column='condicion', blank=True, null=True)
    vendedor = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    fletes = models.FloatField(blank=True, null=True)
    es_excento_iva = models.CharField(max_length=1, blank=True, null=True)
    contacto_1 = models.CharField(max_length=50, blank=True, null=True)
    contacto_2 = models.CharField(max_length=50, blank=True, null=True)
    formato_factura = models.CharField(max_length=10, blank=True, null=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True)
    formato_copias = models.SmallIntegerField(blank=True, null=True)
    tipo_factura = models.CharField(max_length=4, blank=True, null=True)
    dias_gracia = models.SmallIntegerField(blank=True, null=True)
    solo_contado = models.CharField(max_length=1, blank=True, null=True)
    descuento_fijo = models.FloatField(blank=True, null=True)
    excluir_tabla_desc = models.CharField(max_length=1, blank=True, null=True)
    centro_fijo = models.IntegerField(blank=True, null=True)
    exportado = models.CharField(max_length=1, blank=True, null=True)
    factor_o_lista = models.CharField(max_length=1, blank=True, null=True)
    codigo_ica = models.ForeignKey('TercerosIca', models.DO_NOTHING, db_column='codigo_ica', blank=True, null=True)
    descuento_fijo2 = models.FloatField(blank=True, null=True)
    y_dpto = models.CharField(max_length=5, blank=True, null=True)
    y_ciudad = models.CharField(max_length=5, blank=True, null=True)
    ean = models.CharField(max_length=20, blank=True, null=True)
    id = models.IntegerField(unique=True)
    celular = models.CharField(max_length=15, blank=True, null=True)
    id_definicion_tributaria_tipo = models.IntegerField(blank=True, null=True)
    lista2 = models.SmallIntegerField(blank=True, null=True)
    fecha_cumple_ter = models.DateTimeField(blank=True, null=True)
    fecha_cambio_razon = models.DateTimeField(blank=True, null=True)
    razon_comercial = models.CharField(max_length=60, blank=True, null=True)
    estampilla = models.FloatField(blank=True, null=True)
    timbre = models.FloatField(blank=True, null=True)
    impdeporte = models.FloatField(blank=True, null=True)
    impica = models.FloatField(blank=True, null=True)
    impconsumo = models.FloatField(blank=True, null=True)
    y_pais = models.CharField(max_length=5, blank=True, null=True)
    ext_1 = models.CharField(max_length=5, blank=True, null=True)
    codigo_alterno = models.CharField(max_length=20, blank=True, null=True)
    tipo_devolucion = models.CharField(max_length=4, blank=True, null=True)
    usuario = models.CharField(db_column='Usuario', max_length=20, blank=True, null=True)  # Field name made lowercase.
    runt = models.CharField(db_column='Runt', max_length=40, blank=True, null=True)  # Field name made lowercase.
    fecha_runt = models.DateTimeField(db_column='Fecha_Runt', blank=True, null=True)  # Field name made lowercase.
    tipo_direccion = models.SmallIntegerField(blank=True, null=True)
    departamento = models.CharField(max_length=7, blank=True, null=True)
    ciudad2 = models.CharField(max_length=7, blank=True, null=True)
    cupo_credito_vh = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    otro_descuento = models.FloatField(blank=True, null=True)
    no_regulados = models.CharField(max_length=1, blank=True, null=True)
    sincronizado = models.CharField(max_length=1)
    y_barrio = models.CharField(max_length=5, blank=True, null=True)
    estado_civil = models.CharField(max_length=1, blank=True, null=True)
    estrato = models.CharField(max_length=1, blank=True, null=True)
    paginaweb = models.CharField(max_length=80, blank=True, null=True)
    area_labora = models.CharField(max_length=50, blank=True, null=True)
    cargo = models.CharField(max_length=50, blank=True, null=True)
    ext2 = models.CharField(max_length=20, blank=True, null=True)
    celular2 = models.CharField(max_length=20, blank=True, null=True)
    email2 = models.CharField(max_length=50, blank=True, null=True)
    descuento_financiero = models.FloatField(blank=True, null=True)
    actividad_cree = models.ForeignKey('TercerosActividadesCree', models.DO_NOTHING, db_column='actividad_cree', blank=True, null=True)
    es_excento_cree_ventas = models.CharField(max_length=1, blank=True, null=True)
    codigopostal = models.CharField(db_column='codigoPostal', max_length=9, blank=True, null=True)  # Field name made lowercase.
    mail_adicional = models.CharField(max_length=250, blank=True, null=True)
    gln_cabasnet = models.CharField(db_column='GLN_Cabasnet', max_length=30, blank=True, null=True)  # Field name made lowercase.
    codigoactividadeconomica = models.ForeignKey(TercerosActividadEconomica, models.DO_NOTHING, db_column='codigoActividadEconomica', blank=True, null=True)  # Field name made lowercase.
    ftocopia_factura = models.CharField(db_column='ftoCopia_factura', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tienerut = models.CharField(db_column='tieneRUT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    sexo = models.CharField(max_length=1, blank=True, null=True)
    act_mdx = models.IntegerField(blank=True, null=True)
    fecha_modificacion = models.DateTimeField(blank=True, null=True)
    condicion1 = models.CharField(max_length=4, blank=True, null=True)
    formatoremision = models.CharField(db_column='formatoRemision', max_length=20, blank=True, null=True)  # Field name made lowercase.
    copiaremision = models.CharField(db_column='copiaRemision', max_length=1, blank=True, null=True)  # Field name made lowercase.
    es_extranet = models.CharField(max_length=1, blank=True, null=True)
    es_electronico = models.CharField(max_length=1, blank=True, null=True)
    codigopostaldir = models.CharField(db_column='CodigoPostalDir', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'terceros'

class Bodegas(models.Model):
    bodega = models.SmallIntegerField(primary_key=True)
    descripcion = models.CharField(max_length=40)
    centro = models.ForeignKey('Centros', models.DO_NOTHING, db_column='centro')
    direccion = models.CharField(max_length=80, blank=True, null=True)
    telefono = models.CharField(max_length=40, blank=True, null=True)
    texto = models.CharField(max_length=250, blank=True, null=True)
    codigo_cliente = models.CharField(max_length=20, blank=True, null=True)
    id = models.IntegerField(unique=True)
    es_punto_venta = models.BooleanField(blank=True, null=True)
    impresora = models.CharField(max_length=80, blank=True, null=True)
    id_clasificacion = models.IntegerField(blank=True, null=True)
    utilidad = models.IntegerField(db_column='Utilidad', blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(max_length=5, blank=True, null=True)
    es_bod_taller = models.BooleanField(blank=True, null=True)
    acepta_ext = models.BooleanField(db_column='Acepta_Ext', blank=True, null=True)  # Field name made lowercase.
    idsmd = models.CharField(db_column='idSMD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    es_bodega_obsoleta = models.BooleanField()
    es_almacen = models.BooleanField(blank=True, null=True)
    demostracion = models.BooleanField(blank=True, null=True)
    codigopostal = models.CharField(db_column='codigoPostal', max_length=9, blank=True, null=True)  # Field name made lowercase.
    inactiva = models.CharField(max_length=1, blank=True, null=True)
    es_bod_vehiculos = models.BooleanField(blank=True, null=True)
    cuentagarantiarenault = models.CharField(db_column='cuentaGarantiaRenault', max_length=9, blank=True, null=True)  # Field name made lowercase.
    esserviciorapido = models.BooleanField(db_column='EsServicioRapido', blank=True, null=True)  # Field name made lowercase.
    codigobir_renault = models.CharField(db_column='CodigoBIR_Renault', max_length=9, blank=True, null=True)  # Field name made lowercase.
    bac = models.IntegerField(db_column='BAC', blank=True, null=True)  # Field name made lowercase.
    principal = models.CharField(max_length=1, blank=True, null=True)
    departamento = models.CharField(max_length=5, blank=True, null=True)
    ciudad = models.CharField(max_length=5, blank=True, null=True)
    autoretenedorica = models.BooleanField(blank=True, null=True)
    idsede = models.ForeignKey(Sedesdebodegas, models.DO_NOTHING, db_column='idSede', blank=True, null=True)  # Field name made lowercase.
    envia_distrinet = models.CharField(max_length=1, blank=True, null=True)
    renault = models.SmallIntegerField(blank=True, null=True)
    cod_concesionario = models.IntegerField(blank=True, null=True)
    cod_sala = models.IntegerField(blank=True, null=True)
    es_sala_venta = models.BooleanField(blank=True, null=True)
    es_concesion = models.CharField(max_length=1, blank=True, null=True)
    usa_rental = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'bodegas'

class WTallCitasBahias(models.Model):
    bodega = models.ForeignKey(Bodegas, models.DO_NOTHING, db_column='bodega', blank=True, null=True)
    bahia = models.CharField(max_length=4)
    tipobahia = models.ForeignKey('WTallCitasTipobahia', models.DO_NOTHING, db_column='tipoBahia', blank=True, null=True)  # Field name made lowercase.
    activo = models.BooleanField(blank=True, null=True)
    es_tecnico = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'w_tall_citas_bahias'

class WTallCitasCausasCancelacion(models.Model):
    nombre = models.CharField(max_length=400, blank=True, null=True)
    activo = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'w_tall_citas_Causas_Cancelacion'

class ReferenciasGen(models.Model):
    generico = models.CharField(primary_key=True, max_length=10)
    descripcion = models.CharField(max_length=60)

    class Meta:
        managed = False
        db_table = 'referencias_gen'

class ReferenciasCla(models.Model):
    clase = models.CharField(primary_key=True, max_length=10)
    descripcion = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'referencias_cla'

class ReferenciasCon(models.Model):
    contable = models.SmallIntegerField(primary_key=True)
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    cta_iva = models.CharField(max_length=20, blank=True, null=True)
    cta_iva_compras = models.CharField(max_length=20, blank=True, null=True)
    cta_ventas = models.CharField(max_length=20, blank=True, null=True)
    cta_inventario = models.CharField(max_length=20, blank=True, null=True)
    cta_costo = models.CharField(max_length=20, blank=True, null=True)
    cta_iva_dev = models.CharField(max_length=20, blank=True, null=True)
    cta_iva_compras_dev = models.CharField(max_length=20, blank=True, null=True)
    cta_ventas_dev = models.CharField(max_length=20, blank=True, null=True)
    centro = models.IntegerField(blank=True, null=True)
    cta_inv_com = models.CharField(max_length=20, blank=True, null=True)
    cta_dev_inv_com = models.CharField(max_length=20, blank=True, null=True)
    cta_orden = models.CharField(max_length=20, blank=True, null=True)
    cta_orden_contra = models.CharField(max_length=20, blank=True, null=True)
    cta_orden_pvta_en = models.CharField(max_length=20, blank=True, null=True)
    cta_orden_c_pvta_en = models.CharField(max_length=20, blank=True, null=True)
    cta_orden_pvta_re = models.CharField(max_length=20, blank=True, null=True)
    cta_orden_c_pvta_re = models.CharField(max_length=20, blank=True, null=True)
    cta_orden_pvta_iva = models.CharField(max_length=20, blank=True, null=True)
    cta_orden_c_pvta_iva = models.CharField(max_length=20, blank=True, null=True)
    cta_otra1 = models.CharField(max_length=20, blank=True, null=True)
    cta_otra2 = models.CharField(max_length=20, blank=True, null=True)
    cta_ajuste_inflacion = models.CharField(max_length=20, blank=True, null=True)
    cta_costo_aju = models.CharField(max_length=20, blank=True, null=True)
    cta_otra3 = models.CharField(max_length=20, blank=True, null=True)
    cta_descuento = models.CharField(max_length=20, blank=True, null=True)
    activo = models.CharField(db_column='Activo', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'referencias_con'

class ReferenciasSub3(models.Model):
    grupo = models.CharField(primary_key=True, max_length=10)
    subgrupo = models.CharField(max_length=10)
    subgrupo2 = models.CharField(max_length=10)
    subgrupo3 = models.CharField(max_length=10)
    descripcion = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'referencias_sub3'
        unique_together = (('grupo', 'subgrupo', 'subgrupo2', 'subgrupo3'),)

class Terceros1(models.Model):
    concepto_1 = models.CharField(primary_key=True, max_length=5)
    descripcion = models.CharField(max_length=40, blank=True, null=True)
    exportado = models.CharField(max_length=1, blank=True, null=True)
    activo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'terceros_1'

class Terceros10(models.Model):
    concepto_10 = models.CharField(primary_key=True, max_length=5)
    descripcion = models.CharField(max_length=40, blank=True, null=True)
    exportado = models.CharField(max_length=1, blank=True, null=True)
    activo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'terceros_10'

class Terceros2(models.Model):
    concepto_2 = models.CharField(primary_key=True, max_length=5)
    descripcion = models.CharField(max_length=40, blank=True, null=True)
    exportado = models.CharField(max_length=1, blank=True, null=True)
    activo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'terceros_2'

class Terceros3(models.Model):
    concepto_3 = models.CharField(primary_key=True, max_length=5)
    descripcion = models.CharField(max_length=40, blank=True, null=True)
    exportado = models.CharField(max_length=1, blank=True, null=True)
    activo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'terceros_3'

class Terceros4(models.Model):
    concepto_4 = models.CharField(primary_key=True, max_length=5)
    descripcion = models.CharField(max_length=40, blank=True, null=True)
    exportado = models.CharField(max_length=1, blank=True, null=True)
    activo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'terceros_4'

class Terceros5(models.Model):
    concepto_5 = models.CharField(primary_key=True, max_length=5)
    descripcion = models.CharField(max_length=40, blank=True, null=True)
    exportado = models.CharField(max_length=1, blank=True, null=True)
    activo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'terceros_5'

class Terceros6(models.Model):
    concepto_6 = models.CharField(primary_key=True, max_length=5)
    descripcion = models.CharField(max_length=40, blank=True, null=True)
    exportado = models.CharField(max_length=1, blank=True, null=True)
    activo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'terceros_6'

class Terceros7(models.Model):
    concepto_7 = models.CharField(primary_key=True, max_length=5)
    descripcion = models.CharField(max_length=40, blank=True, null=True)
    exportado = models.CharField(max_length=1, blank=True, null=True)
    activo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'terceros_7'

class Terceros8(models.Model):
    concepto_8 = models.CharField(primary_key=True, max_length=5)
    descripcion = models.CharField(max_length=40, blank=True, null=True)
    exportado = models.CharField(max_length=1, blank=True, null=True)
    activo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'terceros_8'

class Terceros9(models.Model):
    concepto_9 = models.CharField(primary_key=True, max_length=5)
    descripcion = models.CharField(max_length=40, blank=True, null=True)
    exportado = models.CharField(max_length=1, blank=True, null=True)
    activo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'terceros_9'

class TercerosIca(models.Model):
    codigo_ica = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=80, blank=True, null=True)
    porcentaje = models.FloatField()

    class Meta:
        managed = False
        db_table = 'terceros_ica'

class TercerosActividadesCree(models.Model):
    actividad = models.CharField(primary_key=True, max_length=4)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    cuenta = models.CharField(max_length=20, blank=True, null=True)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    minimo_cree = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    cuenta_clientes = models.CharField(max_length=20, blank=True, null=True)
    activa = models.CharField(max_length=1)
    cuenta_credito_ventas = models.CharField(max_length=20, blank=True, null=True)
    cuenta_debito_prov = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'terceros_actividades_cree'

class WTallCitasTipobahia(models.Model):
    tipobahia = models.CharField(db_column='tipoBahia', max_length=100, blank=True, null=True)  # Field name made lowercase.
    descripcion = models.CharField(max_length=8000, blank=True, null=True)
    tipotecnico = models.ForeignKey('WTallCitasTipotecnico', models.DO_NOTHING, db_column='tipoTecnico', blank=True, null=True)  # Field name made lowercase.
    activo = models.BooleanField(blank=True, null=True)
    prioridad = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'w_tall_citas_tipoBahia'

class Centros(models.Model):
    centro = models.IntegerField()
    descripcion = models.CharField(max_length=50)
    grupo = models.ForeignKey('CentrosSubgrupos', models.DO_NOTHING, db_column='grupo', related_name='CentrosSubgruposA')
    subgrupo = models.ForeignKey('CentrosSubgrupos', models.DO_NOTHING, db_column='subgrupo', related_name='CentrosSubgruposB')
    nomina = models.CharField(max_length=1, blank=True, null=True)
    exportado = models.CharField(max_length=1, blank=True, null=True)
    id = models.AutoField(unique=True, primary_key=True)
    inactivo = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'centros'

class CentrosGrupos(models.Model):
    grupo = models.CharField(primary_key=True, max_length=10)
    descripcion = models.CharField(max_length=40, blank=True, null=True)
    exportado = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'centros_grupos'

class CentrosSubgrupos(models.Model):
    grupo = models.OneToOneField(CentrosGrupos, models.DO_NOTHING, db_column='grupo', primary_key=True)
    subgrupo = models.CharField(max_length=10)
    descripcion = models.CharField(max_length=40, blank=True, null=True)
    exportado = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'centros_subgrupos'
        unique_together = (('grupo', 'subgrupo'),)

class WTallCitasTipotecnico(models.Model):
    tipotecnico = models.CharField(db_column='tipoTecnico', max_length=100, blank=True, null=True)  # Field name made lowercase.
    activo = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'w_tall_citas_tipoTecnico'

class TallCitasAuditoria(models.Model):
    id_auditoria = models.AutoField(primary_key=True)
    id_cita = models.ForeignKey(TallCitas, models.DO_NOTHING, db_column='id_cita')
    usuario = models.CharField(max_length=10)
    pc = models.CharField(max_length=20)
    fecha_hora = models.DateTimeField()
    notas = models.CharField(max_length=400, blank=True, null=True)
    bodega = models.CharField(max_length=10, blank=True, null=True)
    bahia = models.IntegerField(db_column='Bahia', blank=True, null=True)  # Field name made lowercase.
    tecnico = models.IntegerField(db_column='Tecnico', blank=True, null=True)  # Field name made lowercase.
    nrocita_anterior = models.IntegerField(db_column='NroCita_Anterior', blank=True, null=True)  # Field name made lowercase.
    certificado = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tall_citas_auditoria'

class CrmCitas(models.Model):
    seq = models.AutoField(primary_key=True)
    nit = models.DecimalField(max_digits=18, decimal_places=0)
    contacto = models.IntegerField(blank=True, null=True)
    id_gru = models.SmallIntegerField()
    id_sub = models.SmallIntegerField()
    fecha_hora = models.DateTimeField()
    hora = models.SmallIntegerField()
    fecha_hora_cita = models.DateTimeField(blank=True, null=True)
    fecha_hora_alarma = models.DateTimeField(blank=True, null=True)
    repetir_tipo = models.CharField(max_length=1, blank=True, null=True)
    repetir_cada = models.SmallIntegerField(blank=True, null=True)
    repetir_cada2 = models.SmallIntegerField(blank=True, null=True)
    repetir_expiracion = models.DateTimeField(blank=True, null=True)
    repetir_alarma = models.CharField(max_length=1, blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)  # This field type is a guess.
    resultado = models.SmallIntegerField(blank=True, null=True)
    usuario = models.CharField(max_length=10)
    cerrada = models.CharField(max_length=1, blank=True, null=True)
    documento = models.CharField(max_length=10, blank=True, null=True)
    mail = models.CharField(max_length=45, blank=True, null=True)
    estado = models.IntegerField(db_column='Estado', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CRM_citas'

class TallCitasOperaciones(models.Model):
    id_operacion = models.AutoField(primary_key=True)
    id_cita = models.ForeignKey(TallCitas, models.DO_NOTHING, db_column='id_cita')
    codigo_operacion = models.CharField(max_length=20)
    tipo_operacion = models.CharField(max_length=1)
    cantidad = models.IntegerField()
    tiempo_minutos = models.IntegerField()
    id_tall_tempario = models.ForeignKey('TallTempario', models.DO_NOTHING, db_column='id_tall_tempario', blank=True, null=True)
    check_list = models.BooleanField(blank=True, null=True)
    cliente_campana = models.CharField(max_length=1, blank=True, null=True)
    id_camp = models.IntegerField(blank=True, null=True)
    w_act = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tall_citas_operaciones'
        unique_together = (('id_cita', 'codigo_operacion', 'tipo_operacion'),)

class TallTempario(models.Model):
    clase = models.CharField(max_length=10)
    operacion = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=70, blank=True, null=True)
    tiempo = models.FloatField(blank=True, null=True)
    iva = models.FloatField(blank=True, null=True)
    concepto = models.ForeignKey(TallConceptosOperaciones, models.DO_NOTHING, db_column='concepto', blank=True, null=True)
    bloquear = models.BooleanField()
    precio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    id = models.AutoField(unique=True, primary_key=True)
    comentario = models.CharField(max_length=1000, blank=True, null=True)
    cotizada_t = models.BooleanField(blank=True, null=True)
    escalafon = models.CharField(max_length=1, blank=True, null=True)
    operacion_garantia = models.CharField(db_column='Operacion_Garantia', max_length=20, blank=True, null=True)  # Field name made lowercase.
    espintura = models.CharField(db_column='esPintura', max_length=1, blank=True, null=True)  # Field name made lowercase.
    descripcion_garantia = models.CharField(max_length=160, blank=True, null=True)
    tiempo_mo = models.FloatField(blank=True, null=True)
    div = models.CharField(max_length=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tall_tempario'
        unique_together = (('clase', 'operacion'),)

class ReferenciasImp(models.Model):
    codigo = models.OneToOneField(Referencias, models.DO_NOTHING, db_column='codigo', primary_key=True)
    pos_arancel = models.CharField(max_length=20, blank=True, null=True)
    costo_unitario_fob = models.DecimalField(db_column='costo_unitario_FOB', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    gravamen = models.FloatField(blank=True, null=True)
    explicacion = models.CharField(max_length=800, blank=True, null=True)
    serie = models.CharField(max_length=50)
    chasis = models.CharField(max_length=50, blank=True, null=True)
    motor = models.CharField(max_length=50, blank=True, null=True)
    modelo_ano = models.SmallIntegerField(blank=True, null=True)
    tipo_motor = models.CharField(max_length=50, blank=True, null=True)
    manifiesto = models.CharField(max_length=50, blank=True, null=True)
    nit_prenda = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    nit_adicional_1 = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    nit_adicional_2 = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    nit_adicional_3 = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    horas_uso = models.IntegerField(blank=True, null=True)
    kilometraje = models.IntegerField(blank=True, null=True)
    placa = models.CharField(max_length=10, blank=True, null=True)
    fecha_fin_garantia = models.DateTimeField(blank=True, null=True)
    nit_comprador = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    comprado = models.SmallIntegerField(blank=True, null=True)
    id_modano = models.ForeignKey('VhModeloAno', models.DO_NOTHING, db_column='id_modano', blank=True, null=True)
    color = models.CharField(max_length=3, blank=True, null=True)
    fecha_manifiesto = models.DateTimeField(blank=True, null=True)
    garantia = models.CharField(max_length=20, blank=True, null=True)
    tipo_venta = models.ForeignKey('VhTiposVeh', models.DO_NOTHING, db_column='tipo_venta', blank=True, null=True)
    plan_venta = models.SmallIntegerField(blank=True, null=True)
    usado_comprado = models.SmallIntegerField(blank=True, null=True)
    usado_retomado = models.SmallIntegerField(blank=True, null=True)
    usado_consignado = models.SmallIntegerField(blank=True, null=True)
    recibido_canje = models.SmallIntegerField(blank=True, null=True)
    entregado_canje = models.SmallIntegerField(blank=True, null=True)
    vendido = models.SmallIntegerField(blank=True, null=True)
    asignacion = models.IntegerField(blank=True, null=True)
    entregado_cliente = models.BooleanField(blank=True, null=True)
    entregado_matricula = models.BooleanField(blank=True, null=True)
    reservado = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    fecha_reserva = models.DateTimeField(blank=True, null=True)
    fin_reserva = models.DateTimeField(blank=True, null=True)
    costo_alistamiento = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    costo_compra = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    fecha_venta = models.DateTimeField(blank=True, null=True)
    codigo_concesionario = models.CharField(max_length=10, blank=True, null=True)
    modelo_taller = models.CharField(max_length=10, blank=True, null=True)
    carpeta = models.CharField(max_length=30, blank=True, null=True)
    ciudad_placa = models.CharField(max_length=30, blank=True, null=True)
    otroservicio = models.CharField(db_column='OtroServicio', max_length=15, blank=True, null=True)  # Field name made lowercase.
    fecha_cambio_km = models.DateTimeField(blank=True, null=True)
    color_interno = models.CharField(db_column='Color_Interno', max_length=3, blank=True, null=True)  # Field name made lowercase.
    codigo_radio = models.CharField(db_column='Codigo_Radio', max_length=20, blank=True, null=True)  # Field name made lowercase.
    tiempo_garantia = models.SmallIntegerField(db_column='Tiempo_Garantia', blank=True, null=True)  # Field name made lowercase.
    km_garantia = models.IntegerField(db_column='Km_Garantia', blank=True, null=True)  # Field name made lowercase.
    numsoat = models.CharField(db_column='NumSOAT', max_length=30, blank=True, null=True)  # Field name made lowercase.
    fin_asignacion = models.DateTimeField(blank=True, null=True)
    levante = models.CharField(db_column='Levante', max_length=16, blank=True, null=True)  # Field name made lowercase.
    año_fab = models.IntegerField(db_column='Año_Fab', blank=True, null=True)  # Field name made lowercase.
    oferta = models.DecimalField(db_column='Oferta', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    razon_cambio_prop = models.IntegerField(db_column='Razon_Cambio_Prop', blank=True, null=True)  # Field name made lowercase.
    refrendo = models.CharField(db_column='Refrendo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    fecha_expedicion_manifiesto = models.DateTimeField(blank=True, null=True)
    fecha_obligatorio = models.DateTimeField(blank=True, null=True)
    fecha_gases = models.DateTimeField(blank=True, null=True)
    fecha_tecnico_mecanica = models.DateTimeField(blank=True, null=True)
    id_estado = models.ForeignKey('ReferenciasImpEstados', models.DO_NOTHING, db_column='id_estado', blank=True, null=True)
    pos_arancel_internacional = models.CharField(max_length=20, blank=True, null=True)
    nit_aseguradora = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    fec_vencimiento_seg = models.DateTimeField(blank=True, null=True)
    cabina = models.CharField(max_length=20, blank=True, null=True)
    nit_usuario = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    requiere_registro = models.CharField(max_length=1, blank=True, null=True)
    registro_importacion = models.CharField(max_length=20, blank=True, null=True)
    vencimiento_registro = models.DateTimeField(blank=True, null=True)
    cantidad_registro = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    costo_registro = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    moneda = models.CharField(max_length=3, blank=True, null=True)
    fecha_aprobado = models.DateTimeField(blank=True, null=True)
    puertas = models.SmallIntegerField(blank=True, null=True)
    sinlimitedekmengtia = models.CharField(db_column='sinLimiteDekmEnGtia', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ciudad_manifiesto = models.CharField(max_length=20, blank=True, null=True)
    revista = models.DecimalField(db_column='Revista', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    homologacion = models.CharField(max_length=16, blank=True, null=True)
    es_flota = models.CharField(max_length=2, blank=True, null=True)
    tipopintura = models.CharField(db_column='tipoPintura', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fecha_cambio_horas_uso = models.DateTimeField(blank=True, null=True)
    fecha_entrega = models.DateTimeField(blank=True, null=True)
    consecutivo_compra = models.IntegerField(blank=True, null=True)
    act_mdx = models.IntegerField(blank=True, null=True)
    tipo_caja = models.CharField(max_length=1, blank=True, null=True)
    linea_chevystar = models.CharField(max_length=20, blank=True, null=True)
    blindado = models.CharField(max_length=1, blank=True, null=True)
    convertido_gas = models.CharField(db_column='Convertido_gas', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'referencias_imp'
        unique_together = (('codigo', 'serie'),)

class VhModeloAno(models.Model):
    pass

class VhTiposVeh(models.Model):
    pass

class ReferenciasImpEstados(models.Model):
    pass