"""create tasks table

Revision ID: 001_create_tasks_table
Revises: 
Create Date: 2026-09-27 11:44:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001_create_tasks_table'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'tasks',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('task_type', sa.String(length=50), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='queued'),
        sa.Column('payload', postgresql.JSONB(as_text=True), nullable=False),
        sa.Column('result', postgresql.JSONB(as_text=True), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('idx_tasks_status', 'tasks', ['status'])
    op.create_index('idx_tasks_created_at', 'tasks', [sa.text('created_at DESC')])

def downgrade() -> None:
    op.drop_index('idx_tasks_created_at', table_name='tasks')
    op.drop_index('idx_tasks_status', table_name='tasks')
    op.drop_table('tasks')
