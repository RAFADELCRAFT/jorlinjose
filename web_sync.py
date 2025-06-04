#!/usr/bin/env python3
"""
Sincronizador Web - Jorling Seguidores 2025
Sincroniza usuarios entre la web y el sistema Python
"""

import json
import os
import sqlite3
from datetime import datetime

class WebSyncManager:
    def __init__(self):
        self.data_dir = "data"
        self.web_users_file = os.path.join(self.data_dir, "web_users.json")
        self.python_users_file = os.path.join(self.data_dir, "users.json")
        
        # Crear directorio si no existe
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def extract_from_web_database(self, db_path="web_database.db"):
        """Extraer usuarios desde base de datos web (SQLite)"""
        try:
            if not os.path.exists(db_path):
                print(f"❌ Base de datos web no encontrada: {db_path}")
                return False
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Obtener usuarios de la tabla web
            cursor.execute("""
                SELECT id, username, email, password, balance, isAdmin, createdAt 
                FROM users
            """)
            
            web_users = []
            for row in cursor.fetchall():
                user = {
                    'id': row[0],
                    'username': row[1],
                    'email': row[2],
                    'password': row[3],
                    'balance': float(row[4]) if row[4] else 0,
                    'isAdmin': bool(row[5]) if row[5] else False,
                    'createdAt': row[6] if row[6] else datetime.now().isoformat()
                }
                web_users.append(user)
            
            conn.close()
            
            # Guardar en archivo JSON
            with open(self.web_users_file, 'w', encoding='utf-8') as f:
                json.dump(web_users, f, indent=2, ensure_ascii=False)
            
            print(f"✅ {len(web_users)} usuarios extraídos de la base de datos web.")
            return True
            
        except Exception as e:
            print(f"❌ Error extrayendo usuarios web: {e}")
            return False
    
    def extract_from_web_json(self, json_path="web_users_export.json"):
        """Extraer usuarios desde archivo JSON exportado de la web"""
        try:
            if not os.path.exists(json_path):
                print(f"❌ Archivo JSON web no encontrado: {json_path}")
                return False
            
            with open(json_path, 'r', encoding='utf-8') as f:
                web_users = json.load(f)
            
            # Normalizar formato si es necesario
            normalized_users = []
            for user in web_users:
                normalized_user = {
                    'id': user.get('id', f'web_{int(datetime.now().timestamp())}'),
                    'username': user.get('username', ''),
                    'email': user.get('email', ''),
                    'password': user.get('password', ''),
                    'balance': float(user.get('balance', 0)),
                    'isAdmin': bool(user.get('isAdmin', False)),
                    'createdAt': user.get('createdAt', datetime.now().isoformat())
                }
                normalized_users.append(normalized_user)
            
            # Guardar archivo normalizado
            with open(self.web_users_file, 'w', encoding='utf-8') as f:
                json.dump(normalized_users, f, indent=2, ensure_ascii=False)
            
            print(f"✅ {len(normalized_users)} usuarios importados desde JSON web.")
            return True
            
        except Exception as e:
            print(f"❌ Error importando usuarios desde JSON: {e}")
            return False
    
    def sync_to_python_system(self):
        """Sincronizar usuarios web al sistema Python"""
        try:
            # Cargar usuarios web
            if not os.path.exists(self.web_users_file):
                print("❌ No hay usuarios web para sincronizar.")
                return False
            
            with open(self.web_users_file, 'r', encoding='utf-8') as f:
                web_users = json.load(f)
            
            # Cargar usuarios Python existentes
            python_users = []
            if os.path.exists(self.python_users_file):
                with open(self.python_users_file, 'r', encoding='utf-8') as f:
                    python_users = json.load(f)
            
            # Sincronizar
            synced_count = 0
            updated_count = 0
            
            for web_user in web_users:
                # Buscar usuario existente por email
                existing_user = next((u for u in python_users if u.get('email') == web_user.get('email')), None)
                
                if not existing_user:
                    # Agregar nuevo usuario
                    python_users.append(web_user)
                    synced_count += 1
                    print(f"➕ Nuevo usuario: {web_user.get('username')}")
                else:
                    # Actualizar usuario existente si hay cambios
                    changes = []
                    
                    if existing_user.get('username') != web_user.get('username'):
                        existing_user['username'] = web_user.get('username')
                        changes.append('username')
                    
                    if existing_user.get('balance') != web_user.get('balance'):
                        existing_user['balance'] = web_user.get('balance')
                        changes.append('balance')
                    
                    if changes:
                        updated_count += 1
                        print(f"🔄 Actualizado {existing_user.get('username')}: {', '.join(changes)}")
            
            # Guardar usuarios actualizados
            with open(self.python_users_file, 'w', encoding='utf-8') as f:
                json.dump(python_users, f, indent=2, ensure_ascii=False)
            
            print(f"\n✅ Sincronización completada:")
            print(f"   Nuevos usuarios: {synced_count}")
            print(f"   Usuarios actualizados: {updated_count}")
            print(f"   Total usuarios: {len(python_users)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error sincronizando al sistema Python: {e}")
            return False
    
    def create_sample_web_users(self):
        """Crear usuarios de muestra para pruebas"""
        sample_users = [
            {
                'id': 'web_user_001',
                'username': 'carlos_gamer',
                'email': 'carlos@email.com',
                'password': 'hashed_password_123',
                'balance': 25.50,
                'isAdmin': False,
                'createdAt': '2024-12-01T10:30:00'
            },
            {
                'id': 'web_user_002',
                'username': 'maria_influencer',
                'email': 'maria@email.com',
                'password': 'hashed_password_456',
                'balance': 150.00,
                'isAdmin': False,
                'createdAt': '2024-12-02T14:15:00'
            },
            {
                'id': 'web_user_003',
                'username': 'pedro_business',
                'email': 'pedro@email.com',
                'password': 'hashed_password_789',
                'balance': 75.25,
                'isAdmin': False,
                'createdAt': '2024-12-03T09:45:00'
            }
        ]
        
        with open(self.web_users_file, 'w', encoding='utf-8') as f:
            json.dump(sample_users, f, indent=2, ensure_ascii=False)
        
        print(f"✅ {len(sample_users)} usuarios de muestra creados.")
        return True
    
    def show_sync_status(self):
        """Mostrar estado de sincronización"""
        print("\n📊 ESTADO DE SINCRONIZACIÓN")
        print("=" * 50)
        
        # Usuarios web
        web_count = 0
        if os.path.exists(self.web_users_file):
            with open(self.web_users_file, 'r', encoding='utf-8') as f:
                web_users = json.load(f)
                web_count = len(web_users)
        
        # Usuarios Python
        python_count = 0
        if os.path.exists(self.python_users_file):
            with open(self.python_users_file, 'r', encoding='utf-8') as f:
                python_users = json.load(f)
                python_count = len(python_users)
        
        print(f"👥 Usuarios en sistema web: {web_count}")
        print(f"🐍 Usuarios en sistema Python: {python_count}")
        
        if web_count > 0 and python_count > 0:
            sync_percentage = min((python_count / web_count) * 100, 100)
            print(f"🔄 Sincronización: {sync_percentage:.1f}%")
        
        # Archivos existentes
        print(f"\n📁 ARCHIVOS:")
        print(f"   Web users: {'✅' if os.path.exists(self.web_users_file) else '❌'}")
        print(f"   Python users: {'✅' if os.path.exists(self.python_users_file) else '❌'}")

def main():
    """Función principal del sincronizador"""
    sync_manager = WebSyncManager()
    
    print("🔄 SINCRONIZADOR WEB - JORLING SEGUIDORES 2025")
    print("=" * 60)
    
    while True:
        print("\n📋 OPCIONES DE SINCRONIZACIÓN:")
        print("1. 📊 Ver estado de sincronización")
        print("2. 🗄️  Extraer desde base de datos web (SQLite)")
        print("3. 📄 Importar desde archivo JSON web")
        print("4. 🔄 Sincronizar al sistema Python")
        print("5. 🧪 Crear usuarios de muestra")
        print("6. 🚀 Sincronización completa (JSON → Python)")
        print("7. 🚪 Salir")
        print("=" * 60)
        
        choice = input("Selecciona una opción (1-7): ").strip()
        
        if choice == "1":
            sync_manager.show_sync_status()
        
        elif choice == "2":
            db_path = input("Ruta de la base de datos web (web_database.db): ").strip()
            if not db_path:
                db_path = "web_database.db"
            sync_manager.extract_from_web_database(db_path)
        
        elif choice == "3":
            json_path = input("Ruta del archivo JSON web (web_users_export.json): ").strip()
            if not json_path:
                json_path = "web_users_export.json"
            sync_manager.extract_from_web_json(json_path)
        
        elif choice == "4":
            sync_manager.sync_to_python_system()
        
        elif choice == "5":
            sync_manager.create_sample_web_users()
        
        elif choice == "6":
            print("\n🚀 SINCRONIZACIÓN COMPLETA")
            print("-" * 30)
            
            # Intentar importar desde JSON primero
            json_path = input("Archivo JSON web (Enter para web_users_export.json): ").strip()
            if not json_path:
                json_path = "web_users_export.json"
            
            if sync_manager.extract_from_web_json(json_path):
                sync_manager.sync_to_python_system()
                print("\n🎉 Sincronización completa exitosa!")
            else:
                print("❌ Error en la sincronización completa.")
        
        elif choice == "7":
            print("\n👋 ¡Hasta luego!")
            break
        
        else:
            print("❌ Opción inválida.")

if __name__ == "__main__":
    main()
