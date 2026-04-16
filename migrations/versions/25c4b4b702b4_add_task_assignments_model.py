"""Convert task_assignment from association table to full model (SQLite + SQLAlchemy 2.0)

Revision ID: 25c4b4b702b4
Revises: 526fb8b28315
Create Date: 2026-04-14 15:21:40.770175
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

revision = '25c4b4b702b4'
down_revision = '526fb8b28315'

def upgrade():
    conn = op.get_bind()
    
    # 1. Create NEW table with correct schema
    op.create_table('task_assignment_new',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('volunteer_id', sa.Integer(), sa.ForeignKey('volunteers.id'), nullable=True),
        sa.Column('task_id', sa.Integer(), sa.ForeignKey('tasks.id'), nullable=True),
        sa.Index('ix_task_assignment_volunteer_id', 'volunteer_id'),
        sa.Index('ix_task_assignment_task_id', 'task_id')
    )
    
    # 2. Copy data - FIXED with text()
    conn.execute(text("""
        INSERT INTO task_assignment_new (volunteer_id, task_id)
        SELECT volunteer_id, task_id FROM task_assignment
    """))
    
    # 3. Drop old table
    op.drop_table('task_assignment')
    
    # 4. Rename new table
    op.rename_table('task_assignment_new', 'task_assignment')

def downgrade():
    conn = op.get_bind()
    
    # Create old composite PK table
    op.create_table('task_assignment_old',
        sa.Column('volunteer_id', sa.Integer(), sa.ForeignKey('volunteers.id'), primary_key=True),
        sa.Column('task_id', sa.Integer(), sa.ForeignKey('tasks.id'), primary_key=True)
    )
    
    # Copy data back - FIXED with text()
    conn.execute(text("""
        INSERT INTO task_assignment_old (volunteer_id, task_id)
        SELECT volunteer_id, task_id FROM task_assignment
    """))
    
    # Drop new table
    op.drop_table('task_assignment')
    
    # Rename back
    op.rename_table('task_assignment_old', 'task_assignment')