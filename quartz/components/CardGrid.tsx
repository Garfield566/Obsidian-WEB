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

    // Collect all tags for the search input
    const tagCounts = new Map<string, number>()
    list.forEach(page => {
      const tags = page.frontmatter?.tags ?? []
      tags.forEach((tag: string) => {
        if (tag && tag.trim() !== "") {
          tagCounts.set(tag, (tagCounts.get(tag) || 0) + 1)
        }
      })
    })

    // Collect folder names as filterable items
    const folderCounts = new Map<string, number>()
    list.forEach(page => {
      const slug = page.slug ?? ""
      const parts = slug.split("/")
      // Extract each folder segment (skip the filename)
      for (let i = 0; i < parts.length - 1; i++) {
        let folder = decodeURIComponent(parts[i])
        // Clean up folder names: remove leading numbers, emojis prefixes like "¹", "²", "⁰"
        folder = folder.replace(/^[⁰¹²³⁴⁵⁶⁷⁸⁹\d]+[-\s]*/g, "").replace(/^[^\w\s]*\s*/g, "").trim()
        if (folder && folder.length > 1) {
          folderCounts.set(folder, (folderCounts.get(folder) || 0) + 1)
        }
      }
    })

    // Combine: folders first, then tags
    const allFilters: { label: string; count: number; type: "folder" | "tag" }[] = []
    Array.from(folderCounts.entries())
      .sort((a, b) => b[1] - a[1])
      .forEach(([folder, count]) => {
        allFilters.push({ label: folder, count, type: "folder" })
      })
    Array.from(tagCounts.entries())
      .sort((a, b) => b[1] - a[1])
      .forEach(([tag, count]) => {
        allFilters.push({ label: tag, count, type: "tag" })
      })

    return (
      <div class="masonry-container">
        {/* Tag search bar */}
        <div class="masonry-filters">
          <div class="masonry-tag-search">
            <div class="masonry-search-wrapper">
              <svg class="masonry-search-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
              <input
                type="text"
                class="masonry-tag-input"
                placeholder="Rechercher un tag ou dossier..."
                autocomplete="off"
              />
              <button class="masonry-clear-btn" style="display:none" aria-label="Effacer">✕</button>
            </div>
            <div class="masonry-tag-dropdown" style="display:none">
              {allFilters.map(({ label, count, type }) => (
                <div class="masonry-tag-option" data-tag={label} data-type={type}>
                  <span class="masonry-tag-name">
                    {type === "folder" ? "\uD83D\uDCC1 " : "#"}{label}
                  </span>
                  <span class="masonry-tag-count">{count}</span>
                </div>
              ))}
            </div>
          </div>
          <div class="masonry-active-tag" style="display:none">
            <span class="masonry-active-tag-label"></span>
            <button class="masonry-remove-tag" aria-label="Retirer le filtre">✕</button>
          </div>
        </div>

        {/* Grid */}
        <div class="masonry-grid" style={`--columns: ${opts.columns}`}>
          {list.map((page) => {
            const title = page.frontmatter?.title ?? "Untitled"
            const tags = page.frontmatter?.tags ?? []
            const description = page.description ?? ""
            const coverImage = getCoverImage(page.frontmatter, opts.imageProperties!)
            const date = page.dates ? getDate(cfg, page) : undefined
            // Extract clean folder names from slug
            const slugParts = (page.slug ?? "").split("/")
            const folders = slugParts.slice(0, -1).map(p => {
              let f = decodeURIComponent(p)
              f = f.replace(/^[⁰¹²³⁴⁵⁶⁷⁸⁹\d]+[-\s]*/g, "").replace(/^[^\w\s]*\s*/g, "").trim()
              return f
            }).filter(f => f.length > 1)

            return (
              <a
                href={resolveRelative(fileData.slug!, page.slug!)}
                class="masonry-item internal"
                data-tags={tags.join(",")}
                data-folders={folders.join(",")}
              >
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
      </div>
    )
  }

  CardGrid.afterDOMLoaded = `
document.addEventListener("nav", () => {
  const container = document.querySelector(".masonry-container")
  if (!container) return

  const input = container.querySelector(".masonry-tag-input")
  const dropdown = container.querySelector(".masonry-tag-dropdown")
  const clearBtn = container.querySelector(".masonry-clear-btn")
  const activeTagEl = container.querySelector(".masonry-active-tag")
  const activeTagLabel = container.querySelector(".masonry-active-tag-label")
  const removeTagBtn = container.querySelector(".masonry-remove-tag")
  const options = container.querySelectorAll(".masonry-tag-option")
  const items = container.querySelectorAll(".masonry-item")
  if (!input || !dropdown) return

  let selectedFilter = null
  let selectedType = null

  function filterGrid(filter, type) {
    items.forEach((item) => {
      if (!filter) {
        item.style.display = ""
        return
      }
      if (type === "tag") {
        const tags = (item.getAttribute("data-tags") || "").split(",")
        item.style.display = tags.includes(filter) ? "" : "none"
      } else if (type === "folder") {
        const folders = (item.getAttribute("data-folders") || "").split(",")
        item.style.display = folders.includes(filter) ? "" : "none"
      }
    })
  }

  function selectTag(filter, type) {
    selectedFilter = filter
    selectedType = type
    input.value = ""
    dropdown.style.display = "none"
    clearBtn.style.display = "none"
    activeTagEl.style.display = "flex"
    activeTagLabel.textContent = (type === "folder" ? "\uD83D\uDCC1 " : "#") + filter
    filterGrid(filter, type)
  }

  function clearTag() {
    selectedFilter = null
    selectedType = null
    input.value = ""
    dropdown.style.display = "none"
    clearBtn.style.display = "none"
    activeTagEl.style.display = "none"
    filterGrid(null, null)
  }

  function handleInput() {
    const query = input.value.toLowerCase().trim()
    clearBtn.style.display = query ? "flex" : "none"
    if (!query) {
      dropdown.style.display = "none"
      return
    }
    let hasMatch = false
    options.forEach((opt) => {
      const tag = opt.getAttribute("data-tag").toLowerCase()
      if (tag.includes(query)) {
        opt.style.display = "flex"
        hasMatch = true
      } else {
        opt.style.display = "none"
      }
    })
    dropdown.style.display = hasMatch ? "block" : "none"
  }

  function handleClear() {
    input.value = ""
    dropdown.style.display = "none"
    clearBtn.style.display = "none"
    input.focus()
  }

  input.addEventListener("input", handleInput)
  input.addEventListener("focus", () => {
    if (input.value.trim()) handleInput()
  })

  clearBtn.addEventListener("click", handleClear)
  removeTagBtn.addEventListener("click", clearTag)

  options.forEach((opt) => {
    const handleClick = () => {
      selectTag(opt.getAttribute("data-tag"), opt.getAttribute("data-type") || "tag")
    }
    opt.addEventListener("click", handleClick)
    window.addCleanup(() => opt.removeEventListener("click", handleClick))
  })

  // Close dropdown on outside click
  function handleOutside(e) {
    if (!container.querySelector(".masonry-tag-search").contains(e.target)) {
      dropdown.style.display = "none"
    }
  }
  document.addEventListener("click", handleOutside)

  window.addCleanup(() => {
    input.removeEventListener("input", handleInput)
    clearBtn.removeEventListener("click", handleClear)
    removeTagBtn.removeEventListener("click", clearTag)
    document.removeEventListener("click", handleOutside)
  })
})
`

  CardGrid.css = `
/* Filter bar */
.masonry-container {
  margin-top: 2rem;
}
.masonry-filters {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 1.5rem;
}
/* Tag search */
.masonry-tag-search {
  position: relative;
}
.masonry-search-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  background: var(--light);
  border: 2px solid var(--lightgray);
  border-radius: 10px;
  transition: border-color 0.2s ease;
}
.masonry-search-wrapper:focus-within {
  border-color: var(--secondary);
}
.masonry-search-icon {
  flex-shrink: 0;
  color: var(--gray);
}
.masonry-tag-input {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  font-size: 0.9rem;
  color: var(--dark);
  font-family: var(--bodyFont);
}
.masonry-tag-input::placeholder {
  color: var(--gray);
}
.masonry-clear-btn {
  display: none;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  cursor: pointer;
  color: var(--gray);
  font-size: 0.9rem;
  padding: 2px 4px;
  border-radius: 4px;
}
.masonry-clear-btn:hover {
  color: var(--dark);
  background: var(--lightgray);
}
/* Dropdown */
.masonry-tag-dropdown {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  right: 0;
  background: var(--light);
  border: 1px solid var(--lightgray);
  border-radius: 10px;
  max-height: 250px;
  overflow-y: auto;
  z-index: 100;
  box-shadow: 0 4px 16px rgba(0,0,0,0.12);
}
.masonry-tag-option {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 14px;
  cursor: pointer;
  transition: background 0.1s ease;
}
.masonry-tag-option:hover {
  background: var(--lightgray);
}
.masonry-tag-name {
  font-size: 0.85rem;
  color: var(--dark);
}
.masonry-tag-count {
  font-size: 0.75rem;
  color: var(--gray);
  background: var(--lightgray);
  padding: 2px 8px;
  border-radius: 10px;
}
/* Active tag pill */
.masonry-active-tag {
  display: none;
  align-items: center;
  gap: 8px;
  padding: 6px 14px;
  background: var(--secondary);
  color: var(--light);
  border-radius: 20px;
  width: fit-content;
  font-size: 0.85rem;
}
.masonry-active-tag-label {
  font-weight: 600;
}
.masonry-remove-tag {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--light);
  font-size: 0.85rem;
  padding: 0 2px;
  opacity: 0.8;
}
.masonry-remove-tag:hover {
  opacity: 1;
}

/* Masonry Grid */
.masonry-grid {
  column-count: var(--columns, 4);
  column-gap: 16px;
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
.masonry-item[style*="display: none"] {
  display: none !important;
}
.masonry-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}
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
:root[saved-theme="dark"] .masonry-item {
  background: var(--light);
  box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}
:root[saved-theme="dark"] .masonry-item:hover {
  box-shadow: 0 8px 25px rgba(0,0,0,0.4);
}
:root[saved-theme="dark"] .masonry-search-wrapper {
  background: var(--light);
  border-color: var(--lightgray);
}
:root[saved-theme="dark"] .masonry-tag-dropdown {
  background: var(--light);
  border-color: var(--lightgray);
  box-shadow: 0 4px 16px rgba(0,0,0,0.3);
}
`

  return CardGrid
}) satisfies QuartzComponentConstructor
