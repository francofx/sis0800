"""
Script para importar datos del CSV al sistema Django.
Ejecutar con: python manage.py shell < import_csv.py
O desde el shell de Django: exec(open('import_csv.py').read())
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema0800.settings')
django.setup()

import pandas as pd
from datetime import datetime
from consultas.models import Consulta


def parse_date(date_str):
    """Parsear fechas en diferentes formatos"""
    if pd.isna(date_str) or not date_str:
        return None
    
    date_str = str(date_str).strip()
    
    # Intentar diferentes formatos
    formats = [
        '%d/%m/%Y',
        '%m/%d/%Y',
        '%Y-%m-%d',
        '%d-%m-%Y',
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str.split()[0], fmt).date()
        except:
            continue
    
    return None


def clean_value(val):
    """Limpiar valores nulos o vacíos"""
    if pd.isna(val):
        return None
    val = str(val).strip()
    if val.lower() in ['nan', 'none', 'null', '', 'no lo aporto', 'sin dato', 'sin datos', 's/d']:
        return None
    return val


def import_csv(csv_path):
    """Importar datos del CSV"""
    print(f"Leyendo archivo: {csv_path}")
    
    # Leer CSV
    df = pd.read_csv(csv_path, encoding='utf-8')
    
    print(f"Columnas encontradas: {list(df.columns)}")
    print(f"Total de registros: {len(df)}")
    
    # Mapeo de columnas del CSV a campos del modelo
    column_mapping = {
        'FECHA': 'fecha',
        'ZONA': 'zona',
        'OPERADOR': 'operador',
        'APELLIDO Y NOMBRE INTERLOCUTOR': 'apellido_nombre_interlocutor',
        'CONSULTA': 'consulta',
        'TELÉFONO  INTERLOCUTOR': 'telefono_interlocutor',
        'TIPO DE VÍNCULO CONSULTA INDIRECTA': 'tipo_vinculo',
        'MOTIVO DE LA CONSULTA': 'motivo_consulta',
        'APELLIDO y NOMBRE USUARIO': 'apellido_nombre_usuario',
        'DNI': 'dni',
        'FECHA DE NACIMIENTO': 'fecha_nacimiento',
        'EDAD': 'edad',
        'SEXO': 'sexo',
        'NACIONALIDAD': 'nacionalidad',
        'CIUDAD': 'ciudad',
        'BARRIO': 'barrio',
        'DIRECCION': 'direccion',
        'TELEFONO': 'telefono',
        'ESCOLARIZADO': 'escolarizado',
        'ETAPA ESCOLAR': 'etapa_escolar',
        'OBRA SOCIAL': 'obra_social',
        'NOMBRE OBRA SOCIAL': 'nombre_obra_social',
        'OCUPACION ': 'ocupacion',
        'APELLIDO Y NOMBRE REFERENCIA AFECTIVA': 'apellido_nombre_referencia',
        'DNI  REFERENCIA AFECTIVA': 'dni_referencia',
        'TELEFONO  REFERENCIA AFECTIVA': 'telefono_referencia',
        'TIEMPO DE CONSUMO ': 'tiempo_consumo',
        'TIPO DE SUSTANCIA QUE CONSUME ': 'tipo_sustancia',
        'TRATAMIENTO ANTERIOR': 'tratamiento_anterior',
        'TIPO DE TRATAMIENTO ANTERIOR': 'tipo_tratamiento_anterior',
        'EFECTOR DE SALUD DE REFERENCIA': 'efector_salud_referencia',
        'RIESGO INMINENTE': 'riesgo_inminente',
        'INSTITUCION / EFECTOR DERIVADO': 'institucion_derivado',
        'SEGUIMIENTO': 'seguimiento',
        'SITUACION SOCIAL': 'situacion_social',
        'CARACTERÍSTICA JUDICIAL': 'caracteristica_judicial',
        'INTERVENCIÓN PROPUESTA': 'intervencion_propuesta',
    }
    
    created_count = 0
    error_count = 0
    
    for idx, row in df.iterrows():
        try:
            # Obtener fecha
            fecha_raw = row.get('FECHA')
            fecha = parse_date(fecha_raw)
            
            if not fecha:
                print(f"Fila {idx + 2}: Fecha inválida '{fecha_raw}', usando fecha actual")
                fecha = datetime.now().date()
            
            # Crear diccionario de datos
            data = {
                'fecha': fecha,
                'zona': clean_value(row.get('ZONA')) or 'Sur',
                'operador': clean_value(row.get('OPERADOR')) or 'Sistema',
                'apellido_nombre_interlocutor': clean_value(row.get('APELLIDO Y NOMBRE INTERLOCUTOR')) or 'No especificado',
                'consulta': clean_value(row.get('CONSULTA')) or 'Directa',
                'telefono_interlocutor': clean_value(row.get('TELÉFONO  INTERLOCUTOR')),
                'tipo_vinculo': clean_value(row.get('TIPO DE VÍNCULO CONSULTA INDIRECTA')),
                'motivo_consulta': clean_value(row.get('MOTIVO DE LA CONSULTA')) or 'Sin especificar',
                'apellido_nombre_usuario': clean_value(row.get('APELLIDO y NOMBRE USUARIO')) or 'No especificado',
                'dni': clean_value(row.get('DNI')),
                'fecha_nacimiento': clean_value(row.get('FECHA DE NACIMIENTO')),
                'edad': clean_value(row.get('EDAD')),
                'sexo': clean_value(row.get('SEXO')) or 'Hombre',
                'nacionalidad': clean_value(row.get('NACIONALIDAD')) or 'Argentina',
                'ciudad': clean_value(row.get('CIUDAD')) or 'No especificada',
                'barrio': clean_value(row.get('BARRIO')),
                'direccion': clean_value(row.get('DIRECCION')),
                'telefono': clean_value(row.get('TELEFONO')),
                'escolarizado': clean_value(row.get('ESCOLARIZADO')),
                'etapa_escolar': clean_value(row.get('ETAPA ESCOLAR')),
                'obra_social': clean_value(row.get('OBRA SOCIAL')),
                'nombre_obra_social': clean_value(row.get('NOMBRE OBRA SOCIAL')),
                'ocupacion': clean_value(row.get('OCUPACION ')),
                'apellido_nombre_referencia': clean_value(row.get('APELLIDO Y NOMBRE REFERENCIA AFECTIVA')),
                'dni_referencia': clean_value(row.get('DNI  REFERENCIA AFECTIVA')),
                'telefono_referencia': clean_value(row.get('TELEFONO  REFERENCIA AFECTIVA')),
                'tiempo_consumo': clean_value(row.get('TIEMPO DE CONSUMO ')),
                'tipo_sustancia': clean_value(row.get('TIPO DE SUSTANCIA QUE CONSUME ')),
                'tratamiento_anterior': clean_value(row.get('TRATAMIENTO ANTERIOR')),
                'tipo_tratamiento_anterior': clean_value(row.get('TIPO DE TRATAMIENTO ANTERIOR')),
                'efector_salud_referencia': clean_value(row.get('EFECTOR DE SALUD DE REFERENCIA')),
                'riesgo_inminente': clean_value(row.get('RIESGO INMINENTE')),
                'institucion_derivado': clean_value(row.get('INSTITUCION / EFECTOR DERIVADO')),
                'seguimiento': clean_value(row.get('SEGUIMIENTO')),
                'situacion_social': clean_value(row.get('SITUACION SOCIAL')),
                'caracteristica_judicial': clean_value(row.get('CARACTERÍSTICA JUDICIAL')),
                'intervencion_propuesta': clean_value(row.get('INTERVENCIÓN PROPUESTA')),
            }
            
            # Crear consulta
            consulta = Consulta.objects.create(**data)
            created_count += 1
            
            if created_count % 10 == 0:
                print(f"Importados {created_count} registros...")
                
        except Exception as e:
            error_count += 1
            print(f"Error en fila {idx + 2}: {str(e)}")
    
    print(f"\n{'='*50}")
    print(f"Importación completada!")
    print(f"Registros creados: {created_count}")
    print(f"Errores: {error_count}")
    print(f"Total en BD: {Consulta.objects.count()}")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        csv_path = sys.argv[1]
    else:
        # Ruta por defecto
        csv_path = r"C:\Users\Franco\Downloads\FORMULARIO DE CARGA DE DATOS 0800 (Respuestas) - Respuestas de formulario 1.csv"
    
    import_csv(csv_path)
