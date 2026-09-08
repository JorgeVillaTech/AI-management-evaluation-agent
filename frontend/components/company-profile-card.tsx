import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

// Structure
interface CompanyProfile {
    name: string;
    sector: string;
    risk_score: number;
    trend: string;
    recent_signals: string[];
    error?: string;
}

function riskVariant(score: number): "default" | "destructive" | "secondary" {
    if (score >= 60) return "destructive";
    if (score >= 35) return "secondary";
    return "default";
}

export function CompanyProfileCard({ profile }: { profile: CompanyProfile }) {
    if (profile.error) {
        return (
        <Card className="my-2 border-destructive">
            <CardContent className="pt-4 text-sm text-muted-foreground">
            {profile.error}
            </CardContent>
        </Card>
        );
    }

    return (
        <Card className="my-2">
        <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle>{profile.name}</CardTitle>
            <Badge variant={riskVariant(profile.risk_score)}>
            Risk: {profile.risk_score}
            </Badge>
        </CardHeader>
        <CardContent className="space-y-2 text-sm">
            <p><span className="text-muted-foreground">Sector:</span> {profile.sector}</p>
            <p><span className="text-muted-foreground">Trend:</span> {profile.trend}</p>
            <div>
            <span className="text-muted-foreground">Recent signals:</span>
            <ul className="list-disc list-inside mt-1">
                {profile.recent_signals.map((s, i) => (
                <li key={i}>{s}</li>
                ))}
            </ul>
            </div>
        </CardContent>
        </Card>
    );
}