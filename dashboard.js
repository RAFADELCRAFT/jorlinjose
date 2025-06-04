// Variables del dashboard
let currentSection = "nueva-orden"
const serviceData = {
  instagram: {
    followers: { price: 0.015, min: 100 },
    likes: { price: 0.008, min: 100 },
    views: { price: 0.005, min: 500 },
  },
  tiktok: {
    followers: { price: 0.012, min: 100 },
    likes: { price: 0.007, min: 100 },
    views: { price: 0.003, min: 1000 },
  },
  youtube: {
    subscribers: { price: 0.025, min: 100 },
    likes: { price: 0.01, min: 100 },
    views: { price: 0.006, min: 500 },
  },
  facebook: {
    followers: { price: 0.014, min: 100 },
    likes: { price: 0.006, min: 100 },
    views: { price: 0.004, min: 500 },
  },
  twitter: {
    followers: { price: 0.018, min: 100 },
    likes: { price: 0.009, min: 100 },
    retweets: { price: 0.013, min: 50 },
  },
  whatsapp: {
    members: { price: 0.035, min: 50 },
    groups: { price: 0.025, min: 10 },
  },
}

let currentUser = null
const orders = JSON.parse(localStorage.getItem("orders")) || []
const users = JSON.parse(localStorage.getItem("users")) || []

// Inicializar dashboard
document.addEventListener("DOMContentLoaded", () => {
  checkDashboardAuth()
  loadDashboard()
  setupDashboardEvents()
})

// Verificar autenticación del dashboard
function checkDashboardAuth() {
  const savedUser = localStorage.getItem("currentUser")
  if (!savedUser) {
    window.location.href = "index.html"
    return
  }
  currentUser = JSON.parse(savedUser)
}

// Cargar dashboard
function loadDashboard() {
  if (!currentUser) return

  // Actualizar información del usuario
  document.getElementById("username").textContent = currentUser.username
  document.getElementById("userBalance").textContent = currentUser.balance.toFixed(2)

  // Cargar órdenes del usuario
  loadUserOrders()

  // Configurar formulario de orden
  setupOrderForm()
}

// Configurar eventos del dashboard
function setupDashboardEvents() {
  // Formulario de orden
  const orderForm = document.getElementById("orderForm")
  if (orderForm) {
    orderForm.addEventListener("submit", handleNewOrder)
  }

  // Cambio de plataforma
  const platformSelect = document.getElementById("platform")
  if (platformSelect) {
    platformSelect.addEventListener("change", updateServiceOptions)
  }

  // Cambio de servicio
  const serviceSelect = document.getElementById("service")
  if (serviceSelect) {
    serviceSelect.addEventListener("change", updatePrice)
  }

  // Cambio de cantidad
  const quantityInput = document.getElementById("quantity")
  if (quantityInput) {
    quantityInput.addEventListener("input", updatePrice)
  }

  // Formulario de reembolso
  const refundForm = document.getElementById("refundForm")
  if (refundForm) {
    refundForm.addEventListener("submit", handleRefundRequest)
  }
}

// Toggle sidebar
function toggleSidebar() {
  const sidebar = document.getElementById("sidebar")
  sidebar.classList.toggle("active")
}

// Mostrar sección
function showSection(sectionId) {
  // Ocultar todas las secciones
  document.querySelectorAll(".dashboard-section").forEach((section) => {
    section.classList.remove("active")
  })

  // Mostrar sección seleccionada
  document.getElementById(sectionId).classList.add("active")

  // Actualizar navegación
  document.querySelectorAll(".nav-item").forEach((item) => {
    item.classList.remove("active")
  })
  event.target.classList.add("active")

  // Cerrar sidebar en móvil
  document.getElementById("sidebar").classList.remove("active")

  currentSection = sectionId
}

// Configurar formulario de orden
function setupOrderForm() {
  updateServiceOptions()
}

// Actualizar opciones de servicio
function updateServiceOptions() {
  const platform = document.getElementById("platform").value
  const serviceSelect = document.getElementById("service")

  serviceSelect.innerHTML = '<option value="">Seleccionar servicio</option>'

  if (platform && serviceData[platform]) {
    Object.keys(serviceData[platform]).forEach((service) => {
      const option = document.createElement("option")
      option.value = service
      option.textContent = service.charAt(0).toUpperCase() + service.slice(1)
      serviceSelect.appendChild(option)
    })
  }

  updatePrice()
}

// Actualizar precio
function updatePrice() {
  const platform = document.getElementById("platform").value
  const service = document.getElementById("service").value
  const quantity = Number.parseInt(document.getElementById("quantity").value) || 0
  const priceInput = document.getElementById("price")

  if (platform && service && serviceData[platform] && serviceData[platform][service]) {
    const pricePerUnit = serviceData[platform][service].price
    const totalPrice = (quantity * pricePerUnit).toFixed(2)
    priceInput.value = `$${totalPrice}`
  } else {
    priceInput.value = "$0.00"
  }
}

// Manejar nueva orden
function handleNewOrder(e) {
  e.preventDefault()

  const platform = document.getElementById("platform").value
  const service = document.getElementById("service").value
  const quantity = Number.parseInt(document.getElementById("quantity").value)
  const targetUrl = document.getElementById("targetUrl").value

  if (!platform || !service || !quantity || !targetUrl) {
    showNotification("Por favor completa todos los campos", "error")
    return
  }

  const pricePerUnit = serviceData[platform][service].price
  const totalPrice = quantity * pricePerUnit

  if (currentUser.balance < totalPrice) {
    showNotification(`Saldo insuficiente. Necesitas $${totalPrice.toFixed(2)}`, "error")
    return
  }

  // Crear nueva orden
  const newOrder = {
    id: "order_" + Date.now(),
    userId: currentUser.id,
    platform: platform,
    service: service,
    quantity: quantity,
    price: totalPrice,
    targetUrl: targetUrl,
    status: "pending",
    createdAt: new Date().toISOString(),
  }

  // Actualizar saldo del usuario
  currentUser.balance -= totalPrice
  updateUserInStorage()

  // Guardar orden
  orders.push(newOrder)
  saveOrders()

  // Actualizar UI
  document.getElementById("userBalance").textContent = currentUser.balance.toFixed(2)
  loadUserOrders()

  // Limpiar formulario
  document.getElementById("orderForm").reset()
  updatePrice()

  showNotification("¡Orden creada exitosamente!", "success")

  // Simular procesamiento
  setTimeout(
    () => {
      processOrder(newOrder.id)
    },
    Math.random() * 30000 + 10000,
  ) // 10-40 segundos
}

// Procesar orden
function processOrder(orderId) {
  const orderIndex = orders.findIndex((o) => o.id === orderId)
  if (orderIndex !== -1) {
    orders[orderIndex].status = "processing"
    saveOrders()
    loadUserOrders()

    // Completar orden después de un tiempo
    setTimeout(
      () => {
        orders[orderIndex].status = "completed"
        orders[orderIndex].completedAt = new Date().toISOString()
        saveOrders()
        loadUserOrders()
        showNotification("¡Orden completada!", "success")
      },
      Math.random() * 60000 + 30000,
    ) // 30-90 segundos
  }
}

// Cargar órdenes del usuario
function loadUserOrders() {
  const userOrders = orders.filter((order) => order.userId === currentUser.id)
  const tableBody = document.getElementById("ordersTableBody")

  if (!tableBody) return

  tableBody.innerHTML = ""

  if (userOrders.length === 0) {
    tableBody.innerHTML =
      '<tr><td colspan="8" style="text-align: center; color: var(--text-gray);">No tienes órdenes aún</td></tr>'
    return
  }

  userOrders.reverse().forEach((order) => {
    const row = document.createElement("tr")
    row.innerHTML = `
            <td>${order.id.substring(0, 8)}...</td>
            <td><i class="fab fa-${order.platform}"></i> ${order.platform}</td>
            <td>${order.service}</td>
            <td>${order.quantity.toLocaleString()}</td>
            <td>$${order.price.toFixed(2)}</td>
            <td><span class="status-${order.status}">${getStatusText(order.status)}</span></td>
            <td>${new Date(order.createdAt).toLocaleDateString()}</td>
            <td>
                ${order.status === "pending" ? '<button class="btn-secondary" onclick="cancelOrder(\'' + order.id + "')\">Cancelar</button>" : "-"}
            </td>
        `
    tableBody.appendChild(row)
  })
}

// Obtener texto del estado
function getStatusText(status) {
  const statusTexts = {
    pending: "Pendiente",
    processing: "Procesando",
    completed: "Completado",
    cancelled: "Cancelado",
  }
  return statusTexts[status] || status
}

// Cancelar orden
function cancelOrder(orderId) {
  const orderIndex = orders.findIndex((o) => o.id === orderId)
  if (orderIndex !== -1 && orders[orderIndex].status === "pending") {
    // Reembolsar al usuario
    currentUser.balance += orders[orderIndex].price
    updateUserInStorage()

    // Cancelar orden
    orders[orderIndex].status = "cancelled"
    saveOrders()

    // Actualizar UI
    document.getElementById("userBalance").textContent = currentUser.balance.toFixed(2)
    loadUserOrders()

    showNotification("Orden cancelada y reembolsada", "success")
  }
}

// Manejar solicitud de reembolso
function handleRefundRequest(e) {
  e.preventDefault()

  const orderId = document.getElementById("refundOrderId").value
  const reason = document.getElementById("refundReason").value

  const order = orders.find((o) => o.id.includes(orderId) && o.userId === currentUser.id)

  if (!order) {
    showNotification("Orden no encontrada", "error")
    return
  }

  if (order.status !== "completed") {
    showNotification("Solo se pueden reembolsar órdenes completadas", "error")
    return
  }

  // Simular solicitud de reembolso
  showNotification("Solicitud de reembolso enviada. Te contactaremos pronto.", "success")
  document.getElementById("refundForm").reset()
}

// Contactar soporte
function contactSupport(method) {
  const messages = {
    paypal: "Hola, quiero añadir fondos via PayPal",
    card: "Hola, quiero añadir fondos con tarjeta de crédito",
    crypto: "Hola, quiero añadir fondos con criptomonedas",
  }

  const message = encodeURIComponent(messages[method] || "Hola, necesito ayuda")
  window.open(`https://wa.me/573234135603?text=${message}`, "_blank")
}

// Actualizar usuario en storage
function updateUserInStorage() {
  localStorage.setItem("currentUser", JSON.stringify(currentUser))

  // Actualizar en la lista de usuarios
  const userIndex = users.findIndex((u) => u.id === currentUser.id)
  if (userIndex !== -1) {
    users[userIndex] = currentUser
    saveUsers()
  }
}

// Cerrar sesión
function logout() {
  localStorage.removeItem("currentUser")
  currentUser = null
  window.location.href = "index.html"
}

// Guardar usuarios
function saveUsers() {
  localStorage.setItem("users", JSON.stringify(users))
}

// Guardar órdenes
function saveOrders() {
  localStorage.setItem("orders", JSON.stringify(orders))
}

// Mostrar notificación
function showNotification(message, type = "info") {
  const notification = document.createElement("div")
  notification.className = `notification ${type}`
  notification.innerHTML = `
        <i class="fas fa-${type === "success" ? "check-circle" : type === "error" ? "exclamation-circle" : "info-circle"}"></i>
        ${message}
    `

  document.body.appendChild(notification)

  setTimeout(() => {
    notification.remove()
  }, 4000)
}
