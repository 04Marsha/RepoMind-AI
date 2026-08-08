from app.models.repository.RepositoryInsights import RepositoryInsights

class InsightsAnalyzer:

    def __init__(self, technology_detector):
        self.technology_detector = technology_detector

    def analyze(self, context) -> RepositoryInsights:
        insights = set()
        technologies = self.technology_detector.detect(context)

        names = {
            tech.name
            for tech in technologies
        }

        if "JWT" in names:
            insights.add("Uses JWT authentication")
        if "MongoDB" in names:
            insights.add("Stores data in MongoDB")
        if "PostgreSQL" in names:
            insights.add("Stores data in PostgreSQL")
        if "Redis" in names:
            insights.add("Uses Redis caching")
        if "Mongoose" in names:
            insights.add("Uses Mongoose for MongoDB object modeling")
        if "Cloudinary" in names:
            insights.add("Stores media files using Cloudinary")
        if "Cloudinary" in names:
            insights.add("Stores media files using Cloudinary")
        if "Angular Material" in names:
            insights.add("Uses Angular Material UI components")
        if "RxJS" in names:
            insights.add("Uses reactive programming through RxJS")
        if "Angular Material" in names:
            insights.add(   "Uses Angular Material UI components")
        if "RxJS" in names:
            insights.add("Uses reactive programming through RxJS")
        if "Scikit Learn" in names:
            insights.add("Machine learning models built using Scikit-Learn")
        if "SHAP" in names:
            insights.add("Provides explainable AI insights using SHAP")
        if "PyTorch" in names:
            insights.add("Deep learning models built using PyTorch")

        return (
            RepositoryInsights(
                insights=list(insights)
            )
        )