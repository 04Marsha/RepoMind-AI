from pydantic import BaseModel, Field

class Technology(BaseModel):
    name: str
    category: str
    dependency_names: list[str] = Field(default_factory=list)
    config_files: list[str] = Field(default_factory=list)
    import_patterns: list[str] = Field(default_factory=list)

    def matches(self, dependencies, config_files, imports):
        dependencies = {d.lower() for d in dependencies}
        config_files = {f.lower() for f in config_files}
        imports = {i.lower() for i in imports}

        if any(keyword.lower() in dependencies for keyword in self.dependency_names):
            return True

        if any(file.lower() in config_files for file in self.config_files): 
            return True

        if any(module == pattern.lower() or module.startswith(pattern.lower() + ".")
               for module in imports
               for pattern in self.import_patterns
            ):
            return True

        return False