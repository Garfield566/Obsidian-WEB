import { FullSlug, resolveRelative } from "../util/path"
import { QuartzPluginData } from "../plugins/vfile"
import { Date, getDate } from "./Date"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { GlobalConfiguration } from "../cfg"

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
  columns?: number
  excludeFolders?: string[]
  imageProperties?: string[]
  requireImage?: boolean
}

const defaultOptions: CardGridOptions = {
  showTags: true,
  showDate: false,
  showDescription: true,
  columns: 4,
  excludeFolders: [".obsidian", ".trash", "templates", "private", "emergent-tags"],
  imageProperties: ["cover", "image", "banner", "thumbnail", "poster"],
  requireImage: true,
}

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
        if (slug === fileData.slug) return false
        if (slug.endsWith("/index") || slug === "index") return false
        if (isExcluded(slug, opts.excludeFolders!)) return false
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
      <div class="masonry-grid" style={`--columns: ${opts.columns}`}>
        {list.map((page) => {
          const title = page.frontmatter?.title ?? "Untitled"
          const tags = page.frontmatter?.tags ?? []
          const description = page.description ?? ""
          const coverImage = getCoverImage(page.frontmatter, opts.imageProperties!)
          const date = page.dates ? getDate(cfg, page) : undefined

          return (
            <a href={resolveRelative(fileData.slug!, page.slug!)} class="masonry-item internal">
              {coverImage && (
                <div class="masonry-cover">
                  <img
                    src={coverImage.startsWith("http") ? coverImage : resolveRelative(fileData.slug!, coverImage as FullSlug)}
                    alt={title}
                    loading="lazy"
                  />
                </div>
              )}
              <div class="masonry-content">
                <h3 class="masonry-title">{title}</h3>
                {opts.showDate && date && (
                  <p class="masonry-date">
                    <Date date={date} locale={cfg.locale} />
                  </p>
                )}
                {opts.showDescription && description && (
                  <p class="masonry-desc">{description}</p>
                )}
                {opts.showTags && tags.length > 0 && (
                  <div class="masonry-tags">
                    {tags.slice(0, 3).map((tag) => (
                      <span class="masonry-tag">#{tag}</span>
                    ))}
                  </div>
                )}
              </div>
            </a>
          )
        })}
      </div>
    )
  }

  CardGrid.css = `
/* Masonry Grid - Pinterest Style */
.masonry-grid {
  column-count: var(--columns, 4);
  column-gap: 16px;
  margin-top: 2rem;
}

@media (max-width: 1200px) {
  .masonry-grid { column-count: 3; }
}

@media (max-width: 900px) {
  .masonry-grid { column-count: 2; }
}

@media (max-width: 600px) {
  .masonry-grid { column-count: 2; column-gap: 10px; }
}

/* Card Item */
.masonry-item {
  display: block;
  break-inside: avoid;
  margin-bottom: 16px;
  background: var(--light);
  border-radius: 16px;
  overflow: hidden;
  text-decoration: none;
  color: inherit;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}

.masonry-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

/* Cover Image */
.masonry-cover {
  width: 100%;
  overflow: hidden;
  background: var(--lightgray);
}

.masonry-cover img {
  width: 100%;
  height: auto;
  display: block;
  transition: transform 0.3s ease;
}

.masonry-item:hover .masonry-cover img {
  transform: scale(1.05);
}

/* Content */
.masonry-content {
  padding: 12px;
}

.masonry-title {
  margin: 0 0 6px 0;
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--dark);
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.masonry-date {
  margin: 0 0 6px 0;
  font-size: 0.75rem;
  color: var(--gray);
}

.masonry-desc {
  margin: 0 0 8px 0;
  font-size: 0.8rem;
  color: var(--darkgray);
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.masonry-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.masonry-tag {
  font-size: 0.7rem;
  padding: 2px 8px;
  background: var(--highlight);
  color: var(--secondary);
  border-radius: 12px;
}

/* Dark mode */
:root[saved-theme="dark"] .masonry-item {
  background: var(--light);
  box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}

:root[saved-theme="dark"] .masonry-item:hover {
  box-shadow: 0 8px 25px rgba(0,0,0,0.4);
}
`

  return CardGrid
}) satisfies QuartzComponentConstructor
