interface CompanyProfile {
    name: string;
    sector: string;
    risk_score: number;
    trend: string;
    recent_signals: string[];
    error?: string;
}

function riskColor(score: number) {
    if (score >= 60) return "var(--risk-high)";
    if (score >= 35) return "var(--accent)";
    return "var(--risk-low)";
}

export function CompanyProfileCard({ profile }: { profile: CompanyProfile }) {
    if (profile.error) {
        return (
        <div className="my-2 border rounded-md p-3 text-sm" style={{ borderColor: "var(--risk-high)", color: "var(--risk-high)" }}>
            {profile.error}
        </div>
        );
    }

    return (
        <div className="my-2 border rounded-md overflow-hidden" style={{ borderColor: "var(--hairline)" }}>
        <div className="flex items-center justify-between px-4 py-3 border-b" style={{ borderColor: "var(--hairline)" }}>
            <span className="font-display font-medium">{profile.name}</span>
            <span className="font-mono text-sm px-2 py-0.5 rounded text-white" style={{ background: riskColor(profile.risk_score) }}>
            {profile.risk_score}
            </span>
        </div>
        <div className="px-4 py-3 text-sm">
            <div className="grid grid-cols-[80px_1fr] gap-y-1.5">
            <span className="text-muted-foreground">Sector</span>
            <span>{profile.sector}</span>
            <span className="text-muted-foreground">Trend</span>
            <span>{profile.trend}</span>
            </div>
            <div className="mt-3">
            <span className="text-muted-foreground">Recent signals</span>
            <ul className="list-disc list-inside mt-1">
                {profile.recent_signals.map((s, i) => <li key={i}>{s}</li>)}
            </ul>
            </div>
        </div>
        </div>
    );
}