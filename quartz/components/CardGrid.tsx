import { FullSlug, resolveRelative } from "../util/path"
import { QuartzPluginData } from "../plugins/vfile"
import { Date, getDate } from "./Date"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { GlobalConfiguration } from "../cfg"
import style from "./styles/cardGrid.scss"

export type SortFn = (f1: QuartzPluginData, f2: QuartzPluginData) => number

export function byDateAndAlphabetical(cfg: GlobalConfiguration): SortFn {
  return (f1, f2) => {
    if (f1.dates && f2.dates) {
      return getDate(cfg, f2)!.getTime() - getDate(cfg, f1)!.getTime()
    } else if (f1.dates && !f2.dates) {
      return -1
    } else if (!f1.dates && f2.dates) {
      return 1
    }
    const f1Title = f1.frontmatter?.title.toLowerCase() ?? ""
    const f2Title = f2.frontmatter?.title.toLowerCase() ?? ""
    return f1Title.localeCompare(f2Title)
  }
}

interface CardGridOptions {
  limit?: number
  sort?: SortFn
  showTags?: boolean
  showDate?: boolean
  showDescription?: boolean
  columns?: 2 | 3 | 4
  /** Folders to include (e.g., ["Personnages", "Projets"]) - if empty, includes all */
  folders?: string[]
  /** Folders to exclude (e.g., [".obsidian", ".trash"]) */
  excludeFolders?: string[]
  /** Frontmatter properties to search for cover image (first found wins) */
  imageProperties?: string[]
  /** Only show files that have a cover image */
  requireImage?: boolean
}

const defaultOptions: CardGridOptions = {
  showTags: true,
  showDate: true,
  showDescription: true,
  columns: 3,
  folders: [],
  excludeFolders: [".obsidian", ".trash", "templates", "private"],
  imageProperties: ["cover", "image", "banner", "thumbnail", "poster"],
  requireImage: false,
}

// Helper to get cover image from multiple possible properties
function getCoverImage(frontmatter: Record<string, unknown> | undefined, properties: string[]): string | undefined {
  if (!frontmatter) return undefined
  for (const prop of properties) {
    const value = frontmatter[prop]
    if (typeof value === "string" && value.trim() !== "") {
      return value
    }
  }
  return undefined
}

// Helper to check if slug is in allowed folders
function isInFolders(slug: string, folders: string[]): boolean {
  if (folders.length === 0) return true
  return folders.some(folder => {
    const normalizedFolder = folder.toLowerCase().replace(/\//g, "/")
    const normalizedSlug = slug.toLowerCase()
    return normalizedSlug.startsWith(normalizedFolder + "/") || normalizedSlug.includes("/" + normalizedFolder + "/")
  })
}

// Helper to check if slug is in excluded folders
function isExcluded(slug: string, excludeFolders: string[]): boolean {
  return excludeFolders.some(folder => {
    const normalizedFolder = folder.toLowerCase()
    const normalizedSlug = slug.toLowerCase()
    return normalizedSlug.startsWith(normalizedFolder + "/") ||
           normalizedSlug.includes("/" + normalizedFolder + "/") ||
           normalizedSlug === normalizedFolder
  })
}

export default ((userOpts?: CardGridOptions) => {
  const opts = { ...defaultOptions, ...userOpts }

  const CardGrid: QuartzComponent = (props: QuartzComponentProps) => {
    const { cfg, fileData, allFiles } = props
    const sorter = opts.sort ?? byDateAndAlphabetical(cfg)

    let list = allFiles
      .filter((file) => {
        const slug = file.slug ?? ""
        // Exclude current page
        if (slug === fileData.slug) return false
        // Exclude index files
        if (slug.endsWith("/index") || slug === "index") return false
        // Exclude folders in excludeFolders
        if (isExcluded(slug, opts.excludeFolders!)) return false
        // Filter by folders if specified
        if (!isInFolders(slug, opts.folders!)) return false
        // Filter by image requirement
        if (opts.requireImage) {
          const cover = getCoverImage(file.frontmatter, opts.imageProperties!)
          if (!cover) return false
        }
        return true
      })
      .sort(sorter)

    if (opts.limit) {
      list = list.slice(0, opts.limit)
    }

    if (list.length === 0) {
      return null
    }

    return (
      <div class={`card-grid columns-${opts.columns}`}>
        {list.map((page) => {
          const title = page.frontmatter?.title ?? "Untitled"
          const tags = page.frontmatter?.tags ?? []
          const description = page.description ?? ""
          const coverImage = getCoverImage(page.frontmatter, opts.imageProperties!)
          const date = page.dates ? getDate(cfg, page) : undefined

          return (
            <a
              href={resolveRelative(fileData.slug!, page.slug!)}
              class="card-link internal"
            >
              <article class={`card ${coverImage ? "has-cover" : "no-cover"}`}>
                {coverImage && (
                  <div class="card-cover">
                    <img
                      src={coverImage.startsWith("http") ? coverImage : resolveRelative(fileData.slug!, coverImage as FullSlug)}
                      alt={title}
                      loading="lazy"
                    />
                  </div>
                )}
                <div class="card-content">
                  <h3 class="card-title">{title}</h3>
                  {opts.showDate && date && (
                    <p class="card-date">
                      <Date date={date} locale={cfg.locale} />
                    </p>
                  )}
                  {opts.showDescription && description && (
                    <p class="card-description">{description}</p>
                  )}
                  {opts.showTags && tags.length > 0 && (
                    <ul class="card-tags">
                      {tags.slice(0, 3).map((tag) => (
                        <li class="card-tag">#{tag}</li>
                      ))}
                    </ul>
                  )}
                </div>
              </article>
            </a>
          )
        })}
      </div>
    )
  }

  CardGrid.css = style
  return CardGrid
}) satisfies QuartzComponentConstructor
