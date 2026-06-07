"""Pydantic schemas."""

from app.schemas.common import (
    HealthResponse,
    PageResponse,
    ErrorResponse,
)
from app.schemas.patent import (
    PatentRead,
    PatentSummary,
    PatentClaimRead,
    PatentSearchRequest,
    PatentSearchResult,
    TherapeuticArea,
    Jurisdiction,
)
from app.schemas.landscape import (
    LandscapeRead,
    LandscapeSummary,
    LandscapeCreate,
    LandscapePatentRead,
    DensityCell,
    LandscapeAnalysis,
)
from app.schemas.watchlist import (
    WatchlistRead,
    WatchlistCreate,
    WatchlistUpdate,
    InfringementAlertRead,
    RiskLevel,
)
from app.schemas.report import (
    ReportRead,
    ReportCreate,
    ReportType,
    ReportStatus,
)

__all__ = [
    "HealthResponse",
    "PageResponse",
    "ErrorResponse",
    "PatentRead",
    "PatentSummary",
    "PatentClaimRead",
    "PatentSearchRequest",
    "PatentSearchResult",
    "TherapeuticArea",
    "Jurisdiction",
    "LandscapeRead",
    "LandscapeSummary",
    "LandscapeCreate",
    "LandscapePatentRead",
    "DensityCell",
    "LandscapeAnalysis",
    "WatchlistRead",
    "WatchlistCreate",
    "WatchlistUpdate",
    "InfringementAlertRead",
    "RiskLevel",
    "ReportRead",
    "ReportCreate",
    "ReportType",
    "ReportStatus",
]
