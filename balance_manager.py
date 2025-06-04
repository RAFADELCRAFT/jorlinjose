#!/usr/bin/env python3
"""
Gestor de Saldos - Jorling Seguidores 2025
Sistema rápido para gestión de saldos de usuarios
"""

import json
import os
import base64
from datetime import datetime

class BalanceManager:
    def __init__(self):
        self.data_dir = "data"
        self.users_file = os.path.join(self.data_dir, "users.json")
        
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        self.users = self.load_users()
    
    def load_users(self):
        """Cargar usuarios"""
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error cargando usuarios: {e}")
            return []
    
    def save_users(self):
        """Guardar usuarios"""
        try:
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error guardando usuarios: {e}")
            return False
    
    def find_user(self, username):
        """Buscar usuario por nombre o email"""
        # Buscar por nombre de usuario exacto
        user = next((u for u in self.users if u.get('username', '').lower() == username.lower()), None)
        
        # Si no se encuentra, buscar por email
        if not user:
            user = next((u for u in self.users if u.get('email', '').lower() == username.lower()), None)
        
        # Si aún no se encuentra, buscar por coincidencia parcial en nombre de usuario
        if not user:
            user = next((u for u in self.users if username.lower() in u.get('username', '').lower()), None)
        
        return user
    
    def list_all_users(self):
        """Listar todos los usuarios disponibles"""
        print("\n📋 USUARIOS DISPONIBLES")
        print("-" * 60)
        
        if not self.users:
            print("No hay usuarios registrados.")
            return
        
        print(f"{'Usuario':<20} {'Email':<30} {'Saldo':<10}")
        print("-" * 60)
        
        for user in self.users:
            username = user.get('username', 'N/A')[:18]
            email = user.get('email', 'N/A')[:28]
            balance = f"${user.get('balance', 0):.2f}"
            
            print(f"{username:<20} {email:<30} {balance:<10}")
        
        print(f"\nTotal de usuarios: {len(self.users)}")
    
    def add_balance(self, username, amount):
        """Añadir saldo a usuario"""
        user = self.find_user(username)
        
        if not user:
            print(f"❌ Usuario '{username}' no encontrado")
            print("Usuarios disponibles:")
            self.list_all_users()
            return False
        
        old_balance = user.get('balance', 0)
        user['balance'] = old_balance + amount
        
        if self.save_users():
            print(f"✅ Saldo actualizado para {user.get('username')}")
            print(f"💰 Saldo anterior: ${old_balance:.2f}")
            print(f"💰 Cantidad añadida: ${amount:.2f}")
            print(f"💰 Nuevo saldo: ${user['balance']:.2f}")
            return True
        else:
            print("❌ Error al guardar cambios")
            return False
    
    def get_balance(self, username):
        """Obtener saldo de usuario"""
        user = self.find_user(username)
        if user:
            return user.get('balance', 0)
        return None
    
    def list_users_with_balance(self):
        """Listar usuarios con sus saldos"""
        print("\n💰 SALDOS DE USUARIOS")
        print("-" * 50)
        
        if not self.users:
            print("No hay usuarios registrados.")
            return
        
        # Filtrar solo usuarios regulares (no admins)
        regular_users = [u for u in self.users if not u.get('isAdmin', False)]
        
        if not regular_users:
            print("No hay usuarios regulares registrados.")
            return
        
        print(f"{'Usuario':<20} {'Email':<25} {'Saldo':<10}")
        print("-" * 50)
        
        for user in regular_users:
            username = user.get('username', 'N/A')[:18]
            email = user.get('email', 'N/A')[:23]
            balance = f"${user.get('balance', 0):.2f}"
            
            print(f"{username:<20} {email:<25} {balance:<10}")
        
        total_balance = sum(u.get('balance', 0) for u in regular_users)
        print("-" * 50)
        print(f"Total de usuarios: {len(regular_users)}")
        print(f"Saldo total: ${total_balance:.2f}")

def main():
    """Función principal para gestión rápida de saldos"""
    manager = BalanceManager()
    
    print("💰 GESTOR DE SALDOS - JORLING SEGUIDORES 2025")
    print("=" * 50)
    
    while True:
        print("\n📋 OPCIONES DISPONIBLES:")
        print("1. 💵 Añadir saldo a usuario")
        print("2. 💰 Ver saldo de usuario")
        print("3. 📋 Listar todos los usuarios")
        print("4. 🚪 Salir")
        print("=" * 50)
        
        choice = input("Selecciona una opción (1-4): ").strip()
        
        if choice == "1":
            print("\n💵 AÑADIR SALDO")
            print("-" * 30)
            username = input("Nombre de usuario o email: ").strip()
            
            if not username:
                print("❌ Nombre de usuario requerido")
                continue
            
            try:
                amount = float(input("Cantidad a añadir (USD): $"))
                if amount <= 0:
                    print("❌ La cantidad debe ser mayor a 0")
                    continue
            except ValueError:
                print("❌ Cantidad inválida")
                continue
            
            manager.add_balance(username, amount)
        
        elif choice == "2":
            print("\n💰 CONSULTAR SALDO")
            print("-" * 30)
            username = input("Nombre de usuario o email: ").strip()
            
            balance = manager.get_balance(username)
            if balance is not None:
                user = manager.find_user(username)
                print(f"💰 Saldo de {user.get('username')}: ${balance:.2f}")
            else:
                print(f"❌ Usuario '{username}' no encontrado")
                print("Usuarios disponibles:")
                manager.list_all_users()
        
        elif choice == "3":
            manager.list_users_with_balance()
        
        elif choice == "4":
            print("\n👋 ¡Hasta luego!")
            break
        
        else:
            print("❌ Opción inválida. Por favor selecciona 1-4.")

if __name__ == "__main__":
    main()
