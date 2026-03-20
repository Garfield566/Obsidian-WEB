import { Code, Root as MdRoot } from "mdast"
import { QuartzTransformerPlugin } from "../types"
import { visit } from "unist-util-visit"
import { load, tex, dvi2svg } from "node-tikzjax"
import { h } from "hastscript"
import { Element, Properties } from "hast"
import { toHtml } from "hast-util-to-html"
import { fromHtmlIsomorphic } from "hast-util-from-html-isomorphic"
import { BuildCtx } from "../../util/ctx"

async function tex2svg(input: string, showConsole: boolean) {
  await load()
  const dvi = await tex(input, {
    texPackages: { pgfplots: "", amsmath: "intlimits" },
    tikzLibraries: "arrows.meta,calc,positioning,patterns",
    addToPreamble: "% comment",
    showConsole,
  })
  const svg = await dvi2svg(dvi)
  return svg
}

interface TikzNode {
  index: number
  value: string
  parent: MdRoot
  base64?: string
}

function parseStyle(meta: string | null | undefined): string {
  if (!meta) return ""
  const styleMatch = meta.match(/style\s*=\s*["']([^"']+)["']/)
  return styleMatch ? styleMatch[1] : ""
}

const docs = (node: Code): string => JSON.stringify(node.value)

function makeTikzGraph(node: Code, svg: string, style?: string): Element {
  const mathMl = h(
    "span.tikz-mathml",
    h(
      "math",
      { xmlns: "http://www.w3.org/1998/Math/MathML" },
      h(
        "semantics",
        h("annotation", { encoding: "application/x-tex" }, { type: "text", value: docs(node) }),
      ),
    ),
  )

  const properties: Properties = { "data-remark-tikz": true, style: "" }
  if (style) properties.style = style

  return h(
    "figure.tikz",
    properties,
    mathMl,
    fromHtmlIsomorphic(svg, { fragment: true }),
  )
}

interface Options {
  showConsole: boolean
}

const defaultOpts: Options = {
  showConsole: false,
}

export const TikzJax: QuartzTransformerPlugin<Options> = (opts?: Options) => {
  const o = { ...defaultOpts, ...opts }
  return {
    name: "TikzJax",
    markdownPlugins(ctx: BuildCtx) {
      // Skip tikz transpilation during watch mode (takes too long)
      if (ctx.argv.watch) return []

      return [
        () => async (tree) => {
          const nodes: TikzNode[] = []
          visit(tree, "code", (node: Code, index, parent) => {
            const { lang, meta, value } = node
            if (lang === "tikz") {
              const base64Match = meta?.match(/alt\s*=\s*"data:image\/svg\+xml;base64,([^"]+)"/)
              let base64String = undefined
              if (base64Match) {
                base64String = Buffer.from(base64Match[1], "base64").toString()
              }
              nodes.push({
                index: index as number,
                parent: parent as MdRoot,
                value,
                base64: base64String,
              })
            }
          })

          for (let i = 0; i < nodes.length; i++) {
            const { index, parent, value, base64 } = nodes[i]
            let svg
            try {
              if (base64 !== undefined) {
                svg = base64
              } else {
                svg = await tex2svg(value, o.showConsole)
              }
              const node = parent.children[index] as Code

              parent.children.splice(index, 1, {
                type: "html",
                value: toHtml(makeTikzGraph(node, svg, parseStyle(node?.meta)), {
                  allowDangerousHtml: true,
                }),
              })
            } catch (e) {
              console.error(`[TikzJax] Error rendering TikZ diagram: ${e}`)
              // Keep original code block on error
            }
          }
        },
      ]
    },
    externalResources() {
      return {
        css: [
          {
            content: "https://cdn.jsdelivr.net/npm/node-tikzjax@latest/css/fonts.css",
          },
        ],
      }
    },
  }
}
