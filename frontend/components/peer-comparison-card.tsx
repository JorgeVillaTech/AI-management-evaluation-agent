interface PeerCompany {
    ticker: string;
    name: string;
    exchange: string;
    industry: string;
    market_cap: number;
    current_price: number;
    day_change_percent: number;
}

interface PeerComparison {
    company: PeerCompany;
    peers: PeerCompany[];
    error?: string;
}

function CompanyRow({ company, isPrimary }: { company: PeerCompany; isPrimary?: boolean }) {
    const changeColor = company.day_change_percent >= 0 ? "var(--risk-low)" : "var(--risk-high)";
    return (
        <div
        className="flex items-center justify-between py-2 px-3 border-b last:border-b-0"
        style={{ borderColor: "var(--hairline)", background: isPrimary ? "rgba(180,83,9,0.06)" : "transparent" }}
        >
        <div className="min-w-0">
            <div className="text-sm truncate" style={{ fontWeight: isPrimary ? 500 : 400 }}>{company.name}</div>
            <div className="text-xs text-muted-foreground">{company.ticker} · {company.exchange}</div>
        </div>
        <div className="text-right shrink-0 ml-3">
            <div className="font-mono text-sm">${company.current_price}</div>
            <div className="font-mono text-xs" style={{ color: changeColor }}>
            {company.day_change_percent >= 0 ? "+" : ""}{company.day_change_percent.toFixed(2)}%
            </div>
        </div>
        </div>
    );
}

export function PeerComparisonCard({ comparison }: { comparison: PeerComparison }) {
    if (comparison.error) {
        return (
        <div className="my-2 border rounded-md p-3 text-sm" style={{ borderColor: "var(--risk-high)", color: "var(--risk-high)" }}>
            {comparison.error}
        </div>
        );
    }

    return (
        <div className="my-2 overflow-hidden" style={{ background: "var(--surface)", borderRadius: "var(--radius-md)", border: "1px solid var(--hairline)" }}>
        <div className="px-4 py-3 border-b" style={{ borderColor: "var(--hairline)" }}>
            <div className="font-display font-medium">Peer Comparison</div>
            <div className="text-xs text-muted-foreground">{comparison.company.industry}</div>
        </div>
        <CompanyRow company={comparison.company} isPrimary />
        {comparison.peers.map((p) => (
            <CompanyRow key={p.ticker} company={p} />
        ))}
        </div>
    );
}