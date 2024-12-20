"""Add IoTDevice table

Revision ID: a25ae7d54e70
Revises: fd7030ac4b57
Create Date: 2024-05-26 17:31:51.173441

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a25ae7d54e70'
down_revision: Union[str, None] = 'fd7030ac4b57'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('iot_devices',
    sa.Column('id', sa.String(), autoincrement=False, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('device_type', sa.String(), nullable=True),
    sa.Column('architecture', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_iot_devices_id'), 'iot_devices', ['id'], unique=True)
    op.drop_index('ix_iot_device_settings_device_id', table_name='iot_device_settings')
    op.drop_column('iot_device_settings', 'device_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('iot_device_settings', sa.Column('device_id', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.create_index('ix_iot_device_settings_device_id', 'iot_device_settings', ['device_id'], unique=False)
    op.drop_index(op.f('ix_iot_devices_id'), table_name='iot_devices')
    op.drop_table('iot_devices')
    # ### end Alembic commands ###
