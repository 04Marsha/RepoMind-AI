from app.models.technology.technology import Technology

TECHNOLOGIES = [

    Technology(
        name="Angular",
        category="frontend_framework",
        dependency_names=["@angular/core"],
        config_files=["angular.json"],
        import_patterns=["@angular/core"]
    ),

    Technology(
        name="React",
        category="frontend_framework",
        dependency_names=["react"],
        import_patterns=["react"]
    ),

    Technology(
        name="FastAPI",
        category="backend_framework",
        dependency_names=["fastapi"],
        import_patterns=["fastapi"]
    ),

    Technology(
        name="Spring Boot",
        category="backend_framework",
        dependency_names=["spring-boot"],
        import_patterns=["org.springframework.boot"]
    ),

    Technology(
        name="MongoDB",
        category="database",
        dependency_names=["mongodb"]
    ),

    Technology(
        name="Mongoose",
        category="orm",
        dependency_names=["mongoose"]
    ),

    Technology(
        name="PostgreSQL",
        category="database",
        dependency_names=["pg", "postgresql", "psycopg2", "psycopg"]
    ),

    Technology(
        name="Redis",
        category="database",
        dependency_names=["redis"]
    ),

    Technology(
        name="Vitest",
        category="testing",
        dependency_names=["vitest"]
    ),

    Technology(
        name="Jest",
        category="testing",
        dependency_names=["jest"]
    ),

    Technology(
        name="Jasmine",
        category="testing",
        dependency_names=["jasmine-core"]
    ),

    Technology(
        name="Karma",
        category="testing",
        dependency_names=["karma"]
    ),

    Technology(
        name="Angular CLI",
        category="build_tool",
        dependency_names=[
            "@angular-devkit/build-angular",
            "@angular/cli"
        ]
    ),

    Technology(
        name="Angular Material",
        category="frontend_library",
        dependency_names=["@angular/material"]
    ),

    Technology(
        name="RxJS",
        category="library",
        dependency_names=["rxjs"]
    ),

    Technology(
        name="Express",
        category="backend_framework",
        dependency_names=["express"]
    ),

    Technology(
        name="Cloudinary",
        category="storage",
        dependency_names=["cloudinary"]
    ),

    Technology(
        name="JWT",
        category="authentication",
        dependency_names=["jsonwebtoken"]
    ),

    Technology(
        name="Multer",
        category="file_upload",
        dependency_names=["multer"]
    ),

    Technology(
        name="Django",
        category="backend_framework",
        dependency_names=["django"],
        import_patterns=["django"]
    ),

    Technology(
        name="FastAPI",
        category="backend_framework",
        dependency_names=["fastapi"],
        import_patterns=["fastapi"]
    ),

    Technology(
        name="Flask",
        category="backend_framework",
        dependency_names=["flask"],
        import_patterns=[
            "from flask import",
            "import flask"
        ]
    ),

    Technology(
        name="Express",
        category="backend_framework",
        dependency_names=["express"]
    ),

    Technology(
        name="Scikit Learn",
        category="machine_learning",
        dependency_names=["scikit-learn", "sklearn"]
    ),

    Technology(
        name="TensorFlow",
        category="machine_learning",
        dependency_names=["tensorflow"]
    ),

    Technology(
        name="PyTorch",
        category="machine_learning",
        dependency_names=["torch"]
    ),

    Technology(
        name="SHAP",
        category="machine_learning",
        dependency_names=["shap"]
    )
]