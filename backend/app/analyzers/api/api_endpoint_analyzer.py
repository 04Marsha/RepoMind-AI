import re

from app.models.api.ApiAnalysis import ApiAnalysis
from app.models.repository.RepositoryContext import RepositoryContext
from app.models.api.ApiEndpoint import ApiEndpoint

class ApiEndpointAnalyzer:

    def __init__(self, repository_analyzer):
        self.repository_analyzer = repository_analyzer

    def analyze(self, context: RepositoryContext) -> ApiAnalysis:

        analysis = ApiAnalysis()

        analysis.endpoints.extend(
            self.detect_fastapi(context)
        )

        analysis.endpoints.extend(
            self.detect_flask(context)
        )

        analysis.endpoints.extend(
            self.detect_express(context)
        )

        analysis.endpoints.extend(
            self.detect_spring_boot(context)
        )

        analysis.endpoints = self.deduplicate_endpoints(
            analysis.endpoints
        )

        return analysis

    def get_source_files(self, context: RepositoryContext, *extensions: str): 
        return [
            file for file in self.repository_analyzer.get_source_files(context.repository_root)
            if file.suffix in extensions
        ]

    def find_handler(self, text: str, start: int):
        handler_pattern = re.compile(r'(?:async\s+)?def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(')
        match = handler_pattern.search(text, start)

        if match:
            return match.group(1)
        return "Unknown"
    
    def find_router_prefixes(self, text: str) -> dict[str, str]:

        pattern = re.compile(r'([A-Za-z_][A-Za-z0-9_]*)\s*=\s*APIRouter\((.*?)\)', re.DOTALL)
        prefixes = {}

        for match in pattern.finditer(text):
            router_name = match.group(1)
            arguments = match.group(2)

            prefix_match = re.search(r'prefix\s*=\s*[\'"]([^\'"]+)[\'"]', arguments)
            if prefix_match:
                prefixes[router_name] = prefix_match.group(1)
            else:
                prefixes[router_name] = ""

        return prefixes

    def detect_fastapi(self, context):
        endpoints = []
        pattern = re.compile(
            r'@([A-Za-z_][A-Za-z0-9_]*)\.(get|post|put|delete|patch|options|head)\(\s*[\'"]([^\'"]+)[\'"]',
            re.DOTALL
        )

        for file in self.get_source_files(context, ".py"):
            text = file.read_text(encoding="utf-8", errors="ignore")
            router_prefixes = self.find_router_prefixes(text)
            matches = pattern.finditer(text)

            for match in matches:
                router_name = match.group(1)
                router = router_prefixes.get(router_name)
                method = match.group(2).upper()
                path = match.group(3)
                full_path = (router_prefixes.get(router_name, "") + path)
                handler = self.find_handler(text, match.end())

                endpoints.append(
                    ApiEndpoint(
                        framework="FastAPI",
                        router=router,
                        method=method,
                        path=full_path,
                        handler=handler,
                        file=str(file.relative_to(context.repository_root))
                    )
                )
        return endpoints
    
    def detect_flask(self, context):
        endpoints = []

        route_pattern = re.compile(
            r'@([A-Za-z_][A-Za-z0-9_]*)\.route\(\s*[\'"]([^\'"]+)[\'"]([^)]*)\)',
            re.DOTALL
        )

        for file in self.get_source_files(context, ".py"):
            text = file.read_text(encoding="utf-8", errors="ignore")

            if "from flask" not in text.lower() and "import flask" not in text.lower():
                continue

            for match in route_pattern.finditer(text):
                router_name = match.group(1)
                path = match.group(2)
                arguments = match.group(3)
                methods = ["GET"]

                method_match = re.search(
                    r'methods\s*=\s*\[([^\]]+)\]',
                    arguments,
                    re.IGNORECASE
                )

                if method_match:
                    methods = re.findall(
                        r'[\'"]([A-Za-z]+)[\'"]',
                        method_match.group(1)
                    )

                handler = self.find_handler(text, match.end())

                for method in methods:
                    endpoints.append(
                        ApiEndpoint(
                            framework="Flask",
                            router=router_name,
                            method=method.upper(),
                            path=path,
                            handler=handler,
                            file=str(file.relative_to(context.repository_root))
                        )
                    )
        return endpoints

    def find_express_handler(self, text: str, start: int):
        handler_pattern = re.compile(r',\s*([A-Za-z_][A-Za-z0-9_.]*)\s*\);')
        match = handler_pattern.search(text, start)
        if match:
            return match.group(1)
        return "Anonymous"

    def find_express_prefixes(self, text: str):
        prefixes = {}

        pattern = re.compile(
            r'app\.use\(\s*[\'"]([^\'"]+)[\'"]\s*,\s*([A-Za-z_][A-Za-z0-9_]*)',
            re.IGNORECASE
        )
    
        for match in pattern.finditer(text):
            prefix = match.group(1)
            router_var = match.group(2)
    
            prefixes[router_var] = prefix

        return prefixes

    def detect_express(self, context):
        endpoints = []

        pattern = re.compile(
            r'\b(router|app)\.(get|post|put|delete|patch)\(\s*[\'"]([^\'"]*)[\'"]', 
            re.IGNORECASE
        )

        route_prefixes = {}

        for file in self.get_source_files(context, ".js", ".ts"):
            text = file.read_text(encoding="utf-8", errors="ignore")

            route_prefixes.update(
                self.find_express_prefixes(text)
            )

        for file in self.get_source_files(context, ".js", ".ts"):
            text = file.read_text(encoding="utf-8", errors="ignore")

            for match in pattern.finditer(text):
                router_name = match.group(1)
                method = match.group(2).upper()
                path = match.group(3)

                prefix = route_prefixes.get(router_name, "")
                handler = self.find_express_handler(text, match.end())

                endpoints.append(
                    ApiEndpoint(
                        framework="Express",
                        router=router_name,
                        method=method,
                        path=path,
                        handler=handler,
                        file=str(file.relative_to(context.repository_root))
                    )
                )

        return endpoints

    def find_java_handler(self, text: str, start: int):
        pattern = re.compile(r'public\s+[A-Za-z0-9_<>,\[\]]+\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(')
        match = pattern.search(text, start)

        if match:
            return match.group(1)
        return "Unknown"

    def detect_spring_boot(self, context):
        endpoints = []

        class_pattern = re.compile(r'@RequestMapping\(\s*"([^"]*)"\s*\)')

        mapping_pattern = re.compile(
            r'@(Get|Post|Put|Delete|Patch)Mapping(?:\(\s*"([^"]*)"\s*\))?',
            re.IGNORECASE
        )

        for file in self.get_source_files(context, ".java"):
            text = file.read_text(encoding="utf-8", errors="ignore")
            prefix = ""
            class_match = class_pattern.search(text)

            if class_match:
                prefix = class_match.group(1)

            for match in mapping_pattern.finditer(text):
                method = match.group(1).upper()
                path = match.group(2) or ""
                handler = self.find_java_handler(text, match.end())

                endpoints.append(
                    ApiEndpoint(
                        framework="Spring Boot",
                        router=prefix,
                        method=method,
                        path=prefix + path,
                        handler=handler,
                        file=str(file.relative_to(context.repository_root))
                    )
                )
        return endpoints


    def deduplicate_endpoints(self, endpoints: list[ApiEndpoint]) -> list[ApiEndpoint]:
        seen = set()
        unique = []
    
        for endpoint in endpoints:
    
            key = (
                endpoint.framework,
                endpoint.method,
                endpoint.path
            )
    
            if key not in seen:
                seen.add(key)
                unique.append(endpoint)
    
        return unique