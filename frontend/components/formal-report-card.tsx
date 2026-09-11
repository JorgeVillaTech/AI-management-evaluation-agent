interface FormalReport {
    company_name: string;
    sector: string;
    risk_score: number;
    risk_level: "High" | "Moderate" | "Low";
    trend: string;
    executive_summary: string;
    key_signals: string[];
    recommendation: string;
    error?: string;
}

function levelColor(level: string) {
    if (level === "High") return "var(--risk-high)";
    if (level === "Moderate") return "var(--accent)";
    return "var(--risk-low)";
}

export function FormalReportCard({ report }: { report: FormalReport }) {
    if (report.error) {
        return (
        <div className="my-2 border rounded-md p-3 text-sm" style={{ borderColor: "var(--risk-high)", color: "var(--risk-high)" }}>
            {report.error}
        </div>
        );
    }

    return (
        <div className="my-2 border rounded-md overflow-hidden" style={{ borderColor: "var(--hairline)" }}>
        <div className="flex items-center justify-between px-4 py-3 border-b" style={{ borderColor: "var(--hairline)" }}>
            <div>
            <div className="font-display font-medium">{report.company_name}</div>
            <div className="text-xs text-muted-foreground">Formal Risk Report</div>
            </div>
            <span className="font-mono text-sm px-2 py-0.5 rounded text-white" style={{ background: levelColor(report.risk_level) }}>
            {report.risk_level}
            </span>
        </div>
        <div className="px-4 py-3 space-y-3 text-sm">
            <p>{report.executive_summary}</p>
            <div>
            <span className="text-muted-foreground">Key signals</span>
            <ul className="list-disc list-inside mt-1">
                {report.key_signals.map((s, i) => <li key={i}>{s}</li>)}
            </ul>
            </div>
            <p className="border-t pt-2" style={{ borderColor: "var(--hairline)" }}>
            <span className="text-muted-foreground">Recommendation</span> {report.recommendation}
            </p>
        </div>
        </div>
    );
}