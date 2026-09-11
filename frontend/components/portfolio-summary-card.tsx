interface PortfolioEntry {
    name: string;
    risk_score: number;
    trend?: string;
    sector: string;
}

interface PortfolioSummary {
    total_companies: number;
    high_risk_count: number;
    worsening_count: number;
    top_concerns: PortfolioEntry[];
    worsening_trend: PortfolioEntry[];
}

function riskColor(score: number) {
    if (score >= 60) return "var(--risk-high)";
    if (score >= 35) return "var(--accent)";
    return "var(--risk-low)";
}

function EntryRow({ entry }: { entry: PortfolioEntry }) {
    return (
        <div className="flex items-center justify-between py-1.5 border-b last:border-b-0" style={{ borderColor: "var(--hairline)" }}>
        <div className="flex items-center gap-2 min-w-0">
            <span className="w-1 h-3.5 shrink-0 rounded-sm" style={{ background: riskColor(entry.risk_score) }} />
            <span className="truncate">{entry.name}</span>
        </div>
        <span className="font-mono text-xs text-muted-foreground shrink-0 ml-2">{entry.sector}</span>
        <span className="font-mono ml-2 shrink-0">{entry.risk_score}</span>
        </div>
    );
}

export function PortfolioSummaryCard({ summary }: { summary: PortfolioSummary }) {
    return (
        <div className="my-2 overflow-hidden" style={{ background: "var(--surface)", borderRadius: "var(--radius-md)", border: "1px solid var(--hairline)" }}>
        <div className="px-4 py-3 border-b" style={{ borderColor: "var(--hairline)" }}>
            <div className="font-display font-medium">Portfolio Risk Summary</div>
            <div className="flex gap-4 mt-1.5 text-xs text-muted-foreground">
            <span>{summary.total_companies} companies tracked</span>
            <span style={{ color: "var(--risk-high)" }}>{summary.high_risk_count} high-risk</span>
            <span style={{ color: "var(--accent)" }}>{summary.worsening_count} worsening</span>
            </div>
        </div>

        <div className="px-4 py-3 border-b text-sm" style={{ borderColor: "var(--hairline)" }}>
            <div className="text-xs text-muted-foreground mb-1.5">Top concerns</div>
            {summary.top_concerns.map((c) => <EntryRow key={c.name} entry={c} />)}
        </div>

        <div className="px-4 py-3 text-sm">
            <div className="text-xs text-muted-foreground mb-1.5">Worsening trend</div>
            {summary.worsening_trend.map((c) => <EntryRow key={c.name} entry={c} />)}
        </div>
        </div>
    );
}