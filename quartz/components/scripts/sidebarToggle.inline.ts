// Restore saved state immediately on page load
const savedState = localStorage.getItem("sidebar-hidden")
if (savedState === "true") {
  document.body.classList.add("sidebar-hidden")
}

// Handle click events
document.addEventListener("nav", () => {
  // Restore state
  const saved = localStorage.getItem("sidebar-hidden")
  if (saved === "true") {
    document.body.classList.add("sidebar-hidden")
  }

  // Setup click handlers
  const buttons = document.querySelectorAll(".sidebar-toggle")
  buttons.forEach((btn) => {
    const handleClick = (e: Event) => {
      e.preventDefault()
      e.stopPropagation()
      document.body.classList.toggle("sidebar-hidden")
      const isHidden = document.body.classList.contains("sidebar-hidden")
      localStorage.setItem("sidebar-hidden", String(isHidden))
    }
    btn.removeEventListener("click", handleClick as EventListener)
    btn.addEventListener("click", handleClick as EventListener)
  })
})
