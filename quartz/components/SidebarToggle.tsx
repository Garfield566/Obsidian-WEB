import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

const SidebarToggle: QuartzComponent = (_props: QuartzComponentProps) => {
  return (
    <button
      class="sidebar-toggle"
      id="sidebar-toggle"
      aria-label="Toggle sidebar"
      title="Masquer/Afficher le panneau"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="20"
        height="20"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
        class="sidebar-toggle-icon"
      >
        <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
        <line x1="9" y1="3" x2="9" y2="21"></line>
      </svg>
    </button>
  )
}

SidebarToggle.css = `
.sidebar-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  padding: 0;
  background: var(--light);
  border: 1px solid var(--lightgray);
  border-radius: 8px;
  cursor: pointer;
  color: var(--darkgray);
  transition: all 0.2s ease;
}

.sidebar-toggle:hover {
  background: var(--lightgray);
  color: var(--dark);
}

.sidebar-toggle-icon {
  transition: transform 0.2s ease;
}

/* When sidebar is hidden */
body.sidebar-hidden .sidebar-toggle-icon {
  transform: scaleX(-1);
}

body.sidebar-hidden .left {
  display: none !important;
}

body.sidebar-hidden .center {
  grid-column: 1 / -1 !important;
  max-width: 100% !important;
}

body.sidebar-hidden .page {
  grid-template-columns: 1fr !important;
}

@media all and (max-width: 800px) {
  .sidebar-toggle {
    display: none;
  }
}
`

SidebarToggle.afterDOMLoaded = `
document.addEventListener("DOMContentLoaded", () => {
  const toggleBtn = document.getElementById("sidebar-toggle");
  if (!toggleBtn) return;

  // Restore saved state
  const savedState = localStorage.getItem("sidebar-hidden");
  if (savedState === "true") {
    document.body.classList.add("sidebar-hidden");
  }

  toggleBtn.addEventListener("click", () => {
    document.body.classList.toggle("sidebar-hidden");
    const isHidden = document.body.classList.contains("sidebar-hidden");
    localStorage.setItem("sidebar-hidden", isHidden.toString());
  });
});
`

export default (() => SidebarToggle) satisfies QuartzComponentConstructor
