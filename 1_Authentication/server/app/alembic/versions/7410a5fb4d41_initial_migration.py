"""Initial migration

Revision ID: 7410a5fb4d41
Revises: 
Create Date: 2024-08-16 10:35:35.656428

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7410a5fb4d41'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(length=225), nullable=True),
    sa.Column('email', sa.String(length=225), nullable=False),
    sa.Column('hashed_password', sa.String(length=225), nullable=False),
    sa.Column('image', sa.String(length=225), nullable=True),
    sa.Column('role', sa.String(length=225), nullable=False),
    sa.Column('account_type', sa.String(length=225), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_table('item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=225), nullable=True),
    sa.Column('description', sa.String(length=225), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_item_id'), 'item', ['id'], unique=False)
    op.create_index(op.f('ix_item_title'), 'item', ['title'], unique=False)
    op.create_table('token',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('refresh_token', sa.String(length=225), nullable=True),
    sa.Column('exp', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_token_id'), 'token', ['id'], unique=False)
    op.create_index(op.f('ix_token_refresh_token'), 'token', ['refresh_token'], unique=False)
    op.create_table('verify',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('verify_code', sa.String(length=225), nullable=True),
    sa.Column('exp', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_verify_id'), 'verify', ['id'], unique=False)
    op.create_index(op.f('ix_verify_verify_code'), 'verify', ['verify_code'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_verify_verify_code'), table_name='verify')
    op.drop_index(op.f('ix_verify_id'), table_name='verify')
    op.drop_table('verify')
    op.drop_index(op.f('ix_token_refresh_token'), table_name='token')
    op.drop_index(op.f('ix_token_id'), table_name='token')
    op.drop_table('token')
    op.drop_index(op.f('ix_item_title'), table_name='item')
    op.drop_index(op.f('ix_item_id'), table_name='item')
    op.drop_table('item')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###