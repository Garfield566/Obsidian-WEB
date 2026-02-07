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
  imageProperty?: string  // frontmatter property for cover image (default: "cover")
}

const defaultOptions: CardGridOptions = {
  showTags: true,
  showDate: true,
  showDescription: true,
  columns: 3,
  imageProperty: "cover",
}

export default ((userOpts?: CardGridOptions) => {
  const opts = { ...defaultOptions, ...userOpts }

  const CardGrid: QuartzComponent = (props: QuartzComponentProps) => {
    const { cfg, fileData, allFiles } = props
    const sorter = opts.sort ?? byDateAndAlphabetical(cfg)

    let list = allFiles
      .filter((file) => file.slug !== fileData.slug) // exclude current page
      .sort(sorter)

    if (opts.limit) {
      list = list.slice(0, opts.limit)
    }

    return (
      <div class={`card-grid columns-${opts.columns}`}>
        {list.map((page) => {
          const title = page.frontmatter?.title ?? "Untitled"
          const tags = page.frontmatter?.tags ?? []
          const description = page.description ?? ""
          const coverImage = page.frontmatter?.[opts.imageProperty!] as string | undefined
          const date = page.dates ? getDate(cfg, page) : undefined

          return (
            <a
              href={resolveRelative(fileData.slug!, page.slug!)}
              class="card-link internal"
            >
              <article class="card">
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
