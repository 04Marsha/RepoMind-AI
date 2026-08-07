ENTRY_POINT_FILES = {

    # Python
    "main.py",
    "app.py",
    "server.py",

    # Node
    "index.js",
    "app.js",
    "server.js",

    "index.ts",
    "app.ts",
    "server.ts",

    # Java
    "Application.java",

    # Go
    "main.go",

    # Rust
    "main.rs"
}

EXTENSION_LANGUAGE = {
    ".py": "Python",
    ".java": "Java",
    ".kt": "Kotlin",
    ".kts": "Kotlin",

    ".js": "JavaScript",
    ".jsx": "JavaScript",

    ".ts": "TypeScript",
    ".tsx": "TypeScript",

    ".html": "HTML",
    ".css": "CSS",
    ".scss": "SCSS",
    ".sass": "SASS",
    ".less": "LESS",

    ".go": "Go",
    ".rs": "Rust",
    ".cpp": "C++",
    ".cc": "C++",
    ".cxx": "C++",
    ".c": "C",
    ".h": "C/C++",

    ".cs": "C#",
    ".php": "PHP",
    ".rb": "Ruby",
    ".swift": "Swift",
    ".dart": "Dart",

    ".vue": "Vue",
    ".svelte": "Svelte",

    ".sql": "SQL",
    ".sh": "Shell",
    ".ps1": "PowerShell",

    ".yaml": "YAML",
    ".yml": "YAML",
    ".xml": "XML",
    ".json": "JSON",
    ".toml": "TOML",
}

LANGUAGE_FILES = {
    "requirements.txt": "Python",
    "pyproject.toml": "Python",
    "package.json": "JavaScript/TypeScript",
    "pom.xml": "Java",
    "build.gradle": "Java/Kotlin",
    "go.mod": "Go",
    "Cargo.toml": "Rust",
}

IGNORE_DIRECTORIES = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
    "coverage",
    ".idea",
    ".vscode",
    ".next",
    ".angular",
    "target",
    "out"
}

IGNORE_FILES = {
    ".env.example",
    ".DS_Store",
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "poetry.lock"
}

DOCUMENTATION_FILES = {
    "README.md",
    "README.rst",
    "README.txt",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "LICENSE",
}

CONFIGURATION_FILES = {
    "requirements.txt",
    "pyproject.toml",
    "package.json",
    "package-lock.json",
    "tsconfig.json",
    "angular.json",
    "vite.config.ts",
    "vite.config.js",
    "next.config.js",
    "next.config.ts",
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
    "pom.xml",
    "build.gradle",
    "go.mod",
    "Cargo.toml",
}

DEPENDENCY_FILES = {
    "requirements.txt",
    "pyproject.toml",
    "package.json",
    "pom.xml",
    "build.gradle",
    "go.mod",
    "Cargo.toml",
}

NON_PRIMARY = {
    "HTML",
    "CSS",
    "SCSS",
    "JSON",
    "YAML",
    "XML",
    "Markdown"
}