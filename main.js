// Variables globales
let currentUser = null
const users = JSON.parse(localStorage.getItem("users")) || []
const orders = JSON.parse(localStorage.getItem("orders")) || []

// Inicialización
document.addEventListener("DOMContentLoaded", () => {
  initializeApp()
  startLiveStats()
  checkUserSession()
})

// Inicializar aplicación
function initializeApp() {
  // Crear usuario admin por defecto si no existe
  if (users.length === 0) {
    const adminUser = {
      id: "admin_" + Date.now(),
      username: "admin",
      email: "admin@jorling.com",
      password: hashPassword("admin123"),
      balance: 10000,
      isAdmin: true,
      createdAt: new Date().toISOString(),
    }
    users.push(adminUser)
    saveUsers()
  }

  // Configurar event listeners
  setupEventListeners()
}

// Configurar event listeners
function setupEventListeners() {
  // Formulario de login
  const loginForm = document.getElementById("loginForm")
  if (loginForm) {
    loginForm.addEventListener("submit", handleLogin)
  }

  // Formulario de registro
  const registerForm = document.getElementById("registerForm")
  if (registerForm) {
    registerForm.addEventListener("submit", handleRegister)
  }

  // Smooth scrolling para enlaces
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault()
      const target = document.querySelector(this.getAttribute("href"))
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        })
      }
    })
  })
}

// Estadísticas en tiempo real
function startLiveStats() {
  const liveViews = document.getElementById("liveViews")
  const liveFollowers = document.getElementById("liveFollowers")
  const liveOrders = document.getElementById("liveOrders")

  if (liveViews && liveFollowers && liveOrders) {
    setInterval(() => {
      // Simular incremento de estadísticas
      const currentViews = Number.parseInt(liveViews.textContent.replace(/,/g, ""))
      const currentFollowers = Number.parseInt(liveFollowers.textContent.replace(/,/g, ""))
      const currentOrders = Number.parseInt(liveOrders.textContent.replace(/,/g, ""))

      liveViews.textContent = (currentViews + Math.floor(Math.random() * 50) + 10).toLocaleString()
      liveFollowers.textContent = (currentFollowers + Math.floor(Math.random() * 5) + 1).toLocaleString()
      liveOrders.textContent = (currentOrders + Math.floor(Math.random() * 3) + 1).toLocaleString()
    }, 5000)
  }
}

// Hash de contraseña simple
function hashPassword(password) {
  return btoa(password + "jorling_salt_2025")
}

// Verificar sesión de usuario
function checkUserSession() {
  const savedUser = localStorage.getItem("currentUser")
  if (savedUser) {
    currentUser = JSON.parse(savedUser)
    if (window.location.pathname.includes("dashboard.html")) {
      loadDashboard()
    } else {
      // Redirigir al dashboard si ya está logueado
      window.location.href = "dashboard.html"
    }
  }
}

// Manejar login
function handleLogin(e) {
  e.preventDefault()

  const username = document.getElementById("loginUsername").value
  const password = document.getElementById("loginPassword").value

  const user = users.find((u) => u.username === username && u.password === hashPassword(password))

  if (user) {
    currentUser = user
    localStorage.setItem("currentUser", JSON.stringify(user))
    showNotification("¡Bienvenido de vuelta!", "success")
    setTimeout(() => {
      window.location.href = "dashboard.html"
    }, 1000)
  } else {
    showNotification("Usuario o contraseña incorrectos", "error")
  }
}

// Manejar registro
function handleRegister(e) {
  e.preventDefault()

  const username = document.getElementById("regUsername").value
  const email = document.getElementById("regEmail").value
  const password = document.getElementById("regPassword").value
  const confirmPassword = document.getElementById("regConfirmPassword").value

  // Validaciones
  if (password !== confirmPassword) {
    showNotification("Las contraseñas no coinciden", "error")
    return
  }

  if (users.find((u) => u.username === username)) {
    showNotification("El nombre de usuario ya existe", "error")
    return
  }

  if (users.find((u) => u.email === email)) {
    showNotification("El email ya está registrado", "error")
    return
  }

  // Crear nuevo usuario
  const newUser = {
    id: "user_" + Date.now(),
    username: username,
    email: email,
    password: hashPassword(password),
    balance: 0,
    isAdmin: false,
    createdAt: new Date().toISOString(),
  }

  users.push(newUser)
  saveUsers()

  showNotification("¡Cuenta creada exitosamente!", "success")
  closeModal("registerModal")
  showLoginModal()
}

// Guardar usuarios en localStorage
function saveUsers() {
  localStorage.setItem("users", JSON.stringify(users))
}

// Guardar órdenes en localStorage
function saveOrders() {
  localStorage.setItem("orders", JSON.stringify(orders))
}

// Mostrar modal de login
function showLoginModal() {
  closeModal("registerModal")
  document.getElementById("loginModal").style.display = "block"
}

// Mostrar modal de registro
function showRegisterModal() {
  closeModal("loginModal")
  document.getElementById("registerModal").style.display = "block"
}

// Cerrar modal
function closeModal(modalId) {
  document.getElementById(modalId).style.display = "none"
}

// Requerir login para servicios
function requireLogin() {
  if (!currentUser) {
    showNotification("Debes iniciar sesión para acceder a los servicios", "error")
    showLoginModal()
  } else {
    window.location.href = "dashboard.html"
  }
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

// Cerrar modales al hacer clic fuera
window.onclick = (event) => {
  const loginModal = document.getElementById("loginModal")
  const registerModal = document.getElementById("registerModal")

  if (event.target === loginModal) {
    closeModal("loginModal")
  }
  if (event.target === registerModal) {
    closeModal("registerModal")
  }
}
