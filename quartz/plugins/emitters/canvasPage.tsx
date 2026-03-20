import path from "path"
import fs from "fs"
import { unified } from "unified"
import remarkParse from "remark-parse"
import remarkRehype from "remark-rehype"
import { toHtml } from "hast-util-to-html"
import { QuartzEmitterPlugin } from "../types"
import { QuartzComponentProps } from "../../components/types"
import HeaderConstructor from "../../components/Header"
import BodyConstructor from "../../components/Body"
import { pageResources, renderPage } from "../../components/renderPage"
import { FullPageLayout } from "../../cfg"
import { FilePath, FullSlug, joinSegments, slugifyFilePath } from "../../util/path"
import { pathToRoot } from "../../util/path"
import { defaultContentPageLayout, sharedPageComponents } from "../../../quartz.layout"
import Graph from "../../components/Graph"
import Backlinks from "../../components/Backlinks"
import CanvasContent from "../../components/pages/CanvasContent"
import { write } from "./helpers"
import { BuildCtx } from "../../util/ctx"
import { Root } from "hast"
import { StaticResources } from "../../util/resources"

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

const mdProcessor = unified()
  .use(remarkParse)
  .use(remarkRehype, { allowDangerousHtml: true })

async function processCanvasMarkdown(text: string): Promise<string> {
  const mdast = mdProcessor.parse(text)
  const hast = await mdProcessor.run(mdast)
  return toHtml(hast as any, { allowDangerousHtml: true })
}

async function processCanvasFile(
  ctx: BuildCtx,
  canvasRelPath: FilePath,
  allFiles: any[],
  opts: FullPageLayout,
  resources: StaticResources,
) {
  const fullPath = joinSegments(ctx.argv.directory, canvasRelPath) as string
  const rawJson = await fs.promises.readFile(fullPath, "utf-8")
  const canvasData: CanvasData = JSON.parse(rawJson)

  // Handle empty or malformed canvas files
  if (!canvasData.nodes || !Array.isArray(canvasData.nodes)) {
    canvasData.nodes = []
  }
  if (!canvasData.edges || !Array.isArray(canvasData.edges)) {
    canvasData.edges = []
  }

  // Pre-render markdown in text nodes
  for (const node of canvasData.nodes) {
    if (node.type === "text" && node.text) {
      node.renderedHtml = await processCanvasMarkdown(node.text)
    }
  }

  // Resolve file node paths to slugs for navigation
  for (const node of canvasData.nodes) {
    if (node.type === "file" && node.file) {
      // Strip .md extension and slugify for Quartz navigation
      const filePath = node.file.replace(/\.md$/, "")
      node.file = slugifyFilePath(filePath as FilePath, true) as string
    }
  }

  // Compute slug: strip .canvas extension
  const slug = slugifyFilePath(canvasRelPath as FilePath, true) as FullSlug

  // Derive title from filename
  const fileName = path.basename(canvasRelPath, ".canvas")

  // Build fileData for renderPage
  const fileData = {
    slug,
    filePath: canvasRelPath,
    relativePath: canvasRelPath,
    frontmatter: {
      title: fileName,
      tags: [] as string[],
    },
    canvasData,
  }

  // Empty HAST tree - the CanvasContent component handles rendering
  const tree: Root = { type: "root", children: [] }

  const externalResources = pageResources(pathToRoot(slug), resources)
  const componentData: QuartzComponentProps = {
    ctx,
    fileData: fileData as any,
    externalResources,
    cfg: ctx.cfg.configuration,
    children: [],
    tree,
    allFiles,
  }

  const content = renderPage(ctx.cfg.configuration, slug, componentData, opts, externalResources)
  return write({
    ctx,
    content,
    slug,
    ext: ".html",
  })
}

export const CanvasPage: QuartzEmitterPlugin<Partial<FullPageLayout>> = (userOpts) => {
  const opts: FullPageLayout = {
    ...sharedPageComponents,
    ...defaultContentPageLayout,
    pageBody: CanvasContent(),
    // Move Graph and Backlinks below the canvas for more space
    afterBody: [...(sharedPageComponents.afterBody ?? []), Graph(), Backlinks()],
    right: [],
    ...userOpts,
  }

  const { head: Head, header, beforeBody, pageBody, afterBody, left, right, footer: Footer } = opts
  const Header = HeaderConstructor()
  const Body = BodyConstructor()

  return {
    name: "CanvasPage",
    getQuartzComponents() {
      return [
        Head,
        Header,
        Body,
        ...header,
        ...beforeBody,
        pageBody,
        ...afterBody,
        ...left,
        ...right,
        Footer,
      ]
    },
    async *emit(ctx, content, resources) {
      const allFiles = content.map((c) => c[1].data)

      // Find all .canvas files
      const canvasFiles = ctx.allFiles.filter((fp) => fp.endsWith(".canvas"))

      for (const canvasPath of canvasFiles) {
        try {
          yield processCanvasFile(ctx, canvasPath as FilePath, allFiles, opts, resources)
        } catch (err) {
          console.warn(`[CanvasPage] Failed to process ${canvasPath}:`, err)
        }
      }
    },
    async *partialEmit(ctx, content, resources, changeEvents) {
      const allFiles = content.map((c) => c[1].data)

      for (const changeEvent of changeEvents) {
        if (!changeEvent.path.endsWith(".canvas")) continue
        if (changeEvent.type === "delete") continue

        try {
          yield processCanvasFile(
            ctx,
            changeEvent.path as FilePath,
            allFiles,
            opts,
            resources,
          )
        } catch (err) {
          console.warn(`[CanvasPage] Failed to process ${changeEvent.path}:`, err)
        }
      }
    },
  }
}
