-- Insert data
INSERT INTO roadmaps (id, name, swimlane_column_title)
VALUES (1, 'Database Architecture Roadmap', 'DATABASE CAPABILITIES');

INSERT INTO swimlanes (id, roadmap_id, name, type)
VALUES
    (1, 1, 'Data Modeling', 'PLATFORM'),
    (2, 1, 'Query Optimization', 'INDEPENDENT'),
    (3, 1, 'Replication and Sharding', 'PLATFORM'),
    (4, 1, 'Backup and Recovery', 'INDEPENDENT'),
    (5, 1, 'Security and Encryption', 'PLATFORM');

INSERT INTO events (id, swimlane_id, name, date, type)
VALUES
    (1, 1, 'Implement Data Vault Modeling', '2024-06-30', 'TARGET'),
    (2, 1, 'Adopt Graph Database for Complex Relationships', '2025-12-31', 'DECISION'),
    (3, 2, 'Upgrade to Latest Query Optimizer', '2024-03-31', 'COMPLETED'),
    (4, 2, 'Implement Materialized Views', '2025-09-30', 'TARGET'),
    (5, 3, 'Set up Multi-Region Replication', '2024-09-30', 'COMPLETED'),
    (6, 3, 'Implement Sharding for Horizontal Scalability', '2026-06-30', 'TARGET'),
    (7, 4, 'Implement Continuous Backup Strategy', '2024-12-31', 'TARGET'),
    (8, 4, 'Test Disaster Recovery Plan', '2025-06-30', 'RETIREMENT'),
    (9, 5, 'Enable Column-Level Encryption', '2024-09-30', 'COMPLETED'),
    (10, 5, 'Implement Row-Level Security', '2026-03-31', 'TARGET');