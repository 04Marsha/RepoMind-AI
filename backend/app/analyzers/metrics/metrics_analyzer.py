from app.models.metrics.CodeMetrics import CodeMetrics
from app.models.repository.RepositoryContext import RepositoryContext
from app.analyzers.repository.repository_analyzer import RepositoryAnalyzer

COMMENT_PREFIXES = (
    "#",
    "//",
    "/*",
    "*",
    "--",
)

class MetricsAnalyzer:

    def __init__(self, repository_analyzer: RepositoryAnalyzer):
        self.repository_analyzer = repository_analyzer

    def analyze(self, context: RepositoryContext) -> CodeMetrics:
        metrics = CodeMetrics()
        total_lines = 0
        blank_lines = 0
        comment_lines = 0
        code_lines = 0

        metrics.total_files = self.repository_analyzer.count_files(context.project_root)
        metrics.source_files = self.repository_analyzer.count_source_files(context.project_root)
        metrics.total_directories = self.repository_analyzer.count_directories(context.project_root)

        for file in self.repository_analyzer.get_source_files(context.project_root):
            text = self.repository_analyzer.read_file(file)

            if not text:
                continue

            for line in text.splitlines():
                total_lines += 1

                stripped = line.strip()
                if not stripped:
                    blank_lines += 1
                    continue

                if stripped.startswith(COMMENT_PREFIXES):
                    comment_lines += 1
                else:
                    code_lines += 1

        metrics.total_lines = total_lines
        metrics.blank_lines = blank_lines
        metrics.comment_lines = comment_lines
        metrics.code_lines = code_lines

        if metrics.source_files:
            metrics.average_file_size = round(metrics.total_lines / metrics.source_files, 2)
        return metrics