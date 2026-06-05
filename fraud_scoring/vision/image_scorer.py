"""Vision fraud scorer — ViT + CLIP image tampering detection.

Sync path: lightweight image hash check (<15ms budget).
Async path: full ViT analysis post-submission.
Planned Week 6.
"""
from __future__ import annotations


class ImageFraudScorer:
    """ViT/CLIP-based image tampering detection."""

    def hash_check_sync(self, image_bytes: bytes) -> float | None:
        """Lightweight perceptual hash check for sync path. None = not implemented."""
        return None  # stub — hash check planned Week 4

    def score_async(self, image_bytes: bytes) -> float | None:
        """Full ViT analysis for async enrichment path. None = not implemented."""
        return None  # stub — ViT scoring planned Week 6
