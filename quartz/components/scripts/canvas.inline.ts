import { removeAllChildren } from "./util"
import { getFullSlug, resolveRelative } from "../../util/path"

interface CanvasNode {
  id: string
  type: "text" | "file" | "group" | "link"
  x: number
  y: number
  width: number
  height: number
  text?: string
  renderedHtml?: string
  file?: string
  url?: string
  color?: string
  label?: string
}

interface CanvasEdge {
  id: string
  fromNode: string
  fromSide: "top" | "bottom" | "left" | "right"
  toNode: string
  toSide: "top" | "bottom" | "left" | "right"
  color?: string
  label?: string
}

interface CanvasData {
  nodes: CanvasNode[]
  edges: CanvasEdge[]
}

function getAnchorPoint(node: CanvasNode, side: string): { x: number; y: number } {
  switch (side) {
    case "top":
      return { x: node.x + node.width / 2, y: node.y }
    case "bottom":
      return { x: node.x + node.width / 2, y: node.y + node.height }
    case "left":
      return { x: node.x, y: node.y + node.height / 2 }
    case "right":
      return { x: node.x + node.width, y: node.y + node.height / 2 }
    default:
      return { x: node.x + node.width / 2, y: node.y + node.height / 2 }
  }
}

function getSideDirection(side: string): { dx: number; dy: number } {
  switch (side) {
    case "top":
      return { dx: 0, dy: -1 }
    case "bottom":
      return { dx: 0, dy: 1 }
    case "left":
      return { dx: -1, dy: 0 }
    case "right":
      return { dx: 1, dy: 0 }
    default:
      return { dx: 0, dy: 0 }
  }
}

function buildEdgePath(
  from: { x: number; y: number },
  fromSide: string,
  to: { x: number; y: number },
  toSide: string,
): string {
  const dx = to.x - from.x
  const dy = to.y - from.y
  const dist = Math.sqrt(dx * dx + dy * dy)
  const offset = Math.min(dist * 0.4, 120)

  const fd = getSideDirection(fromSide)
  const td = getSideDirection(toSide)

  const cp1x = from.x + fd.dx * offset
  const cp1y = from.y + fd.dy * offset
  const cp2x = to.x + td.dx * offset
  const cp2y = to.y + td.dy * offset

  return `M ${from.x} ${from.y} C ${cp1x} ${cp1y}, ${cp2x} ${cp2y}, ${to.x} ${to.y}`
}

function renderCanvas(container: HTMLElement, slug: string) {
  const dataEl = document.getElementById("canvas-data")
  if (!dataEl || !dataEl.textContent) return

  let data: CanvasData
  try {
    data = JSON.parse(dataEl.textContent)
  } catch {
    return
  }

  if (!data.nodes || data.nodes.length === 0) return

  const nodeMap = new Map(data.nodes.map((n) => [n.id, n]))
  const viewport = container.querySelector(".canvas-viewport") as HTMLElement
  const nodesContainer = container.querySelector(".canvas-nodes") as HTMLElement
  const edgesSvg = container.querySelector(".canvas-edges") as SVGSVGElement

  if (!viewport || !nodesContainer || !edgesSvg) return

  removeAllChildren(nodesContainer)
  removeAllChildren(edgesSvg)

  // Compute bounding box
  let minX = Infinity,
    minY = Infinity,
    maxX = -Infinity,
    maxY = -Infinity
  for (const node of data.nodes) {
    minX = Math.min(minX, node.x)
    minY = Math.min(minY, node.y)
    maxX = Math.max(maxX, node.x + node.width)
    maxY = Math.max(maxY, node.y + node.height)
  }

  // Render groups first (they're background containers)
  const groups = data.nodes.filter((n) => n.type === "group")
  const others = data.nodes.filter((n) => n.type !== "group")

  for (const node of [...groups, ...others]) {
    const div = document.createElement("div")
    div.className = `canvas-node canvas-node-${node.type}`
    div.dataset.nodeId = node.id

    if (node.color) {
      if (node.color.startsWith("#")) {
        div.style.borderColor = node.color
        div.style.backgroundColor = node.color + "22"
      } else {
        div.classList.add(`canvas-color-${node.color}`)
      }
    }

    div.style.left = `${node.x}px`
    div.style.top = `${node.y}px`
    div.style.width = `${node.width}px`
    div.style.height = `${node.height}px`

    if (node.type === "text") {
      if (node.renderedHtml) {
        div.innerHTML = node.renderedHtml
      } else if (node.text) {
        div.textContent = node.text
      }
    } else if (node.type === "file") {
      const fileName = node.file?.split("/").pop()?.replace(/\.md$/, "") ?? "File"
      div.innerHTML = `<div class="canvas-file-icon">\u{1F4C4}</div><div class="canvas-file-title">${escapeHtml(fileName)}</div>`
      div.addEventListener("click", (e) => {
        e.stopPropagation()
        if (node.file) {
          const targ = resolveRelative(slug as any, node.file as any)
          window.spaNavigate(new URL(targ, window.location.toString()))
        }
      })
    } else if (node.type === "link") {
      const urlDisplay = node.url ? new URL(node.url).hostname : "Link"
      div.innerHTML = `<div class="canvas-link-icon">\u{1F310}</div><div class="canvas-link-title">${escapeHtml(node.label || urlDisplay)}</div>`
      div.addEventListener("click", (e) => {
        e.stopPropagation()
        if (node.url) {
          window.open(node.url, "_blank", "noopener")
        }
      })
    } else if (node.type === "group") {
      if (node.label) {
        div.innerHTML = `<div class="canvas-group-label">${escapeHtml(node.label)}</div>`
      }
    }

    nodesContainer.appendChild(div)
  }

  // Setup SVG for edges
  const svgPad = 100
  const svgX = minX - svgPad
  const svgY = minY - svgPad
  const svgW = maxX - minX + svgPad * 2
  const svgH = maxY - minY + svgPad * 2

  edgesSvg.setAttribute("viewBox", `${svgX} ${svgY} ${svgW} ${svgH}`)
  edgesSvg.style.left = `${svgX}px`
  edgesSvg.style.top = `${svgY}px`
  edgesSvg.style.width = `${svgW}px`
  edgesSvg.style.height = `${svgH}px`

  // Arrow marker definition
  const defs = document.createElementNS("http://www.w3.org/2000/svg", "defs")
  const marker = document.createElementNS("http://www.w3.org/2000/svg", "marker")
  marker.setAttribute("id", "canvas-arrowhead")
  marker.setAttribute("markerWidth", "8")
  marker.setAttribute("markerHeight", "6")
  marker.setAttribute("refX", "8")
  marker.setAttribute("refY", "3")
  marker.setAttribute("orient", "auto")
  const arrowPath = document.createElementNS("http://www.w3.org/2000/svg", "polygon")
  arrowPath.setAttribute("points", "0 0, 8 3, 0 6")
  arrowPath.setAttribute("class", "canvas-edge-arrow")
  marker.appendChild(arrowPath)
  defs.appendChild(marker)
  edgesSvg.appendChild(defs)

  // Render edges
  for (const edge of data.edges) {
    const fromNode = nodeMap.get(edge.fromNode)
    const toNode = nodeMap.get(edge.toNode)
    if (!fromNode || !toNode) continue

    const fromPt = getAnchorPoint(fromNode, edge.fromSide)
    const toPt = getAnchorPoint(toNode, edge.toSide)
    const pathD = buildEdgePath(fromPt, edge.fromSide, toPt, edge.toSide)

    const pathEl = document.createElementNS("http://www.w3.org/2000/svg", "path")
    pathEl.setAttribute("d", pathD)
    pathEl.setAttribute("class", "canvas-edge")
    pathEl.setAttribute("marker-end", "url(#canvas-arrowhead)")

    if (edge.color) {
      if (edge.color.startsWith("#")) {
        pathEl.style.stroke = edge.color
      } else {
        pathEl.style.stroke = `var(--canvas-color-${edge.color}-border)`
      }
    }

    edgesSvg.appendChild(pathEl)
  }

  // Pan & Zoom state
  let scale = 1
  let panX = 0
  let panY = 0
  let isDragging = false
  let dragStartX = 0
  let dragStartY = 0
  let panStartX = 0
  let panStartY = 0

  function applyTransform() {
    viewport.style.transform = `translate(${panX}px, ${panY}px) scale(${scale})`
  }

  function fitToView() {
    const cw = container.clientWidth
    const ch = container.clientHeight
    const contentWidth = maxX - minX
    const contentHeight = maxY - minY

    if (contentWidth === 0 || contentHeight === 0) return

    const padding = 60
    scale = Math.min((cw - padding * 2) / contentWidth, (ch - padding * 2) / contentHeight, 1.0)
    panX = (cw - contentWidth * scale) / 2 - minX * scale
    panY = (ch - contentHeight * scale) / 2 - minY * scale
    applyTransform()
  }

  // Zoom toward mouse position
  const onWheel = (e: WheelEvent) => {
    e.preventDefault()
    const rect = container.getBoundingClientRect()
    const mouseX = e.clientX - rect.left
    const mouseY = e.clientY - rect.top

    const zoomFactor = e.deltaY > 0 ? 0.9 : 1.1
    const newScale = Math.max(0.05, Math.min(8, scale * zoomFactor))

    panX = mouseX - (mouseX - panX) * (newScale / scale)
    panY = mouseY - (mouseY - panY) * (newScale / scale)
    scale = newScale
    applyTransform()
  }

  const onMouseDown = (e: MouseEvent) => {
    if ((e.target as HTMLElement).closest(".canvas-node-file, .canvas-node-link, .canvas-controls"))
      return
    isDragging = true
    dragStartX = e.clientX
    dragStartY = e.clientY
    panStartX = panX
    panStartY = panY
    container.style.cursor = "grabbing"
  }

  const onMouseMove = (e: MouseEvent) => {
    if (!isDragging) return
    panX = panStartX + (e.clientX - dragStartX)
    panY = panStartY + (e.clientY - dragStartY)
    applyTransform()
  }

  const onMouseUp = () => {
    if (!isDragging) return
    isDragging = false
    container.style.cursor = "grab"
  }

  // Touch support
  let lastTouchDist = 0
  let lastTouchCenter = { x: 0, y: 0 }

  const onTouchStart = (e: TouchEvent) => {
    if (e.touches.length === 1) {
      if ((e.target as HTMLElement).closest(".canvas-node-file, .canvas-node-link, .canvas-controls"))
        return
      isDragging = true
      dragStartX = e.touches[0].clientX
      dragStartY = e.touches[0].clientY
      panStartX = panX
      panStartY = panY
    } else if (e.touches.length === 2) {
      isDragging = false
      const dx = e.touches[1].clientX - e.touches[0].clientX
      const dy = e.touches[1].clientY - e.touches[0].clientY
      lastTouchDist = Math.sqrt(dx * dx + dy * dy)
      lastTouchCenter = {
        x: (e.touches[0].clientX + e.touches[1].clientX) / 2,
        y: (e.touches[0].clientY + e.touches[1].clientY) / 2,
      }
    }
  }

  const onTouchMove = (e: TouchEvent) => {
    if (e.touches.length === 1 && isDragging) {
      e.preventDefault()
      panX = panStartX + (e.touches[0].clientX - dragStartX)
      panY = panStartY + (e.touches[0].clientY - dragStartY)
      applyTransform()
    } else if (e.touches.length === 2) {
      e.preventDefault()
      const dx = e.touches[1].clientX - e.touches[0].clientX
      const dy = e.touches[1].clientY - e.touches[0].clientY
      const dist = Math.sqrt(dx * dx + dy * dy)

      if (lastTouchDist > 0) {
        const rect = container.getBoundingClientRect()
        const cx = (e.touches[0].clientX + e.touches[1].clientX) / 2 - rect.left
        const cy = (e.touches[0].clientY + e.touches[1].clientY) / 2 - rect.top
        const zoomFactor = dist / lastTouchDist
        const newScale = Math.max(0.05, Math.min(8, scale * zoomFactor))

        panX = cx - (cx - panX) * (newScale / scale)
        panY = cy - (cy - panY) * (newScale / scale)
        scale = newScale
        applyTransform()
      }

      lastTouchDist = dist
    }
  }

  const onTouchEnd = () => {
    isDragging = false
    lastTouchDist = 0
  }

  // Bind events
  container.addEventListener("wheel", onWheel, { passive: false })
  container.addEventListener("mousedown", onMouseDown)
  window.addEventListener("mousemove", onMouseMove)
  window.addEventListener("mouseup", onMouseUp)
  container.addEventListener("touchstart", onTouchStart, { passive: true })
  container.addEventListener("touchmove", onTouchMove, { passive: false })
  container.addEventListener("touchend", onTouchEnd)

  // Control buttons
  const zoomInBtn = container.querySelector(".canvas-zoom-in")
  const zoomOutBtn = container.querySelector(".canvas-zoom-out")
  const resetBtn = container.querySelector(".canvas-zoom-reset")

  zoomInBtn?.addEventListener("click", () => {
    const rect = container.getBoundingClientRect()
    const cx = rect.width / 2
    const cy = rect.height / 2
    const newScale = Math.min(8, scale * 1.25)
    panX = cx - (cx - panX) * (newScale / scale)
    panY = cy - (cy - panY) * (newScale / scale)
    scale = newScale
    applyTransform()
  })

  zoomOutBtn?.addEventListener("click", () => {
    const rect = container.getBoundingClientRect()
    const cx = rect.width / 2
    const cy = rect.height / 2
    const newScale = Math.max(0.05, scale * 0.8)
    panX = cx - (cx - panX) * (newScale / scale)
    panY = cy - (cy - panY) * (newScale / scale)
    scale = newScale
    applyTransform()
  })

  resetBtn?.addEventListener("click", () => {
    fitToView()
  })

  // Initial fit
  fitToView()

  // Return cleanup function
  return () => {
    container.removeEventListener("wheel", onWheel)
    container.removeEventListener("mousedown", onMouseDown)
    window.removeEventListener("mousemove", onMouseMove)
    window.removeEventListener("mouseup", onMouseUp)
    container.removeEventListener("touchstart", onTouchStart)
    container.removeEventListener("touchmove", onTouchMove)
    container.removeEventListener("touchend", onTouchEnd)
  }
}

function escapeHtml(str: string): string {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
}

let cleanup: (() => void) | undefined

document.addEventListener("nav", async (e: CustomEventMap["nav"]) => {
  if (cleanup) {
    cleanup()
    cleanup = undefined
  }

  const container = document.getElementById("canvas-container")
  if (!container) return

  const slug = e.detail.url
  cleanup = renderCanvas(container, slug)
})
