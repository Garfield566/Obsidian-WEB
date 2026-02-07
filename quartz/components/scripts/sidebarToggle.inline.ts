// Restore saved state immediately
const savedState = localStorage.getItem("sidebar-hidden")
if (savedState === "true") {
  document.body.classList.add("sidebar-hidden")
}

// Handle navigation (SPA)
document.addEventListener("nav", () => {
  const toggleSidebar = () => {
    document.body.classList.toggle("sidebar-hidden")
    const isHidden = document.body.classList.contains("sidebar-hidden")
    localStorage.setItem("sidebar-hidden", isHidden.toString())
  }

  // Restore state on each navigation
  const savedState = localStorage.getItem("sidebar-hidden")
  if (savedState === "true") {
    document.body.classList.add("sidebar-hidden")
  } else {
    document.body.classList.remove("sidebar-hidden")
  }

  // Add click handlers to all toggle buttons
  for (const toggleBtn of document.getElementsByClassName("sidebar-toggle")) {
    toggleBtn.addEventListener("click", toggleSidebar)
    window.addCleanup(() => toggleBtn.removeEventListener("click", toggleSidebar))
  }
})
