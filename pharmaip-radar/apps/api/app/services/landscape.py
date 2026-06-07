"""Landscape analyzer — density, top assignees, tech clustering."""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import date

import numpy as np
from sklearn.cluster import KMeans

from app.schemas.landscape import (
    AssigneeStat,
    DensityCell,
    LandscapeAnalysis,
    TechCluster,
)


class LandscapeAnalyzer:
    """Compute landscape metrics from a list of patent dicts."""

    def __init__(self, patents: list[dict], n_clusters: int = 4) -> None:
        self.patents = patents
        self.n_clusters = max(1, min(n_clusters, len(patents)))

    def analyze(self) -> LandscapeAnalysis:
        if not self.patents:
            return LandscapeAnalysis(
                total_patents=0,
                unique_assignees=0,
                summary="No patents provided.",
            )

        # Filing trend by year
        trend: dict[int, int] = defaultdict(int)
        for p in self.patents:
            fd = p.get("filing_date")
            if isinstance(fd, str):
                try:
                    fd = date.fromisoformat(fd)
                except ValueError:
                    fd = None
            if isinstance(fd, date):
                trend[fd.year] += 1

        # Density heatmap: IPC class × year
        heatmap: list[DensityCell] = []
        ipc_year: dict[tuple[str, int], int] = defaultdict(int)
        for p in self.patents:
            fd = p.get("filing_date")
            year = None
            if isinstance(fd, str):
                try:
                    year = date.fromisoformat(fd).year
                except ValueError:
                    year = None
            elif isinstance(fd, date):
                year = fd.year
            for ipc in p.get("ipc_classes", []) or []:
                if year is not None:
                    ipc_year[(ipc[:4], year)] += 1  # IPC subclass
        if ipc_year:
            max_count = max(ipc_year.values()) or 1
            for (ipc, year), count in ipc_year.items():
                heatmap.append(
                    DensityCell(
                        ipc_class=ipc,
                        year=year,
                        count=count,
                        density=count / max_count,
                    )
                )

        # Top assignees
        assignees = Counter(
            p["assignee"] for p in self.patents if p.get("assignee")
        )
        total = sum(assignees.values()) or 1
        top_assignees = [
            AssigneeStat(
                assignee=name,
                patent_count=count,
                market_share=count / total,
            )
            for name, count in assignees.most_common(10)
        ]

        # Tech clustering by abstract text
        abstracts = [p.get("abstract", "") or p.get("title", "") for p in self.patents]
        clusters = self._cluster(abstracts)

        # White space: years with little activity
        white_space = []
        if trend:
            avg = sum(trend.values()) / len(trend)
            for y, c in sorted(trend.items()):
                if c < avg * 0.3:
                    white_space.append(str(y))

        return LandscapeAnalysis(
            total_patents=len(self.patents),
            unique_assignees=len(assignees),
            filing_trend=dict(trend),
            density_heatmap=heatmap,
            top_assignees=top_assignees,
            tech_clusters=clusters,
            white_space=white_space,
            summary=self._summary(trend, top_assignees, clusters),
        )

    def _cluster(self, texts: list[str]) -> list[TechCluster]:
        from sklearn.feature_extraction.text import TfidfVectorizer

        if len(texts) < 2:
            return []
        try:
            vec = TfidfVectorizer(stop_words="english", max_features=500)
            X = vec.fit_transform(texts)
            km = KMeans(n_clusters=self.n_clusters, n_init=4, random_state=42)
            labels = km.fit_predict(X)
        except Exception:
            return []

        terms = vec.get_feature_names_out()
        order_centroids = km.cluster_centers_.argsort()[:, ::-1]
        clusters: list[TechCluster] = []
        for cid in range(self.n_clusters):
            members = [i for i, l in enumerate(labels) if l == cid]
            if not members:
                continue
            top_terms = [terms[i] for i in order_centroids[cid, :5]]
            member_assignees = Counter(
                self.patents[i]["assignee"]
                for i in members
                if self.patents[i].get("assignee")
            )
            member_drugs = Counter(
                self.patents[i]["drug_name"]
                for i in members
                if self.patents[i].get("drug_name")
            )
            clusters.append(
                TechCluster(
                    cluster_id=cid,
                    label=", ".join(top_terms[:3]) or f"cluster-{cid}",
                    size=len(members),
                    top_assignees=[a for a, _ in member_assignees.most_common(5)],
                    top_drugs=[d for d, _ in member_drugs.most_common(5)],
                )
            )
        return clusters

    def _summary(
        self,
        trend: dict[int, int],
        top_assignees: list[AssigneeStat],
        clusters: list[TechCluster],
    ) -> str:
        if not trend:
            return "Limited data for analysis."
        peak_year = max(trend, key=trend.get)  # type: ignore[arg-type]
        leader = top_assignees[0].assignee if top_assignees else "Unknown"
        n = len(self.patents)
        return (
            f"Landscape covers {n} patents. Peak filing year: {peak_year} "
            f"({trend[peak_year]} filings). Market leader: {leader}. "
            f"{len(clusters)} distinct technology cluster(s) identified."
        )
