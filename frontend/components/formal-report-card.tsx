import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

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

function levelVariant(level: string): "default" | "destructive" | "secondary" {
    if (level === "High") return "destructive";
    if (level === "Moderate") return "secondary";
    return "default";
}

export function FormalReportCard({ report }: { report: FormalReport }) {
    if (report.error) {
        return (
        <Card className="my-2 border-destructive">
            <CardContent className="pt-4 text-sm text-muted-foreground">{report.error}</CardContent>
        </Card>
        );
    }

    return (
        <Card className="my-2">
        <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle>Formal Risk Report — {report.company_name}</CardTitle>
            <Badge variant={levelVariant(report.risk_level)}>{report.risk_level} risk</Badge>
        </CardHeader>
        <CardContent className="space-y-3 text-sm">
            <p><span className="text-muted-foreground">Executive summary:</span> {report.executive_summary}</p>
            <div>
            <span className="text-muted-foreground">Key signals:</span>
            <ul className="list-disc list-inside mt-1">
                {report.key_signals.map((s, i) => <li key={i}>{s}</li>)}
            </ul>
            </div>
            <p className="border-t pt-2"><span className="text-muted-foreground">Recommendation:</span> {report.recommendation}</p>
        </CardContent>
        </Card>
    );
}