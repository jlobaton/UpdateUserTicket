#################################
#Desarrollado por: Jesus Lobaton
#Fecha de creación: 19/03/2025
###################################

import requests
import csv
import json
import os
import sys
from dotenv import load_dotenv  # Solo si usas .env
from pathlib import Path
from requests.auth import HTTPBasicAuth

# Agregar el directorio raíz al path de Python
sys.path.append(str(Path(__file__).parent.parent)) 

from config.settings import FORM_NAME, CUSTOM_FIELD_ID, RUT_FIELD_NAME

# Cargar variables de entorno (si usas .env)
load_dotenv(Path("config") / ".env")

# Configurar autenticación desde variables de entorno
auth = HTTPBasicAuth(
    f"{os.getenv('ZENDESK_EMAIL')}/token",
    os.getenv('ZENDESK_API_TOKEN')
)
SUBDOMAIN = os.getenv('ZENDESK_SUBDOMAIN')

def clear_screen():
    # Para Windows
    if os.name == 'nt':
        os.system('cls')
    # Para Unix/Linux/MacOS
    else:
        os.system('clear')

def get_inicio(SUBDOMAIN: str, FORM_NAME: str, RUT_FIELD_NAME: str, CUSTOM_FIELD_ID: int) -> None:
    clear_screen()
    print("\nBienvenido al Sistema de Actualización de Tickets")
    print(f"➤ Instancia configurada: {SUBDOMAIN.upper()}")
    print(f"➤ Formulario a buscar : {FORM_NAME}")
    print(f"➤ Nombre del campo de usuario : {RUT_FIELD_NAME.upper()}")
    print(f"➤ ID del campo a actualizar : {CUSTOM_FIELD_ID}")

# Buscar ID del formulario por nombre
def get_form_id(FORM_NAME):
    forms_url = f"https://{SUBDOMAIN}.zendesk.com/api/v2/ticket_forms"
    try:
        response = requests.get(forms_url, auth=auth)
        response.raise_for_status()
        forms = response.json()['ticket_forms']
        
        for form in forms:
            if form['name'].lower() == FORM_NAME.lower():
                return form['id']
        
        print(f"❌ Formulario '{FORM_NAME}' no encontrado")
        print("Formularios disponibles:")
        for form in forms:
            print(f"- {form['name']} (ID: {form['id']})")
        exit()
        
    except Exception as e:
        print(f"Error buscando formulario: {str(e)}")
        exit()

#Inicio
get_inicio(SUBDOMAIN, FORM_NAME, RUT_FIELD_NAME, CUSTOM_FIELD_ID)
form_id = get_form_id(FORM_NAME)

# Buscar tickets resueltos con este formulario
def get_resolved_tickets(form_id):
    tickets = []
    url = f"https://{SUBDOMAIN}.zendesk.com/api/v2/search.json?query=type:ticket status<solved ticket_form_id:{form_id}"
    #print(url)
    while url:
        try:
            response = requests.get(url, auth=auth)
            response.raise_for_status()
            data = response.json()
            #print(data)
            tickets.extend(data['results'])
            url = data['next_page']
        except Exception as e:
            print(f"Error buscando tickets: {str(e)}")
            break
    
    return tickets

############ Inicio del Código ############
tickets = get_resolved_tickets(form_id)
print(f"\n📝 Tickets encontrados: {len(tickets)}")
########################

#Crea un archivo de salida
def crear_archivo():
    total_tickets = len(tickets)
    procesados = 0
    
    with open('output/tickets_actualizado.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['id_ticket', 'rut', 'estatus'])

        for ticket in tickets:
            try:
                ticket_id = ticket['id']
                status = ticket['status']
                requester_id = ticket.get('requester_id')

                if not requester_id:
                    mensaje = f"⚠️ Ticket {ticket_id}: Sin solicitante asociado"
                    writer.writerow([ticket_id, 'N/A', mensaje])
                    continue

                # Obtener RUT del usuario
                user_url = f"https://{SUBDOMAIN}.zendesk.com/api/v2/users/{requester_id}.json"
                response = requests.get(user_url, auth=auth)
                response.raise_for_status()
                user_data = response.json()['user']
                rut_value = user_data.get('user_fields', {}).get(RUT_FIELD_NAME)

                if not rut_value:
                    mensaje = f"⚠️ Ticket {ticket_id}: Usuario sin RUT"
                    writer.writerow([ticket_id, 'N/A', mensaje])
                    continue

                # Actualizar ticket
                update_url = f"https://{SUBDOMAIN}.zendesk.com/api/v2/tickets/{ticket_id}.json"
                payload = {
                    "ticket": {
                        "custom_fields": [
                            {
                                "id": CUSTOM_FIELD_ID,
                                "value": rut_value.strip()
                            }
                        ]
                    }
                }

                response = requests.put(
                    update_url,
                    auth=auth,
                    headers={'Content-Type': 'application/json'},
                    data=json.dumps(payload)
                )
                response.raise_for_status()
                
                mensaje = f"✅ Ticket {ticket_id} procesado"
                writer.writerow([ticket_id, rut_value, mensaje])

            except Exception as e:
                mensaje = f"❌ Error procesando ticket {ticket_id}: {str(e)}"
                writer.writerow([ticket_id, 'ERROR', mensaje])

            finally:
                procesados += 1
                porcentaje = (procesados / total_tickets) * 100
                print(f"\rProgreso: {porcentaje:.1f}% ({procesados}/{total_tickets})", end='', flush=True)

    print("\n✅ Proceso completado. Archivo 'tickets_actualizado.csv' generado")

crear_archivo()