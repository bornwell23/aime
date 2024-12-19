import { version } from "os";
import { versions } from "process";
import v1Router from '@/server/src/api/v1/index.js';

class Definitions {
    constructor() {
        this.ui = {
            port: "8008",
            logLevel: "INFO",
            node_env: "development",
            serviceName: "ui",
            logFileName: "ui.log"
        };
        this.server = {
            api_url: "http://server:3000",
            logLevel: "INFO",
            node_env: "development",
            port: "3000",
            serviceName: "server",
            logFileName: "server.log"
        };
        this.api = {
            version: "v1",
            versions: [
                "v1",
                "v2"],
            routers: {
                "v1": v1Router,
            },
            timeout: 5000
        };
        this.auth = {
            port: "8000",
            logLevel: "INFO",
            node_env: "development",
            serviceName: "auth",
            logFileName: "auth.log",
            jwtsecret: "secret",
        };
    }
}

export { Definitions };