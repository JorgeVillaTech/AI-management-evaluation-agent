interface MeetingBriefing {
    company_name: string;
    risk_score: number;
    risk_level: "High" | "Moderate" | "Low";
    sector: string;
    market_data_available: boolean;
    current_price: number | null;
    exchange: string | null;
    talking_points: string[];
    error?: string;
}

function levelColor(level: string) {
    if (level === "High") return "var(--risk-high)";
    if (level === "Moderate") return "var(--accent)";
    return "var(--risk-low)";
}

export function MeetingBriefingCard({ briefing }: { briefing: MeetingBriefing }) {
    if (briefing.error) {
        return (
        <div className="my-2 border rounded-md p-3 text-sm" style={{ borderColor: "var(--risk-high)", color: "var(--risk-high)" }}>
            {briefing.error}
        </div>
        );
    }

    return (
        <div className="my-2 overflow-hidden" style={{ background: "var(--surface)", borderRadius: "var(--radius-md)", border: "1px solid var(--hairline)" }}>
        <div className="flex items-center justify-between px-4 py-3 border-b" style={{ borderColor: "var(--hairline)" }}>
            <div>
            <div className="font-display font-medium">{briefing.company_name}</div>
            <div className="text-xs text-muted-foreground">Meeting Briefing · {briefing.sector}</div>
            </div>
            <span className="font-mono text-xs px-2.5 py-0.5 rounded-full text-white" style={{ background: levelColor(briefing.risk_level) }}>
            {briefing.risk_level ? (
                <span className="font-mono text-xs px-2.5 py-0.5 rounded-full text-white" style={{ background: levelColor(briefing.risk_level) }}>
                    {briefing.risk_level} risk
                </span>
                ) : (
                <span className="font-mono text-xs px-2.5 py-0.5 rounded-full text-white bg-gray-400">No risk data</span>
                )}
            </span>
        </div>

        <div className="px-4 py-3 grid grid-cols-2 gap-3 border-b text-sm" style={{ borderColor: "var(--hairline)" }}>
            <div>
            <div className="text-xs text-muted-foreground">Risk Score</div>
            <div className="font-mono">{briefing.risk_score !== null ? `${briefing.risk_score}/100` : "N/A"}</div>
            </div>
            <div>
            <div className="text-xs text-muted-foreground">Market Data</div>
            <div className="font-mono">
                {briefing.market_data_available ? `$${briefing.current_price} · ${briefing.exchange}` : "Not available"}
            </div>
            </div>
        </div>

        <div className="px-4 py-3 text-sm">
            <div className="text-xs text-muted-foreground mb-1.5">Talking Points</div>
            <ul className="space-y-1.5">
            {briefing.talking_points.map((point, i) => (
                <li key={i} className="flex gap-2">
                <span className="font-mono text-xs mt-0.5" style={{ color: "var(--accent)" }}>{i + 1}</span>
                <span>{point}</span>
                </li>
            ))}
            </ul>
        </div>
        </div>
    );
}