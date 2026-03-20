import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "../types"
// @ts-ignore
import script from "../scripts/canvas.inline"
import style from "../styles/canvas.scss"

const CanvasContent: QuartzComponent = ({ fileData }: QuartzComponentProps) => {
  const canvasData = (fileData as any).canvasData
  const canvasJson = canvasData ? JSON.stringify(canvasData) : "{}"

  return (
    <div class="canvas-page">
      <div id="canvas-container" class="canvas-container">
        <div class="canvas-controls">
          <button class="canvas-zoom-in" aria-label="Zoom in">
            +
          </button>
          <button class="canvas-zoom-out" aria-label="Zoom out">
            -
          </button>
          <button class="canvas-zoom-reset" aria-label="Reset view">
            Reset
          </button>
        </div>
        <div class="canvas-viewport">
          <svg class="canvas-edges" xmlns="http://www.w3.org/2000/svg" />
          <div class="canvas-nodes" />
        </div>
      </div>
      <script
        type="application/json"
        id="canvas-data"
        dangerouslySetInnerHTML={{ __html: canvasJson }}
      />
    </div>
  )
}

CanvasContent.css = style
CanvasContent.afterDOMLoaded = script

export default (() => CanvasContent) satisfies QuartzComponentConstructor
