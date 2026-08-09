from app.models.structure.ProjectStructure import ProjectStructure
from app.analyzers.structure.constants import IMPORTANT_DIRECTORIES
from app.analyzers.repository.constants import CONFIGURATION_FILES, DOCUMENTATION_FILES 


class StructureAnalyzer:

    def analyze(self, context):
        structure = ProjectStructure()

        # GIVES ALL THE DIRECTORIES
        structure.directories = sorted(
            {
                str(folder.relative_to(context.repository_root))
                for folder in context.repository_root.rglob("*")
                if folder.is_dir()
            }
        )

        # GIVES ALL THE IMPORTANT DIRECTORIES
        structure.important_directories = sorted(
            {
                str(folder.relative_to(context.repository_root))
                for folder in context.repository_root.rglob("*")
                if folder.is_dir()
                and folder.name.lower() in IMPORTANT_DIRECTORIES 
            }
        )

        # GIVES ALL CONFIG FILES
        structure.config_files = sorted(
            {
                file.name
                for file in context.repository_root.rglob("*")
                if file.is_file()
                and file.name in CONFIGURATION_FILES
            }
        )

        # GIVES ALL DOCUMENTATION FILES
        structure.documentation_files = sorted(
            {
                file.name
                for file in context.repository_root.rglob("*")
                if file.is_file()
                and file.name in DOCUMENTATION_FILES
            }
        )

        return structure