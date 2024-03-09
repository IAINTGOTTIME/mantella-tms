"""create account table

Revision ID: 36b7dcb09f95
Revises: 
Create Date: 2024-03-09 16:22:52.687209

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '36b7dcb09f95'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('check_list',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
                              nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('test_case',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('priority', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
                              nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('test_suite',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
                              nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('user',
                    sa.Column('id', sa.Uuid(), nullable=False),
                    sa.Column('username', sa.String(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('hashed_password', sa.String(), nullable=False),
                    sa.Column('is_active', sa.Boolean(), nullable=False),
                    sa.Column('is_superuser', sa.Boolean(), nullable=False),
                    sa.Column('is_verified', sa.Boolean(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
                              nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('check_list_item',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('check_list_id', sa.Integer(), nullable=False),
                    sa.Column('description', sa.String(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
                              nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['check_list_id'], ['check_list.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_check_list_item_check_list_id'), 'check_list_item', ['check_list_id'], unique=False)
    op.create_table('check_list_relationship',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('test_suite_id', sa.Integer(), nullable=False),
                    sa.Column('check_list_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['check_list_id'], ['check_list.id'], ),
                    sa.ForeignKeyConstraint(['test_suite_id'], ['test_suite.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('test_case_relationship',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('test_suite_id', sa.Integer(), nullable=False),
                    sa.Column('test_case_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['test_case_id'], ['test_case.id'], ),
                    sa.ForeignKeyConstraint(['test_suite_id'], ['test_suite.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('test_case_step',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('order', sa.Integer(), nullable=False),
                    sa.Column('description', sa.String(), nullable=False),
                    sa.Column('expected_result', sa.String(), nullable=True),
                    sa.Column('test_case_id', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
                              nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['test_case_id'], ['test_case.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_test_case_step_test_case_id'), 'test_case_step', ['test_case_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_test_case_step_test_case_id'), table_name='test_case_step')
    op.drop_table('test_case_step')
    op.drop_table('test_case_relationship')
    op.drop_table('check_list_relationship')
    op.drop_index(op.f('ix_check_list_item_check_list_id'), table_name='check_list_item')
    op.drop_table('check_list_item')
    op.drop_table('user')
    op.drop_table('test_suite')
    op.drop_table('test_case')
    op.drop_table('check_list')
    # ### end Alembic commands ###
