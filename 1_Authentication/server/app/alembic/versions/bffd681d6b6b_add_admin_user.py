"""add admin user

Revision ID: bffd681d6b6b
Revises: 148558af9706
Create Date: 2024-08-30 12:15:05.930912

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bffd681d6b6b'
down_revision: Union[str, None] = '148558af9706'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.bulk_insert(
        sa.table('user',
            sa.column('id', sa.Integer),
            sa.column('full_name', sa.String),
            sa.column('email', sa.String),
            sa.column('hashed_password', sa.String),
            sa.column('image', sa.String),
            sa.column('role', sa.Integer),
            sa.column('user_pro', sa.Boolean),
            sa.column('account_type', sa.String),
            sa.column('is_active', sa.Boolean),
        ),
        [
            {
                'id': 1,
                'full_name': 'admin1',
                'email': 'admin1@gmail.com',
                'hashed_password': '$2b$12$kKZwpQuIPwriIW26oC8PwupBF7RH2gwpthF01y6s/jDbOJEWvi73W',
                'image': None,
                'role': 'admin',
                'account_type': 'local',
                'is_active': True,
            },
            {
                'id': 2,
                'full_name': 'user1',
                'email': 'user1@gmail.com',
                'hashed_password': '$2b$12$kKZwpQuIPwriIW26oC8PwupBF7RH2gwpthF01y6s/jDbOJEWvi73W',
                'image': None,
                'role': 'user',
                'account_type': 'local',
                'is_active': False,
            }      
        ]
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
