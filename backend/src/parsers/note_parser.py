"""Parser pour les notes Obsidian avec extraction de métadonnées."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import hashlib
import re

import frontmatter


@dataclass
class ParsedNote:
    """Représente une note Obsidian parsée."""

    path: str
    title: str
    content: str  # Texte brut sans frontmatter
    frontmatter: dict = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)
    outgoing_links: list[str] = field(default_factory=list)
    incoming_links: list[str] = field(default_factory=list)
    note_type: Optional[str] = None
    content_hash: str = ""

    def __post_init__(self):
        if not self.content_hash:
            self.content_hash = hashlib.md5(self.content.encode()).hexdigest()


class NoteParser:
    """Parse les notes Obsidian et extrait les métadonnées."""

    # Patterns pour l'extraction
    WIKILINK_PATTERN = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
    TAG_PATTERN = re.compile(r"(?:^|\s)#([a-zA-Z0-9_/\-]+)", re.MULTILINE)
    INLINE_TAG_PATTERN = re.compile(r"#([a-zA-Z0-9_/\-]+)")

    # Extensions de fichiers à ignorer (images, media, etc.)
    IGNORED_EXTENSIONS = {
        '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.webp',
        '.mp3', '.mp4', '.wav', '.ogg', '.webm', '.mov',
        '.pdf', '.zip', '.rar', '.7z',
    }

    # Dossiers à ignorer completement
    IGNORED_FOLDERS = {
        '.obsidian', '.git', '.trash', 'z_Templates', 'Templates',
        'templates', '_templates', 'z_templates', 'Sans titre',
    }

    # Patterns de fichiers à ignorer (case-insensitive matching)
    IGNORED_FILE_PATTERNS = [
        '.sidecar.md',      # Notes d'images (plugin Image Sidecar)
        'Pasted image',     # Images collees
        'Template',         # Fichiers template
        'template',         # Fichiers template (minuscule)
        'Sans titre',       # Notes non nommées
        'Untitled',         # Notes non nommées (anglais)
    ]

    # Préfixes de noms de fichiers à ignorer (commence par...)
    IGNORED_FILE_PREFIXES = [
        'test', 'teste',                    # Notes de test
        'todo', 'a faire',                  # Listes de tâches
        'brouillon', 'draft',               # Brouillons
        'temp', 'tmp', 'scratch',           # Fichiers temporaires
    ]

    # Noms de fichiers exacts à ignorer (sans extension)
    IGNORED_FILE_NAMES = {
        'tests',                            # Fichier tests exact
        'todos',                            # Fichier todos exact
        'drafts',                           # Fichier drafts exact
        'index', 'readme', 'home',          # Fichiers d'index
        'inbox', 'boite de reception',      # Inbox
    }

    def __init__(self, vault_path: str | Path):
        # Résout le chemin en absolu pour éviter les problèmes de chemins relatifs
        self.vault_path = Path(vault_path).resolve()
        self._note_cache: dict[str, ParsedNote] = {}

    def parse_note(self, note_path: str | Path) -> ParsedNote:
        """Parse une note et extrait toutes ses métadonnées."""
        path = Path(note_path)
        # Résout le chemin en absolu
        if not path.is_absolute():
            path = self.vault_path / path
        path = path.resolve()

        with open(path, "r", encoding="utf-8") as f:
            raw_content = f.read()

        # Parse le frontmatter YAML
        post = frontmatter.loads(raw_content)
        fm = dict(post.metadata) if post.metadata else {}
        content = post.content

        # Extrait le titre (premier H1 ou nom du fichier)
        title = self._extract_title(content, path)

        # Extrait les tags (frontmatter + inline)
        tags = self._extract_tags(fm, content)

        # Extrait les liens wiki
        outgoing_links = self._extract_links(content)

        # Détermine le type de note
        note_type = self._determine_note_type(fm, tags, content)

        # Crée le chemin relatif au vault
        relative_path = path.relative_to(self.vault_path).as_posix()

        return ParsedNote(
            path=relative_path,
            title=title,
            content=content,
            frontmatter=fm,
            tags=tags,
            outgoing_links=outgoing_links,
            incoming_links=[],  # Calculé après parsing de toutes les notes
            note_type=note_type,
        )

    def parse_vault(self) -> list[ParsedNote]:
        """Parse toutes les notes du vault."""
        notes: list[ParsedNote] = []
        note_paths: dict[str, ParsedNote] = {}

        # Premier passage : parser toutes les notes markdown
        for md_file in self.vault_path.rglob("*.md"):
            # Ignore les fichiers dans les dossiers exclus
            if any(folder in md_file.parts for folder in self.IGNORED_FOLDERS):
                continue

            # Vérifie que c'est bien un fichier markdown (pas une image, etc.)
            if md_file.suffix.lower() in self.IGNORED_EXTENSIONS:
                continue

            # Ignore les fichiers qui matchent les patterns exclus
            file_name = md_file.name
            file_stem_lower = md_file.stem.lower()
            if any(pattern.lower() in file_name.lower() for pattern in self.IGNORED_FILE_PATTERNS):
                continue

            # Ignore les noms de fichiers exacts (test, brouillon, etc.)
            if file_stem_lower in self.IGNORED_FILE_NAMES:
                continue

            # Ignore les fichiers dont le nom commence par un préfixe exclu
            if any(file_stem_lower.startswith(prefix) for prefix in self.IGNORED_FILE_PREFIXES):
                continue

            try:
                note = self.parse_note(md_file)
                notes.append(note)
                # Index par le nom du fichier (sans extension) pour les liens
                note_name = md_file.stem
                note_paths[note_name.lower()] = note
            except Exception as e:
                # Ignore silently - encoding issues with Windows console
                continue

        # Deuxième passage : calculer les liens entrants
        for note in notes:
            for link in note.outgoing_links:
                link_lower = link.lower()
                if link_lower in note_paths:
                    target_note = note_paths[link_lower]
                    if note.path not in target_note.incoming_links:
                        target_note.incoming_links.append(note.path)

        self._note_cache = {n.path: n for n in notes}
        return notes

    def _extract_title(self, content: str, path: Path) -> str:
        """Extrait le titre de la note."""
        # Cherche le premier H1
        h1_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if h1_match:
            return h1_match.group(1).strip()
        # Sinon utilise le nom du fichier
        return path.stem

    def _extract_tags(self, frontmatter: dict, content: str) -> list[str]:
        """Extrait tous les tags (frontmatter + inline)."""
        tags = set()

        # Tags du frontmatter
        fm_tags = frontmatter.get("tags", [])
        if isinstance(fm_tags, str):
            fm_tags = [fm_tags]
        for tag in fm_tags:
            tags.add(tag.lstrip("#"))

        # Tags inline dans le contenu
        inline_tags = self.INLINE_TAG_PATTERN.findall(content)
        for tag in inline_tags:
            tags.add(tag)

        return sorted(list(tags))

    def _extract_links(self, content: str) -> list[str]:
        """Extrait tous les liens wiki [[...]]."""
        links = self.WIKILINK_PATTERN.findall(content)
        # Nettoie les liens (enlève les ancres #heading)
        cleaned = []
        for link in links:
            # Enlève l'ancre si présente
            link = link.split("#")[0].strip()
            if link and link not in cleaned:
                cleaned.append(link)
        return cleaned

    def _determine_note_type(
        self, frontmatter: dict, tags: list[str], content: str
    ) -> Optional[str]:
        """Détermine le type de note basé sur les métadonnées."""
        # Vérifie le frontmatter d'abord
        if "type" in frontmatter:
            return str(frontmatter["type"])

        # Vérifie les tags pour des patterns de type
        type_patterns = {
            "idee": ["Idée", "idee", "idea"],
            "analyse": ["Analyse", "analyse", "analysis"],
            "oeuvre": ["Oeuvre", "oeuvre", "work"],
            "historique": ["Historique", "historique", "history"],
            "concept": ["Concept", "concept"],
            "personne": ["Personne", "person", "auteur"],
            "methode": ["Méthode", "methode", "method"],
        }

        for note_type, patterns in type_patterns.items():
            for pattern in patterns:
                for tag in tags:
                    if pattern.lower() in tag.lower():
                        return note_type

        return None

    def get_note(self, path: str) -> Optional[ParsedNote]:
        """Récupère une note du cache."""
        return self._note_cache.get(path)
