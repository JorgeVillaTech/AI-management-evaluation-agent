import { HttpAgent } from "@ag-ui/client";
import {
    CopilotRuntime,
    ExperimentalEmptyAdapter,
    copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";
import { NextRequest } from "next/server";

const riskAdvisorAgent = new HttpAgent({
    url: "http://localhost:8000/copilotkit",
});

const runtime = new CopilotRuntime({
    agents: {
        default: riskAdvisorAgent,
    },
});

const serviceAdapter = new ExperimentalEmptyAdapter();

export const POST = async (req: NextRequest) => {
    const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
        runtime,
        serviceAdapter,
        endpoint: "/api/copilotkit",
    });
    return handleRequest(req);
};