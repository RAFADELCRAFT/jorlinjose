#!/usr/bin/env python3
"""
Panel de Administración - Jorling Seguidores 2025
Sistema de gestión para administradores únicamente
"""

import json
import os
import hashlib
import base64
from datetime import datetime, timedelta
import getpass

class JorlingAdmin:
    def __init__(self):
        self.data_dir = "data"
        self.users_file = os.path.join(self.data_dir, "users.json")
        self.orders_file = os.path.join(self.data_dir, "orders.json")
        self.admin_file = os.path.join(self.data_dir, "admin_config.json")
        
        # Crear directorio de datos si no existe
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        self.users = self.load_users()
        self.orders = self.load_orders()
        self.admin_config = self.load_admin_config()
        
    def load_users(self):
        """Cargar usuarios desde archivo JSON"""
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error cargando usuarios: {e}")
            return []
    
    def save_users(self):
        """Guardar usuarios en archivo JSON"""
        try:
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error guardando usuarios: {e}")
            return False
    
    def load_orders(self):
        """Cargar órdenes desde archivo JSON"""
        try:
            if os.path.exists(self.orders_file):
                with open(self.orders_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error cargando órdenes: {e}")
            return []
    
    def save_orders(self):
        """Guardar órdenes en archivo JSON"""
        try:
            with open(self.orders_file, 'w', encoding='utf-8') as f:
                json.dump(self.orders, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error guardando órdenes: {e}")
            return False
    
    def load_admin_config(self):
        """Cargar configuración de admin"""
        try:
            if os.path.exists(self.admin_file):
                with open(self.admin_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {"admin_password": self.hash_password("jorling2025")}
        except Exception as e:
            print(f"Error cargando configuración: {e}")
            return {"admin_password": self.hash_password("jorling2025")}
    
    def save_admin_config(self):
        """Guardar configuración de admin"""
        try:
            with open(self.admin_file, 'w', encoding='utf-8') as f:
                json.dump(self.admin_config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error guardando configuración: {e}")
            return False
    
    def hash_password(self, password):
        """Hash de contraseña"""
        return base64.b64encode((password + 'jorling_salt_2025').encode()).decode()
    
    def authenticate_admin(self):
        """Autenticar administrador"""
        print("🔐 ACCESO RESTRINGIDO - SOLO ADMINISTRADORES")
        print("=" * 50)
        
        for attempt in range(3):
            password = getpass.getpass("Ingresa la contraseña de administrador: ")
            
            if self.hash_password(password) == self.admin_config["admin_password"]:
                print("✅ Acceso autorizado")
                return True
            else:
                print(f"❌ Contraseña incorrecta. Intentos restantes: {2 - attempt}")
        
        print("🚫 Acceso denegado. Demasiados intentos fallidos.")
        return False
    
    def show_main_menu(self):
        """Mostrar menú principal"""
        while True:
            print("\n" + "=" * 60)
            print("🚀 JORLING SEGUIDORES 2025 - PANEL DE ADMINISTRACIÓN")
            print("=" * 60)
            print("1. 👥 Gestión de Usuarios")
            print("2. 📋 Gestión de Órdenes")
            print("3. 💰 Gestión de Saldos")
            print("4. 🎁 Envíos Automáticos")
            print("5. 📊 Estadísticas")
            print("6. ⚙️  Configuración")
            print("7. 🚪 Salir")
            print("=" * 60)
            
            choice = input("Selecciona una opción (1-7): ").strip()
            
            if choice == "1":
                self.user_management_menu()
            elif choice == "2":
                self.order_management_menu()
            elif choice == "3":
                self.balance_management_menu()
            elif choice == "4":
                self.automatic_rewards_menu()
            elif choice == "5":
                self.show_statistics()
            elif choice == "6":
                self.configuration_menu()
            elif choice == "7":
                print("👋 ¡Hasta luego!")
                break
            else:
                print("❌ Opción inválida")
    
    def user_management_menu(self):
        """Menú de gestión de usuarios"""
        while True:
            print("\n" + "=" * 50)
            print("👥 GESTIÓN DE USUARIOS")
            print("=" * 50)
            print("1. 📋 Listar todos los usuarios")
            print("2. 🔍 Buscar usuario")
            print("3. ➕ Crear usuario")
            print("4. ✏️  Editar usuario")
            print("5. 🗑️  Eliminar usuario")
            print("6. ⬅️  Volver al menú principal")
            print("=" * 50)
            
            choice = input("Selecciona una opción (1-6): ").strip()
            
            if choice == "1":
                self.list_all_users()
            elif choice == "2":
                self.search_user()
            elif choice == "3":
                self.create_user()
            elif choice == "4":
                self.edit_user()
            elif choice == "5":
                self.delete_user()
            elif choice == "6":
                break
            else:
                print("❌ Opción inválida")
    
    def list_all_users(self):
        """Listar todos los usuarios"""
        print("\n📋 LISTA DE USUARIOS")
        print("-" * 80)
        
        if not self.users:
            print("No hay usuarios registrados.")
            return
        
        print(f"{'ID':<15} {'Usuario':<20} {'Email':<25} {'Saldo':<10} {'Admin':<5}")
        print("-" * 80)
        
        for user in self.users:
            user_id = user.get('id', 'N/A')[:12] + "..."
            username = user.get('username', 'N/A')[:18]
            email = user.get('email', 'N/A')[:23]
            balance = f"${user.get('balance', 0):.2f}"
            is_admin = "Sí" if user.get('isAdmin', False) else "No"
            
            print(f"{user_id:<15} {username:<20} {email:<25} {balance:<10} {is_admin:<5}")
        
        print(f"\nTotal de usuarios: {len(self.users)}")
    
    def search_user(self):
        """Buscar usuario"""
        search_term = input("Ingresa nombre de usuario o email: ").strip()
        
        found_users = [
            user for user in self.users
            if search_term.lower() in user.get('username', '').lower() or
               search_term.lower() in user.get('email', '').lower()
        ]
        
        if not found_users:
            print("❌ No se encontraron usuarios.")
            return
        
        print(f"\n🔍 RESULTADOS DE BÚSQUEDA ({len(found_users)} encontrados)")
        print("-" * 80)
        
        for i, user in enumerate(found_users, 1):
            print(f"{i}. {user.get('username')} ({user.get('email')}) - Saldo: ${user.get('balance', 0):.2f}")
    
    def create_user(self):
        """Crear nuevo usuario"""
        print("\n➕ CREAR NUEVO USUARIO")
        print("-" * 30)
        
        username = input("Nombre de usuario: ").strip()
        email = input("Email: ").strip()
        password = input("Contraseña: ").strip()
        balance = float(input("Saldo inicial (USD): ") or "0")
        is_admin = input("¿Es administrador? (s/n): ").strip().lower() == 's'
        
        # Verificar si el usuario ya existe
        if any(u.get('username') == username for u in self.users):
            print("❌ El nombre de usuario ya existe.")
            return
        
        if any(u.get('email') == email for u in self.users):
            print("❌ El email ya está registrado.")
            return
        
        new_user = {
            'id': f'user_{int(datetime.now().timestamp())}',
            'username': username,
            'email': email,
            'password': self.hash_password(password),
            'balance': balance,
            'isAdmin': is_admin,
            'createdAt': datetime.now().isoformat()
        }
        
        self.users.append(new_user)
        
        if self.save_users():
            print("✅ Usuario creado exitosamente.")
        else:
            print("❌ Error al crear usuario.")
    
    def edit_user(self):
        """Editar usuario"""
        username = input("Nombre de usuario a editar: ").strip()
        
        user = next((u for u in self.users if u.get('username') == username), None)
        
        if not user:
            print("❌ Usuario no encontrado.")
            return
        
        print(f"\n✏️ EDITANDO USUARIO: {username}")
        print("-" * 40)
        print(f"Email actual: {user.get('email')}")
        print(f"Saldo actual: ${user.get('balance', 0):.2f}")
        print(f"Admin actual: {'Sí' if user.get('isAdmin', False) else 'No'}")
        print()
        
        new_email = input("Nuevo email (Enter para mantener): ").strip()
        new_balance = input("Nuevo saldo (Enter para mantener): ").strip()
        new_password = input("Nueva contraseña (Enter para mantener): ").strip()
        new_admin = input("¿Es admin? s/n (Enter para mantener): ").strip().lower()
        
        if new_email:
            user['email'] = new_email
        
        if new_balance:
            try:
                user['balance'] = float(new_balance)
            except ValueError:
                print("❌ Saldo inválido.")
                return
        
        if new_password:
            user['password'] = self.hash_password(new_password)
        
        if new_admin in ['s', 'n']:
            user['isAdmin'] = new_admin == 's'
        
        if self.save_users():
            print("✅ Usuario actualizado exitosamente.")
        else:
            print("❌ Error al actualizar usuario.")
    
    def delete_user(self):
        """Eliminar usuario"""
        username = input("Nombre de usuario a eliminar: ").strip()
        
        user_index = next((i for i, u in enumerate(self.users) if u.get('username') == username), None)
        
        if user_index is None:
            print("❌ Usuario no encontrado.")
            return
        
        user = self.users[user_index]
        
        print(f"\n🗑️ ELIMINAR USUARIO")
        print("-" * 30)
        print(f"Usuario: {user.get('username')}")
        print(f"Email: {user.get('email')}")
        print(f"Saldo: ${user.get('balance', 0):.2f}")
        
        confirm = input("\n¿Estás seguro? Esta acción no se puede deshacer (s/n): ").strip().lower()
        
        if confirm == 's':
            del self.users[user_index]
            if self.save_users():
                print("✅ Usuario eliminado exitosamente.")
            else:
                print("❌ Error al eliminar usuario.")
        else:
            print("❌ Operación cancelada.")
    
    def balance_management_menu(self):
        """Menú de gestión de saldos"""
        while True:
            print("\n" + "=" * 50)
            print("💰 GESTIÓN DE SALDOS")
            print("=" * 50)
            print("1. 💵 Añadir saldo a usuario")
            print("2. 💸 Restar saldo a usuario")
            print("3. 💰 Ver saldo de usuario")
            print("4. 📊 Reporte de saldos")
            print("5. ⬅️  Volver al menú principal")
            print("=" * 50)
            
            choice = input("Selecciona una opción (1-5): ").strip()
            
            if choice == "1":
                self.add_balance()
            elif choice == "2":
                self.subtract_balance()
            elif choice == "3":
                self.check_balance()
            elif choice == "4":
                self.balance_report()
            elif choice == "5":
                break
            else:
                print("❌ Opción inválida")
    
    def add_balance(self):
        """Añadir saldo a usuario"""
        username = input("Nombre de usuario: ").strip()
        
        user = next((u for u in self.users if u.get('username') == username), None)
        
        if not user:
            print("❌ Usuario no encontrado.")
            return
        
        try:
            amount = float(input("Cantidad a añadir (USD): "))
            if amount <= 0:
                print("❌ La cantidad debe ser mayor a 0.")
                return
        except ValueError:
            print("❌ Cantidad inválida.")
            return
        
        old_balance = user.get('balance', 0)
        user['balance'] = old_balance + amount
        
        if self.save_users():
            print(f"✅ Saldo actualizado:")
            print(f"   Saldo anterior: ${old_balance:.2f}")
            print(f"   Cantidad añadida: ${amount:.2f}")
            print(f"   Nuevo saldo: ${user['balance']:.2f}")
        else:
            print("❌ Error al actualizar saldo.")
    
    def subtract_balance(self):
        """Restar saldo a usuario"""
        username = input("Nombre de usuario: ").strip()
        
        user = next((u for u in self.users if u.get('username') == username), None)
        
        if not user:
            print("❌ Usuario no encontrado.")
            return
        
        try:
            amount = float(input("Cantidad a restar (USD): "))
            if amount <= 0:
                print("❌ La cantidad debe ser mayor a 0.")
                return
        except ValueError:
            print("❌ Cantidad inválida.")
            return
        
        old_balance = user.get('balance', 0)
        
        if old_balance < amount:
            print(f"❌ Saldo insuficiente. Saldo actual: ${old_balance:.2f}")
            return
        
        user['balance'] = old_balance - amount
        
        if self.save_users():
            print(f"✅ Saldo actualizado:")
            print(f"   Saldo anterior: ${old_balance:.2f}")
            print(f"   Cantidad restada: ${amount:.2f}")
            print(f"   Nuevo saldo: ${user['balance']:.2f}")
        else:
            print("❌ Error al actualizar saldo.")
    
    def check_balance(self):
        """Ver saldo de usuario"""
        username = input("Nombre de usuario: ").strip()
        
        user = next((u for u in self.users if u.get('username') == username), None)
        
        if not user:
            print("❌ Usuario no encontrado.")
            return
        
        print(f"\n💰 SALDO DE {username.upper()}")
        print("-" * 30)
        print(f"Saldo actual: ${user.get('balance', 0):.2f}")
        print(f"Fecha de registro: {user.get('createdAt', 'N/A')}")
    
    def balance_report(self):
        """Reporte de saldos"""
        print("\n📊 REPORTE DE SALDOS")
        print("-" * 50)
        
        if not self.users:
            print("No hay usuarios registrados.")
            return
        
        total_balance = sum(user.get('balance', 0) for user in self.users)
        users_with_balance = [user for user in self.users if user.get('balance', 0) > 0]
        
        print(f"Total de usuarios: {len(self.users)}")
        print(f"Usuarios con saldo: {len(users_with_balance)}")
        print(f"Saldo total en el sistema: ${total_balance:.2f}")
        print(f"Saldo promedio: ${total_balance / len(self.users):.2f}")
        
        if users_with_balance:
            print("\nUsuarios con mayor saldo:")
            sorted_users = sorted(users_with_balance, key=lambda x: x.get('balance', 0), reverse=True)
            for i, user in enumerate(sorted_users[:5], 1):
                print(f"{i}. {user.get('username')} - ${user.get('balance', 0):.2f}")
    
    def order_management_menu(self):
        """Menú de gestión de órdenes"""
        while True:
            print("\n" + "=" * 50)
            print("📋 GESTIÓN DE ÓRDENES")
            print("=" * 50)
            print("1. 📋 Listar todas las órdenes")
            print("2. 🔍 Buscar órdenes")
            print("3. ✏️  Cambiar estado de orden")
            print("4. 🗑️  Eliminar orden")
            print("5. 📊 Estadísticas de órdenes")
            print("6. ⬅️  Volver al menú principal")
            print("=" * 50)
            
            choice = input("Selecciona una opción (1-6): ").strip()
            
            if choice == "1":
                self.list_all_orders()
            elif choice == "2":
                self.search_orders()
            elif choice == "3":
                self.change_order_status()
            elif choice == "4":
                self.delete_order()
            elif choice == "5":
                self.order_statistics()
            elif choice == "6":
                break
            else:
                print("❌ Opción inválida")
    
    def list_all_orders(self):
        """Listar todas las órdenes"""
        print("\n📋 LISTA DE ÓRDENES")
        print("-" * 100)
        
        if not self.orders:
            print("No hay órdenes registradas.")
            return
        
        print(f"{'ID':<12} {'Usuario':<15} {'Plataforma':<12} {'Servicio':<12} {'Cantidad':<10} {'Precio':<8} {'Estado':<12}")
        print("-" * 100)
        
        for order in self.orders[-20:]:  # Mostrar últimas 20 órdenes
            order_id = order.get('id', 'N/A')[:10] + "..."
            username = self.get_username_by_id(order.get('userId', ''))[:13]
            platform = order.get('platform', 'N/A')[:10]
            service = order.get('service', 'N/A')[:10]
            quantity = str(order.get('quantity', 0))[:8]
            price = f"${order.get('price', 0):.2f}"[:6]
            status = order.get('status', 'N/A')[:10]
            
            print(f"{order_id:<12} {username:<15} {platform:<12} {service:<12} {quantity:<10} {price:<8} {status:<12}")
        
        print(f"\nMostrando últimas 20 de {len(self.orders)} órdenes totales")
    
    def get_username_by_id(self, user_id):
        """Obtener nombre de usuario por ID"""
        user = next((u for u in self.users if u.get('id') == user_id), None)
        return user.get('username', 'Usuario eliminado') if user else 'N/A'
    
    def search_orders(self):
        """Buscar órdenes"""
        print("\n🔍 BUSCAR ÓRDENES")
        print("1. Por ID de orden")
        print("2. Por nombre de usuario")
        print("3. Por plataforma")
        print("4. Por estado")
        
        choice = input("Selecciona tipo de búsqueda (1-4): ").strip()
        
        if choice == "1":
            search_term = input("ID de orden: ").strip()
            found_orders = [o for o in self.orders if search_term in o.get('id', '')]
        elif choice == "2":
            username = input("Nombre de usuario: ").strip()
            user = next((u for u in self.users if u.get('username') == username), None)
            if not user:
                print("❌ Usuario no encontrado.")
                return
            found_orders = [o for o in self.orders if o.get('userId') == user.get('id')]
        elif choice == "3":
            platform = input("Plataforma: ").strip().lower()
            found_orders = [o for o in self.orders if platform in o.get('platform', '').lower()]
        elif choice == "4":
            status = input("Estado (pending/processing/completed/cancelled): ").strip().lower()
            found_orders = [o for o in self.orders if o.get('status', '').lower() == status]
        else:
            print("❌ Opción inválida.")
            return
        
        if not found_orders:
            print("❌ No se encontraron órdenes.")
            return
        
        print(f"\n📋 RESULTADOS ({len(found_orders)} encontradas)")
        print("-" * 80)
        
        for i, order in enumerate(found_orders[-10:], 1):  # Mostrar últimas 10
            username = self.get_username_by_id(order.get('userId', ''))
            print(f"{i}. {order.get('id')[:15]}... - {username} - {order.get('platform')} - ${order.get('price', 0):.2f} - {order.get('status')}")
    
    def change_order_status(self):
        """Cambiar estado de orden"""
        order_id = input("ID de orden (completo o parcial): ").strip()
        
        order = next((o for o in self.orders if order_id in o.get('id', '')), None)
        
        if not order:
            print("❌ Orden no encontrada.")
            return
        
        print(f"\n✏️ CAMBIAR ESTADO DE ORDEN")
        print("-" * 40)
        print(f"ID: {order.get('id')}")
        print(f"Usuario: {self.get_username_by_id(order.get('userId', ''))}")
        print(f"Estado actual: {order.get('status')}")
        print()
        print("Estados disponibles:")
        print("1. pending")
        print("2. processing")
        print("3. completed")
        print("4. cancelled")
        
        new_status = input("Nuevo estado: ").strip().lower()
        
        if new_status not in ['pending', 'processing', 'completed', 'cancelled']:
            print("❌ Estado inválido.")
            return
        
        order['status'] = new_status
        
        if new_status == 'completed':
            order['completedAt'] = datetime.now().isoformat()
        
        if self.save_orders():
            print(f"✅ Estado actualizado a: {new_status}")
        else:
            print("❌ Error al actualizar estado.")
    
    def delete_order(self):
        """Eliminar orden"""
        order_id = input("ID de orden (completo o parcial): ").strip()
        
        order_index = next((i for i, o in enumerate(self.orders) if order_id in o.get('id', '')), None)
        
        if order_index is None:
            print("❌ Orden no encontrada.")
            return
        
        order = self.orders[order_index]
        
        print(f"\n🗑️ ELIMINAR ORDEN")
        print("-" * 30)
        print(f"ID: {order.get('id')}")
        print(f"Usuario: {self.get_username_by_id(order.get('userId', ''))}")
        print(f"Precio: ${order.get('price', 0):.2f}")
        print(f"Estado: {order.get('status')}")
        
        confirm = input("\n¿Estás seguro? Esta acción no se puede deshacer (s/n): ").strip().lower()
        
        if confirm == 's':
            del self.orders[order_index]
            if self.save_orders():
                print("✅ Orden eliminada exitosamente.")
            else:
                print("❌ Error al eliminar orden.")
        else:
            print("❌ Operación cancelada.")
    
    def order_statistics(self):
        """Estadísticas de órdenes"""
        print("\n📊 ESTADÍSTICAS DE ÓRDENES")
        print("-" * 50)
        
        if not self.orders:
            print("No hay órdenes registradas.")
            return
        
        total_orders = len(self.orders)
        total_revenue = sum(order.get('price', 0) for order in self.orders)
        
        # Estadísticas por estado
        status_counts = {}
        for order in self.orders:
            status = order.get('status', 'unknown')
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # Estadísticas por plataforma
        platform_counts = {}
        platform_revenue = {}
        for order in self.orders:
            platform = order.get('platform', 'unknown')
            price = order.get('price', 0)
            platform_counts[platform] = platform_counts.get(platform, 0) + 1
            platform_revenue[platform] = platform_revenue.get(platform, 0) + price
        
        print(f"Total de órdenes: {total_orders}")
        print(f"Ingresos totales: ${total_revenue:.2f}")
        print(f"Ingreso promedio por orden: ${total_revenue / total_orders:.2f}")
        
        print("\nÓrdenes por estado:")
        for status, count in status_counts.items():
            percentage = (count / total_orders) * 100
            print(f"  {status}: {count} ({percentage:.1f}%)")
        
        print("\nÓrdenes por plataforma:")
        for platform, count in platform_counts.items():
            revenue = platform_revenue.get(platform, 0)
            print(f"  {platform}: {count} órdenes - ${revenue:.2f}")
    
    def show_statistics(self):
        """Mostrar estadísticas generales"""
        print("\n📊 ESTADÍSTICAS GENERALES")
        print("=" * 60)
        
        # Estadísticas de usuarios
        total_users = len(self.users)
        admin_users = len([u for u in self.users if u.get('isAdmin', False)])
        regular_users = total_users - admin_users
        total_balance = sum(u.get('balance', 0) for u in self.users)
        
        print(f"👥 USUARIOS:")
        print(f"   Total: {total_users}")
        print(f"   Regulares: {regular_users}")
        print(f"   Administradores: {admin_users}")
        print(f"   Saldo total: ${total_balance:.2f}")
        
        # Estadísticas de órdenes
        total_orders = len(self.orders)
        total_revenue = sum(o.get('price', 0) for o in self.orders)
        completed_orders = len([o for o in self.orders if o.get('status') == 'completed'])
        
        print(f"\n📋 ÓRDENES:")
        print(f"   Total: {total_orders}")
        print(f"   Completadas: {completed_orders}")
        print(f"   Tasa de éxito: {(completed_orders / total_orders * 100):.1f}%" if total_orders > 0 else "   Tasa de éxito: 0%")
        print(f"   Ingresos totales: ${total_revenue:.2f}")
        
        # Órdenes recientes
        recent_orders = [o for o in self.orders if datetime.fromisoformat(o.get('createdAt', '2024-01-01')) > datetime.now() - timedelta(days=7)]
        print(f"   Órdenes última semana: {len(recent_orders)}")
        
        # Usuarios más activos
        user_order_counts = {}
        for order in self.orders:
            user_id = order.get('userId', '')
            user_order_counts[user_id] = user_order_counts.get(user_id, 0) + 1
        
        if user_order_counts:
            top_user_id = max(user_order_counts, key=user_order_counts.get)
            top_user = next((u for u in self.users if u.get('id') == top_user_id), None)
            if top_user:
                print(f"\n🏆 Usuario más activo: {top_user.get('username')} ({user_order_counts[top_user_id]} órdenes)")
    
    def configuration_menu(self):
        """Menú de configuración"""
        while True:
            print("\n" + "=" * 50)
            print("⚙️ CONFIGURACIÓN")
            print("=" * 50)
            print("1. 🔑 Cambiar contraseña de admin")
            print("2. 💾 Hacer backup de datos")
            print("3. 📥 Restaurar backup")
            print("4. 🧹 Limpiar datos antiguos")
            print("5. ⬅️  Volver al menú principal")
            print("=" * 50)
            
            choice = input("Selecciona una opción (1-5): ").strip()
            
            if choice == "1":
                self.change_admin_password()
            elif choice == "2":
                self.create_backup()
            elif choice == "3":
                self.restore_backup()
            elif choice == "4":
                self.clean_old_data()
            elif choice == "5":
                break
            else:
                print("❌ Opción inválida")
    
    def change_admin_password(self):
        """Cambiar contraseña de administrador"""
        print("\n🔑 CAMBIAR CONTRASEÑA DE ADMINISTRADOR")
        print("-" * 40)
        
        current_password = getpass.getpass("Contraseña actual: ")
        
        if self.hash_password(current_password) != self.admin_config["admin_password"]:
            print("❌ Contraseña actual incorrecta.")
            return
        
        new_password = getpass.getpass("Nueva contraseña: ")
        confirm_password = getpass.getpass("Confirmar nueva contraseña: ")
        
        if new_password != confirm_password:
            print("❌ Las contraseñas no coinciden.")
            return
        
        if len(new_password) < 6:
            print("❌ La contraseña debe tener al menos 6 caracteres.")
            return
        
        self.admin_config["admin_password"] = self.hash_password(new_password)
        
        if self.save_admin_config():
            print("✅ Contraseña actualizada exitosamente.")
        else:
            print("❌ Error al actualizar contraseña.")
    
    def create_backup(self):
        """Crear backup de datos"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = f"backup_{timestamp}"
        
        try:
            os.makedirs(backup_dir)
            
            # Copiar archivos de datos
            import shutil
            if os.path.exists(self.users_file):
                shutil.copy2(self.users_file, backup_dir)
            if os.path.exists(self.orders_file):
                shutil.copy2(self.orders_file, backup_dir)
            if os.path.exists(self.admin_file):
                shutil.copy2(self.admin_file, backup_dir)
            
            print(f"✅ Backup creado en: {backup_dir}")
            
        except Exception as e:
            print(f"❌ Error creando backup: {e}")
    
    def restore_backup(self):
        """Restaurar backup"""
        print("\n📥 RESTAURAR BACKUP")
        print("-" * 30)
        
        # Listar directorios de backup
        backup_dirs = [d for d in os.listdir('.') if d.startswith('backup_')]
        
        if not backup_dirs:
            print("❌ No se encontraron backups.")
            return
        
        print("Backups disponibles:")
        for i, backup_dir in enumerate(backup_dirs, 1):
            print(f"{i}. {backup_dir}")
        
        try:
            choice = int(input("Selecciona backup a restaurar: ")) - 1
            selected_backup = backup_dirs[choice]
        except (ValueError, IndexError):
            print("❌ Selección inválida.")
            return
        
        confirm = input(f"¿Restaurar backup {selected_backup}? Esto sobrescribirá los datos actuales (s/n): ").strip().lower()
        
        if confirm != 's':
            print("❌ Operación cancelada.")
            return
        
        try:
            import shutil
            
            backup_users = os.path.join(selected_backup, "users.json")
            backup_orders = os.path.join(selected_backup, "orders.json")
            backup_admin = os.path.join(selected_backup, "admin_config.json")
            
            if os.path.exists(backup_users):
                shutil.copy2(backup_users, self.users_file)
            if os.path.exists(backup_orders):
                shutil.copy2(backup_orders, self.orders_file)
            if os.path.exists(backup_admin):
                shutil.copy2(backup_admin, self.admin_file)
            
            # Recargar datos
            self.users = self.load_users()
            self.orders = self.load_orders()
            self.admin_config = self.load_admin_config()
            
            print("✅ Backup restaurado exitosamente.")
            
        except Exception as e:
            print(f"❌ Error restaurando backup: {e}")
    
    def clean_old_data(self):
        """Limpiar datos antiguos"""
        print("\n🧹 LIMPIAR DATOS ANTIGUOS")
        print("-" * 30)
        
        days = input("Eliminar órdenes anteriores a cuántos días (30): ").strip()
        try:
            days = int(days) if days else 30
        except ValueError:
            days = 30
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        old_orders = [
            o for o in self.orders 
            if datetime.fromisoformat(o.get('createdAt', '2024-01-01')) < cutoff_date
        ]
        
        if not old_orders:
            print(f"❌ No hay órdenes anteriores a {days} días.")
            return
        
        print(f"Se encontraron {len(old_orders)} órdenes anteriores a {days} días.")
        confirm = input("¿Eliminar estas órdenes? (s/n): ").strip().lower()
        
        if confirm == 's':
            self.orders = [
                o for o in self.orders 
                if datetime.fromisoformat(o.get('createdAt', '2024-01-01')) >= cutoff_date
            ]
            
            if self.save_orders():
                print(f"✅ {len(old_orders)} órdenes eliminadas.")
            else:
                print("❌ Error al eliminar órdenes.")
        else:
            print("❌ Operación cancelada.")

    def sync_web_users(self):
        """Sincronizar usuarios desde la base de datos web"""
        web_users_file = "data/web_users.json"
        
        try:
            if os.path.exists(web_users_file):
                with open(web_users_file, 'r', encoding='utf-8') as f:
                    web_users = json.load(f)
                
                synced_count = 0
                for web_user in web_users:
                    # Verificar si el usuario ya existe en nuestro sistema
                    existing_user = next((u for u in self.users if u.get('email') == web_user.get('email')), None)
                    
                    if not existing_user:
                        # Agregar usuario nuevo desde web
                        new_user = {
                            'id': web_user.get('id', f'web_{int(datetime.now().timestamp())}'),
                            'username': web_user.get('username', ''),
                            'email': web_user.get('email', ''),
                            'password': web_user.get('password', ''),
                            'balance': web_user.get('balance', 0),
                            'isAdmin': web_user.get('isAdmin', False),
                            'createdAt': web_user.get('createdAt', datetime.now().isoformat()),
                            'source': 'web_registration'
                        }
                        self.users.append(new_user)
                        synced_count += 1
                    else:
                        # Actualizar datos si es necesario
                        if existing_user.get('username') != web_user.get('username'):
                            existing_user['username'] = web_user.get('username')
                            synced_count += 1
                
                if synced_count > 0:
                    self.save_users()
                    print(f"✅ {synced_count} usuarios sincronizados desde la web.")
                else:
                    print("ℹ️ No hay nuevos usuarios para sincronizar.")
                    
            else:
                print("❌ No se encontró archivo de usuarios web.")
                
        except Exception as e:
            print(f"❌ Error sincronizando usuarios web: {e}")

    def auto_send_balance_to_registered(self):
        """Enviar saldo automáticamente a usuarios registrados"""
        print("\n💰 ENVÍO AUTOMÁTICO DE SALDO A USUARIOS REGISTRADOS")
        print("=" * 60)
        
        # Primero sincronizar usuarios web
        self.sync_web_users()
        
        if not self.users:
            print("❌ No hay usuarios registrados.")
            return
        
        try:
            amount = float(input("💵 Cantidad a enviar a cada usuario (USD): "))
            if amount <= 0:
                print("❌ La cantidad debe ser mayor a 0.")
                return
        except ValueError:
            print("❌ Cantidad inválida.")
            return
        
        description = input("📝 Descripción del envío: ").strip()
        if not description:
            description = "Bono automático Jorling Seguidores"
        
        # Filtrar usuarios (excluir admins si se desea)
        exclude_admins = input("¿Excluir administradores? (s/n): ").strip().lower() == 's'
        
        target_users = []
        for user in self.users:
            if exclude_admins and user.get('isAdmin', False):
                continue
            target_users.append(user)
        
        if not target_users:
            print("❌ No hay usuarios válidos para enviar saldo.")
            return
        
        print(f"\n📋 Se enviará ${amount:.2f} a {len(target_users)} usuarios:")
        for i, user in enumerate(target_users[:10], 1):  # Mostrar primeros 10
            print(f"  {i}. {user.get('username')} ({user.get('email')})")
        
        if len(target_users) > 10:
            print(f"  ... y {len(target_users) - 10} usuarios más")
        
        total_amount = amount * len(target_users)
        print(f"\n💰 Total a distribuir: ${total_amount:.2f}")
        
        confirm = input("\n¿Confirmar envío masivo? (s/n): ").strip().lower()
        
        if confirm != 's':
            print("❌ Operación cancelada.")
            return
        
        # Procesar envíos
        successful_sends = 0
        failed_sends = 0
        
        print("\n🚀 Procesando envíos...")
        print("-" * 50)
        
        for user in target_users:
            try:
                old_balance = user.get('balance', 0)
                user['balance'] = old_balance + amount
                
                # Registrar la transacción
                user['last_auto_bonus'] = {
                    'amount': amount,
                    'description': description,
                    'date': datetime.now().isoformat(),
                    'old_balance': old_balance,
                    'new_balance': user['balance']
                }
                
                print(f"✅ {user.get('username')}: ${old_balance:.2f} → ${user['balance']:.2f}")
                successful_sends += 1
                
            except Exception as e:
                print(f"❌ Error enviando a {user.get('username', 'Usuario')}: {e}")
                failed_sends += 1
        
        # Guardar cambios
        if self.save_users():
            print(f"\n🎉 ENVÍO COMPLETADO")
            print(f"✅ Exitosos: {successful_sends}")
            print(f"❌ Fallidos: {failed_sends}")
            print(f"💰 Total distribuido: ${amount * successful_sends:.2f}")
        else:
            print("❌ Error guardando cambios.")

    def find_and_reward_active_users(self):
        """Encontrar y recompensar usuarios activos"""
        print("\n🏆 RECOMPENSAR USUARIOS ACTIVOS")
        print("=" * 50)
        
        # Sincronizar primero
        self.sync_web_users()
        
        if not self.users or not self.orders:
            print("❌ No hay suficientes datos para analizar.")
            return
        
        # Analizar actividad de usuarios
        user_activity = {}
        
        for order in self.orders:
            user_id = order.get('userId', '')
            if user_id not in user_activity:
                user_activity[user_id] = {
                    'orders_count': 0,
                    'total_spent': 0,
                    'last_order': None
                }
            
            user_activity[user_id]['orders_count'] += 1
            user_activity[user_id]['total_spent'] += order.get('price', 0)
            
            order_date = order.get('createdAt', '')
            if not user_activity[user_id]['last_order'] or order_date > user_activity[user_id]['last_order']:
                user_activity[user_id]['last_order'] = order_date
        
        # Encontrar usuarios activos
        active_users = []
        
        for user in self.users:
            user_id = user.get('id', '')
            activity = user_activity.get(user_id, {})
            
            orders_count = activity.get('orders_count', 0)
            total_spent = activity.get('total_spent', 0)
            
            # Criterios de actividad (puedes ajustar estos valores)
            if orders_count >= 3 or total_spent >= 50:
                active_users.append({
                    'user': user,
                    'orders': orders_count,
                    'spent': total_spent,
                    'last_order': activity.get('last_order', 'Nunca')
                })
        
        if not active_users:
            print("❌ No se encontraron usuarios activos.")
            return
        
        # Mostrar usuarios activos
        print(f"🎯 USUARIOS ACTIVOS ENCONTRADOS ({len(active_users)}):")
        print("-" * 70)
        print(f"{'Usuario':<20} {'Órdenes':<10} {'Gastado':<12} {'Última Orden':<15}")
        print("-" * 70)
        
        for data in sorted(active_users, key=lambda x: x['spent'], reverse=True):
            user = data['user']
            username = user.get('username', 'N/A')[:18]
            orders = data['orders']
            spent = f"${data['spent']:.2f}"
            last_order = data['last_order'][:10] if data['last_order'] != 'Nunca' else 'Nunca'
            
            print(f"{username:<20} {orders:<10} {spent:<12} {last_order:<15}")
        
        # Opciones de recompensa
        print(f"\n💰 OPCIONES DE RECOMPENSA:")
        print("1. Bono fijo para todos")
        print("2. Bono proporcional al gasto")
        print("3. Bono por número de órdenes")
        print("4. Cancelar")
        
        choice = input("Selecciona opción (1-4): ").strip()
        
        if choice == "1":
            self._reward_fixed_bonus(active_users)
        elif choice == "2":
            self._reward_proportional_bonus(active_users)
        elif choice == "3":
            self._reward_orders_bonus(active_users)
        else:
            print("❌ Operación cancelada.")

    def _reward_fixed_bonus(self, active_users):
        """Recompensa con bono fijo"""
        try:
            amount = float(input("💵 Bono fijo para cada usuario activo (USD): "))
            if amount <= 0:
                print("❌ La cantidad debe ser mayor a 0.")
                return
        except ValueError:
            print("❌ Cantidad inválida.")
            return
        
        description = "Bono por usuario activo - Jorling Seguidores"
        
        total_bonus = amount * len(active_users)
        print(f"\n💰 Total a distribuir: ${total_bonus:.2f}")
        
        confirm = input("¿Confirmar distribución? (s/n): ").strip().lower()
        
        if confirm == 's':
            successful = 0
            for data in active_users:
                user = data['user']
                old_balance = user.get('balance', 0)
                user['balance'] = old_balance + amount
                
                user['last_activity_bonus'] = {
                    'amount': amount,
                    'type': 'fixed_bonus',
                    'description': description,
                    'date': datetime.now().isoformat(),
                    'criteria': f"{data['orders']} órdenes, ${data['spent']:.2f} gastado"
                }
                
                print(f"✅ {user.get('username')}: +${amount:.2f}")
                successful += 1
            
            if self.save_users():
                print(f"\n🎉 {successful} usuarios recompensados exitosamente!")
            else:
                print("❌ Error guardando cambios.")
        else:
            print("❌ Operación cancelada.")

    def _reward_proportional_bonus(self, active_users):
        """Recompensa proporcional al gasto"""
        try:
            percentage = float(input("💵 Porcentaje del gasto a devolver (ej: 5 para 5%): "))
            if percentage <= 0 or percentage > 100:
                print("❌ El porcentaje debe estar entre 0 y 100.")
                return
        except ValueError:
            print("❌ Porcentaje inválido.")
            return
        
        description = f"Cashback {percentage}% por actividad - Jorling Seguidores"
        
        total_bonus = sum(data['spent'] * (percentage / 100) for data in active_users)
        print(f"\n💰 Total a distribuir: ${total_bonus:.2f}")
        
        confirm = input("¿Confirmar distribución? (s/n): ").strip().lower()
        
        if confirm == 's':
            successful = 0
            for data in active_users:
                user = data['user']
                bonus = data['spent'] * (percentage / 100)
                old_balance = user.get('balance', 0)
                user['balance'] = old_balance + bonus
                
                user['last_activity_bonus'] = {
                    'amount': bonus,
                    'type': 'proportional_bonus',
                    'description': description,
                    'date': datetime.now().isoformat(),
                    'criteria': f"{percentage}% de ${data['spent']:.2f}"
                }
                
                print(f"✅ {user.get('username')}: +${bonus:.2f}")
                successful += 1
            
            if self.save_users():
                print(f"\n🎉 {successful} usuarios recompensados exitosamente!")
            else:
                print("❌ Error guardando cambios.")
        else:
            print("❌ Operación cancelada.")

    def _reward_orders_bonus(self, active_users):
        """Recompensa por número de órdenes"""
        try:
            amount_per_order = float(input("💵 Bono por cada orden realizada (USD): "))
            if amount_per_order <= 0:
                print("❌ La cantidad debe ser mayor a 0.")
                return
        except ValueError:
            print("❌ Cantidad inválida.")
            return
        
        description = f"Bono ${amount_per_order:.2f} por orden - Jorling Seguidores"
        
        total_bonus = sum(data['orders'] * amount_per_order for data in active_users)
        print(f"\n💰 Total a distribuir: ${total_bonus:.2f}")
        
        confirm = input("¿Confirmar distribución? (s/n): ").strip().lower()
        
        if confirm == 's':
            successful = 0
            for data in active_users:
                user = data['user']
                bonus = data['orders'] * amount_per_order
                old_balance = user.get('balance', 0)
                user['balance'] = old_balance + bonus
                
                user['last_activity_bonus'] = {
                    'amount': bonus,
                    'type': 'orders_bonus',
                    'description': description,
                    'date': datetime.now().isoformat(),
                    'criteria': f"{data['orders']} órdenes × ${amount_per_order:.2f}"
                }
                
                print(f"✅ {user.get('username')}: +${bonus:.2f} ({data['orders']} órdenes)")
                successful += 1
            
            if self.save_users():
                print(f"\n🎉 {successful} usuarios recompensados exitosamente!")
            else:
                print("❌ Error guardando cambios.")
        else:
            print("❌ Operación cancelada.")

    def automatic_rewards_menu(self):
        """Menú de envíos automáticos y recompensas"""
        while True:
            print("\n" + "=" * 50)
            print("🎁 ENVÍOS AUTOMÁTICOS Y RECOMPENSAS")
            print("=" * 50)
            print("1. 🔄 Sincronizar usuarios web")
            print("2. 💰 Envío masivo a usuarios registrados")
            print("3. 🏆 Recompensar usuarios activos")
            print("4. 📊 Ver usuarios con bonos recientes")
            print("5. ⬅️  Volver al menú principal")
            print("=" * 50)
            
            choice = input("Selecciona una opción (1-5): ").strip()
            
            if choice == "1":
                self.sync_web_users()
            elif choice == "2":
                self.auto_send_balance_to_registered()
            elif choice == "3":
                self.find_and_reward_active_users()
            elif choice == "4":
                self.show_recent_bonuses()
            elif choice == "5":
                break
            else:
                print("❌ Opción inválida")

    def show_recent_bonuses(self):
        """Mostrar usuarios con bonos recientes"""
        print("\n📊 USUARIOS CON BONOS RECIENTES")
        print("-" * 60)
        
        recent_bonuses = []
        
        for user in self.users:
            username = user.get('username', 'N/A')
            
            # Verificar último bono automático
            if 'last_auto_bonus' in user:
                bonus = user['last_auto_bonus']
                recent_bonuses.append({
                    'username': username,
                    'type': 'Bono Automático',
                    'amount': bonus.get('amount', 0),
                    'date': bonus.get('date', ''),
                    'description': bonus.get('description', '')
                })
            
            # Verificar último bono de actividad
            if 'last_activity_bonus' in user:
                bonus = user['last_activity_bonus']
                recent_bonuses.append({
                    'username': username,
                    'type': 'Bono Actividad',
                    'amount': bonus.get('amount', 0),
                    'date': bonus.get('date', ''),
                    'description': bonus.get('description', '')
                })
        
        if not recent_bonuses:
            print("❌ No hay bonos recientes registrados.")
            return
        
        # Ordenar por fecha (más recientes primero)
        recent_bonuses.sort(key=lambda x: x['date'], reverse=True)
        
        print(f"{'Usuario':<20} {'Tipo':<15} {'Cantidad':<12} {'Fecha':<12}")
        print("-" * 60)
        
        for bonus in recent_bonuses[:20]:  # Mostrar últimos 20
            username = bonus['username'][:18]
            bonus_type = bonus['type'][:13]
            amount = f"${bonus['amount']:.2f}"
            date = bonus['date'][:10]
            
            print(f"{username:<20} {bonus_type:<15} {amount:<12} {date:<12}")
        
        if len(recent_bonuses) > 20:
            print(f"\n... y {len(recent_bonuses) - 20} bonos más")

def main():
    """Función principal"""
    admin = JorlingAdmin()
    
    print("🚀 JORLING SEGUIDORES 2025 - SISTEMA DE ADMINISTRACIÓN")
    print("=" * 60)
    
    if admin.authenticate_admin():
        admin.show_main_menu()
    else:
        print("🚫 Acceso denegado.")

if __name__ == "__main__":
    main()
