from typing import Dict, Any, List

HLD_PDF_PATH = r"C:\Users\supra\Downloads\HLD.pdf"
LLD_PDF_PATH = r"C:\Users\supra\Downloads\LLD.pdf"

BACKEND_LEARNING_GUIDES: List[Dict[str, Any]] = [
    {
        "id": "backend_caching",
        "title": "Caching Distributed Systems Master Guide",
        "summary": "Caching patterns, invalidation, distributed cache design, and practical trade-offs.",
        "pdf_path": r"C:\Users\supra\Downloads\caching-distributed-systems-master-guide.pdf",
    },
    {
        "id": "backend_database_architecture",
        "title": "Database Architecture Master Guide",
        "summary": "Data modeling, partitioning, indexing, replication, and scaling database systems.",
        "pdf_path": r"C:\Users\supra\Downloads\database-architecture-master-guide.pdf",
    },
    {
        "id": "backend_api_security",
        "title": "API Security Master Guide",
        "summary": "Authentication, authorization, threat modeling, and secure API implementation practices.",
        "pdf_path": r"C:\Users\supra\Downloads\api-security-master-guide.pdf",
    },
    {
        "id": "backend_system_design",
        "title": "System Design Master Guide",
        "summary": "Scalable architecture foundations and end-to-end backend system design techniques.",
        "pdf_path": r"C:\Users\supra\Downloads\system-design-master-guide.pdf",
    },
    {
        "id": "backend_observability_ops",
        "title": "Observability Operations Master Guide",
        "summary": "Monitoring, logging, tracing, and operations playbooks for production systems.",
        "pdf_path": r"C:\Users\supra\Downloads\observability-operations-master-guide.pdf",
    },
    {
        "id": "backend_python_async",
        "title": "Python Async Master Guide",
        "summary": "Async/await patterns, concurrency control, and performance-oriented Python backend design.",
        "pdf_path": r"C:\Users\supra\Downloads\python-async-master-guide.pdf",
    },
]

HLD_BOOK: Dict[str, Any] = {
    "book_id": "hld",
    "title": "System Design Interview: An Insider's Guide",
    "chapters": [
        {
            "id": "hld_ch_01",
            "title": "Scale from Zero to Millions of Users",
            "pdf_page": 5,
            "chapter_goal": "Understand practical scaling steps from a single server to multi-tier architecture.",
            "questions": [],
        },
        {
            "id": "hld_ch_02",
            "title": "Back-of-the-Envelope Estimation",
            "pdf_page": 34,
            "chapter_goal": "Estimate QPS, storage, bandwidth, and machine counts quickly during design discussions.",
            "questions": [],
        },
        {
            "id": "hld_ch_03",
            "title": "A Framework for System Design Interviews",
            "pdf_page": 42,
            "chapter_goal": "Follow a structured approach from requirements to bottleneck analysis.",
            "questions": [],
        },
        {
            "id": "hld_ch_04",
            "title": "Design a Rate Limiter",
            "pdf_page": 51,
            "chapter_goal": "Learn algorithm and storage trade-offs for distributed request limiting.",
            "questions": [],
        },
        {
            "id": "hld_ch_05",
            "title": "Design Consistent Hashing",
            "pdf_page": 71,
            "chapter_goal": "Understand even distribution and minimal reshuffling in distributed systems.",
            "questions": [],
        },
        {
            "id": "hld_ch_06",
            "title": "Design a Key-Value Store",
            "pdf_page": 87,
            "chapter_goal": "Study replication, partitioning, and consistency choices in distributed storage.",
            "questions": [],
        },
        {
            "id": "hld_ch_07",
            "title": "Design a Unique ID Generator in Distributed Systems",
            "pdf_page": 110,
            "chapter_goal": "Compare centralized and decentralized ID generation strategies.",
            "questions": [],
        },
        {
            "id": "hld_ch_08",
            "title": "Design a URL Shortener",
            "pdf_page": 119,
            "chapter_goal": "Build a scalable shortening service with collision-safe key generation.",
            "questions": [],
        },
        {
            "id": "hld_ch_09",
            "title": "Design a Web Crawler",
            "pdf_page": 132,
            "chapter_goal": "Design polite, fault-tolerant crawling and indexing pipelines.",
            "questions": [],
        },
        {
            "id": "hld_ch_10",
            "title": "Design a Notification System",
            "pdf_page": 151,
            "chapter_goal": "Explore fan-out, channel abstraction, and reliability controls for notifications.",
            "questions": [],
        },
        {
            "id": "hld_ch_11",
            "title": "Design a News Feed System",
            "pdf_page": 166,
            "chapter_goal": "Understand feed generation models, ranking, and storage patterns.",
            "questions": [],
        },
        {
            "id": "hld_ch_12",
            "title": "Design a Chat System",
            "pdf_page": 178,
            "chapter_goal": "Cover realtime messaging architecture, presence, and message delivery guarantees.",
            "questions": [],
        },
        {
            "id": "hld_ch_13",
            "title": "Design a Search Autocomplete System",
            "pdf_page": 200,
            "chapter_goal": "Learn data structures and caching strategies for low-latency suggestions.",
            "questions": [],
        },
        {
            "id": "hld_ch_14",
            "title": "Design YouTube",
            "pdf_page": 220,
            "chapter_goal": "Design upload, transcoding, storage, and global streaming delivery.",
            "questions": [],
        },
        {
            "id": "hld_ch_15",
            "title": "Design Google Drive",
            "pdf_page": 244,
            "chapter_goal": "Review sync architecture, metadata management, and consistency in file collaboration.",
            "questions": [],
        },
        {
            "id": "hld_ch_16",
            "title": "The Learning Continues",
            "pdf_page": 264,
            "chapter_goal": "Use a checklist to continue system design practice after the core chapters.",
            "questions": [],
        },
    ],
}

LLD_BOOK: Dict[str, Any] = {
    "book_id": "lld",
    "title": "Head First Design Patterns",
    "chapters": [
        {
            "id": "lld_ch_01",
            "title": "Welcome to Design Patterns: An Introduction",
            "pdf_page": 39,
            "chapter_goal": "Understand composition over inheritance and why patterns improve flexibility.",
            "questions": [],
        },
        {
            "id": "lld_ch_02",
            "title": "Keeping Your Objects in the Know: The Observer Pattern",
            "pdf_page": 70,
            "chapter_goal": "Model publish-subscribe relationships and decouple state changes from consumers.",
            "questions": [],
        },
        {
            "id": "lld_ch_03",
            "title": "Decorating Objects: The Decorator Pattern",
            "pdf_page": 118,
            "chapter_goal": "Add behavior dynamically without creating deep subclass hierarchies.",
            "questions": [],
        },
        {
            "id": "lld_ch_04",
            "title": "Baking with OO Goodness: The Factory Pattern",
            "pdf_page": 148,
            "chapter_goal": "Encapsulate object creation and keep client code independent of concrete types.",
            "questions": [],
        },
        {
            "id": "lld_ch_05",
            "title": "One of a Kind Objects: The Singleton Pattern",
            "pdf_page": 208,
            "chapter_goal": "Ensure single-instance access safely and evaluate global-state trade-offs.",
            "questions": [],
        },
        {
            "id": "lld_ch_06",
            "title": "Encapsulating Invocation: The Command Pattern",
            "pdf_page": 230,
            "chapter_goal": "Represent actions as objects to support queues, undo, and macro operations.",
            "questions": [],
        },
        {
            "id": "lld_ch_07",
            "title": "Being Adaptive: The Adapter and Facade Patterns",
            "pdf_page": 274,
            "chapter_goal": "Integrate incompatible interfaces and simplify complex subsystems.",
            "questions": [],
        },
        {
            "id": "lld_ch_08",
            "title": "Encapsulating Algorithms: The Template Method Pattern",
            "pdf_page": 314,
            "chapter_goal": "Define algorithm skeletons while letting subclasses customize specific steps.",
            "questions": [],
        },
        {
            "id": "lld_ch_09",
            "title": "Well-managed Collections: The Iterator and Composite Patterns",
            "pdf_page": 354,
            "chapter_goal": "Traverse collections uniformly and represent part-whole structures consistently.",
            "questions": [],
        },
        {
            "id": "lld_ch_10",
            "title": "The State of Things: The State Pattern",
            "pdf_page": 424,
            "chapter_goal": "Model behavior changes cleanly as object state transitions.",
            "questions": [],
        },
        {
            "id": "lld_ch_11",
            "title": "Controlling Object Access: The Proxy Pattern",
            "pdf_page": 468,
            "chapter_goal": "Control access with virtual, remote, and protection proxy variants.",
            "questions": [],
        },
        {
            "id": "lld_ch_12",
            "title": "Patterns of Patterns: Compound Patterns",
            "pdf_page": 538,
            "chapter_goal": "Combine patterns in larger designs and reason about collaboration boundaries.",
            "questions": [],
        },
        {
            "id": "lld_ch_13",
            "title": "Patterns in the Real World: Better Living with Patterns",
            "pdf_page": 616,
            "chapter_goal": "Apply pattern thinking across practical design scenarios and legacy code.",
            "questions": [],
        },
        {
            "id": "lld_ch_14",
            "title": "Appendix: Leftover Patterns",
            "pdf_page": 649,
            "chapter_goal": "Review additional patterns and when each one is preferable.",
            "questions": [],
        },
    ],
}


def chapter_ids(book: Dict[str, Any]) -> List[str]:
    return [chapter["id"] for chapter in book["chapters"]]
