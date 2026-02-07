document.addEventListener("nav", () => {
  const gridContainer = document.querySelector(".card-grid-container")
  if (!gridContainer) return

  const filterButtons = gridContainer.querySelectorAll(".filter-btn")
  const cards = gridContainer.querySelectorAll(".card-link")
  const countEl = gridContainer.querySelector(".card-grid-count")

  const updateCount = () => {
    const visibleCount = gridContainer.querySelectorAll(".card-link:not([style*='display: none'])").length
    if (countEl) {
      countEl.textContent = `${visibleCount} note${visibleCount > 1 ? "s" : ""}`
    }
  }

  const filterCards = (folder: string) => {
    cards.forEach((card) => {
      const cardFolder = card.getAttribute("data-folder") || ""
      if (folder === "all" || cardFolder.toLowerCase().includes(folder.toLowerCase())) {
        ;(card as HTMLElement).style.display = ""
      } else {
        ;(card as HTMLElement).style.display = "none"
      }
    })
    updateCount()
  }

  filterButtons.forEach((btn) => {
    const handleClick = () => {
      filterButtons.forEach((b) => b.classList.remove("active"))
      btn.classList.add("active")
      const folder = btn.getAttribute("data-folder") || "all"
      filterCards(folder)
    }
    btn.addEventListener("click", handleClick)
    window.addCleanup(() => btn.removeEventListener("click", handleClick))
  })

  updateCount()
})
