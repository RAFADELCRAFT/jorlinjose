#!/usr/bin/env python3
"""
Procesador de Órdenes - Jorling Seguidores 2025
Sistema automático para procesar órdenes de usuarios
"""

import json
import os
import time
import random
from datetime import datetime, timedelta

class OrderProcessor:
    def __init__(self):
        self.data_dir = "data"
        self.orders_file = os.path.join(self.data_dir, "orders.json")
        self.users_file = os.path.join(self.data_dir, "users.json")
        
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        self.orders = self.load_orders()
        self.users = self.load_users()
        
        # Configuración de procesamiento por plataforma
        self.processing_config = {
            'instagram': {
                'followers': {'speed': 100, 'delay': 2},
                'likes': {'speed': 200, 'delay': 1},
                'views': {'speed': 500, 'delay': 0.5}
            },
            'tiktok': {
                'followers': {'speed': 150, 'delay': 1.5},
                'likes': {'speed': 300, 'delay': 0.8},
                'views': {'speed': 1000, 'delay': 0.3}
            },
            'youtube': {
                'subscribers': {'speed': 50, 'delay': 3},
                'likes': {'speed': 100, 'delay': 2},
                'views': {'speed': 200, 'delay': 1}
            },
            'facebook': {
                'followers': {'speed': 80, 'delay': 2.5},
                'likes': {'speed': 150, 'delay': 1.5},
                'views': {'speed': 300, 'delay': 1}
            },
            'twitter': {
                'followers': {'speed': 60, 'delay': 3},
                'likes': {'speed': 120, 'delay': 2},
                'retweets': {'speed': 80, 'delay': 2.5}
            },
            'whatsapp': {
                'members': {'speed': 20, 'delay': 5},
                'groups': {'speed': 10, 'delay': 8}
            }
        }
    
    def load_orders(self):
        """Cargar órdenes"""
        try:
            if os.path.exists(self.orders_file):
                with open(self.orders_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error cargando órdenes: {e}")
            return []
    
    def save_orders(self):
        """Guardar órdenes"""
        try:
            with open(self.orders_file, 'w', encoding='utf-8') as f:
                json.dump(self.orders, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error guardando órdenes: {e}")
            return False
    
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
    
    def get_pending_orders(self):
        """Obtener órdenes pendientes"""
        return [order for order in self.orders if order.get('status') == 'pending']
    
    def get_processing_orders(self):
        """Obtener órdenes en procesamiento"""
        return [order for order in self.orders if order.get('status') == 'processing']
    
    def process_order(self, order):
        """Procesar una orden específica"""
        order_id = order.get('id', 'N/A')
        platform = order.get('platform', '')
        service = order.get('service', '')
        quantity = order.get('quantity', 0)
        target_url = order.get('targetUrl', '')
        
        print(f"\n🤖 PROCESANDO ORDEN: {order_id[:15]}...")
        print(f"📱 Plataforma: {platform.upper()}")
        print(f"🎯 Servicio: {service}")
        print(f"📊 Cantidad: {quantity:,}")
        print(f"🔗 Objetivo: {target_url}")
        print("-" * 50)
        
        # Cambiar estado a procesando
        order['status'] = 'processing'
        order['startedAt'] = datetime.now().isoformat()
        self.save_orders()
        
        # Obtener configuración de procesamiento
        config = self.processing_config.get(platform, {}).get(service, {'speed': 100, 'delay': 2})
        speed = config['speed']  # unidades por lote
        delay = config['delay']  # segundos entre lotes
        
        # Calcular tiempo estimado
        total_batches = max(1, quantity // speed)
        estimated_time = total_batches * delay
        
        print(f"⏱️ Tiempo estimado: {estimated_time/60:.1f} minutos")
        print(f"📦 Procesando en lotes de {speed}")
        print("")
        
        # Simular procesamiento por lotes
        processed = 0
        batch_number = 1
        
        while processed < quantity:
            batch_size = min(speed, quantity - processed)
            
            print(f"📦 Lote {batch_number}: Procesando {batch_size} unidades...")
            
            # Simular tiempo de procesamiento
            time.sleep(delay)
            
            processed += batch_size
            progress = (processed / quantity) * 100
            
            print(f"⏳ Progreso: {processed:,}/{quantity:,} ({progress:.1f}%)")
            
            # Simular variaciones en el procesamiento
            if random.random() < 0.1:  # 10% probabilidad de pausa
                pause_time = random.uniform(2, 5)
                print(f"⏸️ Pausa de seguridad: {pause_time:.1f}s")
                time.sleep(pause_time)
            
            batch_number += 1
        
        # Completar orden
        order['status'] = 'completed'
        order['completedAt'] = datetime.now().isoformat()
        order['deliveredQuantity'] = quantity
        
        print(f"\n✅ ¡ORDEN COMPLETADA!")
        print(f"📊 Entregado: {quantity:,} {service}")
        print(f"⏱️ Tiempo total: {(datetime.now() - datetime.fromisoformat(order['startedAt'])).total_seconds()/60:.1f} minutos")
        
        self.save_orders()
        return True
    
    def auto_process_pending_orders(self):
        """Procesar automáticamente órdenes pendientes"""
        pending_orders = self.get_pending_orders()
        
        if not pending_orders:
            print("📋 No hay órdenes pendientes para procesar")
            return
        
        print(f"🚀 PROCESAMIENTO AUTOMÁTICO INICIADO")
        print(f"📋 {len(pending_orders)} órdenes pendientes encontradas")
        print("=" * 60)
        
        for i, order in enumerate(pending_orders, 1):
            print(f"\n📋 ORDEN {i}/{len(pending_orders)}")
            
            try:
                self.process_order(order)
                
                # Pausa entre órdenes
                if i < len(pending_orders):
                    pause_time = random.uniform(5, 15)
                    print(f"\n⏳ Esperando {pause_time:.1f}s antes de la siguiente orden...")
                    time.sleep(pause_time)
                    
            except KeyboardInterrupt:
                print("\n⏹️ Procesamiento interrumpido por el usuario")
                break
            except Exception as e:
                print(f"\n❌ Error procesando orden: {e}")
                order['status'] = 'error'
                order['error'] = str(e)
                self.save_orders()
        
        print(f"\n🏁 PROCESAMIENTO COMPLETADO")
    
    def show_order_status(self):
        """Mostrar estado de órdenes"""
        print("\n📊 ESTADO DE ÓRDENES")
        print("=" * 60)
        
        if not self.orders:
            print("No hay órdenes registradas")
            return
        
        # Contar por estado
        status_counts = {}
        for order in self.orders:
            status = order.get('status', 'unknown')
            status_counts[status] = status_counts.get(status, 0) + 1
        
        print("📋 Resumen por estado:")
        for status, count in status_counts.items():
            emoji = {
                'pending': '⏳',
                'processing': '🔄',
                'completed': '✅',
                'cancelled': '❌',
                'error': '⚠️'
            }.get(status, '❓')
            print(f"   {emoji} {status}: {count}")
        
        # Mostrar órdenes recientes
        recent_orders = sorted(self.orders, key=lambda x: x.get('createdAt', ''), reverse=True)[:10]
        
        print(f"\n📋 Últimas 10 órdenes:")
        print("-" * 80)
        print(f"{'ID':<12} {'Usuario':<15} {'Plataforma':<12} {'Estado':<12} {'Fecha':<12}")
        print("-" * 80)
        
        for order in recent_orders:
            order_id = order.get('id', 'N/A')[:10] + "..."
            user_id = order.get('userId', '')
            username = self.get_username_by_id(user_id)[:13]
            platform = order.get('platform', 'N/A')[:10]
            status = order.get('status', 'N/A')[:10]
            created_date = order.get('createdAt', '')[:10]
            
            print(f"{order_id:<12} {username:<15} {platform:<12} {status:<12} {created_date:<12}")
    
    def get_username_by_id(self, user_id):
        """Obtener nombre de usuario por ID"""
        user = next((u for u in self.users if u.get('id') == user_id), None)
        return user.get('username', 'Usuario eliminado') if user else 'N/A'
    
    def manual_process_order(self):
        """Procesar orden manualmente"""
        pending_orders = self.get_pending_orders()
        
        if not pending_orders:
            print("📋 No hay órdenes pendientes")
            return
        
        print("\n📋 ÓRDENES PENDIENTES:")
        print("-" * 50)
        
        for i, order in enumerate(pending_orders, 1):
            username = self.get_username_by_id(order.get('userId', ''))
            print(f"{i}. {order.get('id')[:15]}... - {username} - {order.get('platform')} - {order.get('service')}")
        
        try:
            choice = int(input("\nSelecciona orden a procesar (número): ")) - 1
            selected_order = pending_orders[choice]
            self.process_order(selected_order)
        except (ValueError, IndexError):
            print("❌ Selección inválida")

def main():
    """Función principal"""
    processor = OrderProcessor()
    
    print("🤖 PROCESADOR DE ÓRDENES - JORLING SEGUIDORES 2025")
    print("=" * 60)
    
    while True:
        print("\n📋 OPCIONES DISPONIBLES:")
        print("1. 🚀 Procesar todas las órdenes pendientes")
        print("2. 🎯 Procesar orden específica")
        print("3. 📊 Ver estado de órdenes")
        print("4. 🔄 Recargar datos")
        print("5. 🚪 Salir")
        print("=" * 60)
        
        choice = input("Selecciona una opción (1-5): ").strip()
        
        if choice == "1":
            processor.auto_process_pending_orders()
        elif choice == "2":
            processor.manual_process_order()
        elif choice == "3":
            processor.show_order_status()
        elif choice == "4":
            processor.orders = processor.load_orders()
            processor.users = processor.load_users()
            print("✅ Datos recargados")
        elif choice == "5":
            print("\n👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida")

if __name__ == "__main__":
    main()
