import { FullSlug, resolveRelative } from "../util/path"
import { QuartzPluginData } from "../plugins/vfile"
import { Date, getDate } from "./Date"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { GlobalConfiguration } from "../cfg"
import style from "./styles/cardGrid.scss"
// @ts-ignore
import script from "./scripts/cardGrid.inline"

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
  columns?: 2 | 3 | 4 | 5
  /** Folders to show as filter buttons */
  filterFolders?: string[]
  /** Folders to exclude (e.g., [".obsidian", ".trash"]) */
  excludeFolders?: string[]
  /** Frontmatter properties to search for cover image (first found wins) */
  imageProperties?: string[]
  /** Only show files that have a cover image */
  requireImage?: boolean
  /** Show filter header */
  showFilters?: boolean
}

const defaultOptions: CardGridOptions = {
  showTags: true,
  showDate: false,
  showDescription: false,
  columns: 4,
  filterFolders: [],
  excludeFolders: [".obsidian", ".trash", "templates", "private", "emergent-tags"],
  imageProperties: ["cover", "image", "banner", "thumbnail", "poster"],
  requireImage: false,
  showFilters: true,
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

// Get the top-level folder from a slug
function getTopFolder(slug: string): string {
  const parts = slug.split("/")
  return parts.length > 1 ? parts[0] : ""
}

// Clean folder name for display
function cleanFolderName(name: string): string {
  return name
    .replace(/[²¹⁰]/g, "")
    .replace(/[👹🧭♟👺📈⚙️🖼📚💡🎯]/g, "")
    .trim()
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

    // Get unique folders for filters
    const folders = new Set<string>()
    list.forEach(file => {
      const folder = getTopFolder(file.slug ?? "")
      if (folder) folders.add(folder)
    })
    const folderList = opts.filterFolders!.length > 0
      ? opts.filterFolders!
      : Array.from(folders).sort()

    return (
      <div class="card-grid-container">
        {opts.showFilters && folderList.length > 1 && (
          <div class="card-grid-header">
            <div class="card-grid-filters">
              <button class="filter-btn active" data-folder="all">Tous</button>
              {folderList.map((folder) => (
                <button class="filter-btn" data-folder={folder}>
                  {cleanFolderName(folder)}
                </button>
              ))}
            </div>
            <span class="card-grid-count">{list.length} notes</span>
          </div>
        )}
        <div class={`card-grid columns-${opts.columns}`}>
          {list.map((page) => {
            const title = page.frontmatter?.title ?? "Untitled"
            const tags = page.frontmatter?.tags ?? []
            const description = page.description ?? ""
            const coverImage = getCoverImage(page.frontmatter, opts.imageProperties!)
            const date = page.dates ? getDate(cfg, page) : undefined
            const folder = getTopFolder(page.slug ?? "")

            return (
              <a
                href={resolveRelative(fileData.slug!, page.slug!)}
                class="card-link internal"
                data-folder={folder}
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
      </div>
    )
  }

  CardGrid.css = style
  CardGrid.afterDOMLoaded = script
  return CardGrid
}) satisfies QuartzComponentConstructor
