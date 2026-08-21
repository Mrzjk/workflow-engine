"""add Workflow Studio execution trace tables"""
from alembic import op
revision="0002_workflow_traces"; down_revision="0001_initial"; branch_labels=None; depends_on=None
def upgrade():
    op.execute("""CREATE TABLE IF NOT EXISTS workflow_traces (id VARCHAR(36) PRIMARY KEY, workflow_id VARCHAR(36) NOT NULL, workflow_run_id VARCHAR(36) NOT NULL UNIQUE, status VARCHAR(32) NOT NULL, input JSON NOT NULL, output JSON NULL, error TEXT NULL, started_at DATETIME NOT NULL, finished_at DATETIME NULL, FOREIGN KEY(workflow_id) REFERENCES workflows(id), FOREIGN KEY(workflow_run_id) REFERENCES workflow_runs(id))""")
    op.execute("""CREATE TABLE IF NOT EXISTS trace_spans (id VARCHAR(36) PRIMARY KEY, trace_id VARCHAR(36) NOT NULL, node_id VARCHAR(128) NOT NULL, node_type VARCHAR(64) NOT NULL, input JSON NOT NULL, output JSON NULL, status VARCHAR(32) NOT NULL, error TEXT NULL, duration FLOAT NULL, started_at DATETIME NOT NULL, finished_at DATETIME NULL, FOREIGN KEY(trace_id) REFERENCES workflow_traces(id))""")
def downgrade(): op.execute("DROP TABLE IF EXISTS trace_spans"); op.execute("DROP TABLE IF EXISTS workflow_traces")
