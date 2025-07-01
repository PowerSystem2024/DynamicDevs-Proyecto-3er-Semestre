from enertech.src.database.DatabaseManager import DatabaseManager
from enertech.src.domain.IndustrialAssetData import IndustrialAssetData
from enertech.src.domain.MaintenanceType import MaintenanceType
from enertech.src.domain.PriorityLevel import PriorityLevel
from enertech.src.domain.Status import Status
from enertech.src.domain.Supervisor import Supervisor
from enertech.src.domain.Technician import Technician
from enertech.src.domain.TimeUnit import TimeUnit
from enertech.src.domain.User import User
from enertech.src.domain.UserBaseData import UserBaseData
from enertech.src.domain.UserRole import UserRole
from enertech.src.domain.WorkOrderData import WorkOrderData
from enertech.src.repository.IndustrialAssetRepository import IndustrialAssetRepository
from enertech.src.repository.SupervisorRepository import SupervisorRepository
from enertech.src.repository.TechnicianRepository import TechnicianRepository
from enertech.src.repository.WorkOrderRepository import WorkOrderRepository
from enertech.src.service.IndustrialAssetService import IndustrialAssetService
from enertech.src.service.SupervisorService import SupervisorService
from enertech.src.service.TechnicianService import TechnicianService
from enertech.src.service.WorkOrderService import WorkOrderService

db_config = {
    'host': 'localhost',
    'user': 'postgres',
    'password': 'root',
    'dbname': 'enertech_db',
    'port': 5432
}
db_manager = DatabaseManager(db_config)
db_manager.initialize()  # Inicializa la base de datos y el esquema

# repositorio
asset_repository = IndustrialAssetRepository(db_manager)
order_repository = WorkOrderRepository(db_manager)
tech_repository = TechnicianRepository(db_manager)
supervisor_repository = SupervisorRepository(db_manager)

# servicios
asset_service = IndustrialAssetService(asset_repository)
order_service = WorkOrderService(order_repository)
tech_service = TechnicianService(tech_repository, order_service)
supervisor_service = SupervisorService(supervisor_repository, order_service, tech_service, asset_service)


def register_user() -> User:
    print(f"\n--- Registro de usuario ---")
    print("Selecciona el tipo de usuario a registrar:")
    print("1. Supervisor")
    print("2. Técnico")
    print("3. Volver al menú principal")
    registered_user = None  # Inicializa la variable para almacenar el usuario registrado
    while True:
        option = input("Ingresa el número de la opción: ")
        if option == '1':
            print(f"\n--- Registro de SUPERVISOR ---")
            first_name = input("Nombre: ")
            last_name = input("Apellido: ")
            email = input("Email: ")
            password = input("Contraseña: ")
            assigned_area = input("Área asignada: ")

            user_data = UserBaseData(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
            )
            try:
                registered_user = supervisor_service.create_supervisor(user_data, assigned_area)
                print("Supervisor registrado exitosamente. Ahora puedes iniciar sesión.")
            except Exception as ex:
                print(f"Error al registrar el supervisor: {ex}")
            break
        elif option == '2':
            print(f"\n--- Registro de TÉCNICO ---")
            first_name = input("Nombre: ")
            last_name = input("Apellido: ")
            email = input("Email: ")
            password = input("Contraseña: ")
            max_active_orders = int(input("Máximo de órdenes activas: "))

            user_data = UserBaseData(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
            )
            try:
                registered_user = tech_service.create_technician(user_data, max_active_orders)
                print("Técnico registrado exitosamente. Ahora puedes iniciar sesión.")
            except Exception as ex:
                print(f"Error al registrar el técnico: {ex}")
            break
        elif option == '3':
            print("Volviendo al menú principal...")
            break  # Vuelve al menú principal sin registrar un usuario
        else:
            print("Opción inválida. Por favor, elige 1 o 2.")
    return registered_user


def login(role):
    print(f"\n--- Iniciar Sesión como {role} ---")
    email = input("Email: ")
    password = input("Contraseña: ")
    # Simulación de credenciales
    if role == UserRole.SUPERVISOR.value:
        try:
            supervisor_service.exist_supervisor_by_credentials(email, password)
            print("Iniciaste seción como SUPERVISOR!")
            return supervisor_service.get_supervisor_by_email(email)
        except Exception as ex:
            print(f"Error al iniciar sesión: {ex}")
            return None
    elif role == UserRole.TECHNICIAN.value:
        try:
            tech_service.exist_technician_by_credentials(email, password)
            print("Iniciaste seción como TÉCNICO!")
            return tech_service.get_technician_by_email(email)
        except Exception as ex:
            print(f"Error al iniciar sesión: {ex}")
            return None
    else:
        print("Rol no reconocido. Por favor, intenta de nuevo.")
        return None


def supervisor_menu(supervisor: Supervisor):
    """Muestra el menú para usuarios Supervisores."""
    while True:
        print("\n--- Menú de Supervisor ---")
        print("1. Registrar un activo industrial")
        print("2. Iniciar una orden de trabajo")
        print("3. Asignar técnico a una orden de trabajo")
        print("4. Listar las órdenes de trabajo no asignadas")
        print("5. Cerrar sesión")
        opcion = input("Selecciona una opción: \n")

        if opcion == '1':
            print("\n--Registrar un activo industrial--")
            asset_type = input("Tipo de activo: ")
            model = input("Modelo: ")
            location = input("Ubicación: ")
            acquisition_date = input("Fecha de adquisición (dd/mm/yyyy): ")
            asset_data = IndustrialAssetData(
                asset_type=asset_type,
                model=model,
                location=location,
                acquisition_date=acquisition_date
            )
            try:
                asset = asset_service.create_asset(asset_data)
                print(f"Activo industrial registrado. Detalles del activo: \n{asset}")
            except Exception as ex:
                print(f"Error al registrar el activo: {ex}")
        elif opcion == '2':
            print("--Iniciar una orden de trabajo--")
            print("Lista de activos industriales existentes:")
            assets = asset_repository.list_by_criteria({})
            if not assets:
                print("No hay activos industriales registrados.")
                continue
            else:
                for asset in assets:
                    print(f"{asset}")
            asset_id = int(input("Ingresa el ID del activo industrial: "))
            try:
                asset_service.get_asset_by_id(asset_id)
            except Exception as ex:
                print(f"Ha ocurrido un error al obtener el activo: {ex}")
                continue
            print("\n--Datos de la orden de trabajo--")
            title = input("Título: ")
            while True:
                print("Selecciona el tipo de mantenimiento:")
                print("1. Preventivo")
                print("2. Correctivo")
                selected_option = input("Ingresa el número de la opción: ")
                if selected_option == '1':
                    maintenance_type = MaintenanceType.PREVENTIVE
                    break
                elif selected_option == '2':
                    maintenance_type = MaintenanceType.CORRECTIVE
                    break
                else:
                    print("Opción inválida. Por favor, elige 1 o 2.")
            while True:
                print("Selecciona el nivel de prioridad:")
                print("1. Critico")
                print("2. Urgente")
                print("3. Alta")
                print("4. Media")
                print("5. Baja")
                selected_option = input("Ingresa el número de la opción: ")
                if selected_option == '1':
                    priority = PriorityLevel.CRITICAL
                    break
                elif selected_option == '2':
                    priority = PriorityLevel.URGENT
                    break
                elif selected_option == '3':
                    priority = PriorityLevel.HIGH
                    break
                elif selected_option == '4':
                    priority = PriorityLevel.MEDIUM
                    break
                elif selected_option == '5':
                    priority = PriorityLevel.LOW
                    break
                else:
                    print("Opción inválida. Por favor, elige una opción del 1 al 5.")
            estimated_time = int(input("Tiempo estimado (horas, días, semanas): "))
            while True:
                print("Selecciona la unidad de tiempo:")
                print("1. Horas")
                print("2. Días")
                print("3. Semanas")
                selected_option = input("Ingresa el número de la opción: ")
                if selected_option == '1':
                    estimated_time_unit = TimeUnit.HOURS
                    break
                elif selected_option == '2':
                    estimated_time_unit = TimeUnit.DAYS
                    break
                elif selected_option == '3':
                    estimated_time_unit = TimeUnit.WEEKS
                    break
                else:
                    print("Opción inválida. Por favor, elige una opción del 1 al 3.")
            description = input("Descripción: ")
            order_data = WorkOrderData(
                title=title,
                maintenance_type=maintenance_type,
                priority=priority,
                status=Status.IN_PROGRESS,
                estimated_time=estimated_time,
                estimated_time_unit=estimated_time_unit,
                description=description
            )
            try:
                asset = asset_service.get_asset_by_id(asset_id)
                work_order = supervisor_service.initiate_work_order(order_data, asset.id, supervisor.id)
                print(f"Orden de trabajo iniciada exitosamente. Detalles: \n{work_order}")
            except Exception as ex:
                print(f"Error al iniciar la orden de trabajo: {ex}")
        elif opcion == '3':
            print("--Asignar técnico a una orden de trabajo--")
            print("Ordenes lisas para asignar:")
            unassigned_orders = order_service.list_work_orders(
                {'status': Status.UNASSIGNED.value, 'created_by': supervisor.id})
            if not unassigned_orders:
                print("No hay órdenes de trabajo sin asignar.")
                continue
            else:
                for order in unassigned_orders:
                    print(f"Orden ID: {order.id}, Título: {order.title}, Descripción: {order.description}")
            work_order_id = int(input("Ingresa el ID de la orden de trabajo: "))
            print("Técnicos disponibles:")
            technicians = tech_repository.list_by_criteria({})
            if not technicians:
                print("No hay técnicos disponibles.")
                continue
            else:
                for technician in technicians:
                    print(f"Técnico ID: {technician.id}, Nombre: {technician.first_name} {technician.last_name}")
            technician_id = int(input("Ingresa el ID del técnico a asignar: "))
            try:
                assigned_order = supervisor_service.assign_work_order(technician_id, work_order_id)
                print(f"Técnico asignado exitosamente a la orden de trabajo {assigned_order.id}.")
            except Exception as ex:
                print(f"Error al asignar técnico: {ex}")
        elif opcion == '4':
            print("--Listar órdenes de trabajo sin asignar--")
            unassigned_orders = order_service.list_work_orders(
                {'status': Status.UNASSIGNED.value, 'technician_id': None, 'created_by': supervisor.id})
            if unassigned_orders:
                for order in unassigned_orders:
                    print(f"Orden ID: {order.id}, Título: {order.title}, Descripción: {order.description}")
            else:
                print("No hay órdenes de trabajo sin asignar.")
        elif opcion == '5':
            print("Cerrando sesión de Supervisor...")
            break  # Vuelve al menú de inicio de sesión
        else:
            print("Opción inválida. Por favor, elige una opción del 1 al 5.")


def technician_menu(tech: Technician):
    """Muestra el menú para usuarios Técnicos."""
    while True:
        print("\n--- Menú de Técnicos ---")
        print("1. Listar órdenes de trabajo asignadas")
        print("2. Resolver una orden de trabajo")
        print("3. Cerrar sesión")
        option = input("Selecciona una opción: ")

        if option == '1':
            print("\n--Lista de órdenes asignadas--")
            orders = tech_service.get_assigned_work_orders(tech)
            if orders:
                for order in orders:
                    print(f"Orden ID: {order.id}, Descripción: {order.description}")
            else:
                print("No tienes órdenes de trabajo pendientes.")
        elif option == '2':
            print("\n--Resolver una orden de trabajo--")
            order_id = int(input("Ingresa el ID de la orden de trabajo a resolver: "))
            closure_comments = input("Ingresa los comentarios de cierre: ")
            try:
                resolved_order = tech_service.mark_order_as_resolved(order_id, tech.id, closure_comments)
                print(f"Orden de trabajo {resolved_order.id} resuelta exitosamente.")
                print(f"Detalles de la orden resuelta: \n{resolved_order}")
            except Exception as ex:
                print(f"Error al resolver la orden: {ex}")
        elif option == '3':
            print("Cerrando sesión de Técnico...")
            break  # Vuelve al menú de inicio de sesión
        else:
            print("Opción inválida. Por favor, elige una opción del 1 al 3.")


def main():
    """Función principal del sistema de gestión."""
    while True:
        print("\n--- Menú Principal ---")
        print("1. Registrarse")
        print("2. Iniciar Sesión como Supervisor")
        print("3. Iniciar Sesión como Técnico")
        print("4. Salir de la aplicación")
        option = input("Selecciona una opción: \n")

        if option == '1':
            register_user()
        elif option == '2':
            supervisor = login(UserRole.SUPERVISOR.value)
            if supervisor:
                supervisor_menu(supervisor)
        elif option == '3':
            tech = login(UserRole.TECHNICIAN.value)
            if tech:
                technician_menu(tech)
        elif option == '4':
            print("Has salido de la aplicación. ¡Hasta pronto!")
            break
        else:
            print("Opción inválida. Por favor, elige 1, 2 o 3.")


# Iniciar la aplicación
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        print(f"\nError inesperado: {e}")
        print("Por favor, contacta al administrador del sistema.")
