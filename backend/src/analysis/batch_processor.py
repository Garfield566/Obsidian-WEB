"""Processeur par batch pour traitement efficace de grands volumes."""

from dataclasses import dataclass
from typing import Iterator, Optional, Callable, Any
import time


@dataclass
class BatchProgress:
    """État de progression du traitement par batch."""
    current_batch: int
    total_batches: int
    items_processed: int
    total_items: int
    elapsed_seconds: float
    items_per_second: float

    @property
    def percentage(self) -> float:
        if self.total_items == 0:
            return 100.0
        return (self.items_processed / self.total_items) * 100

    @property
    def eta_seconds(self) -> float:
        if self.items_per_second == 0:
            return 0
        remaining = self.total_items - self.items_processed
        return remaining / self.items_per_second


class BatchProcessor:
    """Processeur pour traitement par batch avec suivi de progression."""

    def __init__(
        self,
        batch_size: int = 100,
        progress_callback: Optional[Callable[[BatchProgress], None]] = None,
    ):
        self.batch_size = batch_size
        self.progress_callback = progress_callback

    def process(
        self,
        items: list,
        process_fn: Callable[[list], Any],
        desc: str = "Processing",
    ) -> list:
        """Traite une liste d'items par batch.

        Args:
            items: Liste d'items à traiter
            process_fn: Fonction qui traite un batch et retourne les résultats
            desc: Description pour le log

        Returns:
            Liste des résultats combinés
        """
        total = len(items)
        if total == 0:
            return []

        results = []
        start_time = time.time()
        items_processed = 0

        for batch_idx, batch in enumerate(self._batches(items)):
            batch_results = process_fn(batch)

            if isinstance(batch_results, list):
                results.extend(batch_results)
            elif isinstance(batch_results, dict):
                if not results:
                    results = {}
                results.update(batch_results)
            else:
                results.append(batch_results)

            items_processed += len(batch)
            elapsed = time.time() - start_time
            rate = items_processed / elapsed if elapsed > 0 else 0

            if self.progress_callback:
                progress = BatchProgress(
                    current_batch=batch_idx + 1,
                    total_batches=(total + self.batch_size - 1) // self.batch_size,
                    items_processed=items_processed,
                    total_items=total,
                    elapsed_seconds=elapsed,
                    items_per_second=rate,
                )
                self.progress_callback(progress)

        return results

    def process_pairs(
        self,
        items: list,
        process_fn: Callable[[list, list], Any],
        max_comparisons: int = 100000,
        desc: str = "Processing pairs",
    ) -> list:
        """Traite des paires d'items de manière efficace.

        Utilise un échantillonnage si trop de comparaisons.

        Args:
            items: Liste d'items
            process_fn: Fonction qui traite deux listes et retourne les résultats
            max_comparisons: Nombre max de comparaisons
            desc: Description

        Returns:
            Liste des résultats
        """
        n = len(items)
        total_pairs = n * (n - 1) // 2

        if total_pairs <= max_comparisons:
            # Traitement exhaustif par blocs
            return self._process_pairs_exhaustive(items, process_fn, desc)
        else:
            # Échantillonnage intelligent
            return self._process_pairs_sampled(items, process_fn, max_comparisons, desc)

    def _process_pairs_exhaustive(
        self,
        items: list,
        process_fn: Callable,
        desc: str,
    ) -> list:
        """Traitement exhaustif des paires."""
        n = len(items)
        results = []
        start_time = time.time()
        pairs_processed = 0
        total_pairs = n * (n - 1) // 2

        # Traite par blocs de lignes
        for i in range(0, n, self.batch_size):
            batch_i = items[i:i + self.batch_size]
            remaining = items[i + len(batch_i):]

            if remaining:
                batch_results = process_fn(batch_i, remaining)
                if batch_results:
                    results.extend(batch_results)

            # Paires dans le batch lui-même
            for j in range(len(batch_i)):
                for k in range(j + 1, len(batch_i)):
                    result = process_fn([batch_i[j]], [batch_i[k]])
                    if result:
                        results.extend(result)

            pairs_processed += len(batch_i) * len(remaining) + len(batch_i) * (len(batch_i) - 1) // 2

            if self.progress_callback:
                elapsed = time.time() - start_time
                progress = BatchProgress(
                    current_batch=i // self.batch_size + 1,
                    total_batches=(n + self.batch_size - 1) // self.batch_size,
                    items_processed=pairs_processed,
                    total_items=total_pairs,
                    elapsed_seconds=elapsed,
                    items_per_second=pairs_processed / elapsed if elapsed > 0 else 0,
                )
                self.progress_callback(progress)

        return results

    def _process_pairs_sampled(
        self,
        items: list,
        process_fn: Callable,
        max_comparisons: int,
        desc: str,
    ) -> list:
        """Traitement échantillonné des paires."""
        import random

        n = len(items)
        results = []

        # Calcule le taux d'échantillonnage
        total_pairs = n * (n - 1) // 2
        sample_rate = max_comparisons / total_pairs

        start_time = time.time()
        comparisons_done = 0

        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < sample_rate:
                    result = process_fn([items[i]], [items[j]])
                    if result:
                        results.extend(result)
                    comparisons_done += 1

                    if comparisons_done >= max_comparisons:
                        return results

                    if self.progress_callback and comparisons_done % 1000 == 0:
                        elapsed = time.time() - start_time
                        progress = BatchProgress(
                            current_batch=comparisons_done // 1000,
                            total_batches=max_comparisons // 1000,
                            items_processed=comparisons_done,
                            total_items=max_comparisons,
                            elapsed_seconds=elapsed,
                            items_per_second=comparisons_done / elapsed if elapsed > 0 else 0,
                        )
                        self.progress_callback(progress)

        return results

    def _batches(self, items: list) -> Iterator[list]:
        """Génère des batches à partir d'une liste."""
        for i in range(0, len(items), self.batch_size):
            yield items[i:i + self.batch_size]


def print_progress(progress: BatchProgress) -> None:
    """Callback de progression par défaut."""
    eta = progress.eta_seconds
    eta_str = f"{int(eta // 60)}m {int(eta % 60)}s" if eta > 0 else "N/A"

    print(
        f"\r  [{progress.percentage:5.1f}%] "
        f"{progress.items_processed}/{progress.total_items} "
        f"({progress.items_per_second:.1f}/s) "
        f"ETA: {eta_str}",
        end="",
        flush=True,
    )

    if progress.items_processed >= progress.total_items:
        print()  # Nouvelle ligne à la fin
