from pydantic import BaseModel, Field

class Technology(BaseModel):
    name: str
    category: str
    dependency_names: list[str] = Field(default_factory=list)
    config_files: list[str] = Field(default_factory=list)
    import_patterns: list[str] = Field(default_factory=list)

    def matches(self, dependencies, config_files, imports):
        if any(keyword in dependencies for keyword in self.dependency_names):
            return True

        if any(file in config_files for file in self.config_files): 
            return True

        if any(module == pattern or module.startswith(pattern + ".")
               for module in imports
               for pattern in self.import_patterns
            ):
            return True

        return False