// @ts-ignore
import sidebarToggleScript from "./scripts/sidebarToggle.inline"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

const SidebarToggle: QuartzComponent = (_props: QuartzComponentProps) => {
  return (
    <button
      class="sidebar-toggle"
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

SidebarToggle.afterDOMLoaded = sidebarToggleScript

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
  flex-shrink: 0;
}

.sidebar-toggle:hover {
  background: var(--lightgray);
  color: var(--dark);
}

.sidebar-toggle-icon {
  transition: transform 0.2s ease;
}

/* When sidebar is hidden - keep button visible */
body.sidebar-hidden .sidebar-toggle {
  position: fixed !important;
  top: 1rem;
  left: 1rem;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}

body.sidebar-hidden .sidebar-toggle-icon {
  transform: scaleX(-1);
}

body.sidebar-hidden .left {
  display: none !important;
}

body.sidebar-hidden .page {
  grid-template-columns: 1fr !important;
}

body.sidebar-hidden .center {
  margin-left: auto;
  margin-right: auto;
  max-width: 100%;
  padding-left: 2rem;
  padding-right: 2rem;
}

@media all and (max-width: 800px) {
  .sidebar-toggle {
    display: none;
  }
}
`

export default (() => SidebarToggle) satisfies QuartzComponentConstructor
