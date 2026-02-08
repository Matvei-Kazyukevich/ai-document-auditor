# AI Document Auditor
# Database ER-diagram 

```mermaid
erDiagram

    DOCUMENTS {
        int id PK
        string original_filename
        string storage_path
        string content_type
        bigint size_bytes
        string sha256
        enum status
        string error_message
        datetime created_at
        datetime updated_at
    }

    PARSED_WORKS {
        int id PK
        int document_id FK
        string work_name_raw
        string work_name_norm
        string unit
        decimal quantity
        decimal unit_price
        decimal total_price
        string stage
        string source_section
        int row_index
        datetime created_at
    }

    AUDIT_FINDINGS {
        int id PK
        int document_id FK
        int parsed_work_id FK
        int rule_id FK
        enum risk_type
        enum severity
        string title
        string description
        string recommendation
        datetime created_at
    }

    DOCUMENT_EMBEDDINGS {
        int id PK
        int document_id FK
        int parsed_work_id FK
        string embedding_model
        vector embedding_vector
        datetime created_at
    }

    PROCESSING_LOGS {
        int id PK
        int document_id FK
        string step
        enum status
        string message
        datetime created_at
    }

    REPORTS {
        int id PK
        int document_id FK
        enum report_type
        string storage_path
        datetime created_at
    }

    RULES {
        int id PK
        string code
        string name
        string description
        enum severity
        boolean is_active
        datetime created_at
        datetime updated_at
    }

    RULE_EXECUTIONS {
        int id PK
        int rule_id FK
        int document_id FK
        enum status
        string error_message
        datetime started_at
        datetime finished_at
    }

    SEMANTIC_MATCHES {
        int id PK
        int left_work_id FK
        int right_work_id FK
        decimal similarity_score
        enum match_type
        string embedding_model
        boolean is_accepted
        string accepted_by
        datetime created_at
    }

    ANOMALY_SCORES {
        int id PK
        int document_id FK
        int parsed_work_id FK
        string metric
        decimal score
        decimal threshold
        string model_name
        datetime created_at
    }

    DOCUMENTS ||--o{ PARSED_WORKS : contains
    DOCUMENTS ||--o{ AUDIT_FINDINGS : has
    DOCUMENTS ||--o{ DOCUMENT_EMBEDDINGS : has
    DOCUMENTS ||--o{ PROCESSING_LOGS : logs
    DOCUMENTS ||--o{ REPORTS : generates
    DOCUMENTS ||--o{ RULE_EXECUTIONS : triggers
    DOCUMENTS ||--o{ ANOMALY_SCORES : produces

    PARSED_WORKS ||--o{ AUDIT_FINDINGS : flagged_by
    PARSED_WORKS ||--o{ DOCUMENT_EMBEDDINGS : embedded_as
    PARSED_WORKS ||--o{ SEMANTIC_MATCHES : matched_with
    PARSED_WORKS ||--o{ ANOMALY_SCORES : evaluated_by

    RULES ||--o{ RULE_EXECUTIONS : executed_as
    RULES ||--o{ AUDIT_FINDINGS : referenced_by

    SEMANTIC_MATCHES }o--|| PARSED_WORKS : left_work
    SEMANTIC_MATCHES }o--|| PARSED_WORKS : right_work
